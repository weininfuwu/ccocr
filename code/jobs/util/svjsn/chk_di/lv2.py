#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   lv2.py      260327  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

from .chk               import chk
from m.prnt             import prnt
from jobs.env           import jkvs

jkv = jkvs.DI

def lv2(bn,jsn,pcnt):
    chk(list(jsn.keys()), jkv.page, f'''jsn lv2 keys check ERR
        json      : {bn}
        expected  : {jkv.page}
        detected  : {list(jsn.keys())}''')

    if jsn['lines'] == [] and jsn['words'] == []:
        prnt(f'adding dummy line and word to {bn} pg{pcnt+1}')
        jsn['lines'].append({
            "content"  : "DUMMYlineFORblankPAGE",
            "polygon"  : [ 1.0, 0.1, 1.5, 0.1, 1.5, 0.2, 1.0, 0.2 ],
            "spans"    : [ { "offset": 0, "length": 21 } ] })
        jsn['words'].append({
            "content"   : "dummyWORDforBLANKpage",
            "polygon"   : [ 1.0, 0.1, 1.5, 0.1, 1.5, 0.2, 1.0, 0.2 ],
            "confidence": 1.0,
            "span"      : { "offset": 0, "length": 21 } })

    return jsn['lines'], jsn['words']
