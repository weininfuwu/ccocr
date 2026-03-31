#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   toys.py     251221  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import json
import os
import tkinter.filedialog as fd
import tkinter.simpledialog as sd

from m.env          import D
from m.prnt         import prnt
from .kickPS        import kickPS
from .toys_askmulti import toys_askmulti


def fwrite(file,txt):
    with open(file,'w',encoding='utf-8') as f:
        f.write(txt)
    return

def fread(file):
    if not os.path.isfile(file):
        return None
    with open(file,'r',encoding='utf-8') as f:
        return f.read()

def askmulti(prmpt,itmCnt,itmLen,fname):
    flwd    = D.flwd
    ofname  = fname
    fname   = os.path.join(flwd,fname)
    if not os.path.isfile(fname):
        while True:
            rtn = toys_askmulti(prmpt,itmCnt,itmLen)    # type(rtn) == list
            if len(rtn) > 0:
                break
        prnt(f'rtn {rtn} type(rtn) {type(rtn)}')
        with open(fname,'w',encoding='utf-8') as f:
            json.dump(rtn, f, indent=2)
        return rtn
    prnt(f'checking on saved file\n  {fname}')
    with open(fname,'r',encoding='utf-8') as f:
        rtn = json.load(f)
    return rtn

def askint(ttl,prmpt,fname):
    flwd    = D.flwd
    ofname  = fname
    fname   = os.path.join(flwd,fname)
    if not os.path.isfile(fname):
        while True:
            val = sd.askinteger(ttl,prmpt)
            prnt(f'input value "{val}"')
            if val != None:
                break
        fwrite(fname,str(val))
        return val
    prnt(f'checking on saved file\n  {fname}')
    val = fread(fname)
    return val

def askfile(prmpt,fname):
    flwd    = D.flwd
    ofname  = fname
    fname   = os.path.join(flwd,fname)
    if not os.path.isfile(fname):                   # NO record
        fpath = fd.askopenfilename(title=prmpt)
        if fpath == '':
            prnt('redo askfile')
            askfile(prmpt,fname)
        fpath = os.path.normpath(fpath)
        fwrite(fname,fpath)
        return fpath
    prnt(f'checking on saved file\n  {fname}')      # HAS record
    fpath = fread(fname)
    if os.path.isfile(fpath):                       # tgt exists
        prnt(f'file exists\n  {fname}')
        return fpath
    initD = os.path.dirname(fpath)                  # tgt NOT exists
    while True:
        prnt(f'see if dir exists\n  {initD}')
        if os.path.isdir(initD):
            break
        initD = os.path.dirname(initD)
        if len(initD) <= 3:                 ## C:\
            initD = f'C:{os.sep}'
            break
    prnt(f'initD\n  {initD}')
    fpath = fd.askopenfilename( title       = prmpt ,
                                initialdir  = initD )
    if fpath == '':
        prnt('redo askfileNS')
        askfileNS(prmpt,fname)
    fwrite(fname,fpath)
    return fpath

def askfileNS(prmpt,fname):
    flwd    = D.flwd
    ofname  = fname
    fname   = os.path.join(flwd,fname)
    if not os.path.isfile(fname):
        fpath = fd.askopenfilename(title = prmpt)
        fwrite(fname,fpath)
        return fpath
    prnt(f'checking on saved file\n  {fname}')
    fpath = fread(fname)


    initD = os.path.dirname(fpath)
    if os.path.isfile(fpath):
        prnt(f'file exists\n  {fname}')
        fpath = fd.askopenfilename( title       = prmpt ,
                                    initialdir  = initD )
                                #   initialfile only works for VERY SHORT name
        fwrite(fname,fpath)
        return fpath
    while True:
        prnt(f'see if dir exists\n  {initD}')
        if os.path.isdir(initD):
            break
        initD = os.path.dirname(initD)
        if len(initD) <= 3:                 ## C:\
            initD = f'C:{os.sep}'
            break
    prnt(f'initD\n  {initD}')
    fpath = fd.askopenfilename( title       = prmpt ,
                                initialdir  = initD )
    if fpath == '':
        prnt('redo askfileNS')
        askfileNS(prmpt,fname)
    fwrite(fname,fpath)
    return fpath

def askdir(prmpt,fname):
    flwd    = D.flwd
    ofname  = fname
    fname   = os.path.join(flwd,fname)
    if not os.path.isfile(fname):
        fpath = fd.askdirectory(title=prmpt)
        if fpath == '':
            prnt('redo askdir')
            askdir(prmpt,fname)
        fpath = os.path.normpath(fpath)
        fwrite(fname,fpath)
        return fpath
    prnt(f'checking on saved dir\n  {fname}')
    fpath = fread(fname)
    if not os.path.isdir(fpath):
        os.remove(fname)
        askdir(prmpt,ofname)
    return fpath

def askdirNS(prmpt,fname):
    flwd    = D.flwd
    ofname  = fname
    fname   = os.path.join(flwd,fname)
    fpath   = kickPS(
        'toys_askFld.ps1'                                                   ,
        [   os.path.join(os.path.dirname(__file__),'toys_askFld.ps1')   ,
            prmpt                                                       ,
            fname                                                       ]   )
    prnt(f'fpath befor splitlines()\n  {fpath}')
    fpath = fpath.splitlines()[-1]
    return fpath
