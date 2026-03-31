#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   chkjsn_chk.py
#
#--------1---------2---------3---------4---------5---------6---------7--------#


def chk(val,tobe,msg):
    if val != tobe:
        raise Exception(msg)
    return
