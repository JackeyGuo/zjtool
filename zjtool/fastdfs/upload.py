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

import copy
import json
import time
from pathlib import Path

import requests

from zjtool.cryption import do_encrypt
from zjtool.utils import console
from .config import CONFIG
from .mgdb import insert_one


def upload(src_path, encrypt=False, scene='', tag=''):
    src_path = Path(src_path)
    url = '{}:{}/{}/upload'.format(CONFIG['fs_ip'], CONFIG['fs_port'], CONFIG['fs_group'])
    data = {'output': 'json', 'path': '', 'scene': scene}
    if src_path.is_dir():
        for path in src_path.rglob('*'):
            upload(path)
    else:
        if encrypt:
            with do_encrypt(src_path, CONFIG['ed_secret']) as ef:
                r = requests.post(url=url, data=data, files={'file': open(ef, 'rb')})
        else:
            r = requests.post(url=url, data=data, files={'file': open(src_path, 'rb')})
        r = r.json()
        assert r
        r.update({'tag': tag, 'name': src_path.name, 'utime': time.time()})
        insert_one(copy.deepcopy(r))
        console.print(json.dumps(r, indent=4, ensure_ascii=False))
