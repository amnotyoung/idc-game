"""
Aid World — 타이틀 화면 배경
320×180 픽셀아트
구성: 나이탬바 섬 전경 + 주인공 뒷모습 + 이해관계자 실루엣 + 피지 요소
"""
from PIL import Image, ImageDraw
import os

OUT = "/Users/nddn/Documents/Claude/Projects/IDC game/assets/sprites/tilesets"
os.makedirs(OUT, exist_ok=True)

W, H = 320, 180
img = Image.new("RGBA", (W, H))
d = ImageDraw.Draw(img)

# ═══════════════════════════════════
# 팔레트
# ═══════════════════════════════════
# 석양 하늘 (오렌지~보라 그라디언트)
SKY_TOP    = (45, 35, 82)       # 짙은 보라
SKY_MID    = (145, 75, 95)      # 분홍빛
SKY_BOT    = (225, 148, 68)     # 주황
SUN_COL    = (248, 205, 95)     # 태양
SUN_GLOW   = (255, 225, 135)
CLOUD_COL  = (195, 135, 105)    # 석양 구름

# 바다
SEA_DARK   = (28, 58, 95)
SEA_MID    = (42, 82, 125)
SEA_LIGHT  = (65, 108, 155)
SEA_REFL   = (195, 145, 85)     # 석양 반사

# 섬
ISLAND_DARK  = (22, 55, 28)
ISLAND_MID   = (35, 78, 38)
ISLAND_LIGHT = (52, 105, 48)

# 모래
SAND = (195, 172, 118)
SAND_D = (165, 145, 98)

# 야자수
PALM_TRK = (55, 38, 18)
PALM_LF  = (28, 65, 25)
PALM_LFD = (18, 48, 15)

# 캐릭터 색상
PLAYER_HAIR  = (30, 20, 10)
PLAYER_SHIRT = (30, 80, 160)     # KODA 파란 셔츠
PLAYER_PANTS = (50, 50, 75)
PLAYER_SKIN  = (200, 160, 115)

# 실루엣 (이해관계자들 — 어두운 톤)
SIL_BASE = (25, 25, 35)
SIL_LIGHT = (45, 42, 55)

# 텍스트
TEXT_COL = (248, 242, 225)
TEXT_SHADOW = (35, 28, 22)

# ═══════════════════════════════════
# 1. 석양 하늘 그라디언트
# ═══════════════════════════════════
for y in range(100):
    t = y / 100
    if t < 0.4:
        # 보라 → 분홍
        s = t / 0.4
        r = int(SKY_TOP[0] + (SKY_MID[0] - SKY_TOP[0]) * s)
        g = int(SKY_TOP[1] + (SKY_MID[1] - SKY_TOP[1]) * s)
        b = int(SKY_TOP[2] + (SKY_MID[2] - SKY_TOP[2]) * s)
    else:
        # 분홍 → 주황
        s = (t - 0.4) / 0.6
        r = int(SKY_MID[0] + (SKY_BOT[0] - SKY_MID[0]) * s)
        g = int(SKY_MID[1] + (SKY_BOT[1] - SKY_MID[1]) * s)
        b = int(SKY_MID[2] + (SKY_BOT[2] - SKY_MID[2]) * s)
    d.line([0, y, W-1, y], fill=(r, g, b, 255))

# ═══════════════════════════════════
# 2. 태양 (수평선 근처, 우측)
# ═══════════════════════════════════
SUN_CX, SUN_CY = 248, 82
# 글로우
for gr in range(22, 6, -2):
    alpha = 60 - gr * 2
    d.ellipse([SUN_CX-gr, SUN_CY-gr, SUN_CX+gr, SUN_CY+gr],
              fill=(SUN_GLOW[0], SUN_GLOW[1], SUN_GLOW[2], alpha))
# 태양 본체
d.ellipse([SUN_CX-8, SUN_CY-8, SUN_CX+8, SUN_CY+8], fill=(*SUN_COL, 255))
d.ellipse([SUN_CX-6, SUN_CY-6, SUN_CX+6, SUN_CY+6], fill=(*SUN_GLOW, 255))

# ═══════════════════════════════════
# 3. 석양 구름
# ═══════════════════════════════════
clouds = [(30, 35, 55, 12), (100, 28, 48, 10), (185, 42, 40, 8),
          (270, 32, 35, 10), (55, 55, 42, 9), (220, 50, 38, 8)]
for cx, cy, cw, ch in clouds:
    d.ellipse([cx, cy, cx+cw, cy+ch], fill=(*CLOUD_COL, 120))
    d.ellipse([cx+3, cy-2, cx+cw-2, cy+ch-2], fill=(*CLOUD_COL, 80))

# ═══════════════════════════════════
# 4. 원경 섬 실루엣 (나이탬바)
# ═══════════════════════════════════
# 뒷 산
island_far = [
    (0, 98), (0, 88), (25, 78), (55, 72), (80, 68),
    (110, 65), (140, 70), (170, 64), (200, 68), (230, 72),
    (260, 76), (290, 80), (320, 85), (320, 98)
]
d.polygon(island_far, fill=(*ISLAND_DARK, 255))

# 앞 산
island_mid = [
    (0, 98), (0, 82), (20, 78), (45, 74), (70, 72),
    (100, 68), (120, 72), (150, 75), (180, 70), (210, 74),
    (240, 78), (280, 82), (310, 86), (320, 88), (320, 98)
]
d.polygon(island_mid, fill=(*ISLAND_MID, 255))

# 밝은 초목
island_front = [
    (0, 98), (0, 90), (30, 86), (60, 84), (90, 88),
    (120, 85), (150, 82), (180, 86), (210, 84), (240, 88),
    (270, 86), (300, 90), (320, 88), (320, 98)
]
d.polygon(island_front, fill=(*ISLAND_LIGHT, 255))

# ═══════════════════════════════════
# 5. 야자수 3그루 (섬 위)
# ═══════════════════════════════════
def palm(px, py, h=22, lean=3):
    for i in range(h):
        ox = int(i * lean / h)
        d.rectangle([px+ox, py-i, px+ox+1, py-i+1], fill=(*PALM_TRK, 255))
    top_x, top_y = px + lean, py - h
    leaves = [(-12,-6,10,4), (-8,-10,7,3), (0,-12,12,4),
              (6,-8,12,3), (-3,-5,9,5), (-10,-3,8,4)]
    for lx, ly, lw, lh in leaves:
        d.ellipse([top_x+lx, top_y+ly, top_x+lx+lw, top_y+ly+lh], fill=(*PALM_LF, 255))
    for lx, ly, lw, lh in leaves[1::2]:
        d.ellipse([top_x+lx+1, top_y+ly+1, top_x+lx+lw-1, top_y+ly+lh-1], fill=(*PALM_LFD, 255))
    # 코코넛
    for ox2, oy2 in [(-1,-3),(2,-2),(-3,-1)]:
        d.ellipse([top_x+ox2, top_y+oy2, top_x+ox2+3, top_y+oy2+3], fill=(65,48,25,255))

palm(48, 88, 24, 3)
palm(155, 82, 20, -2)
palm(275, 86, 18, 2)

# ═══════════════════════════════════
# 6. 전통 부레(bure) 오두막 실루엣
# ═══════════════════════════════════
# 벽
d.rectangle([130, 80, 170, 95], fill=(*SIL_BASE, 200))
# 지붕
d.polygon([125, 80, 150, 65, 175, 80], fill=(*SIL_BASE, 220))

# ═══════════════════════════════════
# 7. 바다
# ═══════════════════════════════════
for y in range(98, H):
    t = (y - 98) / (H - 98)
    r = int(SEA_DARK[0] + (SEA_MID[0] - SEA_DARK[0]) * t)
    g = int(SEA_DARK[1] + (SEA_MID[1] - SEA_DARK[1]) * t)
    b = int(SEA_DARK[2] + (SEA_MID[2] - SEA_DARK[2]) * t)
    d.line([0, y, W-1, y], fill=(r, g, b, 255))

# 석양 반사 (태양 아래 수면)
for y in range(100, H, 3):
    width = max(2, 18 - (y - 100) // 4)
    x_center = SUN_CX + (y - 100) // 8
    alpha = max(30, 140 - (y - 100) * 2)
    d.line([x_center - width, y, x_center + width, y],
           fill=(SEA_REFL[0], SEA_REFL[1], SEA_REFL[2], alpha))

# 잔물결
for y in range(102, H, 4):
    for x in range(10, W-10, 18):
        d.line([x, y, x+8, y], fill=(*SEA_LIGHT, 100))

# ═══════════════════════════════════
# 8. 모래사장 (하단 전경)
# ═══════════════════════════════════
sand_line = [
    (0, H), (0, 148), (15, 145), (40, 142), (70, 140),
    (100, 138), (130, 136), (160, 135), (190, 136),
    (220, 138), (250, 140), (280, 142), (310, 145), (320, 148), (320, H)
]
d.polygon(sand_line, fill=(*SAND, 255))
# 모래 텍스처
for x in range(0, W, 6):
    for y in range(140, H, 4):
        if (x + y) % 12 < 3:
            d.point((x, y), fill=(*SAND_D, 255))

# ═══════════════════════════════════
# 9. 주인공 뒷모습 (중앙, 바다를 바라보며)
# ═══════════════════════════════════
PX, PY = 160, 128  # 발 위치

# 다리
d.rectangle([PX-3, PY-8, PX-1, PY], fill=(*PLAYER_PANTS, 255))
d.rectangle([PX+1, PY-8, PX+3, PY], fill=(*PLAYER_PANTS, 255))
# 신발
d.rectangle([PX-4, PY, PX, PY+2], fill=(35, 28, 18, 255))
d.rectangle([PX+1, PY, PX+4, PY+2], fill=(35, 28, 18, 255))
# 셔츠
d.rectangle([PX-5, PY-16, PX+5, PY-8], fill=(*PLAYER_SHIRT, 255))
# 팔
d.rectangle([PX-7, PY-15, PX-5, PY-10], fill=(*PLAYER_SKIN, 255))
d.rectangle([PX+5, PY-15, PX+7, PY-10], fill=(*PLAYER_SKIN, 255))
# 목
d.rectangle([PX-1, PY-19, PX+1, PY-16], fill=(*PLAYER_SKIN, 255))
# 머리 (뒷모습)
d.rectangle([PX-4, PY-25, PX+4, PY-18], fill=(*PLAYER_HAIR, 255))

# ═══════════════════════════════════
# 10. 이해관계자 실루엣들 (양옆에 서 있는)
# ═══════════════════════════════════
def silhouette(sx, sy, features=None):
    """간단한 인물 실루엣"""
    # 다리
    d.rectangle([sx-2, sy-6, sx, sy], fill=(*SIL_BASE, 220))
    d.rectangle([sx+1, sy-6, sx+3, sy], fill=(*SIL_BASE, 220))
    # 몸
    d.rectangle([sx-3, sy-13, sx+4, sy-6], fill=(*SIL_BASE, 220))
    # 머리
    d.rectangle([sx-2, sy-19, sx+3, sy-13], fill=(*SIL_BASE, 220))

    if features == "ratu":
        # 지팡이
        d.line([(sx-5, sy-18), (sx-5, sy+1)], fill=(*SIL_LIGHT, 200))
        # 넓은 어깨
        d.rectangle([sx-5, sy-13, sx+6, sy-10], fill=(*SIL_BASE, 220))
        # 회색 머리 하이라이트
        d.rectangle([sx-2, sy-19, sx+3, sy-17], fill=(*SIL_LIGHT, 180))
    elif features == "mere":
        # 긴 머리
        d.rectangle([sx-4, sy-17, sx-2, sy-10], fill=(*SIL_BASE, 220))
        d.rectangle([sx+3, sy-17, sx+5, sy-10], fill=(*SIL_BASE, 220))
        # 배낭
        d.rectangle([sx-1, sy-12, sx+2, sy-8], fill=(*SIL_LIGHT, 150))
    elif features == "lani":
        # 공구 벨트
        d.rectangle([sx-3, sy-7, sx+4, sy-6], fill=(*SIL_LIGHT, 180))
    elif features == "timoci":
        # 넥타이 느낌
        d.line([(sx+1, sy-13), (sx+1, sy-8)], fill=(*SIL_LIGHT, 160))
    elif features == "james":
        # 서류
        d.rectangle([sx+4, sy-11, sx+7, sy-8], fill=(*SIL_LIGHT, 160))

# 왼쪽 그룹: Ratu, Lani
silhouette(55, 148, "ratu")
silhouette(78, 150, "lani")

# 오른쪽 그룹: Mere, Timoci, James
silhouette(235, 148, "mere")
silhouette(258, 150, "timoci")
silhouette(280, 149, "james")

# ═══════════════════════════════════
# 11. 피지 요소: 양고나 그릇 (모래 위 하단)
# ═══════════════════════════════════
# 타노아(양고나 그릇) — 중앙 하단
TX, TY = 160, 168
d.ellipse([TX-8, TY-3, TX+8, TY+3], fill=(95, 62, 32, 255))
d.ellipse([TX-6, TY-2, TX+6, TY+1], fill=(115, 78, 42, 255))
# 다리
d.rectangle([TX-9, TY+2, TX-7, TY+5], fill=(78, 52, 25, 255))
d.rectangle([TX+7, TY+2, TX+9, TY+5], fill=(78, 52, 25, 255))

# ═══════════════════════════════════
# 12. 타이틀 텍스트 영역 (상단)
# ═══════════════════════════════════
# "AID WORLD" — 픽셀 블록 문자
# 간단히 큰 블록으로 표현 (5x7 폰트 느낌)
title_y = 12
# 그림자
for dx, dy in [(1,1)]:
    # A
    for px2, py2 in [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),
                     (1,0),(2,0),(3,0),(1,3),(2,3),(3,3),
                     (3,0),(3,1),(3,2),(3,3),(3,4),(3,5),(3,6)]:
        d.rectangle([82+px2*3+dx, title_y+py2*3+dy, 82+px2*3+2+dx, title_y+py2*3+2+dy],
                    fill=(*TEXT_SHADOW, 200))

# 실제로 PIL에서 픽셀 폰트 그리기는 복잡하므로
# 대신 단순한 블록 텍스트를 사용
# "AID WORLD" 를 두꺼운 라인으로
# 상단 중앙에 반투명 배너
d.rectangle([60, 8, 260, 35], fill=(0, 0, 0, 100))
# 타이틀 — 블록 단위로
# "AID" 부분
letters_aid = [
    # A (x offset = 0)
    [(0,6),(0,5),(0,4),(0,3),(0,2),(0,1),(1,0),(2,0),(3,0),(3,1),(3,2),(3,3),(3,4),(3,5),(3,6),(1,3),(2,3)],
    # I (x offset = 5)
    [(5,0),(6,0),(7,0),(6,1),(6,2),(6,3),(6,4),(6,5),(6,6),(5,6),(7,6)],
    # D (x offset = 9)
    [(9,0),(9,1),(9,2),(9,3),(9,4),(9,5),(9,6),(10,0),(11,0),(12,1),(12,2),(12,3),(12,4),(12,5),(11,6),(10,6)],
]
# "WORLD" 부분
letters_world = [
    # W (x offset = 0)
    [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(1,6),(2,5),(2,4),(3,6),(4,5),(4,4),(4,3),(4,2),(4,1),(4,0)],
    # O (x offset = 6)
    [(7,0),(8,0),(6,1),(6,2),(6,3),(6,4),(6,5),(7,6),(8,6),(9,1),(9,2),(9,3),(9,4),(9,5)],
    # R (x offset = 11)
    [(11,0),(11,1),(11,2),(11,3),(11,4),(11,5),(11,6),(12,0),(13,0),(14,1),(14,2),(13,3),(12,3),(13,4),(14,5),(14,6)],
    # L (x offset = 16)
    [(16,0),(16,1),(16,2),(16,3),(16,4),(16,5),(16,6),(17,6),(18,6),(19,6)],
    # D (x offset = 21)
    [(21,0),(21,1),(21,2),(21,3),(21,4),(21,5),(21,6),(22,0),(23,0),(24,1),(24,2),(24,3),(24,4),(24,5),(23,6),(22,6)],
]

BLOCK = 2
# "AID" — 좌측
AID_X = 92
for letter in letters_aid:
    for px2, py2 in letter:
        x1 = AID_X + px2 * (BLOCK+1)
        y1 = title_y + py2 * (BLOCK+1)
        d.rectangle([x1, y1, x1+BLOCK, y1+BLOCK], fill=(*TEXT_COL, 255))

# "WORLD" — 우측
WORLD_X = AID_X + 15 * (BLOCK+1) + 6
for letter in letters_world:
    for px2, py2 in letter:
        x1 = WORLD_X + px2 * (BLOCK+1)
        y1 = title_y + py2 * (BLOCK+1)
        d.rectangle([x1, y1, x1+BLOCK, y1+BLOCK], fill=(*TEXT_COL, 255))

# ═══════════════════════════════════
# 13. 부제 "나이탬바 섬 이야기" (작게)
# ═══════════════════════════════════
# 부제는 별도 Label 노드로 처리 (Godot 씬에서)
# 여기서는 반투명 바를 깔아둠
d.rectangle([95, 36, 225, 44], fill=(0, 0, 0, 80))

# ═══════════════════════════════════
# 14. 피지 국기 색상 악센트 (하단 테두리)
# ═══════════════════════════════════
d.rectangle([0, H-3, W, H-1], fill=(28, 68, 148, 180))   # 파랑
d.rectangle([0, H-5, W, H-3], fill=(205, 40, 40, 120))   # 빨강 (유니언잭 느낌)

# ═══════════════════════════════════
# 저장
# ═══════════════════════════════════
out_path = os.path.join(OUT, "title_bg.png")
img.save(out_path)
print(f"저장됨: {out_path}")
