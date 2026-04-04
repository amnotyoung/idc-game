"""
수바 ↔ 나이탬바 바다 전환 컷
320x180 픽셀아트 — 에메랄드 바다 + 콘크리트 선착장 + 야자수 섬 원경
사진 참고: 투명한 청록 바다, 콘크리트 잔교, 야자수 숲, 초가지붕 부레
"""
from PIL import Image, ImageDraw
import os

OUT = "/Users/nddn/Documents/Claude/Projects/IDC game/assets/sprites/tilesets"
os.makedirs(OUT, exist_ok=True)

W, H = 320, 180
img = Image.new("RGBA", (W, H))
d = ImageDraw.Draw(img)

# ═══════════════════════════════════
# 팔레트 — 사진 기반
# ═══════════════════════════════════
# 하늘 (맑은 열대 파랑)
SKY_TOP  = (42, 108, 195)
SKY_MID  = (68, 148, 218)
SKY_BOT  = (115, 185, 238)

# 구름 (얇은 새털구름)
CIRRUS   = (215, 228, 242)
CIRRUS_L = (232, 240, 250)

# 바다 (에메랄드~청록 그라디언트)
SEA_SHAL = (85, 195, 172)     # 얕은 바다 (에메랄드)
SEA_MID  = (62, 172, 155)     # 중간
SEA_DEEP = (42, 145, 135)     # 깊은 쪽
SEA_GLOW = (125, 218, 195)    # 수면 반짝임
SEA_FOAM = (195, 232, 222)    # 파도 거품

# 잔교 (콘크리트)
PIER_TOP  = (215, 205, 185)   # 콘크리트 상면
PIER_SIDE = (185, 175, 158)   # 측면
PIER_EDGE = (165, 155, 138)   # 엣지
PIER_WET  = (155, 148, 132)   # 물에 젖은 부분

# 섬 (빽빽한 열대림)
TREE_DARK  = (18, 62, 28)
TREE_MID   = (32, 95, 38)
TREE_LIGHT = (48, 128, 52)
TREE_BRIGHT = (65, 155, 62)

# 야자수
PALM_TRK  = (95, 72, 38)
PALM_TRD  = (72, 52, 25)
PALM_LF   = (35, 118, 32)
PALM_LFD  = (22, 88, 18)
PALM_LFL  = (55, 148, 48)

# 부레 (초가지붕)
BURE_WALL = (168, 135, 85)
BURE_ROOF = (145, 125, 82)
BURE_ROFD = (118, 98, 62)

# 돌담
STONE = (135, 128, 115)
STONE_D = (108, 102, 92)

# ═══════════════════════════════════
# 1. 하늘 (상단 60%)
# ═══════════════════════════════════
for y in range(95):
    t = y / 95
    if t < 0.5:
        s = t / 0.5
        r = int(SKY_TOP[0] + (SKY_MID[0] - SKY_TOP[0]) * s)
        g = int(SKY_TOP[1] + (SKY_MID[1] - SKY_TOP[1]) * s)
        b = int(SKY_TOP[2] + (SKY_MID[2] - SKY_TOP[2]) * s)
    else:
        s = (t - 0.5) / 0.5
        r = int(SKY_MID[0] + (SKY_BOT[0] - SKY_MID[0]) * s)
        g = int(SKY_MID[1] + (SKY_BOT[1] - SKY_MID[1]) * s)
        b = int(SKY_MID[2] + (SKY_BOT[2] - SKY_MID[2]) * s)
    d.line([0, y, W, y], fill=(r, g, b, 255))

# 새털구름 (얇고 길게)
cirrus_data = [
    (20, 15, 120, 4), (80, 22, 95, 3), (160, 10, 110, 5),
    (200, 30, 80, 3), (250, 18, 60, 4), (30, 38, 70, 2),
    (140, 35, 90, 3), (270, 25, 45, 3),
]
for cx, cy, cw, ch in cirrus_data:
    d.ellipse([cx, cy, cx+cw, cy+ch], fill=(*CIRRUS, 100))
    d.ellipse([cx+5, cy-1, cx+cw-8, cy+ch-1], fill=(*CIRRUS_L, 80))

# ═══════════════════════════════════
# 2. 섬 (y=55~100, 빽빽한 열대림)
# ═══════════════════════════════════
# 뒷 나무층 (짙은 초록)
trees_back = [
    (0,95), (0,72), (15,65), (30,58), (50,55), (70,52),
    (90,48), (110,50), (130,46), (150,50), (170,48),
    (190,52), (210,50), (230,48), (250,52), (270,55),
    (290,58), (310,62), (320,65), (320,95)
]
d.polygon(trees_back, fill=(*TREE_DARK, 255))

# 중간 나무층
trees_mid = [
    (0,95), (0,78), (12,72), (28,65), (45,60), (65,56),
    (85,52), (100,55), (120,50), (140,54), (155,52),
    (175,56), (195,54), (215,58), (235,55), (255,58),
    (275,62), (295,66), (310,70), (320,72), (320,95)
]
d.polygon(trees_mid, fill=(*TREE_MID, 255))

# 앞 나무층 (밝은 초록)
trees_front = [
    (0,95), (0,82), (20,78), (40,74), (60,70), (80,68),
    (100,72), (120,68), (140,72), (160,70), (180,74),
    (200,70), (220,72), (240,68), (260,72), (280,75),
    (300,78), (320,80), (320,95)
]
d.polygon(trees_front, fill=(*TREE_LIGHT, 255))

# 나무 사이 밝은 점 (잎 하이라이트)
import random
random.seed(42)
for _ in range(80):
    x = random.randint(0, W)
    y = random.randint(52, 90)
    s = random.randint(2, 5)
    d.ellipse([x, y, x+s, y+s], fill=(*TREE_BRIGHT, 180))

# ═══════════════════════════════════
# 3. 야자수 (섬 위, 사진처럼 바람에 휘어진)
# ═══════════════════════════════════
def palm_wind(px, py, h=28, lean=5):
    """바람에 휘어진 야자수"""
    for i in range(h):
        curve = int((i / h) ** 1.5 * lean)
        cx = px + curve
        w = max(1, 3 - i * 2 // h)
        col = PALM_TRK if i % 3 != 2 else PALM_TRD
        d.rectangle([cx-w, py-i, cx+w, py-i+1], fill=(*col, 255))
    top_x = px + lean
    top_y = py - h
    # 잎 (바람에 오른쪽으로 쏠림)
    leaves = [
        (-10, -6, 12, 4), (-6, -10, 10, 3), (2, -12, 14, 4),
        (8, -6, 14, 3), (-2, -4, 10, 5), (10, -8, 12, 3),
        (-8, -2, 8, 4), (6, -10, 10, 3),
    ]
    for lx, ly, lw, lh in leaves:
        bx = top_x + lx
        by = top_y + ly
        d.ellipse([bx, by, bx+lw, by+lh], fill=(*PALM_LF, 255))
    for lx, ly, lw, lh in leaves[::2]:
        bx = top_x + lx + 1
        by = top_y + ly + 1
        d.ellipse([bx, by, bx+lw-2, by+lh-1], fill=(*PALM_LFD, 255))
    for lx, ly, lw, lh in leaves[1::3]:
        bx = top_x + lx + 2
        by = top_y + ly
        d.ellipse([bx, by, bx+lw-1, by+lh], fill=(*PALM_LFL, 200))
    # 코코넛
    for ox, oy in [(-2,-3),(3,-2),(-4,-1)]:
        d.ellipse([top_x+ox, top_y+oy, top_x+ox+3, top_y+oy+3], fill=(78,58,28,255))

palm_wind(25, 82, 30, 6)
palm_wind(60, 78, 26, 4)
palm_wind(95, 75, 32, 7)
palm_wind(130, 80, 24, 5)
palm_wind(165, 76, 28, 6)
palm_wind(200, 82, 22, 4)
palm_wind(235, 78, 30, 8)
palm_wind(270, 80, 26, 5)
palm_wind(300, 84, 22, 4)
# 겹치는 작은 야자수들
palm_wind(45, 80, 18, 3)
palm_wind(115, 82, 16, 3)
palm_wind(185, 84, 20, 4)
palm_wind(255, 82, 18, 3)

# ═══════════════════════════════════
# 4. 부레 오두막 + 돌담 (나무 사이사이)
# ═══════════════════════════════════
# 부레 1 (좌)
d.rectangle([75, 72, 105, 88], fill=(*BURE_WALL, 255))
d.polygon([70, 72, 90, 58, 110, 72], fill=(*BURE_ROOF, 255))
d.polygon([70, 72, 90, 58, 90, 72], fill=(*BURE_ROFD, 255))

# 부레 2 (우)
d.rectangle([220, 70, 248, 86], fill=(*BURE_WALL, 255))
d.polygon([215, 70, 234, 56, 253, 70], fill=(*BURE_ROOF, 255))
d.polygon([215, 70, 234, 56, 234, 70], fill=(*BURE_ROFD, 255))

# 돌담 (해안선)
for x in range(0, W, 3):
    y_base = 92 + (x % 7) // 3
    d.rectangle([x, y_base, x+2, y_base+3], fill=(*STONE, 255))
    d.rectangle([x, y_base+3, x+2, y_base+4], fill=(*STONE_D, 255))

# ═══════════════════════════════════
# 5. 바다 (에메랄드 그라디언트)
# ═══════════════════════════════════
for y in range(95, H):
    t = (y - 95) / (H - 95)
    r = int(SEA_SHAL[0] + (SEA_DEEP[0] - SEA_SHAL[0]) * t)
    g = int(SEA_SHAL[1] + (SEA_DEEP[1] - SEA_SHAL[1]) * t)
    b = int(SEA_SHAL[2] + (SEA_DEEP[2] - SEA_SHAL[2]) * t)
    d.line([0, y, W, y], fill=(r, g, b, 255))

# 수면 반짝임 (밝은 점들)
for _ in range(60):
    x = random.randint(0, W)
    y = random.randint(97, H-5)
    w = random.randint(3, 8)
    d.line([x, y, x+w, y], fill=(*SEA_GLOW, 120))

# 파도 거품 (해안선 근처)
for x in range(0, W, 8):
    fy = 96 + (x % 5) // 2
    d.line([x, fy, x+5, fy], fill=(*SEA_FOAM, 150))

# ═══════════════════════════════════
# 6. 잔교 (중앙, 카메라 쪽으로 뻗어나감)
# ═══════════════════════════════════
# 원근법 — 위(좁음) → 아래(넓음)
for y in range(95, H):
    t = (y - 95) / (H - 95)
    half_w = int(4 + t * 14)  # 위에서 4px → 아래에서 18px
    cx = 160
    # 상면
    d.line([cx - half_w, y, cx + half_w, y], fill=(*PIER_TOP, 255))
    # 좌측면
    d.point((cx - half_w, y), fill=(*PIER_EDGE, 255))
    # 우측면
    d.point((cx + half_w, y), fill=(*PIER_EDGE, 255))
    # 젖은 자국 (가장자리)
    if y > 100:
        d.point((cx - half_w + 1, y), fill=(*PIER_WET, 200))
        d.point((cx + half_w - 1, y), fill=(*PIER_WET, 200))

# 잔교 표면 질감 (균열/이음새)
for y in range(100, H, 8):
    t = (y - 95) / (H - 95)
    half_w = int(4 + t * 14)
    cx = 160
    d.line([cx - half_w + 2, y, cx + half_w - 2, y], fill=(*PIER_SIDE, 180))

# ═══════════════════════════════════
# 7. 자막 영역 (하단 반투명)
# ═══════════════════════════════════
d.rectangle([0, H-22, W, H], fill=(0, 0, 0, 100))

# ═══════════════════════════════════
out_path = os.path.join(OUT, "sea_transition.png")
img.save(out_path)
print(f"저장됨: {out_path}")
