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

import os
import cv2
import numpy as np


def resize_img(img, dst_size=(100, 32)):
    src_h, src_w = img.shape[:2]

    nw = int(np.ceil(dst_size[1] * src_w / src_h))
    nw = dst_size[0] if nw > dst_size[0] else nw

    resized = cv2.resize(img, (nw, dst_size[1]))
    empty = np.ones((dst_size[1], dst_size[0], 3), dtype=img.dtype) * 127
    empty[:, :nw, :] = resized
    return empty


def walk_dirs(paths, suffix):
    dir_map = {}

    if not isinstance(paths, list):
        paths = [paths]

    for path in paths:
        for (root, dirs, files) in os.walk(path):
            for item in files:
                if item.endswith(suffix):
                    d = os.path.abspath(os.path.join(root, item))
                    # dir_map[item.split('.')[0]] = d
                    dir_map[os.path.splitext(item)[0]] = d
    return dir_map


if __name__ == '__main__':
    # gt_files = walk_dirs('/mnt/nvme1n1/zhangsy/deep-text-recognition-benchmark/gt', 'txt')
    gt_files = [
        '/10t/zhangsy/data/plates/cc_0724_single.txt',
        '/10t/bss/plate/model_data/pic_clean/single/same/single.txt',
        '/10t/zhangsy/plate/plate_shengfen_ocr_test.txt',
        '/home/bss/10t/plate/model_data/v6/v6_single.txt',
        '/10t/bss/plate/Temp/imgaug_deal/train_list/imgaug_train.txt',
        '/10t/bss/plate/Temp/imgaug_deal/train_list/rare_province.txt',
        '/10t/bss/plate/Temp/imgaug_deal/test_list/imgaug_train_error.txt',
        '/10t/bss/plate/Temp/imgaug_deal/test_list/rare_province_error.txt',
    ]

    save_dir = '/home/xupeichao/ws/onnx2openvino/slpr_128x32/data'
    os.makedirs(save_dir, exist_ok=True)

    all_lines = []
    for gf in gt_files:
        with open(gf, 'r') as f:
            lines = f.readlines()
            lines = np.random.choice(lines, size=100)
            all_lines.extend(lines)

    count = 0
    with open(os.path.join(save_dir, 'annotation.txt'), 'w', encoding='utf-8') as fout:
        for line in all_lines:
            impt, labe = line.strip().split('\t')

            image = cv2.imread(impt)
            image = resize_img(image, (128, 32))

            save_path = os.path.join(save_dir, '{}.jpg'.format(count))
            save_path = os.path.abspath(save_path)
            print(save_path, image.shape)

            fout.write(
                '{} {}\n'.format(
                    os.path.split(save_path)[-1], labe
                )
            )
            cv2.imwrite(save_path, image)

            count += 1
