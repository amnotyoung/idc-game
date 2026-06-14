#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""대화-핸들러 정합성 전수 감사 (읽기 전용, 게임 파일 수정 안 함)."""
import json, re, glob, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DIA_DIR = os.path.join(ROOT, "data", "dialogues")
GD_DIRS = [os.path.join(ROOT, "scripts", "world"), os.path.join(ROOT, "scripts", "systems")]

# trust_manager 의 신뢰 대상 키 (modify 가 받는 유효 id)
TRUST_KEYS = {"timoci", "ratu_josefa", "mere", "james", "lani", "wati"}

# 코드가 런타임에 dialogues[...] 로 주입하는 노드 (JSON 밖)
RUNTIME_NODES = {"ch1_email_result", "ch5_report"}

# ---- 1. JSON 대화 로드 ----
nodes = {}          # id -> node dict
node_file = {}      # id -> 파일명
for path in sorted(glob.glob(os.path.join(DIA_DIR, "*.json"))):
    data = json.load(open(path, encoding="utf-8"))
    for nid, node in data.items():
        if nid in nodes:
            print(f"[중복 ID] {nid} ({os.path.basename(path)} 와 {node_file[nid]})")
        nodes[nid] = node
        node_file[nid] = os.path.basename(path)

all_ids = set(nodes) | RUNTIME_NODES

# ---- 2. JSON 내부 참조 수집 ----
next_refs = []      # (src_id, next_id)
cond_flags = set()  # condition 플래그
effect_ids = []     # (src_id, npc_id)
for nid, node in nodes.items():
    for ch in node.get("choices", []):
        nx = ch.get("next", "")
        if nx:
            next_refs.append((nid, nx))
        cond = ch.get("condition", "")
        if cond:
            cond_flags.add(cond)
        for npc in ch.get("effects", {}):
            effect_ids.append((nid, npc))

# ---- 3. GD 핸들러에서 문자열/플래그 수집 ----
gd_text = ""
for d in GD_DIRS:
    for path in sorted(glob.glob(os.path.join(d, "*.gd"))):
        gd_text += "\n" + open(path, encoding="utf-8").read()

set_flags   = set(re.findall(r'set_flag\("([^"]+)"\)', gd_text))
has_flags   = set(re.findall(r'has_flag\("([^"]+)"\)', gd_text))
start_calls = set(re.findall(r'\.start\("([^"]+)"\)', gd_text))
# NPC 대사 지정 + 대화 스왑 + dialogues 주입/참조
did_assign  = set(re.findall(r'dialogue_id\s*=\s*"([^"]+)"', gd_text))
cur_assign  = set(re.findall(r'current_dialogue_id\s*=\s*"([^"]+)"', gd_text))
dict_ref    = set(re.findall(r'dialogues\["([^"]+)"\]', gd_text))
# _on_dialogue_ended 가 처리하는 terminal id (match/== 문자열) — 광역 수집
handled_ids = set(re.findall(r'==\s*"([^"]+)"', gd_text)) | \
              set(re.findall(r'"((?:ch|street|island|bula|hindi|police)[^"]*)"\s*[:,]', gd_text))

gd_referenced = start_calls | did_assign | cur_assign | dict_ref

print("=" * 70)
print("대화-핸들러 정합성 감사")
print("=" * 70)
print(f"JSON 노드 {len(nodes)}개 / 핸들러 set_flag {len(set_flags)}종 / has_flag {len(has_flags)}종")

def section(t): print(f"\n----- {t} -----")

# ---- 검사 1: 깨진 next 참조 ----
section("1. 깨진 next 참조 (대화 내부)")
bad = [(s, n) for s, n in next_refs if n not in all_ids]
for s, n in bad: print(f"  ✗ {s} → next:'{n}' (존재하지 않음)")
if not bad: print("  ✓ 모든 next 참조 유효")

# ---- 검사 2: 점수 증발 (잘못된 effects npc_id) ----
section("2. effects npc_id 유효성 (trust_manager 키와 대조)")
bad = [(s, n) for s, n in effect_ids if n not in TRUST_KEYS]
for s, n in sorted(set(bad)): print(f"  ✗ {s} effects:'{n}' → modify 가 무시 = 점수 증발")
if not bad: print("  ✓ 모든 effects npc_id 유효")

# ---- 검사 3: 핸들러가 start/지정하는 id 가 JSON 에 있나 ----
section("3. 핸들러 참조 id 유효성 (start / dialogue_id / dialogues[])")
bad = sorted(i for i in gd_referenced if i not in all_ids)
for i in bad: print(f"  ✗ 핸들러가 '{i}' 참조하지만 JSON/런타임에 없음")
if not bad: print("  ✓ 핸들러가 참조하는 모든 대화 id 존재")

# ---- 검사 4: condition 플래그가 코드에서 set 되나 ----
section("4. condition 플래그 set 여부")
bad = sorted(f for f in cond_flags if f not in set_flags)
for f in bad: print(f"  ✗ condition '{f}' → set_flag 호출 없음 = 선택지 영원히 안 뜸")
if not bad: print(f"  ✓ 모든 condition 플래그({sorted(cond_flags)}) set 됨")

# ---- 검사 5: has_flag 로 읽지만 set 안 되는 플래그 ----
section("5. has_flag 로 읽지만 set_flag 없는 플래그 (죽은 분기)")
bad = sorted(f for f in has_flags if f not in set_flags)
for f in bad: print(f"  ✗ has_flag('{f}') 체크하지만 아무도 set 안 함 → 항상 false")
if not bad: print("  ✓ 읽는 모든 플래그가 set 됨")

# ---- 검사 6: set 하지만 아무도 안 읽는 플래그 (불용) ----
# condition(대화 JSON)으로 쓰이는 플래그는 has_flag 없이도 "사용 중"으로 인정
section("6. set 하지만 안 읽는 플래그 (has_flag·condition 모두 미사용 = 진짜 불용)")
bad = sorted(f for f in set_flags if f not in has_flags and f not in cond_flags)
for f in bad: print(f"  · set_flag('{f}') 하지만 has_flag 체크 없음")
if not bad: print("  ✓ 없음")

# ---- 검사 7: 고아 노드 (아무도 도달 못 함) ----
section("7. 고아 노드 (next/start/dialogue_id 어디서도 참조 안 됨)")
reachable = {n for _, n in next_refs} | gd_referenced
# 명백한 진입점(핸들러 start)과 런타임 노드는 제외
entrypoints = start_calls | RUNTIME_NODES
orphans = sorted(i for i in nodes if i not in reachable and i not in entrypoints)
for i in orphans: print(f"  ? {i} ({node_file[i]}) — 도달 경로 불명")
if not orphans: print("  ✓ 고아 노드 없음")

# ---- 검사 8: terminal 노드인데 핸들러 미처리 (참고용 휴리스틱) ----
section("8. terminal 노드(choices 없음) 중 핸들러가 언급 안 하는 것")
print("   (대부분 정상 — 단순 안내 대사. '진행이 멈추면 안 되는' 노드만 주의)")
terminals = [i for i, n in nodes.items() if not n.get("choices")]
unhandled = sorted(i for i in terminals if i not in handled_ids and i not in gd_referenced)
# 너무 많으면 압축: 핸들러가 start 하거나 dialogue_id 로 쓰는 건 정상이므로 위 gd_referenced 로 이미 걸러짐
for i in unhandled:
    print(f"  · {i} ({node_file[i]})")
print(f"   terminal 총 {len(terminals)}개 중 핸들러 무언급 {len(unhandled)}개")
