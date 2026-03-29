#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   drwpng.py   260328  cy
#   updated: 260328 STR/CNV naming; handle both apisrc; inline draw
#   updated: 260328 fix jw/jh per (engine,apisrc) via page_geom
#
#   Create pngROT, pngMK, pngRMK from dump.db + pngPRE.
#   Called from control.py after svjsn().
#
#   pngROT  hoge.ext.01.png            rotation-corrected canvas
#   pngMK   hoge.ext.{STR|CNV}.{CV|DI}.{page:02d}.png
#   pngRMK  hoge.ext.{STR|CNV}.{CV|DI}.{page:02d}.png
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import os
import sqlite3

import cv2

from m.env      import D
from m.prnt     import prnt
from m.cv2read  import cv2read
from m.cv2write import cv2write
from jobs.env   import DD
from jobs.util.s2l              import s2l
from jobs.jsn2db.markpng.blnkpng import blnkpng
from jobs.jsn2db.markpng.rotate  import rotate
from jobs.jsn2db.markpng.nTyp    import nTyp

def _dpi_lv_tag(apisrc):
    if apisrc == 'original':
        return 'nd.lvn'
    from jobs.env import DD as _DD
    return f'{_DD.frmopt["dpi"]}.{_DD.frmopt["qlty"]}'


def drwpng():
    _setup_dirs()
    pdfs, page_geom, data = _load_db()
    if not pdfs:
        prnt('drwpng: no entries, skip')
        return
    blnkpng(pdfs, DD.pngPRE, DD.pngROT)
    _draw_mk(data, pdfs, page_geom)
    _draw_rmk(data, pdfs, page_geom)
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
      pdfs      : { pdf: { page: {angl, jw, jh} } }
                  one entry per (pdf, page) — first-encountered angl used for blnkpng()
                  ow/oh filled in later by blnkpng()
      page_geom : { (pdf, page, engine, apisrc): {jw, jh} }
                  per-combination jw/jh for correct coordinate scaling
      data      : { (pdf, tag, engine): { page: [(node, tl_x..bl_y)] } }
                  tag = 'CNV' or 'STR'
    """
    con = sqlite3.connect(DD.dbf)
    cur = con.cursor()

    pdfs = {}
    page_geom = {}
    cur.execute('SELECT pdf, page, angl, jw, jh, engine, apisrc FROM page')
    for pdf, page, angl, jw, jh, engine, apisrc in cur.fetchall():
        pdfs.setdefault(pdf, {})
        pdfs[pdf].setdefault(
            page, {'angl': angl, 'jw': jw, 'jh': jh})
        page_geom[(pdf, page, engine, apisrc)] = {'jw': jw, 'jh': jh}

    cur.execute('''
        SELECT pdf, page, node,
               otl_x, otl_y, otr_x, otr_y,
               obr_x, obr_y, obl_x, obl_y,
               engine, apisrc
        FROM elm''')
    data = {}
    for row in cur.fetchall():
        (pdf, page, node,
         tl_x, tl_y, tr_x, tr_y,
         br_x, br_y, bl_x, bl_y,
         engine, apisrc) = row
        key = (pdf, apisrc, engine)
        data.setdefault(key, {})
        data[key].setdefault(page, [])
        data[key][page].append((
            node,
            tl_x, tl_y, tr_x, tr_y,
            br_x, br_y, bl_x, bl_y))
    con.close()
    return pdfs, page_geom, data


def _draw_mk(data, pdfs, page_geom):
    """pngPRE + pre-rotation boxes -> pngMK"""
    for (pdf, apisrc, engine), pages in data.items():
        for page, elems in pages.items():
            ow  = pdfs[pdf][page]['ow']
            oh  = pdfs[pdf][page]['oh']
            geom = page_geom[(pdf, page, engine, apisrc)]
            jw  = geom['jw']
            jh  = geom['jh']
            src = os.path.join(
                DD.pngPRE, s2l(pdf, page, 'png'))
            dst = os.path.join(
                DD.pngMK,
                _dstname(pdf, apisrc, engine, page))
            img = cv2read(src)
            for (node,
                 tl_x, tl_y, tr_x, tr_y,
                 br_x, br_y, bl_x, bl_y) in elems:
                tl = (round(tl_x * ow / jw),
                      round(tl_y * oh / jh))
                tr = (round(tr_x * ow / jw),
                      round(tr_y * oh / jh))
                br = (round(br_x * ow / jw),
                      round(br_y * oh / jh))
                bl = (round(bl_x * ow / jw),
                      round(bl_y * oh / jh))
                _boxes(img, node, tl, tr, br, bl)
            cv2write(dst, img)


def _draw_rmk(data, pdfs, page_geom):
    """pngROT + post-rotation boxes -> pngRMK"""
    for (pdf, apisrc, engine), pages in data.items():
        for page, elems in pages.items():
            pg   = pdfs[pdf][page]
            ow   = pg['ow']
            oh   = pg['oh']
            angl = pg['angl']
            geom = page_geom[(pdf, page, engine, apisrc)]
            jw   = geom['jw']
            jh   = geom['jh']
            src  = os.path.join(
                DD.pngROT, s2l(pdf, page, 'png'))
            dst  = os.path.join(
                DD.pngRMK,
                _dstname(pdf, apisrc, engine, page))
            img  = cv2read(src)
            for (node,
                 otl_x, otl_y, otr_x, otr_y,
                 obr_x, obr_y, obl_x, obl_y) in elems:
                tl, tr, br, bl = rotate(
                    angl,
                    otl_x, otl_y, otr_x, otr_y,
                    obr_x, obr_y, obl_x, obl_y,
                    ow, oh, jw, jh)
                _boxes(img, node, tl, tr, br, bl)
            cv2write(dst, img)


def _boxes(img, node, tl, tr, br, bl):
    is_word   = '.' in node
    color     = nTyp.wrd[1]  if is_word else nTyp.line[1]
    thickness = nTyp.wrd[0]  if is_word else nTyp.line[0]
    org = (br[0], br[1] + 20) if is_word else (tl[0], tl[1] - 10)
    cv2.line(img, tl, tr, color, thickness)
    cv2.line(img, tr, br, color, thickness)
    cv2.line(img, br, bl, color, thickness)
    cv2.line(img, bl, tl, color, thickness)
    cv2.putText(img, node, org,
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 1)


def _dstname(pdf, apisrc, engine, page):
    dpi_lv = _dpi_lv_tag(apisrc)
    return f'{pdf}.{engine}.{dpi_lv}.{page:02d}.png'
