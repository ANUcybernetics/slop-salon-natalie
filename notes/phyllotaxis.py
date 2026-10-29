import math
import sys

import numpy as np
from PIL import Image, ImageDraw

seed = int(sys.argv[1])
out = sys.argv[2]
n_pts = int(sys.argv[3]) if len(sys.argv) > 3 else 2400
size = int(sys.argv[4]) if len(sys.argv) > 4 else 1000
dot_frac = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5

BG = (14, 12, 20)
PLUM = (92, 40, 120)
CREAM = (240, 226, 196)

rng = np.random.default_rng(seed)
eps = rng.uniform(-0.006, 0.006)
golden_turn = 1 - 1 / ((1 + 5 ** 0.5) / 2)
turn = golden_turn + eps

SS = 2
S = size * SS
R = S * 0.47
cx = cy = S / 2
spacing = R * math.sqrt(math.pi / n_pts)
d = dot_frac * spacing

img = Image.new("RGB", (S, S), BG)
draw = ImageDraw.Draw(img)
for n in range(n_pts):
    r = R * math.sqrt((n + 0.5) / n_pts)
    th = 2 * math.pi * turn * n
    x = cx + r * math.cos(th)
    y = cy + r * math.sin(th)
    u = n / n_pts
    col = tuple(int(a + (b - a) * u) for a, b in zip(PLUM, CREAM))
    draw.ellipse([x - d, y - d, x + d, y + d], fill=col)

img.resize((size, size), Image.LANCZOS).save(out)
print(f"seed {seed} eps {eps:.5f} turn {turn:.6f} -> {out}")
