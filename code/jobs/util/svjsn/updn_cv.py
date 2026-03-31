#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   updn.py     250129  cy
#   updn_cv.py  260324  cy
#   updated: 260324.070440 by cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import json
import os
import requests
import time


from requests.exceptions import ConnectionError

import urllib3
from urllib3.exceptions import InsecureRequestWarning

from m.prnt     import prnt
from jobs.util.msg       import cred_ng, nw_err
from jobs.env   import DD

urllib3.disable_warnings(InsecureRequestWarning)

def updn_cv(png, jsnf): # can be any image incl pdf
    #
    #   up
    #
    bdy = open(png,'rb').read()
    cnt = 1
    prnt(f'going to up (CV) {os.path.basename(png)}')
    while True:
        if cnt > 3:
            nw_err(e)
            raise Exception('max retry reached to upload')
        try:
            res = requests.post(
                DD.url_up               ,
                headers = DD.hdr_up     ,
                data    = bdy           ,
#                proxies = DD.proxy      ,
                verify  = False         )
        except ConnectionError as e:
            prnt(f'ConnectionError as {e}')
            if not DD.cred_ok:
                prnt('possible cred NG, qutting')
                cred_ng(e)
                quit()
            else:
                prnt('possible nw error ({cnt}/4)')
                cnt += 1
                time.sleep(6)
                continue
        break
    DD.cred_ok = True
    if res.status_code != 202:
        raise Exception(
            f'status code: {res.status_code} \n{res.headers}\n  {res.text}')
    if 'Operation-Location' not in res.headers:
        raise Exception(
            f'no "Operation-Location"\n  {res.headers}\n  {res.text}')
    url_dn = res.headers['Operation-Location']
    #
    #   down
    #
    prnt(f'going to dwn (CV) {os.path.basename(png)}')
    while True:
        cnt = 1
        while True:
            if cnt > 3:
                raise Exception('max retry reached to donwload')
            try:
                res = requests.get(
                    url_dn              ,
                    headers = DD.hdr_dn ,
#                    proxies = DD.proxy  ,
                    verify  = False     )
            except ConnectionError as e:
                prnt(f'ConnectionError {cnt}/4 as {e}')
                cnt += 1
                time.sleep(6)
                continue
            break
        if res.status_code != 200:
            raise Exception(
                f'unexpected status_code {res.status_code}\n  {res.text}')
        hdr, ctype = phdr(res.headers)
        stat = pbdy(ctype,res)
        if stat != 'succeeded':
            time.sleep(1)
        else:
            break
    res = res.json()
    with open(jsnf,'w',encoding='utf-8') as f:
        json.dump(res, f, indent=2, ensure_ascii=False)
    return res # returns json

def phdr(hdr):
    ctype = None
    out = ''
    for i in hdr:
        out += f'  {i}: {hdr[i]}\n'
        if i == 'Content-Type':
            ctype = hdr[i]
    if ctype == None:
        raise Exception('no "Content-Type" in headers\n  {hdr}')
    return out, ctype

def pbdy(ctype,bdy):
    stat = None
    if not ctype.startswith('application/json'):
        raise Exception(f'not json body\n  {bdy.text}')
    bdy = bdy.json()
    if 'status' not in bdy:
        raise Exception(f'body has no "status"\n  {bdy}')
    stat = bdy['status']
    return stat
