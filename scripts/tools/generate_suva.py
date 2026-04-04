"""
Aid World — 수바 거리 배경 v3 (랜드마크 반영)
실제 수바 랜드마크: Albert Park, Parliament (시계탑), Grand Pacific Hotel, Damodar City
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
SKY1 = (148, 168, 195)
SKY2 = (175, 192, 210)
CLOUD_D = (195, 202, 215)
CLOUD_L = (218, 224, 232)

SEA   = (88, 128, 165)
SEA_L = (105, 148, 182)

MTN1  = (95, 112, 102)
MTN2  = (115, 132, 118)
MTN3  = (78,  95,  85)

ROAD      = (105, 98, 88)
ROAD_L    = (118, 110, 100)
ROAD_LINE = (215, 200, 75)
SIDEWALK  = (165, 158, 145)
SIDE_EDGE = (148, 140, 128)
CURB      = (190, 182, 168)

GRASS   = (72, 145, 62)
GRASS_D = (55, 118, 48)
GRASS_L = (95, 168, 80)

WIN_GLASS = (148, 195, 222)
WIN_REFL  = (192, 222, 238)
WIN_FRAME = (88, 82, 72)
WIN_DARK  = (55, 68, 88)

# KODA
KODA_T    = (72,  118, 68)
CONC      = (208, 200, 185, 255)
CONC_BAND = (178, 170, 155, 255)
CONC_SIDE = (155, 148, 135, 255)
LOBBY_GL  = (125, 178, 210, 255)

# Parliament
PARL_WALL  = (228, 218, 198)
PARL_TRIM  = (188, 178, 158)
PARL_DARK  = (148, 138, 118)
PARL_TOWER = (238, 228, 208)
PARL_DOME  = (55, 105, 145)  # 청록 유약 타일
PARL_DOME_L = (75, 135, 175)
CLOCK_FACE = (242, 240, 235)

# Grand Pacific Hotel
GPH_WALL = (245, 242, 238)
GPH_TRIM = (195, 188, 178)
GPH_COL  = (235, 232, 225)

# Damodar City
DAM_WALL  = (225, 225, 228)
DAM_RED   = (195, 45, 45)
DAM_SIGN  = (240, 210, 55)
DAM_GLASS = (115, 155, 185)

DOOR_W = (185, 158, 112)
DOOR_D = (142, 118, 80)

PAL_TRK = (138, 105, 62)
PAL_TRD = (108, 82,  45)
PAL_GR  = (52,  142, 55)
PAL_GD  = (35,  112, 40)

FENCE   = (232, 228, 220)
FLAG_B  = (28,  68,  148)

# ════════════════════════════════
# 0. 하늘 그라디언트
# ════════════════════════════════
for y in range(0, 60):
    t = y / 60
    r = int(SKY1[0] + (SKY2[0]-SKY1[0]) * t)
    g = int(SKY1[1] + (SKY2[1]-SKY1[1]) * t)
    b = int(SKY1[2] + (SKY2[2]-SKY1[2]) * t)
    d.line([0, y, W-1, y], fill=(r,g,b,255))

clouds = [
    (0,  6, 55, 16), (48, 3, 38, 14), (82,  8, 42, 12),
    (135, 4, 50, 15),(178, 2, 45, 13),(225, 6, 48, 14),
    (268, 5, 42, 12),(295, 8, 22, 10),
]
for cx, cy, cw, ch in clouds:
    d.ellipse([cx, cy, cx+cw, cy+ch], fill=(*CLOUD_D, 255))
    d.ellipse([cx+4, cy-3, cx+cw-3, cy+ch-2], fill=(*CLOUD_L, 255))

# ════════════════════════════════
# 1. 항구/바다 (원경)
# ════════════════════════════════
for y in range(40, 56):
    t = (y-40) / 15
    r = int(SEA[0] + (SEA_L[0]-SEA[0]) * t)
    g = int(SEA[1] + (SEA_L[1]-SEA[1]) * t)
    b = int(SEA[2] + (SEA_L[2]-SEA[2]) * t)
    d.line([0, y, W-1, y], fill=(r,g,b,255))
for wx in range(10, W-10, 22):
    d.line([wx, 48, wx+10, 48], fill=(*SEA_L, 180), width=1)

# ════════════════════════════════
# 2. 산 실루엣 (원경)
# ════════════════════════════════
d.polygon([0,45, 0,55, 35,38, 70,50, 100,35, 140,48,
           180,32, 220,46, 260,36, 300,48, W,42, W,55], fill=(*MTN2, 255))
d.polygon([0,52, 0,58, 28,44, 55,54, 85,42, 115,55,
           145,40, 175,52, 210,38, 245,52, 280,44, W,50, W,58], fill=(*MTN1, 255))
for tx in range(0, W, 14):
    h2 = 5 + (tx % 7)
    d.rectangle([tx, 54, tx+2, 54+h2], fill=(*MTN3, 255))
    d.ellipse([tx-3, 50, tx+6, 57], fill=(*MTN3, 255))

# ════════════════════════════════
# 3. Grand Pacific Hotel (원경 — Albert Park 뒤)
#    흰색 식민지풍 2층, 기둥, 발코니
#    x=60~130, y=30~58 (원경이므로 작게)
# ════════════════════════════════
d.rectangle([60, 35, 130, 58], fill=(*GPH_WALL, 255))
# 지붕
d.rectangle([58, 33, 132, 37], fill=(*GPH_TRIM, 255))
d.rectangle([60, 30, 130, 34], fill=(*GPH_TRIM, 255))
# 기둥 (8개)
for px in range(62, 130, 10):
    d.rectangle([px, 35, px+2, 58], fill=(*GPH_COL, 255))
# 2층 발코니 라인
d.rectangle([60, 45, 130, 47], fill=(*GPH_TRIM, 255))
# 창문 (2층)
for wx in range(64, 128, 10):
    d.rectangle([wx, 37, wx+6, 43], fill=(*WIN_GLASS, 200))
# 창문 (1층)
for wx in range(64, 128, 10):
    d.rectangle([wx, 49, wx+6, 55], fill=(*WIN_GLASS, 200))
# 중앙 입구 포르티코
d.rectangle([88, 30, 102, 36], fill=(*GPH_WALL, 255))
d.polygon([86, 30, 95, 24, 104, 30], fill=(*GPH_TRIM, 255))
# "GRAND PACIFIC HOTEL" 간판 (작은 텍스트 블록)
for sx in range(72, 120, 5):
    d.rectangle([sx, 31, sx+3, 33], fill=(*PARL_DARK, 255))

# ════════════════════════════════
# 4. KODA 사무소 — Ratu Sukuna House 스타일 (x=0~55)
# ════════════════════════════════
TOWER_X1, TOWER_X2 = 0, 55
d.rectangle([TOWER_X1, 2, TOWER_X2, 72], fill=CONC)

LOBBY_H = 14
FLOOR_H = 7
floor_tops = [2]
y_cur = 2 + LOBBY_H
for _ in range(8):
    floor_tops.append(y_cur)
    y_cur += FLOOR_H

for fy in floor_tops[1:]:
    d.rectangle([TOWER_X1, fy, TOWER_X2, fy+2], fill=CONC_BAND)

d.rectangle([TOWER_X2-3, 2, TOWER_X2, 72], fill=CONC_SIDE)

WIN_COLS = [3, 11, 20, 29, 38, 47]
for fi, fy in enumerate(floor_tops[1:]):
    for wx in WIN_COLS:
        wy = fy + 3
        d.rectangle([wx, wy, wx+6, wy+3], fill=(108,100,88,255))
        d.rectangle([wx+1, wy+1, wx+5, wy+2], fill=(142,188,218,255))

d.rectangle([TOWER_X1, 58, TOWER_X2, 72], fill=(LOBBY_GL[0],LOBBY_GL[1],LOBBY_GL[2],180))
for lx in range(TOWER_X1+6, TOWER_X2, 8):
    d.line([lx, 58, lx, 72], fill=(108,100,88,255), width=1)
d.line([TOWER_X1, 64, TOWER_X2, 64], fill=(108,100,88,255), width=1)
d.rectangle([22, 62, 36, 72], fill=(45, 55, 68, 255))

d.rectangle([TOWER_X1, 2, TOWER_X2, 4], fill=CONC_BAND)
d.rectangle([26, 0, 28, 3], fill=CONC_SIDE)

# KODA 간판
d.rectangle([TOWER_X1, 54, TOWER_X2, 58], fill=(*KODA_T, 255))
for sx in [6, 14, 22, 30, 38]:
    d.rectangle([sx, 55, sx+5, 57], fill=(240, 238, 228, 255))

# ════════════════════════════════
# 5. Albert Park (x=55~120)
#    녹지 운동장, 럭비 H 골대, 저 관중석
# ════════════════════════════════
# 하늘이 보이는 열린 공간 — 건물 없음 (원경 GPH가 뒤에 보임)
# 잔디밭 (y=58~72)
d.rectangle([55, 58, 120, 72], fill=(*GRASS, 255))
# 잔디 질감
for x in range(56, 120, 3):
    for y in range(59, 72, 3):
        shade = GRASS_D if (x+y) % 5 < 2 else GRASS_L
        d.rectangle([x, y, x+1, y+1], fill=(*shade, 255))

# 럭비 H 골대 (좌)
POST_COL = (235, 235, 232)
d.rectangle([66, 48, 68, 72], fill=(*POST_COL, 255))  # 좌 기둥
d.rectangle([78, 48, 80, 72], fill=(*POST_COL, 255))  # 우 기둥
d.rectangle([66, 48, 80, 50], fill=(*POST_COL, 255))  # 가로대

# 럭비 H 골대 (우)
d.rectangle([102, 50, 104, 72], fill=(*POST_COL, 255))
d.rectangle([112, 50, 114, 72], fill=(*POST_COL, 255))
d.rectangle([102, 50, 114, 52], fill=(*POST_COL, 255))

# 관중석 (좌측 끝, 소형)
STAND_COL = (175, 170, 162)
d.rectangle([56, 60, 64, 72], fill=(*STAND_COL, 255))
d.rectangle([56, 62, 64, 64], fill=(155, 150, 142, 255))
d.rectangle([56, 66, 64, 68], fill=(155, 150, 142, 255))
# 지붕
d.rectangle([55, 56, 65, 60], fill=(120, 115, 108, 255))

# 공원 철제 울타리 (하단)
for fx in range(55, 121, 4):
    d.rectangle([fx, 70, fx+1, 73], fill=(88, 88, 95, 255))
d.line([55, 71, 120, 71], fill=(88, 88, 95, 255), width=1)

# "Albert Park" 작은 표지판
d.rectangle([84, 68, 100, 72], fill=(35, 85, 45, 255))
for sx in [86, 90, 94]:
    d.rectangle([sx, 69, sx+2, 71], fill=(235, 232, 225, 255))

# ════════════════════════════════
# 6. Damodar City (x=120~170)
#    현대식 쇼핑몰/시네마 — 밝은 간판
# ════════════════════════════════
# 건물 본체
d.rectangle([120, 35, 170, 72], fill=(*DAM_WALL, 255))
# 지붕
d.rectangle([119, 33, 171, 36], fill=(185, 185, 190, 255))
# 빨간 상단 간판띠 "DAMODAR CITY"
d.rectangle([120, 36, 170, 44], fill=(*DAM_RED, 255))
# 간판 텍스트 (흰 블록)
for sx in range(124, 166, 5):
    d.rectangle([sx, 38, sx+3, 42], fill=(240, 238, 232, 255))
# 영화관 마키 (노란 띠)
d.rectangle([122, 44, 168, 50], fill=(*DAM_SIGN, 255))
d.rectangle([122, 44, 168, 46], fill=(220, 190, 45, 255))
# 마키 전구 느낌
for bx in range(124, 168, 4):
    d.ellipse([bx, 47, bx+2, 49], fill=(255, 248, 200, 255))
# 유리 전면
d.rectangle([122, 50, 168, 72], fill=(*DAM_GLASS, 220))
# 유리 구획선
for gx in range(130, 168, 12):
    d.line([gx, 50, gx, 72], fill=(88, 82, 72, 255), width=1)
d.line([122, 60, 168, 60], fill=(88, 82, 72, 255), width=1)
# 중앙 입구
d.rectangle([139, 60, 151, 72], fill=(75, 115, 148, 255))
d.line([145, 60, 145, 72], fill=(88, 82, 72, 255), width=1)
# 입구 위 조명
d.rectangle([138, 58, 152, 61], fill=(242, 238, 225, 255))
# 건물 측면 장식 (좌)
d.rectangle([120, 35, 122, 72], fill=(195, 195, 200, 255))

# ════════════════════════════════
# 7. Parliament / Government Buildings (x=170~260)
#    아르데코, 시계탑 (Big Ben), 유약 타일 돔
# ════════════════════════════════
# 메인 건물 (2층)
d.rectangle([170, 40, 260, 72], fill=(*PARL_WALL, 255))
# 지붕 — 아르데코 계단식
d.rectangle([170, 38, 260, 42], fill=(*PARL_TRIM, 255))
d.rectangle([175, 36, 255, 40], fill=(*PARL_TRIM, 255))
# 아르데코 수평 장식선
d.line([170, 44, 260, 44], fill=(*PARL_DARK, 255), width=1)
d.line([170, 55, 260, 55], fill=(*PARL_DARK, 255), width=1)

# 시계탑 (중앙, x=205~230, 건물보다 훨씬 높이)
d.rectangle([205, 8, 230, 40], fill=(*PARL_TOWER, 255))
# 탑 테두리
d.rectangle([205, 8, 207, 40], fill=(*PARL_TRIM, 255))
d.rectangle([228, 8, 230, 40], fill=(*PARL_TRIM, 255))
# 탑 수평 장식 (아르데코 줄)
for ty in [10, 18, 28]:
    d.line([205, ty, 230, ty], fill=(*PARL_DARK, 255), width=1)
# 유약 타일 돔
d.polygon([205, 8, 217, 0, 230, 8], fill=(*PARL_DOME, 255))
d.polygon([208, 8, 217, 2, 226, 8], fill=(*PARL_DOME_L, 255))
# 돔 꼭대기 핀
d.rectangle([216, 0, 218, 4], fill=(*PARL_DARK, 255))
# 시계 (원형)
d.ellipse([212, 20, 224, 32], fill=(*CLOCK_FACE, 255))
d.ellipse([213, 21, 223, 31], fill=(*CLOCK_FACE, 255))
# 시계 테두리
d.ellipse([212, 20, 224, 32], outline=(*PARL_DARK, 255))
# 시계 바늘
d.line([218, 26, 218, 22], fill=(*PARL_DARK, 255), width=1)  # 분침
d.line([218, 26, 221, 24], fill=(*PARL_DARK, 255), width=1)  # 시침

# 탑 아래 아치 창문
for wx in [208, 216, 224]:
    d.rectangle([wx, 33, wx+5, 39], fill=(*WIN_GLASS, 220))
    d.ellipse([wx, 33, wx+5, 36], fill=(*WIN_GLASS, 220))

# 메인 건물 2층 창문 (아치형)
for wx in [174, 184, 194, 234, 244, 254]:
    d.rectangle([wx, 42, wx+7, 52], fill=(*WIN_GLASS, 220))
    d.ellipse([wx, 42, wx+7, 47], fill=(*WIN_GLASS, 220))
    d.line([wx+3, 42, wx+3, 52], fill=(*PARL_DARK, 200), width=1)

# 1층 창문 + 입구
for wx in [174, 184, 194, 234, 244, 254]:
    d.rectangle([wx, 58, wx+7, 68], fill=(*WIN_GLASS, 200))
# 중앙 입구 (x≈217, door position)
d.rectangle([210, 55, 225, 72], fill=(*PARL_DARK, 255))
d.rectangle([212, 57, 223, 72], fill=(*DOOR_W, 255))
d.ellipse([212, 55, 223, 62], fill=(*PARL_TRIM, 255))
# 입구 기둥 (좌우)
d.rectangle([208, 55, 211, 72], fill=(*PARL_WALL, 255))
d.rectangle([224, 55, 227, 72], fill=(*PARL_WALL, 255))
# 계단
d.rectangle([210, 70, 225, 72], fill=(*PARL_TRIM, 255))

# 피지 국기 (의회 앞)
d.rectangle([175, 30, 177, 50], fill=(138, 125, 105, 255))
d.rectangle([177, 30, 192, 38], fill=(*FLAG_B, 255))
d.rectangle([177, 30, 185, 34], fill=(205, 40, 40, 255))
d.rectangle([181, 30, 183, 38], fill=(232, 228, 218, 255))
d.rectangle([177, 33, 192, 35], fill=(232, 228, 218, 255))

# ════════════════════════════════
# 8. 국제기구 사무소 (x=265~320)
# ════════════════════════════════
UN_CONC   = (215, 210, 198, 255)
UN_BAND   = (188, 182, 170, 255)
UN_SIDE   = (175, 168, 155, 255)
UN_WIN    = (118, 155, 185, 255)
UN_WIN_F  = (95, 90, 82, 255)
UN_BLUE   = (42, 88, 155, 255)
UN_CANOPY = (38, 42, 52, 255)

d.rectangle([265, 10, 320, 72], fill=UN_CONC)
d.rectangle([265, 10, 270, 72], fill=UN_SIDE)
d.rectangle([316, 10, 320, 72], fill=UN_SIDE)

for fy in [10, 20, 30, 40, 50, 60]:
    d.rectangle([265, fy, 320, fy+2], fill=UN_BAND)

for fy in [14, 24, 34, 44, 54]:
    for wx in [272, 280, 288, 296, 306]:
        d.rectangle([wx, fy, wx+6, fy+4], fill=UN_WIN_F)
        d.rectangle([wx+1, fy+1, wx+5, fy+3], fill=UN_WIN)

d.rectangle([266, 14, 278, 20], fill=UN_BLUE)
for sx in [268, 271, 274]:
    d.rectangle([sx, 16, sx+2, 18], fill=(230, 235, 245, 255))

d.rectangle([278, 64, 308, 68], fill=UN_CANOPY)
d.rectangle([283, 66, 297, 72], fill=(85, 128, 165, 255))
d.line([(290, 66), (290, 72)], fill=UN_WIN_F, width=1)
d.rectangle([282, 63, 298, 66], fill=UN_BLUE)

d.rectangle([265, 10, 320, 12], fill=UN_BAND)

# ════════════════════════════════
# 9. 인도 (y=72~82)
# ════════════════════════════════
d.rectangle([0, 72, W-1, 82], fill=(*SIDEWALK, 255))
d.line([0, 72, W-1, 72], fill=(*SIDE_EDGE, 255), width=1)
d.line([0, 82, W-1, 82], fill=(*SIDE_EDGE, 255), width=1)
for x in range(0, W, 16):
    d.line([x, 72, x, 82], fill=(*SIDE_EDGE, 255), width=1)
for y in range(76, 82, 4):
    d.line([0, y, W-1, y], fill=(*SIDE_EDGE, 200), width=1)
d.rectangle([0, 80, W-1, 83], fill=(*CURB, 255))

# ════════════════════════════════
# 10. 도로 (y=83~148)
# ════════════════════════════════
for y in range(83, 148):
    shade = ROAD if (y//6)%2==0 else ROAD_L
    d.line([0, y, W-1, y], fill=(*shade, 255))
for x in range(0, W, 20):
    d.rectangle([x, 113, x+10, 116], fill=(*ROAD_LINE, 255))
d.line([0, 83, W-1, 83], fill=(185, 178, 165, 255), width=1)
d.line([0, 147, W-1, 147], fill=(185, 178, 165, 255), width=1)

# ════════════════════════════════
# 11. 잔디 화단 + 목책 (y=148~158)
# ════════════════════════════════
d.rectangle([0, 148, W-1, 158], fill=(*GRASS, 255))
for x in range(0, W, 4):
    d.line([x, 149, x, 153], fill=(*GRASS_D, 255), width=1)
d.rectangle([0, 148, W-1, 150], fill=(*FENCE, 255))
for fx in range(0, W, 6):
    d.rectangle([fx, 148, fx+2, 158], fill=(*FENCE, 255))
    d.polygon([fx, 148, fx+1, 145, fx+2, 148], fill=(*FENCE, 255))

# ════════════════════════════════
# 12. 야자수
# ════════════════════════════════
def palm(px, ground_y, height=30):
    for i in range(height):
        lean = i // 8
        cx2 = px + lean
        w2 = max(1, 3 - i * 2 // height)
        d.rectangle([cx2-w2, ground_y-i, cx2+w2, ground_y-i+1],
                    fill=(*PAL_TRK, 255) if i%3!=2 else (*PAL_TRD, 255))
    top = ground_y - height
    leaf_data = [
        (-16, -8, 14, 5), (-10, -12, 8, 4), (2, -14, 16, 5),
        (8, -8, 16, 4),   (-4, -6, 12, 6),  (-14, -4, 10, 5),
    ]
    for lx, ly, lw, lh in leaf_data:
        bx = px + lean + lx
        by = top + ly
        d.ellipse([bx, by, bx+lw, by+lh], fill=(*PAL_GR, 255))
    for lx, ly, lw, lh in leaf_data[1::2]:
        bx = px + lean + lx + 2
        by = top + ly + 1
        d.ellipse([bx, by, bx+lw-2, by+lh-1], fill=(*PAL_GD, 255))
    for ox, oy in [(-2,-4),(3,-3),(-5,-2)]:
        d.ellipse([px+lean+ox, top+oy, px+lean+ox+4, top+oy+4],
                  fill=(88, 68, 38, 255))

# 야자수: Albert Park 주변 + 도로변
palm(52,  80, 28)   # KODA-Albert 경계
palm(118, 80, 26)   # Albert-Damodar 경계
palm(168, 80, 24)   # Damodar-Parliament 경계
palm(258, 80, 30)   # Parliament-IntlOrg 경계

# ════════════════════════════════
# 13. 가로등
# ════════════════════════════════
def lamppost(lx, ly=80):
    d.rectangle([lx-1, ly, lx+1, ly+28], fill=(155, 150, 140, 255))
    d.line([lx, ly, lx+8, ly-4], fill=(155, 150, 140, 255), width=2)
    d.ellipse([lx+5, ly-8, lx+13, ly-1], fill=(242, 228, 155, 255))

lamppost(45,  75)
lamppost(145, 75)
lamppost(235, 75)
lamppost(305, 75)

# ════════════════════════════════
# 14. 도로 표지판 ("Victoria Parade")
# ════════════════════════════════
d.rectangle([155, 72, 157, 88], fill=(175, 168, 155, 255))
d.rectangle([148, 73, 172, 80], fill=(45, 118, 62, 255))
d.rectangle([148, 73, 172, 80], outline=(32, 95, 48, 255), width=1)
for tx in range(150, 170, 4):
    d.rectangle([tx, 75, tx+2, 78], fill=(240, 238, 232, 255))

# ════════════════════════════════
# 15. 주차된 차
# ════════════════════════════════
# 차 1 (빨간, 좌)
d.rectangle([15, 92, 45, 104], fill=(188, 55, 48, 255))
d.rectangle([20, 89, 40, 94], fill=(168, 48, 42, 255))
d.rectangle([16, 100, 22, 106], fill=(42, 42, 42, 255))
d.rectangle([38, 100, 44, 106], fill=(42, 42, 42, 255))
d.rectangle([22, 90, 38, 94], fill=(*WIN_GLASS, 200))

# 차 2 (검정, 우)
d.rectangle([200, 94, 235, 106], fill=(45, 45, 52, 255))
d.rectangle([205, 91, 230, 96], fill=(38, 38, 45, 255))
d.rectangle([201, 102, 208, 108], fill=(32, 32, 32, 255))
d.rectangle([227, 102, 234, 108], fill=(32, 32, 32, 255))
d.rectangle([207, 91, 228, 96], fill=(*WIN_GLASS, 180))

# ════════════════════════════════
# 16. 항구 / 선착장 (하단, y=158~180)
# ════════════════════════════════
HARBOR_SEA    = (48,  82, 115)
HARBOR_DEEP   = (35,  62,  92)
HARBOR_REFL   = (68, 108, 148)
QUAY_CONC     = (152, 145, 132)
QUAY_EDGE     = (122, 115, 105)
QUAY_SHADOW   = (102,  95,  85)
JETTY_WOOD    = (128,  96,  60)
JETTY_DARK    = (105,  78,  46)
BOLLARD_BODY  = (66,  66,  74)
BOLLARD_CAP   = (88,  88,  98)
ROPE_COL      = (168, 148, 108)

for y in range(163, 180):
    t = (y - 163) / 17
    r = int(HARBOR_SEA[0] + (HARBOR_DEEP[0] - HARBOR_SEA[0]) * t)
    g = int(HARBOR_SEA[1] + (HARBOR_DEEP[1] - HARBOR_SEA[1]) * t)
    b = int(HARBOR_SEA[2] + (HARBOR_DEEP[2] - HARBOR_SEA[2]) * t)
    d.line([0, y, W-1, y], fill=(r, g, b, 255))

for wy in [165, 168, 172, 176]:
    for wx in range(5, 130, 22):
        d.line([wx, wy, wx + 9, wy], fill=(*HARBOR_REFL, 180), width=1)
    for wx in range(312, 195, -22):
        d.line([wx - 8, wy, wx, wy], fill=(*HARBOR_REFL, 160), width=1)

# 부두 (좌: x=0~133, 우: x=187~320)
d.rectangle([0, 158, 133, 163], fill=(*QUAY_CONC, 255))
d.rectangle([0, 163, 133, 167], fill=(*QUAY_SHADOW, 255))
d.line([0, 163, 133, 163], fill=(*QUAY_EDGE, 255), width=1)
d.rectangle([187, 158, W, 163], fill=(*QUAY_CONC, 255))
d.rectangle([187, 163, W, 167], fill=(*QUAY_SHADOW, 255))
d.line([187, 163, W, 163], fill=(*QUAY_EDGE, 255), width=1)

# 목재 선착장 (x=133~187)
d.rectangle([133, 158, 135, 178], fill=(*JETTY_DARK, 255))
d.rectangle([185, 158, 187, 178], fill=(*JETTY_DARK, 255))
d.rectangle([133, 178, 187, 180], fill=(*JETTY_DARK, 255))
for py in range(158, 178):
    plank = JETTY_WOOD if (py % 4) < 2 else JETTY_DARK
    d.rectangle([135, py, 185, py + 1], fill=(*plank, 255))
for py in range(162, 178, 4):
    d.line([135, py, 185, py], fill=(*JETTY_DARK, 200), width=1)

# 볼라드
for bx in [141, 160, 179]:
    d.rectangle([bx - 1, 162, bx + 1, 172], fill=(*BOLLARD_BODY, 255))
    d.ellipse([bx - 3, 160, bx + 3, 165], fill=(*BOLLARD_CAP, 255))

# 모터보트 (나이탬바와 동일)
HULL_DARK  = ( 28,  82, 148, 255)
HULL_LIGHT = ( 52, 112, 175, 255)
INTERIOR   = (218, 212, 200, 255)
MOTOR_BODY = ( 48,  50,  55, 255)
MOTOR_ARM  = ( 38,  40,  44, 255)
WINDSHIELD = (175, 212, 238, 255)

BX1, BX2 = 191, 229
BY1, BY2 = 163, 175

hull_pts = [
    (BX1 + 4, BY2), (BX1, BY1 + 6), (BX1, BY1 + 3),
    (BX1 + 6, BY1), (BX2 - 2, BY1), (BX2, BY1 + 4), (BX2, BY2 - 1),
]
d.polygon(hull_pts, fill=HULL_DARK)
d.line([(BX1 + 6, BY1), (BX2 - 2, BY1)], fill=HULL_LIGHT, width=2)
d.line([(BX1, BY1 + 3), (BX1 + 6, BY1)], fill=HULL_LIGHT, width=1)
d.rectangle([BX1 + 5, BY1 + 2, BX2 - 4, BY1 + 7], fill=INTERIOR)
d.polygon([
    (BX1 + 8, BY1 + 2), (BX1 + 12, BY1 - 2),
    (BX1 + 20, BY1 - 2), (BX1 + 22, BY1 + 2)
], fill=WINDSHIELD)
d.rectangle([BX2 - 1, BY1 + 2, BX2 + 4, BY1 + 9], fill=MOTOR_BODY)
d.rectangle([BX2 + 2, BY1 + 9, BX2 + 4, BY2 - 1], fill=MOTOR_ARM)
d.rectangle([BX2, BY2 - 2, BX2 + 5, BY2], fill=MOTOR_BODY)
d.line([(BX1, BY1 + 5), (181, 169)], fill=(*ROPE_COL, 255), width=1)

for i in range(4):
    rc = (int(28*0.5), int(82*0.5), int(148*0.55), 180 - i*40)
    d.line([(BX1+6+i, BY2+1+i), (BX2-i, BY2+1+i)], fill=rc)

img.save(os.path.join(OUT, "suva_street_bg.png"))
print("저장됨: suva_street_bg.png")
