import sys
import numpy as np
from PIL import Image

seed = int(sys.argv[1])
out = sys.argv[2]
iters = int(sys.argv[3]) if len(sys.argv) > 3 else 400
size = int(sys.argv[4]) if len(sys.argv) > 4 else 1000

rng = np.random.default_rng(seed)
a, b, c, d = rng.uniform(-2.0, 2.0, 4)

P = 200000
x = rng.uniform(-0.1, 0.1, P)
y = rng.uniform(-0.1, 0.1, P)

for _ in range(20):
    x, y = np.sin(a * y) + c * np.cos(a * x), np.sin(b * x) + d * np.cos(b * y)

pts = []
for _ in range(60):
    x, y = np.sin(a * y) + c * np.cos(a * x), np.sin(b * x) + d * np.cos(b * y)
    pts.append(np.concatenate([x, y]))
pts = np.concatenate(pts)
lo, hi = np.percentile(pts, 0.05), np.percentile(pts, 99.95)
pad = 0.05 * (hi - lo)
lo, hi = min(lo, hi) - pad, max(lo, hi) + pad
H = np.zeros((size, size), dtype=np.float64)
for _ in range(iters):
    x, y = np.sin(a * y) + c * np.cos(a * x), np.sin(b * x) + d * np.cos(b * y)
    ix = ((x - lo) / (hi - lo) * size).astype(np.int64)
    iy = ((y - lo) / (hi - lo) * size).astype(np.int64)
    ok = (ix >= 0) & (ix < size) & (iy >= 0) & (iy < size)
    np.add.at(H, (iy[ok], ix[ok]), 1.0)

t = np.log1p(H)
t = t / t.max()
bg = np.array([14, 12, 20], float)
hot = np.array([236, 214, 170], float)
rgb = bg + (hot - bg) * t[..., None] ** 0.8
Image.fromarray(rgb.clip(0, 255).astype(np.uint8)).save(out)
print(f"a={a:.4f} b={b:.4f} c={c:.4f} d={d:.4f} hit_frac={(H > 0).mean():.3f}")
