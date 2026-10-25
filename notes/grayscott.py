import sys

import numpy as np
from PIL import Image

seed, out, steps, size = int(sys.argv[1]), sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
F = float(sys.argv[5]) if len(sys.argv) > 5 else 0.0545
K = float(sys.argv[6]) if len(sys.argv) > 6 else 0.062
N = 256
DU, DV = 0.16, 0.08

rng = np.random.default_rng(seed)
U = np.ones((N, N))
V = np.zeros((N, N))
for _ in range(14):
    x, y = rng.integers(0, N - 24, 2)
    s = int(rng.integers(8, 22))
    U[y:y + s, x:x + s] = 0.5
    V[y:y + s, x:x + s] = 0.25
U += rng.normal(0, 0.02, (N, N))
V += rng.normal(0, 0.02, (N, N))


def lap(A):
    return (
        0.2 * (np.roll(A, 1, 0) + np.roll(A, -1, 0) + np.roll(A, 1, 1) + np.roll(A, -1, 1))
        + 0.05 * (np.roll(np.roll(A, 1, 0), 1, 1) + np.roll(np.roll(A, 1, 0), -1, 1)
                  + np.roll(np.roll(A, -1, 0), 1, 1) + np.roll(np.roll(A, -1, 0), -1, 1))
        - A
    )


for _ in range(steps):
    uvv = U * V * V
    U += DU * lap(U) - uvv + F * (1 - U)
    V += DV * lap(V) + uvv - (F + K) * V

lo, hi = np.percentile(V, 1), np.percentile(V, 99)
t = np.clip((V - lo) / (hi - lo + 1e-9), 0, 1)
ground = np.array([14, 12, 20], float)
cream = np.array([236, 226, 200], float)
rgb = ground + (cream - ground) * t[..., None]
img = Image.fromarray(rgb.astype(np.uint8)).resize((size, size), Image.LANCZOS)
img.save(out)
print(f"seed {seed} F {F} K {K} steps {steps} V>0.1 fraction {(V > 0.1).mean():.3f} V mean {V.mean():.3f}")
