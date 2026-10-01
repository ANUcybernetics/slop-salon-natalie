import re, sys

path = sys.argv[1]
src = open(path).read()

def fail(msg):
    print('FAIL:', msg)
    sys.exit(1)

want_header = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 5200 640">'
if not src.startswith(want_header):
    fail('header/viewBox')
if src.count('<rect width="5200" height="640" fill="#f6f1e7"/>') != 1:
    fail('rect')
if src.count('<polyline') != 5:
    fail('polyline count')
if src.count('</g>') != 1 or src.count('</svg>') != 1 or src.count('<g ') != 1:
    fail('group tags')
if not src.endswith('\n  </g>\n</svg>\n') or src.count('\n  </g>\n</svg>\n') != 1:
    tail = '\n  </g>\n anchor is wrong'
    fail(tail)

ticks = re.findall(r'<polyline data-tick="([^"]+)" points="([^"]+)"', src)
if [t for t, _ in ticks] != ['n1', 'n2', 'n3', 'n4', 'n5']:
    fail('tick order/set: %r' % [t for t, _ in ticks])

prev_end = None
for t, p in ticks:
    pts = [tuple(map(int, q.split(','))) for q in p.split()]
    if any(b <= a for a, b in zip(pts, pts[1:])):
        fail('x not strictly increasing in %s' % t)
    if prev_end is not None and pts[0] != prev_end:
        fail('seam into %s: %s vs %s' % (t, pts[0], prev_end))
    prev_end = pts[-1]

n5 = [tuple(map(int, q.split(','))) for q in dict(ticks)['n5'].split()]
if n5[0] != (4520, 384):
    fail('n5 seam point')
terr = [y for _, y in n5[12:16]]
if terr != [462] * 4:
    fail('terrace: %r' % terr)
wob = [y for _, y in n5[31:39]]
if wob != [498, 500, 501, 499, 497, 496, 496, 497]:
    fail('wobble: %r' % wob)
if n5[-1] != (5156, 498):
    fail('rest: %r' % n5[-1])
if max(y for _, y in n5) != 501:
    fail('deepest y')

print('verify: all checks pass (%d stretches)' % len(ticks))
