#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   aby.py  250224  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import json
import os
import subprocess

import openpyxl

from m.prnt         import prnt
from m.env          import D
from ..env          import DD
#from .sorter      import sorter
from .sorter.sorter import sorter
from .oos           import oos
#from .digdb         import digdb
from .digdb.digdb   import digdb
from .writexl_dbg   import writexl_dbg
from .writexl_e     import writexl_e
from .writexl_np    import writexl_np
from .use_web.btns  import btns
from .use_web.tbls  import tbls
from .flsk_xl       import flsk_xl

def aby(msconf):
    srtr    = msconf.sorter
    docdef  = msconf.docdef
    sorter(srtr)
    oos()
    dig = digdb(docdef)
    writexl_dbg(dig)
    if DD.use_spic:
        if DD.use_macro:
            writexl_e(dig)
        if DD.use_web:
            htmlsrc = btns(dig)
            tbls(htmlsrc)
    else:
        writexl_np(dig)
    flsk_xl()
    return
