#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   usepng.py   260318  cy
#   updated: 260321 strip_label handles CV/DI suffixes
#
#   Utility functions for DD.pdf2api / DD.png2api checking.
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import os

from ..env import DD

def use_png_conversion():
    # True when PNG conversion is performed before sending to API
    return DD.png2api

def use_straight():
    # True when files are sent to API as-is (without PNG conversion)
    return DD.pdf2api

def use_noup_png():
    # True when NOUP.png (marking copy) should be used instead of plain .png
    return DD.pdf2api

def strip_label(name):
    # Remove BOTH-mode and engine suffixes added to elmlst[0] for Excel column A labeling
    return (name
            .replace(' STRAIGHT', '')
            .replace(' from PNG', '')
            .replace(' CV', '')
            .replace(' DI', ''))

def straight_name(bn):
    # ncv: send original file as-is to pngUP (no suffix)
    return bn
