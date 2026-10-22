import sys

import numpy as np
from PIL import Image

SEED = int(sys.argv[1])
OUT = sys.argv[2]
SHARP = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
RATIO_OVERRIDE = float(sys.argv[4]) if len(sys.argv) > 4 else None
OFFSET_OVERRIDE = float(sys.argv[5]) if len(sys.argv) > 5 else None
SIZE = 1000

rng = np.random.default_rng(SEED)
c1 = np.array([0.5, 0.5]) + rng.uniform(-0.1, 0.1, 2)
theta = rng.uniform(0, 2 * np.pi)
offset = rng.uniform(0.03, 0.09)
if OFFSET_OVERRIDE is not None:
    offset = OFFSET_OVERRIDE
c2 = c1 + offset * np.array([np.cos(theta), np.sin(theta)])
k1 = rng.uniform(150, 230)
ratio = rng.uniform(1.02, 1.06)
if RATIO_OVERRIDE is not None:
    ratio = RATIO_OVERRIDE
k2 = k1 * ratio

ax = np.linspace(0, 1, SIZE)
X, Y = np.meshgrid(ax, ax)
r1 = (X - c1[0]) ** 2 + (Y - c1[1]) ** 2
r2 = (X - c2[0]) ** 2 + (Y - c2[1]) ** 2
s = 0.5 * (np.cos(k1 * r1) + np.cos(k2 * r2))
v = 0.5 + 0.5 * np.tanh(SHARP * 2.0 * s)

STOPS = np.array([0.0, 0.5, 1.0])
RGB = np.array([[14, 12, 20], [104, 58, 116], [240, 226, 196]], dtype=float)
img = np.stack([np.interp(v, STOPS, RGB[:, c]) for c in range(3)], axis=-1).astype(np.uint8)
Image.fromarray(img, "RGB").save(OUT)
print(f"seed={SEED} k1={k1:.1f} k2={k2:.1f} c1={c1.round(3)} c2={c2.round(3)} out={OUT}")
