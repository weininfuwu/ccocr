#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   pchk.py     230330  cy
#   ToDo        nks_nonaka  エラーメール 参照がループ
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import pandas as pd
import numpy as np

from m.prnt                     import prnt
from ..pdchk.fill             import fill
from ..pdchk.remove_nokids    import remove_nokids
from ..pdchk.draw_loop        import draw_loop

def pchk(docdef):
    for docname in docdef:
        lvl = docdef[docname]
        lvlcnt = 0
        family = []
        while lvl != None:
            lvlcnt += 1
            for dl in lvl.defs:
                family.append(dl)

            board = pd.DataFrame(
                data = np.zeros((len(family),len(family)),dtype=int),
                index = [ f'p_{i.dname}' for i in family ],
                columns = [ f'c_{i.dname}' for i in family ] )

#            print(f'==== blank board for {docname} {lvlcnt} ====')
#            print(board)
#            print(f'==== END blank board for {docname} {lvlcnt} ====')


            fill(family,board,docname)
#            print(f'==== filled board for {docname} {lvlcnt} ====')
#            print(board)
#            print(f'==== END filled board for {docname} {lvlcnt} ====')


            if not remove_nokids(board):
                chain = draw_loop(board)
                if chain != []:
                    raise Exception(f'ERROR: {docname} has reference loop "{chain}"')
            lvl = lvl.child
    return

