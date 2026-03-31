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
    #
    chk(list(jsn.keys()), jkv.top, f'''jsn lv1 keys check ERR
    json     : {bn}
    expected : {jkv.top}
    detected : {list(jsn.keys())}''')
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

    chk(jsn['contentFormat'], jkv.cfmt, f'''jsn lv1 contentFormat check ERR
    json     : {bn}
    expected : {jkv.cfmt}
    detected : {jsn['contentFormat']}''')

    return jsn['pages']
