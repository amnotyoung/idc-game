"""
토지청 사무실 배경 (5층)
320x180 픽셀아트 — 현대적, 밝고 깨끗한 사무실
출력: assets/sprites/tilesets/landoffice_bg.png
"""
from PIL import Image, ImageDraw
import os

OUT = "/Users/nddn/Documents/Claude/Projects/IDC game/assets/sprites/tilesets"
os.makedirs(OUT, exist_ok=True)

W, H = 320, 180
img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
d = ImageDraw.Draw(img)

# 팔레트 — 밝고 현대적
CEIL       = (242, 240, 235, 255)
WALL       = (235, 238, 240, 255)   # 밝은 회청색
WALL_TRIM  = (215, 218, 222, 255)
FLOOR      = (195, 192, 185, 255)   # 회색 타일
FLOOR_D    = (178, 175, 168, 255)
FLOOR_LINE = (165, 162, 155, 255)
WIN_SKY    = (135, 190, 235, 255)
WIN_SKY2   = (165, 210, 248, 255)
WIN_FRAME  = (175, 175, 180, 255)   # 알루미늄 프레임
DESK_TOP   = (215, 212, 205, 255)   # 밝은 데스크
DESK_SIDE  = (185, 182, 175, 255)
DESK_LEG   = (148, 145, 138, 255)
MONITOR    = (35, 35, 42, 255)
SCREEN     = (88, 155, 195, 255)
CHAIR      = (55, 55, 65, 255)
PLANT      = (62, 135, 55, 255)
PLANT_D    = (45, 105, 40, 255)
POT        = (165, 128, 85, 255)
SHELF      = (195, 188, 175, 255)
SIGN       = (42, 88, 135, 255)     # 토지청 간판
PAPER      = (245, 242, 232, 255)
MAP_BG     = (225, 218, 195, 255)   # 지도 배경
MAP_LINE   = (55, 105, 65, 255)     # 지도 선
DOOR_COL   = (175, 172, 165, 255)
LIGHT_FIX  = (225, 228, 232, 255)
LIGHT_ON   = (255, 250, 235, 255)

# 1. 천장
d.rectangle([0, 0, W-1, 35], fill=CEIL)
d.line([0, 35, W-1, 35], fill=WALL_TRIM, width=1)
# 형광등 (2개)
for lx in [80, 240]:
    d.rectangle([lx-25, 8, lx+25, 12], fill=LIGHT_FIX)
    d.rectangle([lx-22, 9, lx+22, 11], fill=LIGHT_ON)

# 2. 벽
d.rectangle([0, 35, W-1, 110], fill=WALL)
d.rectangle([0, 108, W-1, 112], fill=WALL_TRIM)

# 3. 바닥 (회색 타일)
for y in range(112, H):
    d.line([0, y, W-1, y], fill=FLOOR if (y//8)%2==0 else FLOOR_D)
for y in range(112, H, 8):
    d.line([0, y, W-1, y], fill=FLOOR_LINE, width=1)
for x in range(0, W, 12):
    d.line([x, 112, x, H-1], fill=FLOOR_LINE, width=1)

# 4. 창문 (큰 유리창 2개 — 현대적)
for wx in [60, 200]:
    # 프레임
    d.rectangle([wx-35, 40, wx+35, 95], fill=WIN_FRAME)
    # 유리
    d.rectangle([wx-33, 42, wx-2, 93], fill=WIN_SKY)
    d.rectangle([wx+2, 42, wx+33, 93], fill=WIN_SKY)
    # 하늘 그라디언트
    for y in range(42, 93):
        t = (y - 42) / 50
        r = int(WIN_SKY[0] + (WIN_SKY2[0]-WIN_SKY[0]) * t)
        g = int(WIN_SKY[1] + (WIN_SKY2[1]-WIN_SKY[1]) * t)
        b = int(WIN_SKY[2] + (WIN_SKY2[2]-WIN_SKY[2]) * t)
        d.line([wx-33, y, wx-2, y], fill=(r,g,b,255))
        d.line([wx+2, y, wx+33, y], fill=(r,g,b,255))
    # 구름
    d.ellipse([wx-20, 50, wx+5, 58], fill=(240, 242, 248, 255))
    # 중앙 프레임 세로선
    d.line([wx, 42, wx, 93], fill=WIN_FRAME, width=2)
    # 가로 프레임
    d.line([wx-33, 68, wx+33, 68], fill=WIN_FRAME, width=1)

# 5. 벽 왼쪽: 토지청 간판 + 지도
# 간판
d.rectangle([10, 42, 35, 52], fill=SIGN)
for sx in range(13, 32, 4):
    d.rectangle([sx, 45, sx+2, 49], fill=(225, 228, 235, 255))
# 지도 (섬 형태)
d.rectangle([10, 58, 38, 90], fill=MAP_BG)
d.rectangle([10, 58, 38, 90], outline=(155, 148, 128, 255))
# 섬 윤곽
d.polygon([15, 70, 20, 62, 28, 65, 33, 72, 30, 82, 22, 85, 15, 78], fill=MAP_LINE)
d.point((24, 72), fill=(195, 45, 35, 255))  # 마커

# 6. 책장 (오른쪽 벽)
d.rectangle([268, 40, 310, 105], fill=SHELF)
for sy in [50, 65, 80, 95]:
    d.line([270, sy, 308, sy], fill=(175, 168, 155, 255), width=1)
# 파일/책
for sy in [42, 57, 72, 87]:
    for sx in range(272, 306, 6):
        col = [(55, 85, 125, 255), (125, 55, 55, 255), (55, 105, 65, 255), (165, 135, 55, 255)]
        d.rectangle([sx, sy, sx+4, sy+7], fill=col[(sx//6)%4])

# 7. Sela 책상 (중앙)
d.rectangle([120, 85, 200, 95], fill=DESK_TOP)
d.rectangle([120, 95, 200, 105], fill=DESK_SIDE)
d.rectangle([125, 105, 130, 112], fill=DESK_LEG)
d.rectangle([190, 105, 195, 112], fill=DESK_LEG)
# 모니터
d.rectangle([148, 75, 172, 88], fill=MONITOR)
d.rectangle([150, 77, 170, 86], fill=SCREEN)
d.rectangle([157, 88, 163, 90], fill=MONITOR)
# 서류 더미
d.rectangle([125, 82, 145, 90], fill=PAPER)
d.rectangle([126, 83, 144, 84], fill=(215, 212, 205, 255))
# 펜꽂이
d.rectangle([178, 82, 185, 88], fill=(85, 82, 75, 255))

# 8. 의자 (책상 아래)
d.rectangle([152, 100, 168, 112], fill=CHAIR)
d.rectangle([152, 96, 168, 100], fill=(65, 65, 75, 255))

# 9. 화분 (창문 사이)
d.rectangle([132, 98, 138, 110], fill=POT)
d.ellipse([130, 88, 140, 100], fill=PLANT)
d.ellipse([128, 82, 138, 92], fill=PLANT_D)
d.ellipse([133, 78, 142, 88], fill=PLANT)

# 10. 출입문 (왼쪽 하단)
d.rectangle([40, 50, 55, 110], fill=DOOR_COL)
d.rectangle([42, 52, 53, 108], fill=(185, 182, 175, 255))
d.point((51, 80), fill=(165, 155, 105, 255))  # 손잡이

# ── 저장 ──
out_path = os.path.join(OUT, "landoffice_bg.png")
img.save(out_path)
print(f"저장됨: {out_path}")
