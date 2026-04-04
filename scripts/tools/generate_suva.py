"""
Aid World — 수바 거리 배경 v2
실제 수바(Fiji) 참고: 식민지 건물+현대 빌딩 혼재, 성당, 야자수, 항구+산 원경
320x180 픽셀아트
"""
from PIL import Image, ImageDraw
import os

OUT = "/Users/nddn/Documents/Claude/Projects/IDC game/assets/sprites/tilesets"
os.makedirs(OUT, exist_ok=True)

W, H = 320, 180
img = Image.new("RGBA", (W, H))
d = ImageDraw.Draw(img)

# ── 팔레트 ──
# 하늘 (흐린 열대 — 회청색)
SKY1 = (148, 168, 195)
SKY2 = (175, 192, 210)
CLOUD_D = (195, 202, 215)
CLOUD_L = (218, 224, 232)

# 항구/바다
SEA   = (88, 128, 165)
SEA_L = (105, 148, 182)

# 산 실루엣
MTN1  = (95, 112, 102)
MTN2  = (115, 132, 118)
MTN3  = (78,  95,  85)

# 도로/인도
ROAD      = (105, 98, 88)
ROAD_L    = (118, 110, 100)
ROAD_LINE = (215, 200, 75)   # 노란 중앙선
SIDEWALK  = (165, 158, 145)
SIDE_EDGE = (148, 140, 128)
CURB      = (190, 182, 168)

# 잔디
GRASS   = (72, 145, 62)
GRASS_D = (55, 118, 48)

# 건물 공통
WIN_GLASS = (148, 195, 222)
WIN_REFL  = (192, 222, 238)
WIN_FRAME = (88, 82, 72)
WIN_DARK  = (55, 68, 88)     # 어두운 창문

# ── 건물별 색상 ──
# 현대 유리빌딩 (좌)
MOD_WALL  = (195, 198, 202)
MOD_PANEL = (175, 178, 185)
MOD_TRIM  = (88,  92, 102)

# 성당 (중앙 원경)
CAT_STONE = (155, 148, 135)
CAT_DARK  = (118, 112, 102)
CAT_ARCH  = (88,  82,  72)

# Jack's 느낌 밝은 상점 (중앙)
JACKS_BG   = (155, 195, 45)   # 라임 그린
JACKS_TRIM = (55,  62,  55)
JACKS_WALL = (228, 225, 218)
JACKS_ROOF = (62,  62,  58)

# 식민지 상가 (우)
COL_WALL  = (228, 215, 195)
COL_TRIM  = (88,  72,  48)
COL_ROOF  = (142, 108, 72)   # 골함석(corrugated iron) 느낌
COL_VRAN  = (62,  52,  42)   # 베란다 기둥

# KODA 사무소 (좌단, 플레이어 출발점)
KODA_W    = (208, 220, 198)
KODA_T    = (72,  118, 68)
KODA_ROOF = (55,  95,  52)

# 파란 호텔 타워 (원경 우)
HOTEL_W   = (115, 148, 192)
HOTEL_D   = (88,  115, 158)
HOTEL_TOP = (72,  98,  138)

# 문
DOOR_W = (185, 158, 112)
DOOR_D = (142, 118, 80)

# 야자수
PAL_TRK = (138, 105, 62)
PAL_TRD = (108, 82,  45)
PAL_GR  = (52,  142, 55)
PAL_GD  = (35,  112, 40)
PAL_GY  = (80,  158, 72)    # 밝은 잎

# 기타
FENCE   = (232, 228, 220)
SIGN_GR = (45,  118, 62)    # 도로 표지판 배경
FLAG_B  = (28,  68,  148)   # 피지 국기색

# ════════════════════════════════
# 0. 하늘 그라디언트 (흐린 열대)
# ════════════════════════════════
for y in range(0, 60):
    t = y / 60
    r = int(SKY1[0] + (SKY2[0]-SKY1[0]) * t)
    g = int(SKY1[1] + (SKY2[1]-SKY1[1]) * t)
    b = int(SKY1[2] + (SKY2[2]-SKY1[2]) * t)
    d.line([0, y, W-1, y], fill=(r,g,b,255))

# 구름 (두껍고 낮은 열대구름)
clouds = [
    (0,  6, 55, 16), (48, 3, 38, 14), (82,  8, 42, 12),
    (135, 4, 50, 15),(178, 2, 45, 13),(225, 6, 48, 14),
    (268, 5, 42, 12),(295, 8, 22, 10),
]
for cx, cy, cw, ch in clouds:
    d.ellipse([cx, cy, cx+cw, cy+ch], fill=(*CLOUD_D, 255))
    d.ellipse([cx+4, cy-3, cx+cw-3, cy+ch-2], fill=(*CLOUD_L, 255))
    d.ellipse([cx+cw//2-5, cy-2, cx+cw//2+8, cy+ch-3], fill=(*CLOUD_L, 255))

# ════════════════════════════════
# 1. 항구/바다 (원경 — y=40~55)
# ════════════════════════════════
for y in range(40, 56):
    t = (y-40) / 15
    r = int(SEA[0] + (SEA_L[0]-SEA[0]) * t)
    g = int(SEA[1] + (SEA_L[1]-SEA[1]) * t)
    b = int(SEA[2] + (SEA_L[2]-SEA[2]) * t)
    d.line([0, y, W-1, y], fill=(r,g,b,255))

# 파도 하이라이트
for wx in range(10, W-10, 22):
    d.line([wx, 48, wx+10, 48], fill=(*SEA_L, 180), width=1)

# ════════════════════════════════
# 2. 산 실루엣 (원경)
# ════════════════════════════════
# 뒷 산 (연한)
d.polygon([0,45, 0,55, 35,38, 70,50, 100,35, 140,48,
           180,32, 220,46, 260,36, 300,48, W,42, W,55], fill=(*MTN2, 255))
# 앞 산 (진한)
d.polygon([0,52, 0,58, 28,44, 55,54, 85,42, 115,55,
           145,40, 175,52, 210,38, 245,52, 280,44, W,50, W,58], fill=(*MTN1, 255))
# 산 앞 나무 실루엣
for tx in range(0, W, 14):
    h2 = 5 + (tx % 7)
    d.rectangle([tx, 54, tx+2, 54+h2], fill=(*MTN3, 255))
    d.ellipse([tx-3, 50, tx+6, 57], fill=(*MTN3, 255))

# ════════════════════════════════
# 3. 원경 건물 실루엣 (y=30~60)
# ════════════════════════════════
# 파란 원형 호텔 타워 (Tanoa Plaza 느낌, 우측 원경)
d.rectangle([248, 18, 272, 58], fill=(*HOTEL_W, 255))
d.rectangle([250, 18, 270, 22], fill=(*HOTEL_TOP, 255))
# 타워 창문
for wy in range(24, 56, 5):
    for wx in [252, 258, 264]:
        d.rectangle([wx, wy, wx+4, wy+3], fill=(*WIN_GLASS, 220))
# 타워 로고
d.ellipse([255, 19, 265, 23], fill=(*HOTEL_TOP, 255))

# 흰 행정건물 (원경 중앙)
d.rectangle([145, 28, 185, 60], fill=(225, 218, 205, 255))
for wy in range(32, 58, 6):
    for wx in [148, 156, 164, 172]:
        d.rectangle([wx, wy, wx+6, wy+4], fill=(*WIN_DARK, 200))

# ════════════════════════════════
# 4. 성당 (중앙 원경 — 수바 성당 느낌)
# ════════════════════════════════
# 본당
d.rectangle([128, 38, 172, 72], fill=(*CAT_STONE, 255))
# 정면 삼각형 지붕
d.polygon([126, 38, 150, 22, 174, 38], fill=(*CAT_DARK, 255))
# 첨탑 (좌)
d.rectangle([130, 15, 140, 40], fill=(*CAT_STONE, 255))
d.polygon([130,15, 135,6, 140,15], fill=(*CAT_DARK, 255))
d.rectangle([134, 4, 136, 8], fill=(*CAT_ARCH, 255))   # 십자가
d.rectangle([132, 5, 138, 6], fill=(*CAT_ARCH, 255))
# 첨탑 (우)
d.rectangle([160, 18, 170, 40], fill=(*CAT_STONE, 255))
d.polygon([160,18, 165,10, 170,18], fill=(*CAT_DARK, 255))
d.rectangle([164, 8, 166, 12], fill=(*CAT_ARCH, 255))
d.rectangle([162, 9, 168, 10], fill=(*CAT_ARCH, 255))
# 성당 창문 (아치형)
for wx in [134, 147, 158]:
    d.rectangle([wx, 42, wx+8, 54], fill=(*WIN_GLASS, 230))
    d.ellipse([wx, 42, wx+8, 48], fill=(*WIN_GLASS, 230))
    d.line([wx+4, 42, wx+4, 54], fill=(*CAT_ARCH, 200), width=1)
# 성당 문
d.rectangle([143, 56, 157, 72], fill=(*DOOR_D, 255))
d.ellipse([143, 56, 157, 64], fill=(*DOOR_W, 255))

# ════════════════════════════════
# 5+6. KODA 사무소 — Ratu Sukuna House 스타일
#       9층 1970s 브루탈리스트 콘크리트 타워
#       x=0~58, y=2~72
# ════════════════════════════════
CONC      = (208, 200, 185, 255)   # 메인 콘크리트 (따뜻한 베이지)
CONC_BAND = (178, 170, 155, 255)   # 층간 슬라브 (어둡게)
CONC_SIDE = (155, 148, 135, 255)   # 측면 그림자
WIN_W     = (142, 188, 218, 255)   # 창문 유리
WIN_F     = (108, 100, 88,  255)   # 창문 프레임
WIN_R     = (185, 215, 232, 255)   # 창문 반사
LOBBY_GL  = (125, 178, 210, 255)   # 로비 유리

TOWER_X1, TOWER_X2 = 0, 58

# 타워 본체
d.rectangle([TOWER_X1, 2, TOWER_X2, 72], fill=CONC)

# 9개 층 — 위에서 아래로 (층당 약 7.5px)
# y=2~72 = 70px / 9층 ≈ 7.8px per floor
# 1층(로비)은 높게, 2~9층은 균등하게
LOBBY_H = 14   # 1층 높이
FLOOR_H = 7    # 2~9층 높이
# 층 슬라브선 (수평 콘크리트 띠)
floor_tops = [2]  # 각 층 상단 y
y_cur = 2 + LOBBY_H
for _ in range(8):
    floor_tops.append(y_cur)
    y_cur += FLOOR_H

# 슬라브 띠 그리기 (층 구분선)
for fy in floor_tops[1:]:
    d.rectangle([TOWER_X1, fy, TOWER_X2, fy+2], fill=CONC_BAND)

# 측면 그림자 (우측 엣지)
d.rectangle([TOWER_X2-3, 2, TOWER_X2, 72], fill=CONC_SIDE)

# 창문 그리드 (2~9층)
WIN_COLS = [3, 11, 20, 29, 38, 47]   # 창문 x 시작 (6개 열)
for fi, fy in enumerate(floor_tops[1:]):  # 2층(index 1)부터
    for wx in WIN_COLS:
        wy = fy + 3
        d.rectangle([wx, wy, wx+6, wy+3], fill=WIN_F)
        d.rectangle([wx+1, wy+1, wx+5, wy+2], fill=WIN_W)
        d.rectangle([wx+1, wy+1, wx+3, wy+1], fill=(WIN_R[0],WIN_R[1],WIN_R[2],200))  # 반사

# 1층 로비 (유리 커튼월)
d.rectangle([TOWER_X1, 58, TOWER_X2, 72], fill=(LOBBY_GL[0],LOBBY_GL[1],LOBBY_GL[2],180))
# 로비 격자
for lx in range(TOWER_X1+6, TOWER_X2, 8):
    d.line([lx, 58, lx, 72], fill=WIN_F, width=1)
d.line([TOWER_X1, 64, TOWER_X2, 64], fill=WIN_F, width=1)
# 중앙 입구 (어둡게)
d.rectangle([22, 62, 36, 72], fill=(45, 55, 68, 255))
d.rectangle([23, 63, 35, 72], fill=(38, 48, 60, 255))
# 입구 양쪽 반사
d.rectangle([38, 62, 44, 72], fill=(WIN_R[0],WIN_R[1],WIN_R[2],200))
d.rectangle([14, 62, 20, 72], fill=(WIN_R[0],WIN_R[1],WIN_R[2],200))

# 옥상 처리 (평지붕 + 난간)
d.rectangle([TOWER_X1, 2, TOWER_X2, 4], fill=CONC_BAND)
d.rectangle([TOWER_X1, 2, TOWER_X1+2, 8], fill=CONC_BAND)   # 좌 코너
d.rectangle([TOWER_X2-2, 2, TOWER_X2, 8], fill=CONC_BAND)   # 우 코너

# 옥상 위 안테나/장비
d.rectangle([26, 0, 28, 3], fill=CONC_SIDE)
d.rectangle([38, 1, 42, 3], fill=CONC_BAND)

# 지상 입구 캐노피 (처마)
d.rectangle([18, 56, 40, 59], fill=CONC_BAND)
d.rectangle([20, 59, 38, 61], fill=CONC_SIDE)

# KODA 간판 (1층 상단 띠)
d.rectangle([TOWER_X1, 54, TOWER_X2, 58], fill=(*KODA_T, 255))
# 간판 텍스트 (흰 블록들로 표현)
for sx in [6, 14, 22, 30, 38]:
    d.rectangle([sx, 55, sx+5, 57], fill=(240, 238, 228, 255))

# ════════════════════════════════
# 7. Jack's of Fiji 느낌 밝은 상점 (중앙)
# ════════════════════════════════
# 건물 배경 (베이지)
d.rectangle([58, 45, 125, 72], fill=(*JACKS_WALL, 255))
# 라임 그린 대형 간판
d.rectangle([58, 45, 125, 62], fill=(*JACKS_BG, 255))
d.rectangle([58, 45, 125, 62], outline=(*JACKS_TRIM, 255), width=1)
# 간판 안 가로 스트라이프
for sy in range(47, 61, 3):
    d.line([60, sy, 123, sy], fill=(140, 178, 40, 255), width=1)
# 지붕 처마
d.rectangle([56, 61, 127, 65], fill=(*JACKS_ROOF, 255))
d.rectangle([58, 63, 125, 67], fill=(*JACKS_WALL, 255))
# 유리 쇼윈도
d.rectangle([60, 65, 88, 72], fill=(*WIN_GLASS, 230))
d.rectangle([60, 65, 62, 72], fill=(*WIN_FRAME, 255), width=1)
d.rectangle([95, 65, 123, 72], fill=(*WIN_GLASS, 230))
# 입구
d.rectangle([82, 64, 92, 72], fill=(*DOOR_W, 255))

# ════════════════════════════════
# 8. 식민지 상가 — 베란다 있는 2층 (우측)
# ════════════════════════════════
# 2층
d.rectangle([185, 40, 248, 72], fill=(*COL_WALL, 255))
# 골함석 지붕
for i in range(5):
    shade = COL_ROOF if i%2==0 else (COL_ROOF[0]-18, COL_ROOF[1]-14, COL_ROOF[2]-10)
    d.rectangle([185, 38+i, 248, 40+i], fill=(*shade, 255))
# 2층 창문 (작은 직사각형 여럿)
for wx in [190, 202, 214, 226, 235]:
    d.rectangle([wx, 43, wx+9, 52], fill=(*WIN_GLASS, 220))
    d.rectangle([wx, 43, wx+4, 46], fill=(*WIN_REFL, 180))
# 베란다 (1층 처마)
d.rectangle([185, 60, 248, 64], fill=(*COL_TRIM, 255))
# 베란다 기둥
for px in range(188, 248, 12):
    d.rectangle([px, 60, px+3, 72], fill=(*COL_VRAN, 255))
# 1층 문/창
d.rectangle([188, 64, 202, 72], fill=(*WIN_GLASS, 200))
d.rectangle([210, 64, 224, 72], fill=(*DOOR_W, 255))
d.rectangle([232, 64, 246, 72], fill=(*WIN_GLASS, 200))
# 트림
d.line([185, 40, 248, 40], fill=(*COL_TRIM, 255), width=2)
d.line([185, 60, 248, 60], fill=(*COL_TRIM, 255), width=1)

# ════════════════════════════════
# 9. 국제기구 사무소 — Kadavu House 스타일
#    6층 콘크리트 빌딩, UN 간판, x=268~320, y=8~72
# ════════════════════════════════
UN_CONC   = (215, 210, 198, 255)   # 크림색 콘크리트
UN_BAND   = (188, 182, 170, 255)   # 층간 슬래브
UN_SIDE   = (175, 168, 155, 255)   # 측면 기둥 그림자
UN_WIN    = (118, 155, 185, 255)   # 창문 유리
UN_WIN_F  = (95, 90, 82, 255)     # 창문 프레임
UN_BLUE   = (42, 88, 155, 255)    # UN 파랑
UN_CANOPY = (38, 42, 52, 255)     # 입구 캐노피

# 건물 본체
d.rectangle([268, 8, 320, 72], fill=UN_CONC)

# 좌측 수직 기둥 (세로 돌출부)
d.rectangle([268, 8, 273, 72], fill=UN_SIDE)
# 우측 기둥 (화면 가장자리)
d.rectangle([316, 8, 320, 72], fill=UN_SIDE)

# 6개 층 슬래브선 (수평 콘크리트 띠)
for fy in [8, 18, 28, 38, 48, 58]:
    d.rectangle([268, fy, 320, fy+2], fill=UN_BAND)

# 창문 그리드 (5개 층, 각 층 4~5개 창)
for fy in [12, 22, 32, 42, 52]:
    for wx in [275, 283, 291, 299, 308]:
        d.rectangle([wx, fy, wx+6, fy+4], fill=UN_WIN_F)
        d.rectangle([wx+1, fy+1, wx+5, fy+3], fill=UN_WIN)

# UN 간판 (좌측 상단 — 파란 직사각형 + 흰 텍스트)
d.rectangle([269, 12, 281, 18], fill=UN_BLUE)
for sx in [271, 274, 277]:
    d.rectangle([sx, 14, sx+2, 16], fill=(230, 235, 245, 255))

# 1층 입구 캐노피 (어두운 처마)
d.rectangle([278, 64, 310, 68], fill=UN_CANOPY)
d.rectangle([280, 68, 308, 72], fill=UN_CANOPY)
# 입구 유리문 (center=290)
d.rectangle([283, 66, 297, 72], fill=(85, 128, 165, 255))
d.line([(290, 66), (290, 72)], fill=UN_WIN_F, width=1)  # 문 중앙선
# 입구 위 UN 간판
d.rectangle([282, 63, 298, 66], fill=UN_BLUE)
for sx in [284, 288, 292]:
    d.rectangle([sx, 64, sx+2, 65], fill=(230, 235, 245, 255))

# 옥상 처리 (평지붕 + 난간)
d.rectangle([268, 8, 320, 10], fill=UN_BAND)

# 건물 앞 야자수 (작은 팬 팜)
d.rectangle([271, 48, 273, 63], fill=(*PAL_TRK, 255))
for lx, ly in [(-4,-6),(-2,-8),(1,-9),(4,-7),(6,-4)]:
    d.ellipse([272+lx-2, 48+ly-2, 272+lx+3, 48+ly+3], fill=(*PAL_GR, 255))

# ════════════════════════════════
# 10. 인도 (y=72~82)
# ════════════════════════════════
d.rectangle([0, 72, W-1, 82], fill=(*SIDEWALK, 255))
d.line([0, 72, W-1, 72], fill=(*SIDE_EDGE, 255), width=1)
d.line([0, 82, W-1, 82], fill=(*SIDE_EDGE, 255), width=1)
# 인도 타일
for x in range(0, W, 16):
    d.line([x, 72, x, 82], fill=(*SIDE_EDGE, 255), width=1)
for y in range(76, 82, 4):
    d.line([0, y, W-1, y], fill=(*SIDE_EDGE, 200), width=1)
# 연석(curb)
d.rectangle([0, 80, W-1, 83], fill=(*CURB, 255))

# ════════════════════════════════
# 11. 도로 (y=83~148)
# ════════════════════════════════
for y in range(83, 148):
    shade = ROAD if (y//6)%2==0 else ROAD_L
    d.line([0, y, W-1, y], fill=(*shade, 255))

# 중앙선 (노란 점선)
for x in range(0, W, 20):
    d.rectangle([x, 113, x+10, 116], fill=(*ROAD_LINE, 255))

# 흰 차선
d.line([0, 83, W-1, 83], fill=(185, 178, 165, 255), width=1)
d.line([0, 147, W-1, 147], fill=(185, 178, 165, 255), width=1)

# ════════════════════════════════
# 12. 잔디 화단 (인도 앞, y=148~158)
# ════════════════════════════════
d.rectangle([0, 148, W-1, 158], fill=(*GRASS, 255))
for x in range(0, W, 4):
    d.line([x, 149, x, 153], fill=(*GRASS_D, 255), width=1)

# 흰 목책 (white picket fence)
d.rectangle([0, 148, W-1, 150], fill=(*FENCE, 255))
for fx in range(0, W, 6):
    d.rectangle([fx, 148, fx+2, 158], fill=(*FENCE, 255))
    d.polygon([fx, 148, fx+1, 145, fx+2, 148], fill=(*FENCE, 255))

# ════════════════════════════════
# 13. 야자수들
# ════════════════════════════════
def palm(px, ground_y, height=30):
    # 줄기 (약간 휨)
    for i in range(height):
        lean = i // 8
        cx2 = px + lean
        w2 = max(1, 3 - i * 2 // height)
        d.rectangle([cx2-w2, ground_y-i, cx2+w2, ground_y-i+1],
                    fill=(*PAL_TRK, 255) if i%3!=2 else (*PAL_TRD, 255))
    top = ground_y - height
    # 잎 (여러 방향)
    leaf_data = [
        (-16, -8, 14, 5), (-10, -12, 8, 4), (2, -14, 16, 5),
        (8, -8, 16, 4),   (-4, -6, 12, 6),  (-14, -4, 10, 5),
    ]
    for lx, ly, lw, lh in leaf_data:
        bx = px + lean + lx
        by = top + ly
        d.ellipse([bx, by, bx+lw, by+lh], fill=(*PAL_GR, 255))
    # 잎 어두운 부분 (겹침)
    for lx, ly, lw, lh in leaf_data[1::2]:
        bx = px + lean + lx + 2
        by = top + ly + 1
        d.ellipse([bx, by, bx+lw-2, by+lh-1], fill=(*PAL_GD, 255))
    # 코코넛
    for ox, oy in [(-2,-4),(3,-3),(-5,-2)]:
        d.ellipse([px+lean+ox, top+oy, px+lean+ox+4, top+oy+4],
                  fill=(88, 68, 38, 255))

palm(30,  80, 28)
palm(82,  80, 32)
palm(148, 80, 26)
palm(220, 80, 30)
palm(298, 78, 24)

# ════════════════════════════════
# 14. 가로등
# ════════════════════════════════
def lamppost(lx, ly=80):
    d.rectangle([lx-1, ly, lx+1, ly+28], fill=(155, 150, 140, 255))
    # 팔 (lamp arm)
    d.line([lx, ly, lx+8, ly-4], fill=(155, 150, 140, 255), width=2)
    d.ellipse([lx+5, ly-8, lx+13, ly-1], fill=(242, 228, 155, 255))
    d.ellipse([lx+7, ly-7, lx+11, ly-2], fill=(255, 245, 180, 255))

lamppost(55,  75)
lamppost(195, 75)
lamppost(300, 75)

# ════════════════════════════════
# 15. 도로 표지판 (Goodenough St 느낌)
# ════════════════════════════════
# 표지판 기둥
d.rectangle([108, 72, 110, 88], fill=(175, 168, 155, 255))
# 표지판 판
d.rectangle([100, 73, 128, 80], fill=(*SIGN_GR, 255))
d.rectangle([100, 73, 128, 80], outline=(32, 95, 48, 255), width=1)
# 텍스트 표현 (흰 점선)
for tx in range(103, 125, 4):
    d.rectangle([tx, 75, tx+2, 78], fill=(240, 238, 232, 255))

# ════════════════════════════════
# 16. 피지 국기 (성당 옆 깃발)
# ════════════════════════════════
d.rectangle([175, 30, 177, 50], fill=(138, 125, 105, 255))  # 깃대
d.rectangle([177, 30, 192, 38], fill=(*FLAG_B, 255))
d.rectangle([177, 30, 185, 34], fill=(205, 40, 40, 255))    # 유니언잭 느낌
d.rectangle([181, 30, 183, 38], fill=(232, 228, 218, 255))
d.rectangle([177, 33, 192, 35], fill=(232, 228, 218, 255))

# ════════════════════════════════
# 17. 주차된 차 힌트 (도로 위 장식)
# ════════════════════════════════
# 차 1 (빨간, 좌)
d.rectangle([15, 92, 45, 104], fill=(188, 55, 48, 255))
d.rectangle([20, 89, 40, 94], fill=(168, 48, 42, 255))
d.rectangle([16, 100, 22, 106], fill=(42, 42, 42, 255))   # 바퀴
d.rectangle([38, 100, 44, 106], fill=(42, 42, 42, 255))
d.rectangle([22, 90, 38, 94], fill=(*WIN_GLASS, 200))

# 차 2 (검정, 중)
d.rectangle([165, 94, 200, 106], fill=(45, 45, 52, 255))
d.rectangle([170, 91, 195, 96], fill=(38, 38, 45, 255))
d.rectangle([166, 102, 173, 108], fill=(32, 32, 32, 255))
d.rectangle([192, 102, 199, 108], fill=(32, 32, 32, 255))
d.rectangle([172, 91, 193, 96], fill=(*WIN_GLASS, 180))

# ════════════════════════════════
# 18. 항구 / 선착장 (하단, y=158~180)
#     수바 항 — 콘크리트 부두 + 목재 선착장 + 인터아일랜드 페리
# ════════════════════════════════
HARBOR_SEA    = (48,  82, 115)   # 수바 만 (어두운 청록)
HARBOR_DEEP   = (35,  62,  92)   # 깊은 바다
HARBOR_REFL   = (68, 108, 148)   # 수면 반사
QUAY_CONC     = (152, 145, 132)  # 부두 콘크리트
QUAY_EDGE     = (122, 115, 105)  # 콘크리트 엣지
QUAY_SHADOW   = (102,  95,  85)  # 수중 부두벽
JETTY_WOOD    = (128,  96,  60)  # 목재 널빤지
JETTY_DARK    = (105,  78,  46)  # 어두운 판자
BOLLARD_BODY  = (66,  66,  74)   # 볼라드 기둥
BOLLARD_CAP   = (88,  88,  98)   # 볼라드 상단
ROPE_COL      = (168, 148, 108)  # 계류 로프
FERRY_HULL    = (230, 228, 215)  # 페리 선체 (크림)
FERRY_REDLINE = (192,  45,  36)  # 워터라인 (빨강)
FERRY_CABIN   = ( 50,  78, 122)  # 선실 (파랑)
FERRY_WIN_C   = (130, 172, 208)  # 선실 창문
FERRY_DECK    = (200, 195, 180)  # 갑판
FERRY_FUNNEL  = ( 38,  38,  46)  # 굴뚝
FERRY_SMOKE   = (165, 162, 158)  # 연기

# ── 바다 (전체 하단) ───────────────────────────────────────
for y in range(163, 180):
    t = (y - 163) / 17
    r = int(HARBOR_SEA[0] + (HARBOR_DEEP[0] - HARBOR_SEA[0]) * t)
    g = int(HARBOR_SEA[1] + (HARBOR_DEEP[1] - HARBOR_SEA[1]) * t)
    b = int(HARBOR_SEA[2] + (HARBOR_DEEP[2] - HARBOR_SEA[2]) * t)
    d.line([0, y, W-1, y], fill=(r, g, b, 255))

# 수면 반사 (선착장 좌/우)
for wy in [165, 168, 172, 176]:
    for wx in range(5, 130, 22):
        d.line([wx, wy, wx + 9, wy], fill=(*HARBOR_REFL, 180), width=1)
    for wx in range(312, 195, -22):
        d.line([wx - 8, wy, wx, wy], fill=(*HARBOR_REFL, 160), width=1)

# ── 부두 콘크리트 벽 (좌: x=0~133, 우: x=187~320) ─────────
# 좌측 부두
d.rectangle([0, 158, 133, 163], fill=(*QUAY_CONC, 255))
d.rectangle([0, 163, 133, 167], fill=(*QUAY_SHADOW, 255))
d.line([0, 163, 133, 163], fill=(*QUAY_EDGE, 255), width=1)
# 우측 부두
d.rectangle([187, 158, W, 163], fill=(*QUAY_CONC, 255))
d.rectangle([187, 163, W, 167], fill=(*QUAY_SHADOW, 255))
d.line([187, 163, W, 163], fill=(*QUAY_EDGE, 255), width=1)

# ── 목재 선착장 (x=133~187, y=158~178) ──────────────────────
# 측면 마구리
d.rectangle([133, 158, 135, 178], fill=(*JETTY_DARK, 255))
d.rectangle([185, 158, 187, 178], fill=(*JETTY_DARK, 255))
# 하단 수중 지지대
d.rectangle([133, 178, 187, 180], fill=(*JETTY_DARK, 255))
# 판자 (가로 결)
for py in range(158, 178):
    plank = JETTY_WOOD if (py % 4) < 2 else JETTY_DARK
    d.rectangle([135, py, 185, py + 1], fill=(*plank, 255))
# 판자 틈 선
for py in range(162, 178, 4):
    d.line([135, py, 185, py], fill=(*JETTY_DARK, 200), width=1)

# ── 볼라드 (철제 계류 말뚝 × 3) ──────────────────────────────
for bx in [141, 160, 179]:
    d.rectangle([bx - 1, 162, bx + 1, 172], fill=(*BOLLARD_BODY, 255))
    d.ellipse([bx - 3, 160, bx + 3, 165], fill=(*BOLLARD_CAP, 255))

# ── 페리 — 인터아일랜드 여객선 ──────────────────────────────
# 수바 항에서 외곽 섬으로 다니는 크루즈 페리 (크림 선체, 파란 선실)
FX1, FX2   = 192, 308          # 선체 좌/우
FY_WL      = 174               # 흘수선 y
FY_DECK    = 158               # 갑판 y

# 선체 본체 (크림)
d.polygon([
    FX1,     FY_WL,            # 선미 하단
    FX1,     FY_DECK + 5,      # 선미 측면
    FX1 + 4, FY_DECK + 1,      # 선미 상단
    FX2 - 8, FY_DECK + 1,      # 선수 근처
    FX2,     FY_DECK + 7,      # 선수 뾰족
    FX2,     FY_WL,            # 선수 하단
], fill=(*FERRY_HULL, 255))

# 워터라인 (빨간 띠)
d.rectangle([FX1, FY_WL - 2, FX2, FY_WL], fill=(*FERRY_REDLINE, 255))

# 갑판 선 (어두운 그림자)
d.line([FX1 + 4, FY_DECK + 2, FX2 - 6, FY_DECK + 2],
       fill=(*FERRY_DECK, 255), width=2)

# 선실 블록 (갑판 위)
CAB_Y1 = FY_DECK - 12
CAB_Y2 = FY_DECK + 1
d.rectangle([FX1 + 6, CAB_Y1, FX2 - 12, CAB_Y2], fill=(*FERRY_CABIN, 255))

# 선실 창문 행
for cwx in range(FX1 + 10, FX2 - 14, 10):
    d.rectangle([cwx, CAB_Y1 + 3, cwx + 6, CAB_Y1 + 8],
                fill=(*FERRY_WIN_C, 255))

# 조타실 (선수 쪽 상부)
d.rectangle([FX2 - 24, CAB_Y1 - 6, FX2 - 10, CAB_Y1],
            fill=(38, 62, 102, 255))
d.rectangle([FX2 - 22, CAB_Y1 - 5, FX2 - 12, CAB_Y1 - 1],
            fill=(*FERRY_WIN_C, 200))

# 굴뚝 (2개) + 연기
for fx in [FX1 + 22, FX1 + 34]:
    d.rectangle([fx, CAB_Y1 - 10, fx + 5, CAB_Y1], fill=(*FERRY_FUNNEL, 255))
    d.ellipse([fx - 1, CAB_Y1 - 13, fx + 6, CAB_Y1 - 9],
              fill=(*FERRY_SMOKE, 160))
    d.ellipse([fx,     CAB_Y1 - 16, fx + 5, CAB_Y1 - 12],
              fill=(*FERRY_SMOKE, 100))

# 갑판 난간 (흰 점선)
for nx in range(FX1 + 5, FX2 - 6, 4):
    d.point([nx, FY_DECK + 1], fill=(222, 220, 210, 255))

# ── 모터보트 (나이탬바와 동일한 배 — 선착장 우측) ───────────
# 나이탬바 island와 같은 파란 유리섬유 소형 모터보트
HULL_DARK  = ( 28,  82, 148, 255)   # 파란 유리섬유 선체
HULL_LIGHT = ( 52, 112, 175, 255)   # 선체 상단 하이라이트
INTERIOR   = (218, 212, 200, 255)   # 선내 (베이지 흰)
MOTOR_BODY = ( 48,  50,  55, 255)   # 선외기 본체
MOTOR_ARM  = ( 38,  40,  44, 255)   # 선외기 팔
WINDSHIELD = (175, 212, 238, 255)   # 앞유리

BX1, BX2 = 191, 229   # 보트 좌우 (38px — 나이탬바와 동일 폭)
BY1, BY2 = 163, 175   # 보트 상하 (수바 수면 y=163 기준)

# 선체 본체 (뾰족한 배 형태)
hull_pts = [
    (BX1 + 4, BY2), (BX1,     BY1 + 6),
    (BX1,     BY1 + 3),
    (BX1 + 6, BY1),
    (BX2 - 2, BY1),
    (BX2,     BY1 + 4),
    (BX2,     BY2 - 1),
]
d.polygon(hull_pts, fill=HULL_DARK)
# 선체 상단 하이라이트
d.line([(BX1 + 6, BY1), (BX2 - 2, BY1)], fill=HULL_LIGHT, width=2)
d.line([(BX1, BY1 + 3), (BX1 + 6, BY1)], fill=HULL_LIGHT, width=1)
# 선내
d.rectangle([BX1 + 5, BY1 + 2, BX2 - 4, BY1 + 7], fill=INTERIOR)
# 앞유리 (조종석 바람막이)
d.polygon([
    (BX1 + 8,  BY1 + 2), (BX1 + 12, BY1 - 2),
    (BX1 + 20, BY1 - 2), (BX1 + 22, BY1 + 2)
], fill=WINDSHIELD)
d.line([(BX1 + 8,  BY1 + 2), (BX1 + 12, BY1 - 2)], fill=(120, 160, 195, 255), width=1)
d.line([(BX1 + 12, BY1 - 2), (BX1 + 20, BY1 - 2)], fill=(120, 160, 195, 255), width=1)
# 선외기 (오른쪽 끝)
d.rectangle([BX2 - 1, BY1 + 2, BX2 + 4, BY1 + 9], fill=MOTOR_BODY)
d.rectangle([BX2 + 2, BY1 + 9, BX2 + 4, BY2 - 1], fill=MOTOR_ARM)
d.rectangle([BX2,     BY2 - 2, BX2 + 5, BY2],     fill=MOTOR_BODY)

# 계류 로프 (보트 앞 → 선착장 볼라드)
d.line([(BX1, BY1 + 5), (181, 169)], fill=(*ROPE_COL, 255), width=1)

# 보트 물 반사
for i in range(4):
    rc = (int(28 * 0.5), int(82 * 0.5), int(148 * 0.55), 180 - i * 40)
    d.line([(BX1 + 6 + i, BY2 + 1 + i), (BX2 - i, BY2 + 1 + i)], fill=rc)

img.save(os.path.join(OUT, "suva_street_bg.png"))
print("저장됨: suva_street_bg.png")
