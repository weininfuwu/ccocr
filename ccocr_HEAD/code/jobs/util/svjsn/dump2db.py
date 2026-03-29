#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   dump2db.py      260328  cy
#   updated: 260328 add angl/jw/jh to page; add 8-pt polygon to elm
#   updated: 260328 apply rotate() before storing top/btm/lft/ryt (fix rotated docs)
#
#   Write jsn4db results to {jobid}.dump.db (SQLite).
#   Called from svjsn() after all jsn4db() calls complete.
#
#   Input:  results dict  { dst_path: out_dict }
#           out_dict keys: pdf, engine, apisrc, pages
#
#   Tables:
#     page(pdf, page, ptop, plft, pryt, angl, jw, jh, engine, apisrc)
#     elm (seq, pdf, page, node, typ, top..ryt, txt,
#          otop..oryt, otl_x..obl_y, pg_top, pg_btm, conf,
#          engine, apisrc)
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import os
import sqlite3

from m.prnt                         import prnt
from m.env                          import D
from jobs.env                       import DD
from jobs.jsn2db.markpng.rotate     import rotate
from .dump2db_xl                    import dump2db_xl


def dump2db(results):
    """
    results : { dst_path: out_dict }
    Writes page + elm tables, then generates dump Excel.
    """
    dbf    = os.path.join(D.logd, f'{D.jobid}.dump.db')
    DD.dbf = dbf
    prnt('writing dump db')

    con = sqlite3.connect(dbf)
    cur = con.cursor()
    _create_tables(cur)

    for out in results.values():
        _write_out(cur, out)

    con.commit()
    con.close()
    dump2db_xl()


def _create_tables(cur):
    cur.execute('''
        CREATE TABLE IF NOT EXISTS page (
            pdf     TEXT,
            page    INTEGER,
            ptop    INTEGER,
            plft    INTEGER,
            pryt    INTEGER,
            angl    REAL,
            jw      REAL,
            jh      REAL,
            engine  TEXT,
            apisrc  TEXT,
            UNIQUE(pdf, page, engine, apisrc)
        )''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS elm (
            seq     INTEGER PRIMARY KEY,
            pdf     TEXT,
            page    INTEGER,
            node    TEXT,
            typ     TEXT,
            top     INTEGER,
            btm     INTEGER,
            lft     INTEGER,
            ryt     INTEGER,
            txt     TEXT,
            otop    INTEGER,
            obtm    INTEGER,
            olft    INTEGER,
            oryt    INTEGER,
            otl_x   REAL,
            otl_y   REAL,
            otr_x   REAL,
            otr_y   REAL,
            obr_x   REAL,
            obr_y   REAL,
            obl_x   REAL,
            obl_y   REAL,
            note1   TEXT,
            note2   TEXT,
            note3   TEXT,
            pg_top  INTEGER,
            pg_btm  INTEGER,
            conf    REAL,
            engine  TEXT,
            apisrc  TEXT
        )''')


def _rot_bbox(elm, angl, ow, oh, jw, jh):
    """Return (rot_top, rot_btm, rot_lft, rot_ryt) in rotated coordinate space."""
    tl, tr, br, bl = rotate(
        angl,
        elm['otl_x'], elm['otl_y'],
        elm['otr_x'], elm['otr_y'],
        elm['obr_x'], elm['obr_y'],
        elm['obl_x'], elm['obl_y'],
        ow, oh, jw, jh)
    xs = [tl[0], tr[0], br[0], bl[0]]
    ys = [tl[1], tr[1], br[1], bl[1]]
    return min(ys), max(ys), min(xs), max(xs)


def _write_out(cur, out):
    pdf    = out['pdf']
    engine = out['engine']
    apisrc = out['apisrc']
    tb_exp = 100000

    for pg in out['pages']:
        page_num = pg['page']
        angl = pg['angl']
        jw   = pg['jw']
        jh   = pg['jh']
        if jw < 50:        # inch coords (original PDF): scale up for rotate() precision
            ow, oh = jw * 1000, jh * 1000
        else:
            ow, oh = jw, jh  # PNG: API pixel coords == image pixel dims

        # Collect all elements (line/word/orphan) in order
        all_elms = []
        for line in pg['lines']:
            all_elms.append((line, 'line'))
            for word in line.get('words', []):
                all_elms.append((word, 'word'))
        for word in pg.get('orphan_words', []):
            all_elms.append((word, 'orphan'))

        # Rotate each element's polygon; keep only valid (non-inverted) bboxes
        rot_bboxes = []
        for elm, typ in all_elms:
            rt, rb, rl, rr = _rot_bbox(elm, angl, ow, oh, jw, jh)
            rot_bboxes.append((rt, rb, rl, rr) if rt <= rb and rl <= rr else None)

        # Page bounds from rotated, valid bboxes
        valid = [b for b in rot_bboxes if b is not None]
        if valid:
            ptop = min(b[0] for b in valid)
            plft = min(b[2] for b in valid)
            pryt = max(b[3] for b in valid)
        else:
            ptop, plft, pryt = pg['ptop'], pg['plft'], pg['pryt']
        zm = 1200 / (pryt - plft) if (pryt - plft) > 0 else 1.0

        cur.execute('''
            INSERT OR IGNORE INTO page(
                pdf, page, ptop, plft, pryt,
                angl, jw, jh, engine, apisrc)
            VALUES(?,?,?,?,?,?,?,?,?,?)''', (
            pdf, page_num, ptop, plft, pryt,
            angl, jw, jh, engine, apisrc))

        for (elm, typ), bbox in zip(all_elms, rot_bboxes):
            if bbox is None:
                continue
            rt, rb, rl, rr = bbox
            top = round((rt - ptop) * zm)
            btm = round((rb - ptop) * zm)
            lft = round((rl - plft) * zm)
            ryt = round((rr - plft) * zm)
            _ins_elm(cur, pdf, page_num, engine, apisrc,
                     elm, typ, tb_exp, top, btm, lft, ryt)


def _ins_elm(cur, pdf, page_num, engine, apisrc,
             elm, typ, tb_exp, top, btm, lft, ryt):
    cur.execute('''
        INSERT INTO elm(
            pdf, page, node, typ,
            top, btm, lft, ryt,
            txt,
            otop, obtm, olft, oryt,
            otl_x, otl_y, otr_x, otr_y,
            obr_x, obr_y, obl_x, obl_y,
            pg_top, pg_btm,
            conf, engine, apisrc
        ) VALUES(
            ?,?,?,?,
            ?,?,?,?,
            ?,
            ?,?,?,?,
            ?,?,?,?,
            ?,?,?,?,
            ?,?,
            ?,?,?)''', (
        pdf, page_num, elm['node'], typ,
        top, btm, lft, ryt,
        elm['text'],
        elm['otop'], elm['obtm'], elm['olft'], elm['oryt'],
        elm['otl_x'], elm['otl_y'],
        elm['otr_x'], elm['otr_y'],
        elm['obr_x'], elm['obr_y'],
        elm['obl_x'], elm['obl_y'],
        page_num * tb_exp + top,
        page_num * tb_exp + btm,
        elm['conf'], engine, apisrc,
    ))
