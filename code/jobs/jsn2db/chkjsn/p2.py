#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   p2.py       250222  cy
#   updated: 260321 allow orphan_words key (DI-only)
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import re

from .chk               import chk
from m.prnt             import prnt
from ...env             import jkv, DD
from ...util.l2s      import l2s
#from ...util.orgname  import orgname

def p2(bn,jsn):
    # orphan_words is a DI-only extra key, ignore it for key validation
    keys_to_check = [k for k in jsn.keys() if k != 'orphan_words']
    chk(keys_to_check, jkv.page, f'''PAGE LV KEY ERR
        json      : {bn}
        expcected : {jkv.page}
        detected  : {list(jsn.keys())}''')
    angl = jsn['angle']
    ww = jsn['width']
    hh = jsn['height']
    if not any(jsn['lines']):

        prnt(f'adding dummy line and word\n  {bn}')
        jsn['lines'].append({
            "boundingBox": [ 145, 35, 161, 35, 161, 58, 145, 58 ],
            "text": "DUMMYlineFORblankPAGE",
            "appearance": {
                    "style": { "name": "other", "confidence": 1 } },
            "words": [ {
                "boundingBox": [ 145, 35, 161, 35, 161, 58, 145, 58 ],
                "text": "dummyWORDforBLANKpage",
                "confidence": 1 } ] })

    img_fn, img_pg = l2s(bn)
#    if DD.jobtyp == 'cnf':
#        img_fn, img_pg = l2s(bn)
#    elif DD.jobtyp == 'frm':
#        img_fn, img_pg = orgname(bn)
#    else:
#        raise Exception('PG BUG')
    return [img_fn,img_pg,angl,ww,hh]
