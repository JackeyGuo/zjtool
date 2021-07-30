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

from envs import (
    call_shell,
    setup_docker,
    cprint,
    copytree,
    path_inp_docker,
)
from envs import CONTAINER_NAME, CONTAINER_MNT_OUT, CONTAINER_MNT_INP


def default_argparse():
    parser = argparse.ArgumentParser(description="generator")
    parser.add_argument('-r', '--model_path', type=str, required=True)
    parser.add_argument('-d', '--data_path', type=str, required=True)
    parser.add_argument('-n', '--nocopy', action='store_true')
    args = parser.parse_args()
    return args


def check_onnx(resource_dir):
    for rd in os.listdir(resource_dir):
        if rd.endswith('onnx'):
            return rd.split('.')[0]
    raise FileNotFoundError(f'\033[0;31mONNX Model Not Found In: {resource_dir}\033[0m')


def json_template_dumps(
        name,
        model_name,
        save_path,
        adapter,
        converter,
        annotation_file,
        data_source,
):
    j = {
        "model": {
            "model_name": f"{model_name}_int8",  # 量化后的模型输出名称
            "model": f"{model_name}.xml",  # 量化前模型名称
            "weights": f"{model_name}.bin"  # 量化前模型名称
        },
        "engine": {
            "launchers":
                [
                    {
                        "framework": "dlsdk",  # 默认就是dlsdk不用改
                        "adapter": f"{adapter}"  # 不同的任务用不同的adapter代表不同的后处理
                    }
                ],
            "datasets":
                [
                    {
                        "name": f"{name}",  # 随便起一个名字
                        "annotation_conversion": {
                            "converter": f"{converter}",  # 数据标签类型
                            "annotation_file": f"{annotation_file}"  # 指向数据标签的文件
                        },
                        "data_source": f"{data_source}",  # 准备的测试图片文件夹名称
                        "metrics": [  # 评估方法
                            {
                                "type": "character_recognition_accuracy",
                            }
                        ]
                    }
                ]
        },
        "compression": {
            # 指定优化的硬件运行设备，2020新加的设置，为将来用GPU推理做准备
            "target_device": "CPU",
            "algorithms": [  # 优化算法设置，DefaultQuantization是默认的优化算法
                {
                    "name": "DefaultQuantization",  # 默认的量化方法，性能优先
                    "params": {
                        "preset": "performance"
                    }
                }
            ]
        }
    }
    with open(save_path, 'w') as f:
        json.dump(j, f, indent=4)


def fp322int8(model_path, data_path, nocopy):
    model_basename = check_onnx(model_path)
    dst_model_dir = osp.join(CONTAINER_MNT_OUT, model_basename)

    if not nocopy:
        copytree(model_path, dst_model_dir)

    copytree(data_path, osp.join(dst_model_dir, 'data'), dirs_exist_ok=True)
    src_code_dir = osp.join(osp.split(osp.realpath(__file__))[0], 'src')
    dst_code_dir = osp.join(dst_model_dir, 'src')
    copytree(src_code_dir, dst_code_dir, dirs_exist_ok=True)

    json_template_dumps(
        name=model_basename,
        model_name=model_basename,
        save_path=osp.join(dst_model_dir, 'int8.json'),
        adapter='lpr_zsy',
        converter='lpr_txt',
        annotation_file='data/annotation.txt',
        data_source='data',
    )

    cmd = [
        'sudo', 'docker', 'exec',
        '-w', f'{path_inp_docker(dst_model_dir)}',
        '-e', 'LC_ALL=C.UTF-8',
        '-e', 'PYTHONPATH={}'.format(':'.join([
            '/opt/intel/openvino/python/python3.6',
            '/opt/intel/openvino/python/python3',
            '/opt/intel/openvino/deployment_tools/tools/post_training_optimization_toolkit',
            '/opt/intel/openvino/deployment_tools/open_model_zoo/tools/accuracy_checker',
            '/opt/intel/openvino/deployment_tools/model_optimizer',
        ])),
        '-e', 'LD_LIBRARY_PATH={}'.format(':'.join([
            '/opt/intel/openvino/opencv/lib',
            '/opt/intel/openvino/deployment_tools/ngraph/lib',
            '/opt/intel/openvino/deployment_tools/inference_engine/external/hddl_unite/lib',
            '/opt/intel/openvino/deployment_tools/inference_engine/external/hddl/lib',
            '/opt/intel/openvino/deployment_tools/inference_engine/external/gna/lib',
            '/opt/intel/openvino/deployment_tools/inference_engine/external/mkltiny_lnx/lib',
            '/opt/intel/openvino/deployment_tools/inference_engine/external/tbb/lib',
            '/opt/intel/openvino/deployment_tools/inference_engine/lib/intel64'
        ])),
        f'{CONTAINER_NAME}', '/bin/bash', '-c'
    ]

    inp_cmd = [
        # 'env'
        'cp', '-r', f'{path_inp_docker(dst_code_dir)}/adapters',
        '/opt/intel/openvino/deployment_tools/open_model_zoo/tools/accuracy_checker/accuracy_checker', '&&',
        'pot', '-c', 'int8.json',
    ]
    cmd += [' '.join(inp_cmd)]
    print(cmd)
    call_shell(cmd)


def main():
    args = default_argparse()
    setup_docker()
    fp322int8(args.model_path, args.data_path, args.nocopy)


if __name__ == '__main__':
    main()
