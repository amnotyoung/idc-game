"""
피지 정부청사 회의실 배경 생성
320x180 픽셀아트 — 권위적이고 약간 답답한 분위기
출력: assets/sprites/tilesets/government_bg.png
"""
from PIL import Image, ImageDraw
import os

OUT = "/Users/nddn/Documents/Claude/Projects/IDC game/assets/sprites/tilesets"
os.makedirs(OUT, exist_ok=True)

W, H = 320, 180
img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
d = ImageDraw.Draw(img)

# ─── 색상 팔레트 ───
WALL_BASE   = (225, 218, 200, 255)   # 크림/베이지 벽
WALL_SHADOW = (205, 196, 178, 255)   # 벽 아래 그림자
MOLDING     = (210, 200, 182, 255)   # 몰딩 라인
FLOOR_A     = (148, 102, 58, 255)    # 나무 마루 A
FLOOR_B     = (135, 92, 50, 255)     # 나무 마루 B
FLOOR_C     = (160, 115, 68, 255)    # 나무 마루 C (밝은 줄)
TABLE_TOP   = (68, 38, 18, 255)      # 마호가니 테이블 상면
TABLE_SIDE  = (48, 25, 10, 255)      # 테이블 측면 (어둡게)
TABLE_EDGE  = (85, 50, 24, 255)      # 테이블 엣지 하이라이트
CHAIR_SEAT  = (58, 32, 14, 255)      # 의자 시트
CHAIR_BACK  = (48, 25, 10, 255)      # 의자 등받이
CHAIR_LEG   = (42, 20, 8, 255)       # 의자 다리
WINDOW_SKY  = (130, 185, 230, 255)   # 하늘
WINDOW_SKY2 = (160, 205, 245, 255)   # 밝은 하늘
WINDOW_FRAME= (195, 188, 170, 255)   # 창문 프레임
WINDOW_SILL = (180, 172, 152, 255)   # 창틀
CLOUD       = (245, 248, 252, 255)   # 구름
PAPER       = (240, 236, 220, 255)   # 서류 색상
PAPER2      = (228, 224, 208, 255)   # 서류 어두운
FLAG_BG     = (12, 56, 132, 255)     # 피지 국기 파랑
FLAG_CROSS  = (255, 255, 255, 255)   # 흰 십자
FLAG_FRAME  = (175, 148, 105, 255)   # 액자 프레임
CERT_FRAME  = (148, 118, 75, 255)    # 학위증 액자
CERT_BG     = (248, 242, 225, 255)   # 학위증 배경
DOOR_WOOD   = (118, 78, 38, 255)     # 문 나무색
DOOR_FRAME  = (98, 62, 28, 255)      # 문 프레임
DOOR_PANEL  = (105, 68, 32, 255)     # 문 패널
DOOR_KNOB   = (188, 155, 85, 255)    # 문 손잡이
CEIL        = (235, 230, 215, 255)   # 천장

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. 천장
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
d.rectangle([0, 0, W-1, 38], fill=CEIL)
# 천장 몰딩 라인 (오래된 건물 느낌)
d.line([0, 38, W-1, 38], fill=MOLDING, width=2)
d.line([0, 40, W-1, 40], fill=(195, 185, 165, 255), width=1)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. 벽 (천장 아래 ~ 바닥 위)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
d.rectangle([0, 38, W-1, 115], fill=WALL_BASE)
# 벽 하단 몰딩 라인 (걸레받이)
d.rectangle([0, 110, W-1, 115], fill=MOLDING)
d.line([0, 110, W-1, 110], fill=(185, 175, 155, 255), width=1)
d.line([0, 115, W-1, 115], fill=(185, 175, 155, 255), width=1)

# 벽 약간 텍스처 (오래된 벽 느낌 — 미세한 수직선)
for x in range(10, W, 18):
    d.line([x, 42, x, 109], fill=(218, 210, 192, 255), width=1)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. 바닥 (나무 마루 패턴)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
d.rectangle([0, 115, W-1, H-1], fill=FLOOR_A)

# 마루 판자 줄 (가로 라인)
for y in range(115, H, 5):
    d.line([0, y, W-1, y], fill=FLOOR_B, width=1)

# 마루 판자 결 (대각선 느낌 — 세로 줄)
plank_colors = [FLOOR_A, FLOOR_B, FLOOR_C, FLOOR_B, FLOOR_A, FLOOR_C]
plank_w = 18
for xi, x in enumerate(range(0, W, plank_w)):
    col = plank_colors[xi % len(plank_colors)]
    d.rectangle([x, 115, x + plank_w - 2, H-1], fill=col)
    # 판자 경계선
    d.line([x + plank_w - 1, 115, x + plank_w - 1, H-1], fill=FLOOR_B, width=1)

# 마루 광택 (상단 하이라이트)
for x in range(0, W, plank_w):
    d.line([x, 115, x + plank_w - 2, 115], fill=FLOOR_C, width=1)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. 창문 2개 (상단 벽)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def draw_window(d, wx, wy, ww, wh):
    """창문 그리기"""
    # 하늘
    d.rectangle([wx+3, wy+3, wx+ww-3, wy+wh-3], fill=WINDOW_SKY)
    # 밝은 하늘 위쪽
    d.rectangle([wx+3, wy+3, wx+ww-3, wy+wh//2], fill=WINDOW_SKY2)
    # 구름 (작게)
    cx1, cy1 = wx + ww//4, wy + 8
    d.ellipse([cx1-6, cy1-2, cx1+6, cy1+2], fill=CLOUD)
    d.ellipse([cx1-3, cy1-4, cx1+3, cy1], fill=CLOUD)
    cx2, cy2 = wx + 3*ww//4, wy + 12
    d.ellipse([cx2-5, cy2-2, cx2+5, cy2+2], fill=CLOUD)
    d.ellipse([cx2-2, cy2-4, cx2+2, cy2], fill=CLOUD)
    # 창문 프레임
    d.rectangle([wx, wy, wx+ww, wy+wh], outline=WINDOW_FRAME, width=3)
    # 창문 십자 (가로/세로 분리)
    mid_x = wx + ww // 2
    mid_y = wy + wh // 2
    d.line([mid_x, wy, mid_x, wy+wh], fill=WINDOW_FRAME, width=2)
    d.line([wx, mid_y, wx+ww, mid_y], fill=WINDOW_FRAME, width=2)
    # 창틀 (외곽)
    d.rectangle([wx-2, wy-2, wx+ww+2, wy+wh+2], outline=WINDOW_SILL, width=2)
    # 창틀 아래 선반
    d.rectangle([wx-4, wy+wh+2, wx+ww+4, wy+wh+5], fill=WINDOW_SILL)

draw_window(d, 45, 44, 52, 40)
draw_window(d, 222, 44, 52, 40)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 5. 피지 국기 액자 (중앙 상단 벽)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
fx, fy = 140, 46
fw, fh = 40, 26
# 액자 외곽
d.rectangle([fx-3, fy-3, fx+fw+3, fy+fh+3], fill=FLAG_FRAME)
d.rectangle([fx-2, fy-2, fx+fw+2, fy+fh+2], fill=(145, 118, 72, 255))
# 국기 배경 (하늘색)
d.rectangle([fx, fy, fx+fw, fy+fh], fill=FLAG_BG)
# 흰 십자 (유니언 잭 단순화)
d.line([fx, fy, fx+fw//2, fy+fh//2], fill=FLAG_CROSS, width=1)
d.line([fx+fw, fy, fx+fw//2, fy+fh//2], fill=FLAG_CROSS, width=1)
d.line([fx+fw//2, fy, fx+fw//2, fy+fh], fill=FLAG_CROSS, width=2)
d.line([fx, fy+fh//2, fx+fw, fy+fh//2], fill=FLAG_CROSS, width=2)
# 오른쪽 문장 (단순화 — 흰 방패 모양)
shield_x = fx + fw//2 + 5
d.polygon([
    shield_x, fy+3,
    shield_x+10, fy+3,
    shield_x+10, fy+fh-5,
    shield_x+5, fy+fh-1,
    shield_x, fy+fh-5
], fill=(245, 242, 235, 255))
# 액자 유리 반짝임
d.line([fx+1, fy+1, fx+fw//3, fy+fh//4], fill=(200, 220, 245, 60), width=1)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 6. 학위증/표창장 액자들
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def draw_cert(d, cx, cy, cw, ch):
    """학위증/표창장 액자"""
    d.rectangle([cx-2, cy-2, cx+cw+2, cy+ch+2], fill=CERT_FRAME)
    d.rectangle([cx, cy, cx+cw, cy+ch], fill=CERT_BG)
    # 내용 (텍스트 라인 흉내)
    for li, ly in enumerate(range(cy+4, cy+ch-2, 4)):
        line_w = cw - 8 if li % 3 != 1 else cw - 16
        d.line([cx+4, ly, cx+4+line_w, ly], fill=(160, 145, 115, 255), width=1)
    # 상단 장식선
    d.line([cx+2, cy+2, cx+cw-2, cy+2], fill=(148, 118, 75, 255), width=1)

draw_cert(d, 12, 50, 28, 20)   # 왼쪽 작은 액자
draw_cert(d, 15, 76, 22, 16)   # 왼쪽 두번째
draw_cert(d, 278, 50, 28, 20)  # 오른쪽 액자
draw_cert(d, 280, 76, 22, 16)  # 오른쪽 두번째

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 7. 회의 테이블 (마호가니, 중앙)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
tx, ty = 55, 88
tw, th = 210, 38

# 테이블 측면 (두께감)
d.rectangle([tx, ty+th, tx+tw, ty+th+8], fill=TABLE_SIDE)
# 테이블 상면
d.rectangle([tx, ty, tx+tw, ty+th], fill=TABLE_TOP)
# 테이블 상면 엣지 하이라이트
d.line([tx, ty, tx+tw, ty], fill=TABLE_EDGE, width=2)
d.line([tx, ty, tx, ty+th], fill=TABLE_EDGE, width=1)
d.line([tx+tw, ty, tx+tw, ty+th], fill=(42, 20, 8, 255), width=1)
# 테이블 목재 결 (가로 라인)
for gy in range(ty+4, ty+th, 6):
    d.line([tx+2, gy, tx+tw-2, gy], fill=(55, 30, 12, 255), width=1)
# 테이블 광택
d.rectangle([tx+5, ty+2, tx+tw//3, ty+5], fill=(85, 52, 26, 100))

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 8. 의자들 (테이블 주변)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def draw_chair_back(d, cx, cy):
    """테이블 상단(위쪽)에 등받이만 보이는 의자"""
    # 등받이
    d.rectangle([cx-6, cy-10, cx+6, cy-3], fill=CHAIR_BACK)
    d.rectangle([cx-5, cy-9, cx+5, cy-4], fill=(62, 35, 15, 255))
    # 등받이 다리 두 개
    d.rectangle([cx-5, cy-3, cx-3, cy+1], fill=CHAIR_LEG)
    d.rectangle([cx+3, cy-3, cx+5, cy+1], fill=CHAIR_LEG)

def draw_chair_front(d, cx, cy):
    """테이블 하단(앞쪽)에 앉는 면 + 앞다리 보이는 의자"""
    # 앉는 면
    d.rectangle([cx-6, cy, cx+6, cy+5], fill=CHAIR_SEAT)
    d.line([cx-6, cy, cx+6, cy], fill=(68, 40, 18, 255), width=1)
    # 앞다리
    d.rectangle([cx-5, cy+5, cx-3, cy+10], fill=CHAIR_LEG)
    d.rectangle([cx+3, cy+5, cx+5, cy+10], fill=CHAIR_LEG)

# 테이블 상단 의자들 (등받이만)
chair_top_y = ty - 2
for cx in [80, 115, 160, 205, 240]:
    draw_chair_back(d, cx, chair_top_y)

# 테이블 하단 의자들 (앞면)
chair_bot_y = ty + th + 8
for cx in [80, 130, 185, 240]:
    draw_chair_front(d, cx, chair_bot_y)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 9. Timoci 자리 — 테이블 상단 중앙 (서류 쌓임)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
timoci_x = 155
# 서류 스택
d.rectangle([timoci_x-14, ty+4, timoci_x+14, ty+10], fill=PAPER)
d.rectangle([timoci_x-12, ty+2, timoci_x+12, ty+8], fill=PAPER2)
d.rectangle([timoci_x-13, ty+1, timoci_x+13, ty+7], fill=PAPER)
# 서류 위 텍스트 라인 (흉내)
for li in range(3):
    d.line([timoci_x-10, ty+2+li*2, timoci_x+10, ty+2+li*2], fill=(175, 165, 140, 255), width=1)
# 서류 클립/스테이플러 흉내
d.rectangle([timoci_x+8, ty+1, timoci_x+12, ty+3], fill=(125, 125, 125, 200))

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 10. 왼쪽 하단 문 (출구 방향)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
dx, dy = 10, 115
dw, dh = 32, 65
# 문 프레임 (두껍게)
d.rectangle([dx-3, dy-3, dx+dw+3, H], fill=DOOR_FRAME)
# 문짝
d.rectangle([dx, dy, dx+dw, H], fill=DOOR_WOOD)
# 문 패널 (2개)
d.rectangle([dx+3, dy+4, dx+dw-3, dy+dh//2-2], fill=DOOR_PANEL)
d.rectangle([dx+3, dy+dh//2+2, dx+dw-3, H-4], fill=DOOR_PANEL)
# 문 패널 내부 선
d.rectangle([dx+4, dy+5, dx+dw-4, dy+dh//2-3], outline=(90, 58, 24, 255), width=1)
d.rectangle([dx+4, dy+dh//2+3, dx+dw-4, H-5], outline=(90, 58, 24, 255), width=1)
# 문 손잡이
d.ellipse([dx+dw-7, dy+dh//2-3, dx+dw-3, dy+dh//2+1], fill=DOOR_KNOB)
# 문 세로 몰딩
d.line([dx, dy, dx, H], fill=DOOR_FRAME, width=1)
d.line([dx+dw, dy, dx+dw, H], fill=DOOR_FRAME, width=1)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 11. 마무리 — 전체적인 분위기 강화
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 창문 빛줄기 (왼쪽 창문에서 바닥으로)
for bi in range(5):
    bx_start = 45 + bi * 8
    bx_end   = bx_start + 35
    d.polygon([
        bx_start, 84,
        bx_end,   84,
        bx_end + 12, H,
        bx_start + 4, H
    ], fill=(255, 245, 210, 8))

# 창문 빛줄기 (오른쪽 창문)
for bi in range(5):
    bx_start = 222 + bi * 8
    bx_end   = bx_start + 35
    d.polygon([
        bx_start, 84,
        bx_end,   84,
        bx_end + 12, H,
        bx_start + 4, H
    ], fill=(255, 245, 210, 8))

# 전체 약한 비네팅 (가장자리 어둡게 — 답답한 느낌)
for xi in range(0, 30, 2):
    alpha = int(35 * (1 - xi / 30))
    d.line([xi, 0, xi, H], fill=(0, 0, 0, alpha), width=1)
    d.line([W-1-xi, 0, W-1-xi, H], fill=(0, 0, 0, alpha), width=1)

# 저장
out_path = os.path.join(OUT, "government_bg.png")
img.save(out_path)
print(f"저장됨: government_bg.png ({W}x{H})")
