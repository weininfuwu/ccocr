#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   lv2.py      260325  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

from .chk               import chk
from m.prnt             import prnt
from jobs.env           import jkvs
from jobs.util.l2s      import l2s

jkv = jkvs.CV

def lv2(bn,jsn,pcnt):
    chk(list(jsn.keys()), jkv.page, f'''jsn lv2 keys check ERR
        json      : {bn}
        expcected : {jkv.page}
        detected  : {list(jsn.keys())}''')
    if jsn['lines'] == []:
        prnt(f'adding dummy line and word to {bn} pg{pcnt}')
        jsn['lines'].append({
            "boundingBox": [ 145, 35, 161, 35, 161, 58, 145, 58 ],
            "text": "DUMMYlineFORblankPAGE",
            "appearance": {
                    "style": { "name": "other", "confidence": 1 } },
            "words": [ {
                "boundingBox": [ 145, 35, 161, 35, 161, 58, 145, 58 ],
                "text": "dummyWORDforBLANKpage",
                "confidence": 1 } ] })
    return jsn['lines']
