#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   encChk.py   260125  cy
#   updated: 260322 add UniJIS-UCS2-H to bad font list
#   updated: 260323.084924 by cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import os
from typing import Any, Dict, Set

from pypdf.generic  import IndirectObject

from m.prnt         import prnt
from m.env          import D
from jobs.env       import DD
from .mojibake      import config, MojibakeFixer
from .pdf_analyzer  import PDFAnalyzer

# encodings that cause character loss when PNG-converted and sent to API
BAD_FONTS = {'90ms-RKSJ-H', 'UniJIS-UCS2-H'}

def _dereference(obj: Any) -> Any:
    """間接参照を解決（互換性用）"""
    if isinstance(obj, IndirectObject):
        return obj.get_object()
    return obj

def _name(obj: Any) -> str:
    """文字列に正規化（互換性用）"""
    if obj is None:
        return ""
    obj = _dereference(obj)
    if hasattr(obj, "name"):
        name_obj = obj.name
        if isinstance(name_obj, bytes):
            try:
                raw_str = name_obj.decode('shift_jis', errors='replace')
            except:
                raw_str = str(name_obj)
        else:
            raw_str = str(name_obj)
    elif isinstance(obj, str):
        raw_str = obj
    else:
        raw_str = str(obj)
    return MojibakeFixer.fix(raw_str, "legacy_name_function").lstrip("/")

def list_font_encodings(pdf_path: str) -> Dict[int, Set[str]]:
    """各ページで検出したエンコーディング名の集合を返す（互換性維持）"""
    analyzer = PDFAnalyzer(pdf_path)
    page_to_encodings: Dict[int, Set[str]] = {}
    for i, page in enumerate(analyzer.reader.pages):
        encodings: Set[str] = set()
        resources = _dereference(page.get("/Resources"))
        if not resources:
            page_to_encodings[i] = encodings
            continue
        fonts = _dereference(resources.get("/Font"))
        if not fonts:
            page_to_encodings[i] = encodings
            continue
        for font_key, font_ref in fonts.items():
            font_dict = _dereference(font_ref)
            if not hasattr(font_dict, "get"):
                continue
            subtype  = _name(font_dict.get("/Subtype",  ""))
            basefont = _name(font_dict.get("/BaseFont", ""))
            encoding = font_dict.get("/Encoding")
            cmap_name = _name(encoding) if encoding is not None else None
            if cmap_name:
                encodings.add(cmap_name)
        page_to_encodings[i] = encodings
    return page_to_encodings

def caller(pdf_path: str) -> tuple:
    """従来のcaller関数（互換性維持）
    Returns (rslt, page_to_encodings)
    """
    result = list_font_encodings(pdf_path)
    bn     = os.path.basename(pdf_path)
    rslt   = []
    for page_index, encs in result.items():
        page_no = page_index + 1
        if encs:
            prnt(f"[{bn} pg {page_no}] Encodings: {sorted(encs)}")
            rslt.append(False if encs & BAD_FONTS else True)
        else:
            prnt(f"[{bn} pg {page_no}] Encodings: (none or not found)")
            rslt.append(True)
    rslt = [False, rslt] if False in rslt else [True, rslt]
    return rslt, result

def encChk(pdf: str) -> list:
    """メイン関数（従来のインターフェース維持）"""
    bn  = os.path.basename(pdf)
    prnt(f'checking "{bn}"')

    rslt, enc_map = caller(pdf)
    prnt(f'result {rslt}')
    if rslt[0] == False:
#        bn  = os.path.basename(pdf)
        prnt(f'adding to DD.skipPdf "{bn}"')
        DD.skipPdf.append(bn)
        bad = set()
        for encs in enc_map.values():
            bad |= (encs & BAD_FONTS)
        DD.skipPdfEnc[bn] = bad
#    prnt(f'skippdf {DD.skipPdf}')
    return rslt

if __name__ == "__main__":
    from .ext import main
    main()
