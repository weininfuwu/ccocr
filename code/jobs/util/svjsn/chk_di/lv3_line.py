#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   lv3_line.py     260327  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

from .chk       import chk
from m.prnt     import prnt
from jobs.env   import jkvs

jkv = jkvs.DI

def lv3_line(bn,jsn,pcnt,lcnt):
    chk(list(jsn.keys()), jkv.line, f'''LINE LV KEY ERR
    json      : {bn} p{pcnt+1} l{lcnt+1}
    expected  : {jkv.line}
    detected  : {list(jsn.keys())}''')

    if len(jsn['polygon']) != 8:
        raise Exception(f'''LINE polygon length ERR
    json      : {bn} p{pcnt+1} l{lcnt+1}
    expected  : 8
    detected  : {len(jsn['polygon'])}''')

    if not isinstance(jsn['spans'], list) or len(jsn['spans']) == 0:
        raise Exception(f'''LINE spans ERR (empty or not list)
    json      : {bn} p{pcnt+1} l{lcnt+1}
    detected  : {jsn['spans']}''')
