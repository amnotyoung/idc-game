"""
세부세부 세레모니 컷씬 배경
320x180 — 부레 내부, 둥글게 앉은 사람들, 중앙 타노아
"""
from PIL import Image, ImageDraw
import os, math

OUT = "/Users/nddn/Documents/Claude/Projects/IDC game/assets/sprites/tilesets"
os.makedirs(OUT, exist_ok=True)

W, H = 320, 180
img = Image.new("RGBA", (W, H))
d = ImageDraw.Draw(img)

# 팔레트
BURE_WALL  = (145, 115, 68)     # 부레 벽 (대나무/짚)
BURE_WALL2 = (128, 98, 55)
ROOF_IN    = (105, 78, 42)      # 초가지붕 안쪽
ROOF_BEAM  = (88, 62, 32)       # 지붕 서까래
FLOOR_MAT  = (165, 138, 85)     # 바닥 매트
FLOOR_MAT2 = (148, 122, 75)
FLOOR_EDGE = (128, 105, 62)

TANOA      = (78, 52, 25)       # 타노아 (짙은 나무)
TANOA_L    = (98, 68, 35)
KAVA_LIQUID = (135, 125, 105)   # 양고나 액체 (회갈색)
KAVA_FOAM  = (155, 145, 125)

BILO       = (158, 128, 78)     # 코코넛 잔
BILO_D     = (128, 98, 55)

SKIN_DARK  = (140, 95, 60)      # 피지 피부톤
SKIN_MED   = (155, 108, 68)
SULU_GOLD  = (185, 148, 42)     # Ratu sulu
SULU_BLUE  = (42, 68, 118)      # 일반 sulu
SULU_GREEN = (55, 95, 48)
SHIRT_RED  = (165, 55, 38)
CLOTH_WHITE = (225, 218, 205)   # 거름천

LIGHT      = (225, 195, 135)    # 따뜻한 빛
SHADOW     = (85, 62, 35)

# ═══════════════════ 1. 지붕 안쪽 (상단) ═══════════════════
for y in range(50):
    t = y / 50
    r = int(ROOF_IN[0] - t * 15)
    g = int(ROOF_IN[1] - t * 12)
    b = int(ROOF_IN[2] - t * 8)
    d.line([0, y, W, y], fill=(r, g, b, 255))

# 서까래 (방사형)
cx, cy = 160, -20
for angle in range(0, 360, 15):
    rad = math.radians(angle)
    ex = int(cx + math.cos(rad) * 200)
    ey = int(cy + math.sin(rad) * 120)
    d.line([(cx, cy), (ex, ey)], fill=(*ROOF_BEAM, 180), width=1)

# ═══════════════════ 2. 벽 (중단) ═══════════════════
for y in range(30, 75):
    t = (y - 30) / 45
    col = BURE_WALL if int(t * 20) % 2 == 0 else BURE_WALL2
    d.line([0, y, W, y], fill=(*col, 255))

# 대나무 세로줄
for x in range(0, W, 12):
    d.line([x, 30, x, 75], fill=(*BURE_WALL2, 200), width=1)

# 벽-바닥 경계
d.line([0, 75, W, 75], fill=(*FLOOR_EDGE, 255), width=2)

# ═══════════════════ 3. 바닥 매트 ═══════════════════
for y in range(75, H):
    col = FLOOR_MAT if (y // 4) % 2 == 0 else FLOOR_MAT2
    d.line([0, y, W, y], fill=(*col, 255))

# 매트 짜임 패턴
for y in range(77, H, 4):
    for x in range(0, W, 6):
        d.rectangle([x, y, x+3, y+2], fill=(*FLOOR_EDGE, 100))

# ═══════════════════ 4. 타노아 (중앙) ═══════════════════
TX, TY = 160, 118
# 그릇 본체 (타원)
d.ellipse([TX-22, TY-8, TX+22, TY+8], fill=(*TANOA, 255))
d.ellipse([TX-20, TY-6, TX+20, TY+6], fill=(*TANOA_L, 255))
# 양고나 액체
d.ellipse([TX-18, TY-4, TX+18, TY+4], fill=(*KAVA_LIQUID, 255))
d.ellipse([TX-12, TY-2, TX+8, TY+1], fill=(*KAVA_FOAM, 180))
# 다리 (4개)
for lx in [TX-20, TX-10, TX+10, TX+20]:
    d.rectangle([lx-2, TY+7, lx+2, TY+12], fill=(*TANOA, 255))

# ═══════════════════ 5. 거름천 (타노아 옆) ═══════════════════
d.polygon([(TX+25, TY-5), (TX+35, TY-12), (TX+40, TY+5), (TX+30, TY+5)],
          fill=(*CLOTH_WHITE, 200))

# ═══════════════════ 6. 빌로 (코코넛 잔들) ═══════════════════
for bx, by in [(TX-30, TY+2), (TX+28, TY-2), (TX-8, TY+10)]:
    d.ellipse([bx-4, by-2, bx+4, by+2], fill=(*BILO, 255))
    d.ellipse([bx-3, by-1, bx+3, by+1], fill=(*BILO_D, 255))

# ═══════════════════ 7. 사람들 (둥글게 앉은 실루엣) ═══════════════════
def seated_person(sx, sy, sulu_col, skin=SKIN_DARK, has_shirt=False, shirt_col=None, large=False):
    """앉은 사람 (정면/반측면)"""
    w = 8 if large else 6
    h = 10 if large else 8
    # 다리 (접고 앉음)
    d.ellipse([sx-w, sy+h-4, sx+w, sy+h+2], fill=(*sulu_col, 255))
    # 몸통
    if has_shirt and shirt_col:
        d.rectangle([sx-w//2, sy, sx+w//2, sy+h-3], fill=(*shirt_col, 255))
    else:
        d.rectangle([sx-w//2, sy, sx+w//2, sy+h-3], fill=(*skin, 255))
    # 머리
    d.ellipse([sx-4, sy-6, sx+4, sy+1], fill=(*skin, 255))

# Ratu Josefa (중앙 위, 가장 큼 — 금색 sulu)
seated_person(160, 82, SULU_GOLD, SKIN_DARK, large=True)
# Ratu 머리 위 회색 (노인)
d.ellipse([156, 76, 164, 79], fill=(168, 165, 158, 255))

# 주인공 (아래 중앙 — 파란 셔츠)
seated_person(160, 135, (50,50,75), (200,160,115), True, (30,80,160))

# 마을 사람들 (양 옆)
# 좌측
seated_person(60, 100, SULU_BLUE, SKIN_MED)
seated_person(90, 110, SULU_GREEN, SKIN_DARK, True, SHIRT_RED)
seated_person(45, 125, SULU_BLUE, SKIN_MED)

# 우측
seated_person(260, 100, SULU_GREEN, SKIN_MED)
seated_person(235, 112, SULU_BLUE, SKIN_DARK)
seated_person(275, 128, SULU_BLUE, SKIN_MED, True, SHIRT_RED)

# Lani (우측 앞)
seated_person(210, 130, (88,108,78), SKIN_MED, True, (105,128,95))

# Mere (좌측 앞 — 주황 셔츠)
seated_person(110, 132, (58,85,55), (160,110,70), True, (205,88,42))

# ═══════════════════ 8. 따뜻한 빛 ═══════════════════
# 중앙에서 퍼지는 은은한 빛
for r_size in range(60, 20, -5):
    alpha = 15
    d.ellipse([TX-r_size, TY-r_size//2, TX+r_size, TY+r_size//2],
              fill=(LIGHT[0], LIGHT[1], LIGHT[2], alpha))

# ═══════════════════ 9. 자막 영역 ═══════════════════
d.rectangle([0, H-18, W, H], fill=(0, 0, 0, 80))

out_path = os.path.join(OUT, "sevusevu_bg.png")
img.save(out_path)
print(f"저장됨: {out_path}")
