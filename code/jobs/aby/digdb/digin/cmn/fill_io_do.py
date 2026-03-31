#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   fill_io_do.py       230427  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

from m.prnt import prnt

def fill_io_do(io,do):
    if io.resubrtn == None:
        io.seq      = None
        io.node     = None
        io.txt      = None
        io.page     = None
        io.pg_top   = None
        io.pg_btm   = None
        io.top      = None
        io.btm      = None
        io.lft      = None
        io.ryt      = None
        io.otop     = None
        io.obtm     = None
        io.olft     = None
        io.oryt     = None
        top         = None
        btm         = None
        lft         = None
        ryt         = None
    else:
        [ seq ,node,txt ,page ,
          pg_top, pg_btm,
          top ,btm ,lft ,ryt  ,
          otop,obtm,olft,oryt,conf ] = io.resubrtn
        io.seq      = seq
        io.node     = node
        io.txt      = txt
        io.page     = page
        io.pg_top   = pg_top
        io.pg_btm   = pg_btm
        io.top      = top
        io.btm      = btm
        io.lft      = lft
        io.ryt      = ryt
        io.otop     = otop
        io.obtm     = obtm
        io.olft     = olft
        io.oryt     = oryt
        io.conf     = conf
    do.itm.append(io)
    do.locdic[f'TOP_{io.dl.dname}']    = io.pg_top
    do.locdic[f'BTM_{io.dl.dname}']    = io.pg_btm
    do.locdic[f'LFT_{io.dl.dname}']    = lft
    do.locdic[f'RYT_{io.dl.dname}']    = ryt
    if (    io.dl.rg != None and
            (   io.dl.rg.startswith('gk_')  or
                io.dl.rg.startswith('gm_')  )):
        do.nxtdic[f'TPN_{io.dl.dname}']    = io.pg_top
        do.nxtdic[f'BTN_{io.dl.dname}']    = io.pg_btm
    return
