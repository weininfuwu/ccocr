#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   pdf2png.py  250131  cy
#   updated: 260320.095341 by cy
#
#   ref
#   https://aijimy.com/dx/python-ocr-technique/
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import glob
import shutil
import os

from PIL        import ImageFile

from m.prnt             import prnt
from m.env              import D
from jobs.env           import DD
from jobs.txtmode.twoup import twoup
from jobs.util.usepng   import use_png_conversion
from .conv              import conv

def pdf2png():
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    inputd  = DD.inputd
    pdf2up  = DD.pdf2up
    jobtyp  = DD.jobtyp
    img     = DD.img
    pngPRE  = DD.pngPRE
    pngUP   = DD.pngUP
    #
    #   inputd -> img
    #
    for itm in sorted(glob.glob(os.path.join(inputd, '*'))):
        bn = os.path.basename(itm)
        if os.path.splitext(itm)[1].lower()[1:] not in DD.imgext:
            prnt(f'skip handling {bn}')
            continue
        shutil.copy(itm, img)
        prnt(f'     handling {bn}')
    #
    #   img -> pngPRE
    #
    opt     = DD.frmopt
    dpi     = opt['dpi']
    qlty    = opt['qlty']
    dpidic  = { 'default'   : 200,
                '200dpi'    : 200,
                '300dpi'    : 300,
                '400dpi'    : 400 }
    dpi = dpidic[dpi]
    prnt(f'''
  frmopt {DD.frmopt}
  dpi    {dpi}
  qlty   {qlty}''')
    for itm in sorted(glob.glob(os.path.join(img, '*'))):
        ext = os.path.splitext(itm)[1].lower()
        bn  = os.path.basename(itm)
        conv(itm, bn, pngPRE, pngUP, dpi, qlty)
    #
    #   pngPRE -> pngUP
    #
    for itm in sorted(glob.glob(os.path.join(pngPRE, '*'))):
        bn    = os.path.basename(itm)
        bnBDY = os.path.splitext(bn)[0]
        if jobtyp == 'txt' and pdf2up:
            twoup(itm)
            continue
        if not use_png_conversion():
            #   usepng=False : pngPRE files are canvas only, not sent to API
            continue
        # bad-font PNGs are already in pngUP (copied in conv._conv_pdf);
        # skip here to avoid double-copy
        org = '.'.join(bn.split('.')[:-2])
        if org in DD.skipPdf:
            prnt(f'skip pngUP bad-font PNG: {bn}')
            continue
        if os.path.isfile(os.path.join(pngUP, f'{bnBDY}.pdf')):
            prnt(f'{bnBDY}.png aready in pngUP, maybe by maniacSplit')
            continue
        shutil.copy(itm, pngUP)
        prnt(f'copied to pngUP     {bn}')
    if DD.skipPdf: # if no PNG conversion DD.skipPdf == []
        lines = [f'  {f}: {sorted(DD.skipPdfEnc.get(f, set()))}'
                 for f in DD.skipPdf]
        prnt('bad font PDFs:\n' + '\n'.join(lines))
    return
