import re

W_OLD, W_NEW = 4560, 5200

# n5: the descent from the ledge (4520,384) to the shelf (y=498).
# x = 4520 + 12k, k=0..53 -> 5156 (44 px of ground on 5200 paper).
# A: departure — one breath back (echo of the hold's breath), then the fall.
# B: fall to the terrace at 462 (the octave under the ledge).
# C: terrace, flat at 462.
# D: second fall to the shelf.
# E: the settle — the pen finds the shelf, wobbling the way t2/t64 did.
YS = [
    384, 383, 385, 390, 398, 409, 421, 433, 443, 451, 457, 461,   # A+B (k0-k11)
    462, 462, 462, 462,                                           # C terrace (k12-k15)
    463, 465, 468, 472, 476, 480, 483, 486, 488, 490, 492, 494,
    495, 496, 497,                                                # D (k16-k30)
    498, 500, 501, 499, 497, 496, 496, 497,                       # E wobble (k31-k38)
    498, 498, 497, 496, 496, 497, 498, 498, 497, 496, 496, 497,
    498, 498, 498,                                                # E settle (k39-k53)
]
assert len(YS) == 54
X0, DX = 4520, 12
pts = [(X0 + DX * k, y) for k, y in enumerate(YS)]
assert pts[-1] == (5156, 498)

# per-stretch sanity before it goes anywhere near the file
assert all(b[0] > a[0] for a, b in zip(pts, pts[1:])), 'x not strictly increasing'
assert pts[0] == (4520, 384), 'seam: must open on the hold end'
terr = [y for _, y in pts[12:16]]
assert terr == [462] * 4, 'terrace at 462'
assert max(y for _, y in pts[31:]) == 501 and min(y for _, y in pts[31:]) >= 496
assert max(y for _, y in pts) == 501, 'deep point is the wobble, nothing deeper'

pts_str = ' '.join('%d,%d' % p for p in pts)
line = '    <polyline data-tick="n5" points="%s" />\n' % pts_str

src = open('work/scroll-2.svg').read()

# widen: viewBox and rect together, each asserted count==1 before replace
assert src.count('viewBox="0 0 %d 640"' % W_OLD) == 1
assert src.count('width="%d"' % W_OLD) == 1
src = src.replace('viewBox="0 0 %d 640"' % W_OLD, 'viewBox="0 0 %d 640"' % W_NEW)
src = src.replace('width="%d"' % W_OLD, 'width="%d"' % W_NEW)

# insert as text before the anchor; anchor read from bytes, asserted to match once
anchor = '\n  </g>\n</svg>\n'
assert src.endswith(anchor)
assert src.count(anchor) == 1
out = src[:-len(anchor)] + '\n' + line.rstrip('\n') + anchor

open('/tmp/scroll-2-built.svg', 'w').write(out)
open('assets/n5-points.txt', 'w').write('\n'.join('%d,%d' % p for p in pts) + '\n')
print('built: %d points, x %d -> %d, paper %d' % (len(pts), pts[0][0], pts[-1][0], W_NEW))
