W_OLD, W_NEW = 7120, 7760

# n9: the climb crosses home. from the terrace touch (6980,462) the riser
# keeps its law — steady, no holds — and passes home (320) mid-ink,
# UNMARKED, the way n2 taught going down. the heights never notice.
# the eye does: first ink above home on this sheet.
# the end ON the hill (242, the 880 rung) — touched, not taken,
# rhyming n8's terrace ending. the climb does not rest.
PTS = [
    (6980, 462),
    (7024, 445),
    (7068, 428),
    (7112, 411),
    (7156, 395),
    (7200, 379),
    (7244, 363),
    (7288, 347),
    (7332, 331),
    (7376, 315),
    (7420, 299),
    (7464, 283),
    (7508, 268),
    (7552, 255),
    (7596, 242),
]
assert len(PTS) == 15
assert all(b[0] > a[0] for a, b in zip(PTS, PTS[1:])), 'x not strictly increasing'
assert all(b[1] < a[1] for a, b in zip(PTS, PTS[1:])), 'a riser: y strictly decreasing'
assert PTS[0] == (6980, 462), 'seam: opens on the terrace touch'
assert PTS[-1] == (7596, 242), 'ends on the hill, touched not taken'
assert max(y for _, y in PTS) == 462, 'low point is the seam'
assert min(y for _, y in PTS) == 242, 'high point is the hill end'
# crossings mid-ink: the ledge (384) and HOME (320) pass under the pen
for rung in (384, 320):
    assert any(min(a[1], b[1]) < rung < max(a[1], b[1])
               for a, b in zip(PTS, PTS[1:])), 'rung %d crossed mid-ink' % rung
# home crossed BETWEEN points, never ON one — unmarked
assert not any(y == 320 for _, y in PTS), 'home never on a point'
assert PTS[-1][0] <= W_NEW - 140, 'headroom on the widened paper'

pts_str = ' '.join('%d,%d' % p for p in PTS)
line = '    <polyline data-tick="n9" points="%s" />\n' % pts_str

src = open('work/scroll-2.svg').read()

# widen first: viewBox and rect together, each asserted count==1
assert src.count('viewBox="0 0 %d 640"' % W_OLD) == 1
assert src.count('width="%d"' % W_OLD) == 1
src = src.replace('viewBox="0 0 7120 640"', 'viewBox="0 0 7760 640"')
src = src.replace('width="7120"', 'width="7760"')

# insert as text before the anchor; anchor read from bytes, asserted once
anchor = '\n  </g>\n</svg>\n'
assert src.endswith(anchor)
assert src.count(anchor) == 1
out = src[:-len(anchor)] + '\n' + line.rstrip('\n') + anchor

open('/tmp/scroll-2-built.svg', 'w').write(out)
open('assets/n9-points.txt', 'w').write('\n'.join('%d,%d' % p for p in PTS) + '\n')
print('built: %d points, x %d -> %d, paper %d' % (len(PTS), PTS[0][0], PTS[-1][0], W_NEW))
