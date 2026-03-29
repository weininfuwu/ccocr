#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   wrd2line.py     260327  cy
#
#   Post-process jsnRAW+ and write jsnRAW++.
#
#   vision  : copy jsnRAW+ as-is to jsnRAW++
#   intelli : rotate-correct each word polygon, find the line with highest
#             IOS (intersection / word-area), attach word to that line.
#             Words that match no line go to orphan_words[] at page level.
#             Result is written to jsnRAW++.
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import json
import math
import os

from m.prnt   import prnt
from m.env    import D


# ---------------------------------------------------------------------------
# public entry point
# ---------------------------------------------------------------------------

def wrd2line(bn, jsn, engine, jsnf):
    """
    bn     : pngUP basename (for logging)
    jsn    : JSON dict already returned by chk_cv / chk_di (jsnRAW+ content)
    engine : 'vision' or 'intelli'
    jsnf   : path to jsnRAW file; jsnRAW++ uses same filename in sibling dir

    vision  : write jsnRAW+ content as-is to jsnRAW++
    intelli : assign page-level words to lines, write result to jsnRAW++
    Returns the written dict.
    """
    jsnraw_plus2 = os.path.join(D.logd, 'jsnRAW++')
    os.makedirs(jsnraw_plus2, exist_ok=True)

    if engine == 'vision':
        dst = os.path.join(jsnraw_plus2, os.path.basename(jsnf))
        with open(dst, 'w', encoding='utf-8') as f:
            json.dump(jsn, f, indent=2, ensure_ascii=False)
        prnt(f'wrd2line (CV) saved   {os.path.basename(dst)}')
        return jsn

    elif engine == 'intelli':
        out = _convert_di(jsn)
        dst = os.path.join(jsnraw_plus2, os.path.basename(jsnf))
        with open(dst, 'w', encoding='utf-8') as f:
            json.dump(out, f, indent=2, ensure_ascii=False)
        prnt(f'wrd2line (DI) saved   {os.path.basename(dst)}')
        return out

    else:
        raise Exception(f'wrd2line: unknown engine: {engine}')


# ---------------------------------------------------------------------------
# intelli conversion
# ---------------------------------------------------------------------------

def _convert_di(data):
    """
    Walk pages[], assign each page-level word to its best-matching line
    via IOS after tilt correction.  Words with IOS == 0 go to orphan_words[].
    Removes the flat 'words' list from each page (all assigned or orphaned).
    Returns a new dict (shallow copy of data with pages replaced).
    """
    pages_in  = data.get('pages', [])
    pages_out = [_convert_page(p) for p in pages_in]

    out = dict(data)
    out['pages'] = pages_out
    return out


def _convert_page(page):
    lines_raw = page.get('lines', [])
    words_raw = page.get('words', [])
    angle_deg = page.get('angle', 0.0)
    img_w     = page.get('width',  1.0)
    img_h     = page.get('height', 1.0)

    def derot(poly):
        return _derotate_polygon(poly, angle_deg, img_w, img_h)

    # bucket[li] = list of (derotated_x_min, word_dict)
    buckets      = [[] for _ in lines_raw]
    orphan_words = []

    for word in words_raw:
        w_poly_raw   = word.get('polygon', [0] * 8)
        w_poly_derot = derot(w_poly_raw)
        w_area       = _area(_bbox(w_poly_derot))

        best_idx = -1
        best_ios = 0.0
        for li, line in enumerate(lines_raw):
            l_poly_derot = derot(line.get('polygon', [0] * 8))
            score = _ios_word(w_poly_derot, l_poly_derot, w_area)
            if score > best_ios:
                best_ios = score
                best_idx = li

        if best_idx >= 0:
            x_min = _bbox(w_poly_derot)[0]
            buckets[best_idx].append((x_min, word))
        else:
            orphan_words.append(word)

    # build output lines sorted left-to-right within each line
    lines_out = []
    for li, line in enumerate(lines_raw):
        sorted_words = [w for _, w in sorted(buckets[li], key=lambda t: t[0])]
        line_out = dict(line)
        line_out['words'] = sorted_words
        lines_out.append(line_out)

    page_out = dict(page)
    page_out['lines']        = lines_out
    page_out['orphan_words'] = orphan_words  # always present; empty list if no orphans
    page_out.pop('words', None)              # consumed; all words now under lines or orphan_words
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
    rad = -math.radians(angle_deg)
    cx, cy = img_w / 2.0, img_h / 2.0
    out = []
    for i in range(0, len(polygon), 2):
        rx, ry = _rotate_point(polygon[i], polygon[i+1], cx, cy, rad)
        out += [rx, ry]
    return out


def _bbox(polygon):
    # (x_min, y_min, x_max, y_max) from flat [x0,y0,x1,y1,...] list
    xs = polygon[0::2]
    ys = polygon[1::2]
    return min(xs), min(ys), max(xs), max(ys)


def _area(bbox):
    x0, y0, x1, y1 = bbox
    return max((x1 - x0) * (y1 - y0), 1)


def _ios_word(w_poly, l_poly, w_area):
    """
    Intersection area / word area.
    Answers: what fraction of this word overlaps the line?
    """
    wx0, wy0, wx1, wy1 = _bbox(w_poly)
    lx0, ly0, lx1, ly1 = _bbox(l_poly)
    ix0 = max(wx0, lx0)
    iy0 = max(wy0, ly0)
    ix1 = min(wx1, lx1)
    iy1 = min(wy1, ly1)
    if ix1 <= ix0 or iy1 <= iy0:
        return 0.0
    inter = (ix1 - ix0) * (iy1 - iy0)
    return inter / w_area
