#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   b64.py
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import base64

def main():
    basetext = __file__
    go_print(basetext)
    base64_object = base64.b64encode(basetext.encode())
    go_print(base64_object)
    base64object_decode = base64.b64encode(basetext.encode()).decode('ascii')
    go_print(base64object_decode)
    base64_object_str_cast = str(base64.b64encode(basetext.encode()))
    go_print(base64_object_str_cast)

def go_print(printdata):
    print("GP: ----- ----- -----")
    print(type(printdata))
    print(printdata)

if __name__ == "__main__":
    main()
