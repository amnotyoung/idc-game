# Aid World — 프로젝트 가이드

## 게임 개요
- **장르**: Godot 4 탑다운 2D 내러티브 게임 (한국어)
- **배경**: 피지 수바 + 나이탬바 섬, 수자원 개발 사업
- **주제**: 국제개발협력에서 신뢰·협력·주민 주체성의 중요성
- **플레이 시간**: 1~2시간
- **해상도**: 320×180 픽셀아트

## 핵심 설계 원칙

### 1. 비선형 진행
- 플레이어가 **어떤 순서로든** 수바 거리→정부청사→국제기구→나이탬바를 방문 가능
- 어떤 경로든 True 엔딩 도달 가능해야 함
- 새 기능 추가 시 **5개 경로(A~E) 모두 검증** 필수

### 2. 점수 = 태도, 선물 ≠ 결정적
- 신뢰 점수는 **대화에서의 태도**(경청, 협력, 솔직함)로 결정
- 양고나 종류(뿌리/가루/망고/빈손)는 **분위기 차이만** — 점수 결정적이면 안 됨
- "올바른 선물 사가기"가 게임 핵심이면 국제개발협력이 부정적으로 비춰짐

### 3. 상식적 응대에 패널티 없음
- 나쁜 선택 = **0점 (기회비용만)**, 진짜 나쁜 선택만 감점
- 비슷한 의미의 선택지는 비슷한 점수 (큰 격차 X)
- 실수해도 NPC 대화 보너스 + 메일로 만회 가능

### 4. 현실적 묘사
- 피지는 **상위중소득국** — 낙후 과장 금지, 빈곤포르노 금지
- 문제는 "물이 없음"이 아니라 **"기존 인프라 유지보수 부재"**
- 아동노동 묘사 금지
- 모티브: Lomaiviti 주 외곽 섬 (Bureta 사례 기반)

### 5. 캐릭터 일관성
- Mere는 **사무실에서 퇴장 후 섬에서 재회** — 동시에 두 곳에 존재 불가
- NPC가 "X에게 가봐라" 하면 게임 내에서 **실제로 가서 할 수 있어야** 함
- 등장하지 않는 인물 이름 언급 금지 (예: Seru)

## 기술 구조

### choose() next 체인
- `choose()`에서 `next`가 있으면 **`end()` 호출 안 함** — 대화 내부 직접 전환
- `dialogue_ended`는 **terminal 대화**(choices 없음 or next 없음)에서만 발생
- 핸들러는 반드시 terminal ID만 체크해야 함

### 씬 전환 시 대화 리셋
- `SceneManager.go_to()`에서 `DialogueManager.is_active` 체크 → 강제 종료
- 대화 중 씬 전환 시 freeze 방지

### 입력 처리
- `dialogue_box.gd`는 `_input` 사용 (not `_unhandled_input`)
- 선택지 표시 중 Enter → 포커스된 버튼의 `pressed` 직접 emit
- 선택 후 버튼은 `remove_child()` + `queue_free()`로 즉시 분리

## 주요 캐릭터

| 이름 | 성별 | 소속 | 역할 |
|------|------|------|------|
| 주인공 | 성별 중립 | KODA | 플레이어 |
| Mere | 여 | Pacific Roots NGO | 현장 활동가 |
| Vikash | 남 (Indo-Fijian) | 국가계획부 3층 | ODA 심사 |
| Sela | 여 (iTaukei) | 토지청 5층 | 토지 동의 |
| James | 남 (호주) | APAT | 기술자문 |
| Ratu Josefa | 남 (iTaukei) | 나이탬바 마을 | 추장 |
| Lani | 여 (iTaukei) | 나이탬바 마을 | 청년회 리더 |
| Wati | — | KODA | 현지 직원, 튜토리얼 |

## 신뢰 시스템

### 엔딩 판정 (5명, Wati 제외)
- **True**: 5명 모두 ≥ 70
- **Normal**: 3~4명 ≥ 70
- **Bad**: ≤ 2명 ≥ 70
- 판정 시점: `ch5_resolve` (최종 선택 후)

### 점수 소스 비중
- 기관 협력(Mere+Vikash+James) **61%** : 마을(Ratu+Lani) **38%**
- → 마을만 잘한다고 True 엔딩 안 됨, **게임 전반의 협력이 핵심**

### 만회 메커닉
- 컴퓨터 메일: 만난 이해관계자에게 +3 (랜덤, 반복 가능)
- NPC 대화 보너스: 거리/섬 NPC와 대화 시 관련 이해관계자 +2~3
- 신뢰도별 메일 답장 톤 차이 (0~24 냉담, 25~49 사무적, 50~69 호의적, 70+ 협력적) — HUD `_tier_label`·엔딩 판정(70)과 동일 경계
- HUD: 신뢰 낮은 이해관계자에게 회복 힌트 tooltip, 최근 변화량(±N) 표시

## 동의서 파이프라인

```
Ratu 동의(ch3_good_ending) = 동의서 서명 통합
  ├─ Sela 이미 만남 → 섬에서 한큐 (ch3_ratu_close_good_sign)
  ├─ Sela 안 만남 → 재방문 시 서명 (ch3_consent_ratu)
  └─ Sela 첫 방문 + 이미 서명 → 바로 제출 (ch2_sela_consent_direct)

엔딩 진입: ch4_consent_submitted → KODA 사무실 → 최종 회의
```

## 파일 구조

```
scripts/
  systems/     — trust_manager, dialogue_manager, scene_manager
  player/      — player.gd (걷기70/달리기130, Shift 토글)
  npc/         — npc_base, street_npc
  ui/          — dialogue_box (_input 기반), title_screen
  world/       — chapter1_office, chapter2_government, chapter3_island,
                  chapter4_intl, chapter5_ending, suva_street, building_exit
  tools/       — PIL 배경/스프라이트 생성기

data/dialogues/ — chapter1~5.json, street_npcs.json

scenes/
  ui/          — title_screen, dialogue_box
  world/       — chapter1_office, government_building, naitamba_island,
                  intl_org_office, suva_street, ending_scene
```

## 변경 시 체크리스트

### 대화 수정 시
- [ ] JSON 유효성 (`python3 -c "import json; json.load(open(f))"`)
- [ ] `next` 참조가 존재하는 dialogue ID인지
- [ ] `effects`의 NPC ID가 유효한지
- [ ] `condition` 플래그가 코드에서 `set_flag()`되는지
- [ ] terminal 대화면 `_on_dialogue_ended` 핸들러에 등록됐는지

### 흐름 수정 시
- [ ] 5개 경로(A~E) 시뮬레이션 통과
- [ ] NPC가 언급한 것을 실제로 할 수 있는지
- [ ] 동시에 두 곳에 존재하는 NPC 없는지
- [ ] `ch4_sela_contacted`, `ch3_good_ending`, `ch4_consent_obtained` 등 핵심 플래그 정합성

### 점수 수정 시
- [ ] 전체 밸런스 시뮬레이션 재실행
- [ ] 5명 모두 최적 경로에서 70 이상
- [ ] 선물 종류가 결정적 변수가 되지 않는지
- [ ] 상식적 응대가 패널티받지 않는지
