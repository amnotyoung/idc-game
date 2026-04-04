"""
Sela — 토지청 여성 공무원 스프라이트
네이비 블라우스, 연한 갈색 sulu i ra (여성 정장 치마), 긴 머리
4방향 스프라이트시트 (64x16, 각 16x16)
"""
from PIL import Image, ImageDraw
import os

OUT = "/Users/nddn/Documents/Claude/Projects/IDC game/assets/sprites/characters"
os.makedirs(OUT, exist_ok=True)

img = Image.new("RGBA", (64, 16), (0,0,0,0))
d = ImageDraw.Draw(img)

SKIN    = (155, 108, 68, 255)
BLOUSE  = (55, 75, 120, 255)      # 네이비 블라우스
BLOUSE_L = (75, 95, 140, 255)     # 밝은 부분
SKIRT   = (128, 108, 82, 255)     # sulu i ra (갈색)
SKIRT_D = (108, 88, 62, 255)      # 치마 어두운 부분
HAIR    = (12, 8, 5, 255)         # 검은 머리
HAIR_H  = (28, 20, 12, 255)      # 머리 하이라이트
SHOE    = (62, 48, 35, 255)       # 구두
ACCESSORY = (185, 155, 45, 255)   # 귀걸이/목걸이 (금색)

for i, facing in enumerate(["down","left","right","up"]):
    ox = i * 16

    # 그림자
    d.ellipse([ox+4, 14, ox+12, 16], fill=(0,0,0,55))

    # 치마 (여성용 sulu i ra — 넓고 무릎까지)
    d.rectangle([ox+4, 10, ox+12, 14], fill=SKIRT)
    d.rectangle([ox+4, 12, ox+12, 14], fill=SKIRT_D)
    # 치마 주름선
    d.line([(ox+7, 10), (ox+7, 14)], fill=SKIRT_D)
    d.line([(ox+9, 10), (ox+9, 14)], fill=SKIRT_D)

    # 구두
    d.rectangle([ox+4, 13, ox+7, 15], fill=SHOE)
    d.rectangle([ox+9, 13, ox+12, 15], fill=SHOE)

    # 블라우스
    d.rectangle([ox+5, 6, ox+11, 10], fill=BLOUSE)
    # 블라우스 밝은 부분
    d.rectangle([ox+5, 6, ox+11, 7], fill=BLOUSE_L)
    # 단추
    d.line([(ox+8, 6), (ox+8, 10)], fill=(45, 60, 95, 255))

    # 팔
    if facing == "left":
        d.rectangle([ox+3, 7, ox+5, 10], fill=SKIN)
        d.rectangle([ox+11, 7, ox+12, 9], fill=SKIN)
    elif facing == "right":
        d.rectangle([ox+4, 7, ox+5, 9], fill=SKIN)
        d.rectangle([ox+11, 7, ox+13, 10], fill=SKIN)
    else:
        d.rectangle([ox+3, 7, ox+5, 10], fill=SKIN)
        d.rectangle([ox+11, 7, ox+13, 10], fill=SKIN)

    # 목
    d.rectangle([ox+7, 4, ox+9, 7], fill=SKIN)
    # 목걸이
    d.point((ox+7, 6), fill=ACCESSORY)
    d.point((ox+8, 6), fill=ACCESSORY)

    # 머리 (긴 머리 — 여성)
    d.rectangle([ox+5, 0, ox+11, 5], fill=SKIN)
    # 머리카락 (윗부분 + 옆으로 내려오는 긴 머리)
    d.rectangle([ox+5, 0, ox+11, 2], fill=HAIR)
    if facing == "down":
        # 앞머리
        d.rectangle([ox+5, 0, ox+11, 1], fill=HAIR)
        # 긴 머리 양옆
        d.rectangle([ox+4, 2, ox+6, 8], fill=HAIR)
        d.rectangle([ox+10, 2, ox+12, 8], fill=HAIR)
        # 머리 하이라이트
        d.point((ox+5, 3), fill=HAIR_H)
        d.point((ox+11, 3), fill=HAIR_H)
        # 귀걸이
        d.point((ox+4, 4), fill=ACCESSORY)
        d.point((ox+12, 4), fill=ACCESSORY)
        # 얼굴
        d.point((ox+7, 3), fill=(20, 12, 8, 255))  # 눈
        d.point((ox+9, 3), fill=(20, 12, 8, 255))
        d.line([ox+7, 4, ox+9, 4], fill=(160, 90, 70, 255))  # 입
    elif facing == "left":
        d.rectangle([ox+10, 1, ox+12, 8], fill=HAIR)
        d.rectangle([ox+5, 1, ox+6, 5], fill=HAIR)
        d.point((ox+6, 3), fill=(20, 12, 8, 255))
    elif facing == "right":
        d.rectangle([ox+4, 1, ox+6, 8], fill=HAIR)
        d.rectangle([ox+10, 1, ox+11, 5], fill=HAIR)
        d.point((ox+10, 3), fill=(20, 12, 8, 255))
    elif facing == "up":
        # 뒷모습 — 긴 머리 전체
        d.rectangle([ox+4, 0, ox+12, 8], fill=HAIR)
        d.point((ox+6, 4), fill=HAIR_H)
        d.point((ox+9, 5), fill=HAIR_H)

out_path = os.path.join(OUT, "sela.png")
img.save(out_path)
print(f"저장됨: {out_path}")
