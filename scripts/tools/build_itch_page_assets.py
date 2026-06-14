#!/usr/bin/env python3
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs" / "itch-page-assets"
FONT = ROOT / "assets" / "fonts" / "NanumGothic-Regular.ttf"

BG = ROOT / "assets" / "sprites" / "tilesets"
CH = ROOT / "assets" / "sprites" / "characters"
OBJ = ROOT / "assets" / "sprites" / "objects"

SCREEN_W, SCREEN_H = 1280, 720
BASE_W, BASE_H = 320, 180
SCALE = 4


def font(size):
    return ImageFont.truetype(str(FONT), size=size)


def img(path):
    return Image.open(path).convert("RGBA")


def sprite(name, frame=0):
    sheet = img(CH / name)
    return sheet.crop((frame * 16, 0, frame * 16 + 16, 16))


def draw_label(draw, x, y, text):
    f = font(18)
    bbox = draw.textbbox((0, 0), text, font=f)
    w = bbox[2] - bbox[0]
    draw.rounded_rectangle((x - w / 2 - 8, y - 28, x + w / 2 + 8, y - 4), radius=8, fill=(24, 22, 18, 185))
    draw.text((x - w / 2, y - 27), text, fill=(255, 244, 201, 255), font=f)


def render_scene(background, actors, objects=(), dialogue=None, caption=None, filename="scene.png"):
    base = img(BG / background)
    for item in objects:
        tex = img(OBJ / item["file"])
        if "scale" in item:
            tex = tex.resize((tex.width * item["scale"], tex.height * item["scale"]), Image.Resampling.NEAREST)
        x, y = item["pos"]
        base.alpha_composite(tex, (int(x - tex.width / 2), int(y - tex.height / 2)))

    for actor in sorted(actors, key=lambda a: a["pos"][1]):
        tex = sprite(actor["file"], actor.get("frame", 0))
        x, y = actor["pos"]
        base.alpha_composite(tex, (int(x - 8), int(y - 8)))

    shot = base.resize((SCREEN_W, SCREEN_H), Image.Resampling.NEAREST)
    draw = ImageDraw.Draw(shot, "RGBA")

    for actor in actors:
        if actor.get("label"):
            x, y = actor["pos"]
            draw_label(draw, x * SCALE, y * SCALE - 30, actor["label"])

    if caption:
        f = font(24)
        draw.rounded_rectangle((32, 28, 32 + draw.textlength(caption, font=f) + 32, 74), radius=12, fill=(10, 16, 22, 175))
        draw.text((48, 36), caption, fill=(235, 242, 236, 255), font=f)

    if dialogue:
        speaker = dialogue.get("speaker", "")
        text = dialogue["text"]
        draw.rounded_rectangle((32, 500, 1248, 688), radius=12, fill=(20, 18, 16, 220), outline=(245, 218, 155, 150), width=2)
        if speaker:
            sf = font(28)
            draw.text((56, 522), speaker, fill=(255, 221, 128, 255), font=sf)
            text_y = 566
        else:
            text_y = 538
        tf = font(30)
        wrapped = wrap_text(draw, text, tf, 1120)
        for line in wrapped[:3]:
            draw.text((56, text_y), line, fill=(244, 244, 238, 255), font=tf)
            text_y += 42

    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / filename
    shot.save(path)
    return path


def wrap_text(draw, text, f, max_w):
    words = text.split()
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else f"{cur} {word}"
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def make_cover():
    bg = img(BG / "naitamba_bg.png")
    cover = bg.resize((889, 500), Image.Resampling.NEAREST).crop((130, 0, 760, 500))
    overlay = Image.new("RGBA", cover.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay, "RGBA")
    od.rectangle((0, 0, 630, 500), fill=(8, 16, 22, 90))
    od.rectangle((0, 300, 630, 500), fill=(7, 10, 12, 130))
    cover.alpha_composite(overlay)

    def paste_sprite(name, x, y, scale=5, frame=0):
        tex = sprite(name, frame).resize((16 * scale, 16 * scale), Image.Resampling.NEAREST)
        cover.alpha_composite(tex, (x - tex.width // 2, y - tex.height // 2))

    tank = img(OBJ / "water_tank.png").resize((128, 96), Image.Resampling.NEAREST)
    cover.alpha_composite(tank, (252, 255))
    paste_sprite("ratu_josefa.png", 178, 338, 5)
    paste_sprite("lani.png", 244, 356, 5)
    paste_sprite("mere.png", 390, 356, 5)
    paste_sprite("timoci.png", 452, 346, 5)
    paste_sprite("player.png", 316, 382, 5)

    draw = ImageDraw.Draw(cover, "RGBA")
    title_font = font(72)
    sub_font = font(26)
    tag_font = font(20)
    draw.text((38, 38), "AID WORLD", fill=(255, 245, 207, 255), font=title_font, stroke_width=3, stroke_fill=(24, 26, 28, 220))
    draw.text((44, 124), "Naitamba Island Story", fill=(236, 247, 241, 255), font=sub_font, stroke_width=2, stroke_fill=(20, 24, 28, 210))
    draw.rounded_rectangle((42, 410, 588, 458), radius=14, fill=(17, 31, 34, 210), outline=(247, 213, 129, 170), width=2)
    draw.text((66, 421), "A negotiation game about trust, water, and community", fill=(245, 239, 221, 255), font=tag_font)

    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "cover.png"
    cover.save(path)
    return path


def make_cover_ko():
    bg = img(BG / "naitamba_bg.png")
    cover = bg.resize((889, 500), Image.Resampling.NEAREST).crop((130, 0, 760, 500))
    overlay = Image.new("RGBA", cover.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay, "RGBA")
    od.rectangle((0, 0, 630, 500), fill=(8, 16, 22, 90))
    od.rectangle((0, 300, 630, 500), fill=(7, 10, 12, 130))
    cover.alpha_composite(overlay)

    def paste_sprite(name, x, y, scale=5, frame=0):
        tex = sprite(name, frame).resize((16 * scale, 16 * scale), Image.Resampling.NEAREST)
        cover.alpha_composite(tex, (x - tex.width // 2, y - tex.height // 2))

    tank = img(OBJ / "water_tank.png").resize((128, 96), Image.Resampling.NEAREST)
    cover.alpha_composite(tank, (252, 255))
    paste_sprite("ratu_josefa.png", 178, 338, 5)
    paste_sprite("lani.png", 244, 356, 5)
    paste_sprite("mere.png", 390, 356, 5)
    paste_sprite("timoci.png", 452, 346, 5)
    paste_sprite("player.png", 316, 382, 5)

    draw = ImageDraw.Draw(cover, "RGBA")
    title_font = font(68)
    sub_font = font(28)
    tag_font = font(20)
    draw.text((38, 40), "Aid World", fill=(255, 245, 207, 255), font=title_font, stroke_width=3, stroke_fill=(24, 26, 28, 220))
    draw.text((44, 126), "나이탬바 섬 이야기", fill=(236, 247, 241, 255), font=sub_font, stroke_width=2, stroke_fill=(20, 24, 28, 210))
    draw.rounded_rectangle((42, 410, 588, 458), radius=14, fill=(17, 31, 34, 210), outline=(247, 213, 129, 170), width=2)
    draw.text((74, 421), "신뢰, 물, 공동체를 둘러싼 협상 게임", fill=(245, 239, 221, 255), font=tag_font)

    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "cover-ko.png"
    cover.save(path)
    return path


def main():
    paths = [
        make_cover(),
        make_cover_ko(),
        render_scene(
            "office_bg.png",
            [
                {"file": "npc_wati.png", "pos": (80, 85), "label": "Wati"},
                {"file": "mere.png", "pos": (160, 62), "label": "Mere"},
                {"file": "player.png", "pos": (160, 110)},
            ],
            objects=[
                {"file": "file_icon.png", "pos": (220, 90), "scale": 1},
                {"file": "computer_icon.png", "pos": (240, 90), "scale": 1},
            ],
            dialogue={"speaker": "Mere", "text": "This project is not paperwork. It's people, and it's vanua."},
            caption="KODA Fiji Office",
            filename="screenshot-01-office.png",
        ),
        render_scene(
            "office_bg.png",
            [
                {"file": "npc_wati.png", "pos": (80, 85), "label": "Wati"},
                {"file": "mere.png", "pos": (160, 62), "label": "Mere"},
                {"file": "player.png", "pos": (160, 110)},
            ],
            objects=[
                {"file": "file_icon.png", "pos": (220, 90), "scale": 1},
                {"file": "computer_icon.png", "pos": (240, 90), "scale": 1},
            ],
            dialogue={"speaker": "Mere", "text": "이 사업은 서류가 아니라 사람, 그리고 vanua예요."},
            caption="KODA 피지 사무소",
            filename="screenshot-01-office-ko.png",
        ),
        render_scene(
            "suva_street_bg.png",
            [
                {"file": "player.png", "pos": (40, 110)},
                {"file": "npc_bula_man.png", "pos": (85, 82)},
                {"file": "npc_street_vendor.png", "pos": (145, 82), "label": "Vendor"},
                {"file": "npc_hindi_woman.png", "pos": (135, 88)},
                {"file": "npc_hindi_man.png", "pos": (60, 135)},
                {"file": "npc_police.png", "pos": (180, 130)},
                {"file": "npc_bula_woman2.png", "pos": (230, 125)},
            ],
            dialogue={"speaker": "Vendor", "text": "Bula vinaka, bro! Visiting a village? Then respect the vanua with a proper gift."},
            caption="Suva Street",
            filename="screenshot-02-suva-street.png",
        ),
        render_scene(
            "suva_street_bg.png",
            [
                {"file": "player.png", "pos": (40, 110)},
                {"file": "npc_bula_man.png", "pos": (85, 82)},
                {"file": "npc_street_vendor.png", "pos": (145, 82), "label": "상인"},
                {"file": "npc_hindi_woman.png", "pos": (135, 88)},
                {"file": "npc_hindi_man.png", "pos": (60, 135)},
                {"file": "npc_police.png", "pos": (180, 130)},
                {"file": "npc_bula_woman2.png", "pos": (230, 125)},
            ],
            dialogue={"speaker": "상인", "text": "Bula vinaka, bro! 마을에 들어가요? 그 vanua에 맞는 선물 챙겨야죠."},
            caption="수바 거리",
            filename="screenshot-02-suva-street-ko.png",
        ),
        render_scene(
            "government_bg.png",
            [
                {"file": "npc_bula_woman.png", "pos": (80, 90), "label": "Reception"},
                {"file": "timoci.png", "pos": (160, 55), "label": "Vikash"},
                {"file": "player.png", "pos": (160, 130)},
            ],
            dialogue={"speaker": "Vikash", "text": "Namaste. The land consent paper trail must be settled before approval."},
            caption="Ministry of National Planning",
            filename="screenshot-03-government.png",
        ),
        render_scene(
            "government_bg.png",
            [
                {"file": "npc_bula_woman.png", "pos": (80, 90), "label": "접수처"},
                {"file": "timoci.png", "pos": (160, 55), "label": "Vikash"},
                {"file": "player.png", "pos": (160, 130)},
            ],
            dialogue={"speaker": "Vikash", "text": "Namaste. 토지 동의 서류 흐름이 정리돼야 승인 절차가 진행됩니다."},
            caption="국가계획부",
            filename="screenshot-03-government-ko.png",
        ),
        render_scene(
            "naitamba_bg.png",
            [
                {"file": "npc_island_child.png", "pos": (55, 125)},
                {"file": "lani.png", "pos": (80, 112), "label": "Lani"},
                {"file": "npc_island_woman.png", "pos": (120, 108)},
                {"file": "ratu_josefa.png", "pos": (160, 112), "label": "Ratu Josefa"},
                {"file": "npc_island_fisher.png", "pos": (180, 130)},
                {"file": "npc_island_elder.png", "pos": (210, 115)},
                {"file": "mere.png", "pos": (235, 95), "label": "Mere"},
                {"file": "player.png", "pos": (160, 130)},
            ],
            dialogue={"speaker": "Ratu Josefa", "text": "There are things our vanua remembers. The promise ten years ago. Nothing remained."},
            caption="Naitamba Island",
            filename="screenshot-04-naitamba.png",
        ),
        render_scene(
            "naitamba_bg.png",
            [
                {"file": "npc_island_child.png", "pos": (55, 125)},
                {"file": "lani.png", "pos": (80, 112), "label": "Lani"},
                {"file": "npc_island_woman.png", "pos": (120, 108)},
                {"file": "ratu_josefa.png", "pos": (160, 112), "label": "Ratu Josefa"},
                {"file": "npc_island_fisher.png", "pos": (180, 130)},
                {"file": "npc_island_elder.png", "pos": (210, 115)},
                {"file": "mere.png", "pos": (235, 95), "label": "Mere"},
                {"file": "player.png", "pos": (160, 130)},
            ],
            dialogue={"speaker": "Ratu Josefa", "text": "우리 vanua가 기억하는 것들이 있소. 10년 전 약속. 아무것도 남지 않았지."},
            caption="나이탬바 섬",
            filename="screenshot-04-naitamba-ko.png",
        ),
        render_scene(
            "sevusevu_bg.png",
            [
                {"file": "ratu_josefa.png", "pos": (160, 78), "label": "Ratu Josefa"},
                {"file": "lani.png", "pos": (118, 122), "label": "Lani"},
                {"file": "mere.png", "pos": (202, 124), "label": "Mere"},
                {"file": "player.png", "pos": (160, 132)},
            ],
            dialogue={"speaker": "Ratu Josefa", "text": "Come in. Let us sit together for talanoa."},
            caption="Sevusevu",
            filename="screenshot-05-sevusevu.png",
        ),
        render_scene(
            "sevusevu_bg.png",
            [
                {"file": "ratu_josefa.png", "pos": (160, 78), "label": "Ratu Josefa"},
                {"file": "lani.png", "pos": (118, 122), "label": "Lani"},
                {"file": "mere.png", "pos": (202, 124), "label": "Mere"},
                {"file": "player.png", "pos": (160, 132)},
            ],
            dialogue={"speaker": "Ratu Josefa", "text": "들어오시오. 함께 앉아 talanoa합시다."},
            caption="세부세부",
            filename="screenshot-05-sevusevu-ko.png",
        ),
    ]
    for path in paths:
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
