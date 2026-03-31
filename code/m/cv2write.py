#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   cv2write.py     250221  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import uuid
import os

import cv2

def cv2write(path, img, allow_overwrite = False):
    if os.path.isfile(path):
        if allow_overwrite:
            os.remove(path)
        else:
            raise Exception(f'''flle alredy exists and allow_overwrite == False
  {path}''')

    bn      = os.path.basename(path)
    ext     = os.path.splitext(path)[1]
    tmpf    = f'{uuid.uuid4()}{ext}'
    dname   = os.path.dirname(path)
    orgd    = os.getcwd()
    os.chdir(dname)
    cv2.imwrite(tmpf,img)


    os.rename(tmpf,bn)
    os.chdir(orgd)
    return
