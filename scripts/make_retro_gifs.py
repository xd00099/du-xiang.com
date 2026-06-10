#!/usr/bin/env python3
"""Generate authentic 1999-style GIF assets into public/retro/."""

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent.parent / "public" / "retro"
OUT.mkdir(parents=True, exist_ok=True)

FONTS = "/System/Library/Fonts/Supplemental"


def font(name, size):
    try:
        return ImageFont.truetype(f"{FONTS}/{name}.ttf", size)
    except OSError:
        return ImageFont.load_default()


def save_gif(path, frames, duration=200, transparent=False):
    if transparent:
        pframes = []
        for f in frames:
            alpha = f.getchannel("A")
            mask = alpha.point(lambda a: 255 if a <= 128 else 0)
            p = f.convert("RGB").convert("P", palette=Image.ADAPTIVE, colors=255)
            p.paste(255, mask)
            pframes.append(p)
        pframes[0].save(
            path, save_all=True, append_images=pframes[1:], loop=0,
            duration=duration, transparency=255, disposal=2,
        )
    else:
        frames[0].save(
            path, save_all=True, append_images=frames[1:], loop=0, duration=duration,
        )
    print(f"wrote {path.name} ({len(frames)} frames)")


def bevel(draw, x0, y0, x1, y1, light="#FFFFFF", dark="#404040", w=2):
    """Win95-style raised bevel."""
    for i in range(w):
        draw.line([(x0 + i, y0 + i), (x1 - i, y0 + i)], fill=light)  # top
        draw.line([(x0 + i, y0 + i), (x0 + i, y1 - i)], fill=light)  # left
        draw.line([(x0 + i, y1 - i), (x1 - i, y1 - i)], fill=dark)   # bottom
        draw.line([(x1 - i, y0 + i), (x1 - i, y1 - i)], fill=dark)   # right


# ---------------------------------------------------------------- stars.gif
def make_stars():
    size = 256
    random.seed(1999)
    stars = [(random.randrange(size), random.randrange(size),
              random.choice(["#FFFFFF", "#FFFFCC", "#CCCCFF", "#AAAAAA"]))
             for _ in range(90)]
    big = random.sample(stars, 14)
    frames = []
    for phase in range(4):
        img = Image.new("RGB", (size, size), "#000022")
        d = ImageDraw.Draw(img)
        for i, (x, y, c) in enumerate(stars):
            tw = (i + phase) % 4
            if tw == 0:
                d.point((x, y), fill="#333355")
            else:
                d.point((x, y), fill=c)
        for i, (x, y, c) in enumerate(big):
            if (i + phase) % 2:
                d.line([(x - 2, y), (x + 2, y)], fill=c)
                d.line([(x, y - 2), (x, y + 2)], fill=c)
        frames.append(img)
    save_gif(OUT / "stars.gif", frames, duration=400)


# ---------------------------------------------------- construction.gif
def make_construction():
    w, h = 420, 54
    band = 12
    fnt = font("Arial Black", 21)
    frames = []
    for phase in range(2):
        img = Image.new("RGB", (w, h), "#000000")
        d = ImageDraw.Draw(img)
        off = phase * 8
        for band_y in (0, h - band):
            for x in range(-band, w + band, 16):
                d.polygon(
                    [(x + off, band_y), (x + 8 + off, band_y),
                     (x - 4 + off, band_y + band), (x - 12 + off, band_y + band)],
                    fill="#FFCC00",
                )
        txt = "UNDER CONSTRUCTION"
        color = "#FFFF00" if phase == 0 else "#FF9900"
        tw = d.textlength(txt, font=fnt)
        d.text(((w - tw) / 2, band + 5), txt, font=fnt, fill=color)
        frames.append(img)
    save_gif(OUT / "construction.gif", frames, duration=350)


# --------------------------------------------------------- divider.gif
def make_divider():
    w, h = 600, 10
    frames = []
    for phase in range(8):
        img = Image.new("RGB", (w, h))
        d = ImageDraw.Draw(img)
        for x in range(w):
            hue = ((x / w) + phase / 8) % 1.0
            d.line([(x, 0), (x, h)], fill=hsv(hue))
        frames.append(img)
    save_gif(OUT / "divider.gif", frames, duration=120)


def hsv(h, s=1.0, v=1.0):
    i = int(h * 6) % 6
    f = h * 6 - int(h * 6)
    p, q, t = v * (1 - s), v * (1 - f * s), v * (1 - (1 - f) * s)
    rgb = [(v, t, p), (q, v, p), (p, v, t), (p, q, v), (t, p, v), (v, p, q)][i]
    return tuple(int(c * 255) for c in rgb)


# ------------------------------------------------------------- new.gif
def make_new():
    w, h = 66, 32
    fnt = font("Arial Black", 16)
    frames = []
    for phase in range(2):
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        cx, cy = w / 2, h / 2
        pts = []
        for i in range(16):
            r = (min(w, h) / 2 - 1) if i % 2 == 0 else (min(w, h) / 4)
            a = math.pi * i / 8 + (0.2 if phase else 0)
            pts.append((cx + r * 1.9 * math.cos(a), cy + r * math.sin(a)))
        d.polygon(pts, fill="#FF0000" if phase == 0 else "#FFFF00")
        txt = "NEW!"
        tw = d.textlength(txt, font=fnt)
        d.text(((w - tw) / 2, cy - 10), txt, font=fnt,
               fill="#FFFF00" if phase == 0 else "#FF0000")
        frames.append(img)
    save_gif(OUT / "new.gif", frames, duration=400, transparent=True)


# ----------------------------------------------------------- email.gif
def make_email():
    w, h = 100, 40
    fnt = font("Arial Bold", 13)
    frames = []
    for phase in range(2):
        img = Image.new("RGB", (w, h), "#000022")
        d = ImageDraw.Draw(img)
        # envelope
        ex0, ey0, ex1, ey1 = 4, 8, 36, 32
        d.rectangle([ex0, ey0, ex1, ey1], fill="#FFFFFF", outline="#888888")
        flap = "#DDDDDD" if phase == 0 else "#FFFFCC"
        d.polygon([(ex0, ey0), (ex1, ey0), ((ex0 + ex1) / 2, ey0 + 14)],
                  fill=flap, outline="#888888")
        color = "#FFFF00" if phase == 0 else "#FF00FF"
        d.text((42, 6), "E-MAIL", font=fnt, fill=color)
        d.text((42, 21), "ME!!", font=fnt, fill=color)
        frames.append(img)
    save_gif(OUT / "email.gif", frames, duration=400)


# ------------------------------------------------------ counter digits
def make_digits():
    fnt = font("Courier New Bold", 24)
    for n in range(10):
        img = Image.new("RGB", (18, 28), "#000000")
        d = ImageDraw.Draw(img)
        d.rectangle([0, 0, 17, 27], outline="#003300")
        txt = str(n)
        tw = d.textlength(txt, font=fnt)
        d.text(((18 - tw) / 2, 0), txt, font=fnt, fill="#00FF00")
        for y in range(0, 28, 3):  # scanlines
            d.line([(1, y), (16, y)], fill="#001A00")
        d.text(((18 - tw) / 2, 0), txt, font=fnt, fill="#00FF00")
        img.save(OUT / f"digit{n}.gif")
    print("wrote digit0-9.gif")


# ----------------------------------------------------------- 88x31 badges
def badge_base(bg="#000000"):
    img = Image.new("RGB", (88, 31), bg)
    return img, ImageDraw.Draw(img)


def make_badges():
    # Netscape NOW!
    frames = []
    for phase in range(2):
        img, d = badge_base("#000044")
        bevel(d, 0, 0, 87, 30, "#6666AA", "#000022")
        d.text((6, 3), "Netscape", font=font("Times New Roman Bold", 14), fill="#FFFFFF")
        d.text((24, 16), "NOW!", font=font("Arial Black", 11),
               fill="#00FF00" if phase == 0 else "#88FF88")
        frames.append(img)
    save_gif(OUT / "netscape.gif", frames, duration=500)

    # Best viewed 800x600
    img, d = badge_base("#000000")
    bevel(d, 0, 0, 87, 30, "#888888", "#222222")
    d.text((9, 4), "BEST VIEWED", font=font("Arial Bold", 10), fill="#FFFFFF")
    d.text((17, 16), "800 x 600", font=font("Arial Bold", 10), fill="#FFFF00")
    img.save(OUT / "bestview.gif")
    print("wrote bestview.gif")

    # Made with Notepad
    img, d = badge_base("#C0C0C0")
    bevel(d, 0, 0, 87, 30, "#FFFFFF", "#404040")
    d.rectangle([6, 7, 20, 24], fill="#FFFFFF", outline="#000080")
    for y in (11, 14, 17, 20):
        d.line([(8, y), (18, y)], fill="#8888FF")
    d.text((25, 4), "made with", font=font("Arial", 9), fill="#000000")
    d.text((25, 14), "Notepad", font=font("Arial Bold", 11), fill="#000080")
    img.save(OUT / "notepad.gif")
    print("wrote notepad.gif")

    # Y2K READY
    frames = []
    for phase in range(2):
        img, d = badge_base("#000000")
        bevel(d, 0, 0, 87, 30, "#005500", "#001100")
        d.text((9, 2), "Y2K", font=font("Arial Black", 14),
               fill="#00FF00" if phase == 0 else "#FF0000")
        d.text((46, 6), "OK!", font=font("Arial Black", 12), fill="#FFFF00")
        d.text((9, 18), "compliant", font=font("Courier New Bold", 10), fill="#00CC00")
        frames.append(img)
    save_gif(OUT / "y2k.gif", frames, duration=600)

    # Valid HTML 3.2
    img, d = badge_base("#FFCC00")
    bevel(d, 0, 0, 87, 30, "#FFEE88", "#996600")
    d.text((8, 3), "VALID", font=font("Arial Black", 11), fill="#000000")
    d.text((8, 15), "HTML 3.2", font=font("Arial Black", 11), fill="#CC0000")
    img.save(OUT / "html32.gif")
    print("wrote html32.gif")

    # GeoCities-style "CYBER HOME" badge
    frames = []
    for phase in range(2):
        img, d = badge_base("#330066")
        bevel(d, 0, 0, 87, 30, "#9966FF", "#110022")
        d.text((7, 3), "DU's CYBER", font=font("Arial Bold", 11),
               fill="#FF00FF" if phase == 0 else "#00FFFF")
        d.text((22, 15), "HOME", font=font("Arial Black", 12),
               fill="#00FFFF" if phase == 0 else "#FF00FF")
        frames.append(img)
    save_gif(OUT / "cyberhome.gif", frames, duration=700)


# -------------------------------------------------------------- balls
def make_balls():
    for name, base in [("ball_red", (255, 0, 0)), ("ball_green", (0, 200, 0)),
                       ("ball_blue", (64, 64, 255)), ("ball_yellow", (255, 220, 0))]:
        frames = []
        for phase in range(3):
            img = Image.new("RGBA", (14, 14), (0, 0, 0, 0))
            d = ImageDraw.Draw(img)
            d.ellipse([1, 1, 12, 12], fill=base + (255,))
            d.ellipse([2, 2, 11, 11], outline=tuple(c // 2 for c in base) + (255,))
            hx = 4 + phase
            d.ellipse([hx, 3, hx + 3, 6], fill=(255, 255, 255, 230))
            frames.append(img)
        save_gif(OUT / f"{name}.gif", frames, duration=300, transparent=True)


# ------------------------------------------------------------ flame bar
def make_flames():
    w, h = 600, 18
    random.seed(42)
    frames = []
    for phase in range(3):
        img = Image.new("RGB", (w, h), "#000000")
        d = ImageDraw.Draw(img)
        for x in range(0, w, 4):
            fh = 6 + int(6 * abs(math.sin(x * 0.13 + phase * 2.1))) + random.randint(0, 4)
            for i, c in [(0, "#FF2200"), (2, "#FF8800"), (4, "#FFFF00")]:
                if fh - i > 0:
                    d.rectangle([x, h - (fh - i), x + 3, h], fill=c)
        frames.append(img)
    save_gif(OUT / "flames.gif", frames, duration=150)


if __name__ == "__main__":
    make_stars()
    make_construction()
    make_divider()
    make_new()
    make_email()
    make_digits()
    make_badges()
    make_balls()
    make_flames()
    print(f"\nAll assets in {OUT}")
