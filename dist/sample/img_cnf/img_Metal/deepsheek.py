#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   deepsheek.py
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import fitz
import os
import glob

pngPRE = 'pngPRE'

#for itm in sorted(glob.glob(os.path.join(img,'*.pdf'))):
for itm in sorted(glob.glob('mtl_mitMAT*.pdf')):
    bn = os.path.basename(itm).replace('.pdf', '')
    print(f'splitting into png     {bn}')
    doc = fitz.open(itm)
    for page_num in range(len(doc)):
        page = doc[page_num]
        # 高解像度でレンダリング
#        zoom = dpi / 72  # 72 DPIを基準
        zoom = 200 / 72
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        
        tmp = f'{bn}.{page_num+1:02}.png'
        tmp = os.path.join(pngPRE, tmp)
        pix.save(tmp)
        print(f'saved at pngPRE\n  {tmp}')
    doc.close()
