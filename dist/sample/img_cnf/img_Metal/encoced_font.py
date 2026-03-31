#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   encoced_font.py
#
#--------1---------2---------3---------4---------5---------6---------7--------#


import PyPDF2

def check_pdf_encodings(pdf_path):
    """PDFのエンコーディングを確認"""
    with open(pdf_path, 'rb') as f:
        pdf = PyPDF2.PdfReader(f)
        
        for i, page in enumerate(pdf.pages):
            print(f"\nPage {i+1}:")
            if '/Resources' in page and '/Font' in page['/Resources']:
                fonts = page['/Resources']['/Font']
                for font_name, font_obj in fonts.items():
                    if '/Encoding' in font_obj:
                        encoding = font_obj['/Encoding']
                        if hasattr(encoding, 'get_object'):
                            encoding = encoding.get_object()
                        print(f"  Font: {font_name}, Encoding: {encoding}")
                    
                    # 埋め込みフォントか確認
                    if '/FontDescriptor' in font_obj:
                        print(f"  - Embedded font: Yes")
                    else:
                        print(f"  - Embedded font: No (system font required)")
