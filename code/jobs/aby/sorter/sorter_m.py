#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   sorter_m.py     230411  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import pprint

from m.prnt     import prnt
from .pgrangematch  import pgrangematch

def pp(x):
    return pprint.pformat(x, indent=2)

def sorter_m(docname,sobj,pdf_pg):
    prnt(f'start "{docname}"\n{pp(pdf_pg)}')
    for key in pdf_pg:
        pdf = key.split('|')[0]  # key = 'pdf|engine|usepng'
        checked = set()
        idx = 0
        while True:
            if len(pdf_pg[key]) == 0:
                prnt('len(pdf_pg[key]==0, go next pdf')
                break
            if idx > len(pdf_pg[key]) - 1:
                prnt(f'all pages checked, go next pdf')
                break
            fmto = pdf_pg[key][idx]
            [fm,to] = fmto
            chknow = set(list(range(fm,to+1)))
            if chknow <= checked:
                prnt(f'skip check as all page in pdf_pg[key][idx] checked')
                idx += 1
                continue
            prnt(f'checking {fmto} / {pdf_pg[key]}\n  {docname} {pdf}')
            pgrangematch(docname,pdf,fmto,sobj,pdf_pg,key) # does mark, popout
            checked = checked.union(set(list(range(fm,to+1))))
    prnt(f'finish all pdf for "{docname}"\n{pp(pdf_pg)}')

'''

    +++ NEW 250415 cy +++
    マルチページ文書仕訳設定ルール
    hd  header page  必須
    md  midium page  任意 (３ページ超があり得る場合必須）
    ft  footer page  必須

    hd,md,md,md,ft
        一般形（ページ数３ページ超）
    hd,ft
        ページ数２ページの場合
    hd+ft
        ページ数１ページの場合

    +++ OLD +++
    マルチページ文書仕訳設定ルール
    hd  header page  必須
    md  midium page  任意
    ft  footer page  任意 (md ある場合は必須)

    hd のみ定義の場合
        hd が見つかったページから pdf の最後まで全部その文書
    ft ある場合
        hd - ft がその文書
    md ある場合
        hd+1 から ft-1 までのすべてが md でないとダメ
        (hd ft は検査対象外)

    ※SP_abv 参照は hd md ft それぞれ内部に閉じていなければ書式エラー



'''

