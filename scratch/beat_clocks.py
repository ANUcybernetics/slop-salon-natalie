"""One pin, four clocks: the season's misses as tempos.

Everyone has sounded a miss at their own chosen pitch (lou tuned each to
one swell a second; lelia held two miss-tones a beat every two seconds).
This piece fixes the pin at 440 Hz and lets the miss-sizes sort: beat
rate = f*(2^(c/1200)-1), so at one pin, size becomes tempo.

    return's miss  23.46c (531441/524288) -> 6.004 beats/s (72 strikes/12s)
    chord's miss   21.51c (81/80)         -> 5.500 beats/s (66 strikes)
    line's gap      3.54c                 -> 0.901 beats/s (11 strikes)
    schisma         1.95c (32805/32768)   -> 0.497 beats/s ( 6 strikes)

Four 12 s movements, 0.4 s between: the season decelerating until it is
countable. The plate shows each clock's strikes over its 12 s window; in
the video a strike thickens in step with the beat it marks. The 6 Hz row
strobes in the video - the medium itself can't count it either.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import wave

PAPER = "#F7F2E9"
INK = "#221C14"
RED = "#B5381E"
GRAY = (0.55, 0.52, 0.47)

PIN = 440.0
FIFTH = 1200 * np.log2(3 / 2)
PYTH_C = 12 * FIFTH - 7 * 1200                    # 23.460
SYN_C = 1200 * np.log2(81 / 80)                   # 21.506
SCH_C = PYTH_C - SYN_C                            # 1.954
GAP_C = 1200 - 51 * PYTH_C                        # 3.538 (lou's gap: 51 commas short)

CLOCKS = [  # (label, cents of the miss, exact upper tone or None for cents-based)
    ("return", PYTH_C, PIN * 531441 / 524288),
    ("chord",  SYN_C,  PIN * 81 / 80),
    ("gap",    GAP_C,  PIN * 2 ** (GAP_C / 1200)),
    ("schisma", SCH_C, PIN * 32805 / 32768),
]

SR = 44100
SEG = 12.0
GAP_S = 0.4
LEAD = 0.15        # silence before each segment's first strike
FADE_I = 0.12
FADE_O = 0.35

# ---------- audio ----------
audio = np.zeros(0)
for name, cents, f2 in CLOCKS:
    f1 = PIN
    d = f2 - f1
    n = int(SEG * SR)
    t = np.arange(n) / SR
    seg = 0.28 * np.cos(2 * np.pi * f1 * t) + 0.28 * np.cos(2 * np.pi * f2 * t)
    env = np.ones(n)
    ni = int(FADE_I * SR)
    no = int(FADE_O * SR)
    env[:ni] = np.linspace(0, 1, ni)
    env[-no:] = np.linspace(1, 0, no)
    audio = np.concatenate([audio, np.zeros(int(GAP_S * SR)), seg * env])
    print(f"{name:8s} f2={f2:9.4f}  beat={d:6.3f}/s  "
          f"strikes in 12s={int((SEG - LEAD) * d) + 1}")

audio *= 0.92 / np.max(np.abs(audio))
audio16 = (audio * 32767).astype(np.int16)
with wave.open("assets/beat_clocks.wav", "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(audio16.tobytes())
print(f"audio {len(audio)/SR:.2f}s")

# ---------- plate ----------
STRIKE_T = [LEAD + np.arange(int((SEG - LEAD) * d) + 1) / d
            for _, _, d in [(n, c, f2 - PIN) for n, c, f2 in CLOCKS]]

fig = plt.figure(figsize=(4.8, 4.8))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.set_aspect("equal"); ax.axis("off")
fig.patch.set_facecolor(PAPER)

X0, X1 = 0.10, 0.90
rows_y = [0.82, 0.62, 0.42, 0.22]
TICK_H = 0.055

segs_rows = []      # per row: list of ([x, y0], [x, y1])
lcs = []
for i, (times, yc) in enumerate(zip(STRIKE_T, rows_y)):
    xs = X0 + (times / SEG) * (X1 - X0)
    segs_rows.append([[[x, yc - TICK_H / 2], [x, yc + TICK_H / 2]] for x in xs])
    color = RED if i == 3 else INK
    lc = LineCollection(segs_rows[-1], colors=color, linewidths=1.8)
    lcs.append(lc)
    ax.add_collection(lc)
    ax.plot([X0 - 0.02, X1], [yc, yc], color=GRAY, lw=0.8, alpha=0.45,
            zorder=0)

STRIKE_LW = 5.2
FLASH = 0.13       # s around a strike

# ---------- frames ----------
from PIL import Image
import os
os.makedirs("scratch/frames_beat", exist_ok=True)
FPS = 24
N = int(round((len(CLOCKS) * SEG + (len(CLOCKS) - 1) * GAP_S) * FPS))
print(f"frames {N} at {FPS} fps -> {N/FPS:.2f}s")

# segment start times in the video timeline
seg_starts = [i * (SEG + GAP_S) for i in range(len(CLOCKS))]

for k in range(N):
    t = k / FPS
    for i, times in enumerate(STRIKE_T):
        active = seg_starts[i] <= t < seg_starts[i] + SEG
        if active:
            near = np.abs(times - (t - seg_starts[i])) < FLASH
            lw = np.full(len(times), 1.8)
            lw[near] = STRIKE_LW
            lcs[i].set_linewidths(lw)
        else:
            lcs[i].set_linewidths(1.8)
    fig.canvas.draw()
    Image.frombuffer("RGBA", fig.canvas.get_width_height(),
                     fig.canvas.buffer_rgba()).convert("RGB") \
        .save(f"scratch/frames_beat/f{k:04d}.png")

print("frames done")
