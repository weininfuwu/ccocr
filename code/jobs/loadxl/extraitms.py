#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   extraitms.py        260317  cy
#   updated: 260319.183859 by cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

from m.env      import D
from m.prnt     import prnt
from ..env      import DD

def extraitms(wb,names):
    [sht,addr] = names['engine'].attr_text.split('!')
    engine = wb[sht][addr].value
    [sht,addr] = names['pdf2png'].attr_text.split('!')
    pdf2png = wb[sht][addr].value
    [sht,addr] = names['frmopt'].attr_text.split('!')
    frmopt = wb[sht][addr].value

    engines = []
    if engine == 'Doc. Intelligence':
        DD.engines = ['intelli']
    elif engine == '[OLD] vision':
        DD.engines = ['vision']
    elif engine == 'BOTH':
        DD.engines = ['intelli', 'vision']
    else:
        raise Exception('BANG!!! at extraitms() AA')

    if pdf2png == 'PNG変換する':    # name 'pdf2png' is used in code
        DD.pdf2api  = False
        DD.png2api  = True
    elif pdf2png == 'PNG変換しない':
        DD.pdf2api  = True
        DD.png2api  = False
    elif pdf2png == '両方':
        DD.pdf2api  = True
        DD.png2api  = True
    else:
        raise Exception('BANG!!! at extraitms() BB')

    if frmopt == 'マクロ付きエクセル':
        DD.use_web      = False
        DD.use_macro    = True
        DD.use_spic     = True
    elif frmopt == 'WEB':
        DD.use_web      = True
        DD.use_macro    = False
        DD.use_spic     = True
    elif frmopt == '両方':
        DD.use_web      = True
        DD.use_macro    = True
        DD.use_spic     = True
    elif frmopt == '確認画面不要':
        DD.use_web      = False
        DD.use_macro    = False
        DD.use_spic     = False
    else:
        raise Exception('BANG!!! at extraitms() CC')

    return
