#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   svjsn.py    260000  cy
#   updated: 260320.093640 by cy
#   updated: 260321 split CV/DI json dirs, add .CV./.DI. suffix to filename
#   updated: 260321 wire updn_di for intelli engine
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import glob
import os

from azure.ai.documentintelligence   import DocumentIntelligenceClient
from azure.core.credentials          import AzureKeyCredential

from m.prnt         import prnt
from jobs.env       import DD
from .updn_cv       import updn_cv
from .updn_di       import updn_di
from .wrd2line      import wrd2line

from .chk_cv.chk_cv     import chk_cv
from .chk_di.chk_di     import chk_di


def svjsn():
    if 'intelli' in DD.engines:
        client = DocumentIntelligenceClient(
            endpoint   = DD.di_ep                       ,
            credential = AzureKeyCredential(DD.di_key)  )
        DD.cred_ok = True
        prnt('DI clinent loaded')

    for png in sorted(glob.glob(os.path.join(DD.pngUP, '*'))):
        bn = os.path.basename(png)
        prnt(f'letting API read {bn}')
        for engine in DD.engines:
            if engine == 'vision':
                jsnf = os.path.join(DD.jsn_raw, f'{bn}.CV.json')
                jsn = updn_cv(png,jsnf)
                jsn = chk_cv(bn,jsn)
            elif engine == 'intelli':
                jsnf = os.path.join(DD.jsn_raw, f'{bn}.DI.json')
                jsn = updn_di(png,jsnf,client)
                jsn = chk_di(bn,jsn)
            else:
                raise Exception(f'unknown engine: {engine}')
            wrd2line(bn, jsn, engine)
    return
