#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   blnkpng.py  230222  cy
#   updated: 260322.085340 by cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import glob
import os

import cv2
import numpy as np

from m.cv2read          import cv2read
from m.cv2write         import cv2write
from m.prnt             import prnt
from jobs.env           import DD
from jobs.util.l2s      import l2s

def blnkpng(pdfs,dir_orgpng,dir_rotpng):
    pngsize = {}

    for png in sorted(glob.glob(os.path.join(dir_orgpng,'*png'))):
        org_img = cv2read(png)
        org_h, org_w = org_img.shape[:2]    ## height = Y, width = X
        lngname = os.path.basename(png)

        [shtname,pgnum] = l2s(lngname)

        rot_png = os.path.join(DD.pngROT,lngname)

        #
        #   blnkpng only receives png-mode entries (straight is excluded upstream).
        #   if shtname is missing from pdfs, it means no OCR result was produced
        #   for this png (blank page or processing error).
        #
        if shtname not in pdfs:
            raise Exception(f'''

    DYING MESSAGE:
    "{shtname}" has no entry in pdfs.
    This png was not matched by any OCR result.
    (straight-mode files should never reach blnkpng -- check markpng.py)

''')
        if pgnum not in pdfs[shtname]:
            raise Exception(f'''

    DYING MESSAGE:
    "{shtname}" p{pgnum} seems to HAS NO TEXT and CANNOT PROCEED.
    mailtain database mannually.

''')
        pdfs[shtname][pgnum]['oh'] = org_h
        pdfs[shtname][pgnum]['ow'] = org_w
        angl = pdfs[shtname][pgnum]['angl']
        rad = angl/180.0*np.pi
        rot_w = int(np.round(
                        org_h * np.absolute(np.sin(rad)) +
                        org_w * np.absolute(np.cos(rad)) ))
        rot_h = int(np.round(
                        org_h * np.absolute(np.cos(rad)) +
                        org_w * np.absolute(np.sin(rad)) ))
        rot_size=(rot_w,rot_h)
        center = (org_w/2,org_h/2)
        scale = 1.0
        rot_mat = cv2.getRotationMatrix2D(center, angl, scale)
        affine_mat = rot_mat.copy()
        affine_mat[0][2] = affine_mat[0][2] - org_w/2 + rot_w/2
        affine_mat[1][2] = affine_mat[1][2] - org_h/2 + rot_h/2
        rot_img = cv2.warpAffine(
            org_img, affine_mat, rot_size, flags=cv2.INTER_CUBIC)
        cv2write(rot_png,rot_img)
        rot_img = cv2read(rot_png)
        rot_h,rot_w = rot_img.shape[:2]
        pdfs[shtname][pgnum]['rh'] = rot_h
        pdfs[shtname][pgnum]['rw'] = rot_w
    return
