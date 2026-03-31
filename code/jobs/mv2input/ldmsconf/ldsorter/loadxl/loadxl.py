#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   loadxl.py   230313  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

from m.prnt import prnt

from openpyxl import load_workbook

from .clm        import clm
from .lv0chk     import lv0chk

def loadxl(mscnf):
    prnt('started')
    ##
    ##  xl -> 2-dim list
    ##
    wb          = load_workbook(mscnf)
    ws          = wb['sorter']
    sht_sorter  = []
    flg         = False
    for row in list(ws.rows):
        row = list(row)
        row = [ ii.value for ii in row ]
        if row[0] == 'ROW_BELOW_IS_FOR_SYSTEM':
            flg = True
            continue
        if not flg:
            continue
        if ( row[0] == None ) or (row[0].startswith('_')):
            continue
        sht_sorter.append(row[:clm.last_row])  # upto 'N'
    wb.close()
    lv0chk(sht_sorter)
    ##
    ## 2-dim list -> dict
    ##
    ##  sorter = {  docname : [ [assem, dname, ... ],
    ##              ... , }
    ##
    sorter = {}
    for row in sht_sorter:
        docname = row[clm.docname]
        other   = row[clm.dname:]
        sorter.setdefault(docname,[])
        sorter[docname].append(other)
    return sorter
