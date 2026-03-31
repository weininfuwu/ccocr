#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   regexchk.py     230427  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import re
from m.prnt import prnt

def regexchk(do,io):
    for i in io.sqlrtn:
        [ seq ,node,txt ,page ,
          pg_top, pg_btm,
          top ,btm ,lft ,ryt,
          otop,obtm,olft,oryt,conf ] = i # except top, ALMOST ALL JUNK
#          otop,obtm,olft,oryt ] = i # except top, ALMOST ALL JUNK
        m = re.search(rf'{io.dl.reg}',txt)
        if m != None:
            ## handle grptgt ('tgt' in _dd)
            if len(m.groups()) > io.dl.grptgt:
                i = list(i)
                i[2] = m.groups()[io.dl.grptgt]
                i = tuple(i)
            elif io.dl.grptgt > 0:
                prnt(f'''

    _dd ERR: {io.dl.dname} "tgt" TOO LARGE, SETTING IGNORED
    len(m.groups()) {len(m.groups())}
    io.dl.grptgt    {io.dl.grptgt}
''')
            io.regrtn.append(i)
    if len(io.regrtn) == 0 and len(io.sqlrtn) > 0:
#        prnt(f'''
#    {do.docname} {io.dl.dname}: hit nothing out of {len(io.sqlrtn)}''')
        if type(io.dl.rg) == str and io.dl.rg.startswith('gk_'):
            do.nomore = True
#            prnt(f'''
#    {do.docname} {io.dl.dname}: {io.dl.rg} no value: do.nomore = True''')
    return
