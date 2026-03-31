#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   go.py
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import glob

from pypdf import PdfReader

for pdf in sorted(glob.glob('*pdf')):
    print(f'{pdf} -----------------------------')
    reader = PdfReader(pdf)
    info = reader.metadata  # DocumentInformationオブジェクト
    print(f'{info}')

    if hasattr(info,'title'):
        print("title:", info.title)
    else:
        print('title: (no such attr)')

    if hasattr(info,'author'):
        print("author:", info.author)
    else:
        print('author: (no such attr)')

    if hasattr(info,'creator'):
        print("creator:", info.creator)
    else:
        print('creator: (no such attr)')

    if hasattr(info,'producer'):
        print("producer:", info.producer)
    else:
        print('producer: (no such attr)')

    try:
        if hasattr(info,'creation_date'):
                print("creation_date:", f'{info.creation_date}')
        else:
            print('creation_date: (no such attr)')
    except Exception:
        print("creation_date: (CANNOT PRINT)")


#    print("Created:", info.creation_date)


#    print("Modified:", info.modification_date)
    try:
        if hasattr(info,'modification_date'):
                print("modification_date:", f'{info.modification_date}')
        else:
            print('modification_date: (no such attr)')
    except Exception:
        print("modification_date: (CANNOT PRINT)")

