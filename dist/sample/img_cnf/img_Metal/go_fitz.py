#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   go_fitz.py
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import glob

import fitz  # PyMuPDF

for pdf in sorted(glob.glob('*pdf')):
    print(f'{pdf} -----------------------------')
    doc = fitz.open(pdf)

    # メタデータの表示
    metadata = doc.metadata
    print(metadata)

    for k in metadata:
        print(f'{k} {metadata[k]}')

#    # 特定の項目にアクセス
#    print(f"タイトル: {metadata['title']}")
#    print(f"作成者: {metadata['author']}")
#    print(f"作成日時: {metadata['creationDate']}")

