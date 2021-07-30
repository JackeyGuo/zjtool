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

import tensorrt as trt

from zjtool.utils import console

TRT_LOGGER = trt.Logger(trt.Logger.WARNING)


def build_engine(
        onnx_file_path,
        engine_file_path,
        convert_mode,
        dynamic_shapes=False,
        max_batch_size=1,
        calibrator=None,
):
    """Takes an ONNX file and creates a TensorRT engine to run inference with"""
    convert_mode = convert_mode.lower()
    assert convert_mode in ['fp32', 'fp16', 'int8'], 'mode should be in ["fp32", "fp16", "int8"]'

    explicit_batch = 1 << (int)(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH) if dynamic_shapes else 0
    with trt.Builder(TRT_LOGGER) as builder, \
            builder.create_network(explicit_batch) as network, \
            trt.OnnxParser(network, TRT_LOGGER) as parser:

        builder.max_workspace_size = 1 << 31
        builder.max_batch_size = max_batch_size
        builder.strict_type_constraints = True

        if convert_mode == 'int8':
            assert (builder.platform_has_fast_int8 == True), 'platform not support int8'
            builder.int8_mode = True
            assert (calibrator is not None)
            builder.int8_calibrator = calibrator
        elif convert_mode == 'fp16':
            assert (builder.platform_has_fast_fp16 == True), 'platform not support fp16'
            builder.fp16_mode = True

        # Parse model file
        if not os.path.exists(onnx_file_path):
            console.print(f'ONNX file {onnx_file_path} not found, please run yolov3_to_onnx.py first to generate it.',
                          style='danger')
            exit(0)

        console.print(f'Loading ONNX file from path {onnx_file_path}...', style='info')
        with open(onnx_file_path, 'rb') as model:
            console.print('Beginning ONNX file parsing', style='info')
            ret = parser.parse(model.read())
            if not ret:
                console.print("Parser ONNX model failed.", style='danger')
                console.print(parser.get_error(0), style='danger')
                exit(0)

        console.print("Completed parsing of ONNX file", style='info')
        console.print(f"Building an engine from file {onnx_file_path}; this may take a while...", style='info')

        engine = builder.build_cuda_engine(network)
        if engine is None:
            console.print("Creating engine failed.", style='danger')
            exit(0)

        console.print("Completed creating Engine", style='info')
        with open(engine_file_path, "wb") as f:
            f.write(engine.serialize())
        return engine


def get_engine(
        onnx_file_path,
        engine_file_path,
        convert_mode,
        dynamic_shapes=False,
        max_batch_size=1,
        calibrator=None,
):
    """Attempts to load a serialized engine if available, otherwise builds a new TensorRT engine and saves it."""

    if os.path.exists(engine_file_path):
        # If a serialized engine exists, use it instead of building an engine.
        console.print(f"Reading engine from file {engine_file_path}", style='info')
        with open(engine_file_path, "rb") as f, trt.Runtime(TRT_LOGGER) as runtime:
            return runtime.deserialize_cuda_engine(f.read())
    else:
        return build_engine(
            onnx_file_path,
            engine_file_path,
            convert_mode,
            dynamic_shapes,
            max_batch_size,
            calibrator,
        )
