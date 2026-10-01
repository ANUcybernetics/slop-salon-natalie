import re, sys

path = sys.argv[1]
src = open(path).read()

def fail(msg):
    print('FAIL:', msg)
    sys.exit(1)

if not src.startswith('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 6480 640">'):
    fail('header/viewBox')
if src.count('<rect width="6480" height="640" fill="#f6f1e7"/>') != 1:
    fail('rect')
if src.count('<polyline') != 7:
    fail('polyline count')
if src.count('</g>') != 1 or src.count('</svg>') != 1 or src.count('<g ') != 1:
    fail('group tags')
if not src.endswith('\n  </g>\n</svg>\n') or src.count('\n  </g>\n</svg>\n') != 1:
    fail('anchor')

ticks = re.findall(r'<polyline data-tick="([^"]+)" points="([^"]+)"', src)
if [t for t, _ in ticks] != ['n1', 'n2', 'n3', 'n4', 'n5', 'n6', 'n7']:
    fail('tick order/set')

prev_end = None
for t, p in ticks:
    pts = [tuple(map(int, q.split(','))) for q in p.split()]
    if any(b <= a for a, b in zip(pts, pts[1:])):
        fail('x not strictly increasing in %s' % t)
    if prev_end is not None and pts[0] != prev_end:
        fail('seam into %s' % t)
    prev_end = pts[-1]

n7 = [tuple(map(int, q.split(','))) for q in dict(ticks)['n7'].split()]
if n7[0] != (5700, 540):
    fail('n7 seam point')
if n7[1] != (5750, 545):
    fail('the leave')
if n7[12] != (6270, 618):
    fail('touch')
if n7[13] != (6280, 620):
    fail('dip')
if n7[-1] != (6340, 618):
    fail('rest')
if max(y for _, y in n7) != 620:
    fail('deepest')
if min(y for _, y in n7) != 540:
    fail('high point')

txt = [tuple(map(int, l.split(','))) for l in open('assets/n7-points.txt').read().strip().split('\n')]
if txt != n7:
    fail('points txt mismatch')

print('verify: all checks pass (%d stretches)' % len(ticks))
