#!/usr/bin/env python3
"""Build meme.png for make.fun's gta6-meme-x-01 bounty.

Composites the OFFICIAL make.fun ghost mark (downloaded from
https://make.fun/press/, mark-1024.png) into an AI-generated Vice City
gamer-room scene and letters the captions with PIL.

The ghost is cut out of its magenta disc by flood-filling the magenta
background from the disc's edge: everything the fill cannot reach (the
white ghost, its black outline, and the magenta star coin, which is
ringed by the ghost's black outline) is the character. It is pasted
into the scene at character size, sitting on the couch beside the
gamer, with a soft shadow so it lives in the room's light.
"""
from collections import deque
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
SIZE = 1080
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def ghost_cutout(mark: Image.Image) -> Image.Image:
    """Return the ghost + star coin as an RGBA cutout of the press mark."""
    rgb = mark.convert("RGB")
    w, h = rgb.size
    px = rgb.load()

    def is_magenta(p):
        r, g, b = p
        return r > 140 and b > 90 and g < 130 and (r - g) > 70

    # Flood fill the magenta disc background from seeds on a ring just
    # inside the disc's edge (the image corners are outside the disc).
    import math

    seen = bytearray(w * h)
    q = deque()
    cx, cy = w // 2, h // 2
    ring = min(w, h) // 2 - 112
    for deg in range(0, 360, 3):
        x = int(cx + ring * math.cos(math.radians(deg)))
        y = int(cy + ring * math.sin(math.radians(deg)))
        if is_magenta(px[x, y]):
            q.append((x, y))
    while q:
        x, y = q.popleft()
        i = y * w + x
        if seen[i]:
            continue
        seen[i] = 1
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx]:
                if is_magenta(px[nx, ny]) and (nx - cx) ** 2 + (ny - cy) ** 2 < (min(w, h) // 2) ** 2:
                    q.append((nx, ny))

    # The character is the connected region of not-background pixels that
    # holds the ghost's centre: the ghost, its outline, and the star coin
    # (whose magenta middle is ringed by the outline, so the background
    # fill never reached it). The disc's black border ring is a separate
    # region and drops away.
    keep = bytearray(w * h)
    q = deque([(cx, cy)])
    keep[cy * w + cx] = 1
    while q:
        x, y = q.popleft()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            i = ny * w + nx
            if 0 <= nx < w and 0 <= ny < h and not keep[i] and not seen[i]:
                keep[i] = 1
                q.append((nx, ny))

    alpha = Image.new("L", (w, h), 0)
    ap = alpha.load()
    for y in range(h):
        for x in range(w):
            if keep[y * w + x]:
                ap[x, y] = 255
    alpha = alpha.filter(ImageFilter.GaussianBlur(1.2))
    out = rgb.convert("RGBA")
    out.putalpha(alpha)
    bbox = alpha.getbbox()
    return out.crop(bbox)


def fit_font(text, max_width, start):
    size = start
    while size > 10:
        f = ImageFont.truetype(FONT_PATH, size)
        if f.getlength(text) <= max_width:
            return f
        size -= 2
    return ImageFont.truetype(FONT_PATH, 10)


def caption(draw, lines, y_top, start_size, max_width=SIZE - 60, gap=6):
    y = y_top
    for line in lines:
        f = fit_font(line, max_width, start_size)
        w = f.getlength(line)
        x = (SIZE - w) / 2
        draw.text((x, y), line, font=f, fill="white",
                  stroke_width=max(3, f.size // 11), stroke_fill="black")
        y += f.size + gap
    return y


def main():
    base = Image.open(ASSETS / "media-generation-gta6-meme-base-0-79774b16-4720-4e63-b716-0659c39989e9.png")
    base = base.convert("RGB").resize((SIZE, SIZE), Image.LANCZOS)
    canvas = base.convert("RGBA")

    ghost = ghost_cutout(Image.open(ASSETS / "mark-1024.png"))
    gh = 445
    gw = int(ghost.width * gh / ghost.height)
    ghost = ghost.resize((gw, gh), Image.LANCZOS)
    gx, gy = 26, 472  # sitting on the couch's left arm, in the room

    shadow = Image.new("RGBA", (gw, gh), (0, 0, 0, 0))
    sh_alpha = ghost.split()[3].point(lambda a: int(a * 0.45))
    shadow.putalpha(sh_alpha)
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    canvas.alpha_composite(shadow, (gx + 14, gy + 18))
    canvas.alpha_composite(ghost, (gx, gy))

    img = canvas.convert("RGB")
    draw = ImageDraw.Draw(img)

    # "99%" stuck on the TV's download bar.
    f99 = ImageFont.truetype(FONT_PATH, 54)
    draw.text((838, 428), "99%", font=f99, fill="white",
              stroke_width=5, stroke_fill="black")

    caption(draw, ["WAITED 13 YEARS", "FOR GTA 6"], 26, 96)
    caption(draw, ["MY AI AGENT ALREADY WON REAL MONEY",
                   "ON MAKE.FUN BEFORE IT DOWNLOADED"], 928, 56)

    img.save(HERE / "meme.png", optimize=True)
    print("meme.png", img.size)


if __name__ == "__main__":
    main()
