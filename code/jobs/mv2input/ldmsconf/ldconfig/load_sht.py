#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   load_sht.py     230317  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

from openpyxl import load_workbook

from .clm import clm

def load_sht(msconfig,docdefs):
    wb = load_workbook(msconfig)
    rtn = {}
    for ddsht in docdefs:
        ws  = wb[f'{ddsht}_dd']
        sht = []
        flg = False
        for row in list(ws.rows):
            row = list(row)
            row = [ ii.value for ii in row ]
            if row[0] == 'ROW_BELOW_IS_FOR_SYSTEM':
                flg = True
                continue
            if not flg:
                continue
            if row[clm.dname] == None:
                continue
            if type(row[clm.dname]) == str and row[clm.dname].startswith('_'):
                continue
            sht.append(row[:clm.last_row])
        rtn[ddsht] = sht
    wb.close()
    return rtn
