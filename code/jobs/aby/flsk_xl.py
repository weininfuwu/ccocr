#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   flsk_xl.py      250606  cy
#   updated: 260320.170237 by cy
#   updated: 260321 handle _xl suffix for both mode
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import json
import os
import shutil

import openpyxl

from m.prnt             import prnt
from m.env              import D
from jobs.env           import DD
from .use_web.use_web   import use_web

def flsk_xl():
    DD.thisOutd = os.path.join(DD.outd,D.jobid)
    D.outdir    = DD.thisOutd
    if D.EMBEDDED != True:
        os.makedirs(DD.thisOutd, exist_ok=True)
    if DD.use_web:
        use_web()
    if DD.use_macro and D.EMBEDDED != True:
        xl_suffix = ''
        xlsm = os.path.join(D.logd,f'{D.jobid}{xl_suffix}.xlsm')
        shutil.copy(xlsm,DD.thisOutd)


    if DD.use_spic == False:
        prnt('NO PIC mode')

#        xlsm = os.path.join(D.logd,f'{D.jobid}.xlsx')
        # updated: 260320.152202 by cy (claud.ai)
        xlsm = os.path.join(D.logd,f'{D.jobid}.xlsm')
        os.makedirs(DD.thisOutd, exist_ok=True)

        shutil.copy(xlsm,DD.thisOutd)

    ignored = os.path.join(D.logd,'IGNORED')
    if os.path.isdir(ignored):
        shutil.copytree(ignored,os.path.join(DD.thisOutd,'IGNORED'))


    if DD.skipPdf != []:
        skipTxt = '\n'.join(DD.skipPdf)
        skipTxt = ( 'Below listed PDFs are using "90ms-RKSJ-H" encoding.\n'
                    'PDF->PNG conversion will LOSE text on page.\n\n'
                    'Use "NO PNG converion" option in config XL.\n\n'
                    f'{skipTxt}')
        skipMsg = os.path.join(DD.thisOutd,'NEED_PREPROCESS.txt')
        with open(skipMsg,'w',encoding='utf-8') as f:
            f.write(skipTxt)
        shutil.copy(skipMsg,D.logd)
        prnt('skip message saved')


    with open(os.path.join(D.logd,'dumpdb_ok.txt'),'w') as f:
        f.write('okok')
    return

