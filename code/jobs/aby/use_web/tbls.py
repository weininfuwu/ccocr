#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   tbls.py     250801  cy
#   updated: 260320 handle clonerow, fix img tag, add data-papa
#   updated: 260321 suppress spic for clone rows
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import os

from m.prnt     import prnt
from m.env      import D
from jobs.env   import DD

def tbls(htmlsrc):

    html = f'<!-- tables.html written by tbls.py {D.jobid} -->'

    for doc in htmlsrc:
        html += f"\n<table id='{doc}'>"

        entries = htmlsrc[doc]
        # entries[0]            = {'hdr': [...]}
        # entries[1+i*3+0]      = {'url': [...]}
        # entries[1+i*3+1]      = {'txt': [...]}
        # entries[1+i*3+2]      = {'clonerow': [...]}

        html += '\n<thead>'
        html += "\n<tr class='hdr'>"
        for itm in entries[0]['hdr']:
            html += f'\n  <th>{itm if itm is not None else ""}</th>'
        html += '\n</tr>'
        html += '\n</thead>'
        html += '\n<tbody>'

        row_count = (len(entries) - 1) // 3
        for ri in range(row_count):
            url_row   = entries[1 + ri*3 + 0]['url']
            txt_row   = entries[1 + ri*3 + 1]['txt']
            clone_row = entries[1 + ri*3 + 2]['clonerow']

            # image row
            html += '\n<tr class="img-row">'
            html += '\n  <th></th><th></th><th></th><th></th>'
            for ci, itm in enumerate(url_row):
                if ci < 4:
                    continue
                is_clone = clone_row[ci] if ci < len(clone_row) else False
                if itm is None or is_clone:
                    html += '\n  <td></td>'
                else:
                    html += f'\n  <td><img {itm} /></td>'
            html += '\n</tr>'

            # text row
            html += "\n<tr class='txt'>"
            for ci, itm in enumerate(txt_row):
                itm = '' if itm is None else itm
                is_clone = clone_row[ci] if ci < len(clone_row) else False
                if ci < 4:
                    html += f'\n  <th>{itm}</th>'
                elif is_clone:
                    # clone cell: editable but linked to papa (row 0 of same col)
                    html += (f'\n  <td>'
                             f'<input value="{itm}" data-clone="true" readonly tabindex="-1" />'
                             f'</td>')
                else:
                    html += f'\n  <td><input value="{itm}" /></td>'
            html += '\n</tr>'

        html += '\n</tbody>'
        html += '\n</table>'

    prnt(f'making tables.html\n  {DD.tblsf}')
    with open(DD.tblsf, 'w', encoding='utf-8') as f:
        f.write(html)

    return
