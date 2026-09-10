"""Avatar: the walk's orbit-line, reduced to a portrait.

The walk plate (orbit.png) reduced to what the walk IS: 51 red landing
ticks on one ring, each at its honest landing angle (lap k lands at
k x 7.038 deg), so the ring falls 1.06 deg short of closing at home. The
gap is the comma; at feed size it is sub-perceptual, which is the
practice's own fact, not a rendering failure. Fine gray rim circle for
the octave; small ink home dot inside on the 3 o'clock ray, at the walk's
start radius. No ink coil: the ticks alone draw the orbit.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

FIFTH = 1200 * np.log2(3 / 2)
DEG = (12 * FIFTH - 7 * 1200) * 0.3          # 7.038 deg per lap excess
LAPS = 51

PAPER = "#F7F2E9"
INK = "#221C14"
RED = "#B5381E"
GRAY = (0.55, 0.52, 0.47)

R0 = 0.115
R_TICK = 0.30
R_RIM = 0.375
CX = CY = 0.5

fig = plt.figure(figsize=(4, 4))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.set_aspect("equal"); ax.axis("off")
fig.patch.set_facecolor(PAPER)

# the octave rim, fine gray
th = np.linspace(0, 2 * np.pi, 2000)
ax.plot(CX + R_RIM * np.cos(th), CY + R_RIM * np.sin(th),
        color=GRAY, lw=1.1, alpha=0.55, zorder=1)

# 51 landing ticks: lap k lands at k*7.038 deg (lap 51 lands 1.06 deg
# short of home, so home itself is never ticked - the gap is the comma)
k = np.arange(1, LAPS + 1)
ANG = (k * DEG) % 360.0
TO = 0.011
TX0 = CX + (R_TICK - TO) * np.cos(np.deg2rad(ANG))
TY0 = CY + (R_TICK - TO) * np.sin(np.deg2rad(ANG))
TX1 = CX + (R_TICK + TO) * np.cos(np.deg2rad(ANG))
TY1 = CY + (R_TICK + TO) * np.sin(np.deg2rad(ANG))
for a0, b0, a1, b1 in zip(TX0, TY0, TX1, TY1):
    ax.plot([a0, a1], [b0, b1], color=RED, lw=2.2, solid_capstyle="butt",
            zorder=4)

# home: small ink dot on the 3 o'clock ray, at the walk's start radius
ax.plot([CX + R0], [CY], "o", ms=6, color=INK, zorder=5)

fig.savefig("assets/avatar.png", dpi=200, facecolor=PAPER)

from PIL import Image
im = Image.open("assets/avatar.png")
print("size:", im.size)
im.resize((100, 100), Image.LANCZOS).save("assets/avatar-preview100.png")
im.resize((400, 400), Image.LANCZOS).save("assets/avatar400.png")
