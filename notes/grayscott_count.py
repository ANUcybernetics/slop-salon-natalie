import sys

import numpy as np
from PIL import Image
from scipy import ndimage

img = np.asarray(Image.open(sys.argv[1]).convert("RGB"), float)
t = (img[..., 0] - 14) / (236 - 14)
mask = t > float(sys.argv[2]) if len(sys.argv) > 2 else t > 0.5
labels, n = ndimage.label(mask, structure=np.ones((3, 3)))
areas = sorted(np.bincount(labels.ravel())[1:], reverse=True)
areas = [a for a in areas if a >= 100]
print(f"{sys.argv[1]}: {len(areas)} components, areas {areas}")
