"""
저수조(water tank) 스프라이트 — 32x24px
콘크리트 원통형 저수조 + 파이프 + 마을 운영 표지판
"""
from PIL import Image, ImageDraw
import os

OUT = "/Users/nddn/Documents/Claude/Projects/IDC game/assets/sprites/objects"
os.makedirs(OUT, exist_ok=True)

img = Image.new("RGBA", (32, 24), (0,0,0,0))
d = ImageDraw.Draw(img)

# 콘크리트 탱크 본체 (원통형)
TANK = (195, 192, 185, 255)
TANK_D = (165, 162, 155, 255)
TANK_L = (215, 212, 205, 255)
PIPE = (108, 112, 118, 255)
PIPE_L = (135, 138, 142, 255)
BASE = (148, 142, 132, 255)
WATER = (72, 155, 185, 255)    # 물 표시
SIGN = (55, 105, 55, 255)

# 기초 (콘크리트 받침)
d.rectangle([4, 20, 28, 23], fill=BASE)

# 탱크 본체 (원통)
d.rectangle([6, 6, 26, 20], fill=TANK)
# 왼쪽 그림자
d.rectangle([6, 6, 9, 20], fill=TANK_D)
# 오른쪽 하이라이트
d.rectangle([23, 6, 26, 20], fill=TANK_L)
# 상단 타원 (뚜껑)
d.ellipse([6, 4, 26, 10], fill=TANK_L)
d.ellipse([8, 5, 24, 9], fill=TANK)
# 물 표시 (탱크 안에 수위선)
d.rectangle([10, 12, 22, 13], fill=WATER)

# 수평 띠 (콘크리트 이음새)
d.line([6, 12, 26, 12], fill=TANK_D, width=1)
d.line([6, 16, 26, 16], fill=TANK_D, width=1)

# 배관 (좌측으로 나감)
d.rectangle([0, 15, 6, 17], fill=PIPE)
d.rectangle([0, 15, 6, 16], fill=PIPE_L)
# 밸브
d.rectangle([2, 13, 5, 15], fill=PIPE)
d.rectangle([3, 12, 4, 14], fill=PIPE_L)

# 배관 (우측 — 마을 방향)
d.rectangle([26, 17, 32, 19], fill=PIPE)
d.rectangle([26, 17, 32, 18], fill=PIPE_L)

# 운영 표지판 (작은 녹색 판)
d.rectangle([12, 1, 20, 5], fill=SIGN)
d.rectangle([15, 5, 17, 7], fill=(88, 82, 72, 255))  # 표지판 기둥
# 표지판 텍스트 (흰 점)
d.point((14, 2), fill=(235, 232, 225, 255))
d.point((16, 2), fill=(235, 232, 225, 255))
d.point((18, 2), fill=(235, 232, 225, 255))
d.point((14, 3), fill=(235, 232, 225, 255))
d.point((16, 3), fill=(235, 232, 225, 255))

out_path = os.path.join(OUT, "water_tank.png")
img.save(out_path)
print(f"저장됨: {out_path}")
