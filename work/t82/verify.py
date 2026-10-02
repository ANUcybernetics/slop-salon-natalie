import re, sys
path = sys.argv[1] if len(sys.argv) > 1 else '/tmp/scroll-2-built.svg'
src = open(path).read()

# whole file, not just the new stretch
assert src.startswith('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 7760 640">')
assert src.count('<rect') == 1 and 'width="7760"' in src and 'height="640"' in src
assert src.count('<polyline') == 9
assert src.count('data-tick="n') == 9
assert 'the second sheet' in src  # header comment intact

ticks = re.findall(r'<polyline data-tick="([^"]+)" points="([^"]+)"', src)
assert [t for t, _ in ticks] == ['n%d' % i for i in range(1, 10)]
poly = {t: [tuple(map(int, q.split(','))) for q in p.split()] for t, p in ticks}

for i in range(2, 10):
    assert poly['n%d' % i][0] == poly['n%d' % (i-1)][-1], 'seam n%d' % i
for t, pts in poly.items():
    assert all(b[0] > a[0] for a, b in zip(pts, pts[1:])), 'x %s' % t
full = [poly['n1'][0]]
for i in range(2, 10):
    full += poly['n%d' % i][1:]
assert all(b[0] > a[0] for a, b in zip(full, full[1:])), 'one line, x never returns'
assert full[0] == (60, 287) and full[-1] == (7596, 242)

n9 = poly['n9']
assert all(b[1] < a[1] for a, b in zip(n9, n9[1:])), 'n9 strictly rising'
assert n9[0] == (6980, 462) and n9[-1] == (7596, 242)
for rung in (384, 320):
    assert any(min(a[1], b[1]) < rung < max(a[1], b[1])
               for a, b in zip(n9, n9[1:])), 'rung %d' % rung
assert not any(y == 320 for _, y in n9), 'home never ON a point'

print('verify ok: 9 stretches, paper 7760, n9 x %d->%d ends y=%d'
      % (n9[0][0], n9[-1][0], n9[-1][1]))
