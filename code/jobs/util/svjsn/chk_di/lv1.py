#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   lv1.py      260327  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

from .chk       import chk
from m.prnt     import prnt
from jobs.env   import jkvs

jkv = jkvs.DI

def lv1(bn,jsn):
    #
    #   check top-level keys exist
    #   'paragraphs' may be absent only when all pages have empty lines and words
    #
    required = [k for k in jkv.top if k != 'paragraphs']
    missing  = [k for k in required if k not in jsn]
    if missing:
        raise Exception(f'''jsn lv1 keys check ERR
    json     : {bn}
    expected : {jkv.top}
    detected : {list(jsn.keys())}
    missing  : {missing}''')
    if 'paragraphs' not in jsn:
        for pg in jsn.get('pages', []):
            if pg.get('lines') or pg.get('words'):
                raise Exception(f'''jsn lv1 paragraphs missing ERR
    json     : {bn}
    expected : {jkv.top}
    detected : {list(jsn.keys())}''')
        prnt(f'paragraphs absent (blank): {bn}')
    #
    #   version / model / format checks
    #
    chk(jsn['apiVersion'], jkv.apiv, f'''jsn lv1 apiVersion check ERR
    json     : {bn}
    expected : {jkv.apiv}
    detected : {jsn['apiVersion']}''')

    chk(jsn['modelId'], jkv.mdl, f'''jsn lv1 modelId check ERR
    json     : {bn}
    expected : {jkv.mdl}
    detected : {jsn['modelId']}''')

    chk(jsn['stringIndexType'], jkv.sit, f'''jsn lv1 stringIndexType check ERR
    json     : {bn}
    expected : {jkv.sit}
    detected : {jsn['stringIndexType']}''')

    chk(jsn['contentFormat'], jkv.cfmt, f'''jsn lv1 contentFormat check ERR
    json     : {bn}
    expected : {jkv.cfmt}
    detected : {jsn['contentFormat']}''')

    if not isinstance(jsn['styles'], list):
        raise Exception(f'''jsn lv1 styles type ERR
    json     : {bn}
    expected : list
    detected : {type(jsn['styles'])}''')

    return jsn['pages']
