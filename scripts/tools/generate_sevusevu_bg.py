"""
세부세부 세레모니 배경 v2
320x180 — 밝고 따뜻한 부레 내부
사루사루(꽃목걸이), 마시(전통천), 둥글게 앉은 사람들, 타노아
"""
from PIL import Image, ImageDraw
import os, math

OUT = "/Users/nddn/Documents/Claude/Projects/IDC game/assets/sprites/tilesets"
os.makedirs(OUT, exist_ok=True)

W, H = 320, 180
img = Image.new("RGBA", (W, H))
d = ImageDraw.Draw(img)

# 따뜻한 팔레트
BURE_WALL  = (185, 155, 105)
BURE_WALL2 = (170, 142, 95)
ROOF_IN    = (142, 112, 72)
ROOF_BEAM  = (118, 88, 52)
FLOOR_MAT  = (195, 168, 115)
FLOOR_MAT2 = (180, 155, 105)
FLOOR_EDGE = (158, 135, 92)

# 마시 (전통천 — 벽 장식)
MASI_BG    = (225, 215, 192)
MASI_PAT   = (95, 62, 35)

# 타노아
TANOA      = (78, 52, 25)
TANOA_L    = (98, 68, 35)
KAVA_LIQ   = (145, 135, 115)
KAVA_FOAM  = (165, 155, 135)

# 빌로
BILO       = (168, 138, 88)
BILO_D     = (138, 108, 65)

# 사루사루 (꽃목걸이)
FLOWER_R   = (218, 75, 85)     # 빨간 히비스커스
FLOWER_Y   = (245, 205, 55)    # 노란 프랑기파니
FLOWER_W   = (242, 238, 228)   # 흰 꽃
FLOWER_P   = (195, 85, 155)    # 분홍
LEAF_G     = (55, 125, 55)     # 꽃 사이 잎

# 사람
SKIN_DARK  = (140, 95, 60)
SKIN_MED   = (155, 108, 68)
SKIN_LIGHT = (200, 160, 115)
SULU_GOLD  = (185, 148, 42)
SULU_BLUE  = (42, 68, 118)
SULU_GREEN = (55, 95, 48)
SHIRT_ORANGE = (205, 88, 42)
SHIRT_BLUE = (30, 80, 160)
SHIRT_RED  = (165, 55, 38)
HAIR_BLK   = (15, 10, 5)
HAIR_GRAY  = (168, 165, 158)

LIGHT      = (245, 225, 175)
CANDLE     = (255, 205, 75)

# ═══════════════ 1. 지붕 (따뜻한 톤) ═══════════════
for y in range(40):
    t = y / 40
    r = int(ROOF_IN[0] + 15 * t)
    g = int(ROOF_IN[1] + 12 * t)
    b = int(ROOF_IN[2] + 8 * t)
    d.line([0, y, W, y], fill=(r, g, b, 255))

# 서까래 (방사형, 밝은 톤)
cx, cy = 160, -15
for angle in range(0, 360, 18):
    rad = math.radians(angle)
    ex = int(cx + math.cos(rad) * 200)
    ey = int(cy + math.sin(rad) * 100)
    d.line([(cx, cy), (ex, ey)], fill=(*ROOF_BEAM, 150), width=1)

# ═══════════════ 2. 벽 (밝고 따뜻) ═══════════════
for y in range(25, 68):
    t = (y - 25) / 43
    col = BURE_WALL if int(t * 20) % 2 == 0 else BURE_WALL2
    d.line([0, y, W, y], fill=(*col, 255))

# 대나무 세로줄
for x in range(0, W, 14):
    d.line([x, 25, x, 68], fill=(*BURE_WALL2, 180), width=1)

# ═══════════════ 3. 마시 (전통천 벽 장식) ═══════════════
# 좌벽 마시
d.rectangle([15, 30, 55, 60], fill=(*MASI_BG, 255))
d.rectangle([15, 30, 55, 60], outline=(*MASI_PAT, 255))
# 마시 기하학 무늬
for my in range(34, 58, 6):
    d.line([18, my, 52, my], fill=(*MASI_PAT, 200), width=1)
for mx in range(20, 52, 8):
    d.line([mx, 32, mx, 58], fill=(*MASI_PAT, 200), width=1)
# 삼각형 패턴
for mx in range(22, 50, 12):
    d.polygon([mx, 36, mx+4, 32, mx+8, 36], fill=(*MASI_PAT, 150))

# 우벽 마시
d.rectangle([265, 30, 305, 60], fill=(*MASI_BG, 255))
d.rectangle([265, 30, 305, 60], outline=(*MASI_PAT, 255))
for my in range(34, 58, 6):
    d.line([268, my, 302, my], fill=(*MASI_PAT, 200), width=1)
for mx in range(270, 302, 8):
    d.line([mx, 32, mx, 58], fill=(*MASI_PAT, 200), width=1)

# ═══════════════ 4. 사루사루 꽃 장식 (천장에서 드리운) ═══════════════
def draw_garland(x1, x2, y_base, sag=8):
    """꽃목걸이 — 곡선에 꽃들"""
    mid = (x1 + x2) // 2
    for x in range(x1, x2, 3):
        t = (x - x1) / max(1, x2 - x1)
        y = y_base + int(sag * math.sin(t * math.pi))
        colors = [FLOWER_R, FLOWER_Y, FLOWER_W, FLOWER_P]
        col = colors[(x // 3) % 4]
        d.ellipse([x-2, y-2, x+2, y+2], fill=(*col, 230))
        if (x // 3) % 3 == 0:
            d.ellipse([x-1, y+2, x+1, y+4], fill=(*LEAF_G, 200))

draw_garland(60, 150, 26, 6)
draw_garland(170, 260, 26, 6)
draw_garland(100, 220, 22, 8)

# ═══════════════ 5. 바닥 매트 (밝은 톤) ═══════════════
d.line([0, 68, W, 68], fill=(*FLOOR_EDGE, 255), width=2)

for y in range(68, H):
    col = FLOOR_MAT if (y // 4) % 2 == 0 else FLOOR_MAT2
    d.line([0, y, W, y], fill=(*col, 255))

for y in range(70, H, 4):
    for x in range(0, W, 6):
        d.rectangle([x, y, x+3, y+2], fill=(*FLOOR_EDGE, 80))

# ═══════════════ 6. 타노아 (중앙) ═══════════════
TX, TY = 160, 112
d.ellipse([TX-24, TY-9, TX+24, TY+9], fill=(*TANOA, 255))
d.ellipse([TX-22, TY-7, TX+22, TY+7], fill=(*TANOA_L, 255))
d.ellipse([TX-20, TY-5, TX+20, TY+5], fill=(*KAVA_LIQ, 255))
d.ellipse([TX-14, TY-3, TX+10, TY+2], fill=(*KAVA_FOAM, 180))
# 다리
for lx in [TX-22, TX-12, TX+12, TX+22]:
    d.rectangle([lx-2, TY+8, lx+2, TY+14], fill=(*TANOA, 255))

# 빌로 (주변에 3개)
for bx, by in [(TX-32, TY+3), (TX+30, TY-1), (TX-10, TY+14)]:
    d.ellipse([bx-5, by-3, bx+5, by+3], fill=(*BILO, 255))
    d.ellipse([bx-4, by-2, bx+4, by+2], fill=(*BILO_D, 255))

# ═══════════════ 7. 촛불/오일 램프 (따뜻한 빛) ═══════════════
for lx in [70, 250]:
    d.rectangle([lx-1, 58, lx+1, 68], fill=(118, 88, 52, 255))
    d.ellipse([lx-3, 54, lx+3, 60], fill=(*CANDLE, 220))
    d.ellipse([lx-5, 52, lx+5, 57], fill=(*LIGHT, 80))

# ═══════════════ 8. 사람들 (둥글게 앉음, 밝게) ═══════════════
def seated(sx, sy, sulu_col, skin, hair_col=HAIR_BLK, has_shirt=False, shirt_col=None,
           large=False, garland=False):
    w = 9 if large else 7
    h = 11 if large else 9
    # 다리 (접고 앉음)
    d.ellipse([sx-w, sy+h-5, sx+w, sy+h+3], fill=(*sulu_col, 255))
    # 몸통
    body_col = shirt_col if has_shirt and shirt_col else skin
    d.rectangle([sx-w//2-1, sy-1, sx+w//2+1, sy+h-4], fill=(*body_col, 255))
    # 팔
    d.rectangle([sx-w//2-3, sy, sx-w//2-1, sy+h-5], fill=(*skin, 255))
    d.rectangle([sx+w//2+1, sy, sx+w//2+3, sy+h-5], fill=(*skin, 255))
    # 목
    d.rectangle([sx-2, sy-4, sx+2, sy], fill=(*skin, 255))
    # 머리
    d.ellipse([sx-5, sy-10, sx+5, sy-3], fill=(*skin, 255))
    d.ellipse([sx-5, sy-10, sx+5, sy-7], fill=(*hair_col, 255))
    # 사루사루 (꽃목걸이)
    if garland:
        for gx in range(sx-4, sx+5, 3):
            col = [FLOWER_R, FLOWER_Y, FLOWER_W][(gx//3)%3]
            d.ellipse([gx-1, sy-1, gx+1, sy+1], fill=(*col, 230))

# Ratu Josefa (중앙 위, 금색 sulu, 크게)
seated(160, 75, SULU_GOLD, SKIN_DARK, HAIR_GRAY, large=True, garland=True)
# Ratu 목걸이 (추장 상징)
d.line([(156, 77), (164, 77)], fill=(195, 45, 35, 255))

# 주인공 (아래 중앙, KODA 파란 셔츠, 꽃목걸이 받음)
seated(160, 130, (50,50,75), SKIN_LIGHT, (30,20,10), True, SHIRT_BLUE, garland=True)

# 마을 사람들 (양 옆, 기도 자세 — 고개 숙인)
# 좌측
seated(50, 95, SULU_BLUE, SKIN_MED)
seated(85, 105, SULU_GREEN, SKIN_DARK, HAIR_BLK, True, SHIRT_RED)
seated(40, 120, SULU_BLUE, SKIN_MED)

# 우측
seated(270, 95, SULU_GREEN, SKIN_MED)
seated(240, 108, SULU_BLUE, SKIN_DARK)
seated(280, 122, SULU_BLUE, SKIN_MED, HAIR_BLK, True, SHIRT_RED)

# Mere (좌측 앞, 주황 셔츠, 꽃목걸이)
seated(105, 128, (58,85,55), SKIN_MED, HAIR_BLK, True, SHIRT_ORANGE, garland=True)

# Lani (우측 앞, 카키)
seated(215, 125, (88,108,78), SKIN_MED, HAIR_BLK, True, (105,128,95), garland=True)

# ═══════════════ 9. 사루사루 바닥 꽃잎 (흩어진) ═══════════════
import random
random.seed(88)
for _ in range(25):
    fx = random.randint(60, 260)
    fy = random.randint(90, 155)
    col = [FLOWER_R, FLOWER_Y, FLOWER_P, FLOWER_W][random.randint(0,3)]
    d.ellipse([fx-1, fy-1, fx+1, fy+1], fill=(*col, 120))

# ═══════════════ 10. 따뜻한 빛 (중앙에서 퍼짐) ═══════════════
for r_size in range(70, 15, -5):
    d.ellipse([TX-r_size, TY-r_size//2, TX+r_size, TY+r_size//2],
              fill=(LIGHT[0], LIGHT[1], LIGHT[2], 12))

# ═══════════════ 11. 자막 영역 ═══════════════
d.rectangle([0, H-18, W, H], fill=(0, 0, 0, 70))

out_path = os.path.join(OUT, "sevusevu_bg.png")
img.save(out_path)
print(f"저장됨: {out_path}")
