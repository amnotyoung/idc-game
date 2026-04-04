"""
전화기 아이콘 스프라이트 (16x16 픽셀아트)
"""
from PIL import Image
import os

OUT = "/Users/nddn/Documents/Claude/Projects/IDC game/assets/sprites/objects"
os.makedirs(OUT, exist_ok=True)

img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
px = img.load()

# 전화기 본체 (짙은 회색)
BODY = (55, 55, 62, 255)
BODY_L = (72, 72, 80, 255)
# 수화기 (검정)
HANDSET = (35, 35, 40, 255)
# 다이얼/버튼 (밝은 회색)
BTN = (145, 142, 135, 255)
BTN_L = (168, 165, 158, 255)
# 코드
CORD = (42, 42, 48, 255)

# 본체 (6x8, 중앙)
for y in range(6, 14):
    for x in range(5, 11):
        px[x, y] = BODY
# 본체 하이라이트
for x in range(5, 11):
    px[x, 6] = BODY_L

# 버튼 (3x3 그리드)
for by in range(8, 13, 2):
    for bx in range(6, 10, 2):
        px[bx, by] = BTN
        px[bx+1, by] = BTN_L

# 수화기 (위에 걸쳐진 형태)
# 좌 귀마개
px[4, 3] = HANDSET
px[4, 4] = HANDSET
px[5, 3] = HANDSET
px[5, 4] = HANDSET
# 우 귀마개
px[10, 3] = HANDSET
px[10, 4] = HANDSET
px[11, 3] = HANDSET
px[11, 4] = HANDSET
# 연결 바
for x in range(5, 11):
    px[x, 5] = HANDSET

# 전화줄 (본체에서 아래로)
px[8, 14] = CORD
px[9, 15] = CORD
px[7, 15] = CORD

out_path = os.path.join(OUT, "phone_icon.png")
img.save(out_path)
print(f"저장됨: {out_path}")
