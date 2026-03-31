#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   resub.py    230511  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import copy
import re

from m.prnt import prnt

def resub(io):
    # posrtn is a list or None
    io.resubrtn = copy.copy(io.posrtn)
    if io.resubrtn == None:
        return
    txt = io.resubrtn[2]
    for i in io.dl.resub:
        if i.rpl == None:
            i.rpl = ''
        if i.flg == None:
            i.flg = 0
        txt = re.sub(rf'{i.ptn}', rf'{i.rpl}', txt, count=i.cnt, flags=i.flg)
    io.resubrtn[2] = txt
    return
