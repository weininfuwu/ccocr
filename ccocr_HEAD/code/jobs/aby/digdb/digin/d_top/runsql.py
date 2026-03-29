#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   runsql.py       230427  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

#from m.aby_sub.digdb_sub.gv import gv
from ...gv  import gv
from m.prnt import prnt

def runsql(docname,pdf,fm,to,do,io,engine='',apisrc=''):
    dl = io.dl
    u_blw = ''
    u_pgt = ''
    u_hdb = ''
    u_abv = ''
    u_pgb = ''
    u_ftt = ''
    use = '[USE THIS]'
    ## TOP
    if (    io.dl.rg != None            and
            io.dl.rg.startswith('gk_')  and
            type(dl.sp_blw) == int      and
            type(do.hdbtm) == int       ):
        sp_blw = max(dl.sp_blw,do.hdbtm)
        u_blw = use
        u_hdb = use
    else:   # dl.sp_blw either int or None
        sp_blw = dl.sp_blw
        u_blw = use
    ## BOTTOM
    if (    io.dl.rg != None            and
            io.dl.rg.startswith('gk_')  and
            type(dl.sp_abv) == int      and
            type(do.fttop) == int       ):
        sp_abv = min(dl.sp_abv,do.fttop)
        u_abv = use
        u_ftt = use
    else:   # dl.sp_abv either int or None
        sp_abv = dl.sp_abv
        u_abv = use
    io.sqltxt = f'''
/*  pdf     : {pdf} p{fm}-{to} doc# {do.docnum}
    docname : {docname}
    level 1, dname {dl.dname}, rg {dl.rg}
    sp_blw of_blw : {dl.sp_blw} {dl.of_blw} {u_blw}
    do.pgtop      : {do.pgtop} {u_pgt}
    do.hdbtm      : {do.hdbtm} {u_hdb}
    sp_abv of_abv : {dl.sp_abv} {dl.of_abv} {u_abv}
    do.pgbtm      : {do.pgbtm} {u_pgb}
    do.fttop      : {do.fttop} {u_ftt}
    lft     : {dl.sp_rof} + {dl.of_rof}
    ryt     : {dl.sp_lof} + {dl.of_lof}
    typ     : {dl.dtyp}    */
SELECT  seq ,node,txt ,page, pg_top, pg_btm,
        top ,btm ,lft ,ryt, otop,obtm,olft,oryt,conf FROM elm
WHERE pdf = :pdf
AND engine = :engine
AND apisrc = :apisrc
AND pg_top >= :top
AND pg_btm <= :btm
AND lft >= :lft
AND ryt <= :ryt
AND typ =  :typ
ORDER BY pg_top, lft'''
    io.sqltxt = io.sqltxt[1:]
    try:
        io.sqlarg = {   'pdf'       : pdf                   ,
                        'engine'    : engine                ,
                        'apisrc'    : apisrc                ,
                        'top'       : sp_blw + dl.of_blw    ,
                        'btm'       : sp_abv + dl.of_abv    ,
                        'lft'       : dl.sp_rof + dl.of_rof ,
                        'ryt'       : dl.sp_lof + dl.of_lof ,
                        'typ'       : dl.dtyp               }
        rtn = gv.cur.execute(io.sqltxt,io.sqlarg).fetchall()
    except Exception as e:
        do.op = 'no_papa'
        io.sqlarg = e
#        prnt(f'''
#    {do.docname} {io.dl.dname}: no_papa''')
        rtn = []
    if len(rtn) == 0:
#        prnt(f'''
#    {docname} {dl.dname}: sql found nothing''')
        if type(dl.rg) == str and dl.rg.startswith('gk_'):
            do.nomore = True
            prnt(f'''
    NOT VERY MUCH TESTED
    {do.docname} {dl.dname}: {dl.rg} no value: do.nomore = True''')
    for i in rtn:
#        print(i)   ## i has CONF
        io.sqlrtn.append(i)
    return
