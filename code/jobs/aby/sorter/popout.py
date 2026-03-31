#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   popout.py       230411  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

from m.prnt import prnt

def popout(pdf_pg,key,fm,to):
    pdf = key  # key may be 'pdf|engine' or plain pdf
    if key not in pdf_pg:
        raise Exception(f'"{key}" not in pdf_pg')
    if fm > to:
        raise Exception(f'"{key}" fm "{fm}" > to "{to}"')
    rmv_ok = False
    for idx,lst in enumerate(pdf_pg[key]):
        [stt,end] = lst
        # 0)  ERROR                   stt > fm or to > end
        if stt > fm or end < fm:
            continue
        # 1)  [--index--]             stt < fm and to < end
        #     +----------- stt
        #     |   +------- fm         pdf_pg[key].insert(idx+1,[to+1,end])
        #     |   | +----- to         pdf_pg[key][idx] = [stt,fm-1]
        #     |   | |   +- end
        #     |   | |   |
        #     o..o| |o..o
        if stt < fm and to < end:
            pdf_pg[key][idx] = [stt,fm-1]
            pdf_pg[key].insert(idx+1,[to+1,end])
            rmv_ok = True
            break
        # 2)  [--index--]             stt == fm and to < end
        #     +----------- stt,fm
        #     |     +----- to         pdf_pg[key][idx] = [to+1,end]
        #     |     |   +- end
        #     |     |   |
        #     |     |o..o
        elif stt == fm and to < end:
            pdf_pg[key][idx] = [to+1,end]
            rmv_ok = True
            break
        # 3)  [--index--]             stt < fm and end == to
        #     +----------- stt
        #     |     +----- fm         pdf_pg[key][index] = [stt,fm-1]
        #     |     |   +- end,to
        #     |     |   |
        #     o....o|   |
        elif stt < fm and end == to:
            pdf_pg[key][idx] = [stt,fm-1]
            rmv_ok = True
            break
        # 4)  [--index--]             stt == fm and end == to
        #     +----------- stt,rm
        #     |                       pdf_pg[key].pop(idx)
        #     |         +- end,to
        #     |         |
        #     |         |
        elif stt == fm and end == to:
            pdf_pg[key].pop(idx)
            rmv_ok = True
            break
        else:
            raise Exception('logic error')
    if not rmv_ok:
        raise Exception(f'failed to remove [{fm},{to}] from pdf_pg[{pdf}] {pdf_pg[key]}')
        ##quit()
    return
