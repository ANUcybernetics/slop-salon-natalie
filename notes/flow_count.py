import math
import sys

import numpy as np

SEED = int(sys.argv[1])
BIN = float(sys.argv[2])
CX, CY = float(sys.argv[3]), float(sys.argv[4])
GRID = 16
GAIN = 2.0
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


count = 0
for i in range(GRID):
    for j in range(GRID):
        x0 = (i + 0.5) / GRID
        y0 = (j + 0.5) / GRID
        pts = trace(x0, y0, 1)[::-1][:-1] + trace(x0, y0, -1)
        if any(abs(x - CX) <= BIN / 2 and abs(y - CY) <= BIN / 2 for x, y in pts):
            count += 1

print(f"seed={SEED} bin={BIN} at=({CX},{CY}) lines={count} of {GRID * GRID}")
