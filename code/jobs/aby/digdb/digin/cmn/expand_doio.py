#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   expand_doio.py  230517  cy
#   updated: 260320.143721 by cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import copy

from .rmv_overwrap  import rmv_overwrap
from m.prnt                     import prnt

    #                                       #
    #   THIS CODE ONLY CALLED ON gk_ ITEM   #
    #                                       #

def expand_doio(do,io):
    doios = []  # list to return
    ###
    ###     STEP 0  overwrapp check
    ###
    if len(io.regrtn) > 1:
        rmv_overwrap(do,io)
    ###
    ###     STEP 1  build doios
    ###
    #
    #   regrtn HAS VALUE    1) set gktop, gkbtm
    #                       2) EXPAND, sort, append to doios
    #
    if len(io.regrtn) > 0:
        for cnt,regrtn in enumerate(io.regrtn):

#            if cnt == 0:
#                ndo = do
#                nio = io
#            else:
#                ndo     = copy.deepcopy(ndo)
#                ndo.oid = id(ndo)
#                nio     = copy.deepcopy(nio)
#                for ndoitm in ndo.itm:
#                    ndoitm.isclone = True

            # updated: 260320.144333 by cy (claud.ai)
            if cnt == 0:
                ndo = do
                nio = io
            else:
                ndo     = copy.deepcopy(do)   # ndo ではなく常に元の do から
                ndo.oid = id(ndo)
                nio     = copy.deepcopy(io)   # nio ではなく常に元の io から
                for ndoitm in ndo.itm:
                    ndoitm.isclone = True

            nio.posrtn  = list(regrtn)
            ndo.gktop   = nio.posrtn[4]
            ndo.gkbtm   = nio.posrtn[5]
            #             pg_top        lft
            doios.append([ndo,nio])
    #
    #   regrtn is blank
    #
    else:
        doios.append([do,io])   # io.posrtn is None by derault
    ###
    ###     STEP 2  set i.inum and i.refi
    ###
    for cnt,di in enumerate(doios):
        [d,i] = di
        #
        #   level 1     level only have gk_ : None -> '01'
        #               else                : '-'  -> '01'
        #
        if d.inum == None or d.inum == '-':
            d.inum = f'{cnt+1:02}'
            ###
            ### 230611
            ### refi mayby in no-use, better consider remove
            ###
            i.refi = '01'
            for ii in d.itm:
                ii.refi = '01'
        #
        #   level 2 or deeper   : extend inum string
        #
        elif type(d.inum) == str:
            d.inum = f'{d.inum}_{cnt+1:02}'
            i.refi = f'{d.inum}_01'
            for ii in d.itm:
    #            if ii.refi == None:
                ii.refi = f'{d.inum}_01'
    return doios
