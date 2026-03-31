#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   mkdrwlst_rot.py
#   updated: 260322 skip straight entries (no marking png exists)
#   updated: 260322 key changed to (bare, engine) for per-engine PNG output
#
#--------1---------2---------3---------4---------5---------6---------7--------#

from .rotate        import rotate
from .nTyp          import nTyp
from .mkdbsrc       import _strip_engine
from ...util.usepng import strip_label

def mkdrwlst_rot(elmlst, pdfs):
    drwlst = {}
    for i in elmlst:
        [pdf_name,page,jw,jh,angl,typ,node,
        otl_x,otl_y,otr_x,otr_y,obr_x,obr_y,obl_x,obl_y,txt,conf,usepng] = i
        # straight entries have no marking png; skip drawing
        if usepng == 'straight':
            continue
        bare, engine = _strip_engine(strip_label(pdf_name))
        ow = pdfs[pdf_name][page]['ow']
        oh = pdfs[pdf_name][page]['oh']
        tl,tr,br,bl = rotate(
            angl,otl_x,otl_y,otr_x,otr_y,obr_x,obr_y,obl_x,obl_y,ow,oh,jw,jh)
        lvl = nTyp.wrd if '.' in node else nTyp.line
        key = (bare, engine)
        drwlst.setdefault(key, {})
        drwlst[key].setdefault(page, [])
        drwlst[key][page].append([lvl,node,tl,tr,br,bl,txt,conf])
    return drwlst
