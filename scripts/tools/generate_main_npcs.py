"""
주요 NPC 3인 리디자인 — 각각 특징 살린 커스텀 스프라이트
64x16 (4방향 × 16x16)
"""
from PIL import Image, ImageDraw
import os

OUT = "/Users/nddn/Documents/Claude/Projects/IDC game/assets/sprites/characters"
os.makedirs(OUT, exist_ok=True)

def new_sheet():
    img = Image.new("RGBA", (64, 16), (0,0,0,0))
    return img, ImageDraw.Draw(img)

def save(img, name):
    img.save(os.path.join(OUT, name))
    print(f"저장됨: {name}")

# ══════════════════════════════════════
# RATU JOSEFA — 연로한 마을 어른
# 회색 머리, 전통 금색 sulu, 넓은 체형, 지팡이
# ══════════════════════════════════════
img, d = new_sheet()
SKIN     = (140, 95, 60, 255)
SULU_G   = (185, 148, 42, 255)    # 금색 전통 sulu
SULU_GD  = (155, 118, 32, 255)
SULU_PAT = (165, 128, 35, 255)    # 문양
HAIR     = (168, 165, 158, 255)    # 회색 머리
HAIR_D   = (138, 135, 128, 255)
STAFF    = (108, 78, 38, 255)     # 지팡이
NECKLACE = (195, 45, 35, 255)     # 붉은 목걸이 (추장 상징)

for i, facing in enumerate(["down","left","right","up"]):
    ox = i * 16
    d.ellipse([ox+3, 14, ox+13, 16], fill=(0,0,0,55))
    # 넓은 sulu (치마 — 추장답게 넓게)
    d.rectangle([ox+3, 9, ox+13, 14], fill=SULU_G)
    d.rectangle([ox+3, 11, ox+13, 13], fill=SULU_GD)
    # 전통 문양 (대각선)
    for mx in range(ox+4, ox+12, 3):
        d.point((mx, 10), fill=SULU_PAT)
        d.point((mx+1, 12), fill=SULU_PAT)
    # 맨발
    d.point((ox+5, 14), fill=SKIN)
    d.point((ox+10, 14), fill=SKIN)
    # 상체 (맨몸 — 전통, 넓은 어깨)
    d.rectangle([ox+4, 4, ox+12, 9], fill=SKIN)
    # 목걸이 (추장 상징)
    if facing != "up":
        d.line([(ox+6, 6), (ox+10, 6)], fill=NECKLACE)
        d.point((ox+8, 7), fill=NECKLACE)
    # 팔 (넓게)
    d.rectangle([ox+2, 5, ox+4, 9], fill=SKIN)
    d.rectangle([ox+12, 5, ox+14, 9], fill=SKIN)
    # 지팡이 (왼손)
    if facing == "down" or facing == "right":
        d.line([(ox+2, 4), (ox+2, 15)], fill=STAFF, width=1)
        d.point((ox+2, 3), fill=(88, 62, 28, 255))  # 손잡이
    elif facing == "left":
        d.line([(ox+13, 4), (ox+13, 15)], fill=STAFF, width=1)
    # 목
    d.rectangle([ox+7, 2, ox+9, 5], fill=SKIN)
    # 머리 (넓고 회색)
    d.rectangle([ox+5, 0, ox+11, 3], fill=SKIN)
    d.rectangle([ox+5, 0, ox+11, 1], fill=HAIR)
    # 회색 수염 (아래)
    if facing == "down":
        d.point((ox+7, 3), fill=HAIR_D)
        d.point((ox+8, 3), fill=HAIR_D)
        d.point((ox+9, 3), fill=HAIR_D)
        # 눈
        d.point((ox+6, 1), fill=(25, 15, 8, 255))
        d.point((ox+10, 1), fill=(25, 15, 8, 255))
        # 주름 (눈 아래)
        d.point((ox+6, 2), fill=(125, 82, 48, 255))
        d.point((ox+10, 2), fill=(125, 82, 48, 255))
    elif facing == "left":
        d.point((ox+6, 1), fill=(25, 15, 8, 255))
        d.rectangle([ox+5, 0, ox+6, 2], fill=HAIR)
    elif facing == "right":
        d.point((ox+10, 1), fill=(25, 15, 8, 255))
        d.rectangle([ox+10, 0, ox+11, 2], fill=HAIR)
    elif facing == "up":
        d.rectangle([ox+5, 0, ox+11, 2], fill=HAIR)

save(img, "ratu_josefa.png")

# ══════════════════════════════════════
# LANI — 기술에 관심 있는 마을 청년
# 짧은 머리, 작업복(카키), 공구 벨트, 역동적
# ══════════════════════════════════════
img, d = new_sheet()
SKIN     = (155, 105, 68, 255)
WORK_TOP = (105, 128, 95, 255)    # 카키 작업복 상의
WORK_BOT = (88, 108, 78, 255)     # 카키 바지
BELT     = (85, 62, 38, 255)      # 공구 벨트 (갈색)
TOOL     = (165, 165, 172, 255)   # 은색 공구
HAIR     = (15, 10, 5, 255)
BOOT     = (72, 55, 35, 255)      # 작업화

for i, facing in enumerate(["down","left","right","up"]):
    ox = i * 16
    d.ellipse([ox+4, 14, ox+12, 16], fill=(0,0,0,55))
    # 바지
    d.rectangle([ox+5, 10, ox+7, 14], fill=WORK_BOT)
    d.rectangle([ox+9, 10, ox+11, 14], fill=WORK_BOT)
    # 공구 벨트
    d.rectangle([ox+4, 9, ox+12, 11], fill=BELT)
    # 벨트 공구 (왼쪽에 렌치)
    if facing != "up":
        d.rectangle([ox+4, 10, ox+5, 12], fill=TOOL)
    # 작업화
    d.rectangle([ox+4, 13, ox+7, 15], fill=BOOT)
    d.rectangle([ox+9, 13, ox+12, 15], fill=BOOT)
    # 작업복 상의
    d.rectangle([ox+5, 5, ox+11, 9], fill=WORK_TOP)
    # 주머니
    d.rectangle([ox+6, 7, ox+8, 9], fill=(95, 118, 85, 255))
    # 팔
    d.rectangle([ox+3, 6, ox+5, 9], fill=SKIN)
    d.rectangle([ox+11, 6, ox+13, 9], fill=SKIN)
    # 목
    d.rectangle([ox+7, 3, ox+9, 6], fill=SKIN)
    # 머리 (짧은 머리)
    d.rectangle([ox+5, 0, ox+11, 4], fill=SKIN)
    d.rectangle([ox+5, 0, ox+11, 2], fill=HAIR)
    if facing == "down":
        d.point((ox+7, 2), fill=(20, 12, 8, 255))
        d.point((ox+9, 2), fill=(20, 12, 8, 255))
        d.line([ox+7, 3, ox+9, 3], fill=(145, 88, 60, 255))
    elif facing == "left":
        d.rectangle([ox+10, 0, ox+11, 3], fill=HAIR)
        d.point((ox+6, 2), fill=(20, 12, 8, 255))
    elif facing == "right":
        d.rectangle([ox+5, 0, ox+6, 3], fill=HAIR)
        d.point((ox+10, 2), fill=(20, 12, 8, 255))
    elif facing == "up":
        d.rectangle([ox+5, 0, ox+11, 3], fill=HAIR)

save(img, "lani.png")

# ══════════════════════════════════════
# MERE — NGO 현장 활동가
# 긴 머리, 주황 셔츠, 어깨 배낭, 클립보드
# ══════════════════════════════════════
img, d = new_sheet()
SKIN     = (160, 110, 70, 255)
SHIRT    = (205, 88, 42, 255)     # 주황 셔츠
SHIRT_D  = (175, 72, 32, 255)
PANTS    = (58, 85, 55, 255)      # 카키 바지
HAIR     = (12, 8, 5, 255)
HAIR_H   = (28, 20, 12, 255)
BAG      = (68, 95, 62, 255)      # 배낭 끈 (올리브)
BAG_BODY = (55, 78, 48, 255)
CLIP     = (225, 222, 212, 255)   # 클립보드
SHOE     = (95, 68, 42, 255)

for i, facing in enumerate(["down","left","right","up"]):
    ox = i * 16
    d.ellipse([ox+4, 14, ox+12, 16], fill=(0,0,0,55))
    # 바지
    d.rectangle([ox+5, 10, ox+7, 14], fill=PANTS)
    d.rectangle([ox+9, 10, ox+11, 14], fill=PANTS)
    # 신발
    d.rectangle([ox+5, 13, ox+7, 15], fill=SHOE)
    d.rectangle([ox+9, 13, ox+11, 15], fill=SHOE)
    # 셔츠
    d.rectangle([ox+5, 5, ox+11, 10], fill=SHIRT)
    d.rectangle([ox+5, 5, ox+11, 6], fill=SHIRT_D)  # 칼라
    # 배낭 끈 (대각선)
    if facing == "down":
        d.line([(ox+6, 5), (ox+5, 10)], fill=BAG)
        d.line([(ox+10, 5), (ox+11, 10)], fill=BAG)
    elif facing == "up":
        # 배낭 본체 (등에 보임)
        d.rectangle([ox+6, 6, ox+10, 12], fill=BAG_BODY)
        d.rectangle([ox+7, 5, ox+9, 7], fill=BAG_BODY)
    # 팔
    d.rectangle([ox+3, 6, ox+5, 9], fill=SKIN)
    d.rectangle([ox+11, 6, ox+13, 9], fill=SKIN)
    # 클립보드 (오른손에)
    if facing == "down" or facing == "right":
        d.rectangle([ox+12, 6, ox+15, 10], fill=CLIP)
        d.rectangle([ox+12, 6, ox+15, 7], fill=(185, 182, 172, 255))
    # 목
    d.rectangle([ox+7, 3, ox+9, 6], fill=SKIN)
    # 머리 (긴 머리 — 여성)
    d.rectangle([ox+5, 0, ox+11, 4], fill=SKIN)
    d.rectangle([ox+5, 0, ox+11, 1], fill=HAIR)
    if facing == "down":
        d.rectangle([ox+4, 1, ox+6, 7], fill=HAIR)
        d.rectangle([ox+10, 1, ox+12, 7], fill=HAIR)
        d.point((ox+5, 3), fill=HAIR_H)
        d.point((ox+7, 2), fill=(22, 14, 8, 255))
        d.point((ox+9, 2), fill=(22, 14, 8, 255))
        d.point((ox+8, 3), fill=(155, 88, 65, 255))
    elif facing == "left":
        d.rectangle([ox+10, 0, ox+12, 7], fill=HAIR)
        d.point((ox+6, 2), fill=(22, 14, 8, 255))
    elif facing == "right":
        d.rectangle([ox+4, 0, ox+6, 7], fill=HAIR)
        d.point((ox+10, 2), fill=(22, 14, 8, 255))
    elif facing == "up":
        d.rectangle([ox+4, 0, ox+12, 7], fill=HAIR)
        d.point((ox+6, 3), fill=HAIR_H)
        d.point((ox+9, 4), fill=HAIR_H)

save(img, "mere.png")

print("\n주요 NPC 3인 리디자인 완료!")
