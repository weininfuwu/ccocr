#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   remove_nokids.py    230316  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

def remove_nokids(board):
    dfttl = board.sum().sum()
    while True:

#        print(f'SUM {dfttl}')
#        print('==== parent count ====')
#        print(board.sum(axis='columns'))


        ser_pcnt = board.sum(axis='columns')
        nokids = list(ser_pcnt[ser_pcnt == 0].index)
        to_clear = [ f'c_{i[2:]}' for i in nokids ]
#        print(f'=== clearing {to_clear}')

        for c_zero in to_clear:
            for p_zero in board[c_zero].index:

#                board.loc[p_zero][c_zero] = 0       ## 250307 cause warning but works
                board.loc[p_zero, c_zero] = 0   # claud says
#                board.loc[c_zero, p_zero] = 0      ## 250307 DOESN'T WORD



# 
# Use `df.loc[row_indexer, "col"] = values` instead, to perform the assignment in a single step and ensure this keeps updating the original `df`.
                # df.loc[row_indexer, "col"] = values

# 
# See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
# 
#   board.loc[p_zero][c_zero] = 0

                

#        print(f'==== blank board ====')
#        print(board)
        new_dfttl = board.sum().sum()
#        print(f'SUM {new_dfttl}')

        if dfttl == new_dfttl:
            break
        dfttl = new_dfttl
#        print('========= NEXT LOOP ===========')
    if dfttl == 0:
        return True
    else:
        return False

