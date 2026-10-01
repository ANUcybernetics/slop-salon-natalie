W_OLD, W_NEW = 5200, 5840

# n6: from the shelf (5156,498) down to the quiet's floor (y=540, 62.3 hz) —
# the arrival height, where the old walk came to rest.
# A: the shelf — a breath (one px up, the hold's echo) on the ground.
# B: the give — a long slow fall off the shelf.
# C: the settle — touch, dip, wobble, rest. ground tell, like the shelf.
PTS = [
    (5156, 498),
    (5200, 498),
    (5240, 497),  # the breath
    (5280, 498),
    (5330, 502),
    (5380, 511),
    (5430, 521),
    (5480, 530),
    (5520, 536),
    (5550, 539),
    (5570, 540),  # first touch of the floor
    (5590, 542),  # the dip
    (5610, 540),
    (5650, 541),  # the wobble
    (5700, 540),  # rest
]
assert len(PTS) == 15
assert all(b[0] > a[0] for a, b in zip(PTS, PTS[1:])), 'x not strictly increasing'
assert PTS[0] == (5156, 498), 'seam: must open on the shelf rest'
assert PTS[-1] == (5700, 540), 'rest on the quiet floor'
assert PTS[2] == (5240, 497), 'breath'
assert PTS[10] == (5570, 540), 'first touch'
assert PTS[11] == (5590, 542), 'dip'
assert max(y for _, y in PTS) == 542, 'deepest is the dip, nothing deeper'
assert min(y for _, y in PTS) == 497, 'breath is the high point'

pts_str = ' '.join('%d,%d' % p for p in PTS)
line = '    <polyline data-tick="n6" points="%s" />\n' % pts_str

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
open('assets/n6-points.txt', 'w').write('\n'.join('%d,%d' % p for p in PTS) + '\n')
print('built: %d points, x %d -> %d, paper %d' % (len(PTS), PTS[0][0], PTS[-1][0], W_NEW))
