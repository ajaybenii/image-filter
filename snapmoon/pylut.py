import os
import logging
from typing import Union

import numpy as np
from PIL import Image
from colour.io.luts.iridas_cube import read_LUT_IridasCube, LUT3D, LUT3x1D

def read_lut(lut_path, clip=False):
    """
    Reads a LUT from the specified path, returning instance of LUT3D or LUT3x1D
    <lut_path>: the path to the file from which to read the LUT (
    <clip>: flag indicating whether to apply clipping of LUT values, limiting all values to the domain's lower and
        upper bounds
    """
    lut: Union[LUT3x1D, LUT3D] = read_LUT_IridasCube(lut_path)
    lut.name = os.path.splitext(os.path.basename(lut_path))[0]  # use base filename instead of internal LUT name

    if clip:
        if lut.domain[0].max() == lut.domain[0].min() and lut.domain[1].max() == lut.domain[1].min():
            lut.table = np.clip(lut.table, lut.domain[0, 0], lut.domain[1, 0])
        else:
            if len(lut.table.shape) == 2:  # 3x1D
                for dim in range(3):
                    lut.table[:, dim] = np.clip(lut.table[:, dim], lut.domain[0, dim], lut.domain[1, dim])
            else:  # 3D
                for dim in range(3):
                    lut.table[:, :, :, dim] = np.clip(lut.table[:, :, :, dim], lut.domain[0, dim], lut.domain[1, dim])

    return lut

def process_image(im, output_path, lut_name, log=False, no_prefix=False, quality=95):
    """Opens the image at <image_path>, transforms it using the passed
    <lut> with trilinear interpolation, and saves the image at
    <output_path>, or if it is None, then the same folder as <image_path>.
    If <thumb> is greater than zero, then the image will be resized to have
    a max height or width of <thumb> before being transformed. Iff <log> is
    True, the image will be changed to log colorspace before the LUT.
    <image_path>: path to input image file
    <output_path>: path to output image folder
    <thumb>: max size for image dimension, 0 indicates no resizing
    <lut>: CubeLUT object containing LUT
    <log>: iff True, transform to log colorspace
    """

    logging.info("Processing image:")
    lut_path = f'luts/{lut_name}.CUBE'
    lut = read_lut(lut_path)

    if (im.mode != 'RGB'):
        im = im.convert('RGB')
    logging.debug("Applying LUT: " + lut.name)
    im_array = np.asarray(im, dtype=np.float32) / 255
    is_non_default_domain = not np.array_equal(lut.domain, np.array([[0., 0., 0.], [1., 1., 1.]]))
    dom_scale = None
    if is_non_default_domain:
        dom_scale = lut.domain[1] - lut.domain[0]
        im_array = im_array * dom_scale + lut.domain[0]
    if log:
        im_array = im_array ** (1/2.2)
    im_array = lut.apply(im_array)
    if log:
        im_array = im_array ** (2.2)
    if is_non_default_domain:
        im_array = (im_array - lut.domain[0]) / dom_scale
    im_array = im_array * 255
    new_im = Image.fromarray(np.uint8(im_array))
    new_im.save(output_path, quality=quality)
