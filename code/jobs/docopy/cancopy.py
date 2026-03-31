#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   cancopy.py      250324  cy
#   updated: 260319.172930 by cy
#   updated: 260328 opt比較: png2api=Falseならdpi/qlty不問
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import glob
import json
import os
import re

from m.env      import D
from m.prnt     import prnt
from jobs.env   import DD

def _opt_match(old, new):
    """png2api=False なら dpi/qlty は比較しない"""
    if old['engines'] != new['engines']:
        return False
    if old['pdf2api'] != new['pdf2api']:
        return False
    if old['png2api'] != new['png2api']:
        return False
    if new['png2api']:
        if old['dpi'] != new['dpi']:
            return False
        if old['qlty'] != new['qlty']:
            return False
    return True


def cancopy():
    hit = False
    logbase = os.path.normpath(os.path.join(D.logd,r'..'))
    for itm in sorted(glob.glob(os.path.join(logbase,'*')), reverse=True):
        bn = os.path.basename(itm)
        if os.path.isfile(itm):
            prnt(f'{bn} skip due to not dir')
            continue
#        m = re.search(r'^[a-z]{2}\d{3}(\.\d{6}){3}$',bn)
        m = re.search(r'_\d{6}(\.\d{6}){2}$',bn)
        if m == None:
            prnt(f'{bn} skip due to dirname NG')
            continue
        if not os.path.isfile(os.path.join(itm,'dumpdb_ok.txt')):
            prnt(f'{bn} skip due to no "dumpdb_ok.txt"')
            continue
        if not os.path.isfile(os.path.join(itm,'opt+imgs.json')):
            prnt(f'{bn} skip due to no "opt+imgs.json"')
            continue
        with open(os.path.join(itm,'opt+imgs.json') ,encoding='utf-8') as f:
            jsn = json.load(f)
        if not _opt_match(jsn['opt'], DD.frmopt):
            prnt(f'{bn} skip due to "frmopt" not same')
            prnt(f'''
 jsn['opt'] -- old_log
 {jsn['opt']}
 DD.frmopt
 {DD.frmopt}''')
            continue
        if jsn['imgs'] != DD.imgs:
            prnt(f'{bn} skip due to "imgs" not same')
            prnt(f'''
 jsn['imgs'] -- old_log
 {jsn['imgs']}
 DD.imgs
 {DD.imgs}''')
            continue
        prnt(f'{bn} HIT!')
        DD.cpysrc = itm
        hit = True
        break
    if not hit:
        return False
    return True
