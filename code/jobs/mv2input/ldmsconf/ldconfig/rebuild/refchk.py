#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   refchk.py       230330  cy
#   ToDo            nks_nonaka エラーメール 座標参照設定部分
#   PG Bug はそのままにしてある
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import re

from m.prnt     import prnt
#from m.errconfig    import ConfigErr

def refchk(lvlo,docname):
    #
    #   anybody refers to level below => ERROR
    #
    #   top level   -> gk_A     ERROR
    #   gk_A        -> gm_A     ERROR
    #   gm_A        -> gk_A     NOT ERROR
    #   gk_A_A      -> gk_A     NOT ERROR
    #   gk_A_A      -> gm_A_A   ERROR
    #
    papas = [] # items in sp_*
    nxtpapa = None
    for lvl in range(len(lvlo)):
        #
        # build papas
        #
        if nxtpapa != None:
            papas.append(nxtpapa)
            nxtpapa = None
        for dl in lvlo[lvl].defs:
            if type(dl.rg) == str and dl.rg.startswith('gk_'):
                nxtpapa = dl.dname
            else:
                papas.append(dl.dname)
        #
        # for each dl
        #
        for dl in lvlo[lvl].defs:
            if type(dl.sp_blw) == str and dl.sp_blw[4:] not in papas:
                raise Exception(f'{docname}_dd: {dl.dname} cannto refer to {dl.sp_blw}')
            if type(dl.sp_abv) == str and dl.sp_abv[4:] not in papas:
                raise Exception(f'{docname}_dd: {dl.dname} cannto refer to {dl.sp_abv}')
            if type(dl.sp_rof) == str and dl.sp_rof[4:] not in papas:
                raise Exception(f'{docname}_dd: {dl.dname} cannto refer to {dl.sp_rof}')
            if type(dl.sp_lof) == str and dl.sp_lof[4:] not in papas:
                raise Exception(f'{docname}_dd: {dl.dname} cannto refer to {dl.sp_lof}')
    #
    #   no gm_A refers to gk_A => ERROR
    #
    for lvl in range(len(lvlo)):
        if lvl == 0:
            continue
        papa = None
        for dl in lvlo[lvl-1].defs:
            if type(dl.rg) == str and dl.rg.startswith('gk_'):
                papa = dl.dname
        if papa == None:
            raise Exception('PG BUG: no papa will never happen {docname} lv{lvl}')
        look_papa = False
        for dl in lvlo[lvl].defs:
            for sp in [dl.sp_blw, dl.sp_abv, dl.sp_rof, dl.sp_lof]:
                if type(sp) == str and sp[4:] == papa:
                    look_papa = True
                    continue
            if look_papa:
                continue
        if look_papa:
            continue ## start checking next level

        ## nobody looking to papa at this level
        lvlstr = None
        for dl in lvlo[lvl].defs:
            if dl.rg.startswith('gm_'):
                lvlstr = dl.rg

                prnt(f'''
lvlstr {lvlstr}''')

        if lvlstr == None:
            raise Exception('LOGIC ERROR, PROGRAM BUG')
        raise Exception(f'{docname} level {lvl} {lvlstr} NOT REFERRING PAPA')
    return
