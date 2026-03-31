#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   chkfont.py
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import glob

# -*- coding: utf-8 -*-
"""
PDF内のフォントエンコーディング（CMap名: /90ms-RKSJ-H 等）を列挙するスクリプト
- 依存: pip install pypdf
"""

from pypdf import PdfReader
from pypdf.generic import IndirectObject
from typing import Any, Dict, Set


def _dereference(obj: Any) -> Any:
    """間接参照（IndirectObject）を安全に解決"""
    if isinstance(obj, IndirectObject):
        return obj.get_object()
    return obj

def _name(obj: Any) -> str:
    """NameObject等を文字列に正規化（例：/90ms-RKSJ-H -> '90ms-RKSJ-H'）"""
    obj = _dereference(obj)
    if hasattr(obj, "name") and isinstance(obj.name, str):
        return obj.name.lstrip("/")  # '/Identity-H' -> 'Identity-H'
    if isinstance(obj, str):
        return obj.lstrip("/")
    return str(obj)

def list_font_encodings(pdf_path: str) -> Dict[int, Set[str]]:
    """
    各ページで検出した CMap/Encoding 名の集合を返す。
    返り値: {ページ番号(0-based): {'90ms-RKSJ-H', 'Identity-H', ...}}
    """
    reader = PdfReader(pdf_path)
    page_to_encodings: Dict[int, Set[str]] = {}

    for i, page in enumerate(reader.pages):
        encodings: Set[str] = set()

        # /Resources → /Font を辿る
        resources = _dereference(page.get("/Resources"))
        if not resources:
            page_to_encodings[i] = encodings
            continue

        fonts = _dereference(resources.get("/Font"))
        if not fonts:
            page_to_encodings[i] = encodings
            continue

        # Font辞書内の各フォントエントリを走査
        for font_key, font_ref in fonts.items():
            font_dict = _dereference(font_ref)
            if not hasattr(font_dict, "get"):
                continue

            subtype = _name(font_dict.get("/Subtype"))
            basefont = _name(font_dict.get("/BaseFont"))
            encoding = font_dict.get("/Encoding")

            # Type0フォントの場合、/Encoding が CMap 名 (NameObject) であることが多い
            cmap_name = None
            if encoding is not None:
                cmap_name = _name(encoding)

            # Type0 でなくても、親 Type0 の /DescendantFonts 側に情報があるケースあり
            # 参考までに DescendantFonts も覗く
            if subtype == "Type0":
                desc = _dereference(font_dict.get("/DescendantFonts"))
                if isinstance(desc, list) and desc:
                    cid_font = _dereference(desc[0])
                    # CIDSystemInfo などを使って補助情報を拾いたい場合はここで処理
                    # ただし CMap名は通常 Type0 の /Encoding に載るためここでは省略

            # 収集
            if cmap_name:
                encodings.add(cmap_name)

            # 参考: ベースフォント名やSubtypeも一緒に出したい場合（ロギング用途）
            # print(f"Page {i+1} | Font {font_key}: Subtype={subtype}, BaseFont={basefont}, Encoding={cmap_name}")

        page_to_encodings[i] = encodings

    return page_to_encodings


def caller(pdf_path):
    result = list_font_encodings(pdf_path)
    for page_index, encs in result.items():
        page_no = page_index + 1
        if encs:
            print(f"[Page {page_no}] Encodings: {sorted(encs)}")
        else:
            print(f"[Page {page_no}] Encodings: (none or not found)")

for pdf in sorted(glob.glob('*pdf')):
    print('-------------------------------------------')
    print(pdf)
    caller(pdf)
