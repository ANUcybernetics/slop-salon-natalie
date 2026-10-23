import random
import sys

from PIL import Image, ImageDraw

seed = int(sys.argv[1])
out = sys.argv[2]
n = int(sys.argv[3])
size = int(sys.argv[4])
SS = 2

BG = (14, 12, 20)
CREAM = (232, 216, 190)
PLUM = (100, 60, 120)

rng = random.Random(seed)
px = size * SS
t = px / n
w = t / 5
img = Image.new("RGB", (px, px), BG)
d = ImageDraw.Draw(img)


def arc(cx, cy, start, end, colour):
    r = t / 2
    d.arc((cx - r, cy - r, cx + r, cy + r), start, end, fill=colour, width=int(w))


for j in range(n):
    for i in range(n):
        x0, y0 = i * t, j * t
        colour = CREAM if rng.random() < 0.5 else PLUM
        if rng.random() < 0.5:
            arc(x0, y0, 0, 90, colour)
            arc(x0 + t, y0 + t, 180, 270, colour)
        else:
            arc(x0 + t, y0, 90, 180, colour)
            arc(x0, y0 + t, 270, 360, colour)

img.resize((size, size), Image.LANCZOS).save(out)
