"""사업파일 아이콘 16x16 — 마닐라 폴더 + 서류"""
from PIL import Image
import os

OUT = "/Users/nddn/Documents/Claude/Projects/IDC game/assets/sprites/objects"
os.makedirs(OUT, exist_ok=True)

img = Image.new("RGBA", (16, 16), (0,0,0,0))
px = img.load()

FOLDER = (205, 178, 105, 255)    # 마닐라 폴더
FOLDER_D = (178, 152, 85, 255)
FOLDER_TAB = (188, 162, 92, 255)
PAPER = (242, 238, 228, 255)
PAPER_D = (215, 210, 198, 255)
TEXT = (88, 85, 78, 255)
STAMP = (178, 48, 42, 255)      # 빨간 도장

# 폴더 탭 (상단)
for x in range(3, 8):
    px[x, 2] = FOLDER_TAB
    px[x, 3] = FOLDER_TAB

# 폴더 본체
for y in range(4, 14):
    for x in range(2, 14):
        px[x, y] = FOLDER
# 폴더 어두운 아래쪽
for y in range(11, 14):
    for x in range(2, 14):
        px[x, y] = FOLDER_D

# 서류 (폴더 위로 삐져나옴)
for y in range(1, 12):
    for x in range(4, 12):
        px[x, y] = PAPER
# 서류 그림자
for y in range(1, 12):
    px[4, y] = PAPER_D

# 텍스트 줄
for x in range(5, 10):
    px[x, 4] = TEXT
for x in range(5, 9):
    px[x, 6] = TEXT
for x in range(5, 11):
    px[x, 8] = TEXT
for x in range(5, 8):
    px[x, 10] = TEXT

# 빨간 도장 (KODA 승인)
for y in range(5, 8):
    for x in range(9, 12):
        if (x + y) % 2 == 0:
            px[x, y] = STAMP

img.save(os.path.join(OUT, "file_icon.png"))
print("저장됨: file_icon.png")
