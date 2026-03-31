#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   sorter_s.py     230411  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

from .pgmatch   import pgmatch
from .mark      import mark
from .popout    import popout
from m.prnt     import prnt

def sorter_s(docname,sobj,pdf_pg):
    for key in pdf_pg:
        pdf = key.split('|')[0]  # key = 'pdf|engine|usepng'
        fmto_list = pdf_pg[key]
        idx = 0
        while idx < len(fmto_list):
            fm, to = fmto_list[idx]
            for pg in range(fm, to + 1):
                if pgmatch(docname, pdf, pg, sobj):
                    mark(docname, key, pg, pg)
                    popout(pdf_pg, key, pg, pg)
                    # ここで、内側のループを終了し、whileループによりforループを再開
                    break
            else:
                # forループがbreakなしで完了したら次の要素へ移動
                idx += 1
