#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   hdbtm_fttop.py  230602  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

from m.prnt import prnt

def hdbtm_fttop(do,io):
    #
    # set hdbtm fttop (do.* is to be updated every time)
    #
    # level 2 or deeper has not 'hd' 'ft', this does nothing
    #
    if io.dl.rg == 'hd':
        hdbtm = io.posrtn[5]
        if type(do.hdbtm) == int:
            do.hdbtm = max([do.hdbtm, hdbtm])
        else:
            do.hdbtm = hdbtm
    elif io.dl.rg == 'ft':
        fttop = io.posrtn[4]
        if type(do.fttop) == int:
            do.fttop = min([do.fttop, fttop])
        else:
            do.fttop = fttop
    return
