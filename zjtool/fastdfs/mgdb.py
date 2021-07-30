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

from pymongo import MongoClient

from .config import CONFIG

_DBClient = MongoClient(
    host=CONFIG['db_ip'],
    port=int(CONFIG['db_port']),
    username=CONFIG['db_user'],
    password=CONFIG['db_pwd'],
)

_DB = _DBClient['gofastdfs'].data


def insert_one(v):
    query = file_info(v['md5'])
    if query is None:
        _DB.insert_one(v)


def file_info(md5: str):
    return _DB.find_one({'md5': md5})


def file_infos(md5: str = None, scene: str = None, tag: str = None) -> dict:
    ret = {}
    if md5:
        query = [_DB.find_one({'md5': md5})]
    else:
        match = {}
        if scene: match.update({'scene': scene})
        if tag: match.update({'tag': tag})
        query = _DB.find(match).sort([('utime', 1)])

    for i, r in enumerate(query):
        r.pop('_id')
        r.pop('domain')
        r.pop('retcode')
        r.pop('retmsg')
        r.pop('src')
        ret[str(i)] = r
    return ret


def delete_all():
    _DB.delete_many({})
