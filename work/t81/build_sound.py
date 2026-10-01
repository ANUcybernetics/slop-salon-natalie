import re, math, wave, struct

src = open('work/scroll-2.svg').read()
ticks = dict(re.findall(r'<polyline data-tick="([^"]+)" points="([^"]+)"', src))
assert list(ticks) == ['n%d' % i for i in range(1, 9)]
pts = [tuple(map(int, q.split(','))) for q in ticks['n8'].split()]
assert pts[0] == (6340, 618) and pts[-1] == (6980, 462)

def f(y): return 440.0 * 2 ** ((320 - y) / 78.0)

fsr = 44100
PACE = 45.0
HOLD = 0.0   # the climb does not rest
FADE = 2.0
walk = (pts[-1][0] - pts[0][0]) / PACE
n = int(round((walk + HOLD) * fsr))
assert n > fsr

buf = [0.0] * n
for off in (-1.1, 1.1):
    t = 0.0
    phase = 0.0
    for i in range(len(pts) - 1):
        (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        d = int(round((x1 - x0) / PACE * fsr))
        f0, f1 = f(y0 + off), f(y1 + off)
        for k in range(d):
            u = k / d
            fv = f0 + (f1 - f0) * u
            phase += 2 * math.pi * fv / fsr
            buf[int(t * fsr) + k] += math.sin(phase)
        t += (x1 - x0) / PACE
    d = int(round(HOLD * fsr))
    for k in range(d):
        phase += 2 * math.pi * f(pts[-1][1] + off) / fsr
        buf[int(walk * fsr) + k] += math.sin(phase)

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
w = wave.open('assets/n8-climb.wav', 'wb')
w.setnchannels(1); w.setsampwidth(2); w.setframerate(fsr)
w.writeframes(pcm); w.close()

w = wave.open('assets/n8-climb.wav')
assert w.getnframes() == n
frames = w.readframes(n)
vals = struct.unpack('<%dh' % n, frames)
rb = max(abs(v) / 32767.0 for v in vals)
w.close()
print('walk %.2f s, total %.2f s' % (walk, walk + HOLD))
print('read-back peak %.3f' % rb)
assert rb <= 1.0
