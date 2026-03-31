#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   btns.py         250730  cy
#   updated: 260320 add clonerow to htmlsrc
#   updated: 260320.171136 by cy
#   updated: 260321 show engine suffix in pdf cell
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import pprint

import json
import os

import openpyxl
from openpyxl.utils.cell        import column_index_from_string
from openpyxl.styles.alignment  import Alignment
from openpyxl.styles            import PatternFill

from m.prnt     import prnt
from m.env      import D
from jobs.env   import DD

def c2n(c):
    return column_index_from_string(c)

def fill_lst(lst,idx,val):
    if len(lst) - 1 >= idx:
        if lst[idx] != None:
            raise Exception(f'cannot overwrite list value: list[{idx}] {val}')
        lst[idx] = val
        return
    while len(lst) - 1 < idx:
        lst.append(None)
    lst[-1] = val
    return

def apndidx(idx,docname):
    idx_itm = f'''
<button class='btn'>
  {docname}
</button>'''
    idx += idx_itm
    return idx

def btns(dig):
    idx = f'''<!-- written by btns.py {D.jobid} -->
'''
    idx_ftr = '\n'
    ##
    ##  btns.html
    ##
    for docname in dig:
        idx = apndidx(idx,docname)
    idx += idx_ftr
    prnt(f'making btns.html\n  {DD.btnsf.replace(D.logd, "")}')
    with open(DD.btnsf,'w',encoding='utf-8') as f:
        f.write(idx)
    ##
    ##  each tab (LOAD)
    ##
    htmlsrc = {}    # htmlsrc[docname] = [ row1, row2, ... ]
                    # rowN = { 'hdr/txt/url/clonerow' : [value, ... ] }
    for docname in dig:
        if len(dig[docname]) == 0:
            continue
        htmlsrc[docname] = [ {'hdr' : [ 'doc#','pdf','page','i#' ]} ]
        #
        #   FIXED clm name
        #
        do0= dig[docname][0]
        for cnt,io in enumerate(do0.itm):
            if io.dl.clm == None:
                continue
            fill_lst(htmlsrc[docname][0]['hdr'],c2n(io.dl.clm)-1,io.dl.dname)
        #
        #   1st row         (clm name)
        #   2nd row onward  (data)
        #
        _last_engine = None
        _row_in_engine = 0
        for row,do in enumerate(dig[docname]):  # do == docObj == 1 biz doc
            # reset row counter when engine changes (CV->DI etc.)
            if do.engine != _last_engine:
                _row_in_engine = 0
                _last_engine = do.engine
            picrow   = [None,None,None,None]
            suffix   = ' '.join(filter(None, [do.engine, do.dpi, do.lvl]))
            pdf_disp = f'{do.pdf} {suffix}' if suffix else do.pdf
            txtrow   = [do.docnum,pdf_disp,do.fm,do.inum]
            clonerow = [None,None,None,None]    # True if column is clone
            for clmidx,io in enumerate(do.itm):
                if io.dl.clm == None:
                    continue
                pic = ( f"src='static/spic/{os.path.basename(io.spic)}' "
                        f"alt='{io.page}_{io.node}'")
                is_readonly = io.isclone or (not io.dl.rg and _row_in_engine > 0)
                fill_lst(picrow,   c2n(io.dl.clm)-1, pic)
                fill_lst(txtrow,   c2n(io.dl.clm)-1, io.txt)
                fill_lst(clonerow, c2n(io.dl.clm)-1, is_readonly)
            htmlsrc[docname].append({'url':      picrow})
            htmlsrc[docname].append({'txt':      txtrow})
            htmlsrc[docname].append({'clonerow': clonerow})
            _row_in_engine += 1
    srcjson = os.path.join(D.logd,'htmlsrc.json')
    with open(srcjson, 'w', encoding='utf-8') as f:
        json.dump(htmlsrc, f, indent=2, ensure_ascii=False)
    prnt(f'htmlsrc.json saved\n  {srcjson}')
    return htmlsrc
