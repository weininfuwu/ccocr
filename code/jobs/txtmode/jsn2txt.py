#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   jsn2txt.py  250302  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import glob
import json
import os
import re
import shutil

from m.prnt     import prnt
from m.env      import D
from jobs.env   import DD

def jsn2txt():
    jsnd    = DD.jsn
    txtd    = os.path.join(D.logd,'text')
    DD.txtd = txtd
    os.mkdir(txtd)
    for jsn in sorted(glob.glob(os.path.join(jsnd,'*'))):
        docname = os.path.splitext(os.path.basename(jsn))[0]
        m = re.search(r'^(.*)\.(\d+)$',docname)
        if m == None:
            raise Exception(f'regex error for {docname}')
        prnt(f'm.groups() {m.groups()}')
        [docname,page] = m.groups()
        prnt(f'writing {docname}.txt')
        if page == '01':
            txt = f'++++++++++++ {docname} ++++++++++++\n'
        else:
            txt = ''
        with open(jsn, encoding='utf-8') as f:
            doc = json.load(f)
        for pg in doc['analyzeResult']['readResults']:
            txt += f'++++++ page {page} ++++++\n'
            for ln in pg['lines']:
                txt += f'{ln["text"]}\n'
        with open(
                os.path.join(txtd,f'{docname}.txt'),'a',encoding='utf-8') as f:
            f.write(txt)
    outd = os.path.join(DD.usrd,D.jobid)
    os.mkdir(outd)
    for txt in sorted(glob.glob(os.path.join(txtd,'*'))):
        shutil.copy(txt,outd)
