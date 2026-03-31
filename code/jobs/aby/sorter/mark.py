#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   mark.py     230407      cy
#   updated: 260321 insert engine into sorter
#   updated: 260322 insert usepng into sorter; key is now 'pdf|engine|usepng'
#
#--------1---------2---------3---------4---------5---------6---------7--------#

from m.prnt import prnt
from .gv    import gv

def mark(docname, key, pg_fm, pg_to):
    pdf              = key.split('|')[0]
    engine, dpi, lv  = gv.pdf_meta.get(key, ('', '', ''))
    gv.cur.execute(
        'INSERT INTO sorter(pdf, pg_fm, pg_to, docname, engine, dpi, lv) '
        'VALUES(?, ?, ?, ?, ?, ?, ?)',
        (pdf, pg_fm, pg_to, docname, engine, dpi, lv))
