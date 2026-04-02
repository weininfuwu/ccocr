#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   askcred.py      250204  cy
#   updated: 260321 add DI key/ep fields
#   updated: 260330 --cv / --di args: show only needed fields
#
#--------1---------2---------3---------4---------5---------6---------7--------#
'''

    THIS CODE IS NOT ORPHAN
    kicked by cred.py / cred_all()

'''

import argparse
import json
import tkinter as tk

parser = argparse.ArgumentParser()
parser.add_argument('--cv', action='store_true')
parser.add_argument('--di', action='store_true')
args    = parser.parse_args()
need_cv = args.cv
need_di = args.di
if not need_cv and not need_di:     # 引数なし → 両方表示（フォールバック）
    need_cv = need_di = True

def make_toggle(ent):
    def handler(ev):
        if ev.widget['text'] == 'みる':
            ev.widget['text'] = '隠す'
            ent['show'] = ''
        else:
            ev.widget['text'] = 'みる'
            ent['show'] = '*'
    return handler

def add_field(root, label_text, show='*'):
    frm_lbl = tk.Frame(root)
    frm_lbl.pack(anchor=tk.W, padx=(10,10))
    tk.Label(frm_lbl, text=label_text).pack(side=tk.LEFT)
    frm = tk.Frame(root)
    frm.pack(anchor=tk.W, padx=(10,10))
    ent = tk.Entry(frm, width=100, show=show)
    ent.pack(side=tk.LEFT)
    btn = tk.Button(frm, text='みる')
    handler = make_toggle(ent)
    btn.bind('<1>',      handler)
    btn.bind('<space>',  handler)
    btn.bind('<Return>', handler)
    btn.pack(side=tk.LEFT, padx=(10,0))
    return ent

ent_cv_key = ent_cv_ep = ent_di_key = ent_di_ep = None

def click_btm(ev):
    rtn = {
        'key'    : ent_cv_key.get() if ent_cv_key else '',
        'ep'     : ent_cv_ep.get()  if ent_cv_ep  else '',
        'di_key' : ent_di_key.get() if ent_di_key else '',
        'di_ep'  : ent_di_ep.get()  if ent_di_ep  else '',
    }
    print(json.dumps(rtn, ensure_ascii=False), end='')
    quit()

root = tk.Tk()
root.geometry('+100+100')
root.title('ccocr：資格情報の保存')
root.protocol('WM_DELETE_WINDOW', (lambda: 'pass')())

## TOP
frm_top = tk.Label(root).pack()
tk.Label(frm_top, text=(
    '\nこの Windows の「資格情報ストア」に課金キー等を保存します。\n'
    '「課金キー」が不明な場合は、取説を参照ください。\n\n'
    'タイプミスした場合、訂正がとても面倒なので慎重にねがいますm(_ _)m'
    )).pack()

## CV
if need_cv:
    tk.Label(root, text='── Computer Vision ──', anchor=tk.W).pack(
        anchor=tk.W, padx=(10,10), pady=(6,0))
    ent_cv_key = add_field(root, 'CV 課金キー')
    ent_cv_key.focus_set()
    ent_cv_ep  = add_field(root, 'CV エンドポイント')

## DI
if need_di:
    tk.Label(root, text='── Document Intelligence ──', anchor=tk.W).pack(
        anchor=tk.W, padx=(10,10), pady=(6,0))
    ent_di_key = add_field(root, 'DI 課金キー')
    if not need_cv:
        ent_di_key.focus_set()
    ent_di_ep  = add_field(root, 'DI エンドポイント')

## BTM
frm_btm = tk.Frame(root)
frm_btm.pack(anchor='center', padx=(10,10), pady=(10,10))
btn_btm = tk.Button(frm_btm, text='保存する')
btn_btm.bind('<1>',      click_btm)
btn_btm.bind('<space>',  click_btm)
btn_btm.bind('<Return>', click_btm)
btn_btm.pack(padx=(10,0))
##
tk.mainloop()
