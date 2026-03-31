#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   aply_locdic.py      230407  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

from m.prnt import prnt

def aply_locdic(sobj,index):
    o = sobj.defs[index]
    dic = sobj.locdic
    try:
        if type(o.sp_abv) != int:
            o.sp_abv = dic[o.sp_abv]
        if type(o.sp_blw) != int:
            o.sp_blw = dic[o.sp_blw]
        if type(o.sp_rof) != int:
            o.sp_rof = dic[o.sp_rof]
        if type(o.sp_lof) != int:
            o.sp_lof = dic[o.sp_lof]
    except KeyError as e:
#        prnt(f'{e} not yet in locdic') # too noisy
        return False
    return True
