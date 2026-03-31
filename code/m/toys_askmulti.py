#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   toys_askmulti.py    251221  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import tkinter as tk

from m.prnt import prnt
from m.env  import D

def toys_askmulti(prmpt,itmCnt,itmLen):
    message = prmpt
    root = tk.Tk()
    root.geometry('+100+100')
    root.title(D.appname)
    root.resizable(False, False)
    rtn = []
    root.protocol('WM_DELETE_WINDOW', (lambda: 'pass')())
    # TOP
    frm_top = tk.Frame(root)
    frm_top.grid(row=0, column=0, columnspan=2, sticky='w', padx=10, pady=(10,5))
    tk.Label(frm_top, text=message).pack(anchor='w')
    # 入力欄の親フレーム
    frm_inputs = tk.Frame(root)
    frm_inputs.grid(row=1, column=0, columnspan=2, sticky='w', padx=10)
    # 1列×10行の入力（幅=25）
    entries = []
    for r in range(itmCnt):
        e = tk.Entry(frm_inputs, width=itmLen)
        e.grid(row=r+1, column=0, padx=(0,10), pady=3, sticky='w')
        entries.append(e)
    entries[0].focus_set()
    def click_btn():
        rtn.clear()
        for e in entries:
            v = e.get().strip()
            if v:
                rtn.append(v)
        try:
            root.unbind('<Return>')
        except Exception:
            pass
        root.quit()
        root.destroy()
    frm_btn = tk.Frame(root)
    frm_btn.grid(row=2, column=0, columnspan=2, padx=10, pady=(5,10))
    btn = tk.Button(frm_btn, text='次へ', command=click_btn)
    btn.pack()
    root.bind('<Return>', lambda ev: btn.invoke())
    root.mainloop()
    prnt(f'rtn {rtn}')
    return rtn


