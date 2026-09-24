import re, sys
path = sys.argv[1]
src = open(path).read()
pat = re.compile(r'<polyline data-tick="(\d+)" tags?|<polyline data-tick="(\d+)" points="([^"]*)"/>')
pls = re.findall(r'<polyline data-tick="(\d+)" points="([^"]*)"/>', src)
assert src.count('<polyline') == len(pls), "polyline count mismatch"
assert len(pls) == 52, f"n={len(pls)}"
ticks = [int(t) for t, _ in pls]
assert ticks == list(range(1, 53)), "ticks not 1..52"
d = dict(pls)
P = lambda k: [tuple(map(int, p.split(','))) for p in d[k].split()]

# header comment survived
assert src.count('the scroll: one line, one tick, never lifted') == 1

# seams: each stretch starts at previous end
for a, b in zip(pls, pls[1:]):
    A = P(a[0]); B = P(b[0])
    assert A[-1] == B[0], f"seam {a[0]}->{b[0]}: {A[-1]} vs {B[0]}"

# x strictly increasing per-stretch
for t, pts in pls:
    xs = [int(p.split(',')[0]) for p in pts.split()]
    assert all(xs[i+1] > xs[i] for i in range(len(xs)-1)), f"x not increasing in tick {t}"

# far s28 = near-28 +6578, x AND y exact
near = P('28'); far = P('52')
assert len(near) == len(far) == 19
for (nx, ny), (fx, fy) in zip(near, far):
    assert fx == nx + 6578 and fy == ny, f"{(nx,ny)} -> {(fx,fy)}"

# no widening: edge unchanged, room 300 after
assert 'viewBox="0 0 14720 640"' in src and 'width="14720"' in src
print(f"OK {path}: 52 stretches, ticks 1..52, seams intact, far s28 = near-28 +6578 exact, edge 14720")
