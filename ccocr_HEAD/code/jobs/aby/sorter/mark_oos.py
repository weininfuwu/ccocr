#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   mark_oos.py     230411      cy
#   updated: 260322 insert engine/usepng; key is now 'pdf|engine|usepng'
#             skip straight entries for OOS (no marking png exists)
#
#--------1---------2---------3---------4---------5---------6---------7--------#

from m.prnt import prnt
from .gv        import gv

def mark_oos(pdf_pg):
    for key in pdf_pg:
        pdf              = key.split('|')[0]
        engine, dpi, lv  = gv.pdf_meta.get(key, ('', '', ''))
        # ncv entries have no marking png, skip OOS processing for them
        if dpi == 'nd':
            continue
        for fmto in pdf_pg[key]:
            [fm, to] = fmto
            gv.cur.execute(
                'INSERT INTO sorter(pdf, pg_fm, pg_to, docname, engine, dpi, lv) '
                'VALUES(?, ?, ?, ?, ?, ?, ?)',
                (pdf, fm, to, '_OOS', engine, dpi, lv))
            if fm == to:
                prnt(f'{pdf} {fm}')
            else:
                prnt(f'{pdf} {fm}-{to}')
