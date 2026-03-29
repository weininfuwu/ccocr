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
#     "apisrc" : "cnvpng" | "original",
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
import re

from m.prnt       import prnt
from m.env        import D
from jobs.env     import DD
from .jsn4db_cv   import convert_cv
from .jsn4db_di   import convert_di


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
        out = convert_cv(jsn)
    elif engine == 'intelli':
        tag = 'DI'
        out = convert_di(jsn)
    else:
        raise Exception(f'jsn4db: unknown engine: {engine}')

    out['engine'] = tag
    out['dpi']    = DD.frmopt['dpi']
    out['qlty']   = DD.frmopt['qlty']
    out['apisrc'] = apisrc

    if apisrc == 'cnvpng':
        pg_num = int(re.search(r'\.(\d+)\.png$', bn).group(1))
        out['pages'][0]['page'] = pg_num
        # hoge.ext.2d.lv0.01.png -> hoge.ext
        base = re.sub(r'\.(2d|3d|4d)\.lv\d\.\d{2}\.png$', '', bn)
        dpi_s = DD.frmopt['dpi']
        lv_s  = DD.frmopt['qlty']
        dst  = os.path.join(jsn4db_dir,
                            f'{base}.{tag}.{dpi_s}.{lv_s}.json')
        if os.path.exists(dst):
            with open(dst, 'r', encoding='utf-8') as f:
                existing = json.load(f)
            existing['pages'].extend(out['pages'])
            out = existing
    else:
        # ncv: bn = hoge.ext (original filename)
        base = bn
        dst  = os.path.join(jsn4db_dir,
                            f'{base}.{tag}.json')

    out['pdf'] = base

    with open(dst, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    prnt(f'jsn4db ({tag}) saved   {os.path.basename(dst)}')
    return out, dst

