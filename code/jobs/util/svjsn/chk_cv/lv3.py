#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   lv3.py      260326  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

from .chk       import chk
from m.prnt     import prnt
from jobs.env   import jkvs

jkv = jkvs.CV

def lv3(bn,jsn,pcnt,lcnt):
    chk(list(jsn.keys()),jkv.line,f'''LINE LV KEY ERR
    json      : {bn} p{pcnt+1} l{lcnt}
    expcected : {jkv.line}
    detected  : {list(jsn.keys())}''')

    chk(list(jsn['appearance'].keys()), jkv.appearance,
    f'''apparance KEY ERR
    json      : {bn} p{pcnt+1} l{lcnt}
    expcected : {jkv.appearance}
    detected  : {list(jsn['appearance'].keys())}''')

    if jsn['appearance']['style']['name'] not in jkv.app_val:
        raise Exception(f'''appearence.style.name HAS UNKNOWN VALUE
    json      : {bn} p{pcnt+1} l{lcnt}
    expcected : {jkv.app_val}
    detected  : {jsn['appearance']['style']['name']}''')

    if 'confidence' not in jsn['appearance']['style']:
        prnt((  f'NO confidence, set Zero: {bn} p{pcnt} l{lcnt} '
                f'({jsn["text"]})'))
        jsn['appearance']['style']['confidence'] = 0

    return jsn['words']

