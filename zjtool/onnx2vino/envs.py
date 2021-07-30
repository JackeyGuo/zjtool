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
import sys
import shutil
import subprocess

CONTAINER_NAME = os.getenv('CONTAINER_NAME')
CONTAINER_MNT_OUT, CONTAINER_MNT_INP = os.getenv('DOCKER_MOUNT_POINT').split(':')


def call_shell(cmd: list):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while popen.poll() is None:
        ret = popen.stdout.readline().decode('GBK')
        sys.stdout.write(ret)
    if popen.poll() != 0:
        err = popen.stderr.read().decode('GBK')
        sys.stdout.write(err)
        raise BrokenPipeError


def cprint(values, color='red'):
    if color == 'red':
        print(f'\033[0;31m{values}\033[0m')


def copytree(src, dst, dirs_exist_ok=False):
    shutil.copytree(src, dst, dirs_exist_ok=dirs_exist_ok)
    cprint('COPY TREE:')
    cprint(f'SRC: {src}')
    cprint(f'DST: {dst}')


def copyfile(src, dst):
    shutil.copy(src, dst)
    cprint('COPY FILE:')
    cprint(f'SRC: {src}')
    cprint(f'DST: {dst}')


def path_inp_docker(src_path: str):
    return os.path.join(CONTAINER_MNT_INP, src_path.rsplit(CONTAINER_MNT_OUT)[-1])


def path_out_docker(src_path: str):
    return os.path.join(CONTAINER_MNT_OUT, src_path.rsplit(CONTAINER_MNT_INP)[-1])


def setup_docker():
    print(f'\033[0;31m** Setup Container **\033[0m')

    p = subprocess.Popen(
        ['sudo', 'docker', 'inspect', '--format', '{{.State.Running}}', f'{CONTAINER_NAME}'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    p.wait()
    r = p.stdout.read().decode('UTF-8').strip()
    if r == 'true':
        print(f'\033[0;31m** Container {CONTAINER_NAME} Already Running. **\033[0m')
        return
    else:
        cmd = [
            'sudo', 'docker', 'run', '-itd',
            '--name', f'{CONTAINER_NAME}',
            '-u', 'root',
            '-v', f'{CONTAINER_MNT_OUT}:{CONTAINER_MNT_INP}',
            '--privileged=true',
            'openvino/ubuntu18_dev', '/bin/bash'
        ]
        strcmd = ' '.join(cmd)
        print(f'\033[0;31m** Start Container {CONTAINER_NAME} With Command Line: **\033[0m')
        print(f'\033[0;31m{strcmd}\033[0m')
        call_shell(cmd)
