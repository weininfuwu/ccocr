#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   rmv_overwrap.py     230615  cy
#   do.dname → do.docname
#   quitコメントアウト      230711 nks_nonaka
#
#--------1---------2---------3---------4---------5---------6---------7--------#

from m.prnt     import prnt

T       = 0    # Threshold
sidx    = 0    # sequence
tidx    = 4    # pg_top
bidx    = 5    # pg_btm
lidx    = 8
ridx    = 9
cidx    = 14   # confidence
txtidx  = 2    # txt (for debug)
diffpoint = 8  

def log_nidx(do,io,lst,idx,nidx):
    L1 = f'OVERWRAP: {do.docname} "{do.pdf}" {do.inum} {io.page} {io.dl.dname}'
    L2 = (  f'remain T {lst[idx][tidx]} B {lst[idx][bidx]} '
            f'L {lst[idx][lidx]} R {lst[idx][ridx]} {lst[idx][cidx]:.3f} '
            f'"{lst[idx][txtidx]}"' )
    L3 = (  f'REMOVE T {lst[nidx][tidx]} B {lst[nidx][bidx]} '
            f'L {lst[nidx][lidx]} R {lst[nidx][ridx]} {lst[nidx][cidx]:.3f} '
            f'"{lst[nidx][txtidx]}"' )
    prnt(f'''
    {L1}
    {L2}
    {L3}''')
    return

def log_idx(do,io,lst,idx,nidx):

    L1 = f'OVERWRAP: {do.docname} "{do.pdf}" {do.inum} {io.dl.dname}'
    L2 = (  f'remain T {lst[nidx][tidx]} B {lst[nidx][bidx]} '
            f'L {lst[nidx][lidx]} R {lst[nidx][ridx]} {lst[nidx][cidx]:.3f} '
            f'"{lst[nidx][txtidx]}"' )
    L3 = (  f'REMOVE T {lst[idx][tidx]} B {lst[idx][bidx]} '
            f'L {lst[idx][lidx]} R {lst[idx][ridx]} {lst[idx][cidx]:.3f} '
            f'"{lst[idx][txtidx]}"' )
    prnt(f'''
    {L1}
    {L2}
    {L3}''')
    return

def rmv_overwrap(do,io):
    lst  = io.regrtn
    ####    overwrapped item to be poped out from io.regrtn ####
    idx  = 0
    while idx < len(lst):
        seq = lst[idx][sidx]
        top = lst[idx][tidx]
        btm = lst[idx][bidx]
        lft = lst[idx][lidx]
        ryt = lst[idx][ridx]
        cnf = lst[idx][cidx]
        cand = []
        nidx = idx + 1
        papa_lost = False
        while nidx < len(lst):
            nseq = lst[nidx][sidx]
            ntop = lst[nidx][tidx]
            nbtm = lst[nidx][bidx]
            nlft = lst[nidx][lidx]
            nryt = lst[nidx][ridx]
            ncnf = lst[nidx][cidx]
            ## out of scope: PG BUG
            if  ntop < top or ( ntop == top and nlft < lft ):
                # SQL has 'ORDER BY pg_top, lft'
                raise Exception(f'''PG BUG (250327)
 ntop {ntop}
 top  {top}
 nlft {nlft}
 lft  {lft}''')
#                prnt('PG BUG')
#                quit()  # 250224 cy
            difftop = top - ntop
            diffbtm = btm - nbtm
            difflft = lft - nlft
            diffryt = ryt - nryt

            if abs(difftop) <= diffpoint and abs(diffbtm) <= diffpoint and abs(difflft) <= diffpoint and abs(diffryt) <= diffpoint:
                if(cnf > ncnf):
                    log_nidx(do,io,lst,idx,nidx)
                    lst.pop(nidx)
                    continue # poped & nidx unch -> see next item
                elif(cnf < ncnf):
                    papa_lost = True
                    log_idx(do,io,lst,idx,nidx)
                    lst.pop(idx)
                    break
                elif(seq > nseq):   ## same conf, use sequence
                    papa_lost = True
                    log_idx(do,io,lst,idx,nidx)
                    lst.pop(idx)
                    break
                else:
                    log_nidx(do,io,lst,idx,nidx)
                    lst.pop(nidx)
                    continue # poped & nidx unch -> see next item

            # if not (btm <= ntop or ryt <= nlft):
            #     if(cnf > ncnf):
            #         log_nidx(do,io,lst,idx,nidx)
            #         lst.pop(nidx)
            #         prnt('消した1')
            #         continue # poped & nidx unch -> see next item
            #     elif(cnf < ncnf):
            #         papa_lost = True
            #         log_idx(do,io,lst,idx,nidx)
            #         lst.pop(idx)
            #         prnt('消した2')
            #         break
            #     elif(seq > nseq):   ## same conf, use sequence
            #         papa_lost = True
            #         log_idx(do,io,lst,idx,nidx)
            #         lst.pop(idx)
            #         prnt('消した3')
            #         break
            #     else:
            #         log_nidx(do,io,lst,idx,nidx)
            #         lst.pop(nidx)
            #         prnt('消した4')
            #         nidx = 1
            #         continue # poped & nidx unch -> see next item
            ## no overwrap
            nidx += 1
        ## break comes here
        if not papa_lost:
            idx += 1
    return
