"""
Aid World — 사무실 배경 생성기 (외부 의존 없음)
밝고 깔끔한 현대 사무실 느낌, 320x180
"""
from PIL import Image, ImageDraw
import os

OUT = "/Users/nddn/Documents/Claude/Projects/IDC game/assets/sprites/tilesets"
os.makedirs(OUT, exist_ok=True)

W, H = 320, 180
img = Image.new("RGBA", (W, H), (0,0,0,255))
d = ImageDraw.Draw(img)

# ── 팔레트 ──
WALL      = (230, 222, 210, 255)   # 크림색 벽
WALL_DARK = (190, 182, 168, 255)   # 벽 그림자/몰딩
FLOOR     = (195, 168, 130, 255)   # 나무 바닥 밝은 부분
FLOOR2    = (182, 156, 118, 255)   # 나무 바닥 어두운 부분
FLOOR_LINE= (165, 140, 105, 255)   # 나무 바닥 결
BASEBOARD = (160, 145, 125, 255)   # 걸레받이
DESK_TOP  = (220, 200, 170, 255)   # 책상 상판 (밝은 나무)
DESK_SIDE = (170, 148, 118, 255)   # 책상 측면
DESK_SHAD = (140, 120, 92,  255)   # 책상 그림자
MONITOR   = (45,  45,  55,  255)   # 모니터 베젤
SCREEN    = (120, 190, 220, 255)   # 화면
SCREEN2   = (80, 150, 190, 255)    # 화면 반사
CHAIR_B   = (70,  95, 145, 255)    # 의자 파란색
CHAIR_D   = (50,  72, 112, 255)    # 의자 어두운
PAPER     = (245, 242, 235, 255)   # 서류
PAPER_L   = (210, 206, 195, 255)   # 서류 줄
SHELF     = (175, 145, 105, 255)   # 책장 나무
SHELF_D   = (140, 112, 78,  255)   # 책장 어두운
BOOK_R    = (185, 60,  55,  255)
BOOK_B    = (55,  100, 175, 255)
BOOK_G    = (55,  145, 70,  255)
BOOK_Y    = (210, 165, 40,  255)
WINDOW    = (185, 220, 240, 255)   # 창문 하늘
WINDOW_F  = (155, 195, 220, 255)   # 창문 반사
FRAME     = (160, 145, 125, 255)   # 창문 프레임
PLANT_G   = (60,  148, 72,  255)   # 화분 잎
PLANT_D   = (42,  112, 54,  255)   # 잎 어두운
POT       = (165, 95,  55,  255)   # 화분
DOOR_W    = (215, 195, 165, 255)   # 문 나무
DOOR_D    = (175, 152, 118, 255)   # 문 어두운
DOOR_F    = (140, 118, 88,  255)   # 문틀
RUG       = (150, 85,  80,  255)   # 러그
RUG_L     = (170, 100, 95,  255)

# ════════════════════════════════
# 1. 벽 (크림색)
# ════════════════════════════════
d.rectangle([0, 0, W-1, H-1], fill=WALL)

# 벽 아랫부분 살짝 다른 톤 (wainscoting 느낌)
d.rectangle([0, 100, W-1, H-1], fill=(220, 212, 198, 255))
d.line([0, 100, W-1, 100], fill=WALL_DARK, width=1)

# 걸레받이
d.rectangle([0, H-14, W-1, H-1], fill=BASEBOARD)
d.line([0, H-14, W-1, H-14], fill=WALL_DARK, width=1)

# ════════════════════════════════
# 2. 바닥 (나무 결 패턴)
# ════════════════════════════════
FLOOR_Y = 105
for y in range(FLOOR_Y, H-13):
    base = FLOOR if (y // 4) % 2 == 0 else FLOOR2
    d.line([0, y, W-1, y], fill=base, width=1)

# 나무 결 세로선
for x in range(0, W, 18):
    offset = (x // 18) % 3 * 6
    for y in range(FLOOR_Y, H-13, 12):
        d.line([x + offset, y, x + offset, y+10], fill=FLOOR_LINE, width=1)

# ════════════════════════════════
# 3. 창문 (상단 벽)
# ════════════════════════════════
for wx in [30, 90, 180, 240]:
    # 창문 외부 프레임
    d.rectangle([wx, 4, wx+36, 52], fill=FRAME)
    # 유리
    d.rectangle([wx+3, 7, wx+33, 49], fill=WINDOW)
    # 반사광
    d.polygon([wx+3,7, wx+12,7, wx+3,20], fill=WINDOW_F)
    # 창문 십자 프레임
    d.line([wx+18, 7, wx+18, 49], fill=FRAME, width=2)
    d.line([wx+3, 28, wx+33, 28], fill=FRAME, width=2)

# ════════════════════════════════
# 4. 문 (상단 중앙)
# ════════════════════════════════
d.rectangle([142, 0, 178, 65], fill=DOOR_F)   # 문틀
d.rectangle([145, 0, 175, 63], fill=DOOR_W)   # 문 패널
# 문 패널 디테일
d.rectangle([148, 5, 172, 30], fill=DOOR_D)
d.rectangle([149, 6, 171, 29], fill=DOOR_W)
d.rectangle([148, 35, 172, 60], fill=DOOR_D)
d.rectangle([149, 36, 171, 59], fill=DOOR_W)
# 손잡이
d.ellipse([167, 30, 172, 35], fill=(180, 155, 80, 255))

# ════════════════════════════════
# 5. 책장 (좌측 벽)
# ════════════════════════════════
d.rectangle([8, 8, 42, 98], fill=SHELF)
d.rectangle([8, 8, 42, 98], outline=SHELF_D, width=1)
# 선반 구분선
for sy in [30, 52, 74]:
    d.line([9, sy, 41, sy], fill=SHELF_D, width=1)
# 책들
books = [BOOK_R, BOOK_B, BOOK_G, BOOK_Y, BOOK_R, BOOK_B]
for row, y0 in enumerate([10, 32, 54, 76]):
    for i, bc in enumerate(books[:4]):
        bx = 10 + i*7
        d.rectangle([bx, y0+1, bx+5, y0+18], fill=bc)

# ════════════════════════════════
# 6. 메인 책상 (좌측)
# ════════════════════════════════
# 책상 그림자
d.rectangle([48, 66, 122, 72], fill=DESK_SHAD)
# 책상 상판
d.rectangle([46, 52, 120, 66], fill=DESK_TOP)
d.rectangle([46, 52, 120, 66], outline=DESK_SIDE, width=1)
# 책상 앞면
d.rectangle([46, 64, 120, 70], fill=DESK_SIDE)

# 모니터
d.rectangle([68, 35, 88, 50], fill=MONITOR)
d.rectangle([70, 37, 86, 48], fill=SCREEN)
d.polygon([70,37, 76,37, 70,43], fill=SCREEN2)
d.rectangle([76, 50, 80, 53], fill=MONITOR)
d.rectangle([74, 53, 82, 54], fill=MONITOR)

# 키보드
d.rectangle([56, 55, 70, 61], fill=(90, 92, 102, 255))
for kx in range(58, 70, 3):
    d.line([kx, 56, kx, 60], fill=(70, 72, 82, 255), width=1)

# 서류
d.rectangle([90, 54, 116, 64], fill=PAPER)
for ly in range(56, 63, 3):
    d.line([92, ly, 114, ly], fill=PAPER_L, width=1)

# 의자
d.rectangle([72, 72, 88, 88], fill=CHAIR_B)
d.rectangle([72, 72, 88, 88], outline=CHAIR_D, width=1)
d.rectangle([74, 70, 86, 73], fill=CHAIR_B)   # 등받이

# ════════════════════════════════
# 7. 보조 책상 (우측)
# ════════════════════════════════
d.rectangle([198, 66, 272, 72], fill=DESK_SHAD)
d.rectangle([196, 52, 270, 66], fill=DESK_TOP)
d.rectangle([196, 52, 270, 66], outline=DESK_SIDE, width=1)
d.rectangle([196, 64, 270, 70], fill=DESK_SIDE)

# 모니터
d.rectangle([216, 35, 236, 50], fill=MONITOR)
d.rectangle([218, 37, 234, 48], fill=SCREEN)
d.polygon([218,37, 224,37, 218,43], fill=SCREEN2)
d.rectangle([224, 50, 228, 53], fill=MONITOR)
d.rectangle([222, 53, 230, 54], fill=MONITOR)

# 키보드
d.rectangle([204, 55, 218, 61], fill=(90, 92, 102, 255))
for kx in range(206, 218, 3):
    d.line([kx, 56, kx, 60], fill=(70, 72, 82, 255), width=1)

# 파일 박스
d.rectangle([244, 53, 262, 65], fill=(185, 160, 120, 255))
d.rectangle([244, 53, 262, 65], outline=DESK_SIDE, width=1)
for fy in range(55, 64, 3):
    d.line([246, fy, 260, fy], fill=DESK_SIDE, width=1)

# 의자
d.rectangle([220, 72, 236, 88], fill=CHAIR_B)
d.rectangle([220, 72, 236, 88], outline=CHAIR_D, width=1)
d.rectangle([222, 70, 234, 73], fill=CHAIR_B)

# ════════════════════════════════
# 8. 회의 테이블 (하단 중앙, 바닥 위)
# ════════════════════════════════
# 테이블 그림자
d.rectangle([94, 142, 228, 148], fill=DESK_SHAD)
# 테이블
d.rectangle([90, 118, 230, 142], fill=DESK_TOP)
d.rectangle([90, 118, 230, 142], outline=DESK_SIDE, width=1)
d.rectangle([90, 138, 230, 144], fill=DESK_SIDE)

# 러그 (테이블 아래)
d.rectangle([82, 116, 238, 158], fill=RUG)
d.rectangle([84, 118, 236, 156], fill=RUG_L)
d.rectangle([90, 118, 230, 142], fill=DESK_TOP)  # 테이블 위에 다시
d.rectangle([90, 118, 230, 142], outline=DESK_SIDE, width=1)
d.rectangle([90, 138, 230, 144], fill=DESK_SIDE)

# 테이블 위 소품
d.rectangle([100, 124, 118, 136], fill=PAPER)
for ly in range(126, 135, 3):
    d.line([102, ly, 116, ly], fill=PAPER_L, width=1)
d.ellipse([130, 125, 142, 137], fill=(175, 95, 55, 255))  # 커피컵
d.ellipse([132, 127, 140, 135], fill=(60, 35, 18, 255))
d.rectangle([155, 122, 195, 138], fill=PAPER)

# 회의 의자들
for cx in [100, 126, 152, 178, 204]:
    # 위쪽 (등받이 위)
    d.rectangle([cx-7, 105, cx+7, 116], fill=CHAIR_B)
    d.rectangle([cx-7, 105, cx+7, 116], outline=CHAIR_D, width=1)
    d.rectangle([cx-5, 103, cx+5, 107], fill=CHAIR_B)
    # 아래쪽
    d.rectangle([cx-7, 145, cx+7, 157], fill=CHAIR_B)
    d.rectangle([cx-7, 145, cx+7, 157], outline=CHAIR_D, width=1)
    d.rectangle([cx-5, 155, cx+5, 159], fill=CHAIR_B)

# ════════════════════════════════
# 9. 화분 (우측 벽 모서리)
# ════════════════════════════════
for px, py in [(292, 55), (292, 88)]:
    d.ellipse([px-8, py-2, px+8, py+8], fill=POT)
    d.ellipse([px-6, py, px+6, py+6], fill=(135, 75, 42, 255))
    d.ellipse([px-6, py-14, px, py-2],  fill=PLANT_G)
    d.ellipse([px-2, py-16, px+6, py-4], fill=PLANT_G)
    d.ellipse([px-4, py-12, px+4, py-2], fill=PLANT_D)

# ════════════════════════════════
# 10. KODA 액자 (우측 벽)
# ════════════════════════════════
d.rectangle([270, 12, 308, 48], fill=(140, 118, 90, 255))  # 액자 테두리
d.rectangle([272, 14, 306, 46], fill=(252, 248, 238, 255)) # 내부 흰색
d.line([274, 20, 304, 20], fill=(180, 172, 155, 255), width=1)
d.line([274, 25, 304, 25], fill=(180, 172, 155, 255), width=1)
d.line([274, 30, 290, 30], fill=(180, 172, 155, 255), width=1)
# KODA 텍스트 느낌 (굵은 선들)
for i, (x1,x2) in enumerate([(274,284),(286,296),(298,304)]):
    d.rectangle([x1, 35, x2, 43], fill=(60, 80, 140, 255))

img.save(os.path.join(OUT, "office_bg.png"))
print("저장됨: office_bg.png")
