#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   lv1.py      260325  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import json

from .chk       import chk
from m.prnt     import prnt
from jobs.env   import jkvs

jkv = jkvs.CV

def lv1(bn,jsn):
    #
    #   check level 1 key exists or not
    #
    chk(list(jsn.keys()), jkv.top, f'''jsn lv1 keys check ERR
    json     : {bn}
    expected : {jkv.top}
    detected : {list(jsn.keys())}''')
    #
    #   key/value check for jsn['analyzeResult']
    #
    jsn = jsn['analyzeResult']
    chk(jsn['version'],jkv.apiv,f'''jsn lv1 api version check ERR
    json     : {bn}
    expected : {jkv.apiv}
    detected : {jsn['version']}''')
    chk(jsn['modelVersion'], jkv.mdlv, f'''jsn lv1 model version check ERR
    json      : {bn}
    expcected : {jkv.mdlv}
        detected  : {jsn['modelVersion']}''')
    return jsn['readResults']

