"""
Aid World — 플레이스홀더 픽셀아트 스프라이트 생성기
각 캐릭터 16x16, 4방향 (하/좌/우/상) 스프라이트시트 생성
"""
from PIL import Image
import os

# 출력 경로
OUT = "/Users/nddn/Documents/Claude/Projects/IDC game/assets/sprites/characters"
os.makedirs(OUT, exist_ok=True)

TRANSPARENT = (0, 0, 0, 0)

def make_character(skin, shirt, pants, hair, filename):
    """
    16x16 캐릭터 4방향 스프라이트시트 생성 (64x16)
    방향 순서: 하(Down) / 좌(Left) / 우(Right) / 상(Up)
    """
    sheet = Image.new("RGBA", (64, 16), TRANSPARENT)

    for i, direction in enumerate(["down", "left", "right", "up"]):
        sprite = Image.new("RGBA", (16, 16), TRANSPARENT)
        px = sprite.load()

        # ── 공통 픽셀 패턴 ──
        # 머리 (6x6, 중앙 상단)
        for y in range(1, 7):
            for x in range(5, 11):
                px[x, y] = skin

        # 머리카락
        for x in range(5, 11):
            px[x, 1] = hair
            px[x, 2] = hair
        if direction == "up":
            for y in range(1, 5):
                for x in range(5, 11):
                    px[x, y] = hair

        # 몸통 (6x4)
        for y in range(7, 11):
            for x in range(5, 11):
                px[x, y] = shirt

        # 팔
        for y in range(7, 10):
            px[4, y] = skin
            px[11, y] = skin

        # 다리
        for y in range(11, 15):
            px[5, y] = pants
            px[6, y] = pants
            px[9, y] = pants
            px[10, y] = pants

        # 신발
        px[5, 15] = (40, 30, 20, 255)
        px[6, 15] = (40, 30, 20, 255)
        px[9, 15] = (40, 30, 20, 255)
        px[10, 15] = (40, 30, 20, 255)

        # 얼굴 (방향별)
        if direction == "down":
            # 눈
            px[6, 4] = (30, 20, 10, 255)
            px[9, 4] = (30, 20, 10, 255)
            # 입
            px[7, 6] = (180, 80, 80, 255)
            px[8, 6] = (180, 80, 80, 255)
        elif direction == "left":
            px[6, 4] = (30, 20, 10, 255)
            px[5, 4] = (30, 20, 10, 255)
        elif direction == "right":
            px[9, 4] = (30, 20, 10, 255)
            px[10, 4] = (30, 20, 10, 255)
        # up: 뒷모습 — 얼굴 없음

        sheet.paste(sprite, (i * 16, 0))

    sheet.save(os.path.join(OUT, filename))
    print(f"  생성됨: {filename}")


# ── 캐릭터별 컬러 정의 ──
characters = [
    {
        "filename": "player.png",
        "skin":  (220, 175, 130, 255),
        "shirt": (30,  80,  160, 255),   # 파란 셔츠 (KODA 직원)
        "pants": (60,  60,  90,  255),
        "hair":  (30,  20,  10,  255),
    },
    {
        "filename": "mere.png",
        "skin":  (160, 110, 70,  255),   # 피지 원주민 피부톤
        "shirt": (200, 80,  40,  255),   # 주황 셔츠
        "pants": (60,  90,  60,  255),
        "hair":  (10,  8,   5,   255),
    },
    {
        "filename": "timoci.png",
        "skin":  (150, 100, 65,  255),
        "shirt": (40,  40,  80,  255),   # 남색 정장
        "pants": (30,  30,  60,  255),
        "hair":  (10,  8,   5,   255),
    },
    {
        "filename": "ratu_josefa.png",
        "skin":  (140, 95,  60,  255),
        "shirt": (180, 140, 40,  255),   # 황금빛 전통 의상
        "pants": (160, 120, 30,  255),
        "hair":  (60,  40,  10,  255),
    },
    {
        "filename": "james.png",
        "skin":  (230, 195, 160, 255),
        "shirt": (200, 200, 200, 255),   # 밝은 회색 셔츠
        "pants": (80,  80,  100, 255),
        "hair":  (180, 140, 80,  255),   # 금발
    },
    {
        "filename": "lani.png",
        "skin":  (155, 105, 68,  255),
        "shirt": (120, 160, 120, 255),   # 초록 셔츠
        "pants": (80,  60,  40,  255),
        "hair":  (15,  10,  5,   255),
    },
    {
        "filename": "sela.png",
        "skin":  (155, 108, 68,  255),   # 피지 피부톤
        "shirt": (65,  95,  140, 255),   # 네이비 블라우스 (공무원)
        "pants": (45,  45,  65,  255),   # 어두운 치마
        "hair":  (12,  8,   5,   255),
    },
]

print("스프라이트 생성 중...")
for c in characters:
    make_character(c["skin"], c["shirt"], c["pants"], c["hair"], c["filename"])

print("\n완료! 생성된 파일:")
for f in os.listdir(OUT):
    print(f"  {f}")
