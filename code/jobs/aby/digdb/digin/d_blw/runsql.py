#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   runsql.py       230427  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

#from m.aby_sub.digdb_sub.gv import gv
from m.prnt import prnt
from ...gv import gv # m_ccocr\m_aby\digdb_sub


def runsql(docname,pdf,fm,to,do,io,engine='',apisrc=''):
    dl = io.dl
    u_blw = ''
    u_pgt = ''
    u_hdb = ''
    u_gkt = ''
    u_abv = ''
    u_pgb = ''
    u_ftt = ''
    u_ngk = ''
    use = '[USE THIS]'
    ## TOP
    if type(dl.sp_blw) == int:
        top = dl.sp_blw + dl.of_blw
        u_blw = use
    else:
        top = [ do.pgtop    ,
                do.hdbtm    ,
                do.gktop    ]
        top = max(list(filter(lambda x: type(x) == int,top)))
        u_pgt = use
        u_hdb = use
        u_gkt = use
    ## BOTTOM
    if type(dl.sp_abv) == int:
        btm  = dl.sp_abv + dl.of_abv
        u_abv = use
    else:
        btm = [ do.pgbtm    ,
                do.fttop    ,
                do.ngktop   ]
        btm = min(list(filter(lambda x: type(x) == int,btm)))
        u_pgb = use
        u_ftt = use
        u_ngk = use
    io.sqltxt = f'''
/*  pdf     : {pdf} p{fm}-{to} doc# {do.docnum}
    docname : {docname}
    level 1, dname {dl.dname}, rg {dl.rg}
    sp_blw of_blw : {dl.sp_blw} {dl.of_blw} {u_blw}
    do.pgtop      : {do.pgtop} {u_pgt}
    do.hdbtm      : {do.hdbtm} {u_hdb}
    do.gktop      : {do.gktop} {u_gkt}
    do.gkbtm      : {do.gkbtm} (for ref)
        ** top ** : {top}
    sp_abv of_abv : {dl.sp_abv} {dl.of_abv} {u_abv}
    do.pgbtm      : {do.pgbtm} {u_pgb}
    do.fttop      : {do.fttop} {u_ftt}
    do.ngktop     : {do.ngktop} {u_ngk}
    do.ngkbtm     : {do.ngkbtm} (for ref)
        ** btm ** : {btm}
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
                        'top'       : top                   ,
                        'btm'       : btm                   ,
                        'lft'       : dl.sp_rof + dl.of_rof ,
                        'ryt'       : dl.sp_lof + dl.of_lof ,
                        'typ'       : dl.dtyp               }
        if type(top) != int:
            raise Exception(f'top is not int "{top}"')
        if type(btm) != int:
            raise Exception(f'btm is not int "{btm}"')
        rtn = gv.cur.execute(io.sqltxt,io.sqlarg).fetchall()
    except Exception as e:
        do.op = 'no_papa'
        io.sqlarg = e
#        prnt(f'''
#    {docname} {dl.dname}: cannot run sql''')
        rtn = []
    if len(rtn) == 0:
#        prnt(f'''
#    {docname} {dl.dname}: sql found nothing''')
        if type(dl.rg) == str and dl.rg.startswith('gk_'):
            do.nomore = True
    for i in rtn:
#        print(f'ho {i}')    # has CONF
        io.sqlrtn.append(i)
    return
