#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   setupdb.py      230411      cy
#   updated: 260321 add engine column to sorter, read from elm.engine
#   updated: 260322 add usepng column to sorter, read from elm.usepng
#             key = 'pdf|engine|usepng' to distinguish all combinations
#   updated: 260328 elm.usepng -> elm.apisrc; map cnvpng/original -> png/straight
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import sqlite3

from .gv import gv

def setupdb(dumpdb):
    gv.ddb = dumpdb
    gv.con = sqlite3.connect(dumpdb)
    gv.cur = gv.con.cursor()
    gv.cur.execute(f'''
        CREATE TABLE IF NOT EXISTS sorter (
            docnum  INTEGER PRIMARY KEY AUTOINCREMENT,  -- 01
            pdf     TEXT,                               -- 02
            pg_fm   INTEGER,                            -- 03
            pg_to   INTEGER,                            -- 04
            docname TEXT,                               -- 05
            engine  TEXT,                               -- 06  'CV' / 'DI' / ''
            usepng  TEXT                                -- 07  'png' / 'straight'
        )''')
    tmplst = gv.cur.execute(
            'SELECT DISTINCT pdf, page, engine, apisrc FROM elm ORDER BY pdf, page'
            ).fetchall()
    # key = 'pdf|engine|usepng' to uniquely identify each processing variant
    _apisrc2usepng = {'cnvpng': 'png', 'original': 'straight'}
    pdf_pg     = {}
    pdf_meta   = {}     # key -> (engine, usepng)
    for i in tmplst:
        pdf, page, engine, apisrc = i[0], i[1], i[2] or '', i[3] or ''
        usepng = _apisrc2usepng.get(apisrc, apisrc)
        key = f'{pdf}|{engine}|{usepng}'
        pdf_pg.setdefault(key, [])
        pdf_pg[key].append(page)
        pdf_meta[key] = (engine, usepng)
    for key in pdf_pg:
        pdf_pg[key] = [[min(pdf_pg[key]), max(pdf_pg[key])]]
    gv.pdf_meta = pdf_meta  # replaces old gv.pdf_engine
    return pdf_pg
