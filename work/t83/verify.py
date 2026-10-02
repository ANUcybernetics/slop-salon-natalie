import re, sys
path = sys.argv[1] if len(sys.argv) > 1 else '/tmp/scroll-2-built.svg'
src = open(path).read()

# whole file, not just the new stretch
assert src.startswith('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 8400 640">')
assert src.count('<rect') == 1 and 'width="8400"' in src and 'height="640"' in src
assert src.count('<polyline') == 10
assert src.count('data-tick="n') == 10
assert 'the second sheet' in src  # header comment intact

ticks = re.findall(r'<polyline data-tick="([^"]+)" points="([^"]+)"', src)
assert [t for t, _ in ticks] == ['n%d' % i for i in range(1, 11)]
poly = {t: [tuple(map(int, q.split(','))) for q in p.split()] for t, p in ticks}

for i in range(2, 11):
    assert poly['n%d' % i][0] == poly['n%d' % (i-1)][-1], 'seam n%d' % n if False else 'seam n%d' % i
for t, pts in poly.items():
    assert all(b[0] > a[0] for a, b in zip(pts, pts[1:])), 'x %s' % t
full = [poly['n1'][0]]
for i in range(2, 11):
    full += poly['n%d' % i][1:]
assert all(b[0] > a[0] for a, b in zip(full, full[1:])), 'one line, x never returns'
assert full[0] == (60, 287) and full[-1] == (8260, 242)

n10 = poly['n10']
assert n10[0] == (7596, 242) and n10[-1] == (8260, 242)
assert all(b[1] >= a[1] for a, b in zip(n10, n10[1:])) == False, 'the hold is flat, not a riser'
assert sorted(set(y for _, y in n10)) == [241, 242], 'the hold sits on the rung with one breath'
assert [p for p in n10 if p[1] == 241] == [(7932, 241)], 'one breath, 1px up, mid-hold'

print('verify ok: 10 stretches, paper 8400, n10 x %d->%d flat at y=242 with one breath at %s'
      % (n10[0][0], n10[-1][0], [p for p in n10 if p[1] == 241][0]))
