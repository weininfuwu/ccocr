#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   clm.py      230330  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#
from openpyxl.utils.cell import column_index_from_string

def c2n(c):
    return column_index_from_string(c) - 1

class clm:
    docname     = c2n('A')  # 0
    dname       = c2n('B')  # 1
    sp_blw      = c2n('C')  # 2
    of_blw      = c2n('D')  # 3
    sp_abv      = c2n('E')
    of_abv      = c2n('F')
    sp_rof      = c2n('G')
    of_rof      = c2n('H')
    sp_lof      = c2n('I')
    of_lof      = c2n('J')
    val         = c2n('K')
    dtyp        = c2n('L')
    alw_m       = c2n('M')
    assem       = c2n('N')
    last_row    = c2n('N')+1

class c2: ## to be used at lst2obj
#    docname     = c2n('A') ## moved to dict key
    dname       = clm.dname     - 1
    sp_blw      = clm.sp_blw    - 1
    of_blw      = clm.of_blw    - 1
    sp_abv      = clm.sp_abv    - 1
    of_abv      = clm.of_abv    - 1
    sp_rof      = clm.sp_rof    - 1
    of_rof      = clm.of_rof    - 1
    sp_lof      = clm.sp_lof    - 1
    of_lof      = clm.of_lof    - 1
    val         = clm.val       - 1
    dtyp        = clm.dtyp      - 1
    alw_m       = clm.alw_m     - 1
    assem       = clm.assem     - 1

class do:
    def __init__(self,lst):
        self.dname  = lst[c2.dname]
        self.sp_blw = lst[c2.sp_blw]
        self.of_blw = lst[c2.of_blw]
        self.sp_abv = lst[c2.sp_abv]
        self.of_abv = lst[c2.of_abv]
        self.sp_rof = lst[c2.sp_rof]
        self.of_rof = lst[c2.of_rof]
        self.sp_lof = lst[c2.sp_lof]
        self.of_lof = lst[c2.of_lof]
        self.val    = lst[c2.val]
        self.dtyp   = lst[c2.dtyp]
        self.alw_m  = lst[c2.alw_m]
        self.assem  = lst[c2.assem]     ## will never be used


