#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   runsql.py   2304007     cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import sqlparse
import re
import sys
import datetime

from m.prnt         import prnt
from .fill_locdic   import fill_locdic
from .gv            import gv

def runsql(sobj,index,pdf,pg):
    dl = sobj.defs[index]
    locdic = sobj.locdic
    sql = f'''
-- {__name__}
-- {dl.dname}
-- {datetime.datetime.now()}
SELECT seq,pdf,page,txt FROM elm 
WHERE typ  = 'line'
AND   pdf  = '{pdf}'
AND   page = '{pg}'
AND   top  > {dl.sp_blw + dl.of_blw}
AND   btm  < {dl.sp_abv + dl.of_abv}
AND   lft  > {dl.sp_rof + dl.of_rof}
AND   ryt  < {dl.sp_lof + dl.of_lof}   '''
    sql = sqlparse.format(sql,reindent=True, keyword_case='upper')
    sql = re.sub(r'^\n','',sql,flags=re.MULTILINE)
    rtn = gv.cur.execute(sql).fetchall()
    dl.matches = []
    for i in rtn:
        [seq,pdf,page,txt] = i
#        m = re.match(rf'{dl.val}',txt)
        m = re.search(rf'{dl.val}',txt)
        if m != None:
            dl.matches.append(seq)
#            if dl.dname == 'endpage':
#                print(f'pdf {pdf} page {pg} txt |{txt}| dl.val |{dl.val}|')
    if dl.alw_m == 'OK' and len(dl.matches) > 1:
        sobj.defs.pop(index)                        # 230413
        return True                                 # 230413
    if dl.matches == []:
        return False
    else:
        fill_locdic(dl,locdic)
        sobj.defs.pop(index)
        return True
