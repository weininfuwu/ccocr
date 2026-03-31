#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   draw_straight.py    260322  cy
#
#   BOTH mode: draw STRAIGHT OCR bounding boxes onto NOUP.png.
#
#   STRAIGHT JSON coords are in inch units (jw/jh).
#   NOUP.png pixel size is ow/oh (filled by blnkpng into pdfs_bare).
#   Conversion: pixel_x = inch_x * ow / jw
#
#   pngMK  <- draw on pngORG (pngPRE) NOUP.png  (pre-rotation)
#   pngRMK <- draw on pngROT          NOUP.png  (post-rotation)
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import os

import cv2

from m.cv2read          import cv2read
from m.cv2write         import cv2write
from m.prnt             import prnt
from ...util.s2l        import s2l
from ...util.usepng     import strip_label
from .mkdbsrc           import _strip_engine
from .nTyp              import nTyp


def draw_straight(elmlst_straight, pdfs_bare, dir_org, dir_mk, dir_rmk):
    """
    Draw STRAIGHT OCR bounding boxes onto NOUP.png files.

    elmlst_straight : straight entries from elmlst (usepng=='straight')
    pdfs_bare       : {bare_pdf: {page: {ow, oh, rw, rh, jw, jh, angl}}}
                      filled by blnkpng() -- provides pixel dimensions
    dir_org         : pngPRE  (source for pngMK)
    dir_mk          : pngMK   (destination, pre-rotation)
    dir_rmk         : pngRMK  (destination, post-rotation)
    """
    prnt('draw_straight: drawing STRAIGHT OCR results onto NOUP.png')

    # group elements by (bare, page, engine)
    pages = {}
    for i in elmlst_straight:
        [pdf_labeled, page, jw, jh, angl, typ, node,
         otl_x, otl_y, otr_x, otr_y, obr_x, obr_y, obl_x, obl_y,
         txt, conf, usepng] = i
        pdf, engine = _strip_engine(pdf_labeled)
        bare        = strip_label(pdf)
        key         = (bare, page, engine)
        pages.setdefault(key, {'jw': jw, 'jh': jh, 'items': []})
        lvl = nTyp.wrd if '.' in node else nTyp.line
        pages[key]['items'].append([lvl, node,
                                    otl_x, otl_y, otr_x, otr_y,
                                    obr_x, obr_y, obl_x, obl_y])

    for (bare, page, engine), v in pages.items():
        eng_tag = f'.{engine}' if engine else ''
        jw   = v['jw']
        jh   = v['jh']

        if bare not in pdfs_bare or page not in pdfs_bare[bare]:
            prnt(f'draw_straight: no pdfs_bare entry for {bare} p{page}, skipping')
            continue

        ow = pdfs_bare[bare][page]['ow']
        oh = pdfs_bare[bare][page]['oh']
        rw = pdfs_bare[bare][page].get('rw', ow)
        rh = pdfs_bare[bare][page].get('rh', oh)

        longname     = s2l(bare, page, 'png')
        longname_src = longname[:-len('.png')] + '.NOUP.png'
        longname_dst = longname[:-len('.png')] + f'{eng_tag}.STR.png'

        # --- pngMK (pre-rotation, from pngORG) ---
        src_mk = os.path.join(dir_org, longname_src)
        dst_mk = os.path.join(dir_mk,  longname_dst)
        if os.path.isfile(src_mk):
            img = cv2read(src_mk)
            for item in v['items']:
                [drwvar, node,
                 otl_x, otl_y, otr_x, otr_y,
                 obr_x, obr_y, obl_x, obl_y] = item
                tl = (round(otl_x * ow / jw), round(otl_y * oh / jh))
                tr = (round(otr_x * ow / jw), round(otr_y * oh / jh))
                br = (round(obr_x * ow / jw), round(obr_y * oh / jh))
                bl = (round(obl_x * ow / jw), round(obl_y * oh / jh))
                [thickness, color, cls] = drwvar
                org = (tl[0], tl[1] - 10) if cls == 'line' else (br[0], br[1] + 20)
                cv2.line(img, tl, tr, color, thickness)
                cv2.line(img, tr, br, color, thickness)
                cv2.line(img, br, bl, color, thickness)
                cv2.line(img, bl, tl, color, thickness)
                cv2.putText(img, node, org,
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 1)
            cv2write(dst_mk, img)
            prnt(f'draw_straight -> pngMK  {longname_dst}')
        else:
            prnt(f'draw_straight: src not found for pngMK: {src_mk}')

        # --- pngRMK (post-rotation, from pngROT) ---
        src_rmk = os.path.join(dir_rmk, longname_src)
        dst_rmk = os.path.join(dir_rmk, longname_dst)
        if os.path.isfile(src_rmk):
            img = cv2read(src_rmk)
            for item in v['items']:
                [drwvar, node,
                 otl_x, otl_y, otr_x, otr_y,
                 obr_x, obr_y, obl_x, obl_y] = item
                # use rotated image pixel dimensions for coord conversion
                tl = (round(otl_x * rw / jw), round(otl_y * rh / jh))
                tr = (round(otr_x * rw / jw), round(otr_y * rh / jh))
                br = (round(obr_x * rw / jw), round(obr_y * rh / jh))
                bl = (round(obl_x * rw / jw), round(obl_y * rh / jh))
                [thickness, color, cls] = drwvar
                org = (tl[0], tl[1] - 10) if cls == 'line' else (br[0], br[1] + 20)
                cv2.line(img, tl, tr, color, thickness)
                cv2.line(img, tr, br, color, thickness)
                cv2.line(img, br, bl, color, thickness)
                cv2.line(img, bl, tl, color, thickness)
                cv2.putText(img, node, org,
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 1)
            cv2write(dst_rmk, img)
            prnt(f'draw_straight -> pngRMK {longname_dst}')
        else:
            prnt(f'draw_straight: src not found for pngRMK: {src_rmk}')
