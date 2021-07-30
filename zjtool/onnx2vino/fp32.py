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
import os.path as osp

from envs import (
    call_shell,
    setup_docker,
    copyfile,
    path_inp_docker,
)
from envs import CONTAINER_NAME, CONTAINER_MNT_OUT


def default_argparse():
    parser = argparse.ArgumentParser(description="generator")
    parser.add_argument('-i', '--input', type=str, required=True)
    parser.add_argument('-s', '--shape', type=str, default='1,3,32,128')
    parser.add_argument('-m', '--mean', type=str, default='127.5,127.5,127.5')
    parser.add_argument('-v', '--scale', type=str, default='127.5,127.5,127.5')
    args = parser.parse_args()
    return args


def onnx2fp32(input, shape, mean, scale):
    model_filename = osp.split(input)[-1]
    model_basename = model_filename.split('.')[0]

    dst_model_dir = osp.join(CONTAINER_MNT_OUT, model_basename)
    os.makedirs(dst_model_dir)

    dst_model_path = os.path.join(dst_model_dir, model_filename)
    copyfile(input, dst_model_path)

    cmd = [
        'sudo', 'docker', 'exec', f'{CONTAINER_NAME}', '/bin/bash', '-c'
    ]
    inp_cmd = [
        'python3',
        '/opt/intel/openvino_2021.1.110/deployment_tools/model_optimizer/mo_onnx.py',
        '--input_model', path_inp_docker(dst_model_path),
        '--output_dir', path_inp_docker(dst_model_dir),
        '--model_name', f'{model_basename}',
        '--input_shape', f'[{shape}]',
        '--mean_values', f'[{mean}]',
        '--scale_values', f'[{scale}]',
        '--reverse_input_channels',
    ]
    cmd += [' '.join(inp_cmd)]
    call_shell(cmd)


def main():
    args = default_argparse()
    setup_docker()
    onnx2fp32(args.input, args.shape, args.mean, args.scale)


if __name__ == '__main__':
    main()
