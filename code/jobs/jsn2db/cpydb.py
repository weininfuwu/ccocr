#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   cpydb.py    250225  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import glob
import os
import re
import shutil
import sqlite3

from m.env  import D
from ..env  import DD
from m.prnt import prnt

def cpyitm(lastd):
    tgt = D.logd
    src = os.path.normpath(os.path.join(D.logd,'..',lastd))
    prnt(f'copy items\n    {src}\n  ->{tgt}')
    shutil.copytree(    os.path.join(src,'pngROT')  ,
                        os.path.join(tgt,'pngROT')  )
    shutil.copytree(    os.path.join(src,'pngRMK')  ,
                        os.path.join(tgt,'pngRMK')  )
    shutil.copytree(    os.path.join(src,'pngMK')   ,
                        os.path.join(tgt,'pngMK')   )
    if os.path.isdir(os.path.join(src,'spic')):
        shutil.copytree(    os.path.join(src,'spic')   ,
                            os.path.join(tgt,'spic')   )

#    if os.path.isdir(os.path.join(src,'IGNORED')):
#        shutil.copytree(    os.path.join(src,'IGNORED') ,
#                            os.path.join(tgt,'IGNORED') )

    shutil.copy(os.path.join(src,f'{lastd}.dump.xlsx')  ,
                os.path.join(tgt,f'{D.jobid}.dump.xlsx' ))
    shutil.copy(os.path.join(src,f'{lastd}.dump.db')    ,
                os.path.join(tgt,f'{D.jobid}.dump.db'   ))
    DD.pngROT   = os.path.join(tgt,'pngROT')
    DD.pngRMK   = os.path.join(tgt,'pngRMK')
    DD.pngMK    = os.path.join(tgt,'pngMK')
    DD.dbf      = os.path.join(tgt,f'{D.jobid}.dump.db')
    DD.dumpf    = os.path.join(tgt,f'{D.jobid}.dump.xlsx')
    #
    #   delete sorter table as it will be created based on msconfig
    #
    con = sqlite3.connect(DD.dbf)
    cur = con.cursor()
    cur.execute('DROP TABLE sorter')

    cur.execute('DROP TABLE IF EXISTS page')

    con.commit()
    con.close()
    prnt(f'dropped sorter table')
    return

def cpydb():
    prnt('started')
    #
    #   pickup current list of jsn and png
    #
    png = set()
    jsn = set()
    for itm in os.listdir(os.path.join(D.logd,'input','jsn')):
        jsn.add(itm)
    for itm in os.listdir(os.path.join(D.logd,'input','png')):
        png.add(itm)
    #
    #   walk through prev logdirs (lastd)
    #
    lastd = []
    logbase = os.path.normpath(os.path.join(D.logd,'..'))
    for itm in reversed(glob.glob(os.path.join(logbase,'*'))):
        bn = os.path.basename(itm)
        if os.path.isfile(itm):
            continue
        if not os.path.isfile(os.path.join(itm,'dumpdb_ok.txt')):
            prnt(f'skip to use as no OK file {bn}')
            continue
        m = re.search(r'^[a-z]{2}\d{3}(\.\d{6}){3}$',bn)
        if m == None:
            prnt(f'skip to use by dirname {bn}')
            continue
        lastd.append(itm)
    for itm in lastd:
        if not os.path.isdir(os.path.join(itm,'input','jsn')):
            continue
        if not os.path.isdir(os.path.join(itm,'input','png')):
            continue
        lastjsn = set()
        lastpng = set()
        for i in os.listdir(os.path.join(itm,'input','jsn')):
            lastjsn.add(i)
        for i in os.listdir(os.path.join(itm,'input','png')):
            lastpng.add(i)
        #
        #   go copy if jsn and png are the same
        #
        if jsn == lastjsn and png == lastpng:
            lastd = os.path.basename(itm)
            prnt(f'checking result of {lastd}')
            if (
                os.path.isdir(os.path.join(itm,'pngROT'))               and
                os.path.isdir(os.path.join(itm,'pngRMK'))               and
                os.path.isdir(os.path.join(itm,'pngMK'))                and
                os.path.isfile(os.path.join(itm,f'{lastd}.dump.xlsx'))  and
                os.path.isfile(os.path.join(itm,f'{lastd}.dump.db'))    ):
                prnt(f'{lastd} OK to copy')
                cpyitm(lastd)
                prnt('finished')
                return True
    return False
