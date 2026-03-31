#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   testcode.py     260322  cy
#
#   Usage:
#       python testcode.py <pdf_path> [dpi]
#
#   For a bad-font PDF, compare:
#       1) pdftoppm  (current)        -> out_toppm/
#       2) pdftocairo                 -> out_cairo/
#
#   Check which produces readable text in the PNG.
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import os
import sys
import shutil

from pdf2image   import convert_from_path
from pypdf       import PdfReader
from pypdf.generic import IndirectObject

# ---------------------------------------------------------------------------
# bad font detection (standalone, no project imports)
# ---------------------------------------------------------------------------

BAD_FONTS = {'90ms-RKSJ-H', 'UniJIS-UCS2-H'}

def _deref(obj):
    if isinstance(obj, IndirectObject):
        return obj.get_object()
    return obj

def _enc_name(obj):
    if obj is None:
        return ''
    obj = _deref(obj)
    if hasattr(obj, 'name'):
        raw = obj.name
        if isinstance(raw, bytes):
            try:
                return raw.decode('shift_jis', errors='replace').lstrip('/')
            except Exception:
                return str(raw).lstrip('/')
        return str(raw).lstrip('/')
    return str(obj).lstrip('/')

def check_fonts(pdf_path):
    """Return {page_no: set_of_encodings}"""
    reader = PdfReader(pdf_path, strict=False)
    result = {}
    for i, page in enumerate(reader.pages):
        encs = set()
        resources = _deref(page.get('/Resources'))
        if not resources:
            result[i+1] = encs
            continue
        fonts = _deref(resources.get('/Font'))
        if not fonts:
            result[i+1] = encs
            continue
        for fkey, fref in fonts.items():
            fd = _deref(fref)
            if not hasattr(fd, 'get'):
                continue
            enc = _enc_name(fd.get('/Encoding'))
            bf  = _enc_name(fd.get('/BaseFont'))
            sub = _enc_name(fd.get('/Subtype'))
            if enc:
                encs.add(enc)
            print(f'  p{i+1} {fkey}: {sub} / {bf} / enc={enc}')
        result[i+1] = encs
    return result

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print('Usage: python testcode.py <pdf_path> [dpi]')
        sys.exit(1)

    pdf_path = sys.argv[1]
    dpi      = int(sys.argv[2]) if len(sys.argv) >= 3 else 200
    bn       = os.path.basename(pdf_path)

    print(f'\n--- font check: {bn} ---')
    enc_map  = check_fonts(pdf_path)
    bad_encs = set()
    for pg, encs in enc_map.items():
        found = encs & BAD_FONTS
        status = f'BAD: {sorted(found)}' if found else 'ok'
        print(f'  page {pg}: {sorted(encs)}  -> {status}')
        bad_encs |= found

    if not bad_encs:
        print('No bad fonts found. Exiting.')
        sys.exit(0)

    print(f'\nBad fonts detected: {sorted(bad_encs)}')
    print(f'Comparing pdftoppm vs pdftocairo at {dpi} dpi ...\n')

    out_toppm = 'out_toppm'
    out_cairo = 'out_cairo'
    for d in [out_toppm, out_cairo]:
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d)

    # --- pdftoppm (current method) ---
    print('--- pdftoppm ---')
    pages = convert_from_path(
        pdf_path, dpi=dpi, use_cropbox=True,
        use_pdftocairo=False)
    for i, pg in enumerate(pages):
        fn = os.path.join(out_toppm, f'{bn}.{i+1:02}.png')
        pg.save(fn)
        print(f'  saved: {fn}')

    # --- pdftocairo ---
    print('--- pdftocairo ---')
    pages = convert_from_path(
        pdf_path, dpi=dpi, use_cropbox=True,
        use_pdftocairo=True)
    for i, pg in enumerate(pages):
        fn = os.path.join(out_cairo, f'{bn}.{i+1:02}.png')
        pg.save(fn)
        print(f'  saved: {fn}')

    print(f'''
Done.
  {out_toppm}/  <- pdftoppm result
  {out_cairo}/  <- pdftocairo result

Open both and compare text rendering.
If pdftocairo shows readable text, use use_pdftocairo=True for bad-font PDFs.
''')

if __name__ == '__main__':
    main()
