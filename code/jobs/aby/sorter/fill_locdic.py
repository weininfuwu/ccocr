#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   fill_locdic.py      2304007 cy
#   ToDo                nks_nonaka  エラーメール sorter複数
#
#--------1---------2---------3---------4---------5---------6---------7--------#

from m.prnt import prnt
from .gv    import gv

def fill_locdic(dl,locdic):

#     prnt(f'DEBUG dl {dl}')
#     prnt(f'DEBUG 2 dl.__dict__ {dl.__dict__}')
#     input('hit me a key')
#     quit()
# 
# 
# 
#     if len(dl.matches) != 1:
#         prnt('''
# 
# 
#     とにかくエラーにする（メール出す）      ナカシャ
# 
#         ''')
#         raise Exception('added 250224 cy')
# #        quit()

    [top,btm,lft,ryt] = gv.cur.execute(
        f'SELECT top,btm,lft,ryt FROM elm WHERE seq = {dl.matches[0]}'
        ).fetchone()
    locdic[f'TOP_{dl.dname}'] = top
    locdic[f'BTM_{dl.dname}'] = btm
    locdic[f'LFT_{dl.dname}'] = lft
    locdic[f'RYT_{dl.dname}'] = ryt
    return
