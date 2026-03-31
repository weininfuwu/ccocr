#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   kickPS.py
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import os
import subprocess

from m.env      import D
from m.prnt     import prnt

def kickPY(pyname, arg=[]):
    pyn     = os.path.basename(pyname)
    arg     = ['python', pyname] + arg
    rtn     = subprocess.run(   arg                             ,
                                stdout      = subprocess.PIPE   ,
                                stderr      = subprocess.STDOUT ,
                                text        = True              ,
                                encoding    = 'cp932'           )
    prnt((
        f'\n--- begin {pyn} output ---({rtn.returncode})---\n'
        f'{rtn.stdout}'
        f'\n--- end {pyn} output ---({rtn.returncode})---'))
    if rtn.returncode == 99:    ## no much meaning
        prnt('quitting due to code 99 from {pyn}')
        quit()
    elif rtn.returncode != 0:
        raise Exception(f'{pyn} failed with code {rtn.returncode}')
    return rtn.stdout

def kickPS(ps1name, arg):
    arg     = ['powershell', '-File' ] + arg
    prnt(f'arg {arg}')
    rtn     = subprocess.run(   arg                             ,
                                stdout      = subprocess.PIPE   ,
                                stderr      = subprocess.STDOUT ,
                                text        = True              ,
                                encoding    = 'cp932'           )
    prnt((
        f'\n--- begin {ps1name} output ---({rtn.returncode})---\n'
        f'{rtn.stdout}'
        f'\n--- end {ps1name} output ---({rtn.returncode})---'))
    if rtn.returncode == 99:    ## error controled inside PS1
        prnt('quitting due to code 99 from {ps1name}')
        quit()                  ## user SHOULD alerady got error msg
    elif rtn.returncode != 0:
        raise Exception(f'{ps1name} failed with code {rtn.returncode}')
    return rtn.stdout

def kickPS_console(ps1name, arg):
    arg     = ['powershell', '-File' ] + arg
    print(f'arg {arg}')
    rtn     = subprocess.run(   arg                             ,
                                stdout      = subprocess.PIPE   ,
                                stderr      = subprocess.STDOUT ,
                                text        = True              ,
                                encoding    = 'cp932'           )
    print((
        f'\n--- begin {ps1name} output ---({rtn.returncode})---\n'
        f'{rtn.stdout}'
        f'\n--- end {ps1name} output ---({rtn.returncode})---'))
    if rtn.returncode == 99:    ## error controled inside PS1
        print('quitting due to code 99 from {ps1name}')
        quit()                  ## user SHOULD alerady got error msg
    elif rtn.returncode != 0:
        raise Exception(f'{ps1name} failed with code {rtn.returncode}')
    return rtn.stdout
