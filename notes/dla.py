import math
import random
import sys

from PIL import Image, ImageDraw

seed = int(sys.argv[1])
out = sys.argv[2]
particles = int(sys.argv[3]) if len(sys.argv) > 3 else 3000
size = int(sys.argv[4]) if len(sys.argv) > 4 else 1000

G = 400
C = G // 2
SS = 2
BG = (14, 12, 20)
PLUM = (92, 40, 120)
CREAM = (240, 226, 196)
DIRS = (1, -1, G, -G)

rnd = random.Random(seed)
occ = bytearray(G * G)
occ[C * G + C] = 1
pts = [(C, C)]
rad = 1.0


def launch():
    th = rnd.uniform(0, 2 * math.pi)
    r = rad + 4
    return int(C + r * math.cos(th)), int(C + r * math.sin(th))


while len(pts) < particles:
    x, y = launch()
    p = y * G + x
    kill2 = (rad + 40) ** 2
    while True:
        p += DIRS[rnd.getrandbits(2)]
        x, y = p % G, p // G
        dx, dy = x - C, y - C
        if dx * dx + dy * dy > kill2:
            break
        if occ[p + 1] or occ[p - 1] or occ[p + G] or occ[p - G]:
            occ[p] = 1
            pts.append((x, y))
            rad = max(rad, math.hypot(dx, dy))
            break

S = size * SS
k = S / G
r = 0.62 * k
img = Image.new("RGB", (S, S), BG)
draw = ImageDraw.Draw(img)
n = len(pts)
for i, (x, y) in enumerate(pts):
    u = i / (n - 1)
    col = tuple(int(a + (b - a) * u) for a, b in zip(PLUM, CREAM))
    cx, cy = (x + 0.5) * k, (y + 0.5) * k
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)

img.resize((size, size), Image.LANCZOS).save(out)
print(f"seed {seed} particles {n} radius {rad:.1f} -> {out}")
