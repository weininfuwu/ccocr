#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   updn_di.py      260321  cy
#   updated: 260324.101203 by cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import json
import math
import os

from azure.core.exceptions import HttpResponseError

from m.prnt     import prnt

def updn_di(png, jsnf, client):    # can be any image incl pdf
    prnt(f'going to up (DI)  {os.path.basename(png)}')
    with open(png, 'rb') as f:
        try:
            poller = client.begin_analyze_document(
                'prebuilt-read',
                body         = f,
                content_type = 'application/octet-stream',
            )
        except HttpResponseError as e:
            prnt(f'DI upload error [{e.status_code}] {e.error.code}: {e.error.message}')
            raise Exception('Document Intelligence へのアップロードが失敗しました')
    prnt(f'going to dwn (DI) {os.path.basename(png)}')
    try:
        rslt = poller.result()
    except HttpResponseError as e:
        prnt(f'DI poll error  [{e.status_code}] {e.error.code}: {e.error.message}')
        raise Exception('Document Intelligence がエラーを返しました')
    rslt = rslt.as_dict()
    with open(jsnf, 'w', encoding='utf-8') as f:
        json.dump(rslt, f, indent=2, ensure_ascii=False)
    prnt(f'DI json saved  {os.path.basename(jsnf)}')
    return


# ---------------------------------------------------------------------------
# geometry helpers
# ---------------------------------------------------------------------------

def _rotate_point(x, y, cx, cy, rad):
    # rotate (x,y) around center (cx,cy) by rad radians
    dx = x - cx
    dy = y - cy
    rx = dx * math.cos(rad) - dy * math.sin(rad) + cx
    ry = dx * math.sin(rad) + dy * math.cos(rad) + cy
    return rx, ry

def _derotate_polygon(polygon, angle_deg, img_w, img_h):
    # rotate polygon points back by -angle so they become axis-aligned
    rad = -math.radians(angle_deg)
    cx, cy = img_w / 2.0, img_h / 2.0
    pts = [(polygon[i], polygon[i+1]) for i in range(0, len(polygon), 2)]
    rotated = [_rotate_point(x, y, cx, cy, rad) for x, y in pts]
    result = []
    for rx, ry in rotated:
        result += [rx, ry]
    return result

def _bbox(polygon):
    # polygon: [x0,y0, x1,y1, x2,y2, x3,y3]
    # returns (x_min, y_min, x_max, y_max)
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

def _polygon_to_bbox(polygon):
    # CV boundingBox: [TL_x, TL_y, TR_x, TR_y, BR_x, BR_y, BL_x, BL_y]
    # DI polygon:     [x0,y0, x1,y1, x2,y2, x3,y3]  same layout
    return list(polygon)

# ---------------------------------------------------------------------------
# CV-compatible JSON builder
# ---------------------------------------------------------------------------

def _di_to_cv(result_dict):
    """
    Convert DI as_dict() result to CV V3.2-compatible dict.
    pages is at top level in DI as_dict().
    words are page-level; assign to lines via IOS.
    """
    pages = result_dict.get('pages', [])

    read_results = []
    for page in pages:
        lines_raw  = page.get('lines', [])
        words_raw  = page.get('words', [])
        angle_deg  = page.get('angle', 0.0)
        img_w      = page.get('width',  1.0)
        img_h      = page.get('height', 1.0)

        # derotate polygons so IOS uses axis-aligned boxes
        def derot(poly):
            return _derotate_polygon(poly, angle_deg, img_w, img_h)

        # assign each word to the line with highest IOS
        line_words   = [[] for _ in lines_raw]
        orphan_words = []
        for word in words_raw:
            w_poly = derot(word.get('polygon', [0] * 8))
            best_idx = -1
            best_ios = 0.0
            for li, line in enumerate(lines_raw):
                l_poly = derot(line.get('polygon', [0] * 8))
                s = _ios(w_poly, l_poly)
                if s > best_ios:
                    best_ios = s
                    best_idx = li
            if best_idx >= 0:
                line_words[best_idx].append(word)
            else:
                orphan_words.append(word)

        lines_out = []
        for li, line in enumerate(lines_raw):
            # sort words left-to-right using derotated x_min
            sorted_words = sorted(
                line_words[li],
                key=lambda w: _bbox(derot(w.get('polygon', [0]*8)))[0]
            )
            words_out = []
            for word in sorted_words:
                words_out.append({
                    'boundingBox' : _polygon_to_bbox(word.get('polygon', [0]*8)),
                    'text'        : word.get('content', ''),
                    'confidence'  : word.get('confidence', 1.0),
                })
            lines_out.append({
                'boundingBox' : _polygon_to_bbox(line.get('polygon', [0]*8)),
                'text'        : line.get('content', ''),
                'appearance'  : {'style': {'name': 'other', 'confidence': 1.0}},
                'words'       : words_out,
            })

        orphan_word_objs = [{
            'boundingBox' : _polygon_to_bbox(w.get('polygon', [0]*8)),
            'text'        : w.get('content', ''),
            'confidence'  : w.get('confidence', 1.0),
        } for w in orphan_words]

        read_results.append({
            'page'   : page.get('pageNumber', 1),
            'angle'  : page.get('angle', 0.0),
            'width'  : page.get('width', 0.0),
            'height' : page.get('height', 0.0),
            'unit'   : page.get('unit', 'pixel'),
            'lines'         : lines_out,
            'orphan_words'  : orphan_word_objs,
        })

    return {
        'status'              : 'succeeded',
        'createdDateTime'     : '',
        'lastUpdatedDateTime' : '',
        'analyzeResult'       : {
            'version'      : '3.2.0',
            'modelVersion' : '2022-04-30',
            'readResults'  : read_results,
        }
    }

