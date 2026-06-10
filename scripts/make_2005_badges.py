#!/usr/bin/env python3
"""Generate 2003-2007 web-standards-era assets into public/standards/.

The 80x15 two-segment buttons are in the style of Jeremy Hedley's
"antipixel" badges, the defining footer ornament of the era.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent.parent / "public" / "standards"
OUT.mkdir(parents=True, exist_ok=True)

FONTS = "/System/Library/Fonts/Supplemental"


def tiny_font():
    for name in ("Verdana Bold", "Tahoma Bold", "Arial Bold"):
        try:
            return ImageFont.truetype(f"{FONTS}/{name}.ttf", 8)
        except OSError:
            continue
    return ImageFont.load_default()


def antipixel(filename, left_text, right_text, left_bg, right_bg,
              left_fg="#FFFFFF", right_fg="#FFFFFF"):
    """Classic 80x15 two-segment badge: 1px dark border, divided color fields."""
    w, h = 80, 15
    img = Image.new("RGB", (w, h), "#666666")
    d = ImageDraw.Draw(img)
    f = tiny_font()
    lw = d.textlength(left_text, font=f)
    split = int(lw) + 8  # left field width: text + padding
    d.rectangle([1, 1, split, h - 2], fill=left_bg)
    d.rectangle([split + 1, 1, w - 2, h - 2], fill=right_bg)
    d.text((5, 3), left_text, font=f, fill=left_fg)
    rw = d.textlength(right_text, font=f)
    d.text((split + 1 + (w - split - 2 - rw) / 2, 3), right_text, font=f, fill=right_fg)
    img.save(OUT / filename)
    print(f"wrote {filename}")


def xml_chiclet():
    """The little orange XML button (c. 2003)."""
    w, h = 36, 14
    img = Image.new("RGB", (w, h), "#995500")
    d = ImageDraw.Draw(img)
    d.rectangle([1, 1, w - 2, h - 2], fill="#FF6600")
    d.line([(1, 1), (w - 2, 1)], fill="#FF9944")
    d.line([(1, 1), (1, h - 2)], fill="#FF9944")
    f = tiny_font()
    tw = d.textlength("XML", font=f)
    d.text(((w - tw) / 2, 2), "XML", font=f, fill="#FFFFFF")
    img.save(OUT / "xml.gif")
    print("wrote xml.gif")


def feed_icon():
    """Standard RSS square icon, 14x14, orange with dot and arcs."""
    s = 14
    img = Image.new("RGB", (s, s), "#FF6600")
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, s - 1, s - 1], outline="#CC4400")
    d.ellipse([2, 9, 5, 12], fill="#FFFFFF")
    for r in (5, 9):
        d.arc([2 - r, 9 - r + 3, 2 + r, 9 + r + 3], start=270, end=360,
              fill="#FFFFFF", width=2)
    img.save(OUT / "feed.gif")
    print("wrote feed.gif")


if __name__ == "__main__":
    antipixel("xhtml.gif", "W3C", "XHTML 1.0", "#365588", "#33A3D6")
    antipixel("css.gif", "W3C", "CSS", "#365588", "#FF9900")
    antipixel("rss.gif", "RSS", "2.0", "#FF6600", "#888888")
    antipixel("firefox.gif", "GET", "FIREFOX", "#333333", "#CC5500")
    antipixel("cc.gif", "CC", "SOME RIGHTS", "#000000", "#AAAAAA",
              right_fg="#000000")
    antipixel("coffee.gif", "POWERED BY", "COFFEE", "#553311", "#996633")
    antipixel("dux.gif", "DU", "XIANG.COM", "#B32D00", "#777777")
    xml_chiclet()
    feed_icon()
    print(f"\nAll assets in {OUT}")
