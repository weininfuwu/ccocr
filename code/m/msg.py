#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   msg.py      241018  cy 
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import os
import subprocess
import tkinter

from tkinter    import messagebox
from datetime   import datetime
from m.env      import D
from m.prnt     import prnt

root = tkinter.Tk()
root.attributes('-topmost', True)
root.withdraw()

def abend(e):
    prnt(f'ABEND\n{e}')
    messagebox.showerror(f'{D.appname} - 異常終了',(
        '処理がズッコケてしてしまいました。\n'
        'ズッコケ詳細は以下の通りです。\n\n'
        f'{e}'
    ))
    return

def finish():
    messagebox.showinfo(f'{D.appname}', (
        '処理が終わりました。\n\n'
        ))
#   fail if path has "&" char
#    subprocess.Popen(['explorer',f'{D.rootFld}'], shell=True)
    os.startfile(D.outdir)
    return

############### below may not be used ##############
def xllocked(xl):
    messagebox.showerror(f'{D.appname} - エクセルロック',(
        '以下のエクセルがロックされているようです。\n'
        '開いてる人を探して、閉じてもらってください。\n\n'
        f'{xl}\n\n'
        'プログラムは一旦ここで終了します。'
    ))
    return
def ljobd_cleanup_fail(path):
    messagebox.showerror(f'フォルダ削除失敗',
        (   'プログラムが使ってた古い仮フォルダの削除に失敗しました。\n\n'
            'OKを押すとフォルダが開くので、中身を削除してください m(_._)m'  ))
    subprocess.Popen(['explorer',path], shell=True)
    return

def msg_err(ttl,bdy):
    messagebox.showerror(ttl,(bdy))
    return

def oldver():
    messagebox.showerror(f'古いエクセル',
        (   'お使いのエクセルはバージョンが古いです。\n\n'
            '最新バージョンを入手して利用ください m(_ _)m'  ))
    return

def argerr(args, app_name):
    messagebox.showerror(f'{app_name} - 不正な起動パラメータ',
        (   'プログラムが正規のエクセル以外で起動されたみたいです。\n\n'
            f'{args}\n\n'
            '処理できません。'))
    return



#def finish(elsp,loadg,app_name='はんこポン'):
def __finish(xl,elsp,loadg,app_name):

    xl = os.path.basename(xl)

    em,es = divmod(elsp.seconds,60)
    lm,ls = divmod(loadg.seconds,60)
    badchars = ''
    if app_name == 'はんこポン':
        from m_hanko.env import DD
        if DD.badchars != None:
            badchars = f'''
【注意】
申請件名にシャチハタクラウドが受け付けない文字がありました。

　　{DD.badchars}

上記の文字を省いた状態で申請メッセージが出されています。

'''
    messagebox.showinfo(f'{app_name}', (
        '処理が終わりました。\n\n'

        f'{xl}\n\n'

        f'{badchars}'
        f'{lm:02}分{ls:02}秒 プログラム読込時間\n'
        f'{em:02}分{es:02}秒 処理時間'))
    return
