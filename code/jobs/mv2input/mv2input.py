#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   mv2input.py     250324  cy
#   updated: 260319.161758 by cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import glob
import hashlib
import json
import os
import shutil

from m.env          import D
from m.prnt         import prnt
from jobs.env       import DD
from jobs.util.msg  import shutilerr,noimg

#from .ldmsconf  import ldmsconf
from .ldmsconf.ldmsconf  import ldmsconf

def mv2input():
    inputd      = os.path.join(D.logd,'input')
    DD.inputd   = inputd
    usrd        = os.path.dirname(D.fpath)
    DD.usrd     = usrd
    try:
        os.makedirs(inputd)
        for fname in os.listdir(usrd):
            src = os.path.join(usrd, fname)
            if os.path.isfile(src):
                shutil.copy2(src, inputd)
    except Exception as e:
        prnt(f'''error while copying files from usrd, quitting
  {e}''')
        shutilerr(usrd,e)
        quit()
    #
    #   check config file
    #
    msconf = ldmsconf()
    msg = ''
    imgs = []
    for itm in sorted(glob.glob(os.path.join(inputd,'*'))):
        kwd = 'f' if os.path.isfile(itm) else 'd'
        bn = os.path.basename(itm)
        ext = os.path.splitext(bn)[1].lower()[1:]
        use = 'use ' if ext in DD.imgext else 'skip'
        if use == 'use ':
            imgs.append(itm)
        msg += f'\n  {kwd} {use} {bn}'
    prnt(f'items in inputd{msg}')

    if len(imgs) == 0:
        prnt(f'no image to process in\n  {usrd}')
        noimg(usrd)
        quit()

    jsn = []
    for itm in imgs:
        bn = os.path.basename(itm)
        with open(itm,'rb') as f:
            dat = f.read()
        sha3 = hashlib.sha3_512(dat).hexdigest()
        jsn.append([bn,sha3])
    DD.imgs = jsn

    jsn = {'opt' : DD.frmopt, 'imgs' : jsn }
    with open(os.path.join(D.logd,'opt+imgs.json'),'w',encoding='utf-8') as f:
        json.dump(jsn,f,indent=2,ensure_ascii=False)
    prnt(f'opt+imgs.json saved\n{json.dumps(jsn, indent=2, ensure_ascii=False)}')
    return msconf
