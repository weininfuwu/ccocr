#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   msg.py      250203  cy
#   updated: 260319.153732 by cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import os
import subprocess
import tkinter
from tkinter    import messagebox
from pathlib    import Path

from m.env      import D
from ..env      import DD

root = tkinter.Tk()
root.attributes('-topmost', True)
root.withdraw()

ttl = 'クレカOCF'

def jpeg2000(bn):
    messagebox.showerror(f'{ttl} pdf2png.py',f'''
JPEG2000 形式のファイルは現在非対応です。
処理をここで終わります。

↓このファイルのことです。
{bn}''')
    return

def finish():
    messagebox.showinfo(f'{ttl} 正常終了',
    f'''処理がおわりました

ボタンを押すと新しくフォルダが開いて、処理結果はそこにあります。
（名前が一番短いエクセルです）

WEB版をお使いの場合、ブラウザにエラーが出るのが正常です。
ブラウザを閉じちゃってください。

(文字起こしの場合、読取結果設定エクセルが置いてあったフォルダの中にあります)''')
    if DD.jobtyp == 'frm':
        subprocess.run(['explorer',Path(DD.thisOutd)], shell=True)
    return

def nw_err(e):
    messagebox.showerror(f'{ttl} updn.py',(
        'OCRエンジンへの接続が拒否されました\n\n'
        'もう一回ためすとうまくいくかもしれません\n\n'
        'エラー詳細↓\n'
        f'{e}'))
    return

def cred_ng(e):
    messagebox.showerror(f'{ttl} updn.py',(
        'OCRエンジンへの接続が拒否されました\n\n'
        '利用初回にこのエラーが出た場合は\n'
        '資格情報を間違えて保存した可能性が高いです\n\n'
        'エラー詳細↓\n'
        f'{e}'))
    return

def cred_unset():
    ret = messagebox.askretrycancel(f'{ttl} cred.py',(
        'OCR課金キー・TTCIDのパスワード のいずれか/両方が空白です\n\n'
        '再試行 ⇨ やりなおす\n'
        'キャンセル ⇨ ここでおわりにする\n\n'
        'どちらかを選んでください'
        ))
    if ret != True:
        print(f'qutting with ret [{ret}]')
        quit()
    return

def noimg(usrd):
    messagebox.showerror(f'{ttl} mv2input.py',(
        '原稿のPDFが無いです\n\n'
        'OK を押すと、フローが覚えてる原稿置き場のフォルダが開きます。\n\n'
        '1) フローが覚えてるフォルダを変えたい\n'
        '　　フォルダごと消して、もう一回フローを動かすと、\n'
        '　　どこのフォルダにするのか聞いてきます。\n\n'
        '2) 開いたのと別のフォルダも使い分けたい\n'
        '　　フローのコピーを作ってそれを動かすと聞いてきます。\n\n'
        'どちらの場合も、原稿置場のフォルダには読取設定エクセルが必要です。'
        ))
    subprocess.run(['explorer',Path(usrd)], shell=True)
    return

def noxl(e):
    fname   = os.path.basename(D.fpath)
    dname   = os.path.dirname(D.fpath)
    messagebox.showerror(f'{ttl} loadxl.py',
                                        (f'''設定エクセルが開けません

＊ ダイアログでエクセルじゃないものを選んだ
＊ 記憶させておいたエクセルが無い

なんてことは無いですか？

↓ファイル名
{fname}
↓フォルダ名
{dname}

↓こんなエラーメッセージです
{e}

確認してやり直してくださいm(_ _)m'''))
    if os.path.isdir(dname):
        subprocess.run(['explorer',Path(dname)], shell=True)
    ## Path(xxx) needs to handel dirname has space

def shutilerr(usrd,e):
    messagebox.showerror(f'{ttl} mv2input.py',
                                        (f'''原稿のあるフォルダを触れません

プログラムが原稿のあるフォルダを触れません。
エクセルが開いたままだったりしませんか？

↓このフォルダのことです
{Path(usrd)}

↓こんなエラーメッセージです
{e}

確認してやり直してくださいm(_ _)m'''))
#    subprocess.run(['explorer',Path(usrd)], shell=True)    # NG 260319
    subprocess.run(['explorer',Path(usrd)])                 # OK 260319
    return
