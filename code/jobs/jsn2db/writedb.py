#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   writedb.py  220711  cy
#   updated: 260321 add engine column to elm table
#   updated: 260322 add usepng column to elm table
#   updated: 260322 add engine/usepng to page table; add UNIQUE constraint
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import os
import sqlite3

from m.prnt import prnt
from m.env  import D
from ..env  import DD

def writedb(dbsrc):
    prnt('writing dump db')
    [elmdb, pagedb] = dbsrc
    dbf     = os.path.join(D.logd, f'{D.jobid}.dump.db')
    DD.dbf  = dbf
    con     = sqlite3.connect(dbf)
    cur     = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS page (
            pdf     TEXT,       -- 01
            page    INTEGER,    -- 02
            ptop    INTEGER,    -- 03
            plft    INTEGER,    -- 04
            pryt    INTEGER,    -- 05
            engine  TEXT,       -- 06  'CV' / 'DI' / ''
            usepng  TEXT,       -- 07  'png' / 'straight'
            UNIQUE(pdf, page, engine, usepng)
        )''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS elm (
            seq         INTEGER PRIMARY KEY,    -- 01 AUTO NUMBERED
            pdf         TEXT,       -- 02
            page        INTEGER,    -- 03
            node        TEXT,       -- 04
            typ         TEXT,       -- 05
            top         INTEGER,    -- 06
            btm         INTEGER,    -- 07
            lft         INTEGER,    -- 08
            ryt         INTEGER,    -- 09
            txt         TEXT,       -- 10
            otop        INTEGER,    -- 11
            obtm        INTEGER,    -- 12
            olft        INTEGER,    -- 13
            oryt        INTEGER,    -- 14
            note1       TEXT,       -- 15   blank
            note2       TEXT,       -- 16   blank
            note3       TEXT,       -- 17   blank
            pg_top      INTEGER,    -- 18
            pg_btm      INTEGER,    -- 19
            conf        REAL,       -- 20
            engine      TEXT,       -- 21  'CV' / 'DI' / ''
            usepng      TEXT        -- 22  'png' / 'straight'
        )''')
    for i in pagedb:
        tpl = tuple(i)
        cur.execute('''
            INSERT OR IGNORE INTO page(
                pdf,    -- 01
                page,   -- 02
                ptop,   -- 03
                plft,   -- 04
                pryt,   -- 05
                engine, -- 06
                usepng  -- 07
            ) VALUES(?,?,?,?,?,?,?)''', tpl)
    for i in elmdb:
        if i[9] > i[10] or i[11] > i[12]:
            continue
        dic = {
            'pdf'   : i[0],
            'page'  : i[1],
            'node'  : i[2],
            'typ'   : i[3],
            'top'   : i[4],
            'btm'   : i[5],
            'lft'   : i[6],
            'ryt'   : i[7],
            'txt'   : i[8],
            'otop'  : i[9],
            'obtm'  : i[10],
            'olft'  : i[11],
            'oryt'  : i[12],
            'conf'  : i[13],
            'engine': i[14],
            'usepng': i[15],
        }
        tb_exp          = 100000
        dic['pg_top']   = dic['page'] * tb_exp + dic['top']
        dic['pg_btm']   = dic['page'] * tb_exp + dic['btm']
        cur.execute('''
            INSERT INTO elm (
                pdf,    page,   node,   typ,
                top,    btm,    lft,    ryt,
                txt,
                otop,   obtm,   olft,   oryt,
                pg_top, pg_btm,
                conf,   engine, usepng
            ) VALUES(
                :pdf,   :page,  :node,  :typ,
                :top,   :btm,   :lft,   :ryt,
                :txt,
                :otop,  :obtm,  :olft,  :oryt,
                :pg_top,:pg_btm,
                :conf,  :engine,:usepng
            )''', dic)
    con.commit()
    con.close()
    return
