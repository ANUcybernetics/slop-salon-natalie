import re, math, wave, struct

src = open('work/scroll-2.svg').read()
ticks = re.findall(r'<polyline data-tick="([^"]+)" points="([^"]+)"', src)
assert [t for t, _ in ticks] == ['n1', 'n2']
pts_all = []
for t, p in ticks:
    pts = [tuple(map(int, q.split(','))) for q in p.split()]
    assert all(b > a for a, b in zip(pts, pts[1:]))
    pts_all += pts

xs = [p[0] for p in pts_all]
assert xs[0] == 60 and xs[-1] == 2560
total_px = xs[-1] - xs[0]

def f(y): return 440.0 * 2 ** ((320 - y) / 78.0)

fsr = 44100
PACE = 45.0            # px per second, the imagined line's pace (t73)
HOLD = 5.0             # s on the rest
FADE = 2.0
walk = total_px / PACE
n = int(round((walk + HOLD) * fsr))

buf = [0.0] * n
for off in (-1.1, 1.1):
    t = 0.0
    phase = 0.0
    for i in range(len(pts_all) - 1):
        (x0, y0), (x1, y1) = pts_all[i], pts_all[i + 1]
        span = x1 - x0
        d = int(round(span / PACE * fsr))
        f0, f1 = f(y0 + off), f(y1 + off)
        for k in range(d):
            u = k / d
            fv = f0 + (f1 - f0) * u
            phase += 2 * math.pi * fv / fsr
            idx = int(t * fsr) + k
            if idx < n: buf[idx] += math.sin(phase)
        t += span / PACE
    # hold the rest
    f_end = f(pts_all[-1][1] + off)
    d = int(round(HOLD * fsr))
    for k in range(d):
        phase += 2 * math.pi * f_end / fsr
        idx = int(walk * fsr) + k
        if idx < n: buf[idx] += math.sin(phase)

def env(i):
    t = i / fsr
    e = 1.0
    if t < 1.0: e *= t
    if t > walk + HOLD - FADE: e *= max(0.0, (walk + HOLD - t) / FADE)
    return e

peak = 0.0
for i in range(n):
    s = buf[i] * env(i) / 2.0
    buf[i] = s
    peak = max(peak, abs(s))

g = 0.95 / peak
buf = [s * g for s in buf]
pcm = struct.pack('<%dh' % n, *[int(max(-1, min(1, s)) * 32767) for s in buf])
w = wave.open('assets/n1n2-inked.wav', 'wb')
w.setnchannels(1); w.setsampwidth(2); w.setframerate(fsr)
w.writeframes(pcm); w.close()
print('walk %.2f s  total %.2f s  raw peak %.3f' % (walk, walk + HOLD, peak))

# read-back peak is the verdict
w = wave.open('assets/n1n2-inked.wav')
assert w.getnframes() == n
frames = w.readframes(n)
vals = struct.unpack('<%dh' % n, frames)
rb = max(abs(v) / 32767.0 for v in vals)
print('read-back peak %.3f' % rb)
assert rb <= 1.0
print('rest reads %.2f Hz  home-crossing near x=1418' % f(344))
