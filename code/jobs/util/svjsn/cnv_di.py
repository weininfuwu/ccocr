#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   cnv_di.py   260324  cy
#
#   Convert DI raw JSON so that each word is assigned to its best-matching
#   line (by IOS after tilt correction).  Words with no overlap go to
#   orphan_words[], which is a sibling of lines[] inside each page.
#
#   Input  : DI raw JSON  (pages[].words / pages[].lines)  from jsnRAW/
#   Output : same structure, with pages[].lines[].words[] filled in
#             and pages[].orphan_words[] added
#             saved to jsnRAW+/  (DD.jsn_raw + '+')
#
#   Usage  : called from svjsn pipeline after jsnRAW is saved
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import json
import math
import os

from jobs.env import DD
from m.prnt   import prnt

def cnv_di(src_path):
    """
    Read DI raw JSON from src_path, convert, write to jsnRAW+/.
    jsnRAW+ is DD.jsn_raw + '+' and is created if it does not exist.
    Returns the converted dict.
    """
    jsn_raw_plus = DD.jsn_raw + '+'
    os.makedirs(jsn_raw_plus, exist_ok=True)

    dst_path = os.path.join(jsn_raw_plus, os.path.basename(src_path))

    with open(src_path, encoding='utf-8') as f:
        data = json.load(f)

    pages_in  = data.get('pages', [])
    pages_out = [_convert_page(p) for p in pages_in]

    data_out = dict(data)
    data_out['pages'] = pages_out
                                    # drop page-level copy

    with open(dst_path, 'w', encoding='utf-8') as f:
        json.dump(data_out, f, indent=2, ensure_ascii=False)

    prnt(f'cnv_di saved  {os.path.basename(dst_path)}')
    return data_out

# ---------------------------------------------------------------------------
# core conversion
# ---------------------------------------------------------------------------

def _convert_page(page):
    """
    Take one page dict from DI raw JSON and return a new page dict where:
      - lines[i].words  : list of word dicts that belong to this line
      - orphan_words    : list of word dicts that matched no line (IOS == 0)

    Original page keys other than 'lines' are preserved as-is.
    """
    lines_raw = page.get('lines', [])
    words_raw = page.get('words', [])
    angle_deg = page.get('angle', 0.0)
    img_w     = page.get('width',  1.0)
    img_h     = page.get('height', 1.0)

    def derot(poly):
        return _derotate_polygon(poly, angle_deg, img_w, img_h)

    # bucket: line index -> list of (derotated_x_min, word_dict)
    buckets      = [[] for _ in lines_raw]
    orphan_words = []

    for word in words_raw:
        w_poly_raw  = word.get('polygon', [0] * 8)
        w_poly_derot = derot(w_poly_raw)

        best_idx = -1
        best_ios = 0.0
        for li, line in enumerate(lines_raw):
            l_poly_derot = derot(line.get('polygon', [0] * 8))
            score = _ios(w_poly_derot, l_poly_derot)
            if score > best_ios:
                best_ios = score
                best_idx = li

        if best_idx >= 0:
            x_min = _bbox(w_poly_derot)[0]
            buckets[best_idx].append((x_min, word))
        else:
            orphan_words.append(word)

    # build output lines: sort each bucket left-to-right by derotated x_min
    lines_out = []
    for li, line in enumerate(lines_raw):
        sorted_words = [w for _, w in sorted(buckets[li], key=lambda t: t[0])]
        line_out = dict(line)           # copy all original keys (polygon, content, ...)
        line_out['words'] = sorted_words
        lines_out.append(line_out)

    page_out = dict(page)               # copy all original keys (pageNumber, angle, ...)
    page_out['lines']        = lines_out
    page_out['orphan_words'] = orphan_words
    page_out.pop('words')
    # 'words' at page level is no longer needed (all assigned), but keep for traceability
    return page_out
# ---------------------------------------------------------------------------
# geometry helpers
# ---------------------------------------------------------------------------

def _rotate_point(x, y, cx, cy, rad):
    dx, dy = x - cx, y - cy
    rx = dx * math.cos(rad) - dy * math.sin(rad) + cx
    ry = dx * math.sin(rad) + dy * math.cos(rad) + cy
    return rx, ry


def _derotate_polygon(polygon, angle_deg, img_w, img_h):
    # rotate polygon back by -angle so coordinates become axis-aligned
    rad = -math.radians(angle_deg)
    cx, cy = img_w / 2.0, img_h / 2.0
    pts = [(polygon[i], polygon[i + 1]) for i in range(0, len(polygon), 2)]
    out = []
    for x, y in pts:
        rx, ry = _rotate_point(x, y, cx, cy, rad)
        out += [rx, ry]
    return out


def _bbox(polygon):
    # returns (x_min, y_min, x_max, y_max) from flat [x0,y0,x1,y1,...] list
    xs = polygon[0::2]
    ys = polygon[1::2]
    return min(xs), min(ys), max(xs), max(ys)


def _ios(a_poly, b_poly):
    # Intersection over Smaller area
    ax0, ay0, ax1, ay1 = _bbox(a_poly)
    bx0, by0, bx1, by1 = _bbox(b_poly)
    ix0 = max(ax0, bx0)
    iy0 = max(ay0, by0)
    ix1 = min(ax1, bx1)
    iy1 = min(ay1, by1)
    if ix1 <= ix0 or iy1 <= iy0:
        return 0.0
    inter = (ix1 - ix0) * (iy1 - iy0)
    area_a = max((ax1 - ax0) * (ay1 - ay0), 1)
    area_b = max((bx1 - bx0) * (by1 - by0), 1)
    return inter / min(area_a, area_b)




