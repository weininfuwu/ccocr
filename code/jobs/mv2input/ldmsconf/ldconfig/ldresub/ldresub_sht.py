#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   ldresub_sht.py  230328  cy
#   ToDo            nks_nonaka  resubシート
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import re

from m.prnt     import prnt
from .clm_resub     import clm
#from m.errconfig    import ConfigErr

def ldresub_sht(resub,wb):
    for docname in resub:

        dnames = resub[docname]['dnames']

        ws = wb[f'{docname}_resub']
        sht = []
        flg = False
        for row in list(ws.rows):
            ##
            ## load one row
            ##
            row = list(row)
            row = [ ii.value for ii in row ]
            if row[clm.dname] == 'ROW_BELOW_IS_FOR_SYSTEM':
                flg = True
                continue
            if not flg:
                continue
            if row[clm.dname] == None:
                continue
            if type(row[clm.dname]) == str and row[clm.dname].startswith('_'):
                continue
            ##
            ## init check
            ##
            # (A) dname
            if row[clm.dname] not in dnames:
                raise Exception(f'resub {docname} has WRONG dname "{row[clm.dname]}"')
            # (B) ptn
            try:
                ptn = rf'{row[clm.ptn]}'
                m = re.compile(row[clm.ptn])
            except Exception as msg:
                prnt(( f'WRONG regex "{row[clm.ptn]}" '
                        f'{docname} {row[clm.dname]}\n'
                        f'{msg}'))
                raise Exception(( f'WRONG regex "{row[clm.ptn]}" '
                        f'{docname} {row[clm.dname]}\n'
                        f'{msg}'))
            # (C) repl  : NO CHECK
            # (D) cnt
            if row[clm.cnt] == None:
                row[clm.cnt] = 0
            if type(row[clm.cnt]) != int or row[clm.cnt] < 0:
                raise Exception(f'resub {docname} has WRONG cnt "{row[clm.cnt]}"')
            # (E) flg
            if row[clm.flg] != None:
                if (type(row[clm.flg]) != str           or
                    not row[clm.flg].startswith('re.')  or
                    len(row[clm.flg]) < 4               ):
                    raise Exception(f'resub {docname} has WRONG flg "{row[clm.flg]}"')
                if not hasattr(re.RegexFlag,row[clm.flg][3:]):
                    raise Exception(f'resub {docname} has WRONG flg "{row[clm.flg]}"')
            ##
            ## finalize
            ##
            sht.append(row[:clm.last_row])
        resub[docname] = sht
    return
