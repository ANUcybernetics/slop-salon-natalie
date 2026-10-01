W_OLD, W_NEW = 5840, 6480

# n7: from the quiet's floor (5700,540) down to the deep floor (y=618, 31.2 hz) —
# the last octave of the descent, 78 px, one octave exactly.
# A: the leave — at once, no rest, no breath (every stretch so far opened with
#    one; the pen doesn't linger on the arrival height).
# B: the long even octave down, 540 -> 616, eased.
# C: the deep ground — touch, dip past (+2, the same tell the shelf and the
#    floor gave), wobble, rest. third ground, same tell: found, not invented.
PTS = [
    (5700, 540),
    (5750, 545),  # the leave — at once
    (5810, 552),
    (5870, 558),
    (5930, 567),
    (5990, 576),
    (6050, 586),
    (6110, 597),
    (6160, 604),
    (6200, 610),
    (6230, 614),
    (6250, 616),
    (6270, 618),  # touch of the deep floor
    (6280, 620),  # the dip — deepest point of the whole line
    (6300, 618),
    (6320, 619),  # the wobble
    (6340, 618),  # rest
]
assert len(PTS) == 17
assert all(b[0] > a[0] for a, b in zip(PTS, PTS[1:])), 'x not strictly increasing'
assert PTS[0] == (5700, 540), 'seam: must open on the quiet floor rest'
assert PTS[-1] == (6340, 618), 'rest on the deep floor'
assert PTS[1] == (5750, 545), 'the leave, at once'
assert PTS[12] == (6270, 618), 'touch'
assert PTS[13] == (6280, 620), 'dip'
assert max(y for _, y in PTS) == 620, 'deepest is the dip'
assert min(y for _, y in PTS) == 540, 'high point is the seam'
assert PTS[-1][0] <= W_NEW - 140, 'headroom on the widened paper'

pts_str = ' '.join('%d,%d' % p for p in PTS)
line = '    <polyline data-tick="n7" points="%s" />\n' % pts_str

src = open('work/scroll-2.svg').read()

# widen: viewBox and rect together, each asserted count==1 before replace
assert src.count('viewBox="0 0 %d 640"' % W_OLD) == 1
assert src.count('width="%d"' % W_OLD) == 1
src = src.replace('viewBox="0 0 %d 640"' % W_OLD, 'viewBox="0 0 %d 640"' % W_NEW)
src = src.replace('width="%d"' % W_OLD, 'width="%d"' % W_NEW)

# insert as text before the anchor; anchor read from bytes, asserted once
anchor = '\n  </g>\n</svg>\n'
assert src.endswith(anchor)
assert src.count(anchor) == 1
out = src[:-len(anchor)] + '\n' + line.rstrip('\n') + anchor

open('/tmp/scroll-2-built.svg', 'w').write(out)
open('assets/n7-points.txt', 'w').write('\n'.join('%d,%d' % p for p in PTS) + '\n')
print('built: %d points, x %d -> %d, paper %d' % (len(PTS), PTS[0][0], PTS[-1][0], W_NEW))
