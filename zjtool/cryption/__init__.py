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


from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory

from zjtool.utils import call_shell

ENCRYPT = Path(__file__).absolute().parent / 'encrypt'
DECRYPT = Path(__file__).absolute().parent / 'decrypt'


@contextmanager
def do_encrypt(src_path: Path, secret: str):
    with TemporaryDirectory() as dirname:
        tmpname = Path(dirname) / (str(src_path.name) + '.encrypt')
        call_shell([
            str(ENCRYPT),
            secret,
            str(src_path),
            str(tmpname),
        ])
        yield tmpname


@contextmanager
def do_decrypt(src_path: Path, secret: str):
    with TemporaryDirectory() as dirname:
        tmpname = Path(dirname) / (str(src_path.name) + '.decrypt')
        yield tmpname
        call_shell([
            str(DECRYPT),
            secret,
            str(tmpname),
            str(src_path),
        ])
