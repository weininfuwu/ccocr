#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   main.py     260224  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import traceback
import sys

from m.prnt         import prnt
from m.setup        import setup, setupPlus
from m.msg          import finish, abend
from jobs.control   import control

from m.env import D

#
#   set very basic vars
#
if len(sys.argv) >= 2 and sys.argv[1].startswith('--'):
    setupPlus()     ## embedded
else:
    setup()
#
#   jobs
#
try:
    control()
except Exception as e:
    prnt(f'''PROGRAM TERMINATED
{traceback.format_exc()}''')
    abend(e)
    quit()
prnt('ALL FINISHED')
if not D.EMBEDDED:
    finish()
