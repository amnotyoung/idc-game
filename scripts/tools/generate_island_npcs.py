"""
나이탬바 섬 마을 주민 NPC 스프라이트
4캐릭터 × 4방향 (64x16 시트)
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

# ══════════════════════════════════
# 1. 노인 여성 (할머니 — 흰 머리, 꽃무늬 sulu)
# ══════════════════════════════════
img, d = new_sheet()
SKIN = (145, 98, 58, 255)
DRESS = (165, 55, 75, 255)       # 빨강 계열 꽃무늬 드레스
DRESS_F = (225, 175, 55, 255)    # 노란 꽃
HAIR = (195, 192, 188, 255)       # 흰머리
SHOE = (108, 82, 52, 255)

for i, facing in enumerate(["down","left","right","up"]):
    ox = i * 16
    d.ellipse([ox+4, 14, ox+12, 16], fill=(0,0,0,55))
    # 드레스 (긴 치마)
    d.rectangle([ox+4, 8, ox+12, 14], fill=DRESS)
    d.point((ox+6, 10), fill=DRESS_F)
    d.point((ox+10, 12), fill=DRESS_F)
    d.point((ox+8, 9), fill=DRESS_F)
    # 신발
    d.rectangle([ox+5, 13, ox+7, 15], fill=SHOE)
    d.rectangle([ox+9, 13, ox+11, 15], fill=SHOE)
    # 상체
    d.rectangle([ox+5, 5, ox+11, 8], fill=DRESS)
    d.point((ox+7, 6), fill=DRESS_F)
    # 팔
    d.rectangle([ox+3, 6, ox+5, 9], fill=SKIN)
    d.rectangle([ox+11, 6, ox+13, 9], fill=SKIN)
    # 목
    d.rectangle([ox+7, 3, ox+9, 6], fill=SKIN)
    # 머리 (둥글게, 흰머리)
    d.rectangle([ox+5, 0, ox+11, 4], fill=SKIN)
    d.rectangle([ox+5, 0, ox+11, 2], fill=HAIR)
    if facing == "down":
        d.rectangle([ox+4, 1, ox+6, 5], fill=HAIR)
        d.rectangle([ox+10, 1, ox+12, 5], fill=HAIR)
        d.point((ox+7, 2), fill=(20,12,8,255))
        d.point((ox+9, 2), fill=(20,12,8,255))
        d.point((ox+8, 3), fill=(140,85,60,255))
    elif facing == "up":
        d.rectangle([ox+4, 0, ox+12, 5], fill=HAIR)

save(img, "npc_island_elder.png")

# ══════════════════════════════════
# 2. 아이 (작은 체형 — 반바지, 맨발)
# ══════════════════════════════════
img, d = new_sheet()
SKIN = (160, 112, 72, 255)
SHIRT = (85, 165, 195, 255)      # 하늘색 티셔츠
SHORTS = (60, 95, 55, 255)       # 초록 반바지
HAIR = (15, 10, 5, 255)

for i, facing in enumerate(["down","left","right","up"]):
    ox = i * 16
    d.ellipse([ox+5, 14, ox+11, 16], fill=(0,0,0,40))
    # 아이는 작게 (y 오프셋 +3)
    BY = 3
    # 반바지
    d.rectangle([ox+6, 10+BY, ox+10, 13+BY], fill=SHORTS)
    # 맨발
    d.point((ox+6, 13+BY), fill=SKIN)
    d.point((ox+9, 13+BY), fill=SKIN)
    # 티셔츠
    d.rectangle([ox+6, 7+BY, ox+10, 10+BY], fill=SHIRT)
    # 팔
    d.rectangle([ox+5, 7+BY, ox+6, 9+BY], fill=SKIN)
    d.rectangle([ox+10, 7+BY, ox+11, 9+BY], fill=SKIN)
    # 목
    d.rectangle([ox+7, 5+BY, ox+9, 7+BY], fill=SKIN)
    # 머리 (둥글고 큰 — 아이 비율)
    d.rectangle([ox+6, 2+BY, ox+10, 6+BY], fill=SKIN)
    d.rectangle([ox+6, 2+BY, ox+10, 3+BY], fill=HAIR)
    if facing == "down":
        d.point((ox+7, 4+BY), fill=(20,12,8,255))
        d.point((ox+9, 4+BY), fill=(20,12,8,255))
        d.point((ox+8, 5+BY), fill=(145,88,65,255))
    elif facing == "up":
        d.rectangle([ox+6, 2+BY, ox+10, 5+BY], fill=HAIR)

save(img, "npc_island_child.png")

# ══════════════════════════════════
# 3. 청년 어부 (근육질, sulu, 맨발)
# ══════════════════════════════════
img, d = new_sheet()
SKIN = (152, 105, 65, 255)
SULU = (42, 68, 118, 255)        # 파란 sulu
SULU_L = (55, 82, 135, 255)
HAIR = (18, 12, 5, 255)

for i, facing in enumerate(["down","left","right","up"]):
    ox = i * 16
    d.ellipse([ox+4, 14, ox+12, 16], fill=(0,0,0,55))
    # sulu
    d.rectangle([ox+4, 9, ox+12, 14], fill=SULU)
    d.line([(ox+7, 9), (ox+7, 14)], fill=SULU_L)
    d.line([(ox+10, 9), (ox+10, 14)], fill=SULU_L)
    # 맨발
    d.point((ox+5, 14), fill=SKIN)
    d.point((ox+10, 14), fill=SKIN)
    # 상체 (맨몸 — 어부)
    d.rectangle([ox+5, 5, ox+11, 9], fill=SKIN)
    # 팔 (넓게)
    d.rectangle([ox+3, 5, ox+5, 9], fill=SKIN)
    d.rectangle([ox+11, 5, ox+13, 9], fill=SKIN)
    # 목
    d.rectangle([ox+7, 3, ox+9, 6], fill=SKIN)
    # 머리
    d.rectangle([ox+5, 0, ox+11, 4], fill=SKIN)
    d.rectangle([ox+5, 0, ox+11, 2], fill=HAIR)
    if facing == "down":
        d.point((ox+7, 2), fill=(20,12,8,255))
        d.point((ox+9, 2), fill=(20,12,8,255))
        d.line([ox+7, 3, ox+9, 3], fill=(140,85,60,255))
    elif facing == "up":
        d.rectangle([ox+5, 0, ox+11, 3], fill=HAIR)

save(img, "npc_island_fisher.png")

# ══════════════════════════════════
# 4. 중년 여성 (시장 차림, 바구니 든)
# ══════════════════════════════════
img, d = new_sheet()
SKIN = (155, 108, 68, 255)
DRESS = (55, 135, 95, 255)       # 초록 드레스
DRESS_F = (195, 175, 55, 255)    # 노란 무늬
HAIR = (15, 10, 5, 255)
BASKET = (175, 138, 82, 255)     # 바구니

for i, facing in enumerate(["down","left","right","up"]):
    ox = i * 16
    d.ellipse([ox+4, 14, ox+12, 16], fill=(0,0,0,55))
    # 드레스
    d.rectangle([ox+4, 8, ox+12, 14], fill=DRESS)
    d.point((ox+6, 10), fill=DRESS_F)
    d.point((ox+9, 12), fill=DRESS_F)
    # 샌들
    d.rectangle([ox+5, 13, ox+7, 15], fill=(118, 88, 55, 255))
    d.rectangle([ox+9, 13, ox+11, 15], fill=(118, 88, 55, 255))
    # 상체
    d.rectangle([ox+5, 5, ox+11, 8], fill=DRESS)
    # 팔 + 바구니 (오른쪽에)
    d.rectangle([ox+3, 6, ox+5, 9], fill=SKIN)
    d.rectangle([ox+11, 6, ox+13, 9], fill=SKIN)
    # 바구니 (오른쪽 팔에)
    if facing != "up":
        d.rectangle([ox+12, 6, ox+15, 10], fill=BASKET)
        d.rectangle([ox+12, 6, ox+15, 7], fill=(155, 118, 68, 255))
    # 목
    d.rectangle([ox+7, 3, ox+9, 6], fill=SKIN)
    # 머리 (긴 머리)
    d.rectangle([ox+5, 0, ox+11, 4], fill=SKIN)
    d.rectangle([ox+5, 0, ox+11, 2], fill=HAIR)
    if facing == "down":
        d.rectangle([ox+4, 1, ox+6, 6], fill=HAIR)
        d.rectangle([ox+10, 1, ox+12, 6], fill=HAIR)
        d.point((ox+7, 2), fill=(20,12,8,255))
        d.point((ox+9, 2), fill=(20,12,8,255))
    elif facing == "up":
        d.rectangle([ox+4, 0, ox+12, 6], fill=HAIR)
    elif facing == "left":
        d.rectangle([ox+10, 1, ox+12, 6], fill=HAIR)
    elif facing == "right":
        d.rectangle([ox+4, 1, ox+6, 6], fill=HAIR)

save(img, "npc_island_woman.png")

print("\n나이탬바 NPC 4종 완료!")
