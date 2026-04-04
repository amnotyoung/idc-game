"""
Aid World — 나이탬바 섬 배경 생성기
320×180 픽셀아트 열대 섬 배경 → assets/sprites/tilesets/naitamba_bg.png
"""
from PIL import Image, ImageDraw
import os

OUT = "/Users/nddn/Documents/Claude/Projects/IDC game/assets/sprites/tilesets"
os.makedirs(OUT, exist_ok=True)

W, H = 320, 180

img = Image.new("RGB", (W, H))
draw = ImageDraw.Draw(img)

# ── 하늘 (y=0~70) ─────────────────────────────────────
SKY_TOP    = (135, 196, 235)
SKY_BOTTOM = (180, 220, 245)
for y in range(71):
    t = y / 70
    r = int(SKY_TOP[0] + (SKY_BOTTOM[0] - SKY_TOP[0]) * t)
    g = int(SKY_TOP[1] + (SKY_BOTTOM[1] - SKY_TOP[1]) * t)
    b = int(SKY_TOP[2] + (SKY_BOTTOM[2] - SKY_TOP[2]) * t)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# ── 구름 (둥근 픽셀 뭉치) ───────────────────────────────
CLOUD = (245, 248, 252)

def draw_cloud(cx, cy, w, h):
    # 중앙 타원
    draw.ellipse([cx - w//2, cy - h//2, cx + w//2, cy + h//2], fill=CLOUD)
    # 좌측 작은 봉우리
    draw.ellipse([cx - w//2 - 4, cy - h//4, cx - w//4, cy + h//4], fill=CLOUD)
    # 우측 작은 봉우리
    draw.ellipse([cx + w//4, cy - h//4, cx + w//2 + 4, cy + h//4], fill=CLOUD)

draw_cloud(55, 22, 38, 14)
draw_cloud(175, 15, 46, 16)
draw_cloud(270, 28, 32, 12)

# ── 열대 초목 언덕 (y=60~130) ──────────────────────────
HILL_DARK  = (34,  90,  34)
HILL_MID   = (48, 120,  48)
HILL_LIGHT = (72, 150,  60)

# 뒷 언덕 (짙은 초록)
hill_back = [
    (0, 130), (0, 95), (30, 82), (60, 72), (90, 68),
    (120, 65), (150, 70), (180, 64), (210, 60), (240, 65),
    (270, 72), (300, 78), (320, 85), (320, 130)
]
draw.polygon(hill_back, fill=HILL_DARK)

# 앞 언덕 (중간 초록)
hill_mid = [
    (0, 130), (0, 105), (20, 98), (50, 90), (80, 88),
    (110, 85), (130, 82), (160, 88), (190, 84), (220, 80),
    (250, 85), (280, 90), (310, 96), (320, 100), (320, 130)
]
draw.polygon(hill_mid, fill=HILL_MID)

# 앞쪽 낮은 초목 (밝은 초록)
hill_front = [
    (0, 130), (0, 115), (30, 110), (60, 108), (90, 112),
    (110, 115), (130, 110), (160, 115), (200, 110), (230, 108),
    (260, 112), (290, 115), (320, 112), (320, 130)
]
draw.polygon(hill_front, fill=HILL_LIGHT)

# ── 모래사장 (y=120~140) ────────────────────────────────
SAND_TOP = (225, 200, 140)
SAND_BOT = (210, 185, 120)
for y in range(120, 141):
    t = (y - 120) / 20
    r = int(SAND_TOP[0] + (SAND_BOT[0] - SAND_TOP[0]) * t)
    g = int(SAND_TOP[1] + (SAND_BOT[1] - SAND_TOP[1]) * t)
    b = int(SAND_TOP[2] + (SAND_BOT[2] - SAND_TOP[2]) * t)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# ── 바다 (y=140~180) ───────────────────────────────────
SEA_BASE  = (32, 148, 160)
SEA_LIGHT = (55, 175, 185)
for y in range(140, H):
    t = (y - 140) / (H - 140)
    r = int(SEA_BASE[0] + (SEA_LIGHT[0] - SEA_BASE[0]) * t * 0.4)
    g = int(SEA_BASE[1] + (SEA_LIGHT[1] - SEA_BASE[1]) * t * 0.4)
    b = int(SEA_BASE[2] + (SEA_LIGHT[2] - SEA_BASE[2]) * t * 0.4)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# 물결 밝은 줄 (2px 간격)
for y in range(143, H, 4):
    for x in range(0, W, 6):
        wave_w = 4 + (x % 3)
        draw.line([(x, y), (x + wave_w, y)], fill=SEA_LIGHT)

# ── 전통 bure 오두막 (중앙 x=130~190, y=70~110) ─────────
WALL_BROWN  = (160, 110,  65)
WALL_SHADOW = (130,  88,  50)
ROOF_DARK   = ( 80,  50,  25)
ROOF_MID    = (105,  70,  35)

# 벽 본체
draw.rectangle([130, 92, 190, 115], fill=WALL_BROWN)
# 벽 그림자 (좌측)
draw.rectangle([130, 92, 140, 115], fill=WALL_SHADOW)
# 문
draw.rectangle([155, 100, 165, 115], fill=(100, 65, 30))
# 창문 좌
draw.rectangle([136, 96, 146, 104], fill=(90, 58, 25))
# 창문 우
draw.rectangle([174, 96, 184, 104], fill=(90, 58, 25))

# 초가지붕 (삼각형 형태)
roof = [(120, 93), (160, 68), (200, 93)]
draw.polygon(roof, fill=ROOF_MID)
# 지붕 그림자 면
roof_shadow = [(120, 93), (160, 68), (160, 93)]
draw.polygon(roof_shadow, fill=ROOF_DARK)
# 지붕 능선
draw.line([(160, 68), (160, 93)], fill=ROOF_DARK, width=1)
# 처마 선
draw.line([(120, 93), (200, 93)], fill=ROOF_DARK, width=2)

# ── 야자수 좌 (x=40) ──────────────────────────────────
PALM_TRUNK = (130, 95, 50)
PALM_LEAF  = (45, 130, 45)

def draw_palm(tx, ty):
    # 기둥 (약간 곡선 느낌으로 2px)
    for i in range(35):
        ox = int(i * 0.15)
        draw.rectangle([tx + ox, ty - i, tx + ox + 2, ty - i + 2], fill=PALM_TRUNK)
    # 잎사귀 부채꼴 6장
    top_x, top_y = tx + 6, ty - 34
    leaf_dirs = [
        (-18, -8), (-14, -14), (-6, -16), (4, -16),
        (12, -12), (16, -6)
    ]
    for dx, dy in leaf_dirs:
        draw.line(
            [(top_x, top_y), (top_x + dx, top_y + dy)],
            fill=PALM_LEAF, width=2
        )
        # 잎 끝 살짝 두껍게
        draw.rectangle(
            [top_x + dx - 1, top_y + dy - 1, top_x + dx + 1, top_y + dy + 1],
            fill=PALM_LEAF
        )

draw_palm(38, 118)
draw_palm(258, 116)

# ── 작은 열대 관목들 ────────────────────────────────────
SHRUB = (55, 140, 55)
shrub_positions = [(50, 118), (75, 122), (200, 120), (225, 118), (100, 125), (240, 124)]
for sx, sy in shrub_positions:
    draw.ellipse([sx - 5, sy - 4, sx + 5, sy + 2], fill=SHRUB)

# ── 모래사장 잔물결 ─────────────────────────────────────
SAND_LINE = (190, 168, 105)
for y in range(124, 140, 5):
    for x in range(10, W - 10, 18):
        draw.line([(x, y), (x + 10, y)], fill=SAND_LINE)

# ── 저장 ───────────────────────────────────────────────
out_path = os.path.join(OUT, "naitamba_bg.png")
img.save(out_path)
print(f"저장됨: {out_path}  ({W}×{H})")
