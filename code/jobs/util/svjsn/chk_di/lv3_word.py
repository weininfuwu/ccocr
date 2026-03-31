#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   lv3_word.py     260327  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

from .chk       import chk
from m.prnt     import prnt
from jobs.env   import jkvs

jkv = jkvs.DI

def lv3_word(bn,jsn,pcnt,wcnt):
    chk(list(jsn.keys()), jkv.word, f'''WORD LV KEY ERR
    json      : {bn} p{pcnt+1} w{wcnt+1}
    expected  : {jkv.word}
    detected  : {list(jsn.keys())}''')

    if len(jsn['polygon']) != 8:
        raise Exception(f'''WORD polygon length ERR
    json      : {bn} p{pcnt+1} w{wcnt+1}
    expected  : 8
    detected  : {len(jsn['polygon'])}''')

    if 'offset' not in jsn['span'] or 'length' not in jsn['span']:
        raise Exception(f'''WORD span keys ERR
    json      : {bn} p{pcnt+1} w{wcnt+1}
    detected  : {jsn['span']}''')
