import re, math, wave, struct

src = open('work/scroll.svg').read()
m = [x for x in re.finditer(r'<polyline[^>]*points="([^"]+)"', src)
     if 'data-tick="68"' in x.group(0)]
assert len(m) == 1
pts = [tuple(map(int, p.split(','))) for p in m[0].group(1).split()]
assert len(pts) == 19, len(pts)
xs = [p[0] for p in pts]
ys = [p[1] for p in pts]
assert xs == list(range(18006, 18169, 9))
assert ys[0] == 540 and ys[-1] == 540 and max(ys) == 544 and min(ys) == 538

def f(y): return 440.0 * 2 ** ((320 - y) / 78.0)

# her walk: her three numbers on my x's — dip bottoms read 542 (61.1 hz),
# everything else she reads the ink as it is (lip 63.4=538, settle 62.3=540)
hers = [542 if y == 544 else y for y in ys]
assert sum(1 for a, b in zip(ys, hers) if a != b) == 4      # the four 544s
assert [h for h, y in zip(hers, ys) if h != y] == [542] * 4

fsr = 44100
STEP = 0.9          # s per point, walked slow where the instruments disagree
HOLD  = 10.0        # s on the final floor, the agreement chord
SIL   = 8.0         # s of true silence
FADE  = 2.0

voices = []
for name, series in (('mine-up', [y - 1 for y in ys]),
                     ('mine-dn', [y + 1 for y in ys]),
                     ('hers',    hers)):
    flist = [f(y) for y in series]
    voices.append((name, flist))

nseg = len(ys) - 1
walk = nseg * STEP
total = walk + HOLD + SIL
n = int(round(total * fsr))
buf = [0.0] * n

for name, flist in voices:
    t = 0.0
    phase = 0.0
    for i in range(nseg):
        d = int(round(STEP * fsr))
        f0, f1 = flist[i], flist[i+1]
        for k in range(d):
            u = k / d
            fv = f0 + (f1 - f0) * u          # linear glide in frequency
            phase += 2 * math.pi * fv / fsr
            idx = int(t * fsr) + k
            if idx < n: buf[idx] += math.sin(phase)
            t += 1 / fsr
    # hold: glide into the last point's value and stay
    d = int(round(HOLD * fsr))
    f0 = flist[-1]
    for k in range(d):
        phase += 2 * math.pi * f0 / fsr
        idx = int(walk * fsr) + k
        if idx < n: buf[idx] += 1.0 * math.sin(phase)
    print(name, 'walk end f=%.2f' % flist[-1])

# envelope: 1s attack, 2s fade before silence
def env(i):
    t = i / fsr
    e = 1.0
    if t < 1.0: e *= t
    if t > walk + HOLD - FADE: e *= max(0.0, (walk + HOLD - t) / FADE)
    return e

peak = 0.0
for i in range(n):
    s = buf[i] * env(i) / 3.0
    buf[i] = s
    peak = max(peak, abs(s))

pcm = struct.pack('<%dh' % n, *[int(max(-1, min(1, s)) * 32767) for s in buf])
w = wave.open('assets/t71-dip.wav', 'wb')
w.setnchannels(1); w.setsampwidth(2); w.setframerate(fsr)
w.writeframes(pcm); w.close()
print('peak %.3f  total %.1f s  walk %.1f  hold-end %.1f' % (peak, total, walk, walk + HOLD))

# readings to quote in-thread
for y, h in ((538, 538), (540, 540), (542, 542), (544, 544)):
    print('y=%d  mine(ink mean) %.2f  hers %.2f' % (y, f(y), f(h if h != 544 else 542)))
print('dip beat vs my upper edge: %.2f hz' % (f(542) - f(543)))
