#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   draw_rot.py     230224  cy
#   updated: 260322 replace use_noup_png() global with explicit use_noup param
#   updated: 260322 rename output: NOUP.png -> PNG.png (BOTH mode marking)
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import os

import cv2

from m.cv2read          import cv2read
from m.cv2write         import cv2write
from m.prnt             import prnt
from ...env             import DD
from ...util.s2l        import s2l

def draw_rot(drwlst, dir_png, dir_marked, use_noup=False):
    # drwlst key is (bare, engine)
    for (bare, engine) in drwlst:
        eng_tag = f'.{engine}' if engine else ''
        for page in drwlst[(bare, engine)]:
            longname_src = s2l(bare, page, 'png')
            if use_noup:
                longname_src = (longname_src[:-len('.png')]
                                + '.NOUP.png')
            longname_dst = (s2l(bare, page, 'png')[:-len('.png')]
                            + f'{eng_tag}.png')
            srcfn = os.path.join(dir_png,    longname_src)
            dstfn = os.path.join(dir_marked, longname_dst)
            img = cv2read(srcfn)
            elmlst = drwlst[(bare, engine)][page]
            for i in elmlst:
                [drwvar,node,tl,tr,br,bl,txt,conf] = i
                [thickness,color,cls] = drwvar
                if cls == 'line':
                    org = (tl[0], tl[1]-10)
                else:
                    org = (br[0], br[1]+20)
                cv2.line(img,tl,tr,color,thickness)
                cv2.line(img,tr,br,color,thickness)
                cv2.line(img,br,bl,color,thickness)
                cv2.line(img,bl,tl,color,thickness)
                cv2.putText(
                    img,
                    text      = node,
                    org       = org,
                    fontFace  = cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale = 0.6,
                    color     = color,
                    thickness = 1)
            cv2write(dstfn, img)
    return
