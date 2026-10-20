import math
import sys

import numpy as np
from PIL import Image, ImageDraw

SEED = int(sys.argv[1])
OUT = sys.argv[2]
GRID = int(sys.argv[3]) if len(sys.argv) > 3 else 16
GAIN = float(sys.argv[4]) if len(sys.argv) > 4 else 2.0
EQUALISE = len(sys.argv) > 5 and sys.argv[5] == "equalise"
SIZE = 1000
STEPS = 260
STEP = 0.0045

rng = np.random.default_rng(SEED)
waves = []
for _ in range(4):
    k = rng.normal(0, 4.0, size=2)
    phi = rng.uniform(0, 2 * math.pi)
    amp = rng.uniform(0.5, 1.0)
    waves.append((k, phi, amp))


def angle(x, y):
    return GAIN * sum(a * math.sin(k[0] * x + k[1] * y + p) for k, p, a in waves)


def trace(x, y, sign):
    pts = [(x, y)]
    for _ in range(STEPS):
        t = angle(x, y)
        x += sign * STEP * math.cos(t)
        y += sign * STEP * math.sin(t)
        if not (0 <= x <= 1 and 0 <= y <= 1):
            break
        pts.append((x, y))
    return pts


LO = np.array([24, 18, 40])
HI = np.array([240, 216, 168])


def unit(t):
    return 0.5 + 0.5 * math.cos(t)


if EQUALISE:
    lattice = np.sort(
        np.array([unit(angle((i + 0.5) / 200, (j + 0.5) / 200)) for i in range(200) for j in range(200)])
    )


def colour(t):
    u = unit(t)
    if EQUALISE:
        u = np.searchsorted(lattice, u) / len(lattice)
    return tuple(int(v) for v in LO + (HI - LO) * u)


img = Image.new("RGB", (SIZE, SIZE), (14, 12, 20))
draw = ImageDraw.Draw(img)
segments = 0
for i in range(GRID):
    for j in range(GRID):
        x0 = (i + 0.5) / GRID
        y0 = (j + 0.5) / GRID
        for sign in (1, -1):
            pts = trace(x0, y0, sign)
            for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
                draw.line(
                    [(xa * SIZE, ya * SIZE), (xb * SIZE, yb * SIZE)],
                    fill=colour(angle(xa, ya)),
                    width=2,
                )
                segments += 1

img.save(OUT)
print(f"seed={SEED} segments={segments} out={OUT}")
