#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   rebuild.py  230323  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

from ..clm import clm as Clm
from ..clm import dl
from .fillobj   import fillobj
from .refchk    import refchk

from m.prnt import prnt


def rebuild(docdef):
    for docname in docdef:
        ## docname = _dd sheet
        dlines = []
        for dline in docdef[docname]:   ## docdef[docname] : 2dim list
            dlines.append(dl(dline))    ## dlines          : list of 'dl' obj
        ##
        ## build level queue as 'lvlq'
        ##                                  lvlo (level object)
        ## [ lvlo,        lvlo ... ]        lvlo.defs   : list of dl obj
        ##   TOP level -> 2nd level         lvlo.child  : None / list of dl obj
        ##
        lvlq = []
        depth = 1
        while True:
            lvlo = fillobj(dlines,depth)
            if lvlo == False:
                break
            lvlq.append(lvlo)
            depth += 1
        ##
        ##  reference chk   at least one gm_ must have reference to
        ##                  gk_ item of upper level
        ##
        refchk(lvlq,docname)
        ##
        ##  connect level objects in level queue
        ##
        ##  1) [lv1,lv2,lv3,lv4]
        ##
        ##  2) [lv1,lv2,lv3]
        ##               |
        ##               +-(child)-lv4
        ##  3) [lv1,lv2]
        ##           |
        ##           +-(child)-lv3
        ##                      |
        ##                      +-(child)-lv4
        ##
        ##  4) [lv1]
        ##       |
        ##       +-(child)-lv2
        ##                  |
        ##                  +-(child)-lv3
        ##                             |
        ##                             +-(child)-lv4
        ##
        while len(lvlq) > 1:
            lvlo_tail = lvlq.pop(-1)
            lvlq[-1].child = lvlo_tail
        ##
        ##  replace docdef content
        ##
        docdef[docname] = lvlq[0]
    return
