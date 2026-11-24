#!/usr/bin/env python3
"""Render the front page for Tuesday 24 November 2026.

Deterministic PIL renderer: same input, same pixels, every run.
Draws a newspaper front page summarising the day's world news.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 234)
INK = (18, 18, 18)
RULE = (60, 60, 60)
ACCENT = (158, 32, 28)
MUTED = (96, 90, 80)
SEA_DARK = (24, 52, 84)
SEA = (38, 84, 128)
SKY = (214, 228, 238)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_lines(draw, text, fnt, width):
    """Greedy word wrap measured with the real font."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, width, text, fnt, fill=INK, leading=None):
    lines = fit_lines(draw, text, fnt, width)
    lh = leading or int(fnt.size * 1.35)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def headline(draw, x, y, width, text, fnt, fill=INK, leading=None):
    lines = fit_lines(draw, text, fnt, width)
    lh = leading or int(fnt.size * 1.08)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def rule(draw, x, y, width, weight=2, fill=RULE):
    draw.rectangle([x, y, x + width, y + weight - 1], fill=fill)


def draw_sea_scene(d, x, y, w, h):
    """Flat illustration: a warship struck at sea off Libya."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    # sun
    d.ellipse([x + w - 110, y + 22, x + w - 46, y + 86], fill=(238, 196, 90))
    # distant coast
    d.polygon([(x, y + h * 0.52), (x + w * 0.30, y + h * 0.44),
               (x + w * 0.55, y + h * 0.52), (x + w, y + h * 0.47),
               (x + w, y + h * 0.56), (x, y + h * 0.56)], fill=(150, 158, 140))
    # sea
    d.rectangle([x, y + int(h * 0.55), x + w, y + h], fill=SEA)
    for i, yy in enumerate((0.62, 0.72, 0.83, 0.93)):
        d.line([x + 12, y + int(h * yy), x + w - 12, y + int(h * yy)],
               fill=(120, 165, 205), width=2)
    # warship silhouette (hull + superstructure), listing slightly
    hx, hy, hw = x + int(w * 0.16), y + int(h * 0.60), int(w * 0.52)
    d.polygon([(hx, hy), (hx + hw, hy), (hx + hw - 26, hy + 34),
               (hx + 18, hy + 34)], fill=(28, 34, 44))
    d.rectangle([hx + 60, hy - 46, hx + 150, hy], fill=(28, 34, 44))
    d.rectangle([hx + 96, hy - 72, hx + 116, hy - 46], fill=(28, 34, 44))
    d.rectangle([hx + 104, hy - 92, hx + 108, hy - 72], fill=(28, 34, 44))
    # explosion burst above the bow
    ex, ey = hx + hw - 40, hy - 30
    for r, col in ((64, (232, 122, 30)), (44, (244, 178, 60)), (24, (252, 226, 120))):
        pts = []
        for k in range(12):
            import math
            ang = k * math.pi / 6
            rr = r if k % 2 == 0 else r * 0.55
            pts.append((ex + rr * math.cos(ang), ey + rr * math.sin(ang)))
        d.polygon(pts, fill=col)
    # smoke
    for cx, cy, cr in ((ex - 52, ey - 46, 20), (ex - 30, ey - 66, 26),
                       (ex + 6, ey - 58, 18)):
        d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(90, 90, 92))
    # small drone boats
    for bx in (int(w * 0.78), int(w * 0.88)):
        d.polygon([(x + bx, y + int(h * 0.80)), (x + bx + 46, y + int(h * 0.80)),
                   (x + bx + 38, y + int(h * 0.84)), (x + bx + 8, y + int(h * 0.84))],
                  fill=(20, 26, 34))
        d.line([x + bx + 10, y + int(h * 0.80), x + bx + 36, y + int(h * 0.80)],
               fill=(200, 210, 220), width=2)
    # caption bar
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(18, 18, 18))
    d.text((x + 10, y + h - 22),
           "A sea-drone strike off Benghazi, Libya — illustration",
           font=font(SANS, 13), fill=(235, 235, 230))


def draw_toll_chart(d, x, y, w, h):
    """Simple bar chart: reported Russian death toll, near 500,000."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 220))
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=1)
    bars = [("2022", 0.42), ("2023", 0.66), ("2024", 0.84), ("2025", 0.95),
            ("2026", 1.00)]
    bw = w // 7
    top = y + 54
    for i, (lbl, frac) in enumerate(bars):
        bx = x + 14 + i * (bw + 6)
        bh = int((y + h - 34 - top) * frac)
        d.rectangle([bx, y + h - 34 - bh, bx + bw, y + h - 34],
                    fill=ACCENT if i == 4 else (120, 110, 96))
        d.text((bx + 2, y + h - 28), lbl, font=font(SANS, 12), fill=INK)
    d.text((x + 12, y + 8), "REPORTED TOLL, CUMULATIVE",
           font=font(SANS_B, 13), fill=INK)
    d.text((x + 12, y + 28), "near 500,000 dead",
           font=font(SERIF_B, 19), fill=ACCENT)


def draw_chip_scene(d, x, y, w, h):
    """Flat illustration: a chip on a board, for the Nvidia story."""
    d.rectangle([x, y, x + w, y + h], fill=(26, 34, 46))
    # circuit traces
    for yy in (y + 30, y + h - 30):
        d.line([x + 16, yy, x + w - 16, yy], fill=(70, 110, 140), width=2)
    for xx in (x + 30, x + w - 30):
        d.line([xx, y + 16, xx, y + h - 16], fill=(70, 110, 140), width=2)
    # chip
    cx, cy, cw, ch = x + w // 2 - 74, y + h // 2 - 52, 148, 104
    for k in range(5):
        px = cx + 12 + k * 26
        d.line([px, cy - 14, px, cy], fill=(180, 190, 200), width=3)
        d.line([px, cy + ch, px, cy + ch + 14], fill=(180, 190, 200), width=3)
    d.rectangle([cx, cy, cx + cw, cy + ch], fill=(16, 120, 90))
    d.rectangle([cx, cy, cx + cw, cy + ch], outline=(200, 210, 215), width=2)
    d.rectangle([cx + 44, cy + 32, cx + cw - 44, cy + ch - 32],
                fill=(12, 84, 62))
    d.text((cx + 34, cy + 42), "NVDA", font=font(SANS_B, 22),
           fill=(235, 240, 235))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 40  # margin
    CW = W - 2 * M  # content width

    # ---- Masthead ----
    d.text((M, 14), "THE WORLD TODAY", font=font(SERIF_B, 68), fill=INK)
    d.text((M, 100), "TUESDAY, 24 NOVEMBER 2026", font=font(SANS_B, 22),
           fill=ACCENT)
    d.text((M, 128), "One day's world news — in one page  •  Price: free",
           font=font(SANS, 16), fill=MUTED)
    rule(d, M, 156, CW, 4)
    rule(d, M, 164, CW, 1)

    # ---- Lead story ----
    lx, ly, lw = M, 182, 600
    d.text((lx, ly), "WAR AT SEA  •  UKRAINE", font=font(SANS_B, 17),
           fill=ACCENT)
    y = headline(d, lx, ly + 28, lw,
                 "Ukraine sinks Russian warship off Libya",
                 font(SERIF_B, 46))
    y = para(d, lx, y + 10, lw,
             "Kyiv says seven sea drones struck a Russian naval base at "
             "Benghazi, destroying a Ka-27 helicopter and hitting the cargo "
             "ship MV Angara — a strike that carries the war far beyond "
             "Europe's shores.",
             font(SERIF, 19), leading=27)
    draw_sea_scene(d, lx, y + 12, lw, 190)
    y = y + 12 + 190 + 14
    lead_bottom = para(d, lx, y, lw,
                       "President Volodymyr Zelenskyy confirmed the operation "
                       "on Monday night. Moscow has not confirmed the loss.",
                       font(SERIF, 17), leading=24)

    # ---- Right column: toll story ----
    rx, rw = M + lw + 28, CW - lw - 28
    rule(d, rx, ly, rw, 1)
    d.text((rx, ly + 8), "THE TOLL", font=font(SANS_B, 17), fill=ACCENT)
    y2 = headline(d, rx, ly + 34, rw,
                  "Hacked data puts Russian death toll near 500,000",
                  font(SERIF_B, 27))
    y2 = para(d, rx, y2 + 8, rw,
              "German and Russian media analysing hacked Rosstat files put "
              "the number of Russian soldiers killed since February 2022 "
              "at close to half a million — far above official figures.",
              font(SERIF, 16), leading=23)
    draw_toll_chart(d, rx, y2 + 10, rw, 150)
    y2 = y2 + 10 + 150 + 12
    d.text((rx, y2), "— Reports, 24 November", font=font(SANS, 13),
           fill=MUTED)

    # ---- Second row: Nvidia ----
    sy = max(lead_bottom, y2) + 14
    rule(d, M, sy, CW, 2)
    d.text((M, sy + 10), "TECHNOLOGY  •  BUSINESS", font=font(SANS_B, 16),
           fill=ACCENT)
    y3 = headline(d, M, sy + 36, 620,
                  "Nvidia rehires Huang in stunning reversal after Trump push",
                  font(SERIF_B, 30))
    y3 = para(d, M, y3 + 8, 620,
              "Jensen Huang is back as chief executive days after his "
              "ouster, after President Trump pressed the board and Vice "
              "President JD Vance lobbied directors.",
              font(SERIF, 17), leading=24)
    draw_chip_scene(d, M + 648, sy + 36, CW - 648, 150)
    nv_bottom = max(y3, sy + 36 + 150)

    # ---- Briefs strip ----
    by = nv_bottom + 12
    rule(d, M, by, CW, 2)
    d.text((M, by + 10), "IN BRIEF", font=font(SANS_B, 16), fill=ACCENT)
    briefs = [
        ("SPACE", "Allies warn Russia may launch a nuclear space weapon "
                  "soon."),
        ("FOOTBALL", "2031 Women's World Cup: USA, Mexico, Costa Rica, "
                     "Jamaica."),
        ("CLIMATE", "COP31 talks collapse with no deal; EU rejects the "
                    "text."),
        ("RECALL", "Honda recalls 810,000 vehicles in the US over airbag "
                   "inflators."),
    ]
    bw = (CW - 3 * 20) // 4
    for i, (kicker, text) in enumerate(briefs):
        bx = M + i * (bw + 20)
        d.text((bx, by + 34), kicker, font=font(SANS_B, 14), fill=ACCENT)
        end = para(d, bx, by + 54, bw, text, font(SERIF, 12), leading=17)
        assert end <= 998, f"brief {kicker} overflows: ends {end}"

    # ---- Footer ----
    rule(d, M, 1000, CW, 1)
    d.text((M, 1006), "Sources: wire reports first published 24 November 2026  •  "
           "Illustrations drawn for this page",
           font=font(SANS, 12), fill=MUTED)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
