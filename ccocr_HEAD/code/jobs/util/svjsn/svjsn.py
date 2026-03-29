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
import re

_CNV_PAT = re.compile(r'^(.+)\.(2d|3d|4d)\.(lv\d)\.(\d{2})\.png$')

from azure.ai.documentintelligence   import DocumentIntelligenceClient
from azure.core.credentials          import AzureKeyCredential

from m.prnt         import prnt
from jobs.env       import DD
from .updn_cv       import updn_cv
from .updn_di       import updn_di
from .wrd2line      import wrd2line
from .jsn4db        import jsn4db
from .dump2db       import dump2db

from .chk_cv.chk_cv     import chk_cv
from .chk_di.chk_di     import chk_di


def svjsn():
    if 'intelli' in DD.engines:
        client = DocumentIntelligenceClient(
            endpoint   = DD.di_ep                       ,
            credential = AzureKeyCredential(DD.di_key)  )
        DD.cred_ok = True
        prnt('DI clinent loaded')

    jsn4db_results = {}
    for png in sorted(glob.glob(os.path.join(DD.pngUP, '*'))):
        bn = os.path.basename(png)
        prnt(f'letting API read {bn}')
        m_cnv  = _CNV_PAT.match(bn)
        apisrc = 'cnvpng' if m_cnv else 'original'
        for engine in DD.engines:
            eng_tag = 'CV' if engine == 'vision' else 'DI'
            if m_cnv:
                base, dpi_s, lv_s, nn = m_cnv.groups()
                jsnf = os.path.join(DD.jsn_raw,
                                    f'{base}.{eng_tag}.{dpi_s}.{lv_s}.{nn}.json')
            else:
                jsnf = os.path.join(DD.jsn_raw, f'{bn}.{eng_tag}.json')
            if engine == 'vision':
                jsn = updn_cv(png, jsnf)
                jsn = chk_cv(bn, jsn)
            elif engine == 'intelli':
                jsn = updn_di(png, jsnf, client)
                jsn = chk_di(bn, jsn)
            else:
                raise Exception(f'unknown engine: {engine}')
            jsn = wrd2line(bn, jsn, engine, jsnf)
            out, dst = jsn4db(bn, jsn, engine, apisrc)
            jsn4db_results[dst] = out

    dump2db(jsn4db_results)
    return
