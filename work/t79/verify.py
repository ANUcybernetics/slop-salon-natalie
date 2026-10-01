import re, sys

path = sys.argv[1]
src = open(path).read()

def fail(msg):
    print('FAIL:', msg)
    sys.exit(1)

if not src.startswith('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 5840 640">'):
    fail('header/viewBox')
if src.count('<rect width="5840" height="640" fill="#f6f1e7"/>') != 1:
    fail('rect')
if src.count('<polyline') != 6:
    fail('polyline count')
if src.count('</g>') != 1 or src.count('</svg>') != 1 or src.count('<g ') != 1:
    fail('group tags')
if not src.endswith('\n  </g>\n</svg>\n') or src.count('\n  </g>\n</svg>\n') != 1:
    fail('anchor')

ticks = re.findall(r'<polyline data-tick="([^"]+)" points="([^"]+)"', src)
if [t for t, _ in ticks] != ['n1', 'n2', 'n3', 'n4', 'n5', 'n6']:
    fail('tick order/set')

prev_end = None
for t, p in ticks:
    pts = [tuple(map(int, q.split(','))) for q in p.split()]
    if any(b <= a for a, b in zip(pts, pts[1:])):
        fail('x not strictly increasing in %s' % t)
    if prev_end is not None and pts[0] != prev_end:
        fail('seam into %s' % t)
    prev_end = pts[-1]

n6 = [tuple(map(int, q.split(','))) for q in dict(ticks)['n6'].split()]
if n6[0] != (5156, 498):
    fail('n6 seam point')
if n6[2] != (5240, 497):
    fail('breath')
if n6[10] != (5570, 540):
    fail('first touch')
if n6[11] != (5590, 542):
    fail('dip')
if n6[-1] != (5700, 540):
    fail('rest')
if max(y for _, y in n6) != 542:
    fail('deepest')
if min(y for _, y in n6) != 497:
    fail('breath high point')

# points txt vs svg: normalize newline-separated vs space-separated
txt = [tuple(map(int, l.split(','))) for l in open('assets/n6-points.txt').read().strip().split('\n')]
if txt != n6:
    fail('points txt mismatch')

print('verify: all checks pass (%d stretches)' % len(ticks))
