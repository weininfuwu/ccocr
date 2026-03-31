#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   fillobj.py  230323  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

class lvl:
    def __init__(self):
        self.defs   = []
        self.child  = None

def fillobj(dlines,depth):
    lvlo = lvl()
    idx = 0
    while idx < len(dlines):
        hit = False
        ## only for initial depth
        if dlines[idx].rg in [None,'hd','ft']:
            hit = True
            lvlo.defs.append(dlines.pop(idx))
        ## gk of this depth
        elif (  len(dlines[idx].rg.split('_')) == depth + 1
                and dlines[idx].rg.startswith('gk')):
            hit = True
            lvlo.defs.append(dlines.pop(idx))
        ## gk of this depth
        elif (  len(dlines[idx].rg.split('_')) == depth
                and dlines[idx].rg.startswith('gm')):
            hit = True
            lvlo.defs.append(dlines.pop(idx))
        if hit:
            continue
        idx += 1
    if len(lvlo.defs) == 0:
        return False
    else:
        return lvlo
