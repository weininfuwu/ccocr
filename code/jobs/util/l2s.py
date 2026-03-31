#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   l2s.py      250222  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import re

from m.prnt import prnt

def l2s(lng):

    #
    #   usepng=False : hoge.pdf.STRAIGHT.json  ->  sht='hoge.pdf', pg=0(全ページ)
    #
    m = re.search(r'^(.*)\.STRAIGHT\.json$', lng)
    if m:
        return m.group(1), 0

    #
    #   usepng=False : hoge.pdf.NN.NOUP.png
    #   usepng=True  : hoge.pdf.NN.json / hoge.pdf.NN.png
    #
    m = re.search((
        r'^(.*)\.'                              # 0 original filename
        r'([a-zA-Z]+)\.'                        # 1 original file extension
        r'(([a-z]{2}\d{3}(\.\d{6}){3})\.)?'    # 2 job id when called azure
        r'(\d+)\.'                              # 4 page number
        r'(?:NOUP\.)?'                          # NOUP marker (usepng=False, optional)
        r'(json|png)$'),lng)                    # 5 json or png

    if m == None:
        raise Exception(f'regex error for "{lng}"')

    [org_fn, org_ext, junkA, jid, junkB, page, ext] = m.groups()
    if jid != None:
        sht = f'{org_fn}.{jid}.{org_ext}'
    else:
        sht = f'{org_fn}.{org_ext}'
    pg = int(page)
#    prnt(f'''
#     {lng}
#  -> {sht} ({pg})''')
    return sht,pg
