#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   init_chk.py 230317  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import re
import collections

from m.prnt             import prnt
from .gkgmchk  import gkgmchk
from .clm                   import clm

#
#    name 'docdef' here is 'docname' elseher
#

def init_chk(docdefs,sorter):
    for docdef in docdefs:
        doctype = sorter[docdef].type   ## used at sp_blw sp_abv check
        dnames  = []    ## to check duplicate
        rgs     = []    ## only check for has_rg or not
        clms    = []    ## to check duplicate
        if len(docdefs[docdef]) == 0:
            raise Exception(   __name__        ,
                            '001_001000_000',
                            [docdef]  )
        for row in docdefs[docdef]:
            ## dname    (A)
            if type(row[clm.dname]) != str:
                raise Exception(f'ERROR {docdef} has WRONG dname "{row[clm.dname]}"')
            if row[clm.dname].isnumeric():
                raise Exception(f'ERROR {docdef} has WRONG dname "{row[clm.dname]}"')
            m = re.match(r'^[a-zA-Z0-9_]+$',row[clm.dname])
            if m == None:
                raise Exception(f'ERROR {docdef} has WRONG dname "{row[clm.dname]}"')
            dnames.append(row[clm.dname])
            ## clm      (B)
            if row[clm.clm] != None:
                m = re.match(r'^[A-Z]*$', row[clm.clm])
                if m == None:
                    raise Exception((  f'ERROR {docdef} {row[clm.dname]} '
                            f'WRONG clm "{row[clm.clm]}"'))
                if row[clm.clm] in ['A','B','C','D']:
                    raise Exception((  f'ERROR {docdef} {row[clm.dname]} '
                            f'WRONG clm "{row[clm.clm]}"'))
                clms.append(row[clm.clm])
            ## sp_blw   (C)
            if type(row[clm.sp_blw]) == int and doctype == 'multi':
                raise Exception(f'''
    ERROR (230608): sp_blw of multipage doc cannot be int
    docname {docdef} ''')
#### cy 230607
#            if row[clm.sp_blw] == None:
#                row[clm.sp_blw] = 0

#            if not ((   type(row[clm.sp_blw]) == int or
#                        row[clm.sp_blw][:4] in [
#                                            'TOP_','BTM_','RYT_','LFT_'])):
            if not ((   type(row[clm.sp_blw])   == int  or
                        row[clm.sp_blw]         == None or
                        (   type(row[clm.sp_blw]) == str and
                            row[clm.sp_blw][:4] in [
                                            'TOP_','BTM_','RYT_','LFT_']))):
                raise Exception((  f'ERROR: {docdef} {row[clm.dname]} '
                        f'has WRONG sp_blw "{row[clm.sp_blw]}"'))
            ## of_blw   (D)
            if row[clm.of_blw] == None:
                row[clm.of_blw] = 0
            if type(row[clm.of_blw]) != int:
                raise Exception((  f'ERROR: {docdef} {row[clm.dname]} '
                        f'has WRONG sp_of "{row[clm.of_blw]}"'))
            ## sp_abv   (E)
            if type(row[clm.sp_abv]) == int and doctype == 'multi':
                raise Exception(f'''
    ERROR (230608): sp_abv of multipage doc cannot be int
    docname {docdef}''')
#### cy 230607
#            if row[clm.sp_abv] == None:
#                row[clm.sp_abv] = misc.tb_exp
#            if not ((   type(row[clm.sp_abv]) == int or
#                        row[clm.sp_abv][:4] in [
#                                'TOP_','BTM_','RYT_','LFT_','TPN_','BTN_'])):
            if not ((   type(row[clm.sp_abv])   == int  or
                        row[clm.sp_abv]         == None or
                        (   type(row[clm.sp_abv]) == str and
                            row[clm.sp_abv][:4] in [
                                'TOP_','BTM_','RYT_','LFT_','TPN_','BTN_']))):
                raise Exception((  f'ERROR: {docdef} {row[clm.dname]} '
                        f'has WRONG sp_abv "{row[clm.sp_abv]}"'))

            ## of_abv   (F)
            if row[clm.of_abv] == None:
                row[clm.of_abv] = 0
            if type(row[clm.of_abv]) != int:
                raise Exception((  f'ERROR: {docdef} {row[clm.dname]} '
                        f'has WRONG sp_of "{row[clm.of_abv]}"'))
            ## sp_rof   (G)
            if row[clm.sp_rof] == None:
                row[clm.sp_rof] = 0
            if not ((   type(row[clm.sp_rof]) == int or
                        row[clm.sp_rof][:4] in [
                                            'TOP_','BTM_','RYT_','LFT_'])):
                raise Exception((  f'ERROR: {docdef} {row[clm.dname]} '
                        f'has WRONG sp_rof "{row[clm.sp_rof]}"'))
            ## of_rof   (H)
            if row[clm.of_rof] == None:
                row[clm.of_rof] = 0
            if type(row[clm.of_rof]) != int:
                raise Exception((  f'ERROR: {docdef} {row[clm.dname]} '
                        f'has WRONG sp_of "{row[clm.of_rof]}"'))
            ## sp_lof   (I)
            if row[clm.sp_lof] == None:
                row[clm.sp_lof] = 9999999
            if not ((   type(row[clm.sp_lof]) == int or
                        row[clm.sp_lof][:4] in [
                                'TOP_','BTM_','RYT_','LFT_','RYN_','LFN_'])):
                raise Exception((  f'ERROR: {docdef} {row[clm.dname]} '
                        f'has WRONG sp_lof "{row[clm.sp_lof]}"'))
            ## of_lof   (J)
            if row[clm.of_lof] == None:
                row[clm.of_lof] = 0
            if type(row[clm.of_lof]) != int:
                raise Exception((  f'ERROR: {docdef} {row[clm.dname]} '
                        f'has WRONG sp_lof "{row[clm.of_lof]}"'))
            ## val      (K)
            if row[clm.val] == None:
                row[clm.val] = '^.*$'
            try:
                ptn = rf'{row[clm.val]}'
                m = re.compile(ptn)
            except re.error as msg:
                raise Exception(( f'WRONG regex val "{row[clm.val]}" '
                        f'{docdef} {row[clm.dname]}\n'
                        f'{msg}'))
            ## tgt      (L)
            if row[clm.tgt] == None:
                row[clm.tgt] = 0
            if type(row[clm.tgt]) != int:
                raise Exception((  f'ERROR: {docdef} {row[clm.dname]} '
                        f'tgt is NOT INT "{row[clm.tgt]}"' ))
            ## dtyp     (M)
            if row[clm.dtyp] == None:
                row[clm.dtyp] = 'line'
            if row[clm.dtyp] not in ['line', 'word']:
                raise Exception((  f'ERROR: {docdef} {row[clm.dname]} '
                        f'has WRONG dtyp "{row[clm.dtyp]}"'))
            ## pos      (N)
            if row[clm.pos] == None:
                row[clm.pos] = 'TOP_LFT'
            if row[clm.pos] not in ['TOP_RYT','TOP_LFT','BTM_RYT','BTM_LFT',
                                    'RYT_TOP','RYT_BTM','LFT_TOP','LFT_BTM' ]:
                raise Exception((  f'ERROR {docdef} {row[clm.dname]} '
                        f'WRONG pos "{row[clm.pos]}"'))
            ## op       (O)
            if row[clm.op] not in [None, 'op']:
                raise Exception(( f'ERROR {docdef} {row[clm.dname]} '
                        f'WRONG op "{row[clm.op]}"'))
            ## rg       (P)
            if (    row[clm.rg] not in [None, 'hd', 'ft']
                    and not row[clm.rg].startswith('gk_')
                    and not row[clm.rg].startswith('gm_') ):
                raise Exception(( f'ERROR {docdef} {row[clm.dname]} '
                        f'WRONG rg "{row[clm.rg]}"'))
            rgs.append(row[clm.rg])
        #
        #       dname   (A) duplication check
        #
        dnames_dup  = [k for k,v in collections.Counter(dnames).items()
                                                                    if v > 1]
        if len(dnames_dup) > 0:
            raise Exception(f'ERROR: duplicated dname in {docdef}: {dnames_dup}')
        #
        #       clm     (B) duplication check
        #
        clms_dup  = [k for k,v in collections.Counter(clms).items() if v > 1]
        if len(clms_dup) > 0:
            raise Exception(f'ERROR: duplicated clm in {docdef}: {clms_dup}')
        #
        #       rg      (P) combination check
        #
        if set(rgs) == {None}:
            continue                ## no rg
        #
        #       check further for repeating groups
        #
        gkgmchk(docdef,rgs)       ## possibly quit()
    return
