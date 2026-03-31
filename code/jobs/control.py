#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   control.py      251225  cy
#   updated: 260320.093743 by cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import os

from m.prnt                 import prnt
from m.env                  import D
from .env                   import DD
from .loadxl.loadxl         import loadxl
from .mv2input.mv2input     import mv2input
from .setup_flds.setup_flds import setup_flds
from .docopy.docopy         import docopy
from .pdf2png.pdf2png       import pdf2png
from .util.svjsn.svjsn      import svjsn
from .util.drwpng           import drwpng
#from .jsn2db.jsn2db         import jsn2db
from .aby.aby               import aby

from .txtmode.jsn2txt       import jsn2txt


def control():
    loadxl()                        # parse global setting only
    if DD.jobtyp == 'frm':
        msconf = mv2input()         # parse _dd and such
        setup_flds()
        if docopy() is False:       # use lod png* or not
            pdf2png()
            svjsn()
            drwpng()
            with open(os.path.join(D.logd, 'dumpdb_ok.txt'), 'w') as f:
                f.write('')
        #
        #   CHECKPOINT (B)
        #
        #   dump.db dump.xlsx   ready
        #   pngROT pngMK pngRMK ready
        #
        aby(msconf)
    elif DD.jobtyp == 'txt':
        setup_flds()
        mv2input()
        pdf2png()                   # -> twoup -> updn
        svjsn()
        jsn2txt()
    else:
        raise Exception('PG bug')
#    finish()
    return
