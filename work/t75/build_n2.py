import re, sys

SVG = 'work/scroll-2.svg'
TMP = '/tmp/scroll2-new.svg'

pts_src = open('assets/n2-points.txt').read().strip()
n2 = [tuple(map(int, p.split(','))) for p in pts_src.split()]
assert len(n2) == 12, len(n2)

src = open(SVG).read()

# --- current-state asserts
assert src.count('<polyline') == 1, src.count('<polyline')
assert 'data-tick="n1"' in src
assert 'n2' not in re.findall(r'data-tick="([^"]+)"', src)

RECT_OLD = '  <rect width="2000" height="640" fill="#f6f1e7"/>'
RECT_NEW = '  <rect width="2640" height="640" fill="#f6f1e7"/>'

vb_old = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2000 640">'
vb_new = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2640 640">'
anchor = '\n  </g>\n</svg>\n'

assert src.count(vb_old) == 1
assert src.count(RECT_OLD) == 1
assert src.count(anchor) == 1

line = '    <polyline data-tick="n2" points="%s" />' % pts_src
new_src = src.replace(vb_old, vb_new).replace(RECT_OLD, RECT_NEW)
assert new_src != src

new_src = new_src.replace(anchor, '\n' + line + anchor)

# --- whole-file verify (gates the cp)
v = new_src
assert v.startswith('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2640 640">')
assert v.count('  <rect width="2640" height="640" fill="#f6f1e7"/>') == 1
assert v.count('<polyline') == 2
ticks = re.findall(r'data-tick="([^"]+)"', v)
assert ticks == ['n1', 'n2']
n1_src = ' '.join(open('assets/imagined-n1-points.txt').read().split())
assert re.search(r'data-tick="n1" points="([^"]+)"', v).group(1) == n1_src
assert re.search(r'data-tick="n2" points="([^"]+)"', v).group(1) == pts_src
assert v.count('same pen, new anchor') == 1

stretches = {}
for m in re.finditer(r'<polyline data-tick="([^"]+)" points="([^"]+)"', v):
    stretches[m.group(1)] = [tuple(map(int, p.split(','))) for p in m.group(2).split()]
for name, pts in stretches.items():
    xs = [p[0] for p in pts]
    assert all(b > a for a, b in zip(xs, xs[1:])), name
    assert all(0 <= x <= 2640 and 0 <= y <= 640 for x, y in pts), name
assert stretches['n2'][0] == stretches['n1'][-1]

open(TMP, 'w').write(new_src)
print('build ok: %d polylines %s, seam %s, paper %s' %
      (len(ticks), ticks, stretches['n2'][0], re.search(r'rect width="(\d+)"', v).group(1)))
