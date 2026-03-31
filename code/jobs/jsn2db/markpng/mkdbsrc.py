#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   mkdbsrc.py  230224  cy
#   updated: 260321 strip engine suffix from pdf_name, add engine to rtn
#   updated: 260322 add usepng to rtn; derive from STRAIGHT in pdf_name
#   updated: 260322 add engine/usepng to rtn_page
#
#--------1---------2---------3---------4---------5---------6---------7--------#

from m.prnt import prnt

def _strip_engine(pdf_name):
    for tag in (' CV', ' DI'):
        if pdf_name.endswith(tag):
            return pdf_name[:-len(tag)], tag.strip()
    return pdf_name, ''

def _derive_usepng(pdf_name):
    # pdf_name at this point still has the STRAIGHT / from PNG label
    # (engine suffix has NOT yet been stripped)
    if ' STRAIGHT' in pdf_name:
        return 'straight'
    return 'png'

def mkdbsrc(drwlst_rot):
    rtn      = []
    rtn_page = []
    for pdf_labeled in drwlst_rot:
        usepng         = _derive_usepng(pdf_labeled)
        pdf, engine    = _strip_engine(pdf_labeled)
        for page in drwlst_rot[pdf_labeled]:
            ptop = 999999999
            plft = 999999999
            pryt = 0
            for i in drwlst_rot[pdf_labeled][page]:
                [junk,node,TL,TR,BR,BL,txt,conf] = i
                [junk1,junk2,typ] = junk
                top  = min(TL[1],TR[1])
                btm  = max(BL[1],BR[1])
                lft  = min(TL[0],BL[0])
                ryt  = max(TR[0],BR[0])
                ptop = min(ptop,top)
                plft = min(plft,lft)
                pryt = max(pryt,ryt)
            zoom = 1200 / (pryt - plft)
            # rtn_page: include engine/usepng so each row is unambiguous
            rtn_page.append([pdf, page, ptop, plft, pryt, engine, usepng])
            for i in drwlst_rot[pdf_labeled][page]:
                [junk,node,TL,TR,BR,BL,txt,conf] = i
                [junk1,junk2,typ] = junk
                top = min(TL[1],TR[1])
                btm = max(BL[1],BR[1])
                lft = min(TL[0],BL[0])
                ryt = max(TR[0],BR[0])
                rtn.append([ pdf, page, node, typ,
                        round((top-ptop)*zoom),
                        round((btm-ptop)*zoom),
                        round((lft-plft)*zoom),
                        round((ryt-plft)*zoom),
                        txt,
                        top, btm, lft, ryt, conf,
                        engine,     # index 14
                        usepng,     # index 15
                        ])
    prnt(f'{len(rtn_page)} pages, {len(rtn)} elements')
    return [rtn, rtn_page]
