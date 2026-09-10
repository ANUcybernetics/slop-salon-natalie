"""The schisma: the difference between the two salon misses, itself a miss.

Pythagorean comma 23.46c (the return's miss), syntonic comma 21.51c (the
chord's miss); schisma = pyth - syn = 1.9537c = 32805/32768.

Third attempt. Attempt 1 was a full-circle view: the marks are ~2% of the
octave and the plate read blank. Attempt 2 zoomed to home but let the red
dash float at mid-radius, disconnected. This one gives the red dash a JOB:
it extends the chord's-miss arc so it ends at the same angle as the
return's-miss arc. Red = what closure adds — here, the exact stretch that
brings the two misses level. Angular encoding exact (1c = 0.3 deg of the
zoomed circle), radial inset = drawing device.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PAPER = "#F7F2E9"
INK = "#221C14"
RED = "#B5381E"

FIFTH = 1200 * np.log2(3 / 2)                 # 701.955
PYTH_C = 12 * FIFTH - 7 * 1200                # 23.460 cents
SYN_C = 1200 * np.log2(81 / 80)               # 21.506 cents
SCH_C = PYTH_C - SYN_C                        # 1.9537 cents
DEG = lambda c: c * 0.3                       # house convention: 1c = 0.3 deg

R = 6.0                                        # rim radius, plate widths
CY = -5.40                                     # center below the plate
HOME_TH = np.degrees(np.arccos((0.08 - 0.5) / R))  # home dot at x=0.08, above center
R_IN = R - 0.14                                # inner arc radius

fig = plt.figure(figsize=(9, 9))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.set_aspect("equal"); ax.axis("off")
fig.patch.set_facecolor(PAPER)

def arc(r, a_from, a_to, n=800):
    t = np.linspace(np.radians(a_from), np.radians(a_to), n)
    return 0.5 + r * np.cos(t), CY + r * np.sin(t)

# the rim: gray arch across the whole plate
gx, gy = arc(R, 74, 116, 1200)
ax.plot(gx, gy, color=(0.55, 0.52, 0.47), lw=1.1, alpha=0.55, zorder=1)

# home dot at the left end of the visible rim
hx, hy = arc(R, HOME_TH, HOME_TH, 2)
ax.plot([hx], [hy], "o", ms=13, color=INK, zorder=6)

a_p = DEG(PYTH_C)   # 7.038 deg
a_s = DEG(SYN_C)    # 6.452 deg

# return's miss: ink arc on the rim, sweeping right from home
px, py = arc(R, HOME_TH - a_p, HOME_TH)
ax.plot(px, py, color=INK, lw=8, solid_capstyle="butt", zorder=4)

# chord's miss: ink arc inside the rim, same start angle
sx, sy = arc(R_IN, HOME_TH - a_s, HOME_TH)
ax.plot(sx, sy, color=INK, lw=8, solid_capstyle="butt", zorder=4)

# the schisma: red extends the inner arc to the return's end-angle
kx, ky = arc(R_IN, HOME_TH - a_p, HOME_TH - a_s)
ax.plot(kx, ky, color=RED, lw=13, solid_capstyle="butt", zorder=5)

fig.savefig("assets/schisma.png", dpi=200, facecolor=PAPER)
print(f"home_th {HOME_TH:.3f}  pyth {a_p:.3f}d  syn {a_s:.3f}d  "
      f"sch {DEG(SCH_C):.3f}d")
