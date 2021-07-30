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

import json
import os

from zjtool.utils import console
from .batches import build_batches_generator
from .calibrator import build_calibrator
from .engine import build_engine


def main_convert(opts):
    assert os.path.exists(opts['onnx_file']), 'ONNX File Not Found!.'
    console.print(json.dumps(opts, indent=4, ensure_ascii=False))
    calibrator = None
    if opts['quant_mode'] == 'int8':
        calibrator = build_calibrator(
            opts['calibrator_type'],
            build_batches_generator(
                file_list=opts['file_list'],
                bchw_shape=opts['bchw_shape'],
                mean_value=opts['mean_value'],
                std_value=opts['std_value'],
                resize_type=opts['resize_type'],
                border_value=opts['border_value'],
                channel_order=opts['channel_order'],
                channel_first=opts['channel_first'],
            ),
            opts['bchw_shape']
        )
    build_engine(
        opts['onnx_file'],
        opts['engine_file'],
        opts['quant_mode'],
        opts['shape_dynamic'],
        opts['bchw_shape'][0],
        calibrator,
    )
