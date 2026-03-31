#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   ldresub.py  230328  cy
#   ToDo        nks_nonaka  エラーメール    resub
#
#--------1---------2---------3---------4---------5---------6---------7--------#

from m.prnt     import prnt
from .ldresub_sht   import ldresub_sht
from .load2docdef   import load2docdef
'''
    resub['docdef name'] = resub dict
    reusbu dict = { 'docname' : resub obj,
                    ... }
    member of resub obj :   .ptn
                            .rpl
                            .cnt
                            .flg
'''

def ldresub(wb,docdef):
    resub = {}
    ##
    ## orphan _resub
    ##
    for sn in wb.sheetnames:
        if sn.endswith('_resub') and f'{sn[:-6]}_dd' not in wb.sheetnames:
            raise Exception(f'{sn} has NO _dd sheet')
    ##
    ## 1) find which _resub to sheet to load
    ## 2) pick up defined dname, store in resub[docname]['dnames']
    ##
    for docname in docdef:
        if f'{docname}_resub' not in wb.sheetnames:
            continue
        resub[docname] = { 'dnames' : [] }
        defs  = docdef[docname].defs
        child = docdef[docname].child
        while True:
            for dl in defs:
                resub[docname]['dnames'].append(dl.dname)
            if child == None:
                break
            else:
                defs  = child.defs
                child = child.child
    ##
    ## 1) load xl sheet
    ## 2) init check
    ## 3) store in resub[docname]['2dimlst']
    ##
    ldresub_sht(resub,wb)
    ##
    ## rebuild resub
    ##
    ##  resub[docname][dname] = [ resub obj, ... ]
    ##
    load2docdef(resub,docdef)
    return
