#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   drwpng.py   260328  cy
#
#   Create pngROT (rotation-corrected), pngMK (pre-rotation marked),
#   pngRMK (post-rotation marked) from dump.db + pngPRE.
#   Called from control.py after svjsn().
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import os
import sqlite3

from m.env    import D
from m.prnt   import prnt
from jobs.env import DD
from jobs.jsn2db.markpng.blnkpng  import blnkpng
from jobs.jsn2db.markpng.rotate   import rotate
from jobs.jsn2db.markpng.nTyp     import nTyp
from jobs.jsn2db.markpng.draw     import draw
from jobs.jsn2db.markpng.draw_rot import draw_rot


def drwpng():
    _setup_dirs()
    pdfs, elmlst = _load_db()
    if not pdfs:
        prnt('drwpng: no cnvpng entries, skip')
        return
    blnkpng(pdfs, DD.pngPRE, DD.pngROT)
    drwlst     = _mk_drwlst(elmlst, pdfs)
    drwlst_rot = _mk_drwlst_rot(elmlst, pdfs)
    draw(drwlst,         DD.pngPRE, DD.pngMK)
    draw_rot(drwlst_rot, DD.pngROT, DD.pngRMK)
    prnt('drwpng done')


def _setup_dirs():
    for attr, name in [
        ('pngROT', 'pngROT'),
        ('pngMK',  'pngMK'),
        ('pngRMK', 'pngRMK'),
    ]:
        d = os.path.join(D.logd, name)
        os.mkdir(d)
        setattr(DD, attr, d)


def _load_db():
    """
    Returns:
      pdfs   : { pdf: { page: {angl, jw, jh} } }
               ow/oh filled in later by blnkpng()
      elmlst : list of tuples from elm WHERE apisrc='cnvpng'
    """
    con = sqlite3.connect(DD.dbf)
    cur = con.cursor()

    pdfs = {}
    cur.execute(
        'SELECT pdf, page, angl, jw, jh '
        'FROM page WHERE apisrc = "cnvpng"')
    for pdf, page, angl, jw, jh in cur.fetchall():
        pdfs.setdefault(pdf, {})
        if page not in pdfs[pdf]:
            pdfs[pdf][page] = {
                'angl': angl, 'jw': jw, 'jh': jh}

    cur.execute('''
        SELECT pdf, page, node, typ,
               otl_x, otl_y, otr_x, otr_y,
               obr_x, obr_y, obl_x, obl_y,
               txt, conf, engine
        FROM elm WHERE apisrc = "cnvpng"''')
    elmlst = cur.fetchall()
    con.close()
    return pdfs, elmlst


def _mk_drwlst(elmlst, pdfs):
    """Build draw list for pngMK (pre-rotation marking)."""
    drwlst = {}
    for row in elmlst:
        (pdf, page, node, typ,
         tl_x, tl_y, tr_x, tr_y,
         br_x, br_y, bl_x, bl_y,
         txt, conf, engine) = row
        pg = pdfs[pdf][page]
        ow, oh = pg['ow'], pg['oh']
        jw, jh = pg['jw'], pg['jh']
        tl = (round(tl_x * ow / jw), round(tl_y * oh / jh))
        tr = (round(tr_x * ow / jw), round(tr_y * oh / jh))
        br = (round(br_x * ow / jw), round(br_y * oh / jh))
        bl = (round(bl_x * ow / jw), round(bl_y * oh / jh))
        lvl = nTyp.wrd if '.' in node else nTyp.line
        key = (pdf, engine)
        drwlst.setdefault(key, {})
        drwlst[key].setdefault(page, [])
        drwlst[key][page].append([lvl, node, tl, tr, br, bl])
    return drwlst


def _mk_drwlst_rot(elmlst, pdfs):
    """Build draw list for pngRMK (post-rotation marking)."""
    drwlst_rot = {}
    for row in elmlst:
        (pdf, page, node, typ,
         otl_x, otl_y, otr_x, otr_y,
         obr_x, obr_y, obl_x, obl_y,
         txt, conf, engine) = row
        pg = pdfs[pdf][page]
        tl, tr, br, bl = rotate(
            pg['angl'],
            otl_x, otl_y, otr_x, otr_y,
            obr_x, obr_y, obl_x, obl_y,
            pg['ow'], pg['oh'], pg['jw'], pg['jh'])
        lvl = nTyp.wrd if '.' in node else nTyp.line
        key = (pdf, engine)
        drwlst_rot.setdefault(key, {})
        drwlst_rot[key].setdefault(page, [])
        drwlst_rot[key][page].append(
            [lvl, node, tl, tr, br, bl, txt, conf])
    return drwlst_rot
