"""
Aid World — Tiny Dungeon 타일셋 기반 사무실 배경 생성
320x180 탑다운 뷰
"""
from PIL import Image, ImageDraw
import os

SRC = "/Users/nddn/Documents/Claude/Projects/IDC game/kenney_tiny-dungeon/Tilemap/tilemap_packed.png"
OUT = "/Users/nddn/Documents/Claude/Projects/IDC game/assets/sprites/tilesets"
os.makedirs(OUT, exist_ok=True)

tilemap = Image.open(SRC)

def tile(col, row):
    """타일맵에서 16x16 타일 하나 추출"""
    return tilemap.crop((col*16, row*16, col*16+16, row*16+16))

def paste_tile(canvas, col, row, x, y):
    t = tile(col, row).convert("RGBA")
    canvas.paste(t, (x, y))

def fill_tile(canvas, col, row, x1, y1, x2, y2):
    """특정 영역을 타일로 채우기"""
    t = tile(col, row).convert("RGBA")
    for ty in range(y1, y2, 16):
        for tx in range(x1, x2, 16):
            w = min(16, x2 - tx)
            h = min(16, y2 - ty)
            canvas.paste(t.crop((0, 0, w, h)), (tx, ty))

W, H = 320, 180
img = Image.new("RGBA", (W, H), (0, 0, 0, 255))

# ── 1. 바닥 — 베이지 카펫 (tiles 0~2, row 3~4 교차) ──
for ty in range(10, 170, 16):
    for tx in range(10, 310, 16):
        c = ((tx // 16) + (ty // 16)) % 2
        fill_tile(img, c, 3, tx, ty, min(tx+16, 310), min(ty+16, 170))

# ── 2. 벽 — 회색 돌 (row 0, col 9~11) ──
# 상단 벽
for tx in range(0, W, 16):
    fill_tile(img, 9 + (tx//16)%3, 0, tx, 0, min(tx+16, W), 10)
# 하단 벽
for tx in range(0, W, 16):
    fill_tile(img, 9 + (tx//16)%3, 1, tx, 170, min(tx+16, W), H)
# 좌측 벽
for ty in range(0, H, 16):
    fill_tile(img, 9, (ty//16)%2, 0, ty, 10, min(ty+16, H))
# 우측 벽
for ty in range(0, H, 16):
    fill_tile(img, 11, (ty//16)%2, 310, ty, W, min(ty+16, H))

# ── 3. 문 (상단 중앙) — 나무문 (col 10~11, row 3) ──
paste_tile(img, 10, 3, 144, 0)
paste_tile(img, 11, 3, 160, 0)

# ── 4. 창문 (좌/우 벽에 밝은 느낌) ──
d = ImageDraw.Draw(img)
for wx in [25, 55]:
    d.rectangle([wx, 1, wx+18, 9], fill=(160, 210, 230, 200))
    d.line([wx+9, 1, wx+9, 9], fill=(100, 140, 160, 255), width=1)
    d.line([wx, 5, wx+18, 5], fill=(100, 140, 160, 255), width=1)
for wx in [247, 277]:
    d.rectangle([wx, 1, wx+18, 9], fill=(160, 210, 230, 200))
    d.line([wx+9, 1, wx+9, 9], fill=(100, 140, 160, 255), width=1)
    d.line([wx, 5, wx+18, 5], fill=(100, 140, 160, 255), width=1)

# ── 5. 책장 (좌측, col 3 row 5~6 스택) ──
paste_tile(img, 3, 5, 12, 20)
paste_tile(img, 3, 6, 12, 36)
paste_tile(img, 3, 5, 12, 52)
paste_tile(img, 3, 6, 12, 68)

# ── 6. 메인 책상 (픽셀아트 수작업) ──
desk = Image.new("RGBA", (72, 28), (0,0,0,0))
dd = ImageDraw.Draw(desk)
dd.rectangle([0, 0, 71, 27],  fill=(150, 105, 55, 255))
dd.rectangle([0, 0, 71, 27],  outline=(100, 70, 35, 255), width=1)
dd.rectangle([0, 22, 71, 27], fill=(120, 82, 42, 255))  # 앞면
# 모니터
dd.rectangle([22, 3, 40, 15], fill=(40, 40, 50, 255))
dd.rectangle([24, 5, 38, 13], fill=(90, 170, 210, 255))
dd.rectangle([29, 15, 33, 17], fill=(40, 40, 50, 255))
dd.rectangle([27, 17, 35, 19], fill=(40, 40, 50, 255))
# 키보드
dd.rectangle([10, 14, 24, 19], fill=(80, 82, 92, 255))
for kx in range(12, 24, 3):
    dd.line([(kx, 15), (kx, 18)], fill=(60, 62, 72, 255), width=1)
# 서류
dd.rectangle([44, 4, 66, 16], fill=(238, 232, 210, 255))
for ly in range(7, 15, 3):
    dd.line([(46, ly), (64, ly)], fill=(180, 174, 155, 255), width=1)
img.paste(desk, (46, 52), desk)

# 의자
chair = Image.new("RGBA", (16, 16), (0,0,0,0))
cd = ImageDraw.Draw(chair)
cd.rectangle([2, 2, 13, 13], fill=(55, 78, 130, 255))
cd.rectangle([2, 2, 13, 13], outline=(38, 55, 95, 255), width=1)
cd.rectangle([4, 0, 11, 3], fill=(55, 78, 130, 255))
img.paste(chair, (74, 82), chair)

# ── 7. 보조 책상 (우측) ──
img.paste(desk, (198, 52), desk)
img.paste(chair, (226, 82), chair)

# ── 8. 회의 테이블 ──
mtable = Image.new("RGBA", (128, 32), (0,0,0,0))
md = ImageDraw.Draw(mtable)
md.rectangle([0, 0, 127, 31], fill=(150, 105, 55, 255))
md.rectangle([0, 0, 127, 31], outline=(100, 70, 35, 255), width=1)
md.rectangle([0, 26, 127, 31], fill=(120, 82, 42, 255))
# 테이블 위 서류/컵
md.rectangle([10, 6, 28, 16],  fill=(238, 232, 210, 255))
md.ellipse([55, 7, 66, 18],    fill=(175, 95, 55, 255))
md.ellipse([57, 9, 64, 16],    fill=(70, 42, 22, 255))
md.rectangle([80, 5, 114, 18], fill=(238, 232, 210, 255))
img.paste(mtable, (96, 132), mtable)

# 회의 의자
for cx in [104, 128, 152, 176, 200]:
    img.paste(chair, (cx - 8, 118), chair)
    img.paste(chair, (cx - 8, 165), chair)

# ── 9. 화분 (col 5, row 5 느낌 수작업) ──
for px, py in [(292, 18), (292, 148)]:
    d.ellipse([px-7, py-3, px+7, py+5], fill=(130, 80, 40, 255))
    d.ellipse([px-5, py-10, px+1, py-2], fill=(55, 135, 65, 255))
    d.ellipse([px-1, py-12, px+6, py-3], fill=(45, 115, 55, 255))
    d.ellipse([px-3, py-8, px+4, py-1],  fill=(65, 150, 70, 255))

# ── 10. 액자/화이트보드 (우측 벽) ──
d.rectangle([268, 15, 306, 48], fill=(90, 80, 68, 255))
d.rectangle([270, 17, 304, 46], fill=(245, 242, 235, 255))
d.line([272, 22, 302, 22], fill=(180, 175, 162, 255), width=1)
d.line([272, 27, 302, 27], fill=(180, 175, 162, 255), width=1)
d.line([272, 32, 290, 32], fill=(180, 175, 162, 255), width=1)
d.text((272, 36), "KODA", fill=(100, 95, 82, 255))

img.save(os.path.join(OUT, "office_bg.png"))
print("저장됨: assets/sprites/tilesets/office_bg.png")
