#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   sorter.py   220721  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import pprint

from m.prnt                     import prnt
from .setupdb        import setupdb
from .sorter_s       import sorter_s
from .sorter_m       import sorter_m
from .mark_oos       import mark_oos
from .gv             import gv
from ...env                      import DD


def pp(x):
    return pprint.pformat(x, indent=2)

def sorter(srtr):
    dumpdb = DD.dbf
    pdf_pg = setupdb(dumpdb)
    #   pdf_pg = { docname : [ [star Page, end page], ... ], ... }
    prnt(f'init pdf_pg\n{pp(pdf_pg)}')
    for docname in srtr:
        sobj = srtr[docname]
        #
        #   sorter_s() sorter_m() updates pdf_pg
        #   (matched pages are removed from pdf_pg)
        #
        if sobj.type == 'single':
            sorter_s(docname,sobj,pdf_pg) # mark docname & reduce pdf_page
        elif sobj.type == 'multi':
            sorter_m(docname,sobj,pdf_pg) # mark docname & reduce pdf_page
        else:
            raise Exception('program error')
        prnt(f'pdf_pg aft "{docname}"\n{pp(pdf_pg)}')
    prnt(f'final pdf_pg\n{pp(pdf_pg)}')
    mark_oos(pdf_pg) # unmaked pages are all '_OOS'
    gv.con.commit()
    return
