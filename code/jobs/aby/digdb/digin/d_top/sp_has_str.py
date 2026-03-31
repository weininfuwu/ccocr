#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   d_top version
#
#   sp_has_str.py   230427  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

from m.prnt import prnt
#from m.env import misc
from .....env import DD

class misc:
    tb_exp = DD.tb_exp

def sp_has_str(do,io,fm,to):
    locdic = do.locdic
    dl = io.dl
    ##
    ## sp_blw
    ##
    if type(dl.sp_blw) == str:
        if dl.sp_blw in locdic:
            dl.sp_blw = locdic[dl.sp_blw]
            if dl.sp_blw == None:
                io.p_nopapa = True
        else:
            return True                             ## RETURN (has_str)
    elif type(dl.sp_blw) == int and dl.sp_blw < misc.tb_exp:
        tmp = dl.sp_blw
        dl.sp_blw = dl.sp_blw + fm * misc.tb_exp
#        prnt(f'''
#    {do.docname} {dl.dname}: dl.sp_blw {tmp} -> {dl.sp_blw}''')
    elif dl.sp_blw == None:
        dl.sp_blw = fm * misc.tb_exp
#        prnt(f'''
#    230701
#    {do.docname} {dl.dname}: dl.sp_blw None -> {dl.sp_blw}''')
    else:   # any big int, unexpceted
        prnt(f'''
    230701
    UNEXPECTED VALUE
    {do.docname} {dl.dname}: dl.sp_blw {dl.sp_blw}''')
    ##
    ##  sp_abv
    ##
    if type(dl.sp_abv) == str:
        if dl.sp_abv in locdic:
            dl.sp_abv = locdic[dl.sp_abv]
            if dl.sp_abv == None:
                io.p_nopapa = True
        else:
            return True                             ## RETURN (has_str)
    elif type(dl.sp_abv) == int and dl.sp_abv < misc.tb_exp:
        tmp = dl.sp_abv
        dl.sp_abv = dl.sp_abv + to * misc.tb_exp
#        prnt(f'''
#    {do.docname} {dl.dname}: dl.sp_abv {tmp} -> {dl.sp_abv}''')
    elif dl.sp_abv == None:
        dl.sp_abv = (to+1) * misc.tb_exp
#        prnt(f'''
#    230701
#    {do.docname} {dl.dname}: dl.sp_abv None -> {dl.sp_abv}''')
    else:   # any big int, unexpceted
        prnt(f'''
    230701
    UNEXPECTED VALUE
    {do.docname} {dl.dname}: dl.sp_abv {dl.sp_abv}''')

    ##
    ## sp_lof
    ##
    if type(dl.sp_lof) == str:
        if dl.sp_lof in locdic:
            dl.sp_lof = locdic[dl.sp_lof]
            if dl.sp_lof == None:
                io.p_nopapa = True
        else:
            return True                             ## RETURN (has_str)
    ##
    ## sp_rof
    ##
    if type(dl.sp_rof) == str:
        if dl.sp_rof in locdic:
            dl.sp_rof = locdic[dl.sp_rof]
            if dl.sp_rof == None:
                io.p_nopapa = True
        else:
            return True                             ## RETURN (has_str)
    return False                                    ## RETURN (NO STR)
