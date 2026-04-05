"""
Vikash — 국가계획부 Indo-Fijian 남성 공무원 스프라이트
남색 정장, 넥타이, 안경, 짧은 검은 머리, 콧수염
4방향 스프라이트시트 (64x16, 각 16x16)
"""
from PIL import Image, ImageDraw
import os

OUT = "/Users/nddn/Documents/Claude/Projects/IDC game/assets/sprites/characters"
img = Image.new("RGBA", (64, 16), (0,0,0,0))
d = ImageDraw.Draw(img)

SKIN     = (178, 135, 90, 255)     # Indo-Fijian 피부톤
SUIT     = (38, 38, 72, 255)      # 남색 정장
SUIT_L   = (52, 52, 88, 255)      # 밝은 부분
PANTS    = (30, 30, 58, 255)      # 바지
PANTS_D  = (22, 22, 45, 255)
SHIRT_W  = (228, 225, 218, 255)   # 흰 셔츠 (넥타이 아래)
TIE      = (155, 35, 35, 255)     # 빨간 넥타이
HAIR     = (10, 8, 5, 255)
GLASSES  = (42, 42, 48, 255)      # 안경 테
SHOE     = (32, 28, 22, 255)

for i, facing in enumerate(["down","left","right","up"]):
    ox = i * 16

    d.ellipse([ox+4, 14, ox+12, 16], fill=(0,0,0,55))

    # 바지
    d.rectangle([ox+5, 11, ox+7, 14], fill=PANTS)
    d.rectangle([ox+9, 11, ox+11, 14], fill=PANTS)
    d.rectangle([ox+7, 11, ox+9, 13], fill=PANTS_D)

    # 구두
    d.rectangle([ox+5, 14, ox+7, 15], fill=SHOE)
    d.rectangle([ox+9, 14, ox+11, 15], fill=SHOE)

    # 정장 재킷
    d.rectangle([ox+4, 6, ox+12, 11], fill=SUIT)
    d.rectangle([ox+4, 6, ox+12, 7], fill=SUIT_L)  # 어깨
    # 흰 셔츠 (V)
    d.point((ox+7, 7), fill=SHIRT_W)
    d.point((ox+8, 7), fill=SHIRT_W)
    d.point((ox+8, 8), fill=SHIRT_W)
    d.point((ox+7, 8), fill=SHIRT_W)
    # 넥타이
    d.line([(ox+8, 7), (ox+8, 10)], fill=TIE)
    d.point((ox+8, 7), fill=TIE)
    # 재킷 단추
    d.point((ox+7, 9), fill=(28, 28, 55, 255))
    d.point((ox+9, 9), fill=(28, 28, 55, 255))

    # 팔
    if facing == "left":
        d.rectangle([ox+3, 7, ox+5, 10], fill=SUIT)
        d.rectangle([ox+11, 7, ox+12, 9], fill=SUIT)
    elif facing == "right":
        d.rectangle([ox+4, 7, ox+5, 9], fill=SUIT)
        d.rectangle([ox+11, 7, ox+13, 10], fill=SUIT)
    else:
        d.rectangle([ox+3, 7, ox+5, 10], fill=SUIT)
        d.rectangle([ox+11, 7, ox+13, 10], fill=SUIT)

    # 목
    d.rectangle([ox+7, 4, ox+9, 7], fill=SKIN)

    # 머리
    d.rectangle([ox+5, 1, ox+11, 5], fill=SKIN)
    # 짧은 머리카락
    d.rectangle([ox+5, 1, ox+11, 2], fill=HAIR)
    if facing == "up":
        d.rectangle([ox+5, 1, ox+11, 4], fill=HAIR)
    elif facing == "left":
        d.rectangle([ox+10, 1, ox+11, 3], fill=HAIR)
    elif facing == "right":
        d.rectangle([ox+5, 1, ox+6, 3], fill=HAIR)

    # 얼굴
    MUSTACHE = (25, 18, 10, 255)
    if facing == "down":
        # 안경
        d.rectangle([ox+6, 3, ox+8, 4], fill=GLASSES)
        d.rectangle([ox+8, 3, ox+10, 4], fill=GLASSES)
        d.point((ox+8, 3), fill=GLASSES)  # 코 브릿지
        # 눈 (안경 안)
        d.point((ox+7, 3), fill=(20, 12, 8, 255))
        d.point((ox+9, 3), fill=(20, 12, 8, 255))
        # 콧수염
        d.line([ox+6, 4, ox+10, 4], fill=MUSTACHE)
    elif facing == "left":
        d.rectangle([ox+5, 3, ox+7, 4], fill=GLASSES)
        d.point((ox+6, 3), fill=(20, 12, 8, 255))
        d.line([ox+5, 4, ox+7, 4], fill=MUSTACHE)
    elif facing == "right":
        d.rectangle([ox+9, 3, ox+11, 4], fill=GLASSES)
        d.point((ox+10, 3), fill=(20, 12, 8, 255))
        d.line([ox+9, 4, ox+11, 4], fill=MUSTACHE)

out_path = os.path.join(OUT, "timoci.png")
img.save(out_path)
print(f"저장됨: {out_path}")
