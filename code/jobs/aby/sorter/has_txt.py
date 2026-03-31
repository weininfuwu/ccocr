#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   has_txt.py      230407  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

def has_txt(dl):
    if (type(dl.sp_abv) == int and type(dl.sp_blw) == int and
        type(dl.sp_rof) == int and type(dl.sp_lof) == int ):
        return False
    else:
        return True
