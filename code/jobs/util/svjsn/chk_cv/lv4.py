#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   lv4.py      260326  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

from .chk       import chk
from m.prnt     import prnt
from jobs.env   import jkvs

jkv = jkvs.CV

def lv4(bn,jsn,pcnt,lcnt,wcnt):
    chk(list(jsn.keys()),jkv.word,f'''WORD LV KEY ERR
    json      : {bn} p{pcnt+1} l{lcnt+1} w{wcnt+1}
    expcected : {jkv.word}
    detected  : {list(jsn.keys())}''')
    return
