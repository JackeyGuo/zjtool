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


import click

from .config import show
from .download import download_from_md5, download_from_url, download_from_json
from .upload import upload as _upload


@click.group()
def fastdfs():
    '''Download and Upload file to FastDFS server.'''
    pass


@fastdfs.command()
@click.option('-f', '--file', type=str, required=True, help='待上传或文件路径')
@click.option('-s', '--scene', type=str, default='default', help='场景(path为空时为默认根目录)')
@click.option('-t', '--tag', type=str, default=None, help='tag标识')
@click.option('-e', '--encrypt', is_flag=True, help='加密上传')
def upload(**kwargs):
    '''
    upload file to fastdfs server.
    '''
    _upload(
        src_path=kwargs['file'],
        encrypt=kwargs['encrypt'],
        scene=kwargs['scene'],
        tag=kwargs['tag'],
    )


@fastdfs.command()
def show_config(**kwargs):
    '''
    show the global config
    '''
    show()


@fastdfs.command()
@click.option('-m', '--md5', type=str, default=None, help='文件md5')
@click.option('-u', '--url', type=str, default=None, help='文件url')
@click.option('-j', '--json', type=str, default=None, help='指定json配置文件')
@click.option('-d', '--dst', type=str, default='.', help='指定保存路径')
@click.option('-s', '--scene', type=str, default=None, help='过滤不符合scene的文件')
@click.option('-t', '--tag', type=str, default=None, help='过滤不符合tag标识的文件')
@click.option('-b', '--branch', type=str, default=None, help='指定业务分支')
@click.option('-e', '--decrypt', is_flag=True, help='下载后解密')
def download(**kwargs):
    '''
    download file using [md5/url/json]
    '''
    if kwargs['json']:
        download_from_json(kwargs['json'], kwargs['branch'])
    if kwargs['md5']:
        download_from_md5(kwargs['md5'], kwargs['dst'], kwargs['decrypt'])
    if kwargs['url']:
        download_from_url(kwargs['url'], kwargs['dst'], kwargs['decrypt'])
