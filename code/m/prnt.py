#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   prnt.py     231020  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import inspect
import os
import re
from datetime import datetime

from .env import D

# Windows 11 / PowerShell で ANSI を有効化
if os.name == 'nt':
    os.system('')

def prnt(msg, st=None, color=None):
    if st is None:
        st = inspect.stack()[1]

    # --- 共通のログ生成ロジック ---
    now     = datetime.now().strftime('%y%m%d.%H%M%S')
    base    = os.path.normpath(os.path.join(os.path.dirname(__file__), r'..'))
    lineno  = st.lineno
    mod     = os.path.normpath(st.filename)
    mod     = mod.replace(base, '')
    mod     = re.sub(r'\.py$', '', mod)
    if mod.startswith(os.sep):
        mod = mod[1:]
    mod     = mod.replace(os.sep, '.')
    log     = f'{now} {mod} {lineno}: {msg}'
    flog    = log
    if color is None and getattr(D, 'EMBEDDED', False):
        flog    = f'e {log}'

    # ファイル保存（共通：色は付けない）
    with open(D.logf, mode='a', encoding='utf-8') as f:
        f.write(f'{flog}\n')
        f.flush()

    # --- コンソール出力の判定 ---
    # colorが明示されていない場合、D.EMBEDDED が True ならシアン(36)をデフォルトに
    if color is None and getattr(D, 'EMBEDDED', False):
        color = '36'

    if color:
        print(f'\033[{color}m{log}\033[0m')
    else:
        print(log)
    return

