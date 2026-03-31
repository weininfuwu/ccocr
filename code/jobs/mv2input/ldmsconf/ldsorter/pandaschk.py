#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   pandaschk.py    230315  cy
#   ToDo            nks_nonaka  エラーメール pandas 参照エラー
#
#   updated: 260319.162720 by cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import pandas as pd
import numpy as np

from m.prnt         import prnt
from ..pdchk.fill             import fill
from ..pdchk.remove_nokids    import remove_nokids
from ..pdchk.draw_loop        import draw_loop

def pandaschk(sorter):
    for docname in sorter:
        obj = sorter[docname]
        if obj.type == 'single':
            chk(obj.defs, f'{docname}_single')
        elif obj.type == 'multi':
            chk(obj.hd, f'{docname}_multi_hd')  #
            chk(obj.md, f'{docname}_multi_md')  #   REFERENCE CANNOT ACROSS!
            chk(obj.ft, f'{docname}_multi_ft')  #
        else:
            raise Exception('program bug')
    return

def chk(lst,title):
    dnames = [ o.dname for o in lst ]
    board = pd.DataFrame(
        data = np.zeros( (len(dnames),len(dnames)), dtype=int ),
        index = [ f'p_{i}' for i in dnames ],       ## row
        columns = [ f'c_{i}' for i in dnames ]  )   ## clm
#    print(f'==== blank board for {title} ====')
#    print(board)
#    print(f'==== end blank board for {title} ====')

    fill(lst,board,title)
#    print(f'==== filled board for {title} ====')
#    print(board)
#    print(f'==== end filled board for {title} ====')

    if not remove_nokids(board):
#        print('=++++++++ NG ++++++++')
#        print(board)
        chain = draw_loop(board)
        if chain != []:
            raise Exception(f'ERROR: {title} has reference loop "{chain}"')
    return
