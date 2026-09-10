"""The Pythagorean comma as the open star {12/7} plus the stroke closure adds.

Thirteen rim points at k * 210.5865 deg (a perfect fifth mapped to degrees:
1 cent = 0.3 deg, fifth = 701.955 cents). Twelve ink chords connect them in
order: the circle-of-fifths star, drawn OPEN - the return lands 7.038 deg past
home, leaving a small gap at the rim. One short red chord bridges the gap:
the thirteenth stroke, the one closure adds. Not a step - a bridge.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

FIFTH_CENTS = 701.955
CENT2DEG = 0.3          # 100 cents (semitone) -> 30 degrees
STEP = FIFTH_CENTS * CENT2DEG                   # 210.5865 deg
COMMA = (FIFTH_CENTS * 12 - 8400) * CENT2DEG    # 7.038 deg

PAPER = "#F7F2E9"
INK = "#221C14"
RED = "#B5381E"
FAINT = (0.13, 0.11, 0.08, 0.25)  # construction circle

R = 0.36
CX = CY = 0.5


def unit(angle_deg, radius=R):
    a = np.deg2rad(angle_deg)
    return CX + radius * np.cos(a), CY + radius * np.sin(a)


def stroke(x0, y0, x1, y1, base=3.2, n_samp=60):
    """One tapered ink stroke: thin at the ends, pressed in the middle."""
    t = np.linspace(0, 1, n_samp)
    xs = x0 + (x1 - x0) * t
    ys = y0 + (y1 - y0) * t
    segs, widths = [], []
    for i in range(n_samp - 1):
        s = (i + 0.5) / n_samp
        w = base * (0.55 + 0.45 * np.sin(np.pi * s))
        segs.append([(xs[i], ys[i]), (xs[i + 1], ys[i + 1])])
        widths.append(w)
    return segs, widths


fig, ax = plt.subplots(figsize=(9, 9), dpi=200)
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)

# construction circle
th = np.linspace(0, 2 * np.pi, 720)
ax.plot(CX + R * np.cos(th), CY + R * np.sin(th), color=FAINT, lw=0.9, zorder=1)

# the walk: thirteen points, twelve exact strokes
angs = [k * STEP for k in range(13)]
pts = [unit(a) for a in angs]

segs, widths = [], []
for k in range(12):
    s, w = stroke(*pts[k], *pts[k + 1])
    segs += s
    widths += w
ax.add_collection(LineCollection(segs, linewidths=widths, color=INK,
                                 capstyle="round", zorder=3))

# the closure stroke, in red: P_12 -> P_0, the width of the comma
s, w = stroke(*pts[12], *pts[0], base=2.1)
ax.add_collection(LineCollection(s, linewidths=w, color=RED,
                                 capstyle="round", zorder=4))

# ink dots at every point the walk touches
for (x, y) in pts:
    ax.add_patch(plt.Circle((x, y), 0.011, color=INK, zorder=5))
# small red dots at the bridge's ends, to set it off from the ink points
xr0, yr0 = unit(angs[0])
xr1, yr1 = unit(angs[12])
ax.add_patch(plt.Circle((xr0, yr0), 0.0045, color=RED, zorder=6))
ax.add_patch(plt.Circle((xr1, yr1), 0.0045, color=RED, zorder=6))

ax.set_xlim(0.08, 0.92)
ax.set_ylim(0.08, 0.92)
ax.set_aspect("equal")
ax.axis("off")
fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
fig.savefig("assets/comma.png", dpi=200, facecolor=PAPER)
print(f"comma: {COMMA:.3f} deg, step: {STEP:.4f} deg")
print("saved assets/comma.png")
