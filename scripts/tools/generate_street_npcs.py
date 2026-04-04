"""
수바 거리 NPC 스프라이트 v2
각자 실루엣이 다르게 — 개별 드로잉
4방향 스프라이트시트 (64x16, 각 16x16)
열 순서: 0=하, 1=좌, 2=우, 3=상
"""
from PIL import Image, ImageDraw
import os

OUT = "/Users/nddn/Documents/Claude/Projects/IDC game/assets/sprites/characters"
os.makedirs(OUT, exist_ok=True)

def new_sheet():
    img = Image.new("RGBA", (64, 16), (0,0,0,0))
    return img, ImageDraw.Draw(img)

def save(img, name):
    img.save(os.path.join(OUT, name))
    print(f"저장됨: {name}")

# ══════════════════════════════════════
# 1. 피지 남성 (파란 셔츠 + sulu 치마바지)
#    특징: 보통 체형, 짧은 머리, 무릎 길이 sulu
# ══════════════════════════════════════
img, d = new_sheet()
SKIN  = (165, 118, 75, 255)
SHIRT = (58, 148, 192, 255)
SULU  = (82, 65, 108, 255)   # 짙은 보라 — sulu
HAIR  = (22, 14, 10, 255)
SHOE  = (38, 30, 22, 255)

for i, facing in enumerate(["down","left","right","up"]):
    ox = i * 16

    # 그림자
    d.ellipse([ox+4,14,ox+12,16], fill=(0,0,0,55))

    # sulu (치마 — 넓게)
    d.rectangle([ox+4, 10, ox+12, 14], fill=SULU)
    # 신발
    d.rectangle([ox+4,13,ox+7,15], fill=SHOE)
    d.rectangle([ox+9,13,ox+12,15], fill=SHOE)

    # 몸통
    d.rectangle([ox+5, 6, ox+11, 10], fill=SHIRT)

    # 팔
    if facing == "left":
        d.rectangle([ox+3,7,ox+5,10], fill=SKIN)
        d.rectangle([ox+11,7,ox+12,9], fill=SKIN)
    elif facing == "right":
        d.rectangle([ox+4,7,ox+5,9], fill=SKIN)
        d.rectangle([ox+11,7,ox+13,10], fill=SKIN)
    else:
        d.rectangle([ox+3,7,ox+5,10], fill=SKIN)
        d.rectangle([ox+11,7,ox+13,10], fill=SKIN)

    # 목
    d.rectangle([ox+7,4,ox+9,7], fill=SKIN)

    # 머리
    d.rectangle([ox+5,1,ox+11,5], fill=SKIN)

    # 머리카락 (짧음)
    d.rectangle([ox+5,1,ox+11,2], fill=HAIR)
    if facing == "left":
        d.rectangle([ox+10,1,ox+11,4], fill=HAIR)
    elif facing == "right":
        d.rectangle([ox+5,1,ox+6,4], fill=HAIR)
    elif facing == "up":
        d.rectangle([ox+5,1,ox+6,4], fill=HAIR)
        d.rectangle([ox+10,1,ox+11,4], fill=HAIR)

    # 얼굴
    if facing == "down":
        d.point((ox+7,3), fill=(20,12,8,255))
        d.point((ox+9,3), fill=(20,12,8,255))
        d.line([ox+7,4,ox+9,4], fill=(160,90,70,255))
    elif facing == "left":
        d.point((ox+6,3), fill=(20,12,8,255))
    elif facing == "right":
        d.point((ox+10,3), fill=(20,12,8,255))

save(img, "npc_bula_man.png")

# ══════════════════════════════════════
# 2. 피지 여성 A (산호색 bula 드레스)
#    특징: 긴 머리, 원피스 실루엣, 약간 넓은 치마
# ══════════════════════════════════════
img, d = new_sheet()
SKIN  = (152, 105, 65, 255)
DRESS = (215, 82, 58, 255)    # 산호/오렌지
DRESS2= (195, 65, 45, 255)    # 드레스 어두운 부분
HAIR  = (18, 10, 6, 255)
HAIR2 = (32, 20, 12, 255)
SHOE  = (120, 68, 42, 255)    # 샌들

for i, facing in enumerate(["down","left","right","up"]):
    ox = i * 16
    d.ellipse([ox+4,14,ox+12,16], fill=(0,0,0,55))

    # 치마 (넓고 길게)
    d.polygon([ox+4,9, ox+3,14, ox+13,14, ox+12,9], fill=DRESS2)
    # 신발
    d.rectangle([ox+5,13,ox+7,15], fill=SHOE)
    d.rectangle([ox+9,13,ox+11,15], fill=SHOE)

    # 몸통
    d.rectangle([ox+5,5,ox+11,10], fill=DRESS)

    # 팔 (가늘게)
    if facing == "left":
        d.rectangle([ox+3,6,ox+5,9], fill=SKIN)
        d.rectangle([ox+11,6,ox+12,8], fill=SKIN)
    elif facing == "right":
        d.rectangle([ox+4,6,ox+5,8], fill=SKIN)
        d.rectangle([ox+11,6,ox+13,9], fill=SKIN)
    else:
        d.rectangle([ox+3,6,ox+5,9], fill=SKIN)
        d.rectangle([ox+11,6,ox+13,9], fill=SKIN)

    # 목
    d.rectangle([ox+7,3,ox+9,6], fill=SKIN)

    # 머리 (약간 둥글게)
    d.ellipse([ox+5,0,ox+11,5], fill=SKIN)

    # 긴 머리카락
    if facing == "down":
        d.rectangle([ox+4,1,ox+6,8], fill=HAIR)   # 왼쪽 머리카락
        d.rectangle([ox+10,1,ox+12,8], fill=HAIR)  # 오른쪽
        d.rectangle([ox+5,0,ox+11,2], fill=HAIR)   # 윗 머리
    elif facing == "left":
        d.rectangle([ox+5,0,ox+11,2], fill=HAIR)
        d.rectangle([ox+10,1,ox+12,8], fill=HAIR)  # 앞 머리카락
    elif facing == "right":
        d.rectangle([ox+5,0,ox+11,2], fill=HAIR)
        d.rectangle([ox+4,1,ox+6,8], fill=HAIR)
    elif facing == "up":
        d.rectangle([ox+4,1,ox+6,8], fill=HAIR)
        d.rectangle([ox+10,1,ox+12,8], fill=HAIR)
        d.rectangle([ox+5,0,ox+11,2], fill=HAIR2)

    # 얼굴
    if facing == "down":
        d.point((ox+7,2), fill=(20,12,8,255))
        d.point((ox+9,2), fill=(20,12,8,255))
        d.point((ox+8,3), fill=(190,110,90,255))  # 입술
    elif facing == "left":
        d.point((ox+6,2), fill=(20,12,8,255))
    elif facing == "right":
        d.point((ox+10,2), fill=(20,12,8,255))

save(img, "npc_bula_woman.png")

# ══════════════════════════════════════
# 3. 노점상 남성 (노란 셔츠 + 밀짚모자)
#    특징: 모자, 앞치마 느낌, 약간 뚱뚱한 체형
# ══════════════════════════════════════
img, d = new_sheet()
SKIN  = (205, 168, 112, 255)   # Indo-Fijian 피부톤 (확실하게 밝게)
SHIRT = (232, 210, 72, 255)
APRON = (235, 225, 195, 255)
PANTS = (58, 78, 45, 255)
HAT   = (205, 175, 105, 255)
HAT_B = (175, 145, 78, 255)
SHOE  = (45, 35, 25, 255)

for i, facing in enumerate(["down","left","right","up"]):
    ox = i * 16
    d.ellipse([ox+3,14,ox+13,16], fill=(0,0,0,55))

    # 다리 (약간 넓게)
    d.rectangle([ox+5,10,ox+8,14], fill=PANTS)
    d.rectangle([ox+9,10,ox+11,14], fill=PANTS)
    d.rectangle([ox+4,13,ox+8,15], fill=SHOE)
    d.rectangle([ox+9,13,ox+12,15], fill=SHOE)

    # 몸통 (넓게)
    d.rectangle([ox+4,6,ox+12,10], fill=SHIRT)
    # 앞치마
    d.rectangle([ox+5,7,ox+11,10], fill=APRON)

    # 팔 (약간 굵게)
    if facing == "left":
        d.rectangle([ox+2,7,ox+4,10], fill=SKIN)
        d.rectangle([ox+12,7,ox+13,9], fill=SKIN)
    elif facing == "right":
        d.rectangle([ox+3,7,ox+4,9], fill=SKIN)
        d.rectangle([ox+12,7,ox+14,10], fill=SKIN)
    else:
        d.rectangle([ox+2,7,ox+4,10], fill=SKIN)
        d.rectangle([ox+12,7,ox+14,10], fill=SKIN)

    # 목
    d.rectangle([ox+7,4,ox+9,7], fill=SKIN)

    # 머리
    d.rectangle([ox+5,2,ox+11,5], fill=SKIN)

    # 밀짚모자
    d.rectangle([ox+4,0,ox+12,2], fill=HAT)   # 챙
    d.rectangle([ox+5,0,ox+11,1], fill=HAT_B) # 모자 테두리
    d.ellipse([ox+5,0,ox+11,3], fill=HAT)     # 모자 윗부분
    d.line([ox+4,2,ox+12,2], fill=HAT_B, width=1)  # 챙 선

    # 얼굴
    if facing == "down":
        d.point((ox+7,3), fill=(20,12,8,255))
        d.point((ox+9,3), fill=(20,12,8,255))
        d.line([ox+7,4,ox+9,4], fill=(165,95,72,255))
    elif facing == "left":
        d.point((ox+6,3), fill=(20,12,8,255))
    elif facing == "right":
        d.point((ox+10,3), fill=(20,12,8,255))

save(img, "npc_street_vendor.png")

# ══════════════════════════════════════
# 4. 피지 경찰 (흰 제복 + 경찰 모자)
#    특징: 군청 모자, 흰 셔츠, 남색 바지, 허리띠
# ══════════════════════════════════════
img, d = new_sheet()
SKIN   = (155, 112, 72, 255)
SHIRT  = (235, 232, 225, 255)
PANTS  = (42, 52, 92, 255)
BELT   = (38, 28, 18, 255)
CAP    = (35, 45, 85, 255)
CAP_B  = (28, 35, 68, 255)
CAP_V  = (235, 215, 80, 255)  # 경찰 모자 앞 장식
SHOE   = (28, 22, 15, 255)

for i, facing in enumerate(["down","left","right","up"]):
    ox = i * 16
    d.ellipse([ox+4,14,ox+12,16], fill=(0,0,0,55))

    # 다리
    d.rectangle([ox+5,10,ox+7,14], fill=PANTS)
    d.rectangle([ox+9,10,ox+11,14], fill=PANTS)
    d.rectangle([ox+4,13,ox+8,15], fill=SHOE)
    d.rectangle([ox+9,13,ox+12,15], fill=SHOE)

    # 몸통
    d.rectangle([ox+5,6,ox+11,10], fill=SHIRT)
    # 허리띠
    d.rectangle([ox+5,9,ox+11,10], fill=BELT)
    # 셔츠 단추선
    d.line([ox+8,6,ox+8,9], fill=(200,198,190,255))

    # 팔 (곧게)
    if facing == "left":
        d.rectangle([ox+3,7,ox+5,10], fill=SHIRT)
        d.rectangle([ox+3,10,ox+4,11], fill=SKIN)
        d.rectangle([ox+11,7,ox+12,9], fill=SHIRT)
    elif facing == "right":
        d.rectangle([ox+4,7,ox+5,9], fill=SHIRT)
        d.rectangle([ox+11,7,ox+13,10], fill=SHIRT)
        d.rectangle([ox+12,10,ox+13,11], fill=SKIN)
    else:
        d.rectangle([ox+3,7,ox+5,10], fill=SHIRT)
        d.rectangle([ox+3,10,ox+4,11], fill=SKIN)
        d.rectangle([ox+11,7,ox+13,10], fill=SHIRT)
        d.rectangle([ox+12,10,ox+13,11], fill=SKIN)

    # 목
    d.rectangle([ox+7,4,ox+9,7], fill=SKIN)

    # 머리
    d.rectangle([ox+5,2,ox+11,5], fill=SKIN)

    # 경찰 모자
    d.rectangle([ox+4,0,ox+12,2], fill=CAP)   # 챙
    d.rectangle([ox+5,0,ox+11,1], fill=CAP_B)
    d.ellipse([ox+5,0,ox+11,3], fill=CAP)
    d.line([ox+4,2,ox+12,2], fill=CAP_B, width=1)
    # 모자 앞 배지
    if facing in ["down","left","right"]:
        d.rectangle([ox+7,1,ox+9,2], fill=CAP_V)

    # 얼굴
    if facing == "down":
        d.point((ox+7,3), fill=(20,12,8,255))
        d.point((ox+9,3), fill=(20,12,8,255))
        d.line([ox+7,4,ox+9,4], fill=(155,85,65,255))
    elif facing == "left":
        d.point((ox+6,3), fill=(20,12,8,255))
    elif facing == "right":
        d.point((ox+10,3), fill=(20,12,8,255))

save(img, "npc_police.png")

# ══════════════════════════════════════
# 5. 피지 여성 B (초록 드레스 + 꽃 머리핀)
#    특징: 긴 머리 + 꽃장식, 밝은 드레스
# ══════════════════════════════════════
img, d = new_sheet()
SKIN  = (148, 102, 62, 255)
DRESS = (85, 168, 88, 255)
DRESS2= (62, 138, 65, 255)
HAIR  = (20, 12, 8, 255)
FLOWER= (228, 72, 105, 255)   # 머리 꽃
SHOE  = (115, 62, 38, 255)

for i, facing in enumerate(["down","left","right","up"]):
    ox = i * 16
    d.ellipse([ox+4,14,ox+12,16], fill=(0,0,0,55))

    # 치마 (플레어)
    d.polygon([ox+4,9, ox+2,14, ox+14,14, ox+12,9], fill=DRESS2)
    d.rectangle([ox+5,13,ox+7,15], fill=SHOE)
    d.rectangle([ox+9,13,ox+11,15], fill=SHOE)

    # 몸통
    d.rectangle([ox+5,5,ox+11,10], fill=DRESS)

    # 팔
    if facing == "left":
        d.rectangle([ox+3,6,ox+5,9], fill=SKIN)
        d.rectangle([ox+11,6,ox+12,8], fill=SKIN)
    elif facing == "right":
        d.rectangle([ox+4,6,ox+5,8], fill=SKIN)
        d.rectangle([ox+11,6,ox+13,9], fill=SKIN)
    else:
        d.rectangle([ox+3,6,ox+5,9], fill=SKIN)
        d.rectangle([ox+11,6,ox+13,9], fill=SKIN)

    # 목
    d.rectangle([ox+7,3,ox+9,6], fill=SKIN)
    # 머리
    d.ellipse([ox+5,0,ox+11,5], fill=SKIN)

    # 긴 머리 + 꽃핀
    if facing == "down":
        d.rectangle([ox+4,1,ox+6,9], fill=HAIR)
        d.rectangle([ox+10,1,ox+12,9], fill=HAIR)
        d.rectangle([ox+5,0,ox+11,2], fill=HAIR)
        d.ellipse([ox+9,0,ox+12,2], fill=FLOWER)  # 꽃핀 우측
    elif facing == "left":
        d.rectangle([ox+5,0,ox+11,2], fill=HAIR)
        d.rectangle([ox+10,1,ox+12,9], fill=HAIR)
        d.ellipse([ox+10,0,ox+13,2], fill=FLOWER)
    elif facing == "right":
        d.rectangle([ox+5,0,ox+11,2], fill=HAIR)
        d.rectangle([ox+4,1,ox+6,9], fill=HAIR)
        d.ellipse([ox+4,0,ox+7,2], fill=FLOWER)
    elif facing == "up":
        d.rectangle([ox+4,1,ox+6,9], fill=HAIR)
        d.rectangle([ox+10,1,ox+12,9], fill=HAIR)
        d.rectangle([ox+5,0,ox+11,2], fill=HAIR)
        d.ellipse([ox+9,0,ox+12,2], fill=FLOWER)

    # 얼굴
    if facing == "down":
        d.point((ox+7,2), fill=(20,12,8,255))
        d.point((ox+9,2), fill=(20,12,8,255))
        d.point((ox+8,3), fill=(200,120,100,255))
    elif facing == "left":
        d.point((ox+6,2), fill=(20,12,8,255))
    elif facing == "right":
        d.point((ox+10,2), fill=(20,12,8,255))

save(img, "npc_bula_woman2.png")

# ══════════════════════════════════════
# 6. Indo-Fijian 여성 (사리)
#    특징: 밝은 피부, 사리 팔루 어깨 걸침, 긴 검은 머리 묶음
# ══════════════════════════════════════
img, d = new_sheet()
SKIN   = (210, 172, 118, 255)   # Indo-Fijian 피부톤
SARI   = (215, 68, 148, 255)    # 핑크 사리
SARI2  = (185, 45, 122, 255)    # 사리 어두운 부분
PALLU  = (235, 105, 168, 255)   # 팔루 (어깨 걸친 부분) — 밝게
BLOUSE = (225, 178, 62, 255)    # 촐리 (블라우스) — 황금색
HAIR   = (15, 8, 5, 255)
BINDI  = (200, 35, 35, 255)     # 이마 빈디 (점)
SHOE   = (125, 78, 42, 255)

for i, facing in enumerate(["down","left","right","up"]):
    ox = i * 16
    d.ellipse([ox+4,14,ox+12,16], fill=(0,0,0,55))

    # 사리 치마 (길고 흘러내리는 느낌)
    d.polygon([ox+4,8, ox+3,14, ox+13,14, ox+12,8], fill=SARI2)
    # 사리 세로 주름선
    for sx in range(ox+5, ox+12, 2):
        d.line([sx,9,sx,14], fill=SARI, width=1)
    d.rectangle([ox+5,13,ox+7,15], fill=SHOE)
    d.rectangle([ox+9,13,ox+11,15], fill=SHOE)

    # 촐리 (짧은 블라우스)
    d.rectangle([ox+5,5,ox+11,9], fill=BLOUSE)

    # 팔루 — 어깨에서 대각선으로 걸침 (사리의 핵심 실루엣)
    if facing in ["down","right"]:
        d.polygon([ox+5,5, ox+3,8, ox+5,8], fill=PALLU)   # 왼쪽 어깨
        d.polygon([ox+3,7, ox+5,5, ox+5,9, ox+3,9], fill=PALLU)
    elif facing in ["left","up"]:
        d.polygon([ox+11,5, ox+13,8, ox+11,8], fill=PALLU)  # 오른쪽 어깨
        d.polygon([ox+11,5, ox+13,7, ox+13,9, ox+11,9], fill=PALLU)

    # 팔
    if facing == "left":
        d.rectangle([ox+3,6,ox+5,9], fill=SKIN)
        d.rectangle([ox+11,6,ox+12,8], fill=PALLU)
    elif facing == "right":
        d.rectangle([ox+4,6,ox+5,8], fill=PALLU)
        d.rectangle([ox+11,6,ox+13,9], fill=SKIN)
    else:
        d.rectangle([ox+3,6,ox+5,9], fill=PALLU)
        d.rectangle([ox+11,6,ox+13,9], fill=SKIN)

    # 목
    d.rectangle([ox+7,3,ox+9,6], fill=SKIN)

    # 머리 (묶은 머리 — 뒤로 올림)
    d.ellipse([ox+5,0,ox+11,4], fill=SKIN)
    # 묶은 머리 번
    d.ellipse([ox+8,0,ox+12,3], fill=HAIR)
    d.rectangle([ox+5,0,ox+11,1], fill=HAIR)   # 가르마

    # 빈디 (이마 점)
    if facing == "down":
        d.point((ox+8,1), fill=BINDI)
    elif facing == "right":
        d.point((ox+9,1), fill=BINDI)
    elif facing == "left":
        d.point((ox+7,1), fill=BINDI)

    # 얼굴
    if facing == "down":
        d.point((ox+7,2), fill=(20,12,8,255))
        d.point((ox+9,2), fill=(20,12,8,255))
        d.point((ox+8,3), fill=(195,105,85,255))
    elif facing == "left":
        d.point((ox+6,2), fill=(20,12,8,255))
    elif facing == "right":
        d.point((ox+10,2), fill=(20,12,8,255))

save(img, "npc_hindi_woman.png")

# ══════════════════════════════════════
# 7. Indo-Fijian 남성 (흰 셔츠 + 슬랙스)
#    특징: 밝은 피부, 단정한 차림, 콧수염
# ══════════════════════════════════════
img, d = new_sheet()
SKIN   = (205, 165, 108, 255)
SHIRT  = (238, 235, 225, 255)   # 흰 셔츠
PANTS  = (58, 52, 45, 255)      # 짙은 갈색 슬랙스
MSTACH = (25, 15, 8, 255)       # 콧수염
HAIR   = (18, 10, 5, 255)
SHOE   = (38, 28, 18, 255)

for i, facing in enumerate(["down","left","right","up"]):
    ox = i * 16
    d.ellipse([ox+4,14,ox+12,16], fill=(0,0,0,55))

    # 다리 (슬랙스 — 깔끔하게)
    d.rectangle([ox+5,10,ox+7,14], fill=PANTS)
    d.rectangle([ox+9,10,ox+11,14], fill=PANTS)
    # 바지 주름선
    d.line([ox+6,10,ox+6,14], fill=(45,40,34,255))
    d.line([ox+10,10,ox+10,14], fill=(45,40,34,255))
    d.rectangle([ox+4,13,ox+8,15], fill=SHOE)
    d.rectangle([ox+9,13,ox+12,15], fill=SHOE)

    # 몸통
    d.rectangle([ox+5,6,ox+11,10], fill=SHIRT)
    # 셔츠 단추
    for by in [7,8,9]:
        d.point((ox+8,by), fill=(200,195,185,255))

    # 팔
    if facing == "left":
        d.rectangle([ox+3,7,ox+5,10], fill=SHIRT)
        d.rectangle([ox+3,10,ox+4,11], fill=SKIN)
        d.rectangle([ox+11,7,ox+12,9], fill=SHIRT)
    elif facing == "right":
        d.rectangle([ox+4,7,ox+5,9], fill=SHIRT)
        d.rectangle([ox+11,7,ox+13,10], fill=SHIRT)
        d.rectangle([ox+12,10,ox+13,11], fill=SKIN)
    else:
        d.rectangle([ox+3,7,ox+5,10], fill=SHIRT)
        d.rectangle([ox+3,10,ox+4,11], fill=SKIN)
        d.rectangle([ox+11,7,ox+13,10], fill=SHIRT)
        d.rectangle([ox+12,10,ox+13,11], fill=SKIN)

    # 목
    d.rectangle([ox+7,4,ox+9,7], fill=SKIN)
    # 머리 (짧은 검은 머리)
    d.rectangle([ox+5,1,ox+11,5], fill=SKIN)
    d.rectangle([ox+5,1,ox+11,2], fill=HAIR)
    if facing == "left":
        d.rectangle([ox+10,1,ox+11,4], fill=HAIR)
    elif facing == "right":
        d.rectangle([ox+5,1,ox+6,4], fill=HAIR)
    elif facing == "up":
        d.rectangle([ox+5,1,ox+6,3], fill=HAIR)
        d.rectangle([ox+10,1,ox+11,3], fill=HAIR)

    # 콧수염 (정면/측면)
    if facing == "down":
        d.line([ox+7,4,ox+9,4], fill=MSTACH)
        d.point((ox+7,3), fill=(20,12,8,255))
        d.point((ox+9,3), fill=(20,12,8,255))
    elif facing == "left":
        d.point((ox+6,4), fill=MSTACH)
        d.point((ox+6,3), fill=(20,12,8,255))
    elif facing == "right":
        d.point((ox+10,4), fill=MSTACH)
        d.point((ox+10,3), fill=(20,12,8,255))

save(img, "npc_hindi_man.png")

# ══════════════════════════════════════
# 8. Wati — iTaukei 피지 여성, 사무직원
#    특징: 흰 블라우스 + 짙은 네이비 sulu jupe, 묶은 머리
# ══════════════════════════════════════
img, d = new_sheet()
SKIN   = (155, 110, 68, 255)
BLOUSE = (238, 235, 228, 255)   # 흰 블라우스
SULU   = (42, 48, 82, 255)      # 짙은 네이비 sulu jupe
HAIR   = (18, 10, 6, 255)
SHOE   = (35, 28, 20, 255)

for i, facing in enumerate(["down","left","right","up"]):
    ox = i * 16
    d.ellipse([ox+4,14,ox+12,16], fill=(0,0,0,55))

    # sulu jupe (무릎 아래 길이 — 여성 사무용 치마)
    d.polygon([ox+4,9, ox+3,14, ox+13,14, ox+12,9], fill=SULU)
    # 치마 주름 라인
    for sx in range(ox+5, ox+12, 2):
        d.line([sx,10,sx,14], fill=(55,62,100,255), width=1)
    # 신발
    d.rectangle([ox+5,13,ox+7,15], fill=SHOE)
    d.rectangle([ox+9,13,ox+11,15], fill=SHOE)

    # 몸통 (흰 블라우스)
    d.rectangle([ox+5,5,ox+11,10], fill=BLOUSE)
    # 블라우스 단추선
    d.line([ox+8,5,ox+8,9], fill=(210,208,200,255))
    # 블라우스 칼라
    if facing == "down":
        d.polygon([ox+7,5, ox+8,6, ox+9,5], fill=(220,218,210,255))

    # 팔
    if facing == "left":
        d.rectangle([ox+3,6,ox+5,9], fill=BLOUSE)
        d.rectangle([ox+3,9,ox+4,10], fill=SKIN)
        d.rectangle([ox+11,6,ox+12,8], fill=BLOUSE)
    elif facing == "right":
        d.rectangle([ox+4,6,ox+5,8], fill=BLOUSE)
        d.rectangle([ox+11,6,ox+13,9], fill=BLOUSE)
        d.rectangle([ox+12,9,ox+13,10], fill=SKIN)
    else:
        d.rectangle([ox+3,6,ox+5,9], fill=BLOUSE)
        d.rectangle([ox+3,9,ox+4,10], fill=SKIN)
        d.rectangle([ox+11,6,ox+13,9], fill=BLOUSE)
        d.rectangle([ox+12,9,ox+13,10], fill=SKIN)

    # 목
    d.rectangle([ox+7,3,ox+9,6], fill=SKIN)

    # 머리 (약간 길게)
    d.ellipse([ox+5,0,ox+11,5], fill=SKIN)

    # 묶은 머리 — 뒤로 올림 (번 스타일, 약간 길게)
    if facing == "down":
        d.rectangle([ox+5,0,ox+11,1], fill=HAIR)    # 윗 머리선
        d.rectangle([ox+4,1,ox+6,6], fill=HAIR)     # 왼쪽 귀 옆 머리
        d.rectangle([ox+10,1,ox+12,6], fill=HAIR)   # 오른쪽 귀 옆 머리
        d.ellipse([ox+7,0,ox+11,2], fill=HAIR)      # 번 (묶은 머리)
    elif facing == "left":
        d.rectangle([ox+5,0,ox+11,1], fill=HAIR)
        d.rectangle([ox+10,1,ox+12,6], fill=HAIR)   # 앞에서 보이는 머리
        d.ellipse([ox+9,0,ox+13,3], fill=HAIR)      # 번 (왼쪽 방향 — 오른쪽에)
    elif facing == "right":
        d.rectangle([ox+5,0,ox+11,1], fill=HAIR)
        d.rectangle([ox+4,1,ox+6,6], fill=HAIR)
        d.ellipse([ox+3,0,ox+7,3], fill=HAIR)       # 번 (오른쪽 방향 — 왼쪽에)
    elif facing == "up":
        d.rectangle([ox+4,1,ox+6,6], fill=HAIR)
        d.rectangle([ox+10,1,ox+12,6], fill=HAIR)
        d.rectangle([ox+5,0,ox+11,2], fill=HAIR)
        d.ellipse([ox+6,0,ox+10,3], fill=HAIR)      # 번 (뒷면 — 정중앙)

    # 얼굴
    if facing == "down":
        d.point((ox+7,2), fill=(20,12,8,255))
        d.point((ox+9,2), fill=(20,12,8,255))
        d.point((ox+8,3), fill=(185,105,82,255))    # 입술
    elif facing == "left":
        d.point((ox+6,2), fill=(20,12,8,255))
    elif facing == "right":
        d.point((ox+10,2), fill=(20,12,8,255))

save(img, "npc_wati.png")
