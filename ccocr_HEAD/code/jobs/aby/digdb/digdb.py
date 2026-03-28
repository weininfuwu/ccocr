#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   digdb.py    230421  cy
#   updated: 260321 strip engine suffix from pdf, set do.engine
#   updated: 260322 read usepng from sorter, set do.usepng
#   updated: 260329 pass engine/apisrc to digin() → SQL filter (fix mixed-elm crash)
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import os
import pickle
import sqlite3

from m.env                  import D
from m.prnt                 import prnt
from ...env                 import DD
from .gv                    import gv
from .digin.digin           import digin
from .spic                  import spic

def digdb(docdef):

    db      = DD.dbf
    jobdir  = D.logf
    jobid   = D.jobid

    dig     = {}
    gv.con  = sqlite3.connect(db)
    gv.cur  = gv.con.cursor()
    rtn     = gv.cur.execute(
        'SELECT pdf, pg_fm, pg_to, docname, docnum, engine, usepng '
        'FROM sorter ORDER BY docnum'
        ).fetchall()
    _apisrc_map = {'png': 'cnvpng', 'straight': 'original'}
    for i in rtn:
        [pdf, fm, to, docname, docnum, engine, usepng] = i
        if docname == '_OOS':
            continue
        apisrc = _apisrc_map.get(usepng, usepng)
        dig.setdefault(docname, [])
        dos = digin(docname, docdef, pdf, fm, to, docnum, jobid, engine, apisrc)
        for do in dos:
            do.engine = engine  if engine  else ''
            do.usepng = usepng  if usepng  else ''
        dig[docname] += dos
    if DD.use_spic:
        spic(dig)
    return dig
