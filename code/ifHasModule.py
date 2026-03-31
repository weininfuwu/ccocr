#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   ifHasModule.py      251230  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import importlib.metadata as m
import sys

try:
    m.version(sys.argv[-1])
    sys.exit(0)
except m.PackageNotFoundError:
    sys.exit(1)
except Exception as e:
    print(e)
    sys.exit(2)

