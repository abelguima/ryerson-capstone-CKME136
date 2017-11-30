# *******************************************************************
# ** Guimaraes, Abel & Ghassem, Tofighi (2017)                     **                                                             **
# ** Implementing filter image for Transport Security TSA analysis **
# ** Python and scikits image script for digital image analysis    **                                                   **
# *******************************************************************

import numpy as np
from skimage.morphology import reconstruction
from scipy.ndimage import gaussian_filter
from scipy import ndimage
from skimage.measure import label
from skimage.measure import regionprops

# @jit(["float32(float32)"], nopython=False)
def clean_image(img, of='mean'):
    img = gaussian_filter(img, 0.99)
    if of.__eq__('mean'):
        thresh = np.mean(img) * 5
    else:
        thresh = np.percentile(img, 99)

    img[img < thresh] = 0
    img[img >= thresh] = 1

    # Remove small white regions
    open_img = ndimage.binary_opening(img)
    # Remove small black hole
    img = ndimage.binary_closing(open_img)

    seed = np.copy(img)
    seed[1:-1, 1:-1] = img.min()
    mask = img

    dilated = reconstruction(seed, mask, method='dilation')
    img_diff = img - dilated

    # label image regions
    label_image = label(img_diff)
    for region in regionprops(label_image):

        # skip small images
        if region.area < 1000:
            img_diff[tuple(region.coords.T)] = 0

    return img_diff
