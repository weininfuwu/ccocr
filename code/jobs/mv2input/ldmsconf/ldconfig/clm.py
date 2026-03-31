#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   clm.py  230323  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#
from openpyxl.utils.cell import column_index_from_string

def c2n(c):
    return column_index_from_string(c) - 1


class clm:
    dname       = c2n('A')  # 0
    clm         = c2n('B')  # 1
    sp_blw      = c2n('C')  # 2
    of_blw      = c2n('D')
    sp_abv      = c2n('E')
    of_abv      = c2n('F')
    sp_rof      = c2n('G')
    of_rof      = c2n('H')
    sp_lof      = c2n('I')
    of_lof      = c2n('J')
    val         = c2n('K')
    tgt         = c2n('L')
    dtyp        = c2n('M')
    pos         = c2n('N')
    op          = c2n('O')
    rg          = c2n('P')
    last_row    = c2n('P')+1

class dl:   ## info in each Definition Line
    def __init__(self, lst):
        self.dname  = lst[clm.dname]
        self.clm    = lst[clm.clm]
        self.sp_blw = lst[clm.sp_blw]
        self.of_blw = lst[clm.of_blw]
        self.sp_abv = lst[clm.sp_abv]
        self.of_abv = lst[clm.of_abv]
        self.sp_rof = lst[clm.sp_rof]
        self.of_rof = lst[clm.of_rof]
        self.sp_lof = lst[clm.sp_lof]
        self.of_lof = lst[clm.of_lof]
        self.val    = lst[clm.val]
        self.tgt    = lst[clm.tgt]
        self.dtyp   = lst[clm.dtyp]
        self.pos    = lst[clm.pos]
        self.op     = lst[clm.op]
        self.rg     = lst[clm.rg]
        ## 230330
        self.resub  = []

