#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   spic.py     230425  cy
#   updated: 260321 use webp for web, jpg for excel
#   updated: 260322 replace use_noup_png() global with do.usepng check
#   updated: 260328 remove use_noup (NOUP files gone); guard ww>=1; guard oww/ohh==0
#   updated: 260328 use rotate() to transform coords to pngROT space (fix rotated docs)
#   updated: 260329 remove straight-entry skip (pngROT and polygon are same for all combos)
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import os
import sqlite3
import cv2

from m.prnt             import prnt
from m.cv2read          import cv2read
from m.cv2write         import cv2write
from m.env              import D
from ...env             import DD
from ...util.s2l        import s2l
from jobs.jsn2db.markpng.rotate import rotate


def _load_geom():
    """Load polygon points and page geometry from dump.db."""
    con = sqlite3.connect(DD.dbf)
    cur = con.cursor()
    poly = {}
    cur.execute(
        'SELECT seq, otl_x, otl_y, otr_x, otr_y, obr_x, obr_y, obl_x, obl_y FROM elm')
    for row in cur.fetchall():
        seq, tl_x, tl_y, tr_x, tr_y, br_x, br_y, bl_x, bl_y = row
        poly[seq] = (tl_x, tl_y, tr_x, tr_y, br_x, br_y, bl_x, bl_y)
    geom = {}
    cur.execute('SELECT pdf, page, angl, jw, jh FROM page')
    for pdf, page, angl, jw, jh in cur.fetchall():
        geom[(pdf, page)] = (angl, jw, jh)
    con.close()
    return poly, geom


def spic(dig):
    prnt('making spics')
    spicdir = DD.spic

    ext = '.webp' if DD.use_web else '.jpg'

    poly, geom = _load_geom()

    clipped = [
        int(i.replace(ext,'')) for i in
        list(filter(lambda x: x.endswith(ext), os.listdir(spicdir))) ]
    err_png = os.path.join(spicdir,'error.png')
    op_png  = os.path.join(spicdir,'op.png')
    np_png  = os.path.join(spicdir,'no_papa.png')
    for docname in dig:
        for docObj in dig[docname]:
            for io in docObj.itm:
                if io.dl.clm is None:
                    continue
                if io.txt is None or io.txt == '':
                    if io.dl.op == 'op':
                        io.spic = op_png
                    elif io.p_nopapa:
                        io.spic = np_png
                    else:
                        io.spic = err_png
                    continue
                if io.seq in clipped:
                    io.spic = os.path.join(spicdir, f'{io.seq}{ext}')
                    continue
                clipped.append(io.seq)
                _longname = s2l(docObj.pdf, io.page, 'png')
                png = os.path.join(DD.pngROT, _longname)
                png = cv2read(png)
                oh, ow = png.shape[:2]
                # transform polygon to pngROT coordinate space via rotate()
                if io.seq not in poly or (docObj.pdf, io.page) not in geom:
                    io.spic = err_png
                    continue
                tl_x, tl_y, tr_x, tr_y, br_x, br_y, bl_x, bl_y = poly[io.seq]
                angl, jw, jh = geom[(docObj.pdf, io.page)]
                # For inch coords (straight mode, jw≈8.26), pass pngROT pixel
                # dims so rotate() scales inch→pixel correctly.
                # For pixel coords (png mode, jw≈1700), scale=1.0 as before.
                if jw < 50:
                    rw, rh = ow, oh
                else:
                    rw, rh = jw, jh
                tl, tr, br, bl = rotate(
                    angl,
                    tl_x, tl_y, tr_x, tr_y, br_x, br_y, bl_x, bl_y,
                    rw, rh, rw, rh)
                xs = [tl[0], tr[0], br[0], bl[0]]
                ys = [tl[1], tr[1], br[1], bl[1]]
                top  = max(min(ys) - 10, 0)
                btm  = min(max(ys) + 10, oh)
                lft  = max(min(xs) - 10, 0)
                ryt  = min(max(xs) + 10, ow)
                clip = png[top:btm, lft:ryt]
                oww  = ryt - lft
                ohh  = btm - top
                if oww <= 0 or ohh <= 0:
                    io.spic = err_png
                    continue
                hh   = int(30 * (30/46))
                ww   = max(1, int(hh * (oww / ohh)))
                clip = cv2.resize(clip, (ww, hh))
                cv2write(os.path.join(spicdir, f'{io.seq}{ext}'), clip)
                io.spic = os.path.join(spicdir, f'{io.seq}{ext}')
    return
