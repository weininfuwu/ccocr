#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   jsn4db_cv.py    260328  cy
#   updated: 260328 add angl/jw/jh to page; polygon via raw4 12-tuple
#
#   Convert CV (Azure Computer Vision) jsnRAW++ into jsn4db page structure.
#
#--------1---------2---------3---------4---------5---------6---------7--------#

from .jsn4db_util import raw4, page_bounds, zoom, elem


def convert_cv(jsn):
    pages_raw = jsn['analyzeResult']['readResults']
    pages_out = []
    for page_raw in pages_raw:
        page_num  = page_raw['page']
        lines_raw = page_raw.get('lines', [])

        elems = _collect(lines_raw)
        ptop, plft, pryt = page_bounds(elems)
        zm = zoom(plft, pryt)

        lines_out = []
        for lno, line in enumerate(lines_raw, 1):
            lraw = raw4(line['boundingBox'])
            conf = line.get('appearance', {}).get(
                'style', {}).get('confidence', 1.0)
            words_out = []
            for wno, word in enumerate(line.get('words', []), 1):
                wraw = raw4(word['boundingBox'])
                words_out.append(elem(
                    f'{lno}.{wno}', wraw, ptop, plft, zm,
                    word.get('text', ''),
                    word.get('confidence', 1.0)))
            lines_out.append({
                **elem(str(lno), lraw, ptop, plft, zm,
                       line.get('text', ''), conf),
                'words': words_out,
            })

        pages_out.append({
            'page' : page_num,
            'angl' : page_raw.get('angle', 0.0),
            'jw'   : page_raw.get('width',  0.0),
            'jh'   : page_raw.get('height', 0.0),
            'ptop' : ptop,
            'plft' : plft,
            'pryt' : pryt,
            'lines': lines_out,
        })

    return {'pages': pages_out}


def _collect(lines_raw):
    elems = []
    for line in lines_raw:
        elems.append(raw4(line['boundingBox']))
        for word in line.get('words', []):
            elems.append(raw4(word['boundingBox']))
    return elems
