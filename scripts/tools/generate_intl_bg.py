"""
Aid World — 국제기구 사무소 실내 배경 생성기
320×180 픽셀아트 UN/국제기구 스타일 사무소 내부
→ assets/sprites/tilesets/intl_org_bg.png
"""
from PIL import Image, ImageDraw
import os

OUT = "/Users/nddn/Documents/Claude/Projects/IDC game/assets/sprites/tilesets"
os.makedirs(OUT, exist_ok=True)

W, H = 320, 180
img = Image.new("RGB", (W, H))
draw = ImageDraw.Draw(img)

# ── 천장 (y=0~18) ──────────────────────────────────────────
CEIL = (220, 222, 228)
draw.rectangle([0, 0, W, 18], fill=CEIL)
# 형광등 (2개)
LAMP = (255, 255, 240)
LAMP_FRAME = (180, 182, 188)
for lx in [80, 220]:
    draw.rectangle([lx - 24, 2, lx + 24, 7], fill=LAMP_FRAME)
    draw.rectangle([lx - 22, 3, lx + 22, 6], fill=LAMP)

# ── 천장-벽 경계선 ──────────────────────────────────────────
draw.line([(0, 18), (W, 18)], fill=(160, 162, 170), width=2)

# ── 뒷벽 (y=18~130) ─────────────────────────────────────────
WALL = (235, 237, 242)
draw.rectangle([0, 18, W, 130], fill=WALL)

# ── 창문 (뒷벽 좌측 2개) ────────────────────────────────────
WIN_SKY = (160, 200, 235)
WIN_FRAME = (180, 182, 188)
WIN_LIGHT = (200, 230, 250)
for wx in [30, 90]:
    # 창틀
    draw.rectangle([wx, 28, wx + 38, 82], fill=WIN_FRAME)
    # 하늘
    draw.rectangle([wx + 2, 30, wx + 36, 80], fill=WIN_SKY)
    # 빛 반사
    draw.rectangle([wx + 3, 31, wx + 12, 50], fill=WIN_LIGHT)
    # 창살 (가로)
    draw.line([(wx + 2, 55), (wx + 36, 55)], fill=WIN_FRAME, width=1)
    # 창살 (세로)
    draw.line([(wx + 19, 30), (wx + 19, 80)], fill=WIN_FRAME, width=1)

# ── UN 스타일 배너 / 현수막 (뒷벽 우측) ────────────────────
UN_BLUE = (0, 90, 180)
BANNER_X = 185
# 배너 배경
draw.rectangle([BANNER_X, 22, BANNER_X + 90, 75], fill=UN_BLUE)
# 배너 테두리
draw.rectangle([BANNER_X, 22, BANNER_X + 90, 75], outline=(255, 255, 255), width=1)
# UN 엠블럼 (간략화: 원 + 선)
CX, CY = BANNER_X + 45, 40
draw.ellipse([CX - 12, CY - 12, CX + 12, CY + 12], outline=(255, 255, 255), width=1)
# 위도선 (3개)
for dy in [-5, 0, 5]:
    draw.ellipse([CX - 12, CY + dy - 3, CX + 12, CY + dy + 3], outline=(255, 255, 255), width=1)
# 경도선 (4개)
for angle_offset in [-8, 0, 8]:
    draw.line([(CX + angle_offset, CY - 12), (CX + angle_offset, CY + 12)], fill=(255, 255, 255), width=1)
# 텍스트 대체 픽셀 블록 (UN 글자)
# U
for py in range(CY + 16, CY + 22):
    draw.point([(CX - 8, py), (CX - 4, py)], fill=(255, 255, 255))
draw.line([(CX - 8, CY + 22), (CX - 4, CY + 22)], fill=(255, 255, 255))
# N
for py in range(CY + 16, CY + 22):
    draw.point([(CX + 2, py), (CX + 6, py)], fill=(255, 255, 255))
draw.line([(CX + 2, CY + 16), (CX + 6, CY + 22)], fill=(255, 255, 255))

# ── 피지 국기 소형 (뒷벽 우측 끝) ─────────────────────────
FLAG_X = 290
draw.rectangle([FLAG_X, 25, FLAG_X + 22, 38], fill=(0, 120, 200))  # 연파랑
draw.rectangle([FLAG_X, 25, FLAG_X + 22, 38], outline=(180, 180, 180))
# 깃대
draw.line([(FLAG_X - 1, 22), (FLAG_X - 1, 50)], fill=(160, 120, 60), width=1)

# ── 안내 포스터 (뒷벽 중앙 하단) ───────────────────────────
POST_C = (245, 242, 230)
draw.rectangle([148, 82, 190, 118], fill=POST_C)
draw.rectangle([148, 82, 190, 118], outline=(180, 175, 160))
# 포스터 내용 픽셀 표현 (선만)
POST_BLUE = (60, 100, 180)
draw.rectangle([152, 86, 186, 95], fill=POST_BLUE)    # 헤더
for line_y in [99, 104, 109]:
    draw.line([(153, line_y), (185, line_y)], fill=(180, 175, 160))

# ── 수납장 / 선반 (좌측 벽) ─────────────────────────────────
SHELF = (190, 175, 155)
SHELF_DARK = (160, 145, 125)
draw.rectangle([0, 28, 14, 115], fill=SHELF)
draw.rectangle([0, 28, 14, 115], outline=SHELF_DARK)
# 선반 선
for sy in [50, 72, 94]:
    draw.line([(0, sy), (14, sy)], fill=SHELF_DARK)
# 서류철 (파랑/빨강 교대)
FILE_COLORS = [(60, 80, 160), (160, 60, 60), (60, 80, 160), (160, 60, 60), (60, 80, 160)]
for i, fc in enumerate(FILE_COLORS):
    fy = 29 + i * 8
    draw.rectangle([1, fy + 1, 12, fy + 7], fill=fc)

# ── 접수 데스크 (좌측, y=95~130) ───────────────────────────
DESK = (180, 160, 130)
DESK_DARK = (140, 120, 95)
DESK_TOP = (200, 182, 152)
# 데스크 본체
draw.rectangle([20, 100, 130, 128], fill=DESK)
draw.rectangle([20, 100, 130, 128], outline=DESK_DARK)
# 데스크 상판
draw.rectangle([18, 95, 132, 102], fill=DESK_TOP)
draw.rectangle([18, 95, 132, 102], outline=DESK_DARK)
# 컴퓨터 모니터
MON_BG = (30, 32, 38)
MON_SCR = (60, 100, 180)
draw.rectangle([50, 72, 78, 96], fill=MON_BG)           # 스탠드
draw.rectangle([52, 74, 76, 94], fill=MON_SCR)          # 화면
draw.line([(64, 96), (64, 102)], fill=MON_BG, width=2)  # 목
draw.rectangle([58, 102, 70, 104], fill=MON_BG)         # 받침
# 서류 더미
PAPER = (248, 246, 236)
draw.rectangle([85, 93, 118, 97], fill=PAPER)
draw.rectangle([87, 91, 116, 95], fill=PAPER)
draw.rectangle([89, 89, 114, 93], fill=PAPER)

# ── James 데스크 (우측, y=88~128) ───────────────────────────
DESK2 = (175, 155, 125)
draw.rectangle([190, 95, 300, 126], fill=DESK2)
draw.rectangle([190, 95, 300, 126], outline=DESK_DARK)
draw.rectangle([188, 88, 302, 96], fill=DESK_TOP)
draw.rectangle([188, 88, 302, 96], outline=DESK_DARK)
# 모니터 (James 데스크)
draw.rectangle([215, 62, 245, 88], fill=MON_BG)
draw.rectangle([217, 64, 243, 86], fill=MON_SCR)
draw.line([(230, 88), (230, 94)], fill=MON_BG, width=2)
draw.rectangle([224, 94, 236, 96], fill=MON_BG)
# 서류
draw.rectangle([253, 86, 292, 90], fill=PAPER)
draw.rectangle([255, 84, 290, 88], fill=PAPER)
# 책 (James 데스크 우측)
BOOK_COLORS = [(80, 100, 160), (160, 90, 60), (60, 130, 80)]
for i, bc in enumerate(BOOK_COLORS):
    bx = 274 + i * 7
    draw.rectangle([bx, 72, bx + 5, 88], fill=bc)

# ── 바닥 (y=128~180) ─────────────────────────────────────────
FLOOR = (205, 198, 185)
FLOOR_LINE = (185, 178, 165)
draw.rectangle([0, 128, W, H], fill=FLOOR)
# 타일 줄눈 (가로)
for fy in range(128, H, 12):
    draw.line([(0, fy), (W, fy)], fill=FLOOR_LINE)
# 타일 줄눈 (세로)
for fx in range(0, W, 24):
    for fy in range(128, H, 24):
        draw.line([(fx, fy), (fx, fy + 12)], fill=FLOOR_LINE)

# ── 이동 경로 가이드 (출구 힌트 zone y=165~180) — 텍스트 없이 바닥만
EXIT_MARK = (185, 178, 168)
draw.rectangle([120, 168, 200, 176], fill=EXIT_MARK)

# ── 저장 ─────────────────────────────────────────────────────
out_path = os.path.join(OUT, "intl_org_bg.png")
img.save(out_path)
print(f"저장 완료: {out_path}")
