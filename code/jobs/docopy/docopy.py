#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   docopy.py       250325  cy
#   updated: 260319.174151 by cy
#
#   copy png* from old log file if matches condition.
#   useful for TRY AND ERROR on making msconfig
#   THEREFORE, pngPRE is not copied and become BLANK
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import os
import shutil
import sqlite3

from m.env      import D
from m.prnt     import prnt
from jobs.env   import DD
from .cancopy   import cancopy

def docopy():

    if not cancopy():
        prnt('no old log can be used')
        return False

    src     = DD.cpysrc                 # log folder of copy source
    srcid   = os.path.basename(src)     # jobid of copy source
    dst     = D.logd
    dstid   = D.jobid
    prnt(f'using result of {os.path.basename(src)}')

    src_pngUP   = os.path.join(src,'pngUP')
    dst_pngUP   = os.path.join(dst,'pngUP')
    src_pngROT  = os.path.join(src,'pngROT')
    dst_pngROT  = os.path.join(dst,'pngROT')
    src_pngMK   = os.path.join(src,'pngMK')
    dst_pngMK   = os.path.join(dst,'pngMK')
    src_pngRMK  = os.path.join(src,'pngRMK')
    dst_pngRMK  = os.path.join(dst,'pngRMK')

    src_spic    = os.path.join(src,'flsk','static','spic')
    dst_spic    = os.path.join(dst,'flsk','static','spic')

    src_dumpxl  = os.path.join(src,f'{srcid}.dump.xlsx')
    dst_dumpxl  = os.path.join(dst,f'{dstid}.dump.xlsx')
    src_dumpdb  = os.path.join(src,f'{srcid}.dump.db')
    dst_dumpdb  = os.path.join(dst,f'{dstid}.dump.db')
    DD.dbf      = dst_dumpdb
    DD.pngROT   = dst_pngROT

    prnt('copying fld "pngUP"')
    shutil.copytree(src_pngUP,dst_pngUP, dirs_exist_ok = True)
    prnt('copying fld "pngROT"')
    shutil.copytree(src_pngROT,dst_pngROT, dirs_exist_ok = True)
    prnt('copying fld "pngMK"')
    shutil.copytree(src_pngMK,dst_pngMK, dirs_exist_ok = True)
    prnt('copying fld "pngRMK"')
    shutil.copytree(src_pngRMK,dst_pngRMK, dirs_exist_ok = True)
    DD.pngRMK = dst_pngRMK
    prnt('copying fld "spic"')
    shutil.copytree(src_spic,dst_spic, dirs_exist_ok = True)
    prnt('copying file "*.dump.xlsx"')
    shutil.copy(src_dumpxl,dst_dumpxl)
    prnt('copying file "*.dump.db"')
    shutil.copy(src_dumpdb,dst_dumpdb)

    con = sqlite3.connect(dst_dumpdb)
    cur = con.cursor()
    cur.execute('DROP TABLE IF EXISTS sorter')
    con.commit()
    con.close()
    prnt('sorter table dropped')
    with open(os.path.join(src,f'API_result_from_{srcid}.txt'),'w',encoding='utf-8') as f:
        f.write(f'by {__file__}')

    src_skipMsg = os.path.join(src,'NEED_PREPROCESS.txt')
    dst_skipMsg = os.path.join(dst,'NEED_PREPROCESS.txt')
    thisOutd    = os.path.join(DD.outd,D.jobid)
    if os.path.isfile(src_skipMsg):
        os.makedirs(thisOutd, exist_ok=True)
        shutil.copy(src_skipMsg,thisOutd)
        shutil.copy(src_skipMsg,dst_skipMsg)
        prnt('saved skip message at outdir')
    else:
        prnt('not found skip message to copy')

    return True
