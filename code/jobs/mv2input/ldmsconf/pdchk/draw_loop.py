#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   draw_loop.py    230316  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

def draw_loop(board):
#    print(board)
    chain = []
    for i in range(len(board)):
        name_p = board.iloc[i].name
        for name_c, val in board.iloc[i].items():
            if val != 0:
                chain.append(f'{name_p[2:]}->{name_c[2:]}')
    chain = ', '.join(chain)
    return chain
