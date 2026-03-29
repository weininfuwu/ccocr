#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   cred.py     250205  cy
#   updated: 260319.153926 by cy
#   updated: 260321 rename keyring keys to ccocr_cv_key/ccocr_cv_ep
#   updated: 260321 add cred_di() for Document Intelligence
#   updated: 260330 cred_all(): engine-aware, connectivity check, single dialog
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import json
import os
import subprocess
import keyring
import requests

from m.prnt         import prnt
from jobs.env       import DD
from jobs.util.msg  import cred_unset

def setenv(key, ep):
    DD.url_up = f'{ep}vision/v3.2/read/analyze?readingOrder=natural'
    DD.hdr_up = {
        'Ocp-Apim-Subscription-Key' : key                           ,
        'Content-Type'              : 'application/octet-stream'    , }
    DD.hdr_dn = { 'Ocp-Apim-Subscription-Key' : key, }
    prnt(f'using CV cred for {ep}')
    return

def setenv_di(key, ep):
    DD.di_key = key
    DD.di_ep  = ep
    prnt(f'using DI cred for {ep}')
    return

def check_cv(key, ep):
    try:
        url = f'{ep}vision/v3.2/read/analyze?readingOrder=natural'
        r = requests.post(url,
            headers = {
                'Ocp-Apim-Subscription-Key' : key,
                'Content-Type'              : 'application/octet-stream',
            },
            data    = b'',
            timeout = 10,
            verify  = False,
        )
        ok = r.status_code != 401
        prnt(f'CV check: {"OK" if ok else "NG"} (http {r.status_code})')
        return ok
    except Exception as e:
        prnt(f'CV check error: {e}')
        return False

def check_di(key, ep):
    try:
        url = f'{ep}documentintelligence/documentModels?api-version=2024-11-30'
        r = requests.get(url,
            headers = {'Ocp-Apim-Subscription-Key': key},
            timeout = 10,
            verify  = False,
        )
        ok = r.status_code != 401
        prnt(f'DI check: {"OK" if ok else "NG"} (http {r.status_code})')
        return ok
    except Exception as e:
        prnt(f'DI check error: {e}')
        return False

def _ask(ask_cv, ask_di):
    while True:
        args = ['python', os.path.join(os.path.dirname(__file__), 'askcred.py')]
        if ask_cv: args.append('--cv')
        if ask_di: args.append('--di')
        jsn = subprocess.run(args, capture_output=True, text=True).stdout
        jsn = json.loads(jsn)
        ok  = True
        if ask_cv:
            jsn['key'] = jsn.get('key', '').strip()
            jsn['ep']  = jsn.get('ep',  '').strip()
            if not jsn['key'] or not jsn['ep']:
                ok = False
        if ask_di:
            jsn['di_key'] = jsn.get('di_key', '').strip()
            jsn['di_ep']  = jsn.get('di_ep',  '').strip()
            if not jsn['di_key'] or not jsn['di_ep']:
                ok = False
        if ok:
            return jsn
        cred_unset()

def cred_all(engines):
    need_cv = 'vision'  in engines
    need_di = 'intelli' in engines
    ask_cv  = False
    ask_di  = False

    if need_cv:
        key = keyring.get_password('ccocr_cv_key', 'me')
        ep  = keyring.get_password('ccocr_cv_ep',  'me')
        if key and ep and check_cv(key, ep):
            setenv(key, ep)
        else:
            prnt('CV cred missing or invalid → asking')
            ask_cv = True

    if need_di:
        key = keyring.get_password('ccocr_di_key', 'me')
        ep  = keyring.get_password('ccocr_di_ep',  'me')
        if key and ep and check_di(key, ep):
            setenv_di(key, ep)
        else:
            prnt('DI cred missing or invalid → asking')
            ask_di = True

    if not ask_cv and not ask_di:
        return

    jsn = _ask(ask_cv, ask_di)

    if ask_cv:
        keyring.set_password('ccocr_cv_key', 'me', jsn['key'])
        keyring.set_password('ccocr_cv_ep',  'me', jsn['ep'])
        setenv(jsn['key'], jsn['ep'])
        prnt('CV credential set/updated')

    if ask_di:
        keyring.set_password('ccocr_di_key', 'me', jsn['di_key'])
        keyring.set_password('ccocr_di_ep',  'me', jsn['di_ep'])
        setenv_di(jsn['di_key'], jsn['di_ep'])
        prnt('DI credential set/updated')

# 旧インタフェース互換（直接呼び出しがあれば）
def cred():    cred_all(['vision'])
def cred_di(): cred_all(['intelli'])
