W_OLD, W_NEW = 6480, 7120

# n8: the pen turns. from the deep floor (6340,618) the climb opens —
# a steady riser, no holds, two octaves up (156 px = 2x78).
# A: the leave — at once, like n7's leave: the climb doesn't linger on the ground.
# B: the riser — even pace, hand wobble only, y never repeats, never dips:
#    the climb does not rest.
# C: crossings mid-ink, unmarked: the floor (540) and the shelf (498) pass
#    under the pen between points. the heights never notice.
# D: the end ON the terrace (462) — the rung the descent settled on in n5 —
#    but touched, not taken: no hold, the next stretch continues the climb.
PTS = [
    (6340, 618),
    (6404, 603),
    (6468, 587),
    (6532, 572),
    (6596, 556),
    (6660, 541),
    (6724, 524),
    (6788, 508),
    (6852, 492),
    (6916, 478),
    (6980, 462),
]
assert len(PTS) == 11
assert all(b[0] > a[0] for a, b in zip(PTS, PTS[1:])), 'x not strictly increasing'
assert all(b[1] < a[1] for a, b in zip(PTS, PTS[1:])), 'a riser: y strictly decreasing'
assert PTS[0] == (6340, 618), 'seam: opens on the deep floor rest'
assert PTS[-1] == (6980, 462), 'ends on the terrace height, touched not taken'
assert max(y for _, y in PTS) == 618, 'low point is the seam (the deep floor)'
assert min(y for _, y in PTS) == 462, 'high point is the terrace end'
for rung in (540, 498):
    assert any(min(a[1], b[1]) < rung < max(a[1], b[1])
               for a, b in zip(PTS, PTS[1:])), 'rung %d crossed mid-ink' % rung
assert PTS[-1][0] <= W_NEW - 140, 'headroom on the widened paper'

pts_str = ' '.join('%d,%d' % p for p in PTS)
line = '    <polyline data-tick="n8" points="%s" />\n' % pts_str

src = open('work/scroll-2.svg').read()

# widen: viewBox and rect together, each asserted count==1 before replace
assert src.count('viewBox="0 0 %d 640"' % W_OLD) == 1
assert src.count('width="%d"' % W_OLD) == 1
src = src.replace('viewBox="0 0 6480 640"', 'viewBox="0 0 7120 640"')
src = src.replace('width="6480"', 'width="7120"')

# insert as text before the anchor; anchor read from bytes, asserted once
anchor = '\n  </g>\n</svg>\n'
assert src.endswith(anchor)
assert src.count(anchor) == 1
out = src[:-len(anchor)] + '\n' + line.rstrip('\n') + anchor

open('/tmp/scroll-2-built.svg', 'w').write(out)
open('assets/n8-points.txt', 'w').write('\n'.join('%d,%d' % p for p in PTS) + '\n')
print('built: %d points, x %d -> %d, paper %d' % (len(PTS), PTS[0][0], PTS[-1][0], W_NEW))
