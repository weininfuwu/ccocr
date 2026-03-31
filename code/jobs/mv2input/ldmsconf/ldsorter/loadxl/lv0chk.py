#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   init_chk.py 230314  cy
#   import send_sorter_err_mail 230710 nks_nonaka
#   import doneall              230807 nks_nonaka
#
#   updated: 260319.162530 by cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import re

from m.prnt     import prnt
from .clm       import clm
from jobs.env   import DD

def lv0chk(sht):
    dnames = []
    assems = {}
    for row in sht:
        ## docname  (A)
        if type(row[clm.docname]) != str:
            raise Exception(f'ERROR sorter has WRONG docname "{row[clm.docname]}"')
        if row[clm.docname].isnumeric():
            raise Exception(f'ERROR sorter has WRONG docname "{row[clm.docname]}"')
        m = re.match(r'^[a-zA-Z0-9_]+$',row[clm.docname])
        if m == None:
            raise Exception(f'ERROR sorter has WRONG docname "{row[clm.docname]}"')
        ## dname    (B)
        if type(row[clm.dname]) != str:
            raise Exception(f'ERROR sorter has WRONG dname "{row[clm.dname]}"')
        if row[clm.dname].isnumeric():
            raise Exception(f'ERROR sorter has WRONG dname "{row[clm.dname]}"')
        m = re.match(r'^[a-zA-Z0-9_]+$',row[clm.dname])
        if m == None:
            raise Exception(f'ERROR sorter has WRONG dname "{row[clm.dname]}"')
        if row[clm.dname] not in dnames:
            dnames.append(row[clm.dname])
        else:
            raise Exception(f'duplicated dname in sorter "{row[clm.dname]}"')
        ## sp_blw   (C)
        if row[clm.sp_blw] == None:
#            row[clm.sp_blw] = 0
            row[clm.sp_blw] = -1    # sql use ">", not ">="
        if not ((   type(row[clm.sp_blw]) == int or
                    (type(row[clm.sp_blw]) == str and
                     row[clm.sp_blw][:4] in ['TOP_','BTM_','RYT_','LFT_']))):
            raise Exception(( f'ERROR: {row[clm.docname]} {row[clm.dname]} '
                        f'has WRONG sp_blw "{row[clm.sp_blw]}"'))
        ## of_blw   (D)
        if row[clm.of_blw] == None:
            row[clm.of_blw] = 0
        if type(row[clm.of_blw]) != int:
            raise Exception(( f'ERROR: {row[clm.docname]} {row[clm.dname]} '
                    f'has WRONG sp_of "{row[clm.of_blw]}"'))
        ## sp_abv   (E)
        if row[clm.sp_abv] == None:
#            row[clm.sp_abv] = 9999999
#            row[clm.sp_abv] = misc.tb_exp
            row[clm.sp_abv] = DD.tb_exp
        if not ((   type(row[clm.sp_abv]) == int or
                    (type(row[clm.sp_abv]) == str and
                     row[clm.sp_abv][:4] in ['TOP_','BTM_','RYT_','LFT_']))):
            raise Exception(( f'ERROR: {row[clm.docname]} {row[clm.dname]} '
                        f'has WRONG sp_abv "{row[clm.sp_abv]}"'))
        ## of_abv   (F)
        if row[clm.of_abv] == None:
            row[clm.of_abv] = 0
        if type(row[clm.of_abv]) != int:
            raise Exception(( f'ERROR: {row[clm.docname]} {row[clm.dname]} '
                    f'has WRONG sp_of "{row[clm.of_abv]}"'))
        ## sp_rof   (G)
        if row[clm.sp_rof] == None:
#            row[clm.sp_rof] = 0
            row[clm.sp_rof] = -1    # sql use ">", not ">="
        if not ((   type(row[clm.sp_rof]) == int or
                    (type(row[clm.sp_rof]) == str and
                     row[clm.sp_rof][:4] in ['TOP_','BTM_','RYT_','LFT_']))):
            raise Exception(( f'ERROR: {row[clm.docname]} {row[clm.dname]} '
                        f'has WRONG sp_rof "{row[clm.sp_rof]}"'))
        ## of_rof   (H)
        if row[clm.of_rof] == None:
            row[clm.of_rof] = 0
        if type(row[clm.of_rof]) != int:
            raise Exception(( f'ERROR: {row[clm.docname]} {row[clm.dname]} '
                    f'has WRONG sp_of "{row[clm.of_rof]}"'))
        ## sp_lof   (I)
        if row[clm.sp_lof] == None:
            row[clm.sp_lof] = 9999999
        if not ((   type(row[clm.sp_lof]) == int or
                    (type(row[clm.sp_lof]) == str and
                     row[clm.sp_lof][:4] in ['TOP_','BTM_','RYT_','LFT_']))):
            raise Exception(( f'ERROR: {row[clm.docname]} {row[clm.dname]} '
                        f'has WRONG sp_lof "{row[clm.sp_lof]}"'))
        ## of_lof   (J)
        if row[clm.of_lof] == None:
            row[clm.of_lof] = 0
        if type(row[clm.of_lof]) != int:
            raise Exception(( f'ERROR: {row[clm.docname]} {row[clm.dname]} '
                    f'has WRONG sp_lof "{row[clm.of_lof]}"'))
        ## val      (K)
        if row[clm.val] == None:
            row[clm.val] = '^.*$'
        try:
            ptn = rf'{row[clm.val]}'
            m = re.compile(ptn)
        except re.error as msg:
            raise Exception(( f'WRONG regex "{row[clm.val]}"'
                    f'{row[clm.docname]} {row[clm.dname]}\n'
                    f'{msg}'))
        ## dtyp     (L)
        if row[clm.dtyp] == None:
            row[clm.dtyp] = 'line'
        if row[clm.dtyp] not in ['line', 'word']:
            raise Exception(( f'ERROR: {row[clm.docname]} {row[clm.dname]} '
                    f'has WRONG dtyp "{row[clm.dtyp]}"'))
        ## alw_m    (M)
        if row[clm.alw_m] == None:
            row[clm.alw_m] = 'NG'
        if row[clm.alw_m] not in ['OK', 'NG']:
            raise Exception(( f'ERROR: {row[clm.docname]} {row[clm.dname]} '
                    f'has WRONG alw_m "{row[clm.alw_m]}"'))
        ## assem    (N)
        if row[clm.assem] not in [ None, 'hd', 'ft', 'md']:
            raise Exception(( f'ERROR: {row[clm.docname]} has WRONG ASSEM '
                    f'{row[clm.assem]}'))
        assems.setdefault(row[clm.docname],set())
        assems[row[clm.docname]].add(row[clm.assem])
    for docname in assems:
        if assems[docname] != {None}:                       # check multpage only
            if {None}.issubset(assems[docname]):            # blank assm => NG
                raise Exception(f'sorter assem error in {docname}')
            elif 'hd' not in assems[docname]:               # no hd => NG
                raise Exception(f'sorter assem error in {docname}')
            elif {'hd','md'} == assems[docname]:
                raise Exception(f'sorter assem error in {docname}')
    return
