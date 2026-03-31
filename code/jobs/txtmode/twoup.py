#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   twoup.py    250218  cy
#   updated: 260320.111540 by cy
#   updated: 260324.074856 by cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import os
import re
import shutil

import cv2
import numpy as np
import skimage.io

from m.prnt                     import prnt
from m.env                      import D
from jobs.env                   import DD
from jobs.util.svjsn.updn_cv    import updn_cv  # TEMP 260324.075005 by cy

class L:
    itm = None
    bn  = None

def chk_direction():
    #
    #   check angle of the 1st page of doc if 2UP mode
    #   (OCR only 1 pic)
    #
    res = updn(L.itm)
    angl = res.json()["analyzeResult"]["readResults"][0]["angle"]
    idx = np.abs(np.asarray(DD.angls) - angl).argmin()
    angl2 = DD.angls[idx]
    angl2 = 180 if angl2 == -180 else angl2
    return angl2

def twoup(itm):
    L.itm = itm
    twoupdic = DD.twoupdic
    bn = os.path.basename(itm)
    L.bn = bn
#    prnt(f'bn {bn}')
    m = re.search(r'^(.*)\.(\d+)\.png$',bn)
    if m == None:
        raise Exception(f'regex error for {itm}')
    [key,num] = m.groups()
#    prnt(f'{key} {num}')
    # setdefault
    if key not in twoupdic:
        angle = chk_direction()
        prnt(f'key {key} angle {angle}')
        twoupdic[key] = angle
    angle = twoupdic[key]
    cwd = os.getcwd()
    os.chdir(DD.pngPRE)
    tmpf = f'__tmp0_{D.jobid}.png'
    tmp1 = f'__tmp1_{D.jobid}.png'
    tmp2 = f'__tmp2_{D.jobid}.png'
    shutil.copy(bn,tmpf)
    img = cv2.imread(tmpf)
    #
    #   rotate 1
    #
    if DD.horiz:
        if angle == 0:
            prnt(f'rot CLOCKWISE   {bn}')
            cv2.imwrite(tmpf,cv2.rotate(img,cv2.ROTATE_90_CLOCKWISE))
        elif angle == -90:
            prnt(f'rot UPSIDE DOWN {bn}')
            cv2.imwrite(tmpf,cv2.rotate(img,cv2.ROTATE_180))
        elif angle == 180:
            prnt(f'rot C_CLOCKWISE {bn}')
            cv2.imwrite(tmpf,cv2.rotate(img,cv2.ROTATE_90_COUNTERCLOCKWISE))
    else:
        if angle == 90:
            prnt(f'rot C_CLOCKWISE {bn}')
            cv2.imwrite(tmpf,cv2.rotate(img,cv2.ROTATE_90_COUNTERCLOCKWISE))
        elif angle == -90:
            prnt(f'rot CLOCKWISE   {bn}')
            cv2.imwrite(tmpf,cv2.rotate(img,cv2.ROTATE_90_CLOCKWISE))
        elif angle == 180:
            prnt(f'rot UPSIDE DOWN {bn}')
            cv2.imwrite(tmpf,cv2.rotate(img,cv2.ROTATE_180))
    #
    #   split upper / lower
    #
    prnt(f'splitting png   {bn}')
    img = skimage.io.imread(tmpf)
    p1,p2 = np.array_split(img,2,0) # CAN SPLIT ONLY UPPER/LOWER (HORIZ)
    #
    #   rotate 2
    #
    if DD.horiz:
        prnt(f'rot C_CLOCKWISE {bn}')
        img = skimage.io.imread(tmpf)
        cv2.imwrite(tmp1,
                cv2.rotate(p1,cv2.ROTATE_90_COUNTERCLOCKWISE))
        cv2.imwrite(tmp2,
                cv2.rotate(p2,cv2.ROTATE_90_COUNTERCLOCKWISE))
    else:
        cv2.imwrite(tmp1,p1)
        cv2.imwrite(tmp2,p2)
    num1 = f'{int(num) * 2 - 1:02}'
    num2 = f'{int(num) * 2:02}'
    #
    #   move to pngUP
    #
    shutil.copy(tmp1,os.path.join(DD.pngUP,f'{key}.{num1}.png'))
    shutil.copy(tmp2,os.path.join(DD.pngUP,f'{key}.{num2}.png'))
    os.chdir(cwd)
    return
