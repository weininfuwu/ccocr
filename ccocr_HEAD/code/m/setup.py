#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   setup.py    251221  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#


from datetime import datetime
import os
import sys

from m.env      import D
from m.prnt     import prnt
from m.kickPS   import kickPS_console as kickPS0
from jobs.env   import DD

import argparse

def setupPlus():  ## for embedded
    parser = argparse.ArgumentParser(description='for EMBEDDED mode')
    parser.add_argument('--sysFld' , required=True)
    parser.add_argument('--flwid'   , required=True)
    parser.add_argument('--appname' , required=True)
    parser.add_argument('--mymail')
    parser.add_argument('--jobid')
    parser.add_argument('--flwd')
    parser.add_argument('--logd')
    parser.add_argument('--logf')
    parser.add_argument('--idx')
    parser.add_argument('--config')
    parser.add_argument('--embedded', action='store_true')

    args = parser.parse_args()

    sysFld      = args.sysFld
    flwid       = args.flwid
    appname     = args.appname
    mymail      = args.mymail   # option
    jobid       = args.jobid    # option
    flwd        = args.flwd     # option
    logd        = args.logd     # option
    logf        = args.logf     # option
    idx         = args.idx      # option
    config      = args.config   # option
    EMBEDDED    = args.embedded

    if mymail is None:
        mymail = kickPS0('mymail.ps1', [os.path.join(
                                    os.path.dirname(__file__),'mymail.ps1')])
    if jobid is None:
        jobid = f"{mymail}_{datetime.now().strftime('%y%m%d.%H%M%S.%f')}"
    if flwd is None:
        flwd = os.path.join(os.getenv('USERPROFILE'),'DigNav','flows',flwid)
    if logd is None:
        logd = os.path.join(sysFld,'log',jobid)
    if logf is None:
        logf = os.path.join(logd,f'{jobid}.txt')
    os.makedirs(logd, exist_ok=True)

    D.sysFld    = sysFld
    D.flwid     = flwid
    D.appname   = appname
    D.mymail    = mymail
    D.jobid     = jobid
    D.flwd      = flwd
    D.logd      = logd
    D.logf      = logf
    D.papaidx   = int(idx)
    DD.config   = config
    D.EMBEDDED  = EMBEDDED
    prnt(f'''
  this is ccocrEmbedded kicked from papa, args are;
  sysFld    {sysFld}
  flwid     {flwid}
  appname   {appname}
  mymail    {mymail}
  jobid     {jobid}
  flwd      {flwd}
  logd      {logd}
  logf      {logf}
  idx       {idx}
  config    {config}
  EMBEDDED  {str(EMBEDDED)}''')

def setup():    ## for nomal use
    [xxx, sysFld, flwid, appname, *rest] = sys.argv
    config = None
    for i, a in enumerate(rest):
        if a == '--config' and i + 1 < len(rest):
            config = rest[i + 1]
    #   sysFld      system folder in Box
    D.sysFld    = sysFld
    D.flwid     = flwid
    D.appname   = appname
    DD.config   = config
    mymail      = kickPS0('mymail.ps1', [os.path.join(
                                    os.path.dirname(__file__),'mymail.ps1')])
    D.mymail    = mymail
    jobid       = f"{mymail}_{datetime.now().strftime('%y%m%d.%H%M%S.%f')}"
    D.jobid     = jobid
    logd        = os.path.join(sysFld,'log',jobid)
    D.logd      = logd
    os.makedirs(logd, exist_ok=True)
    logf        = os.path.join(logd,f'{jobid}.txt')
    D.logf      = logf
    flwd        = os.path.join(os.getenv('USERPROFILE'),'DigNav','flows',flwid)
    D.flwd      = flwd
    prnt('setup completed')
    return
