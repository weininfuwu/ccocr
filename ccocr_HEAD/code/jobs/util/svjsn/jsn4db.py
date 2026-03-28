#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   jsn4db.py       260327  cy
#
#   Convert jsnRAW++ (CV and DI) into DB-ready JSON and save to jsn4db/.
#
#   Coordinates (polygon for DI, boundingBox for CV) share the same layout:
#     [TL_x, TL_y, TR_x, TR_y, BR_x, BR_y, BL_x, BL_y]
#
#   For each page:
#     - raw top/btm/lft/ryt are derived from the 8-point bbox via min/max
#     - page boundary (ptop/plft/pryt) is the union of all elements on the page
#     - normalized coords are scaled so that lft_min=0, ryt_max=1200
#
#   Output JSON (jsn4db/<bn>.<CV|DI>.json):
#   {
#     "engine" : "CV" | "DI",
#     "dpi"    : "200dpi" | "300dpi" | "400dpi",
#     "qlty"   : "lv1" | "lv2" | "lv3",
#     "usepng" : true | false | "BOTH",
#     "pages"  : [
#       {
#         "page" : 1,
#         "ptop" : <int>,   raw  (for DB page table)
#         "plft" : <int>,   raw
#         "pryt" : <int>,   raw
#         "lines": [
#           {
#             "node" : "1",
#             "top"  : <int>,   normalized 0-1200
#             "btm"  : <int>,
#             "lft"  : <int>,
#             "ryt"  : <int>,
#             "otop" : <int>,   raw
#             "obtm" : <int>,
#             "olft" : <int>,
#             "oryt" : <int>,
#             "text" : "...",
#             "conf" : <float>,
#             "words": [
#               {
#                 "node" : "1.1",
#                 "top"  : <int>,
#                 "btm"  : <int>,
#                 "lft"  : <int>,
#                 "ryt"  : <int>,
#                 "otop" : <int>,
#                 "obtm" : <int>,
#                 "olft" : <int>,
#                 "oryt" : <int>,
#                 "text" : "...",
#                 "conf" : <float>
#               }
#             ]
#           }
#         ],
#         "orphan_words": [...]   # DI only; same word structure, node="orphan.N"
#       }
#     ]
#   }
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import json
import os

from m.prnt   import prnt
from m.env    import D
from jobs.env import DD


# ---------------------------------------------------------------------------
# public entry point
# ---------------------------------------------------------------------------

def jsn4db(bn, jsn, engine, apisrc):
    """
    bn     : base filename  (e.g. 'foo.pdf.STRAIGHT.pdf')
    jsn    : dict returned by wrd2line()  (jsnRAW++ content)
    engine : 'vision' or 'intelli'
    apisrc : 'cnvpng' if PNG was sent to API, 'original' if file was sent as-is

    Converts coordinates to normalized top/btm/lft/ryt (0-1200 scale),
    writes result to jsn4db/<bn>.<CV|DI>.json.
    Returns the written dict.
    """
    jsn4db_dir = os.path.join(D.logd, 'jsn4db')
    os.makedirs(jsn4db_dir, exist_ok=True)

    if engine == 'vision':
        tag = 'CV'
        out = _convert_cv(jsn)
    elif engine == 'intelli':
        tag = 'DI'
        out = _convert_di(jsn)
    else:
        raise Exception(f'jsn4db: unknown engine: {engine}')

    out['engine'] = tag
    out['dpi']    = DD.frmopt['dpi']
    out['qlty']   = DD.frmopt['qlty']
    out['apisrc'] = apisrc
    dst = os.path.join(jsn4db_dir, f'{bn}.{tag}.json')
    with open(dst, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    prnt(f'jsn4db ({tag}) saved   {os.path.basename(dst)}')
    return out


# ---------------------------------------------------------------------------
# per-engine converters
# ---------------------------------------------------------------------------

def _convert_cv(jsn):
    pages_raw = jsn['analyzeResult']['readResults']
    pages_out = []
    for page_raw in pages_raw:
        page_num  = page_raw['page']
        lines_raw = page_raw.get('lines', [])

        elems = _collect_cv(lines_raw)
        ptop, plft, pryt = _page_bounds(elems)
        zoom = _zoom(plft, pryt)

        lines_out = []
        for lno, line in enumerate(lines_raw, 1):
            lraw = _raw4(line['boundingBox'])
            conf = line.get('appearance', {}).get('style', {}).get('confidence', 1.0)
            words_out = []
            for wno, word in enumerate(line.get('words', []), 1):
                wraw = _raw4(word['boundingBox'])
                words_out.append(_elem(
                    f'{lno}.{wno}', wraw, ptop, plft, zoom,
                    word.get('text', ''), word.get('confidence', 1.0)))
            lines_out.append({
                **_elem(str(lno), lraw, ptop, plft, zoom,
                        line.get('text', ''), conf),
                'words': words_out,
            })

        pages_out.append({
            'page' : page_num,
            'ptop' : ptop,
            'plft' : plft,
            'pryt' : pryt,
            'lines': lines_out,
        })

    return {'pages': pages_out}


def _convert_di(jsn):
    pages_raw = jsn.get('pages', [])
    pages_out = []
    for page_raw in pages_raw:
        page_num  = page_raw.get('pageNumber', 1)
        lines_raw = page_raw.get('lines', [])
        orphans   = page_raw.get('orphan_words', [])

        elems = _collect_di(lines_raw, orphans)
        ptop, plft, pryt = _page_bounds(elems)
        zoom = _zoom(plft, pryt)

        lines_out = []
        for lno, line in enumerate(lines_raw, 1):
            lraw = _raw4(line['polygon'])
            words_out = []
            for wno, word in enumerate(line.get('words', []), 1):
                wraw = _raw4(word['polygon'])
                words_out.append(_elem(
                    f'{lno}.{wno}', wraw, ptop, plft, zoom,
                    word.get('content', ''), word.get('confidence', 1.0)))
            lines_out.append({
                **_elem(str(lno), lraw, ptop, plft, zoom,
                        line.get('content', ''), 1.0),
                'words': words_out,
            })

        page_dict = {
            'page' : page_num,
            'ptop' : ptop,
            'plft' : plft,
            'pryt' : pryt,
            'lines': lines_out,
        }

        if orphans:
            orphans_out = []
            for ono, word in enumerate(orphans, 1):
                wraw = _raw4(word['polygon'])
                orphans_out.append(_elem(
                    f'orphan.{ono}', wraw, ptop, plft, zoom,
                    word.get('content', ''), word.get('confidence', 1.0)))
            page_dict['orphan_words'] = orphans_out

        pages_out.append(page_dict)

    return {'pages': pages_out}


# ---------------------------------------------------------------------------
# geometry helpers
# ---------------------------------------------------------------------------

def _raw4(bb):
    # bb: [TL_x, TL_y, TR_x, TR_y, BR_x, BR_y, BL_x, BL_y]
    top = min(bb[1], bb[3])
    btm = max(bb[5], bb[7])
    lft = min(bb[0], bb[6])
    ryt = max(bb[2], bb[4])
    return top, btm, lft, ryt


def _collect_cv(lines_raw):
    elems = []
    for line in lines_raw:
        elems.append(_raw4(line['boundingBox']))
        for word in line.get('words', []):
            elems.append(_raw4(word['boundingBox']))
    return elems


def _collect_di(lines_raw, orphans):
    elems = []
    for line in lines_raw:
        elems.append(_raw4(line['polygon']))
        for word in line.get('words', []):
            elems.append(_raw4(word['polygon']))
    for word in orphans:
        elems.append(_raw4(word['polygon']))
    return elems


def _page_bounds(elems):
    ptop = min(e[0] for e in elems)
    plft = min(e[2] for e in elems)
    pryt = max(e[3] for e in elems)
    return ptop, plft, pryt


def _zoom(plft, pryt):
    width = pryt - plft
    return 1200 / width if width > 0 else 1.0


def _elem(node, raw, ptop, plft, zoom, text, conf):
    top, btm, lft, ryt = raw
    return {
        'node' : node,
        'top'  : round((top - ptop) * zoom),
        'btm'  : round((btm - ptop) * zoom),
        'lft'  : round((lft - plft) * zoom),
        'ryt'  : round((ryt - plft) * zoom),
        'otop' : top,
        'obtm' : btm,
        'olft' : lft,
        'oryt' : ryt,
        'text' : text,
        'conf' : conf,
    }
