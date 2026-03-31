#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   fill.py     230330  cy
#   ToDo        nks_nonaka  エラーメール 
#
#--------1---------2---------3---------4---------5---------6---------7--------#

from m.prnt     import prnt

def fill(family,board,docname):
    alw_m_ok = [] # can never be papa
    ##
    ## pickup alw_m = OK (cannot be papa)
    ##
    for dl in family:
        if hasattr(dl,'alw_m') and dl.alw_m == 'OK':
            alw_m_ok.append(dl.dname)
    ##
    ##  check and fill
    ##
    for dl in family:
        fm = f'p_{dl.dname}'
        for sp in [dl.sp_blw,dl.sp_abv,dl.sp_rof,dl.sp_lof]:
            if sp == None:      ## cy 230607
                continue        ## cy 230607
            if type(sp) == int:
                continue
            if sp[4:] in alw_m_ok:
                prnt(f'{docname} {sp[4:]} cannot be a papa because alw_m = OK')
#                quit()
            to = f'c_{sp[4:]}'
            try:
#                board.loc[fm][to] += 1
                board.loc[fm, to] += 1  # claud says
            except KeyError as e:
                prnt(f'INVALID REF @{docname} {fm[2:]} -> {to[2:]}')
#                quit()
    return
