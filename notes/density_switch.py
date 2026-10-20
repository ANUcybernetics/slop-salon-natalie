import sys
import numpy as np
from PIL import Image

N = 480
THRESH = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
OUT = sys.argv[2] if len(sys.argv) > 2 else "assets/density_switch.png"

RULES = {30: np.array([(30 >> i) & 1 for i in range(8)], dtype=np.uint8),
         110: np.array([(110 >> i) & 1 for i in range(8)], dtype=np.uint8)}

row = np.zeros(N, dtype=np.uint8)
row[N // 2] = 1
rows = [row]
rule_log = []
for _ in range(N - 1):
    rule = 110 if rows[-1].mean() >= THRESH else 30
    rule_log.append(rule)
    l = np.roll(rows[-1], 1)
    r = np.roll(rows[-1], -1)
    idx = 4 * l + 2 * rows[-1] + r
    rows.append(RULES[rule][idx])

grid = np.array(rows)
switches = sum(1 for a, b in zip(rule_log, rule_log[1:]) if a != b)
print(f"threshold={THRESH} switches={switches} "
      f"rule30={rule_log.count(30)} rule110={rule_log.count(110)} "
      f"final_mean={rows[-1].mean():.2f}")

BG = np.array([17, 14, 22], dtype=np.uint8)
FG = np.array([240, 226, 196], dtype=np.uint8)
img = np.where(grid[..., None] == 1, FG, BG).astype(np.uint8)
Image.fromarray(img, "RGB").save(OUT)
