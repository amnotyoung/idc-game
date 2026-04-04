"""
정부청사 로비/엘리베이터 홀 배경
320x180 픽셀아트 — 넓은 공간, 엘리베이터 문, 안내판
"""
from PIL import Image, ImageDraw
import os

OUT = "/Users/nddn/Documents/Claude/Projects/IDC game/assets/sprites/tilesets"
os.makedirs(OUT, exist_ok=True)

W, H = 320, 180
img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
d = ImageDraw.Draw(img)

# 팔레트
CEIL     = (232, 228, 218, 255)
WALL     = (218, 212, 198, 255)   # 크림 벽 (정부 건물)
WALL_D   = (198, 192, 178, 255)
MOLDING  = (205, 198, 182, 255)
FLOOR    = (178, 165, 142, 255)   # 대리석 느낌
FLOOR_L  = (195, 182, 158, 255)
FLOOR_D  = (158, 148, 128, 255)
ELEV_DOOR = (165, 168, 175, 255) # 엘리베이터 문 (스테인리스)
ELEV_D   = (135, 138, 145, 255)
ELEV_FRAME = (118, 120, 128, 255)
SIGN_BG  = (42, 75, 118, 255)    # 층 안내판 (파랑)
SIGN_TXT = (235, 232, 225, 255)
PLANT    = (55, 125, 48, 255)
PLANT_D  = (40, 98, 35, 255)
POT      = (155, 120, 78, 255)
BENCH    = (128, 95, 55, 255)    # 나무 벤치
BENCH_L  = (148, 112, 68, 255)
PILLAR   = (205, 198, 185, 255)  # 기둥
PILLAR_D = (185, 178, 165, 255)

# 1. 천장
d.rectangle([0, 0, W, 32], fill=CEIL)
d.line([0, 32, W, 32], fill=MOLDING, width=2)
# 형광등
for lx in [80, 160, 240]:
    d.rectangle([lx-20, 10, lx+20, 14], fill=(228, 232, 235, 255))
    d.rectangle([lx-18, 11, lx+18, 13], fill=(248, 245, 232, 255))

# 2. 벽
d.rectangle([0, 32, W, 108], fill=WALL)
d.rectangle([0, 105, W, 110], fill=MOLDING)
# 벽 텍스처
for x in range(0, W, 24):
    d.line([x, 34, x, 104], fill=WALL_D, width=1)

# 3. 바닥 (대리석 타일 패턴)
for y in range(110, H):
    d.line([0, y, W, y], fill=FLOOR if (y//10)%2==0 else FLOOR_L)
for y in range(110, H, 10):
    d.line([0, y, W, y], fill=FLOOR_D, width=1)
for x in range(0, W, 16):
    d.line([x, 110, x, H], fill=FLOOR_D, width=1)

# 4. 기둥 (좌, 우)
for px in [40, 280]:
    d.rectangle([px-6, 32, px+6, 110], fill=PILLAR)
    d.rectangle([px-6, 32, px-3, 110], fill=PILLAR_D)
    d.rectangle([px-8, 32, px+8, 38], fill=MOLDING)  # 주두
    d.rectangle([px-8, 106, px+8, 110], fill=MOLDING)  # 기초

# 5. 엘리베이터 (중앙 — 2기)
for ex in [130, 190]:
    # 프레임
    d.rectangle([ex-18, 40, ex+18, 100], fill=ELEV_FRAME)
    # 문 (2장)
    d.rectangle([ex-16, 42, ex-1, 98], fill=ELEV_DOOR)
    d.rectangle([ex+1, 42, ex+16, 98], fill=ELEV_DOOR)
    # 문 중앙선 (열리는 부분)
    d.line([ex, 42, ex, 98], fill=ELEV_D, width=2)
    # 문 반사
    d.rectangle([ex-14, 44, ex-8, 55], fill=(185, 188, 195, 255))
    d.rectangle([ex+3, 44, ex+9, 55], fill=(185, 188, 195, 255))
    # 위 표시등 (삼각형)
    d.polygon([ex-4, 37, ex, 33, ex+4, 37], fill=(45, 155, 65, 255))
    # 층 번호 디스플레이
    d.rectangle([ex-6, 34, ex+6, 40], fill=(22, 22, 28, 255))
    d.rectangle([ex-2, 36, ex+2, 38], fill=(55, 185, 75, 255))  # 숫자

# 6. 층 안내판 (벽 좌측)
d.rectangle([60, 48, 110, 95], fill=SIGN_BG)
d.rectangle([60, 48, 110, 95], outline=(32, 55, 95, 255))
# 층 텍스트 블록
for sy, floor_n in [(53, "5F"), (63, "4F"), (73, "3F"), (83, "2F")]:
    for sx in range(65, 85, 5):
        d.rectangle([sx, sy, sx+3, sy+6], fill=SIGN_TXT)
    # 3F, 5F 강조
    if floor_n in ("3F", "5F"):
        d.rectangle([88, sy, 106, sy+6], fill=SIGN_TXT)

# 7. 화분 (좌측)
d.rectangle([18, 92, 28, 108], fill=POT)
d.ellipse([14, 78, 32, 95], fill=PLANT)
d.ellipse([16, 72, 30, 86], fill=PLANT_D)
d.ellipse([20, 68, 34, 80], fill=PLANT)

# 8. 벤치 (우측)
d.rectangle([230, 98, 270, 108], fill=BENCH)
d.rectangle([230, 95, 270, 100], fill=BENCH_L)
d.rectangle([232, 108, 236, 112], fill=BENCH)
d.rectangle([266, 108, 270, 112], fill=BENCH)

# 9. 정부청사 로고/피지 문양 (엘리베이터 사이 벽)
d.rectangle([152, 50, 168, 66], fill=(188, 148, 58, 255))
d.rectangle([154, 52, 166, 64], fill=WALL)
# 피지 국기 느낌
d.rectangle([155, 53, 165, 63], fill=(28, 68, 148, 255))
d.line([160, 53, 160, 63], fill=(235, 232, 225, 255), width=1)
d.line([155, 58, 165, 58], fill=(235, 232, 225, 255), width=1)

# 10. 출입구 (하단 중앙)
d.rectangle([145, 105, 175, 110], fill=FLOOR_L)

out_path = os.path.join(OUT, "lobby_bg.png")
img.save(out_path)
print(f"저장됨: {out_path}")
