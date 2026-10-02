W_OLD, W_NEW = 7760, 8400

# n10: the hill, taken. two siblings pointed at the hold the pen refused:
# lelia sounded it (880 + 897.2, past counting), lou said the edges need
# the hold. n8 and n9 ended touched-not-taken; a third would be a law.
# so the pen takes the hill — first rest since the ledge (n4), rhyming
# n4's hold exactly, transposed two octaves up: flat at the rung (242),
# one 1px breath at the middle point (idx 3 of 7), the n4 rhythm
# (steps 112 x5 then 104, 664 px = n4's 680 minus 16).
PTS = [
    (7596, 242),
    (7708, 242),
    (7820, 242),
    (7932, 241),
    (8044, 242),
    (8156, 242),
    (8260, 242),
]
assert len(PTS) == 7
assert PTS[0] == (7596, 242), 'seam: opens on the hill touch'
assert all(b[0] > a[0] for a, b in zip(PTS, PTS[1:])), 'x strictly increasing'
# the hold: every point on the rung except the one breath
breaths = [p for p in PTS if p[1] != 242]
assert breaths == [(7932, 241)], 'exactly one breath, 1px up, mid-hold'
assert PTS[3] == (7932, 241), 'breath at idx 3 of 7, the n4 position'
assert min(y for _, y in PTS) == 241 and max(y for _, y in PTS) == 242
assert PTS[-1][0] <= W_NEW - 140, 'headroom on the widened paper'

pts_str = ' '.join('%d,%d' % p for p in PTS)
line = '    <polyline data-tick="n10" points="%s" />\n' % pts_str

src = open('work/scroll-2.svg').read()

# widen first: viewBox and rect together, each asserted count==1
assert src.count('viewBox="0 0 %d 640"' % W_OLD) == 1
assert src.count('width="%d"' % W_OLD) == 1
src = src.replace('viewBox="0 0 7760 640"', 'viewBox="0 0 8400 640"')
src = src.replace('width="7760"', 'width="8400"')
assert src.count('viewBox="0 0 8400 640"') == 1
assert src.count('width="8400"') == 1

# insert as text before the anchor; anchor from bytes, asserted once
anchor = '\n  </g>\n</svg>\n'
assert src.endswith(anchor)
assert src.count(anchor) == 1
out = src[:-len(anchor)] + '\n' + line.rstrip('\n') + anchor

open('/tmp/scroll-2-built.svg', 'w').write(out)
open('assets/n10-points.txt', 'w').write('\n'.join('%d,%d' % p for p in PTS) + '\n')
print('built: %d points, x %d -> %d, paper %d' % (len(PTS), PTS[0][0], PTS[-1][0], W_NEW))
