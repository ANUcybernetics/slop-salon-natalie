import sys
import numpy as np
from PIL import Image

seed = int(sys.argv[1])
out = sys.argv[2]
size = int(sys.argv[3]) if len(sys.argv) > 3 else 1000

S = 2 * size
rng = np.random.default_rng(seed)
freq = rng.uniform(1.0, 4.0, 4)
phase = rng.uniform(0, 2 * np.pi, 4)
damp = rng.uniform(0.002, 0.010, 4)
amp = rng.uniform(0.5, 1.0, 4)

T = 300.0
t = np.linspace(0, T, 3_000_000)
decay = [np.exp(-damp[i] * t) for i in range(4)]
x = amp[0] * np.sin(freq[0] * t + phase[0]) * decay[0] + amp[1] * np.sin(freq[1] * t + phase[1]) * decay[1]
y = amp[2] * np.sin(freq[2] * t + phase[2]) * decay[2] + amp[3] * np.sin(freq[3] * t + phase[3]) * decay[3]
m = max(np.abs(x).max(), np.abs(y).max())
x = x / m * 0.92
y = y / m * 0.92

px = ((x + 1) / 2 * (S - 1)).astype(int)
py = ((1 - (y + 1) / 2) * (S - 1)).astype(int)
idx = py * S + px

u = t / T
plum = np.array([150, 70, 140], float)
cream = np.array([240, 226, 196], float)
col = plum + (cream - plum) * u[:, None]

dens = np.bincount(idx, minlength=S * S).astype(float)
acc = np.stack([np.bincount(idx, weights=col[:, c], minlength=S * S) for c in range(3)], axis=-1)
mean = acc / np.maximum(dens, 1)[:, None]
b = np.log1p(dens) / np.log1p(dens.max())

bg = np.array([14, 12, 20], float)
img = bg + (mean - bg) * b[:, None]
img = img.reshape(S, S, 3).clip(0, 255).astype(np.uint8)
Image.fromarray(img).resize((size, size), Image.LANCZOS).save(out)
print(f"seed {seed} freq {np.round(freq, 3).tolist()} damp {np.round(damp, 4).tolist()} hit {int((dens > 0).sum())} px")
