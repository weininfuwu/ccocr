#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   digin.py        230421  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import copy

from m.prnt             import prnt
from .objs        import docObj, itmObj

#from .d_top   import d_top
#from .d_blw   import d_blw

from .d_top.d_top   import d_top
from .d_blw.d_blw   import d_blw

from .nxtdic2locdic   import nxtdic2locdic
#from .marknomore  import marknomore

'''
    +++++ INPUT +++++
    docdef[docname] == input for each type of doc
                    == ddObj
    ddObj.defs      == [ dlObj, ... ]
    ddObj.child     == ddObj (of a level below), or None
    dlObj           == one definition line in _dd

    +++++ OUTPUT +++++
    dos             == [ docObj, ... ]  ## to be appended to dig[docname]
                    see digin_sub.ojbs for detail of docObj
'''

def digin(docname,docdef,pdf,fm,to,docnum,jobid,engine='',apisrc=''):
    lvl = 1
    ## ddObj == Document Definition Object == one _dd sheet
    ##          aka. lvl object
    org_ddObj   = docdef[docname]
    #
    #   top level
    #
    ddObj       = copy.deepcopy(org_ddObj)  # we use pop() to control flow
    ## docObj == Document Object == one buziness document
    do          = docObj(docname,pdf,fm,to,docnum,ddObj)  # blank docObj
    do.oid      = id(do)
    # dos == list of docObj
    dos         = d_top(ddObj,do,docname,pdf,fm,to,engine,apisrc)
    nxtdic2locdic(dos)
    #
    #   deeper level
    #
    while org_ddObj.child != None:
        lvl += 1
        org_ddObj = org_ddObj.child
        new_dos = []
        ttl = len(dos)
        for cnt,do in enumerate(dos):
            ddObj = copy.deepcopy(org_ddObj)    # will use pop() for control
            tmp_dos = d_blw(ddObj,do,docname,pdf,fm,to,engine,apisrc)
            nxtdic2locdic(tmp_dos)
            new_dos += tmp_dos
            #
            #   verbose logging
            #
            log = ((  '\n '
                    f'{docnum} {docname} lv {lvl} "{pdf}" p{fm}-{to} '
                    f'{cnt+1}/{ttl} {do.inum} kids {len(tmp_dos)} ' ))
            if len(tmp_dos) == 1:   ## no expansion happend == all items done
                itms = len(tmp_dos[0].itm)
                log += f'itms {itms}/{do.itmcnt}'
            else:
                log += f'itms -/{do.itmcnt}\n'
                tmp_ttl = len(tmp_dos)
                for tmp_cnt,tmp_do in enumerate(tmp_dos):
                    itm = tmp_do.itm[-1]
                    txt = itm.txt
                    if txt == None:
                        txt = 'None'
                    log += f'   kid {tmp_cnt+1}/{tmp_ttl} itm {len(tmp_do.itm)}/{do.itmcnt} dn {itm.dl.dname} '
                    log += f'txt "{txt}"\n'
                log = log[:-1]
#            prnt(f'{jobid} digged RG'+log)
            ## end verbose loggin
        dos = new_dos
    return dos
