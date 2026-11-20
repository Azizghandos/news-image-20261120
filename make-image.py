#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news front page (1024x1024 PNG).

Editorial infographic drawn with Pillow only: flat colours, simple vector-style
icons, crisp text. Deterministic: same input always writes the same bytes.
Run: python3 make-image.py  -> writes entry.png next to this file.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
NAVY = (20, 33, 61)
NAVY2 = (28, 48, 88)
RED = (193, 39, 45)
GOLD = (217, 164, 65)
INK = (26, 26, 26)
MUTED = (90, 90, 90)
CARD = (255, 255, 255)
LINE = (200, 192, 175)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
def font(bold, size):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(FONT_DIR + name, size)

def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text_block(draw, x, y, lines, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y

def card(draw, x, y, w, h, accent):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD,
                           outline=LINE, width=2)
    draw.rectangle([x, y, x + 8, y + h], fill=accent)

# --- icons (flat, drawn with primitives) -----------------------------------
def icon_scales(d, cx, cy, s, col):
    # pole, beam, two pans, base
    d.line([(cx, cy - 0.55 * s), (cx, cy + 0.55 * s)], fill=col, width=max(4, s // 18))
    d.line([(cx - 0.55 * s, cy - 0.45 * s), (cx + 0.55 * s, cy - 0.45 * s)],
           fill=col, width=max(4, s // 18))
    d.ellipse([cx - 0.09 * s, cy - 0.62 * s, cx + 0.09 * s, cy - 0.44 * s], fill=col)
    for sx in (-1, 1):
        px = cx + sx * 0.55 * s
        d.line([(px, cy - 0.45 * s), (px - 0.28 * s, cy + 0.05 * s)], fill=col, width=max(3, s // 24))
        d.line([(px, cy - 0.45 * s), (px + 0.28 * s, cy + 0.05 * s)], fill=col, width=max(3, s // 24))
        d.polygon([(px - 0.30 * s, cy + 0.05 * s), (px + 0.30 * s, cy + 0.05 * s),
                   (px, cy + 0.32 * s)], fill=col)
    d.line([(cx - 0.35 * s, cy + 0.55 * s), (cx + 0.35 * s, cy + 0.55 * s)],
           fill=col, width=max(4, s // 16))

def icon_flags(d, x, y, w, h):
    # three abstract national flags: US, China, Russia
    fw = w // 3 - 8
    # US: red/white stripes + blue corner
    fx = x
    for i in range(5):
        d.rectangle([fx, y + i * h // 5, fx + fw, y + (i + 1) * h // 5],
                    fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    d.rectangle([fx, y, fx + fw // 2, y + h // 2], fill=NAVY2)
    # China: red with gold stars
    fx = x + w // 3
    d.rectangle([fx, y, fx + fw, y + h], fill=(222, 41, 16))
    for sx, sy in [(0.22, 0.22), (0.42, 0.16), (0.48, 0.34), (0.40, 0.48), (0.22, 0.42)]:
        d.ellipse([fx + sx * fw - 3, y + sy * h - 3, fx + sx * fw + 3, y + sy * h + 3],
                  fill=GOLD)
    # Russia: white / blue / red horizontal
    fx = x + 2 * w // 3
    for i, c in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        d.rectangle([fx, y + i * h // 3, fx + fw, y + (i + 1) * h // 3], fill=c)
    for fx in (x, x + w // 3, x + 2 * w // 3):
        d.rectangle([fx, y, fx + fw, y + h], outline=LINE, width=2)

def icon_skyline(d, x, y, w, h):
    # dark skyline + orange blast star
    import random
    random.seed(7)
    base = y + h
    bx = x
    while bx < x + w - 18:
        bw = random.randint(16, 30)
        bh = random.randint(int(h * 0.35), int(h * 0.8))
        d.rectangle([bx, base - bh, bx + bw, base], fill=NAVY2)
        bx += bw + 4
    cx, cy = x + w - 34, y + 22
    pts = []
    for i in range(16):
        r = 26 if i % 2 == 0 else 11
        import math
        a = math.pi * i / 8
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=(255, 140, 0))
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=RED)

def icon_tower(d, x, y, w, h):
    # Riyadh tower: tall tapering tower + blast cloud
    d.polygon([(x + w * 0.35, y + h), (x + w * 0.42, y), (x + w * 0.58, y),
               (x + w * 0.65, y + h)], fill=NAVY2)
    for i in range(4):
        wy = y + 14 + i * (h - 28) // 4
        d.rectangle([x + w * 0.44, wy, x + w * 0.56, wy + 5], fill=GOLD)
    d.ellipse([x + w * 0.62, y + 4, x + w * 0.98, y + 40], fill=(255, 140, 0))
    d.ellipse([x + w * 0.70, y + 12, x + w * 0.90, y + 32], fill=RED)

def icon_chart(d, x, y, w, h):
    pts = [(x, y + h * 0.15), (x + w * 0.25, y + h * 0.30),
           (x + w * 0.45, y + h * 0.25), (x + w * 0.65, y + h * 0.55),
           (x + w * 0.85, y + h * 0.80), (x + w, y + h * 0.95)]
    d.line(pts, fill=RED, width=7, joint="curve")
    d.polygon([(x + w - 14, y + h * 0.95 - 12), (x + w + 2, y + h * 0.95 - 2),
               (x + w - 2, y + h * 0.95 + 12)], fill=RED)
    d.line([(x, y + h), (x + w, y + h)], fill=MUTED, width=3)
    d.line([(x, y), (x, y + h)], fill=MUTED, width=3)

# --- page -------------------------------------------------------------------
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
d.rectangle([6, 6, W - 7, H - 7], outline=NAVY, width=4)

# masthead
d.rectangle([10, 10, W - 11, 148], fill=NAVY)
d.text((34, 26), "THE WORLD", font=font(True, 66), fill=(255, 255, 255))
d.text((34, 104), "IN ONE PICTURE", font=font(True, 26), fill=GOLD)
d.text((640, 34), "FRIDAY", font=font(True, 40), fill=(255, 255, 255))
d.text((640, 82), "20 NOVEMBER 2026", font=font(True, 30), fill=GOLD)
d.text((34, 158), "THE DAY'S NEWS AT A GLANCE  ·  SIX STORIES AND MORE",
       font=font(True, 21), fill=MUTED)

# lead story: ICJ genocide ruling
card(d, 28, 188, 968, 196, RED)
icon_scales(d, 118, 286, 95, NAVY)
d.text((212, 206), "THE HAGUE  ·  JUSTICE", font=font(True, 20), fill=RED)
hl = wrap(d, "WORLD COURT RULES MYANMAR COMMITTED GENOCIDE",
          font(True, 38), 740)
text_block(d, 212, 232, hl, font(True, 38), NAVY, 44)
sub = wrap(d, "The ICJ's first genocide ruling against a state, over the "
              "Rohingya in 2017. Britain expels Myanmar's military attaché.",
           font(False, 22), 740)
text_block(d, 212, 232 + 44 * len(hl) + 8, sub, font(False, 22), INK, 26)

def story_card(x, y, w, h, accent, icon, kicker, kcol, headline, sub):
    card(d, x, y, w, h, accent)
    icon(x + 24, y + 16)
    d.text((x + 24, y + 82), kicker, font=font(True, 18), fill=kcol)
    hl = wrap(d, headline, font(True, 28), w - 48)
    hy = text_block(d, x + 24, y + 108, hl, font(True, 28), NAVY, 33)
    sub_lines = wrap(d, sub, font(False, 19), w - 48)
    text_block(d, x + 24, hy + 6, sub_lines, font(False, 19), INK, 24)

# row 2
story_card(28, 398, 478, 228, NAVY2,
           lambda ix, iy: icon_flags(d, ix, iy, 150, 54),
           "SHENZHEN  ·  DIPLOMACY", NAVY2,
           "TRUMP, XI & PUTIN MEET IN SHENZHEN",
           "First three-way summit ends with a joint peace declaration.")
story_card(518, 398, 478, 228, RED,
           lambda ix, iy: icon_skyline(d, ix, iy, 200, 54),
           "KYIV  ·  WAR IN UKRAINE", RED,
           "RUSSIA STRIKES KYIV OVERNIGHT",
           "8 killed as bridges are hit; Poland reports its airspace violated.")

# row 3
story_card(28, 640, 478, 228, RED,
           lambda ix, iy: icon_tower(d, ix, iy, 130, 54),
           "RIYADH  ·  MIDDLE EAST", RED,
           "HOUTHI MISSILE HITS RIYADH TOWER",
           "Saudi wealth-fund tower damaged in the financial district.")
story_card(518, 640, 478, 228, NAVY2,
           lambda ix, iy: icon_chart(d, ix, iy, 150, 54),
           "MARKETS  ·  ECONOMY", NAVY2,
           "MARKETS TUMBLE ON AI FEARS",
           "Nikkei −4.8%, S&P 500 −2% for a fifth day; Anthropic debuts +17%.")

# bottom strip
d.rectangle([10, 882, W - 11, 1014], fill=NAVY)
d.text((34, 898), "ALSO TODAY", font=font(True, 20), fill=GOLD)
b1 = wrap(d, "COP31 draft drops the call to phase out fossil fuels  ·  Antalya",
          font(False, 22), 940)
text_block(d, 34, 928, b1, font(False, 22), (255, 255, 255), 28)
b2 = wrap(d, "Kenya discharges its last Ebola patient  ·  EU–UK summit in Brussels",
          font(False, 22), 940)
text_block(d, 34, 928 + 28 * len(b1) + 2, b2, font(False, 22),
           (255, 255, 255), 28)

img.save("entry.png", format="PNG", optimize=True)
print("wrote entry.png", img.size)
