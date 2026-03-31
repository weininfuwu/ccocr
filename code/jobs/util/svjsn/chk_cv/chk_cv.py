#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   chk_cv.py       260324  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import glob
import json
import os

from m.prnt     import prnt
from m.env      import D
from jobs.env   import DD
from .lv1       import lv1
from .lv2       import lv2
from .lv3       import lv3
from .lv4       import lv4

def chk_cv(bn,jsn):
    prnt(f'checking lv1 (top) of {bn}')
    jsns1 = lv1(bn,jsn)                          # ['analyzeResult']
    for pcnt,jsn2 in enumerate(jsns1):
        prnt(f'checking lv2 (page) of {bn} pg{pcnt+1}')
        jsns2 = lv2(bn,jsn2,pcnt)               # ['readResults']
        for lcnt,jsn3 in enumerate(jsns2):
            jsns3 = lv3(bn,jsn3,pcnt,lcnt)
            for wcnt,jsn4 in enumerate(jsns3):
                lv4(bn,jsn4,pcnt,lcnt,wcnt)
    jsnrawPls = os.path.join(D.logd,'jsnRAW+')
    os.makedirs(jsnrawPls, exist_ok=True)
    with open(os.path.join(
                        jsnrawPls,f'{bn}.CV.json'),'w',encoding='utf-8') as f:
        json.dump(jsn, f, indent=2, ensure_ascii=False)
    return jsn
