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
import tempfile

import pycuda.driver as cuda
import tensorrt as trt
import pycuda.autoinit


class IInt8Calibrator2(trt.IInt8EntropyCalibrator2):
    def __init__(self, batches_generator, bchw_shape):
        super(IInt8Calibrator2, self).__init__()

        self.shape = bchw_shape
        self.device_input = cuda.mem_alloc(trt.volume(self.shape) * trt.float32.itemsize)

        self.cache_file = tempfile.mktemp()
        self.batches = batches_generator

    def get_batch(self, names, p_str=None):
        try:
            data = next(self.batches)
            cuda.memcpy_htod(self.device_input, data)
            return [int(self.device_input)]
        except StopIteration:
            return None

    def get_batch_size(self):
        return self.shape[0]

    def read_calibration_cache(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, "rb") as f:
                return f.read()

    def write_calibration_cache(self, cache):
        with open(self.cache_file, "wb") as f:
            f.write(cache)


def build_calibrator(calibrator_type, batches_generator, bchw_shape):
    return eval(calibrator_type)(batches_generator, bchw_shape)
