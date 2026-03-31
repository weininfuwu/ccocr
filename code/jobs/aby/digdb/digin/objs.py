#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   objs.py 230425  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

#from m.env import misc
from ....env import DD

'''
    # dig == everythin obtained by digin() using msconfig
    dig[docname]    = [ docObj, ... ]       # each biz-document
                                            # if has rg:
                                            #   #biz-doc = #instance
                        # one docOjb  == one document (multi/single)
                        #                expanded by each line

    # docObj == info of one document (cloned in rg doc)
    docObj.itm      = [ itmObj, ... ]
    docObj.locdic   = {}                    # location dic
    docObj.nxtdic   = {}                    # temp location dic for TPN_ BTN_
    docObj.inum     = None / inscance count
    docObj.pgtop    = misc.tb_exp * fm
    docObj.pgbtm    = misc.tb_exp * (to+1)
    docObj.hdbtm    = filled/updated by htbtm_fttop()
    docObj.fttop    = filled/updated by htbtm_fttop()
    docObj.gktop    = top of deepest level gk_
    docObj.gkbtm    = btm of deepest lever gk_
    docObj.ngktop   = gktop of next instance
    docObj.ngkbtm   = gkbtm of next instance
    docObj.nomore   if True, no more deeper level
    docObj.lastins  if True, this is the last instance
    docObj.oid      just in case, reserver id(docObj) on create or deepcopy
'''

class docObj:
    def __init__(self,docname,pdf,fm,to,docnum,ddObj):
        self.docname    = docname
        self.pdf        = pdf
        self.fm         = fm
        self.to         = to
        self.docnum     = docnum
        self.itmcnt     = ddObj.defitms     ## ttl count of items
        self.itm        = []
        self.locdic     = {}
        self.nxtdic     = {}
        self.inum       = None

#        self.pgtop      = misc.tb_exp * fm
#        self.pgbtm      = misc.tb_exp * (to+1)

        self.pgtop      = DD.tb_exp * fm
        self.pgbtm      = DD.tb_exp * (to+1)

        self.hdbtm      = None  # updated at hdbtm_fttop()
        self.fttop      = None  # updated at hdbtm_ftttop()
        self.gktop      = None  # set at hdbtm_fttop()
        self.gkbtm      = None  # set at hdbtm_fttop()
        self.ngktop     = None  # set at nxtdic2locdic()
        self.ngkbtm     = None  # set at nxtdic2locdic()
        self.nomore     = False
        self.lastins    = False
        self.oid        = None  # objece id
        self.engine     = ''    # 'CV' or 'DI', set at digdb()
        self.dpi        = ''    # '2d'/'3d'/'4d'/'nd', set at digdb()
        self.lvl        = ''    # 'lv0'-'lv3'/'lvn', set at digdb()

'''
         one itmObj == one line in _dd sheet

    ## values from dl object (definition line)
    itmObj.dl.dname
    itmObj.dl.clm
    itmObj.dl.sp_blw
    itmObj.dl.of_blw
    itmObj.dl.sp_abv
    itmObj.dl.of_abv
    itmObj.dl.sp_rof
    itmObj.dl.of_rof
    itmObj.dl.sp_lof
    itmObj.dl.of_lof
    itmObj.dl.reg       <- originally dl.val
    itmObj.dl.grptgt    <- originally dl.tgt
    itmObj.dl.dtyp
    itmObj.dl.pos
    itmObj.dl.op
    itmObj.dl.rg
    itmObj.dl.resub
    ## values obtained by digin()
    itmObj.seq      = None / seq of captured text -> make mini pic
    itmObj.node     = None / node of captured text
    itmObj.txt      = None / claptured text
    itmObj.page
    itmObj.pgtop
    itmObj.pgbtm
    itmObj.hdbtm
    itmObj.fttop
    itmObj.gktop
    itmObj.gkbtm
    itmObj.top
    itmObj.btm
    itmObj.lft
    itmObj.ryt
    itmObj.otop , obtm, olft, oryt
    itmObj.spic         # job folder 起点のミニ画像へのパス or None
                        # f'spic/{seq}.png'
    itmObj.sqltxt       # 発行したSQL
    itmObj.sqlarg       # 発行したSQLの引数
    itmObj.sqlrtn       # SQL実行で得られた値のリスト
    itmObj.regrtn       # 正規表現で絞り込まれた結果のリスト
    itmObj.posrtn       # _dd シートの pos での絞り込み結果 None or list
    itmObj.resubrtn     # None or list
    itmObj.inum         # instance number (of same repeating grop)
    itmOjb.refi         # instance number reference (for kids)
    itmObj.p_nopapa     # used by spic() use no_papa pic or not
    itmObj.isclone      # this itm is a clone of above doc
    itmObj.confidence   # 230615 confidence info on json

    docObj は pickle にしてジョブフォルダに保存。処理結果の調査に使用。
'''

class itmObj:
    def __init__(self, dl):
        self.dl             = dl
        self.dl.reg         = dl.val    #   'val' in _dd sheet
        self.dl.grptgt      = dl.tgt    #   'tgt' in _dd sheet
        #   io.dl.val io.dl.tgt still exists
        self.seq            = None
        self.node           = None
        self.txt            = None
        self.page           = None
        self.hdbtm          = None
        self.fttop          = None
        self.gktop          = None
        self.gkbtm          = None
        self.top            = None
        self.btm            = None
        self.lft            = None
        self.ryt            = None
        self.otop           = None
        self.obtm           = None
        self.olft           = None
        self.oryt           = None
        self.spic           = None
        self.sqltxt         = None
        self.sqlarg         = None
        self.sqlrtn         = []    # list of tuple
        self.regrtn         = []    # list of tuple
        self.posrtn         = None  # otherwise list
        self.resubrtn       = None  # otherwise list
        self.inum           = None  # expand_doio() gives value
        self.refi           = None  # expand_doio() gives value
        self.p_nopapa       = False # used by spic() to use no_papa pic or not
        self.isclone        = False
        self.confidence     = None  # set at pos_narrow() / expand_doio()
