#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   pos_narrow.py  230427  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

from m.prnt                     import prnt
from .expand_doio    import expand_doio
from .hdbtm_fttop    import hdbtm_fttop

'''
-- SELECT statement in runsql.py
SELECT  seq ,node,txt ,page,
        pg_top, pg_btm,
        top ,btm ,lft ,ryt,
        otop,obtm,olft,oryt FROM elm
'''

def k2i(kwd):
    dic = { 'TOP'   : 4 ,
            'BTM'   : 5 ,
            'LFT'   : 8 ,
            'RYT'   : 9 }
    return dic[kwd]

def pos_narrow(ddObj,do,io,fm,to):
    ##
    ##   expand on gk_ item
    ##
    if type(io.dl.rg) == str and io.dl.rg.startswith('gk_'):
        doios = expand_doio(do,io)
        return doios                             ### RETURN
    ##
    ##   non gk_ item
    ##
    ## set inum
    if do.inum == None:
        do.inum = '-'
    #
    #   if already failed, no need narrowing
    #
    if io.regrtn == []:
        # io.posrtn is None by defalut
        doios = [[do,io]]
        return doios                             ### RETURN
    ###
    ###   do narrowing by position
    ###
    pri = io.dl.pos[:3]
    sec = io.dl.pos[4:]
    cnfidx = 14
    #
    #   PRIMARY key
    #
    if pri  in ['TOP','LFT']:
        tmp = sorted(io.regrtn, key = lambda x: x[k2i(pri)])
    else:
        tmp = sorted(
                io.regrtn, reverse = True,  key = lambda x: x[k2i(pri)])
    cand = []
    for i in tmp:
        if i[k2i(pri)] == tmp[0][k2i(pri)]:
            cand.append(i)
#    prnt(
#    f'{io.dl.dname}: item(s) to mach "{io.dl.pos}" of "{pri}": {len(cand)}')
    #
    #   SECONDARY key
    #
    if len(cand) > 1:
        if sec in ['TOP','LFT']:
            tmp2 = sorted(cand, key = lambda x: x[k2i(sec)])
        else:
            tmp2 = sorted(cand, reverse = True, key = lambda x: x[k2i(sec)])
        cand = []
        for i in tmp2:
            if i[k2i(sec)] == tmp2[0][k2i(sec)]:
                cand.append(i)
#        prnt(f'{io.dl.dname}: item(s) to mach "{io.dl.pos}": {len(cand)}')
    #
    #   CONFIDENCE
    #
    if len(cand) > 1:
        tmp = sorted(io.regrtn, reverse = True, key = lambda x: x[cnfidx])
        cand = []
        for i in tmp:
            if i[cnfidx] == tmp[0][cnfidx]:
                cand.append(i)
#        prnt(f'{io.dl.dname}: item(s) of MAX confidence: {len(cand)}')
    #
    #   choose idx == 0
    #
#    if len(cand) > 1:
#        prnt(f'{io.dl.dname}: 1st one chosen')
    cand = cand[0]

    ### posrtn decided

    io.posrtn = list(cand)
    io.confidence = cand[cnfidx]
    hdbtm_fttop(do,io)
    doios = [[do,io]]
    return doios
