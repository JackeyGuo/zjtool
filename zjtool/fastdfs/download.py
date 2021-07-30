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
import os
from pathlib import Path
from urllib.request import urlopen

import requests
from rich.progress import Progress

from zjtool.cryption import do_decrypt
from zjtool.utils import console, XSTR
from .config import CONFIG
from .mgdb import file_info


def _download(url: str, dst: Path):
    try:
        assert not dst.is_dir()
        file_size = int(urlopen(url).info().get('Content-Length', -1))
        first_byte = os.path.getsize(str(dst)) if (dst.exists()) else 0
        headers = {"Range": "bytes={}-{}".format(first_byte, file_size)}
        req = requests.get(url, headers=headers, stream=True)
        chunk_size = 1024
        with Progress() as progress:
            console.print('[green]GET [yellow]{}'.format(url))
            task = progress.add_task("[bold blue][Downloading...]", total=file_size)
            progress.update(task, advance=first_byte)
            with dst.open('ab') as fw:
                for i, chunk in enumerate(req.iter_content(chunk_size)):
                    if chunk:
                        fw.write(chunk)
                    progress.update(task, advance=chunk_size)
    except Exception:
        console.print_exception()
        return False
    return True


def download_from_url(url: str, dst: str, dec: bool):
    dst = Path(dst)
    if dec:
        with do_decrypt(dst, CONFIG['ed_secret']) as ef:
            assert _download(url, ef)
    else:
        assert _download(url, dst)


def download_from_md5(md5: str, dst: str, dec: bool):
    info = file_info(md5=md5)
    if info is None:
        raise FileNotFoundError
    download_from_url(info['url'], Path(dst) / info['name'], dec)


def download_from_json(jsfile: str, branch: str):
    import re
    jsfile = Path(jsfile)
    assert jsfile.exists() and branch

    with jsfile.open('r') as jf:
        json_str = ''
        for line in jf.readlines():
            if not re.match(r'\s*//', line) and not re.match(r'\s*\n', line):
                xline = XSTR(line)
                json_str += xline.rmCmt()
        cfg = json.loads(json_str)
        console.print(json.dumps(cfg, indent=4, ensure_ascii=False))

        for k, v in cfg.items():
            try:
                if branch not in v['custom_params']:
                    console.print('{} not in {}'.format(branch, k))
                    continue
                url = v['custom_params'][branch]
                dst = jsfile.parent / v['custom_params']['model_path']

                if not dst.parent.exists():
                    os.makedirs(str(dst.parent.absolute()))

                download_from_url(url, dst, not bool(v['custom_params']['model_encrypted']))
            except Exception:
                console.print_exception()
