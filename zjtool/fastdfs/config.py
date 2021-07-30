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
from pathlib import Path

from zjtool.utils import console

USER_PATH = Path('~/.zjtool').expanduser()
USER_PATH.mkdir(exist_ok=True)

CONFIG_PATH = USER_PATH / 'config.json'
if not CONFIG_PATH.exists():
    CONFIG = {
        'fs_ip': 'http://192.168.2.23',
        'fs_port': '8088',
        'fs_group': 'group1',
        'fs_scene': 'default',
        'db_ip': '192.168.2.23',
        'db_port': '27017',
        'db_user': 'admin',
        'db_pwd': 'abc123',
        'ed_secret': 'aksdfiahwekfalkhdfljsdbvjxiuaeoiflskdfls',
    }
    with CONFIG_PATH.open('w') as F:
        json.dump(CONFIG, F, indent=4, ensure_ascii=False)
else:
    with CONFIG_PATH.open('r') as F:
        CONFIG = json.load(F)


def show():
    console.print(json.dumps(CONFIG, indent=4, ensure_ascii=False))


def update(kv):
    assert len(kv) % 2 == 0
    opts = dict(zip(kv[0::2], kv[1::2]))
    CONFIG.update(opts)
    with CONFIG_PATH.open('w') as F:
        json.dump(CONFIG, F, indent=4, ensure_ascii=False)
