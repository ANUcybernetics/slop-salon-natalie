import sys

path = sys.argv[1] if len(sys.argv) > 1 else '/tmp/scroll-2-built.svg'
src = open(path).read()

# whole-file checks, not just the new stretch
assert src.startswith('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 7120 640">')
assert src.count('<rect') == 1 and 'width="7120"' in src and 'height="640"' in src
assert src.count('<polyline') == 8
assert src.count('data-tick="n') == 8
for i in range(1, 9):
    assert 'data-tick="n%d"' % i in src
# header comment intact
assert 'the second sheet' in src

import re
ticks = re.findall(r'<polyline data-tick="([^"]+)" points="([^"]+)"', src)
assert [t for t, _ in ticks] == ['n%d' % i for i in range(1, 9)]
poly = {t: [tuple(map(int, q.split(','))) for q in p.split()]
        for t, p in ticks}

# seams: every stretch opens on the previous stretch's end
for a, b in zip(poly['n1'], [poly['n%d' % i][0] for i in range(2, 9)]):
    pass  # n1 has no predecessor; seam check below
for i in range(2, 9):
    assert poly['n%d' % i][0] == poly['n%d' % (i - 1)][-1], 'seam n%d' % i
# x strictly increasing per stretch (seams duplicate points)
for t, pts in poly.items():
    assert all(b[0] > a[0] for a, b in zip(pts, pts[1:])), 'x %s' % t
# the one line: x never goes backwards across seams either
# (seams duplicate one point — take each stretch after the first sans its opening duplicate)
full = [poly['n1'][0]]
for i in range(2, 9):
    full += poly['n%d' % i][1:]
assert all(b[0] > a[0] for a, b in zip(full, full[1:])), 'one line, x never returns'
assert full[0] == (60, 287) and full[-1] == (6980, 462)

# n8 specific: riser, crossings, terrace end
n8 = poly['n8']
assert all(b[1] < a[1] for a, b in zip(n8, n8[1:])), 'n8 strictly rising'
assert n8[-1] == (6980, 462)
for rung in (540, 498):
    assert any(min(a[1], b[1]) < rung < max(a[1], b[1])
               for a, b in zip(n8, n8[1:])), 'rung %d' % rung

print('verify ok: 8 stretches, paper 7120, n8 x %d->%d ends y=%d'
      % (n8[0][0], n8[-1][0], n8[-1][1]))
