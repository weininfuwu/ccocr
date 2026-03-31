#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   p1.py       250222  cy 
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import json

from .chk       import chk
from m.prnt     import prnt
from ...env     import jkv

def p1(bn,jsn):
    with open(jsn, encoding='utf-8') as f:
        jsn = json.load(f)
    chk(list(jsn.keys()), jkv.top, f'''JSN TOP LV KEY ERR
    json     : {bn}
    expected : {jkv.top}
    detected : {list(jsn.keys())}''')
    jsn = jsn['analyzeResult']
    chk(jsn['version'],jkv.apiv,f'''API VERSION ERR
    json     : {bn}
    expected : {jkv.apiv}
    detected : {jsn['version']}''')
    chk(jsn['modelVersion'], jkv.mdlv, f'''MODEL VERSION ERR
    json      : {bn}
    expcected : {jkv.mdlv}
        detected  : {jsn['modelVersion']}''')
    return jsn

