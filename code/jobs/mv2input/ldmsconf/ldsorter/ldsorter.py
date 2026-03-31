#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   ldsorter.py     220630  cy
#   updated: 260319.162341 by cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import os

from m.prnt             import prnt
from m.env              import D
from jobs.env           import DD
from .loadxl.loadxl     import loadxl
from .lst2obj           import lst2obj
from .pandaschk         import pandaschk

#def ldsorter(mscnf):
def ldsorter():
    mscnf       = os.path.join(DD.inputd,os.path.basename(D.fpath))
    DD.mscnf    = mscnf
    ##
    ##  (1) excel to dict
    ##
    ##  sorter = {  docname : [ [assem, dname, ... ],
    ##              ... , }
    ##
    sorter = loadxl(mscnf)
    ##
    ##  (2) after lst2obj()
    ##
    ##      sorter = { docanme : sobj, ... }
    ##
    ##      sobj.type == single/multi
    ##
    ##      in case sobj.type == single;
    ##          sobj.defs = [ defobj,defobj,... ]
    ##
    ##      in case ojb.typ == multi;
    ##          sobj.hd = [ defobj,defobj,... ]
    ##          sobj.md = [ defobj,defobj,... ]
    ##          sobj.ft = [ defobj,defobj,... ]
    ##
    ##      defobj.dname    = xxx
    ##      defobj.sp_blw
    ##      defobj.of_blw
    ##      defobj.sp_abv
    ##      defobj.of_abv
    ##      defobj.sp_rof
    ##      defobj.of_rof
    ##      defobj.sp_lof
    ##      defobj.of_lof
    ##      defobj.val
    ##      defobj.assem
    ##
    lst2obj(sorter)
    ##
    ##  (3) pandas check
    ##
    pandaschk(sorter)
    prnt('sorter parsed')
    return sorter
