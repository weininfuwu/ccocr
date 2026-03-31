#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   zipenc.py
#
#--------1---------2---------3---------4---------5---------6---------7--------#



import base64, zlib

def main():
    basetext = __file__
    go_print(basetext)

    # 1) そのまま b85
    b85_raw = base64.b85encode(basetext.encode("utf-8"))
    go_print(b85_raw)

    # 2) zlib で圧縮してから b85
    comp = zlib.compress(basetext.encode("utf-8"), level=9)
    b85_comp = base64.b85encode(comp)
    go_print(b85_comp)

    # 3) 短いほうを採用（文字列化）
    best = min((b85_raw, b85_comp), key=len).decode("ascii")
    go_print(best)

    # 4) 復元（採用が圧縮版だったかどうかで分岐）
    restored = try_decode(best)
    go_print(restored)

def try_decode(s: str) -> str:
    """圧縮版か非圧縮版か分からない b85 文字列を復元"""
    data = base64.b85decode(s.encode("ascii"))
    # zlib 圧縮ならヘッダ 0x78 が多い（必須ではない）
    try:
        return zlib.decompress(data).decode("utf-8")
    except zlib.error:
        return data.decode("utf-8")

def go_print(printdata):
    print("GP: ----- ----- -----")
    print(type(printdata))
    print(printdata)

if __name__ == "__main__":
    main()

