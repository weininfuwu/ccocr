#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   d_blw.py        230609  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

from m.prnt             import prnt
from ..objs                  import docObj, itmObj
from .sp_has_str  import sp_has_str
from .runsql      import runsql
from .debugvalue  import debugvalue

from ..cmn.pos_narrow        import pos_narrow
from ..cmn.regexchk          import regexchk
from ..cmn.resub             import resub
from ..cmn.fill_io_do        import fill_io_do

def d_blw(ddObj,do,docname,pdf,fm,to,engine='',apisrc=''):
    idx = 0
    while len(ddObj.defs) > 0:
        if len(ddObj.defs) == 1:
            do.lastins = True
        io = itmObj(ddObj.defs[idx])    ## blank itmObj
        #
        #   do.nomore == True
        #
        if do.nomore == True:
            io.p_nopapa = True
            fill_io_do(io,do)
            debugvalue(do)
            ddObj.defs.pop(idx)                 # POP !!!
            if len(ddObj.defs) == 0:
                dos = [ do ]
                return dos
            idx = 0
            continue
        # gk_* should be at last
        if (    type(io.dl.rg) == str       and
                io.dl.rg.startswith('gk_')  and
                len(ddObj.defs) > 1         ):
            idx += 1
            continue
        # lookup locdic. if failer then continue
        if sp_has_str(do,io,fm,to):
            idx += 1    # skip orphan
            continue    # pandas check should gurantee this control
        runsql(docname,pdf,fm,to,do,io,engine,apisrc)
        regexchk(do,io)
        doios = pos_narrow(ddObj,do,io,fm,to)
        #
        # expansion may happen at pos_narrow_sub.expand_doio
        #
        # if NOT gk_,  doios == [[do,io]]
        # if gk_,      doios == [[do,io],...]
        #
        for doio in doios:
            [xdo,xio] = doio
            resub(xio)
            fill_io_do(xio,xdo)
        dos = [i[0] for i in doios]
        ddObj.defs.pop(idx)                 # POP !!!
        idx = 0
    return dos
