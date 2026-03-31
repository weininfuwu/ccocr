#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   pgmatch.py  230411      cy
#   (was lkup_s.py   230407      cy)
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import copy
from .mark          import mark
from .has_txt       import has_txt
from .aply_locdic   import aply_locdic
from .runsql        import runsql
from .              import gv

from m.prnt         import prnt

def pgmatch(docname,pdf,pg,sobj_org):
    ##
    ##  check ONE page with LIST OF sorter line
    ##
    ##      sobj: list of deflines for ONE docnament
    ##
    sobj = copy.deepcopy(sobj_org)  # make deepcopy as using lst.pop() in runsql()
    sobj.locdic = {}                # refresh for this page
    ### main loop
    index = 0
    while len(sobj.defs) > 0:           # have to pass all tests to graduate
        if has_txt(sobj.defs[index]):   # sp_abv = TOP_hoge etc.
            if aply_locdic(sobj,index):
                if not runsql(sobj,index,pdf,pg):
                    return False        # page is NOT this doc, cannot graduate
                index = 0
            else:
                index +=1               # to next def line
        else:
            if not runsql(sobj,index,pdf,pg):
                return False            # page is NOT this doc, cannot graduate
            index = 0
    return True                         # page is THIS doc / graduate!!
