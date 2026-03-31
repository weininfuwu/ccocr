#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   b85.py
#
#--------1---------2---------3---------4---------5---------6---------7--------#


import base64

def main():
    basetext = __file__
    go_print(basetext)

    # ---- Base85（b85）エンコード：bytes を返す
    b85_object = base64.b85encode(basetext.encode("utf-8"))
    go_print(b85_object)

    # ---- Base85（b85）エンコード文字列（ASCII化）
    b85_str = base64.b85encode(basetext.encode("utf-8")).decode("ascii")
    go_print(b85_str)

    # ---- bytes を str() でキャストした見え方（b"..." 形式）
    b85_object_str_cast = str(base64.b85encode(basetext.encode("utf-8")))
    go_print(b85_object_str_cast)

    # ---- 参考：デコード（復元）
    restored = base64.b85decode(b85_object).decode("utf-8")
    go_print(restored)

def go_print(printdata):
    print("GP: ----- ----- -----")
    print(type(printdata))
    print(printdata)

if __name__ == "__main__":
    main()

