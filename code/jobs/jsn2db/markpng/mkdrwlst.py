#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   mkdrwlst.py 230222  cy
#   updated: 260322 skip straight entries (no marking png exists)
#   updated: 260322 key changed to (bare, engine) for per-engine PNG output
#
#--------1---------2---------3---------4---------5---------6---------7--------#
from .nTyp      import nTyp
from .mkdbsrc   import _strip_engine
from ...util.usepng import strip_label

def mkdrwlst(elmlst, pdfs):
    drwlst = {}
    for i in elmlst:
        [pdf_name,page,jsn_max_x,jsn_max_y,angl,typ,node,
        tl_x,tl_y,tr_x,tr_y,br_x,br_y,bl_x,bl_y,txt,cnf,usepng] = i
        # straight entries have no marking png; skip drawing
        if usepng == 'straight':
            continue
        bare, engine = _strip_engine(strip_label(pdf_name))
        png_max_x = pdfs[pdf_name][page]['ow']
        png_max_y = pdfs[pdf_name][page]['oh']
        tl = (round(tl_x * png_max_x / jsn_max_x), round(tl_y * png_max_y / jsn_max_y))
        tr = (round(tr_x * png_max_x / jsn_max_x), round(tr_y * png_max_y / jsn_max_y))
        br = (round(br_x * png_max_x / jsn_max_x), round(br_y * png_max_y / jsn_max_y))
        bl = (round(bl_x * png_max_x / jsn_max_x), round(bl_y * png_max_y / jsn_max_y))
        lvl = nTyp.wrd if '.' in node else nTyp.line
        key = (bare, engine)
        drwlst.setdefault(key, {})
        drwlst[key].setdefault(page, [])
        drwlst[key][page].append([lvl,node,tl,tr,br,bl])
    return drwlst
