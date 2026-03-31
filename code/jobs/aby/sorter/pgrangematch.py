#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   pgrangematch.py     230411  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import pprint

from .pgmatch   import pgmatch
from .mark      import mark
from .popout    import popout
from m.prnt import prnt

def pp(x):
    return pprint.pformat(x, indent=2)

def pgrangematch(docname,pdf,fmto,sobj,pdf_pg,key=None):
    if key is None: key = pdf  # fallback for single-engine
    prnt(f'start "{docname}" "{pdf}" {fmto}')
    [rng_bgn,rng_end] = fmto
    pg = rng_bgn
    lookfor = 'hd'  # 'hd' or 'ft'
    while True:
        #
        #   chk if has header
        #
        if lookfor == 'hd':
            sobj.defs = sobj.hd
            if pgmatch(docname,pdf,pg,sobj):
                fm = pg
                prnt(f'found hd\n  "{pdf}" "{docname}" pg{pg}')
                #
                #   chk if has footer on the same page
                #
                sobj.defs = sobj.ft
                if pgmatch(docname,pdf,pg,sobj):
                    mark(docname,key,pg,pg)
                    popout(pdf_pg,key,pg,pg)
                    prnt((f'found hd,ft\n  "{pdf}" "{docname}" pg{pg}\n  '
                          f'mark+popout {pg}'))
                else:
#                    popout(pdf_pg,pdf,pg,pg)
                    lookfor = 'ft'
                    prnt((f'found no ft on pg{pg} go next page to find ft\n  '
                          f'NOT popout {pg}'))
            else:
#                popout(pdf_pg,pdf,pg,pg)
                prnt((f'go next page to find hd\n  '
                      f'NOT popout {pg}'))
        #
        #   chk if has foorter or middle
        #
        else:   # lookfor == 'ft'
            sobj.defs = sobj.ft
            if pgmatch(docname,pdf,pg,sobj):
                mark(docname,key,fm,pg)
                popout(pdf_pg,key,fm,pg)
                lookfor = 'hd'
                prnt((f'found ft\n  "{pdf}" "{docname}" pg{pg}\n  '
                      f'mark+popout {fm}-{pg}'))
            elif len(sobj.md) > 0:
                sobj.defs = sobj.md
                if pgmatch(docname,pdf,pg,sobj):
                    prnt(f'found md\n  "{pdf}" "{docname}" pg{pg}')
                else:
                    lookfor = 'hd'
#                    popout(pdf_pg,pdf,fm,pg)
                    prnt(('go next page to find new hd\n  '
                         f'NOT popout {fm}-{pg}'))
            else:   # no 'md' entry in sorter sheet
                lookfor = 'hd'
#                popout(pdf_pg,pdf,fm,pg)
                prnt((f'pg{pg} is not ft and no md entry in sorter, '
                       'go next page to find new hd\n  '
                      f'NOT popout {fm}-{pg}'))
        pg += 1
        if pg > rng_end:
            prnt('no more page, finish loop')
            break
    prnt(f'finish\n  "{docname}" "{pdf}" {fmto}\n{pp(pdf_pg)}')
