#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   debugvalue.py   230610  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#


def debugvalue(do):
    io = do.itm[-1]
    val = '"gk_" of this item or avove does not exists'
    io.sqltxt   = val
    io.sqlarg   = val
    io.sqlrtn   = [(val,)]
    io.regrtn   = [(val,)]
    io.posrtn   = val
    io.resubrtn = val
    return
