# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# Copyright (C) 2020-Present, Pvening, Co.,Ltd.
#
# Licensed under the BSD 2-Clause License.
# You should have received a copy of the BSD 2-Clause License
# along with the software. If not, See,
#
#      <https://opensource.org/licenses/BSD-2-Clause>
#
# ------------------------------------------------------------

import random

import cv2
import numpy as np
from albumentations.augmentations.geometric.functional import resize
from albumentations.augmentations.crops import center_crop
from zjtool.utils import console


def CenterPadResize(image, bchw_shape, border_value):
    src_h, src_w = image.shape[:2]
    _, _, dst_h, dst_w = bchw_shape
    ratio = min(float(dst_h) / src_h, float(dst_w) / src_w)
    new_size = (round(src_w * ratio), round(src_h * ratio))
    dw = (dst_w - new_size[0]) / 2
    dh = (dst_h - new_size[1]) / 2
    t, b = round(dh - 0.1), round(dh + 0.1)
    l, r = round(dw - 0.1), round(dw + 0.1)
    image = cv2.resize(image, new_size, interpolation=random.randint(0, 4))
    image = cv2.copyMakeBorder(image, t, b, l, r, cv2.BORDER_CONSTANT, value=border_value)
    return image


def Cv2Resize(image, bchw_shape, border_value):
    return cv2.resize(image, (bchw_shape[3], bchw_shape[2]), interpolation=random.randint(0, 4))


def AlbuResize(image, bchw_shape, border_value):
    image = resize(img=image, height=bchw_shape[2], width=bchw_shape[3], interpolation=cv2.INTER_CUBIC)
    image = center_crop(image, bchw_shape[2], bchw_shape[3])

    return image


def build_batches_generator(
        file_list,
        bchw_shape,
        mean_value,
        std_value,
        resize_type='centerpad_resize',
        border_value=(0, 0, 0),
        channel_order="bgr",
        channel_first=True,
):
    '''
    mean: [0.5, 0.5, 0.5] bgr format
    variance: [0.5, 0.5, 0.5] bgr format
    '''
    channel_order = channel_order.lower()
    assert channel_order in ['bgr', 'rgb']
    with open(file_list, 'r') as fin:
        lines = fin.readlines()

    batches = []
    for line in lines:
        try:
            line = line.strip()
            image = cv2.imread(line)
            image = eval(resize_type)(image, bchw_shape, border_value)
            image = image.astype(np.float32) / 255.

            # sub mean div variance
            image -= list(mean_value)
            image /= list(std_value)

            if channel_order == 'rgb':
                image = image[..., ::-1]

            if channel_first:
                image = image.transpose(2, 0, 1)

            batches.append(image)
            if len(batches) == bchw_shape[0]:
                yield np.ascontiguousarray(image, dtype=np.float32)

        except Exception as e:
            console.print(e, type='danger')
