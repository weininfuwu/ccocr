#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   chk_di.py       260327  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import json
import os

from m.prnt         import prnt
from m.env          import D
from jobs.env       import DD
from .lv1           import lv1
from .lv2           import lv2
from .lv3_line      import lv3_line
from .lv3_word      import lv3_word

def chk_di(bn,jsn):
    prnt(f'checking lv1 (top) of {bn}')
    jsns1 = lv1(bn,jsn)                            # jsn['pages']
    for pcnt,jsn2 in enumerate(jsns1):
        prnt(f'checking lv2 (page) of {bn} pg{pcnt+1}')
        lines,words = lv2(bn,jsn2,pcnt)            # (lines[], words[])
        for lcnt,jsn3 in enumerate(lines):
            lv3_line(bn,jsn3,pcnt,lcnt)
        for wcnt,jsn4 in enumerate(words):
            lv3_word(bn,jsn4,pcnt,wcnt)
    jsnrawPls = os.path.join(D.logd,'jsnRAW+')
    os.makedirs(jsnrawPls, exist_ok=True)
    with open(os.path.join(
                        jsnrawPls,f'{bn}.DI.json'),'w',encoding='utf-8') as f:
        json.dump(jsn, f, indent=2, ensure_ascii=False)
    return jsn
