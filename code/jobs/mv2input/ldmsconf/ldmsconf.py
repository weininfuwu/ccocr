#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   ldmsconf.py     250225  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

#from .ldsorter   import ldsorter
#from .ldconfig   import ldconfig

from .ldsorter.ldsorter import ldsorter
from .ldconfig.ldconfig import ldconfig

class msc:
    def __init__(self,sorter,docdef):
        self.sorter = sorter
        self.docdef = docdef

def ldmsconf():
    sorter = ldsorter()
    docdef = ldconfig(sorter)
    msconf = msc(sorter,docdef)
    return msconf
