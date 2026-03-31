#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   markpng.py      250220  cy
#   updated: 260320.094318 by cy
#   updated: 260321 use 'in' for BOTH-mode label check (CV/DI suffix appended)
#   updated: 260322 split elmlst by usepng; straight skips blnkpng/draw entirely
#   updated: 260322 fix straight-only: remove raise; _add_straight_to_dbsrc
#             now computes zoom-normalized scaled coords (0-1200) instead of 0-fixed
#   updated: 260322 add draw_straight(): BOTH mode draws STRAIGHT OCR results
#             onto NOUP.png using inch->pixel conversion (jw/jh -> ow/oh)
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import os

from m.prnt import prnt
from m.env  import D
from ...env  import DD
from .blnkpng         import blnkpng
from .mkdrwlst        import mkdrwlst
from .mkdrwlst_rot    import mkdrwlst_rot
from .draw            import draw
from .draw_rot        import draw_rot
from .draw_straight   import draw_straight
from .mkdbsrc         import mkdbsrc, _strip_engine, _derive_usepng
from ...util.usepng   import strip_label

def markpng(elmlst):
    prnt('marking png, making elment list')
    pngROT      = os.path.join(D.logd,'pngROT')
    pngMK       = os.path.join(D.logd,'pngMK')
    pngRMK      = os.path.join(D.logd,'pngRMK')
    DD.pngROT   = pngROT
    DD.pngMK    = pngMK
    DD.pngRMK   = pngRMK
    os.mkdir(pngROT)
    os.mkdir(pngMK)
    os.mkdir(pngRMK)
    pngORG = DD.pngPRE

    # split elmlst into png-converted entries and straight entries
    # usepng value is at index -1 (appended by chkjsn)
    elmlst_png      = [i for i in elmlst if i[-1] == 'png']
    elmlst_straight = [i for i in elmlst if i[-1] == 'straight']

    if not elmlst_png and not elmlst_straight:
        prnt('markpng: no elements found, skipping')
        return [[], []]

    # build pdfs_bare from png entries only (straight has no pngPRE file)
    pdfs_bare = {}
    for i in elmlst_png:
        bare = strip_label(i[0])
        pg   = i[1]
        pdfs_bare.setdefault(bare, {})
        pdfs_bare[bare].setdefault(pg, {'jw': i[2], 'jh': i[3], 'angl': i[4]})

    if pdfs_bare:
        # blnkpng reads pngPRE/*.png, rotates, writes pngROT/*.png
        # it also fills in ow/oh/rw/rh for each page entry
        elmlst_png_bare = [[strip_label(i[0])] + i[1:] for i in elmlst_png]

        #
        #   CHECKPOINT (3)
        #
        #   new folders of BLANK content
        #   pngROT pngMK pngRMK
        #
        prnt('''

    CHECK (3): markpng() is colling blnkpng()
    1) new BLANK folders pngROT pngMK pngRMK

    BACKUP log folder

    to start blnkpng()
    hit a key to go on ...
            ''')
        input('ok? ')

        blnkpng(pdfs_bare, pngORG, pngROT)

        #
        #   CHECKPOINT (4)
        #
        #   pngROT is FILLED with   hoge.ext.NN.NOUP.png    STRAIHGT mode
        #                           hoge.ext.NN.png         PNGUP mode
        #
        #   pngMK pngRMK remain BLANK
        #
        prnt('''

    CHECK (4): back at markpng() from blnkpng()
    1) pngROT is FILLED with    hoge.ext.NN.NOUP.png        STRAIHGT mode
                                hoge.ext.NN.png             PNGUP mode
    2) pngMK pngRMK remain BLANK

    BACKUP log folder

    to start blnkpng()
    hit a key to go on ...
            ''')
        input('ok? ')

        # draw bounding boxes onto pngMK (pre-rotation) and pngRMK (post-rotation)
        drwlst     = mkdrwlst(elmlst_png_bare, pdfs_bare)
        drwlst_rot = mkdrwlst_rot(elmlst_png_bare, pdfs_bare)
        draw(drwlst,     pngORG, pngMK,  use_noup=DD.pdf2api)
        draw_rot(drwlst_rot, pngROT, pngRMK, use_noup=DD.pdf2api)
    else:
        prnt('markpng: no png entries (straight-only mode), skipping blnkpng/draw')

    # BOTH mode: also draw STRAIGHT OCR results onto NOUP.png
    # (straight entries have inch-unit coords; convert to pixel via jw/jh -> ow/oh)
    if DD.pdf2api and DD.png2api and elmlst_straight:
        draw_straight(elmlst_straight, pdfs_bare, pngORG, pngMK, pngRMK)


    # DB source: use full labeled elmlst (png + straight)
    # mkdrwlst_rot skips straight internally; mkdbsrc sees the full set
    # pdfs for labeled lookup: rebuild with labeled keys from png entries
    pdfs_labeled = {}
    for i in elmlst_png:
        key = i[0]
        pg  = i[1]
        pdfs_labeled.setdefault(key, {})
        pdfs_labeled[key].setdefault(pg, {'jw': i[2], 'jh': i[3], 'angl': i[4]})
    # copy ow/oh/rw/rh from pdfs_bare back into pdfs_labeled
    for labeled_key, pages in pdfs_labeled.items():
        bare_key = strip_label(labeled_key)
        for pg, pgval in pages.items():
            if bare_key in pdfs_bare and pg in pdfs_bare[bare_key]:
                for field in ('ow', 'oh', 'rw', 'rh'):
                    if field in pdfs_bare[bare_key][pg]:
                        pgval[field] = pdfs_bare[bare_key][pg][field]

    # straight entries need a placeholder pdfs entry so mkdrwlst_rot can skip them
    # (mkdrwlst_rot already skips usepng=='straight', so pdfs_labeled content
    #  for straight keys is never actually accessed -- but the key must exist
    #  so we add dummy entries here to avoid KeyError if the guard ever changes)
    for i in elmlst_straight:
        key = i[0]
        pg  = i[1]
        pdfs_labeled.setdefault(key, {})
        pdfs_labeled[key].setdefault(pg, {'jw': i[2], 'jh': i[3], 'angl': i[4],
                                          'ow': 1, 'oh': 1, 'rw': 1, 'rh': 1})

    drwlst_rot_labeled = mkdrwlst_rot(elmlst, pdfs_labeled)
    dbsrc = mkdbsrc(drwlst_rot_labeled)

    # straight entries are not in drwlst_rot_labeled (skipped by mkdrwlst_rot),
    # but mkdbsrc must still record them for the DB.
    # add straight entries directly from elmlst_straight.
    _add_straight_to_dbsrc(elmlst_straight, dbsrc)

    return dbsrc


def _add_straight_to_dbsrc(elmlst_straight, dbsrc):
    """
    straight entries have no PNG/rotation coords.
    Scaled coords (top/btm/lft/ryt) are computed from raw JSON coords
    using the same zoom=1200/(pryt-plft) normalization as mkdbsrc(),
    so _dd sheet sp_blw/sp_abv/sp_rof/sp_lof values work on a 0-1200 scale.
    otop/obtm/olft/oryt store raw JSON coords (used by spic, which skips
    straight entries anyway).
    """
    if not elmlst_straight:
        return
    rtn      = dbsrc[0]
    rtn_page = dbsrc[1]

    # pass 1: compute per-page boundary (ptop/plft/pryt) from raw JSON coords
    page_bounds = {}
    for i in elmlst_straight:
        [pdf_labeled,page,jw,jh,angl,typ,node,
         otl_x,otl_y,otr_x,otr_y,obr_x,obr_y,obl_x,obl_y,txt,conf,usepng] = i
        pdf, engine = _strip_engine(pdf_labeled)
        key = (pdf, page, engine)
        top = min(otl_y, otr_y)
        btm = max(obl_y, obr_y)
        lft = min(otl_x, obl_x)
        ryt = max(otr_x, obr_x)
        if key not in page_bounds:
            page_bounds[key] = {'ptop': top, 'plft': lft, 'pryt': ryt,
                                'usepng': usepng}
        else:
            page_bounds[key]['ptop'] = min(page_bounds[key]['ptop'], top)
            page_bounds[key]['plft'] = min(page_bounds[key]['plft'], lft)
            page_bounds[key]['pryt'] = max(page_bounds[key]['pryt'], ryt)

    # rtn_page: one row per (pdf, page, engine)
    for (pdf, page, engine), b in page_bounds.items():
        rtn_page.append([pdf, page, b['ptop'], b['plft'], b['pryt'],
                         engine, b['usepng']])

    # pass 2: compute zoom-normalized scaled coords and append to rtn (elm)
    for i in elmlst_straight:
        [pdf_labeled,page,jw,jh,angl,typ,node,
         otl_x,otl_y,otr_x,otr_y,obr_x,obr_y,obl_x,obl_y,txt,conf,usepng] = i
        pdf, engine = _strip_engine(pdf_labeled)
        key  = (pdf, page, engine)
        b    = page_bounds[key]
        zoom = 1200 / (b['pryt'] - b['plft'])
        top  = min(otl_y, otr_y)
        btm  = max(obl_y, obr_y)
        lft  = min(otl_x, obl_x)
        ryt  = max(otr_x, obr_x)
        rtn.append([pdf, page, node, typ,
                    round((top - b['ptop']) * zoom),    # scaled top
                    round((btm - b['ptop']) * zoom),    # scaled btm
                    round((lft - b['plft']) * zoom),    # scaled lft
                    round((ryt - b['plft']) * zoom),    # scaled ryt
                    txt,
                    top, btm, lft, ryt,                 # otop/obtm/olft/oryt (raw JSON)
                    conf, engine, usepng])
