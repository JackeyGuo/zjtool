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


import argparse
import os
import json
import os.path as osp

from fp32 import onnx2fp32
from int8 import fp322int8
from envs import call_shell, setup_docker
from envs import CONTAINER_NAME, CONTAINER_MNT_OUT, CONTAINER_MNT_INP


def default_argparse():
    parser = argparse.ArgumentParser(description="generator")
    parser.add_argument('-i', '--input', type=str, required=True)
    parser.add_argument('-d', '--data_path', type=str, required=True)
    parser.add_argument('-s', '--shape', type=str, default='1,3,32,320')
    parser.add_argument('-m', '--mean', type=str, default='127.5,127.5,127.5')
    parser.add_argument('-v', '--scale', type=str, default='127.5,127.5,127.5')
    args = parser.parse_args()
    return args


def main():
    args = default_argparse()
    setup_docker()
    onnx2fp32(args.input, args.shape, args.mean, args.scale)
    model_filename = osp.split(args.input)[-1]
    model_basename = model_filename.split('.')[0]
    dst_model_dir = osp.join(CONTAINER_MNT_OUT, model_basename)
    fp322int8(dst_model_dir, args.data_path, nocopy=True)


if __name__ == '__main__':
    main()
