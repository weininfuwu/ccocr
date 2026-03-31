#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   load2docdef.py      230330  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

from m.prnt     import prnt

from .clm_resub import clm,rdl

def load2docdef(resub,docdef):
    for docname in resub:
        for lst in resub[docname]:
            o = rdl(lst)


            lvl = docdef[docname]
            found = False
            while not found:
                for i in lvl.defs:
                    if i.dname == lst[clm.dname]:
                        i.resub.append(o)
                        found = True
                        break
                lvl = lvl.child

#    ##### debug code ####
#    for docname in docdef:
#        lvl = docdef[docname]
#        while lvl != None:
#            for dl in lvl.defs:
#                print(f'{docname} {dl.dname}')
#                if dl.resub != []:
#                    for ro in dl.resub:
#                        print(f'  {ro.ptn} {ro.rpl} {ro.cnt} {ro.flg}')
#            lvl = lvl.child
#
#    prnt('quit')
#    quit()
    return
