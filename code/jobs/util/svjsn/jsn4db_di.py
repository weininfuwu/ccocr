#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   jsn4db_di.py    260328  cy
#   updated: 260328 add angl/jw/jh to page; polygon via raw4 12-tuple
#   updated: 260328 line conf -> None (DI API does not provide line confidence)
#   updated: 260329 line conf None->0: DI API never returns 0, so 0 is safe as
#            sentinel meaning "unknown confidence, treat as lowest priority"
#
#   Convert DI (Azure Document Intelligence) jsnRAW++ into jsn4db structure.
#
#--------1---------2---------3---------4---------5---------6---------7--------#

from .jsn4db_util import raw4, page_bounds, zoom, elem


def convert_di(jsn):
    pages_raw = jsn.get('pages', [])
    pages_out = []
    for page_raw in pages_raw:
        page_num  = page_raw.get('pageNumber', 1)
        lines_raw = page_raw.get('lines', [])
        orphans   = page_raw.get('orphan_words', [])

        elems = _collect(lines_raw, orphans)
        ptop, plft, pryt = page_bounds(elems)
        zm = zoom(plft, pryt)

        lines_out = []
        for lno, line in enumerate(lines_raw, 1):
            lraw = raw4(line['polygon'])
            words_out = []
            for wno, word in enumerate(line.get('words', []), 1):
                wraw = raw4(word['polygon'])
                words_out.append(elem(
                    f'{lno}.{wno}', wraw, ptop, plft, zm,
                    word.get('content', ''),
                    word.get('confidence', 1.0)))
            lines_out.append({
                **elem(str(lno), lraw, ptop, plft, zm,
                       line.get('content', ''), 0),
                'words': words_out,
            })

        page_dict = {
            'page' : page_num,
            'angl' : page_raw.get('angle', 0.0),
            'jw'   : page_raw.get('width',  0.0),
            'jh'   : page_raw.get('height', 0.0),
            'ptop' : ptop,
            'plft' : plft,
            'pryt' : pryt,
            'lines': lines_out,
        }

        if orphans:
            orphans_out = []
            for ono, word in enumerate(orphans, 1):
                wraw = raw4(word['polygon'])
                orphans_out.append(elem(
                    f'orphan.{ono}', wraw, ptop, plft, zm,
                    word.get('content', ''),
                    word.get('confidence', 1.0)))
            page_dict['orphan_words'] = orphans_out

        pages_out.append(page_dict)

    return {'pages': pages_out}


def _collect(lines_raw, orphans):
    elems = []
    for line in lines_raw:
        elems.append(raw4(line['polygon']))
        for word in line.get('words', []):
            elems.append(raw4(word['polygon']))
    for word in orphans:
        elems.append(raw4(word['polygon']))
    return elems
