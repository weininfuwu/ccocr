#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   s2l.py      250222  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import re

from m.prnt import prnt

def s2l(short,page,typ):

    if typ not in ['png','json']:
        raise Exception(f'incorrect type "{typ}", must be "png" or "json"')

    # Strip BOTH-mode labels before regex processing
    short = short.replace(' STRAIGHT', '').replace(' from PNG', '')

    m = re.search((
        r'^(.*?)\.'                          # 0 original filename
        r'(([a-z]{2}\d{3}(\.\d{6}){3})\.)?'    # 1 job id when called azure
        r'([a-zA-Z]+)$'),short)             # 3 original file extension

    if m == None:
        raise Exception(f'regex error for "{short}"')

    [org_fn, junkA, jid, junkB, ext] = m.groups()

    page = f'{page:02}'

    if jid == None:
        long = f'{org_fn}.{ext}.{page}.{typ}'
    else:
        long = f'{org_fn}.{ext}.{jid}.{page}.{typ}'
#    prnt(f'''
#     {short} ({page})
#  -> {long}''')

    return long
