#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   clm_resub.py    230329  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#
from openpyxl.utils.cell import column_index_from_string

def c2n(c):
    return column_index_from_string(c) - 1


class clm:
    dname       = c2n('A')  # 0
    ptn         = c2n('B')  # 1
    rpl         = c2n('C')  # 2
    cnt         = c2n('D')
    flg         = c2n('E')
    last_row    = c2n('E')+1

class rdl:   ## info in each Resub Definition Line
    def __init__(self, lst):
        self.ptn    = lst[clm.ptn]
        self.rpl    = lst[clm.rpl]
        self.cnt    = lst[clm.cnt]
        self.flg    = lst[clm.flg]
