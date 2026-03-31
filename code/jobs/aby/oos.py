#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   oos.py  220704 cy
#   updated: 260321 strip engine suffix before s2l()
#   updated: 260322 read usepng from sorter; straight OOS rows are skipped
#             (mark_oos.py no longer inserts straight rows into _OOS)
#   updated: 260328 remove use_noup; fix pngRMK filename to new naming
#
#--------1---------2---------3---------4---------5---------6---------7--------#
import os
import shutil
import sqlite3

from PIL import Image

from m.prnt             import prnt
from m.env              import D
from ..env              import DD
from ..util.s2l         import s2l

def oos():
    pngRMK  = DD.pngRMK
    dumpdb  = DD.dbf
    ignrd   = os.path.join(D.logd, 'IGNORED')
    con     = sqlite3.connect(dumpdb)
    cur     = con.cursor()
    rtn     = cur.execute(
        "SELECT pdf, pg_fm, pg_to, dpi, lv, engine FROM sorter WHERE docname = '_OOS'"
        ).fetchall()
    for i in rtn:
        [pdf, pg, pg_to, dpi, lv, engine] = i
        # ncv rows are not inserted into _OOS by mark_oos, but guard anyway
        if dpi == 'nd':
            continue
        os.makedirs(ignrd, exist_ok=True)
        while pg <= pg_to:
            longname = f'{pdf}.{engine}.{dpi}.{lv}.{pg:02d}.png'
            prnt(longname)
            shutil.copy(os.path.join(pngRMK, longname), ignrd)
            pg += 1
    return
