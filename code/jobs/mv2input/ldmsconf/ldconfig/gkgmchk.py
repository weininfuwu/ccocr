#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   gkgmchk.py  230320  cy
#   ToDo        nks_nonaka　エラーメール追加
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import re

from m.prnt             import prnt

#from m.errconfig            import ConfigErr

def gkgmchk(docdef,attrs):
    gkset = set()
    for i in attrs:
        ## 230516   allow None
        if i == None:
            continue
        ##
        ## multi gk is NG
        ##
        if i.startswith('gk') and attrs.count(i) > 1:
            raise Exception(f'{docdef} has multi "{i}"')
        ##
        ## gk naming check
        ##
        if  i.startswith('gk_'):
            m = re.match(r'^gk(_[^_]+)*$',i)
            if m == None:
                raise Exception(f'rg naming error in {docdef} "{i}"')
        ##
        ## find gm with no gk
        ##
        m = re.match(r'^gm_(.*)',i)
        if m != None:
            if not f'gk_{m.groups()[0]}' in attrs:
                raise Exception(f'{docdef} {i} has NO matching gk')
        ##
        ## build gkset for chk (A) (B)
        ##
        if  i.startswith('gk_'):
            gkset.add(i)
    ##
    ## (A) chk if gk has papa
    ##
    for i in attrs:
        ## 230516   allow None
        if i == None:
            continue
        if not i.startswith('gk_'):
            continue
        papa = i.split('_')
        if len(papa) < 3:
            continue
        papa = '_'.join(papa[:-1])
        if papa not in gkset:
            raise Exception(f'no papa gk in {docdef} "{papa}"')
    ##
    ## (B) chk if multiple rg of same depth
    ##
    gklst = [ i.split('_') for i in gkset ]
    gkdic = {}
    for i in gklst:
        if len(i) in gkdic and gkdic[len(i)] != i:
            raise Exception((  f'multi RG in {docdef}: '
                    f'''"{'_'.join(i)}" "{'_'.join(gkdic[len(i)])}"'''))
        gkdic[len(i)] = i
    return
