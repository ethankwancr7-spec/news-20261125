"""Draw the 1024×1024 front page. Run locally; the grader only copies the PNG."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import stories

ROOT = Path(__file__).resolve().parent
ENTRY = ROOT / "assets" / "entry.png"
FONTS = Path(r"C:\Windows\Fonts")

W = H = 1024
MARGIN = 32
PAPER = "#F4EFE6"
INK = "#1B1B1B"
RULE = "#CFC6B8"


def face(filename: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONTS / filename), size)


def ink_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> int:
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0]


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = word if not current else f"{current} {word}"
        if ink_width(draw, trial, font) <= max_w:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def tone(hex_color: str, factor: float) -> tuple[int, int, int]:
    red, green, blue = bytes.fromhex(hex_color[1:])
    return tuple(max(0, min(255, int(channel * factor))) for channel in (red, green, blue))


def draw_chip(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    pin = "#D5E0DA"
    for index in range(3):
        pin_y = y + 5 + index * 7
        draw.rectangle((x, pin_y, x + 5, pin_y + 3), fill=pin)
        draw.rectangle((x + 23, pin_y, x + 28, pin_y + 3), fill=pin)
    draw.rounded_rectangle((x + 5, y + 2, x + 23, y + 24), radius=2, fill="#1C4A40", outline="#B7D4C8", width=1)
    draw.rectangle((x + 9, y + 7, x + 19, y + 19), fill="#2E7A68")
    axle = x + 31
    draw.line((axle, y + 6, axle, y + 16), fill="#F05448", width=2)
    draw.polygon([(axle - 5, y + 14), (axle + 5, y + 14), (axle, y + 22)], fill="#F05448")


def draw_lead_art(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    left, top, right, bottom = box
    draw.text((left, top), "NASDAQ −4%", font=face("arialbd.ttf", 14), fill="#F6C9C4")

    wall_top = bottom - 98
    banner_font = face("arialbd.ttf", 15)
    banner_text = "NEW US TARIFFS 15–35%"
    banner_w = ink_width(draw, banner_text, banner_font) + 28
    banner_h = 26
    banner_bottom = wall_top - 4
    banner_top = banner_bottom - banner_h
    banner_left = left + ((right - left) - banner_w) // 2
    chart_box = (left, top + 20, right - 48, banner_top - 8)

    grid = "#3A4E66"
    chart_l, chart_t, chart_r, chart_b = chart_box
    for step in range(1, 4):
        y = chart_t + (chart_b - chart_t) * step // 4
        draw.line([(chart_l, y), (chart_r, y)], fill=grid, width=1)
    for step in range(1, 5):
        x = chart_l + (chart_r - chart_l) * step // 5
        draw.line([(x, chart_t), (x, chart_b)], fill=grid, width=1)

    fracs = (0.12, 0.08, 0.18, 0.14, 0.26, 0.30, 0.38, 0.46, 0.72, 0.98)
    span = chart_r - chart_l
    height = chart_b - chart_t
    points = []
    for index, frac in enumerate(fracs):
        x = chart_l + round(span * index / (len(fracs) - 1))
        y = chart_t + round(height * frac)
        points.append((x, y))
    draw.line(points, fill="#F05448", width=3, joint="curve")
    end_x, end_y = points[-1]

    labels = (
        ("CHINA", "#C2453A"),
        ("EU", "#3A6FBF"),
        ("JAPAN", "#4A6494"),
        ("INDIA", "#C46822"),
        ("KOREA", "#1E8A80"),
        ("TAIWAN", "#2F8A52"),
        ("VIETNAM", "#8A6428"),
        ("SINGAPORE", "#8E4A78"),
    )
    columns, rows = 4, 2
    gap = 6
    cell_w = (right - left - gap * (columns - 1)) // columns
    cell_h = (bottom - wall_top - gap * (rows - 1)) // rows
    label_font = face("arialbd.ttf", 13)
    for index, (name, color) in enumerate(labels):
        col, row = index % columns, index // columns
        x = left + col * (cell_w + gap)
        y = wall_top + row * (cell_h + gap)
        draw.rectangle((x, y, x + cell_w, y + cell_h), fill=color)
        rib = tone(color, 0.72)
        for rib_index in range(1, 4):
            rib_x = x + cell_w * rib_index // 4
            draw.line([(rib_x, y + 4), (rib_x, y + cell_h - 4)], fill=rib, width=2)
        cap = tone(color, 0.55)
        draw.rectangle((x, y + cell_h - 4, x + cell_w, y + cell_h), fill=cap)
        for corner in ((x, y), (x + cell_w - 5, y), (x, y + cell_h - 5), (x + cell_w - 5, y + cell_h - 5)):
            draw.rectangle((corner[0], corner[1], corner[0] + 5, corner[1] + 5), fill=cap)
        text_w = ink_width(draw, name, label_font)
        text_box = draw.textbbox((0, 0), name, font=label_font)
        text_h = text_box[3] - text_box[1]
        draw.text(
            (x + (cell_w - text_w) / 2, y + (cell_h - text_h) / 2 - text_box[1]),
            name,
            font=label_font,
            fill="#FFFFFF",
        )

    draw.rectangle((banner_left, banner_top, banner_left + banner_w, banner_bottom), fill="#F3E6C4")
    text_box = draw.textbbox((0, 0), banner_text, font=banner_font)
    draw.text(
        (
            banner_left + 14,
            banner_top + (banner_h - (text_box[3] - text_box[1])) / 2 - text_box[1],
        ),
        banner_text,
        font=banner_font,
        fill=INK,
    )
    draw_chip(draw, end_x + 10, end_y - 26)
    draw.ellipse((end_x - 4, end_y - 4, end_x + 4, end_y + 4), fill="#F05448")


def draw_lead_copy(draw: ImageDraw.ImageDraw, left: int, top: int, right: int, bottom: int) -> None:
    width = right - left
    draw.text((left, top), stories.LEAD["tag"], font=face("arialbd.ttf", 13), fill="#E6C98A")
    y = top + 18

    headline_size = 34
    headline = stories.LEAD["headline"]
    headline_font = face("georgiab.ttf", headline_size)
    lines = wrap_text(draw, headline, headline_font, width)
    while len(lines) > 2 and headline_size > 22:
        headline_size -= 1
        headline_font = face("georgiab.ttf", headline_size)
        lines = wrap_text(draw, headline, headline_font, width)
    for line in lines:
        draw.text((left, y), line, font=headline_font, fill="#F6F1E7")
        y += headline_size + 2
    y += 8

    bullet_size = 17
    bullet_font = face("georgia.ttf", bullet_size)
    blocks = [wrap_text(draw, bullet, bullet_font, width - 16) for bullet in stories.LEAD["bullets"]]
    while bullet_size > 13:
        line_h = bullet_size + 3
        needed = sum(len(block) * line_h for block in blocks) + 5 * (len(blocks) - 1)
        if y + needed <= bottom:
            break
        bullet_size -= 1
        bullet_font = face("georgia.ttf", bullet_size)
        blocks = [wrap_text(draw, bullet, bullet_font, width - 16) for bullet in stories.LEAD["bullets"]]
    line_h = bullet_size + 3
    for block in blocks:
        for index, line in enumerate(block):
            if index == 0:
                draw.ellipse((left, y + 6, left + 6, y + 12), fill="#F05448")
            draw.text((left + 14, y), line, font=bullet_font, fill="#E7E0D4")
            y += line_h
        y += 5


def draw_lead(draw: ImageDraw.ImageDraw) -> None:
    x0, y0, x1, y1 = MARGIN, 104, W - MARGIN, 372
    draw.rectangle((x0, y0, x1, y1), fill="#1E2A3A")
    split = x0 + int((x1 - x0) * 0.56)
    draw_lead_art(draw, (x0 + 12, y0 + 12, split - 12, y1 - 12))
    draw_lead_copy(draw, split + 8, y0 + 14, x1 - 10, y1 - 12)


def draw_masthead(draw: ImageDraw.ImageDraw) -> None:
    title_font = face("georgiab.ttf", 44)
    meta_font = face("georgia.ttf", 16)
    title = "THE WORLD IN ONE PAGE"
    title_w = ink_width(draw, title, title_font)
    draw.text(((W - title_w) / 2, 12), title, font=title_font, fill=INK)

    meta_y = 64
    draw.text((MARGIN, meta_y), stories.DATE_LINE, font=meta_font, fill=INK)
    strap = stories.strapline()
    strap_w = ink_width(draw, strap, meta_font)
    draw.text((W - MARGIN - strap_w, meta_y), strap, font=meta_font, fill=INK)

    rule_y = 90
    draw.line([(MARGIN, rule_y), (W - MARGIN, rule_y)], fill=INK, width=2)
    draw.line([(MARGIN, rule_y + 4), (W - MARGIN, rule_y + 4)], fill=INK, width=1)


def continent_color(name: str) -> str:
    for region in stories.REGIONS:
        if region["continent"] == name:
            return region["color"]
    return INK


def draw_tanker(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    draw.polygon([(x + 1, y + 16), (x + 6, y + 25), (x + 30, y + 25), (x + 24, y + 16)], fill="#1A4558")
    draw.rectangle((x + 4, y + 13, x + 25, y + 17), fill="#3E7F99")
    draw.rectangle((x + 6, y + 8, x + 13, y + 14), fill="#D5DEE4")
    draw.rectangle((x + 18, y + 6, x + 24, y + 14), fill="#EEF2F4")
    draw.polygon([(x + 8, y + 8), (x + 11, y + 0), (x + 14, y + 8)], fill="#E4533A")
    draw.polygon([(x + 9, y + 8), (x + 11, y + 3), (x + 13, y + 8)], fill="#F6C14A")


def draw_refinery(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    draw.rectangle((x + 7, y + 11, x + 15, y + 26), fill="#4E585F")
    draw.polygon([(x + 6, y + 11), (x + 11, y + 5), (x + 16, y + 11)], fill="#333B40")
    draw.rectangle((x + 7, y + 16, x + 15, y + 18), fill="#D5DDE2")
    draw.rectangle((x + 4, y + 25, x + 20, y + 28), fill="#2E363B")
    draw.polygon([(x + 9, y + 5), (x + 11, y + 0), (x + 13, y + 5)], fill="#E4533A")
    draw.polygon([(x + 10, y + 5), (x + 11, y + 2), (x + 12, y + 5)], fill="#F6C14A")
    draw.line([(x + 17, y + 8), (x + 29, y + 8)], fill=INK, width=1)
    draw.ellipse((x + 20, y + 6, x + 26, y + 11), fill="#2B5FA8")
    draw.line([(x + 17, y + 6), (x + 20, y + 6)], fill=INK, width=2)
    draw.line([(x + 26, y + 6), (x + 29, y + 6)], fill=INK, width=2)


def draw_tiles(draw: ImageDraw.ImageDraw) -> None:
    y0, y1 = 382, 520
    gap = 12
    tile_w = (W - 2 * MARGIN - 2 * gap) // 3
    for index, tile in enumerate(stories.TILES):
        x = MARGIN + index * (tile_w + gap)
        accent = continent_color(tile["continent"])
        draw.rectangle((x, y0, x + tile_w, y1), fill="#FFFCF7", outline=RULE)
        draw.rectangle((x + 1, y0 + 1, x + tile_w - 1, y0 + 5), fill=accent)

        pad = 8
        icon_x, icon_y = x + pad, y0 + 12
        if tile["icon"] == "tanker":
            draw_tanker(draw, icon_x, icon_y)
            icon_w, icon_h = 32, 26
        elif tile["icon"] == "refinery":
            draw_refinery(draw, icon_x, icon_y)
            icon_w, icon_h = 30, 28
        else:
            draw_chip(draw, icon_x, icon_y)
            icon_w, icon_h = 36, 26

        tag_font = face("arialbd.ttf", 13)
        tag_box = draw.textbbox((0, 0), tile["tag"], font=tag_font)
        tag_h = tag_box[3] - tag_box[1]
        draw.text(
            (icon_x + icon_w + 6, icon_y + (icon_h - tag_h) / 2 - tag_box[1]),
            tile["tag"],
            font=tag_font,
            fill=accent,
        )

        text_w = tile_w - 2 * pad
        head_font = face("georgiab.ttf", 22)
        lines = wrap_text(draw, tile["headline"], head_font, text_w)
        if len(lines) > 2:
            head_font = face("georgiab.ttf", 20)
            lines = wrap_text(draw, tile["headline"], head_font, text_w)
        cursor = icon_y + icon_h + 6
        headline_bottom = cursor
        for line in lines:
            draw.text((x + pad, cursor), line, font=head_font, fill=INK)
            headline_bottom = draw.textbbox((x + pad, cursor), line, font=head_font)[3]
            cursor = headline_bottom + 1

        deck_font = face("calibri.ttf", 15)
        deck_lines = wrap_text(draw, tile["deck"], deck_font, text_w)
        if len(deck_lines) > 2:
            deck_font = face("calibri.ttf", 14)
            deck_lines = wrap_text(draw, tile["deck"], deck_font, text_w)
        deck_y = headline_bottom + 8
        for line in deck_lines:
            draw.text((x + pad, deck_y), line, font=deck_font, fill="#333333")
            deck_y = draw.textbbox((x + pad, deck_y), line, font=deck_font)[3] + 2


def item_tokens(lead: str, text: str) -> list[tuple[str, str]]:
    return [("b", word) for word in lead.split()] + [("r", word) for word in text.split()]


def region_fonts() -> tuple[ImageFont.FreeTypeFont, ImageFont.FreeTypeFont]:
    return face("segoeuib.ttf", 14), face("segoeui.ttf", 14)


def layout_item(draw: ImageDraw.ImageDraw, lead: str, text: str, max_w: int) -> int:
    bold, regular = region_fonts()
    lines = 1
    cursor = 0
    for kind, word in item_tokens(lead, text):
        font = bold if kind == "b" else regular
        word_w = ink_width(draw, word, font)
        space = 0 if cursor == 0 else ink_width(draw, " ", font)
        if cursor and cursor + space + word_w > max_w:
            lines += 1
            cursor = word_w
        else:
            cursor += space + word_w
    return lines


def draw_item(draw: ImageDraw.ImageDraw, lead: str, text: str, x: int, y: int, max_w: int) -> None:
    bold, regular = region_fonts()
    cursor_x = x
    cursor_y = y
    for kind, word in item_tokens(lead, text):
        font = bold if kind == "b" else regular
        word_w = ink_width(draw, word, font)
        space = 0 if cursor_x == x else ink_width(draw, " ", font)
        if cursor_x != x and cursor_x + space + word_w > x + max_w:
            cursor_x = x
            cursor_y += round(14 * 1.2)
            space = 0
        cursor_x += space
        draw.text((cursor_x, cursor_y), word, font=font, fill="#333333")
        cursor_x += word_w


def draw_regions(draw: ImageDraw.ImageDraw) -> None:
    gap_x, gap_y = 8, 12
    row_h = (996 - 530 - gap_y) // 2
    col_w = (W - 2 * MARGIN - 3 * gap_x) // 4
    text_inset = 12
    max_w = col_w - text_inset - 2
    header_font = face("arialbd.ttf", 13)
    for index, region in enumerate(stories.REGIONS):
        col, row = index % 4, index // 4
        x = MARGIN + col * (col_w + gap_x)
        y = 530 + row * (row_h + gap_y)
        draw.rectangle((x, y, x + col_w, y + 24), fill=region["color"])
        count = str(len(region["items"]))
        name_box = draw.textbbox((0, 0), region["name"], font=header_font)
        count_w = ink_width(draw, count, header_font)
        name_h = name_box[3] - name_box[1]
        header_y = y + (24 - name_h) / 2 - name_box[1]
        draw.text((x + 8, header_y), region["name"], font=header_font, fill="#FFFFFF")
        draw.text((x + col_w - 8 - count_w, header_y), count, font=header_font, fill="#FFFFFF")

        pitch = round(14 * 1.2)
        cursor = y + 24 + 8
        for item in region["items"]:
            draw.ellipse((x + 3, cursor + 8, x + 9, cursor + 14), fill=region["color"])
            draw_item(draw, item["lead"], item["text"], x + text_inset, cursor, max_w)
            cursor += layout_item(draw, item["lead"], item["text"], max_w) * pitch + 10


def draw_footer(draw: ImageDraw.ImageDraw) -> None:
    footer_font = face("calibri.ttf", 12)
    box = draw.textbbox((0, 0), stories.FOOTER, font=footer_font)
    text_h = box[3] - box[1]
    draw.text((MARGIN, 1000 + (24 - text_h) / 2 - box[1]), stories.FOOTER, font=footer_font, fill="#8A8175")


def render(path: Path = ENTRY) -> Path:
    image = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(image)
    draw_masthead(draw)
    draw_lead(draw)
    draw_tiles(draw)
    draw_regions(draw)
    draw_footer(draw)
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, format="PNG")
    return path


if __name__ == "__main__":
    print(render())
