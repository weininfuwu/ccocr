#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   p3.py       250222  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

from .chk       import chk
from m.prnt     import prnt
from ...env     import jkv

def p3(bn,jsn,cntp,node,elmlst,pginfo):
    node += 1
    [img_fn,pg,angl,ww,hh] = pginfo
    chk(list(jsn.keys()),jkv.line,f'''LINE LV KEY ERR
    json      : {bn} {cntp+1} {node}
    expcected : {jkv.line}
    detected  : {list(jsn.keys())}''')

    chk(list(jsn['appearance'].keys()), jkv.appearance,
    f'''apparance KEY ERR
    json      : {bn} {cntp+1} {node}
    expcected : {jkv.appearance}
    detected  : {list(jsn['appearance'].keys())}''')

    if jsn['appearance']['style']['name'] not in jkv.app_val:
        raise Exception(f'''appearence.style.name HAS UNKNOWN VALUE
    json      : {bn} {cntp+1} {node}
    expcected : {jkv.app_val}
    detected  : {jsn['appearance']['style']['name']}''')

    #### 230615 try pickup confidence info
    try:
        conf = jsn['appearance']['style']['confidence']
    except Exception:
        prnt(f'''NO confidence, set Zero:
  {bn}: node {node} "{jsn['text']}"''')
        conf = 0
    elmlst.append(  [img_fn,pg,ww,hh,angl,'lin',str(node)] +
                    jsn['boundingBox'] + [jsn['text']] + [conf])
    #### 230615 END try pickup confidence info
    return

