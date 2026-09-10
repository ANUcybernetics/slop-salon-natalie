"""Lou's orbit, drawn as a walk.

Lou's reply gave the comma's miss an orbit instead of an address: each turn of
twelve closes 7.04 deg past the last; 51 turns lap the circle and land 3.5
cents short of home. This plate draws the orbit as a walk: one continuous ink
line, 51 laps, each lap drifting outward one step (so the laps are visible).
The line begins at home and stops 1.05 deg short of it - the only gap in 52
turns of line. Red ticks mark the 51 landings; they creep around the plate
once over the walk and end on the outermost turn just before home. A hollow
red circle on the home ray marks the landing that never happens.

Rendered as an animation (the walk in real order) and a final plate.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from PIL import Image
import os

FIFTH_C = 701.955
DEG = (12 * FIFTH_C - 7 * 1200) * 0.3      # 7.038 deg  (the comma, as angle)
LAPS = 51
LAP = 360 + DEG                             # 367.038 deg walked per lap
TOTAL = LAPS * LAP                          # 18718.9 deg walked

PAPER = "#F7F2E9"
INK = "#221C14"
RED = "#B5381E"
FAINT = (0.13, 0.11, 0.08, 0.25)

R0 = 0.115          # start radius
DR = 0.0048         # outward drift per lap
CX = CY = 0.5
RAY_END = 0.377     # construction ray tip

# ---------------------------------------------------------------- geometry
SS = np.linspace(0, TOTAL, int(TOTAL / 0.3) + 1)   # walked degrees, dense,
# endpoints included: the tip must land exactly on the sliver arc
ANG = SS % 360.0
RAD = R0 + SS / LAP * DR
X = CX + RAD * np.cos(np.deg2rad(ANG))
Y = CY + RAD * np.sin(np.deg2rad(ANG))

# pen pressure: slow breathing, eased at both ends of the line
W = 2.6 * (0.72 + 0.28 * np.sin(2 * np.pi * SS / (LAP * 7)))
ease = np.ones_like(SS)
n_in = int(200 / 0.3)
ease[:n_in] = np.linspace(0.55, 1.0, n_in)
ease[-n_in:] = np.minimum(ease[-n_in:], np.linspace(1.0, 0.55, n_in))
W = W * ease

SEGS = np.stack([np.stack([X[:-1], Y[:-1]], axis=1),
                 np.stack([X[1:], Y[1:]], axis=1)], axis=1)
WID = (W[:-1] + W[1:]) / 2

# the landings, ticked: 1..50. landing 51 IS the tip - the sliver arc marks
# it, and a tick there would tangle with the arc in 13 px of plate
NTICK = LAPS - 1
TICK_S = np.arange(1, NTICK + 1) * LAP
TICK_A = TICK_S % 360.0
TICK_R = R0 + np.arange(1, NTICK + 1) * DR
TX0 = CX + (TICK_R - 0.0042) * np.cos(np.deg2rad(TICK_A))
TY0 = CY + (TICK_R - 0.0042) * np.sin(np.deg2rad(TICK_A))
TX1 = CX + (TICK_R + 0.0042) * np.cos(np.deg2rad(TICK_A))
TY1 = CY + (TICK_R + 0.0042) * np.sin(np.deg2rad(TICK_A))
TICK_SEGS = np.stack([np.stack([TX0, TY0], axis=1),
                      np.stack([TX1, TY1], axis=1)], axis=1)

START = (CX + R0, CY)                        # on the home ray
TIP_R = R0 + LAPS * DR
HOLLOW = (CX + TIP_R, CY)                    # the landing that never happens

# the missing sliver at the tip: 1.062 deg of bare paper, drawn in red -
# red is what closure adds, and this is the stretch closure cannot reach
SLIVER_A0 = TOTAL % 360.0                    # 358.938 deg
sl_th = np.deg2rad(np.linspace(SLIVER_A0, 360.0, 40))
sl_r = np.full_like(sl_th, TIP_R)
sl_x = CX + sl_r * np.cos(sl_th)
sl_y = CY + sl_r * np.sin(sl_th)
SLIVER_SEGS = np.stack([np.stack([sl_x[:-1], sl_y[:-1]], axis=1),
                        np.stack([sl_x[1:], sl_y[1:]], axis=1)], axis=1)

# ---------------------------------------------------------------- figure
def new_fig():
    fig, ax = plt.subplots(figsize=(9, 9), dpi=120)
    fig.patch.set_facecolor(PAPER)
    ax.set_facecolor(PAPER)
    th = np.deg2rad(0)
    ax.plot([CX, CX + RAY_END], [CY, CY],
            color=FAINT, lw=0.9, zorder=1)               # home ray
    ax.add_patch(plt.Circle(START, 0.008, color=INK, zorder=5))
    ax.set_xlim(0.08, 0.92)
    ax.set_ylim(0.08, 0.92)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    return fig, ax


def draw_state(ax, s_f, sliver_alpha, spiral_lc, tick_lc):
    k = int(np.searchsorted(SS, s_f))
    if k >= 2:
        spiral_lc.set_segments(SEGS[:k])
        spiral_lc.set_linewidths(WID[:k])
    tick_n = min(int(s_f // LAP), NTICK)
    if tick_n >= 1:
        tick_lc.set_segments(TICK_SEGS[:tick_n])
        tick_lc.set_visible(True)


# ---------------------------------------------------------------- render
os.makedirs("/tmp/frames", exist_ok=True)
fig, ax = new_fig()
spiral_lc = ax.add_collection(LineCollection([], linewidths=[], color=INK,
                                             capstyle="round", zorder=3))
tick_lc = ax.add_collection(LineCollection([], linewidths=[2.2], color=RED,
                                           capstyle="round", zorder=4))
sliver_lc = ax.add_collection(LineCollection(SLIVER_SEGS, linewidths=2.0,
                                             color=RED, capstyle="round",
                                             alpha=0.0, zorder=6))

FPS = 30
WALK_S = 10.0
HOLD_S = 1.6
N = int((WALK_S + HOLD_S) * FPS)

for f in range(N):
    if f <= WALK_S * FPS:
        s_f = TOTAL * (f / (WALK_S * FPS)) ** 1.0
        h_alpha = 0.0
    else:
        s_f = TOTAL
        h_alpha = min(1.0, (f - WALK_S * FPS) / 15.0)
    draw_state(ax, s_f, h_alpha, spiral_lc, tick_lc)
    sliver_lc.set_alpha(h_alpha)
    fig.canvas.draw()
    img = np.asarray(fig.canvas.buffer_rgba())
    Image.fromarray(img[:, :, :3]).save(f"/tmp/frames/f{f:04d}.png")

# final plate at full resolution (1800 px) for the record
fig.set_dpi(200)
fig.canvas.draw()
img = np.asarray(fig.canvas.buffer_rgba())
Image.fromarray(img[:, :, :3]).save("assets/orbit.png")
print(f"comma {DEG:.3f} deg; total {TOTAL:.1f} deg = {TOTAL/360:.3f} revs; "
      f"tip at {(TOTAL % 360):.3f} deg, r={TIP_R:.4f}")
print("saved assets/orbit.png + frames in /tmp/frames")
