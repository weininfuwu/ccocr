#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   p4.py       250222  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

from .chk       import chk
from m.prnt     import prnt
from ...env     import jkv

def p4(bn,jsn,cntp,node,wnode,elmlst,pginfo):
    node += 1
    wnode += 1
    [img_fn,pg,angl,ww,hh] = pginfo
    chk(list(jsn.keys()),jkv.word,f'''jobid words NODE KEY ERR
    image file: {bn} {cntp+1} {node+1} {wnode+1}
    expcected : {jkv.word}
    detected  : {list(jsn.keys())}''')
    #### 230615 try pickup confidence info
    try:
        conft = jsn['confidence']
    except Exception:
        prnt(f''''NO confidence, set Zero:
    {bn}: node {node}.{wnode} "{jsn['text']}"''')
        conft = 0
    elmlst.append(
        [img_fn,pg,ww,hh,angl,'wrd',f'{node}.{wnode}'] +
        jsn['boundingBox'] + [jsn['text']] + [conft] )
    #### 230615 END try pickup confidence info
    return
