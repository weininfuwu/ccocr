#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   cv2read.py      250221  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import uuid
import os
import shutil

import cv2

def cv2read(path):
    if not os.path.isfile(path):
        raise Exception(f'file not exists\n{path}')
    bn      = os.path.basename(path)
    ext     = os.path.splitext(path)[1] # ext == '.txt' and such
    tmpf    = f'{uuid.uuid4()}{ext}'
    dname   = os.path.dirname(path)
    orgd    = os.getcwd()
    os.chdir(dname)
    shutil.copy(bn,tmpf)
    rtn = cv2.imread(tmpf)
    os.remove(tmpf)
    os.chdir(orgd)
    return rtn
