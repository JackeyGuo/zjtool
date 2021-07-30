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

from collections import namedtuple

PreLoadParams = namedtuple(
    'PreLoadParams',
    ['file_list', 'input_shape', 'mean', 'variance', 'channel_order', 'channel_first']
)

ConvertParams = namedtuple(
    'ConvertParams',
    ['onnx_file', 'engine_file', 'mode', 'dynamic_shape', 'max_batch_size', 'calibrator']
)
