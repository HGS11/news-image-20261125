#!/usr/bin/env python3
"""Deterministic 1024x1024 front-page newspaper renderer for Wednesday 25 November 2026."""

import os
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1024
HEIGHT = 1024
MARGIN = 14
CONTENT_W = WIDTH - 2 * MARGIN  # 996

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
F_SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
F_SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
F_SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
F_SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

# Colour palette
BG_CREAM = (246, 240, 226)
PAPER_ALT = (252, 248, 238)
DATE_BOX_BG = (253, 243, 234)
INK = (22, 22, 26)
MUTED = (74, 70, 64)
RULE_DARK = (40, 38, 35)
RULE_LIGHT = (196, 187, 170)
RED = (176, 28, 28)
NAVY = (20, 36, 62)
NAVY_DARK = (14, 26, 46)
WHITE = (252, 250, 245)
SEA_BLUE = (205, 222, 232)
LAND_TAN = (212, 198, 168)
LAND_EDGE = (130, 118, 96)

REGION_COLORS = {
    "Europe": (44, 82, 130),
    "Middle East": (166, 68, 38),
    "Asia-Pacific": (36, 110, 92),
    "Americas": (122, 62, 128),
    "Africa": (158, 108, 30),
    "Oceania": (34, 118, 146),
    "World": (72, 78, 88),
}

TAG_COLORS = {
    "REPORTED": (36, 102, 72),
    "CLAIM": (176, 62, 28),
    "FORECAST": (46, 86, 146),
    "PENDING": (152, 100, 20),
}


def load_font(path, size):
    return ImageFont.truetype(path, size)


def text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = word if not current else current + " " + word
        w, _ = text_size(draw, candidate, font)
        if w <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(draw, x, y, max_width, text, font, fill, line_height, max_lines=None):
    lines = wrap_text(draw, text, font, max_width)
    if max_lines is not None and len(lines) > max_lines:
        raise ValueError(
            "Text exceeded max_lines="
            + str(max_lines)
            + " (got "
            + str(len(lines))
            + "): "
            + text[:60]
        )
    cy = y
    for line in lines:
        w, _ = text_size(draw, line, font)
        if w > max_width + 1:
            raise ValueError("Line overflow width=" + str(w) + ">" + str(max_width) + ": " + line)
        draw.text((x, cy), line, font=font, fill=fill)
        cy += line_height
    return cy


def draw_centered_text(draw, cx, y, text, font, fill):
    w, _ = text_size(draw, text, font)
    draw.text((cx - w // 2, y), text, font=font, fill=fill)


# ---------------------------------------------------------------------------
# Flat geometric illustrations for Leads (1..3) and Small Stories (4..15)
# ---------------------------------------------------------------------------

def draw_lead_illustration(draw, kind, x, y, w, h):
    if kind == 1:
        # Cartagena supermarket rescue
        draw.rectangle([x, y, x + w, y + h], fill=(224, 232, 238), outline=RULE_LIGHT)
        # Road
        draw.rectangle([x, y + h - 8, x + w, y + h], fill=(78, 82, 88))
        # Supermarket building
        bx0, by0, bx1, by1 = x + 46, y + 5, x + w - 96, y + h - 8
        draw.rectangle([bx0, by0, bx1, by1], fill=(244, 236, 214), outline=INK)
        # Red/orange awning stripes
        draw.rectangle([bx0 - 4, by0 + 6, bx1 + 4, by0 + 12], fill=RED, outline=INK)
        for sx in range(bx0, bx1, 14):
            draw.rectangle([sx, by0 + 6, min(sx + 7, bx1), by0 + 12], fill=WHITE)
        # Entrance glass doors and windows
        mid = (bx0 + bx1) // 2
        draw.rectangle([mid - 14, by0 + 14, mid + 14, by1], fill=(130, 174, 204), outline=INK)
        draw.line([mid, by0 + 14, mid, by1], fill=INK, width=1)
        draw.rectangle([bx0 + 10, by0 + 14, mid - 22, by1 - 4], fill=(168, 200, 218), outline=INK)
        draw.rectangle([mid + 22, by0 + 14, bx1 - 10, by1 - 4], fill=(168, 200, 218), outline=INK)
        # Armoured van on right
        vx0, vy0, vx1, vy1 = x + w - 82, y + 14, x + w - 18, y + h - 9
        draw.rectangle([vx0, vy0, vx1, vy1], fill=NAVY, outline=INK)
        draw.rectangle([vx1 - 16, vy0 + 3, vx1 - 3, vy0 + 9], fill=(170, 210, 230))
        draw.ellipse([vx0 + 6, vy1 - 4, vx0 + 16, vy1 + 4], fill=INK)
        draw.ellipse([vx1 - 18, vy1 - 4, vx1 - 8, vy1 + 4], fill=INK)
        # Freed figure silhouettes on left
        for fx in (x + 14, x + 26, x + 36):
            draw.ellipse([fx, y + 18, fx + 6, y + 24], fill=NAVY)
            draw.rectangle([fx + 1, y + 24, fx + 5, y + h - 8], fill=RED)

    elif kind == 2:
        # Jiuquan Long March 2F rocket to Tiangong
        draw.rectangle([x, y, x + w, y + h], fill=(16, 28, 52), outline=RULE_LIGHT)
        # Stars & orbital arc
        for sx, sy in ((22, 10), (54, 24), (84, 9), (120, 30), (206, 12), (242, 28), (284, 10), (298, 26)):
            draw.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=WHITE)
        draw.arc([x + 170, y + 4, x + w - 12, y + 54], start=190, end=340, fill=(100, 145, 190), width=1)
        # Tiny Tiangong station silhouette in upper right
        tx, ty = x + w - 62, y + 12
        draw.rectangle([tx, ty + 3, tx + 24, ty + 7], fill=(220, 224, 230))
        draw.rectangle([tx + 5, ty - 3, tx + 8, ty + 13], fill=(70, 130, 190))
        draw.rectangle([tx + 15, ty - 3, tx + 18, ty + 13], fill=(70, 130, 190))
        # Desert ground & launch tower
        draw.rectangle([x, y + h - 7, x + w, y + h], fill=(176, 152, 114))
        draw.rectangle([x + 105, y + 10, x + 114, y + h - 7], fill=(130, 138, 148))
        draw.line([x + 114, y + 16, x + 132, y + 16], fill=(130, 138, 148), width=2)
        # Rocket body (Long March 2F)
        rx = x + 148
        draw.polygon([(rx, y + 3), (rx - 7, y + 13), (rx + 7, y + 13)], fill=RED)
        draw.rectangle([rx - 7, y + 13, rx + 7, y + h - 13], fill=WHITE, outline=INK)
        # Side boosters
        draw.rectangle([rx - 13, y + 20, rx - 7, y + h - 13], fill=(228, 228, 232), outline=INK)
        draw.rectangle([rx + 7, y + 20, rx + 13, y + h - 13], fill=(228, 228, 232), outline=INK)
        # Exhaust flame
        draw.polygon([(rx - 9, y + h - 13), (rx + 9, y + h - 13), (rx, y + h - 2)], fill=(238, 140, 32))
        draw.polygon([(rx - 4, y + h - 13), (rx + 4, y + h - 13), (rx, y + h - 5)], fill=(252, 226, 110))

    elif kind == 3:
        # Canberra Australia-Solomon Islands signing table & two flags
        draw.rectangle([x, y, x + w, y + h], fill=(236, 230, 216), outline=RULE_LIGHT)
        # Australian flag (left)
        fx1, fy1, fw, fh = x + 22, y + 6, 48, 24
        draw.rectangle([fx1, fy1, fx1 + fw, fy1 + fh], fill=(18, 46, 118), outline=INK)
        draw.rectangle([fx1, fy1, fx1 + 20, fy1 + 11], fill=(20, 56, 138))
        draw.line([fx1, fy1 + 5, fx1 + 20, fy1 + 5], fill=WHITE, width=3)
        draw.line([fx1 + 10, fy1, fx1 + 10, fy1 + 11], fill=WHITE, width=3)
        draw.line([fx1, fy1 + 5, fx1 + 20, fy1 + 5], fill=RED, width=1)
        draw.line([fx1 + 10, fy1, fx1 + 10, fy1 + 11], fill=RED, width=1)
        for sx, sy in ((10, 17), (32, 8), (38, 14), (29, 17), (41, 6)):
            draw.ellipse([fx1 + sx, fy1 + sy, fx1 + sx + 2, fy1 + sy + 2], fill=WHITE)
        # Solomon Islands flag (right)
        fx2, fy2 = x + w - 70, y + 6
        draw.polygon([(fx2, fy2), (fx2 + fw, fy2), (fx2, fy2 + fh)], fill=(24, 78, 152))
        draw.polygon([(fx2 + fw, fy2), (fx2 + fw, fy2 + fh), (fx2, fy2 + fh)], fill=(36, 124, 66))
        draw.line([fx2, fy2 + fh, fx2 + fw, fy2], fill=(236, 198, 42), width=3)
        draw.rectangle([fx2, fy2, fx2 + fw, fy2 + fh], outline=INK)
        for sx, sy in ((5, 4), (11, 4), (8, 8), (5, 12), (11, 12)):
            draw.ellipse([fx2 + sx, fy2 + sy, fx2 + sx + 2, fy2 + sy + 2], fill=WHITE)
        # Signing table & treaty paper in center
        tx0, tx1 = x + 102, x + w - 102
        draw.rectangle([tx0, y + 25, tx1, y + h - 4], fill=(142, 92, 54), outline=INK)
        # Two leaders behind table
        for px in (tx0 + 20, tx1 - 28):
            draw.ellipse([px, y + 8, px + 10, y + 17], fill=(224, 186, 152), outline=INK)
            draw.rectangle([px - 3, y + 17, px + 13, y + 25], fill=NAVY)
        # Treaty document + red seal
        mid = (tx0 + tx1) // 2
        draw.rectangle([mid - 16, y + 19, mid + 16, y + 32], fill=WHITE, outline=INK)
        draw.line([mid - 11, y + 23, mid + 11, y + 23], fill=MUTED, width=1)
        draw.line([mid - 11, y + 27, mid + 4, y + 27], fill=MUTED, width=1)
        draw.ellipse([mid + 6, y + 26, mid + 12, y + 31], fill=RED)


def draw_small_illustration(draw, story_id, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(236, 232, 222), outline=RULE_LIGHT)
    if story_id == 4:
        # Hodeidah port cranes + smoke
        draw.rectangle([x, y + h - 6, x + w, y + h], fill=(64, 118, 156))
        draw.rectangle([x + 12, y + h - 12, x + w - 12, y + h - 6], fill=(156, 146, 130))
        draw.line([x + 30, y + h - 12, x + 30, y + 5], fill=RED, width=2)
        draw.line([x + 30, y + 6, x + 58, y + 11], fill=RED, width=2)
        draw.line([x + 95, y + h - 12, x + 95, y + 6], fill=NAVY, width=2)
        draw.line([x + 95, y + 7, x + 120, y + 12], fill=NAVY, width=2)
        draw.ellipse([x + 56, y + 4, x + 74, y + 15], fill=(92, 92, 96))
        draw.ellipse([x + 68, y + 2, x + 84, y + 12], fill=(128, 128, 132))
    elif story_id == 5:
        # Hormuz two burning tankers
        draw.rectangle([x, y, x + w, y + h - 10], fill=(214, 226, 234))
        draw.rectangle([x, y + h - 10, x + w, y + h], fill=(48, 102, 144))
        for tx in (x + 22, x + 86):
            draw.polygon([(tx, y + h - 12), (tx + 44, y + h - 12), (tx + 38, y + h - 5), (tx + 4, y + h - 5)], fill=INK)
            draw.polygon([(tx + 14, y + h - 12), (tx + 26, y + h - 12), (tx + 20, y + 4)], fill=(224, 92, 24))
            draw.polygon([(tx + 17, y + h - 12), (tx + 23, y + h - 12), (tx + 20, y + 9)], fill=(248, 206, 62))
    elif story_id == 6:
        # Asian markets plunge chart
        draw.rectangle([x, y, x + w, y + h], fill=(244, 240, 232), outline=RULE_LIGHT)
        for gy in (y + 7, y + 14, y + 21):
            draw.line([x + 6, gy, x + w - 6, gy], fill=(218, 212, 200), width=1)
        pts = [(x + 10, y + 6), (x + 38, y + 9), (x + 60, y + 7), (x + 88, y + 16), (x + 112, y + 14), (x + w - 12, y + h - 4)]
        draw.line(pts, fill=RED, width=2)
    elif story_id == 7:
        # Brussels EU stars + manifesto
        draw.rectangle([x, y, x + w, y + h], fill=(24, 52, 114))
        cx, cy = x + 38, y + h // 2
        for dx, dy in ((0, -8), (6, -6), (8, 0), (6, 6), (0, 8), (-6, 6), (-8, 0), (-6, -6)):
            draw.ellipse([cx + dx - 1, cy + dy - 1, cx + dx + 1, cy + dy + 1], fill=(244, 204, 48))
        draw.rectangle([x + 76, y + 4, x + w - 18, y + h - 4], fill=WHITE, outline=INK)
        draw.line([x + 82, y + 9, x + w - 24, y + 9], fill=NAVY, width=1)
        draw.line([x + 82, y + 14, x + w - 24, y + 14], fill=MUTED, width=1)
        draw.line([x + 82, y + 19, x + w - 34, y + 19], fill=RED, width=1)
    elif story_id == 8:
        # New York courthouse & gavel
        draw.polygon([(x + 22, y + 11), (x + 54, y + 3), (x + 86, y + 11)], fill=(190, 182, 168), outline=INK)
        draw.rectangle([x + 24, y + 11, x + 84, y + h - 3], fill=(230, 224, 212), outline=INK)
        for cx in (x + 32, x + 46, x + 60, x + 74):
            draw.line([cx, y + 11, cx, y + h - 3], fill=INK, width=2)
        draw.rectangle([x + 102, y + 7, x + 124, y + 14], fill=(134, 78, 38), outline=INK)
        draw.line([x + 113, y + 14, x + 132, y + h - 4], fill=(112, 64, 30), width=2)
    elif story_id == 9:
        # Bangladesh flag + wage bars
        draw.rectangle([x + 14, y + 5, x + 56, y + h - 5], fill=(16, 106, 72), outline=INK)
        draw.ellipse([x + 27, y + 7, x + 41, y + h - 7], fill=RED)
        for i, bh in enumerate((8, 12, 17)):
            bx = x + 72 + i * 20
            draw.rectangle([bx, y + h - 4 - bh, bx + 12, y + h - 4], fill=NAVY if i < 2 else RED)
    elif story_id == 10:
        # Flooded Indonesian mine
        draw.rectangle([x, y, x + w, y + 11], fill=(144, 120, 88))
        draw.rectangle([x, y + 11, x + w, y + h], fill=(64, 54, 46))
        draw.rectangle([x + 56, y + 4, x + 94, y + h - 2], fill=(42, 36, 32))
        draw.rectangle([x + 56, y + 15, x + 94, y + h - 2], fill=(48, 108, 148))
        draw.line([x + 56, y + 4, x + 56, y + h - 2], fill=(196, 168, 112), width=2)
        draw.line([x + 94, y + 4, x + 94, y + h - 2], fill=(196, 168, 112), width=2)
    elif story_id == 11:
        # Gulf of Mexico plane crash search
        draw.rectangle([x, y, x + w, y + h - 11], fill=(208, 224, 236))
        draw.rectangle([x, y + h - 11, x + w, y + h], fill=(46, 104, 152))
        draw.polygon([(x + 38, y + h - 11), (x + 56, y + h - 11), (x + 48, y + 6)], fill=WHITE, outline=INK)
        draw.rectangle([x + 88, y + h - 14, x + 116, y + h - 10], fill=RED, outline=INK)
    elif story_id == 12:
        # DR Congo clinic + red cross
        draw.rectangle([x + 44, y + 5, x + w - 44, y + h - 3], fill=WHITE, outline=INK)
        cx, cy = x + w // 2, y + (h + 2) // 2
        draw.rectangle([cx - 3, cy - 8, cx + 3, cy + 8], fill=RED)
        draw.rectangle([cx - 8, cy - 3, cx + 8, cy + 3], fill=RED)
    elif story_id == 13:
        # Australian inflation spike
        draw.rectangle([x, y, x + w, y + h], fill=(244, 240, 232), outline=RULE_LIGHT)
        for i, bh in enumerate((6, 9, 11, 14, 20)):
            bx = x + 18 + i * 24
            draw.rectangle([bx, y + h - 3 - bh, bx + 14, y + h - 3], fill=NAVY if i < 4 else RED)
    elif story_id == 14:
        # UK energy bills rising
        draw.polygon([(x + 26, y + 13), (x + 46, y + 4), (x + 66, y + 13)], fill=RED, outline=INK)
        draw.rectangle([x + 31, y + 13, x + 61, y + h - 3], fill=(242, 234, 214), outline=INK)
        draw.rectangle([x + 42, y + 17, x + 50, y + h - 3], fill=NAVY)
        draw.polygon([(x + 92, y + 6), (x + 102, y + 6), (x + 97, y + 14), (x + 105, y + 14), (x + 90, y + h - 3), (x + 95, y + 16), (x + 88, y + 16)], fill=(228, 134, 28))
    elif story_id == 15:
        # Argentina recession
        draw.rectangle([x + 14, y + 5, x + 56, y + 11], fill=(116, 172, 223))
        draw.rectangle([x + 14, y + 11, x + 56, y + 17], fill=WHITE)
        draw.rectangle([x + 14, y + 17, x + 56, y + 23], fill=(116, 172, 223))
        draw.rectangle([x + 14, y + 5, x + 56, y + 23], outline=INK)
        pts = [(x + 74, y + 6), (x + 96, y + 11), (x + 116, y + 16), (x + w - 14, y + h - 4)]
        draw.line(pts, fill=RED, width=2)


# ---------------------------------------------------------------------------
# World map renderer (flat continent silhouettes + pins 1..15)
# ---------------------------------------------------------------------------

def draw_world_map(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=SEA_BLUE, outline=RULE_DARK)

    def proj(lon, lat):
        px = x + int((lon + 180.0) / 360.0 * w)
        py = y + int((82.0 - lat) / 142.0 * h)
        return px, py

    def poly(coords):
        pts = [proj(lo, la) for lo, la in coords]
        draw.polygon(pts, fill=LAND_TAN, outline=LAND_EDGE)

    # North America
    poly([(-166, 65), (-135, 70), (-92, 68), (-58, 52), (-74, 40), (-82, 25), (-96, 20), (-86, 10), (-94, 15), (-108, 24), (-124, 44), (-142, 58)])
    # Greenland
    poly([(-54, 76), (-20, 78), (-22, 64), (-46, 61)])
    # South America
    poly([(-79, 10), (-62, 11), (-36, -6), (-42, -24), (-64, -46), (-70, -54), (-76, -42), (-72, -18), (-81, -4)])
    # Europe
    poly([(-9, 37), (-9, 44), (-2, 48), (4, 53), (12, 56), (26, 70), (42, 68), (54, 62), (48, 45), (30, 42), (16, 40), (5, 43), (-4, 36)])
    # UK & Ireland
    poly([(-7, 50), (-5, 58), (1, 57), (2, 51)])
    # Africa
    poly([(-17, 15), (-10, 34), (10, 36), (32, 31), (43, 12), (51, 12), (40, -10), (34, -26), (20, -34), (14, -22), (9, 4), (-8, 5)])
    # Madagascar
    poly([(44, -25), (50, -14), (48, -12), (43, -23)])
    # Asia
    poly([(28, 41), (46, 44), (58, 62), (104, 74), (168, 66), (160, 54), (138, 44), (122, 34), (120, 22), (108, 10), (100, 14), (92, 22), (78, 8), (68, 24), (54, 24), (44, 14), (35, 30)])
    # Japan
    poly([(131, 32), (141, 44), (145, 42), (135, 31)])
    # Indonesia / Maritime SE Asia
    poly([(96, 4), (106, -6), (118, -8), (114, 1)])
    poly([(128, -2), (141, -8), (140, -2), (128, 1)])
    # Australia & New Zealand
    poly([(114, -22), (130, -12), (142, -12), (153, -26), (148, -38), (134, -34), (116, -34)])
    poly([(168, -46), (178, -36), (179, -39), (170, -47)])

    # Equator subtle line
    _, eq_y = proj(0, 0)
    draw.line([x + 1, eq_y, x + w - 1, eq_y], fill=(176, 196, 210), width=1)

    # Numbered pins for stories 1..15 (slight offsets where needed for legibility)
    pins = [
        (1, -75.5, 10.4, 0, 0),      # Cartagena
        (2, 100.3, 40.9, 0, 0),      # Jiuquan
        (3, 147.0, -37.0, -4, 3),    # Canberra
        (4, 42.0, 14.0, -3, 2),      # Hodeidah
        (5, 57.5, 27.5, 4, -2),      # Hormuz
        (6, 134.0, 36.0, 0, 0),      # Tokyo/Seoul
        (7, 8.0, 49.0, 5, 2),        # Brussels
        (8, -73.0, 42.0, 4, -3),     # New York
        (9, 90.4, 23.8, 0, 0),       # Dhaka
        (10, 114.0, -4.0, 0, 0),     # Indonesia
        (11, -90.0, 27.0, -4, 2),    # Gulf of Mexico
        (12, 29.0, 1.8, 0, 0),       # Ituri
        (13, 153.5, -31.0, 5, -3),   # Sydney
        (14, -4.0, 54.0, -5, -3),    # London
        (15, -58.4, -34.6, 0, 0),    # Buenos Aires
    ]

    font_pin = load_font(F_SANS_B, 10)
    for num, lon, lat, dx, dy in pins:
        px, py = proj(lon, lat)
        px += dx
        py += dy
        r = 6
        draw.ellipse([px - r, py - r, px + r, py + r], fill=RED, outline=WHITE)
        label = str(num)
        lw, lh = text_size(draw, label, font_pin)
        draw.text((px - lw // 2, py - lh // 2 - 1), label, font=font_pin, fill=WHITE)


# ---------------------------------------------------------------------------
# Verified story data
# ---------------------------------------------------------------------------

LEADS = [
    {
        "num": 1,
        "location": "CARTAGENA, COLOMBIA",
        "region": "Americas",
        "tag": "REPORTED",
        "headline": "Hostages freed as forces storm Cartagena supermarket",
        "body": (
            "Special forces stormed a supermarket in Cartagena on Wednesday, ending a "
            "hostage-taking that began the previous day when a robbery of an armoured "
            "vehicle failed. About 30 people held in the store were freed unharmed; one "
            "assailant was killed. President Abelardo de la Espriella said every hostage "
            "came out alive."
        ),
        "sources": "Sources: wire reports via Horizon 25 Nov.",
    },
    {
        "num": 2,
        "location": "JIUQUAN, CHINA",
        "region": "Asia-Pacific",
        "tag": "REPORTED",
        "headline": "Pakistan's first astronaut flies to China's space station",
        "body": (
            "Pakistan's first astronaut, Zeeshan Ali, lifted off on a Long March 2F rocket "
            "from the Jiuquan base bound for China's Tiangong space station — the first "
            "foreign national to fly to the Chinese station. The flight makes Pakistan the "
            "latest country to reach orbit aboard a Chinese spacecraft."
        ),
        "sources": "Sources: 3 via Horizon 25 Nov; One Turn 25 Nov.",
    },
    {
        "num": 3,
        "location": "CANBERRA, AUSTRALIA",
        "region": "Oceania",
        "tag": "REPORTED",
        "headline": "Australia and Solomon Islands sign security treaty",
        "body": (
            "Australia and Solomon Islands signed a security treaty in Canberra on Wednesday "
            "naming Australia the Pacific nation's primary security partner and ruling out "
            "foreign military or security bases on Solomon Islands territory. PM Jeremiah "
            "Manele signed alongside Anthony Albanese; the 2022 China pact is reportedly scrapped."
        ),
        "sources": "Sources: Australian PM office; Reuters, 25 Nov.",
    },
]

SMALL_STORIES = [
    {
        "num": 4,
        "location": "HODEIDAH",
        "region": "Middle East",
        "tag": "REPORTED",
        "headline": "Hodeidah struck; Houthis warn Jeddah",
        "body": "Coalition hit Yemen's port after Riyadh attack hurt 11.",
        "source": "Horizon / Indian media",
    },
    {
        "num": 5,
        "location": "HORMUZ STRAIT",
        "region": "Middle East",
        "tag": "CLAIM",
        "headline": "Iran says tankers hit Hormuz mines",
        "body": "IRGC said two oil tankers caught fire; unconfirmed.",
        "source": "IRIB 06:34Z / One Turn",
    },
    {
        "num": 6,
        "location": "TOKYO / SEOUL",
        "region": "World",
        "tag": "REPORTED",
        "headline": "Asian shares drop on AI doubts",
        "body": "Nikkei fell 2.78%, S Korea over 6%; Brent slid 4.37%.",
        "source": "Horizon market data",
    },
    {
        "num": 7,
        "location": "BRUSSELS",
        "region": "Europe",
        "tag": "REPORTED",
        "headline": "EU vows 'whatever it takes' on Ukraine",
        "body": "90+ leaders urged closing 70bn-euro gap via Russian assets.",
        "source": "Friends of Europe",
    },
    {
        "num": 8,
        "location": "NEW YORK",
        "region": "Americas",
        "tag": "REPORTED",
        "headline": "Huawei guilty in US bank-fraud trial",
        "body": "Guilty of fraud & trade theft; cleared of racketeering.",
        "source": "4 sources via Horizon",
    },
    {
        "num": 9,
        "location": "DHAKA",
        "region": "Asia-Pacific",
        "tag": "PENDING",
        "headline": "Bangladesh raises textile wage 36%",
        "body": "Pay rise follows October protests; workers not yet settled.",
        "source": "4 sources via Horizon",
    },
    {
        "num": 10,
        "location": "INDONESIA",
        "region": "Asia-Pacific",
        "tag": "PENDING",
        "headline": "Rescuers hunt dozens in flooded mine",
        "body": "Trapped 100m down since 23 Nov; 26 cited, no rescue yet.",
        "source": "Horizon / One Turn",
    },
    {
        "num": 11,
        "location": "GULF OF MEXICO",
        "region": "Americas",
        "tag": "REPORTED",
        "headline": "Six dead in Gulf small plane crash",
        "body": "Two boys aged 8 and 10 died off Mississippi coast.",
        "source": "2 sources via Horizon",
    },
    {
        "num": 12,
        "location": "ITURI, DR CONGO",
        "region": "Africa",
        "tag": "REPORTED",
        "headline": "UN: Ebola fuels violence on women",
        "body": "Over 5,800 dead since May; fighting traps staff.",
        "source": "Horizon / UN News",
    },
    {
        "num": 13,
        "location": "SYDNEY",
        "region": "Oceania",
        "tag": "REPORTED",
        "headline": "Australian inflation jumps to 4.9%",
        "body": "Up from 4.3% in Sept, above 2.5% target; ASX up 1.35%.",
        "source": "One Turn Australia",
    },
    {
        "num": 14,
        "location": "LONDON",
        "region": "Europe",
        "tag": "REPORTED",
        "headline": "UK energy bills to rise 26% in Jan",
        "body": "Ofgem cap rises from 1,723 to 2,166 pounds a year.",
        "source": "2 sources via Horizon",
    },
    {
        "num": 15,
        "location": "BUENOS AIRES",
        "region": "Americas",
        "tag": "REPORTED",
        "headline": "Argentina enters technical recession",
        "body": "Q3 output fell 1.2% YoY after two shrinking quarters.",
        "source": "4 sources via Horizon",
    },
]

ALSO_ON_WEDNESDAY = [
    (16, "REPORTED", "India 3rd in Lowy Asia Power Index (40.5); US 78.9, China 73.6, Pakistan 16th.", "Lowy Inst. 04:53Z"),
    (17, "REPORTED", "Geneva: UN warns decades of HIV/AIDS gains risk unravelling as funding falls.", "PANA 06:22Z"),
    (18, "REPORTED", "Jerusalem: Golan's Democrats halt Eisenkot talks as Yashar signs Beiteinu pact.", "Horizon"),
    (19, "REPORTED", "Shanghai: Party chief & Politburo member Chen Jining under anti-corruption probe.", "Straits Times"),
    (20, "REPORTED", "Washington: Kilmar Abrego Garcia leaves the United States for Spain voluntarily.", "Le Monde"),
    (21, "REPORTED", "Beijing: Xiamen Airlines orders 50 Boeing 737 MAX 8 jets for about $7.4bn.", "Horizon markets"),
    (22, "REPORTED", "Paris: BYD opens exclusive talks to take over Ineos Automotive's French plant.", "Horizon markets"),
    (23, "REPORTED", "Kourou: Ariane 6 completes 10th launch, orbiting 36 Amazon Leo satellites.", "La Tribune"),
    (24, "REPORTED", "Newcastle: Canada's women beat Team World 10-0 in Para hockey world opener.", "CBC Sports"),
    (25, "REPORTED", "Suva: Officials warn Fiji's drought emergency could stretch into 2027.", "PINA 25 Nov"),
    (26, "FORECAST", "Pacific: Fisheries ministers at WCPFC23 set to decide bigeye tuna catch limits.", "PINA 25 Nov"),
    (27, "REPORTED", "Paris: Brussels gives lenient opinion on France 2027 budget; Senate cuts tax break.", "Horizon markets"),
    (28, "REPORTED", "Kuala Lumpur: Malaysia Airlines orders ten Boeing 787s, deliveries 2032-2035.", "Straits Times"),
    (29, "REPORTED", "Kinshasa: DR Congo freezes cobalt exports again as prices fall.", "Jeune Afrique"),
    (30, "REPORTED", "Washington: US prepares new tariff plan targeting China, EU and other partners.", "BBC Business"),
    (31, "REPORTED", "Space: Europe's Hera probe studies the asteroid NASA deflected four years ago.", "BBC"),
]


def render():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_CREAM)
    draw = ImageDraw.Draw(img)

    # Fonts (>= 11px for all body text)
    f_strip = load_font(F_SANS_B, 11)
    f_masthead = load_font(F_SERIF_B, 35)
    f_standfirst = load_font(F_SERIF, 12)
    f_fig_num = load_font(F_SERIF_B, 19)
    f_sans_11 = load_font(F_SANS, 11)
    f_sans_b11 = load_font(F_SANS_B, 11)
    f_lead_hl = load_font(F_SERIF_B, 14)
    f_small_hl = load_font(F_SERIF_B, 11)
    f_sec_hdr = load_font(F_SANS_B, 11)

    y = 4

    # 1. Thin dark rule + navy top strip
    draw.line([MARGIN, y, WIDTH - MARGIN, y], fill=RULE_DARK, width=2)
    y += 4
    draw.rectangle([MARGIN, y, WIDTH - MARGIN, y + 21], fill=NAVY)
    draw.text((MARGIN + 8, y + 4), "THE WORLD ON ONE PAGE", font=f_strip, fill=WHITE)
    right_top = "31 STORIES  ·  7 REGIONS  ·  EVERY STORY DATED WEDNESDAY 25 NOVEMBER 2026"
    rw, _ = text_size(draw, right_top, f_strip)
    draw.text((WIDTH - MARGIN - 8 - rw, y + 4), right_top, font=f_strip, fill=WHITE)
    y += 23

    # 2. Masthead
    draw_centered_text(draw, WIDTH // 2, y, "Wednesday 25 November 2026", f_masthead, INK)
    y += 38

    # 3. Standfirst (regular DejaVu Serif, coloured red)
    standfirst = (
        "Cartagena hostages freed  ·  Pakistan's first astronaut flies to Tiangong  ·  "
        "Australia–Solomon Islands security treaty"
    )
    sw, _ = text_size(draw, standfirst, f_standfirst)
    if sw > CONTENT_W:
        raise ValueError("Standfirst overflow: " + str(sw))
    draw_centered_text(draw, WIDTH // 2, y, standfirst, f_standfirst, RED)
    y += 17
    draw.line([MARGIN, y, WIDTH - MARGIN, y], fill=RULE_DARK, width=1)
    y += 3

    # 4. Figures strip (6 large red serif numbers + short sans caption)
    figures = [
        ("-2.78%", "Nikkei 225 fall on Wednesday"),
        ("+36%", "Bangladesh textile wage rise"),
        ("5,800+", "Ebola deaths in Congo since May"),
        ("50", "Boeing jets in China order ($7.4bn)"),
        ("4.9%", "Australian inflation, up from 4.3%"),
        ("100 m", "Depth of flooded Indonesian mine"),
    ]
    fig_h = 44
    draw.rectangle([MARGIN, y, WIDTH - MARGIN, y + fig_h], fill=PAPER_ALT, outline=RULE_LIGHT)
    col_w = CONTENT_W / 6.0
    for idx, (num_str, cap_str) in enumerate(figures):
        fx = int(MARGIN + idx * col_w)
        fw = int(col_w)
        if idx > 0:
            draw.line([fx, y + 4, fx, y + fig_h - 4], fill=RULE_LIGHT, width=1)
        draw_centered_text(draw, fx + fw // 2, y + 1, num_str, f_fig_num, RED)
        lines = wrap_text(draw, cap_str, f_sans_11, fw - 10)
        if len(lines) > 2:
            raise ValueError("Figure caption exceeded 2 lines: " + cap_str)
        cy = y + 21
        for line in lines:
            draw_centered_text(draw, fx + fw // 2, cy, line, f_sans_11, INK)
            cy += 11
    y += fig_h + 3

    # 5. Region bar (7 colour-coded segments)
    regions = [
        ("Europe", 4),
        ("Middle East", 3),
        ("Asia-Pacific", 6),
        ("Americas", 5),
        ("Africa", 2),
        ("Oceania", 5),
        ("World", 6),
    ]
    reg_h = 19
    # Base minimum width + proportional share so every label fits cleanly
    base_w = 24
    rem_w = CONTENT_W - base_w * len(regions)
    rx = MARGIN
    for i, (rname, rcount) in enumerate(regions):
        if i == len(regions) - 1:
            seg_w = (WIDTH - MARGIN) - rx
        else:
            seg_w = base_w + round(rem_w * (rcount / 31.0))
        draw.rectangle([rx, y, rx + seg_w, y + reg_h], fill=REGION_COLORS[rname], outline=BG_CREAM)
        label = rname + " " + str(rcount)
        lw, _ = text_size(draw, label, f_sans_b11)
        if lw > seg_w - 4:
            raise ValueError("Region label overflow: " + label + " width=" + str(lw) + " seg_w=" + str(seg_w))
        draw_centered_text(draw, rx + seg_w // 2, y + 3, label, f_sans_b11, WHITE)
        rx += seg_w
    y += reg_h + 3

    # 6. "The day in UTC" timeline strip
    utc_h = 37
    draw.rectangle([MARGIN, y, WIDTH - MARGIN, y + utc_h], fill=NAVY_DARK)
    label_box_w = 88
    draw.rectangle([MARGIN, y, MARGIN + label_box_w, y + utc_h], fill=RED)
    draw_centered_text(draw, MARGIN + label_box_w // 2, y + 6, "THE DAY", f_sans_b11, WHITE)
    draw_centered_text(draw, MARGIN + label_box_w // 2, y + 18, "IN UTC", f_sans_b11, WHITE)

    utc_events = [
        ("00:09Z", "Guards say tankers hit Hormuz mines"),
        ("04:53Z", "Lowy Asia Power Index published"),
        ("06:22Z", "UN warns HIV gains at risk"),
        ("06:34Z", "Iran says 2 tankers ablaze in Hormuz"),
        ("Canberra", "Australia-Solomons treaty signed"),
        ("Cartagena", "Forces free store hostages"),
    ]
    ev_area_w = CONTENT_W - label_box_w
    ev_w = ev_area_w / 6.0
    for idx, (tstamp, desc) in enumerate(utc_events):
        ex = int(MARGIN + label_box_w + idx * ev_w)
        ew = int(ev_w)
        if idx > 0:
            draw.line([ex, y + 4, ex, y + utc_h - 4], fill=(48, 66, 94), width=1)
        draw.text((ex + 6, y + 2), tstamp, font=f_sans_b11, fill=(252, 206, 114))
        draw_wrapped(draw, ex + 6, y + 14, ew - 10, desc, f_sans_11, WHITE, 11, max_lines=2)
    y += utc_h + 4

    # 7. Three lead stories side by side
    lead_gap = 8
    lead_w = (CONTENT_W - 2 * lead_gap) // 3  # 326
    lead_h = 207
    for idx, lead in enumerate(LEADS):
        lx = MARGIN + idx * (lead_w + lead_gap)
        draw.rectangle([lx, y, lx + lead_w, y + lead_h], fill=PAPER_ALT, outline=RULE_LIGHT)
        pad = 7
        inner_w = lead_w - 2 * pad
        draw_lead_illustration(draw, lead["num"], lx + pad, y + 4, inner_w, 38)

        cy = y + 45
        # Number + Location + Category + Certainty tag
        num_txt = str(lead["num"]) + " "
        draw.text((lx + pad, cy), num_txt, font=f_sans_b11, fill=RED)
        nw, _ = text_size(draw, num_txt, f_sans_b11)
        meta_txt = lead["location"] + " (" + lead["region"] + ")"
        draw.text((lx + pad + nw, cy), meta_txt, font=f_sans_b11, fill=NAVY)

        tag_txt = lead["tag"]
        tw, _ = text_size(draw, tag_txt, f_sans_b11)
        tx = lx + lead_w - pad - tw - 8
        draw.rectangle([tx, cy - 1, tx + tw + 8, cy + 12], fill=TAG_COLORS[tag_txt])
        draw.text((tx + 4, cy), tag_txt, font=f_sans_b11, fill=WHITE)
        cy += 15

        # Headline (2 lines)
        cy = draw_wrapped(draw, lx + pad, cy, inner_w, lead["headline"], f_lead_hl, INK, 16, max_lines=2)
        cy += 2

        # Body (up to 7 lines at 11px sans)
        cy = draw_wrapped(draw, lx + pad, cy, inner_w, lead["body"], f_sans_11, INK, 13, max_lines=7)

        # Sources line anchored near bottom
        draw_wrapped(draw, lx + pad, y + lead_h - 15, inner_w, lead["sources"], f_sans_11, MUTED, 12, max_lines=1)

    y += lead_h + 4

    # 8. Two rows of smaller illustrated stories (6 per row, 12 total)
    card_gap = 6
    card_w = (CONTENT_W - 5 * card_gap) // 6  # 161
    row_h = 134
    for row_idx in range(2):
        ry = y + row_idx * (row_h + 3)
        for col_idx in range(6):
            st = SMALL_STORIES[row_idx * 6 + col_idx]
            cx = MARGIN + col_idx * (card_w + card_gap)
            draw.rectangle([cx, ry, cx + card_w, ry + row_h], fill=PAPER_ALT, outline=RULE_LIGHT)
            pad = 5
            iw = card_w - 2 * pad
            draw_small_illustration(draw, st["num"], cx + pad, ry + 4, iw, 24)

            ty = ry + 30
            num_s = str(st["num"]) + " "
            draw.text((cx + pad, ty), num_s, font=f_sans_b11, fill=RED)
            nw, _ = text_size(draw, num_s, f_sans_b11)
            draw.text((cx + pad + nw, ty), st["location"], font=f_sans_b11, fill=NAVY)
            ty += 12

            draw.text((cx + pad, ty), st["region"], font=f_sans_11, fill=MUTED)
            tag_s = st["tag"]
            tw, _ = text_size(draw, tag_s, f_sans_b11)
            draw.rectangle([cx + card_w - pad - tw - 6, ty - 1, cx + card_w - pad, ty + 12], fill=TAG_COLORS[tag_s])
            draw.text((cx + card_w - pad - tw - 3, ty), tag_s, font=f_sans_b11, fill=WHITE)
            ty += 14

            ty = draw_wrapped(draw, cx + pad, ty, iw, st["headline"], f_small_hl, INK, 13, max_lines=2)
            ty += 2
            ty = draw_wrapped(draw, cx + pad, ty, iw, st["body"], f_sans_11, INK, 12, max_lines=3)
            draw_wrapped(draw, cx + pad, ry + row_h - 14, iw, st["source"], f_sans_11, MUTED, 11, max_lines=1)

    y += 2 * row_h + 3 + 4

    # 9. "Also on Wednesday" (16 items) on left + 10. "Where it happened" world map on right
    mid_h = 221
    also_w = 640
    map_gap = 8
    map_w = CONTENT_W - also_w - map_gap  # 348

    # Section 9 panel
    draw.rectangle([MARGIN, y, MARGIN + also_w, y + mid_h], fill=PAPER_ALT, outline=RULE_LIGHT)
    draw.rectangle([MARGIN, y, MARGIN + also_w, y + 17], fill=NAVY)
    draw.text((MARGIN + 7, y + 2), "ALSO ON WEDNESDAY (STORIES 16–31)", font=f_sec_hdr, fill=WHITE)

    iy = y + 19
    for num, tag, headline, source in ALSO_ON_WEDNESDAY:
        prefix = str(num) + ". "
        draw.text((MARGIN + 6, iy), prefix, font=f_sans_b11, fill=RED)
        pw, _ = text_size(draw, prefix, f_sans_b11)

        if tag == "FORECAST":
            badge = "FORECAST "
            draw.text((MARGIN + 6 + pw, iy), badge, font=f_sans_b11, fill=TAG_COLORS["FORECAST"])
            bw, _ = text_size(draw, badge, f_sans_b11)
        else:
            bw = 0

        # Source on right in muted ink, headline on left
        src_txt = "(" + source + ")"
        sw, _ = text_size(draw, src_txt, f_sans_11)
        max_hl_w = also_w - 14 - pw - bw - sw - 6
        hl_w, _ = text_size(draw, headline, f_sans_11)
        if hl_w > max_hl_w:
            raise ValueError("Item " + str(num) + " overflow: " + str(hl_w) + ">" + str(max_hl_w) + " " + headline)
        draw.text((MARGIN + 6 + pw + bw, iy), headline, font=f_sans_11, fill=INK)
        draw.text((MARGIN + also_w - 6 - sw, iy), src_txt, font=f_sans_11, fill=MUTED)
        iy += 12.5

    # Section 10 panel: World map
    mx = MARGIN + also_w + map_gap
    draw.rectangle([mx, y, mx + map_w, y + mid_h], fill=PAPER_ALT, outline=RULE_LIGHT)
    draw.rectangle([mx, y, mx + map_w, y + 17], fill=NAVY)
    draw.text((mx + 7, y + 2), "WHERE IT HAPPENED (STORIES 1–15)", font=f_sec_hdr, fill=WHITE)

    draw_world_map(draw, mx + 6, y + 20, map_w - 12, 173)
    map_note = "Numbered red pins show leads (1–3) and illustrated briefs (4–15)."
    draw_wrapped(draw, mx + 6, y + 196, map_w - 12, map_note, f_sans_11, MUTED, 11, max_lines=2)

    y += mid_h + 4

    # 11. Red-bordered "Date check" footer box
    date_h = 46
    draw.rectangle([MARGIN, y, WIDTH - MARGIN, y + date_h], fill=DATE_BOX_BG, outline=RED, width=2)
    date_prefix = "DATE CHECK: "
    draw.text((MARGIN + 7, y + 4), date_prefix, font=f_sans_b11, fill=RED)
    dpw, _ = text_size(draw, date_prefix, f_sans_b11)
    date_text = (
        "Every story on this page happened or was first reported on Wednesday 25 November 2026. "
        "Earlier stories deliberately omitted: COP31 ended without a deal (Sun 22 Nov); "
        "BepiColombo reached Mercury (Sat 21 Nov); Gaza strike on Hamas security chief (Tue 24 Nov); "
        "Senegal AFCON title restored (Tue 24 Nov); Real Madrid 5-1 PSV (Tue 24 Nov)."
    )
    # Render first line after prefix, remaining lines full width
    words = date_text.split()
    first_line = ""
    rest_idx = 0
    for i, w_tok in enumerate(words):
        cand = w_tok if not first_line else first_line + " " + w_tok
        cw, _ = text_size(draw, cand, f_sans_11)
        if cw <= CONTENT_W - 14 - dpw:
            first_line = cand
            rest_idx = i + 1
        else:
            break
    draw.text((MARGIN + 7 + dpw, y + 4), first_line, font=f_sans_11, fill=INK)
    rest_text = " ".join(words[rest_idx:])
    draw_wrapped(draw, MARGIN + 7, y + 17, CONTENT_W - 14, rest_text, f_sans_11, INK, 13, max_lines=2)
    y += date_h + 3

    # 12. Sources line & certainty legend
    sources_line = (
        "SOURCES: Horizon 25 Nov briefing, Australian PM office treaty page, One Turn 25 Nov, "
        "PANA, PINA, Reuters, BBC, IRIB, UN News, Lowy Institute, Ofgem, INDEC."
    )
    draw_wrapped(draw, MARGIN + 2, y, CONTENT_W - 4, sources_line, f_sans_11, MUTED, 12, max_lines=1)
    y += 13
    legend_line = (
        "CERTAINTY TAGS:  REPORTED = wires confirm it  |  CLAIM = one side's account  |  "
        "FORECAST = still to happen  |  PENDING = not settled  (Items 16–31 REPORTED unless tagged)."
    )
    draw_wrapped(draw, MARGIN + 2, y, CONTENT_W - 4, legend_line, f_sans_11, INK, 12, max_lines=1)
    y += 13

    # 13. Navy bottom strip
    bot_h = 20
    draw.rectangle([MARGIN, y, WIDTH - MARGIN, y + bot_h], fill=NAVY)
    draw.text((MARGIN + 8, y + 3), "THE WORLD ON ONE PAGE", font=f_strip, fill=WHITE)
    right_bot = "WEDNESDAY 25 NOVEMBER 2026  ·  ONE PAGE"
    rbw, _ = text_size(draw, right_bot, f_strip)
    draw.text((WIDTH - MARGIN - 8 - rbw, y + 3), right_bot, font=f_strip, fill=WHITE)
    y += bot_h

    if y > HEIGHT - 2:
        raise ValueError("Page overflowed HEIGHT: y=" + str(y))

    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    render()
