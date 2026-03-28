#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   spic.py     230425  cy
#   updated: 260321 use webp for web, jpg for excel
#   updated: 260322 replace use_noup_png() global with do.usepng check
#   updated: 260328 remove use_noup (NOUP files gone); guard ww>=1
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import os
import cv2

from m.prnt             import prnt
from m.cv2read          import cv2read
from m.cv2write         import cv2write
from m.env              import D
from ...env             import DD
from ...util.s2l        import s2l

def spic(dig):
    prnt('making spics')
    spicdir = DD.spic

    ext = '.webp' if DD.use_web else '.jpg'

    clipped = [
        int(i.replace(ext,'')) for i in
        list(filter(lambda x: x.endswith(ext), os.listdir(spicdir))) ]
    err_png = os.path.join(spicdir,'error.png')
    op_png  = os.path.join(spicdir,'op.png')
    np_png  = os.path.join(spicdir,'no_papa.png')
    for docname in dig:
        for docObj in dig[docname]:
            # straight entries have no rotated marking png; skip spic entirely
            if docObj.usepng == 'straight':
                for io in docObj.itm:
                    if io.dl.clm is None:
                        continue
                    io.spic = err_png   # placeholder so downstream never sees None
                continue
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
                h, w = png.shape[:2]
                top  = max(io.otop - 10, 0)
                btm  = min(io.obtm + 10, h)
                lft  = max(io.olft - 10, 0)
                ryt  = min(io.oryt + 10, w)
                clip = png[top:btm, lft:ryt]
                oww  = ryt - lft
                ohh  = btm - top
                hh   = int(30 * (30/46))
                ww   = max(1, int(hh * (oww / ohh)))
                clip = cv2.resize(clip, (ww, hh))
                cv2write(os.path.join(spicdir, f'{io.seq}{ext}'), clip)
                io.spic = os.path.join(spicdir, f'{io.seq}{ext}')
    return
