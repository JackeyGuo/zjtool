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


import subprocess
import sys

from rich.console import Console
from rich.theme import Theme

console = Console(theme=Theme({
    'info': 'dim cyan',
    'warning': 'magenta',
    'danger': 'red',
}))


def call_shell(cmd: list):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while popen.poll() is None:
        ret = popen.stdout.readline().decode('GBK')
        sys.stdout.write(ret)
    if popen.poll() != 0:
        err = popen.stderr.read().decode('GBK')
        sys.stdout.write(err)
        raise BrokenPipeError


def extract_kwargs(func, kwargs):
    return {
        varname: kwargs[varname]
        for varname in func.__code__.co_varnames
        if varname in kwargs
    }


class XSTR:
    def __init__(self, instr):
        self.instr = instr

    # 删除“//”标志后的注释
    def rmCmt(self):
        qtCnt = cmtPos = slashPos = 0
        rearLine = self.instr
        # rearline: 前一个“//”之后的字符串，
        # 双引号里的“//”不是注释标志，所以遇到这种情况，仍需继续查找后续的“//”
        while rearLine.find('//') >= 0:  # 查找“//”
            slashPos = rearLine.find('//')
            cmtPos += slashPos
            # print 'slashPos: ' + str(slashPos)
            headLine = rearLine[:slashPos]
            while headLine.find('"') >= 0:  # 查找“//”前的双引号
                qtPos = headLine.find('"')
                if not self.isEscapeOpr(headLine[:qtPos]):  # 如果双引号没有被转义
                    qtCnt += 1  # 双引号的数量加1
                headLine = headLine[qtPos + 1:]
                # print qtCnt
            if qtCnt % 2 == 0:  # 如果双引号的数量为偶数，则说明“//”是注释标志
                # print self.instr[:cmtPos]
                return self.instr[:cmtPos]
            rearLine = rearLine[slashPos + 2:]
            # print rearLine
            cmtPos += 2
        # print self.instr
        return self.instr

    # 判断是否为转义字符
    def isEscapeOpr(self, instr):
        if len(instr) <= 0:
            return False
        cnt = 0
        while instr[-1] == '\\':
            cnt += 1
            instr = instr[:-1]
        if cnt % 2 == 1:
            return True
        else:
            return False
