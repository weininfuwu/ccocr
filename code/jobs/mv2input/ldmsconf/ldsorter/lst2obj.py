#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   lst2obj.py  230315  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

from m.prnt         import prnt
from .loadxl.clm    import c2,do

class so:
    def __init__(self,typ):
        self.type   = typ
        if typ == 'single':
            self.defs = []
        elif typ == 'multi':
            self.hd = []
            self.md = []
            self.ft = []
        else:
            prnt('program bug')
            # raise ConfigErr("")
            raise Exception('configerror')

def lst2obj(sorter):
    for docname in sorter:
        load(sorter,docname,sorter[docname])
    return

def load(sorter,docname,dlines):
    if dlines[0][c2.assem] == None:
        load_single(sorter,docname,dlines)
    elif dlines[0][c2.assem] in ['hd','md','ft']:
        load_multi(sorter,docname,dlines)
    else:
        prnt('PROGAM BUG')
        #raise ConfigErr("")
        raise Exception('config error')
    return

def load_single(sorter,docname,dlines):
    sobj  = so('single')
    for dline in dlines:
        sobj.defs.append(do(dline))
    sorter[docname] = sobj
    return

def load_multi(sorter,docname,dlines):
    sobj  = so('multi')
    for dline in dlines:
        if dline[c2.assem] == 'hd':
            sobj.hd.append(do(dline))
        elif dline[c2.assem] == 'md':
            sobj.md.append(do(dline))
        elif dline[c2.assem] == 'ft':
            sobj.ft.append(do(dline))
        else:
            prnt('program bug')
            # raise ConfigErr("")
            raise Exception('config error')
    sorter[docname] = sobj
    return
