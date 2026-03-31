#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   jsn4db_util.py  260328  cy
#   updated: 260328 raw4 returns 12-tuple (min/max + 8-pt polygon)
#
#   Shared geometry helpers for jsn4db converters.
#
#--------1---------2---------3---------4---------5---------6---------7--------#


def raw4(bb):
    # bb: [TL_x, TL_y, TR_x, TR_y, BR_x, BR_y, BL_x, BL_y]
    tl_x, tl_y = bb[0], bb[1]
    tr_x, tr_y = bb[2], bb[3]
    br_x, br_y = bb[4], bb[5]
    bl_x, bl_y = bb[6], bb[7]
    top = min(tl_y, tr_y)
    btm = max(br_y, bl_y)
    lft = min(tl_x, bl_x)
    ryt = max(tr_x, br_x)
    return (top, btm, lft, ryt,
            tl_x, tl_y, tr_x, tr_y,
            br_x, br_y, bl_x, bl_y)


def page_bounds(elems):
    ptop = min(e[0] for e in elems)
    plft = min(e[2] for e in elems)
    pryt = max(e[3] for e in elems)
    return ptop, plft, pryt


def zoom(plft, pryt):
    width = pryt - plft
    return 1200 / width if width > 0 else 1.0


def elem(node, raw, ptop, plft, zm, text, conf):
    (top, btm, lft, ryt,
     tl_x, tl_y, tr_x, tr_y,
     br_x, br_y, bl_x, bl_y) = raw
    return {
        'node' : node,
        'top'  : round((top - ptop) * zm),
        'btm'  : round((btm - ptop) * zm),
        'lft'  : round((lft - plft) * zm),
        'ryt'  : round((ryt - plft) * zm),
        'otop' : top,
        'obtm' : btm,
        'olft' : lft,
        'oryt' : ryt,
        'otl_x': tl_x, 'otl_y': tl_y,
        'otr_x': tr_x, 'otr_y': tr_y,
        'obr_x': br_x, 'obr_y': br_y,
        'obl_x': bl_x, 'obl_y': bl_y,
        'text' : text,
        'conf' : conf,
    }
