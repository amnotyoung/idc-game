"""
바다 전환 컷 — 바다 한가운데
모터보트가 바다를 가르며 달리고, 바다새가 날고,
수면 아래로 물고기와 거북이가 보이는 픽셀아트
320x180
"""
from PIL import Image, ImageDraw
import os, random

random.seed(42)
OUT = "/Users/nddn/Documents/Claude/Projects/IDC game/assets/sprites/tilesets"
os.makedirs(OUT, exist_ok=True)

W, H = 320, 180
img = Image.new("RGBA", (W, H))
d = ImageDraw.Draw(img)

# ═══════════════════ 팔레트 ═══════════════════
SKY_TOP  = (42, 108, 195)
SKY_BOT  = (115, 188, 240)
CLOUD    = (232, 240, 250)
CLOUD_D  = (210, 225, 242)

SEA_TOP  = (52, 168, 158)    # 수면 (에메랄드)
SEA_MID  = (38, 135, 135)    # 중간
SEA_DEEP = (22, 75, 95)      # 심해
SEA_GLOW = (95, 205, 185)    # 반짝임
FOAM     = (205, 238, 228)   # 거품

BOAT_HULL  = (28, 82, 148)
BOAT_LIGHT = (52, 112, 175)
BOAT_INT   = (218, 212, 200)
MOTOR      = (48, 50, 55)
WINDSHIELD = (175, 212, 238)
WAKE       = (175, 225, 215)  # 물보라

BIRD_COL = (45, 42, 38)

FISH_A   = (218, 165, 55)    # 노란 물고기
FISH_B   = (55, 145, 195)    # 파란 물고기
FISH_C   = (195, 85, 55)     # 주황 물고기

TURTLE_SHELL = (62, 108, 55)
TURTLE_SHELL_D = (45, 82, 38)
TURTLE_SKIN  = (88, 145, 75)
TURTLE_BELLY = (165, 185, 128)

CORAL_A  = (195, 95, 75)     # 산호
CORAL_B  = (165, 55, 85)
CORAL_C  = (218, 148, 55)
SEAWEED  = (32, 95, 52)
SEAWEED_L = (48, 125, 65)

SAND_BOT = (148, 135, 108)
SAND_D   = (128, 115, 92)

# ═══════════════════ 1. 하늘 (y=0~55) ═══════════════════
for y in range(56):
    t = y / 55
    r = int(SKY_TOP[0] + (SKY_BOT[0] - SKY_TOP[0]) * t)
    g = int(SKY_TOP[1] + (SKY_BOT[1] - SKY_TOP[1]) * t)
    b = int(SKY_TOP[2] + (SKY_BOT[2] - SKY_TOP[2]) * t)
    d.line([0, y, W, y], fill=(r, g, b, 255))

# 구름
for cx, cy, cw, ch in [(20,12,65,18),(110,8,55,14),(210,15,50,12),(280,5,35,10),(155,22,40,10)]:
    d.ellipse([cx, cy, cx+cw, cy+ch], fill=(*CLOUD_D, 200))
    d.ellipse([cx+3, cy-2, cx+cw-5, cy+ch-3], fill=(*CLOUD, 200))

# ═══════════════════ 2. 수면 (y=55~70, 투명층) ═══════════════════
for y in range(55, 72):
    t = (y - 55) / 16
    r = int(SEA_TOP[0] * (1 - t*0.3))
    g = int(SEA_TOP[1] * (1 - t*0.15))
    b = int(SEA_TOP[2] * (1 - t*0.1))
    d.line([0, y, W, y], fill=(r, g, b, 255))

# 수면 반짝임
for _ in range(40):
    x = random.randint(0, W)
    y = random.randint(56, 68)
    w = random.randint(4, 12)
    d.line([x, y, x+w, y], fill=(*SEA_GLOW, 150))

# ═══════════════════ 3. 수중 (y=70~180) ═══════════════════
for y in range(70, H):
    t = (y - 70) / (H - 70)
    r = int(SEA_MID[0] + (SEA_DEEP[0] - SEA_MID[0]) * t)
    g = int(SEA_MID[1] + (SEA_DEEP[1] - SEA_MID[1]) * t)
    b = int(SEA_MID[2] + (SEA_DEEP[2] - SEA_MID[2]) * t)
    d.line([0, y, W, y], fill=(r, g, b, 255))

# 빛줄기 (수면에서 내려오는 사선 빛)
for bx in [40, 120, 200, 280]:
    for i in range(40):
        x1 = bx + i
        y1 = 72 + i * 2
        d.line([x1, y1, x1+3, y1], fill=(85, 175, 165, 40))

# ═══════════════════ 4. 해저 (y=155~180) ═══════════════════
# 모래
for y in range(158, H):
    t = (y - 158) / 22
    r = int(SAND_BOT[0] + (SAND_D[0] - SAND_BOT[0]) * t * 0.5)
    g = int(SAND_BOT[1] + (SAND_D[1] - SAND_BOT[1]) * t * 0.5)
    b = int(SAND_BOT[2] + (SAND_D[2] - SAND_BOT[2]) * t * 0.5)
    d.line([0, y, W, y], fill=(r, g, b, 200))

# 산호
corals = [(30,158,12,8,CORAL_A),(80,155,10,12,CORAL_B),(140,160,14,8,CORAL_C),
          (210,157,10,10,CORAL_A),(270,159,12,7,CORAL_B),(310,156,8,10,CORAL_C)]
for cx, cy, cw, ch, col in corals:
    d.ellipse([cx, cy-ch, cx+cw, cy], fill=(*col, 200))
    d.ellipse([cx+2, cy-ch+2, cx+cw-2, cy-2], fill=(col[0]+20, col[1]+20, col[2]+20, 180))

# 해초
for sx in [20, 65, 115, 175, 235, 290]:
    h = random.randint(15, 30)
    for i in range(h):
        sway = int(3 * ((i/h)**0.5) * (1 if sx%2==0 else -1))
        col = SEAWEED if i < h//2 else SEAWEED_L
        d.rectangle([sx+sway, 160-i, sx+sway+2, 162-i], fill=(*col, 180))

# ═══════════════════ 5. 물고기들 ═══════════════════
def draw_fish(fx, fy, size, col, direction=1):
    """작은 열대어"""
    # 몸통 (타원)
    d.ellipse([fx, fy, fx+size*2, fy+size], fill=(*col, 220))
    # 꼬리 (삼각형)
    tail_x = fx if direction > 0 else fx + size*2
    d.polygon([
        (tail_x, fy + size//2),
        (tail_x - size*direction, fy),
        (tail_x - size*direction, fy + size)
    ], fill=(*col, 200))
    # 눈
    eye_x = fx + size*2 - 2 if direction > 0 else fx + 2
    d.ellipse([eye_x-1, fy+size//3, eye_x+1, fy+size//3+2], fill=(255,255,255,220))
    d.point((eye_x, fy+size//3+1), fill=(20,20,25,220))

# 물고기 무리 (좌하단)
for i in range(5):
    x = 35 + i * 12 + random.randint(-3, 3)
    y = 110 + random.randint(-5, 5)
    draw_fish(x, y, 4, FISH_A, 1)

# 파란 물고기 (중앙)
for i in range(4):
    x = 155 + i * 14 + random.randint(-4, 4)
    y = 125 + random.randint(-4, 4)
    draw_fish(x, y, 5, FISH_B, -1)

# 주황 물고기 (우하단)
for i in range(3):
    x = 240 + i * 15 + random.randint(-3, 3)
    y = 140 + random.randint(-3, 3)
    draw_fish(x, y, 4, FISH_C, 1)

# ═══════════════════ 6. 거북이 ═══════════════════
TX, TY = 190, 95  # 수면 근처에서 유영
# 등딱지 (타원)
d.ellipse([TX-10, TY-6, TX+10, TY+6], fill=(*TURTLE_SHELL, 220))
d.ellipse([TX-8, TY-4, TX+8, TY+4], fill=(*TURTLE_SHELL_D, 200))
# 등딱지 무늬 (육각형 느낌)
for ox, oy in [(-4,-2),(0,-3),(4,-2),(-4,1),(0,2),(4,1)]:
    d.rectangle([TX+ox, TY+oy, TX+ox+2, TY+oy+2], fill=(*TURTLE_SHELL, 180))
# 머리
d.ellipse([TX+9, TY-3, TX+16, TY+3], fill=(*TURTLE_SKIN, 220))
d.point((TX+14, TY-1), fill=(20,20,25,200))  # 눈
# 앞 지느러미
d.polygon([(TX-5, TY-5), (TX-12, TY-10), (TX-8, TY-3)], fill=(*TURTLE_SKIN, 200))
d.polygon([(TX-5, TY+5), (TX-12, TY+10), (TX-8, TY+3)], fill=(*TURTLE_SKIN, 200))
# 뒷 지느러미
d.polygon([(TX-8, TY-2), (TX-14, TY-1), (TX-10, TY+2)], fill=(*TURTLE_SKIN, 160))
# 배
d.ellipse([TX-6, TY-2, TX+6, TY+4], fill=(*TURTLE_BELLY, 120))

# ═══════════════════ 7. 모터보트 (나이탬바/수바 항구와 완전 동일 구조 × 1.5배) ═══════════════════
# 항구 보트: BX1=176,BX2=214,BY1=150,BY2=162 (38×12px)
# 전환씬: 1.5배 = 57×18px
HULL_DARK  = (28, 82, 148)
HULL_LIGHT = (52, 112, 175)
INTERIOR   = (218, 212, 200)
MOTOR_BODY = (48, 50, 55)
MOTOR_ARM  = (38, 40, 44)
WINDSHIELD = (175, 212, 238)

BX1, BX2 = 110, 167   # 57px 폭
BY1, BY2 = 40, 58     # 18px 높이

# 선체 (나이탬바와 동일한 뾰족한 폴리곤)
hull_pts = [
    (BX1 + 6, BY2), (BX1,     BY1 + 9),
    (BX1,     BY1 + 5),
    (BX1 + 9, BY1),
    (BX2 - 3, BY1),
    (BX2,     BY1 + 6),
    (BX2,     BY2 - 2),
]
d.polygon(hull_pts, fill=(*HULL_DARK, 255))
# 선체 상단 하이라이트
d.line([(BX1 + 9, BY1), (BX2 - 3, BY1)], fill=(*HULL_LIGHT, 255), width=2)
d.line([(BX1, BY1 + 5), (BX1 + 9, BY1)], fill=(*HULL_LIGHT, 255), width=1)
# 선내 (베이지)
d.rectangle([BX1 + 8, BY1 + 3, BX2 - 6, BY1 + 11], fill=(*INTERIOR, 255))
# 앞유리 (조종석 바람막이)
d.polygon([
    (BX1 + 12, BY1 + 3), (BX1 + 18, BY1 - 3),
    (BX1 + 30, BY1 - 3), (BX1 + 33, BY1 + 3)
], fill=(*WINDSHIELD, 230))
d.line([(BX1 + 12, BY1 + 3), (BX1 + 18, BY1 - 3)], fill=(120,160,195,255), width=1)
d.line([(BX1 + 18, BY1 - 3), (BX1 + 30, BY1 - 3)], fill=(120,160,195,255), width=1)
# 선외기 (오른쪽 끝)
d.rectangle([BX2 - 2, BY1 + 3, BX2 + 6, BY1 + 14], fill=(*MOTOR_BODY, 255))
d.rectangle([BX2 + 3, BY1 + 14, BX2 + 6, BY2 - 2], fill=(*MOTOR_ARM, 255))
d.rectangle([BX2,     BY2 - 3, BX2 + 8, BY2],     fill=(*MOTOR_BODY, 255))

# 물보라 (선외기 뒤)
for i in range(12):
    wx = BX2 + 10 + i * 6
    wy = BY1 + 8 + random.randint(-3, 3)
    alpha = max(30, 220 - i * 17)
    d.ellipse([wx, wy, wx+8, wy+5], fill=(*WAKE, alpha))
    d.ellipse([wx+2, wy-1, wx+6, wy+3], fill=(*FOAM, alpha))
# 뱃머리 물살
for i in range(6):
    wx = BX1 - 4 - i * 4
    wy = BY1 + 10 + i * 2
    d.ellipse([wx, wy, wx+6, wy+4], fill=(*FOAM, 170 - i*25))

# 탑승자 (주인공 + 뱃사공)
# 뱃사공 (선외기 쪽, 피지인)
d.rectangle([BX2 - 14, BY1 - 6, BX2 - 8, BY1 + 3], fill=(140,95,60,230))
d.rectangle([BX2 - 15, BY1 - 10, BX2 - 7, BY1 - 5], fill=(140,95,60,230))
d.rectangle([BX2 - 15, BY1 - 10, BX2 - 7, BY1 - 8], fill=(15,10,5,230))
# 주인공 (앞쪽, KODA 파란 셔츠)
d.rectangle([BX1 + 16, BY1 - 6, BX1 + 24, BY1 + 3], fill=(30,80,160,230))
d.rectangle([BX1 + 15, BY1 - 10, BX1 + 25, BY1 - 5], fill=(200,160,115,230))
d.rectangle([BX1 + 15, BY1 - 13, BX1 + 25, BY1 - 9], fill=(30,20,10,230))

# ═══════════════════ 8. 바다새 ═══════════════════
def draw_bird(bx, by, size=6, open=True):
    if open:
        # 날개 펼침 (V자)
        d.line([(bx-size, by-size//2), (bx, by), (bx+size, by-size//2)],
               fill=(*BIRD_COL, 230), width=2)
    else:
        # 날개 접힘 (얇은 V)
        d.line([(bx-size//2, by-1), (bx, by), (bx+size//2, by-1)],
               fill=(*BIRD_COL, 230), width=1)
    # 머리
    d.ellipse([bx-1, by-1, bx+1, by+1], fill=(*BIRD_COL, 230))

draw_bird(85, 20, 8, True)
draw_bird(105, 28, 6, False)
draw_bird(70, 32, 7, True)
draw_bird(250, 18, 9, True)
draw_bird(268, 25, 5, False)

# ═══════════════════ 9. 수면 경계선 ═══════════════════
# 수면 반사/굴절 경계
for x in range(0, W, 5):
    fy = 55 + (x % 7) // 3
    d.line([x, fy, x+3, fy], fill=(*SEA_GLOW, 180))

# ═══════════════════ 10. 자막 영역 ═══════════════════
d.rectangle([0, H-20, W, H], fill=(0, 0, 0, 90))

# ═══════════════════ 저장 ═══════════════════
out_path = os.path.join(OUT, "sea_transition.png")
img.save(out_path)
print(f"저장됨: {out_path}")
