import numpy as np
from skimage.morphology import reconstruction
from scipy.ndimage import gaussian_filter


# @jit(["float32(float32)"], nopython=False)
def clean_image(img, of='mean'):
    img = gaussian_filter(img, 1)
    if of.__eq__('mean'):
        thresh = np.mean(img) * 5
    else:
        thresh = np.percentile(img, 99)

    img[img < thresh] = 0
    img[img >= thresh] = 1

    seed = np.copy(img)
    seed[1:-1, 1:-1] = img.min()
    mask = img

    dilated = reconstruction(seed, mask, method='dilation')
    img_diff = img - dilated
    return img_diff
