#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   nxtdic2locdic.py    230529  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

#from m.env import misc
from m.prnt import prnt

def nxtdic2locdic(dos):
    keys = list(dos[0].nxtdic.keys())
    dos[-1].lastins = True
    #
    #   fill TPN_ BTN_
    #
    idx = 0
    while idx + 1 < len(dos):
        for k in dos[idx+1].nxtdic:
            dos[idx].locdic[k] = dos[idx+1].nxtdic[k]
        dos[idx].ngktop = dos[idx+1].gktop
        dos[idx].ngkbtm = dos[idx+1].gkbtm
        idx += 1
    #
    #   clear nextdic
    #
    for idx in range(len(dos)):
        dos[idx].nxtdic = {}
