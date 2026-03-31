#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   go.py
#
#--------1---------2---------3---------4---------5---------6---------7--------#

from pdf2image import convert_from_path
from PIL import Image

# PDFを変換（imagesは「リスト」になります）
images = convert_from_path('1pg.pdf', dpi=300)

if images:
    # ★ここが重要：リストの最初の要素（1ページ目）を取り出す
    page_image = images[0]

    # 1ページ目（画像オブジェクト）に対して rotate を実行
    rotated_image = page_image.rotate(15, resample=Image.BICUBIC, expand=True)

    rotated_image.save('output.png', 'PNG')
    print("変換成功！")

