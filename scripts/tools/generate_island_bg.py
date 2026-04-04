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

# ── 선착장 (Jetty) — 중앙 x=148~172, 해안(y=137)~바다(y=168) ──
JETTY_PLANK  = (145, 105,  60)   # 나무 판자
JETTY_SHADOW = (105,  72,  38)   # 판자 음영
JETTY_POST   = ( 90,  58,  28)   # 파일링(기둥)
JETTY_EDGE   = (115,  80,  42)   # 측면 마감

JX1, JX2 = 148, 172   # 선착장 좌우 (24px 폭)
JY1, JY2 = 137, 168   # 선착장 상하

# 판자 표면 (2px 간격 가로선)
for y in range(JY1, JY2):
    draw.line([(JX1, y), (JX2, y)], fill=JETTY_PLANK)
# 판자 이음새 (어두운 가로선, 3px 간격)
for y in range(JY1, JY2, 3):
    draw.line([(JX1 + 1, y), (JX2 - 1, y)], fill=JETTY_SHADOW)
# 측면 마감 (세로 엣지)
draw.line([(JX1, JY1), (JX1, JY2)], fill=JETTY_EDGE, width=2)
draw.line([(JX2, JY1), (JX2, JY2)], fill=JETTY_EDGE, width=2)
# 수중 파일링 기둥 (4개 — 바다 부분만)
for px in [JX1 + 3, JX1 + 9, JX2 - 9, JX2 - 3]:
    draw.rectangle([px - 1, JY2, px + 1, JY2 + 9], fill=JETTY_POST)
# 난간 (상단 좌우 기둥 + 가로대)
for px in [JX1 + 1, JX2 - 1]:
    draw.rectangle([px - 1, JY1, px + 1, JY1 + 18], fill=JETTY_EDGE)
draw.line([(JX1 + 1, JY1 + 9), (JX2 - 1, JY1 + 9)], fill=JETTY_EDGE, width=1)
draw.line([(JX1 + 1, JY1 + 18), (JX2 - 1, JY1 + 18)], fill=JETTY_EDGE, width=1)

# ── 모터보트 (선착장 우측, x=175~215, y=149~162) ─────────
HULL_DARK  = ( 28,  82, 148)   # 파란 유리섬유 선체
HULL_LIGHT = ( 52, 112, 175)   # 선체 상단 하이라이트
HULL_BELLY = ( 22,  65, 120)   # 선체 하단 그림자
INTERIOR   = (218, 212, 200)   # 선내 (베이지 흰)
MOTOR_BODY = ( 48,  50,  55)   # 선외기 본체
MOTOR_ARM  = ( 38,  40,  44)   # 선외기 팔
WINDSHIELD = (175, 212, 238)   # 앞유리
ROPE_COL   = (178, 152,  88)   # 계류줄

BX1, BX2 = 176, 214   # 보트 좌우
BY1, BY2 = 150, 162   # 보트 상하

# 선체 하단 (뾰족한 배 형태)
hull_pts = [
    (BX1 + 4, BY2), (BX1,     BY1 + 6),
    (BX1,     BY1 + 3),
    (BX1 + 6, BY1),
    (BX2 - 2, BY1),
    (BX2,     BY1 + 4),
    (BX2,     BY2 - 1),
]
draw.polygon(hull_pts, fill=HULL_DARK)
# 선체 상단 하이라이트 (1px 선)
draw.line([(BX1 + 6, BY1), (BX2 - 2, BY1)], fill=HULL_LIGHT, width=2)
# 선체 좌측 경사 하이라이트
draw.line([(BX1, BY1 + 3), (BX1 + 6, BY1)], fill=HULL_LIGHT, width=1)
# 선내 (상단에서 약간 아래로 오목한 영역)
draw.rectangle([BX1 + 5, BY1 + 2, BX2 - 4, BY1 + 7], fill=INTERIOR)
# 앞유리 (조종석 바람막이)
draw.polygon([
    (BX1 + 8, BY1 + 2), (BX1 + 12, BY1 - 2),
    (BX1 + 20, BY1 - 2), (BX1 + 22, BY1 + 2)
], fill=WINDSHIELD)
draw.line([(BX1 + 8, BY1 + 2), (BX1 + 12, BY1 - 2)], fill=(120, 160, 195), width=1)
draw.line([(BX1 + 12, BY1 - 2), (BX1 + 20, BY1 - 2)], fill=(120, 160, 195), width=1)
# 선외기 (오른쪽 끝)
draw.rectangle([BX2 - 1, BY1 + 2, BX2 + 4, BY1 + 9], fill=MOTOR_BODY)
draw.rectangle([BX2 + 2, BY1 + 9, BX2 + 4, BY2 - 1], fill=MOTOR_ARM)
draw.rectangle([BX2,     BY2 - 2, BX2 + 5, BY2],     fill=MOTOR_BODY)  # 프로펠러

# 계류줄 (보트 앞 끝 → 선착장)
draw.line([(BX1, BY1 + 5), (JX2, JY1 + 22)], fill=ROPE_COL, width=1)

# 보트 물 반사 그림자
for i in range(4):
    alpha_col = (
        int(HULL_DARK[0] * 0.5), int(HULL_DARK[1] * 0.5),
        int(HULL_DARK[2] * 0.55)
    )
    draw.line([(BX1 + 6 + i, BY2 + 1 + i), (BX2 - i, BY2 + 1 + i)],
              fill=alpha_col)

# ── 저장 ───────────────────────────────────────────────
out_path = os.path.join(OUT, "naitamba_bg.png")
img.save(out_path)
print(f"저장됨: {out_path}  ({W}×{H})")
