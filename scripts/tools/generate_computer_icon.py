"""컴퓨터 아이콘 16x16"""
from PIL import Image
import os

OUT = "/Users/nddn/Documents/Claude/Projects/IDC game/assets/sprites/objects"
os.makedirs(OUT, exist_ok=True)

img = Image.new("RGBA", (16, 16), (0,0,0,0))
px = img.load()

MON = (55, 55, 62, 255)
SCREEN = (72, 135, 175, 255)
SCREEN_L = (95, 165, 205, 255)
BASE = (65, 62, 58, 255)
KEY = (75, 72, 68, 255)
KEY_L = (95, 92, 88, 255)

# 모니터
for y in range(2, 10):
    for x in range(3, 13):
        px[x, y] = MON
# 화면
for y in range(3, 9):
    for x in range(4, 12):
        px[x, y] = SCREEN
# 화면 하이라이트
for x in range(4, 8):
    px[x, 3] = SCREEN_L
# 화면 텍스트 (작은 줄)
for x in range(5, 10):
    px[x, 5] = (145, 195, 225, 255)
for x in range(5, 8):
    px[x, 7] = (145, 195, 225, 255)
# 모니터 받침
for x in range(6, 10):
    px[x, 10] = BASE
px[7, 11] = BASE
px[8, 11] = BASE
# 키보드
for y in range(12, 14):
    for x in range(2, 14):
        px[x, y] = KEY
for x in range(3, 13, 2):
    px[x, 12] = KEY_L
for x in range(4, 12, 2):
    px[x, 13] = KEY_L

img.save(os.path.join(OUT, "computer_icon.png"))
print("저장됨: computer_icon.png")
