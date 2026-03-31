#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   read_pypdf.py
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import glob

from pypdf import PdfReader

for pdf in sorted(glob.glob('mtl_mitMAT_*pdf')):
    print('-----------------------------------')
    print(pdf)

    reader = PdfReader(pdf)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    print(text)
