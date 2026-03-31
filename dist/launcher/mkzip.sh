#!/bin/bash
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 :
#
# mkzip.sh   260316 cy
#
#--------1---------2---------3---------4---------5---------6---------7---------8

set -e
OUT=ccocr.zip

rm -f "$OUT"

zip -r "$OUT" \
    code/jobs/ \
    code/m/ \
    code/main.py \
    code/mymail.ps1

# poppler はカラフォルダとして追加
zip "$OUT" code/poppler/

echo "created: $OUT"
