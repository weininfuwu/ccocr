#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   setup_flds.py       250131  cy
#   updated: 260319.190153 by cy
#   updated: 260321 add jsnRAW dir
#   updated: 260329 remove pdfpg (unused)
#
#   this is for 'frm' mode
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import glob
import os
import shutil

from m.env              import D
from m.prnt             import prnt
from ..util.msg         import shutilerr
from ..env              import DD
from .cred import cred_all

def setup_flds():

    cred_all(DD.engines)
    quit()  # 260330 動作確認用 TODO: 削除

    inputd      = os.path.join(D.logd,'input')
    img         = os.path.join(D.logd,'img')        # picfile in input
    pngPRE      = os.path.join(D.logd,'pngPRE')     # png of abv
    pngUP       = os.path.join(D.logd,'pngUP')      # PNG converted files for API
    jsn         = os.path.join(D.logd,'jsn')        # marged json    : jsnd
    jsn_raw     = os.path.join(D.logd,'jsnRAW')     # API responses (CV + DI)
    pngROT      = os.path.join(D.logd,'pngROT')
    pngMRKD     = os.path.join(D.logd,'pngMRKD')
    pngRMRKD    = os.path.join(D.logd,'pngRMRKD')
    ingored     = os.path.join(D.logd,'IGNORED')
    usrd        = os.path.dirname(D.fpath)
    src_flsk    = os.path.normpath(os.path.join(
                    os.path.dirname(__file__),r'..','aby','use_web','FLASK'))

    flskrt      = os.path.join(D.logd,'flsk')
    shutil.copytree(src_flsk,flskrt)
    spic        = os.path.join(flskrt,'static','spic')
    btnsf       = os.path.join(flskrt,'templates','include','btns.html')
    tblsf       = os.path.join(flskrt,'templates','include','tables.html')
    DD.flskrt   = flskrt
    DD.spic     = spic
    DD.btnsf    = btnsf
    DD.tblsf    = tblsf

    os.mkdir(img)
    os.mkdir(pngPRE)
    os.mkdir(pngUP)
    os.mkdir(jsn)
    os.mkdir(jsn_raw)
    DD.inputd           = inputd
    DD.img              = img
    DD.pngPRE           = pngPRE
    DD.pngUP            = pngUP
    DD.jsn      = jsn
    DD.jsn_raw  = jsn_raw
    DD.usrd     = usrd

    DD.outd     = os.path.join(D.sysFld,'output')
    DD.thisOutd = None

    return
