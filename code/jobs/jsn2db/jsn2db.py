#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   jsn2db.py       250225  cy
#
#   0) if nor previous result, do below
#   1) check json
#   2) make elment db and dump excel
#   3) rotate png and mark
#
#--------1---------2---------3---------4---------5---------6---------7--------#


from m.prnt             import prnt
from ..env              import DD
from .cpydb             import cpydb
from .chkjsn.chkjsn     import chkjsn
from .markpng.markpng   import markpng
from .writedb           import writedb
from .writexl           import writexl


def jsn2db():
#    prnt('started')
#    if DD.jobtyp == 'cnf' and cpydb():
#        return
    elmlst  = chkjsn()
    #
    #   CHECKPOINT (2)
    #
    #   NO CHANGE in log folder except log.txt
    #
    prnt('''

    CHECK (2): chkjsn() finished
    1) should NO CHANG in jsn/png folders

    BACKUP log folder

    to start markpng()
    hit a key to go on ...
            ''')
    input('ok? ')

    dbsrc   = markpng(elmlst)
    #
    #   CHECKPOINT (5)
    #
    #   pntMK pngRMK asf:
    #       hoge.ext.NN.NOUP.png    exists & MARKED
    #       hoge.ext.NN.png         NOT EXISTS
    #
    prnt('''

    CHECK (5): back at jsn2db() from markpng()
    1) pntMK pngRMK as flws;
            hoge.ext.NN.NOUP.png    exists & MARKED
            hoge.ext.NN.png         SHOULD EXISTS BUT NOT

    BACKUP log folder

    to start writedb()
    hit a key to go on ...
            ''')
    input('ok? ')

    writedb(dbsrc)
    writexl()
    return
