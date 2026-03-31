#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   chkjsn.py   250219  cy
#   updated: 260320.094535 by cy
#   updated: 260321 process jsnRAW, append engine suffix to elmlst pdf
#   updated: 260322 add usepng label ('png'/'straight') to elmlst[0];
#             straight entries skip pngPRE existence check (no marking png)
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import glob
import json
import os

from m.prnt             import prnt
from jobs.env           import DD, jkv
from .p1                import p1
from .p2                import p2
from .p3                import p3
from .p4                import p4
from jobs.util.usepng   import strip_label

def _chkjsn_dir(jsndir, engine_tag, elmlst):
    for jsn in sorted(glob.glob(os.path.join(jsndir, '*.json'))):
        bn = os.path.basename(jsn)
        if bn == 'DI_RAW_DEBUG.json':
            continue
        # bn examples:
        #   hoge.pdf.NN.CV.json       -> usepng='png'
        #   hoge.pdf.STRAIGHT.CV.json -> usepng='straight'

        bdy_with_tag = os.path.splitext(bn)[0]              # hoge.pdf.NN.CV
        bdy = bdy_with_tag[:-(len(engine_tag) + 1)]         # hoge.pdf.NN  or  hoge.pdf.STRAIGHT

        is_straight = bdy.endswith('.STRAIGHT')

        if is_straight:
            org_bn  = bdy[:-len('.STRAIGHT')]   # 'hoge.pdf'
            usepng  = 'straight'
            prnt(f'{bn} (STRAIGHT)')
            jsn_data = p1(bn, jsn)
            bn_l2s = f'{bdy}.json'
            for cntp, page_jsn in enumerate(jsn_data['readResults']):
                pginfo = p2(bn_l2s, page_jsn)
                pginfo[1] = cntp + 1
                idx_before = len(elmlst)
                for node, line_jsn in enumerate(page_jsn['lines']):
                    p3(bn, line_jsn, cntp, node, elmlst, pginfo)
                    for wnode, word_jsn in enumerate(line_jsn['words']):
                        p4(bn, word_jsn, cntp, node, wnode, elmlst, pginfo)
                for k in range(idx_before, len(elmlst)):
                    label_both  = ' STRAIGHT' if (DD.pdf2api and DD.png2api) else ''
                    elmlst[k][0] = elmlst[k][0] + label_both + f' {engine_tag}'
                    elmlst[k].append(usepng)    # index -1: usepng
        else:
            png = os.path.join(DD.pngPRE, f'{bdy}.png')
            if not os.path.isfile(png):
                raise Exception(f'NO PNG {bdy}.png')
            usepng = 'png'
            prnt(bn)
            jsn_data = p1(bn, jsn)
            bn_l2s = f'{bdy}.json'
            for cntp, page_jsn in enumerate(jsn_data['readResults']):
                pginfo = p2(bn_l2s, page_jsn)
                idx_before = len(elmlst)
                for node, line_jsn in enumerate(page_jsn['lines']):
                    p3(bn, line_jsn, cntp, node, elmlst, pginfo)
                    for wnode, word_jsn in enumerate(line_jsn['words']):
                        p4(bn, word_jsn, cntp, node, wnode, elmlst, pginfo)
                for k in range(idx_before, len(elmlst)):
                    label_both  = ' from PNG' if (DD.pdf2api and DD.png2api) else ''
                    elmlst[k][0] = elmlst[k][0] + label_both + f' {engine_tag}'
                    elmlst[k].append(usepng)    # index -1: usepng

def chkjsn():
    elmlst = []
    if 'vision' in DD.engines:
        _chkjsn_dir(DD.jsn_raw, 'CV', elmlst)
    if 'intelli' in DD.engines:
        _chkjsn_dir(DD.jsn_raw, 'DI', elmlst)
    return elmlst
