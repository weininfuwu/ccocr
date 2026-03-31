#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   rotate.py   220905  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import sys
import numpy as np

from m.prnt import prnt

def rotate(angl,otl_x,otl_y,otr_x,otr_y,obr_x,obr_y,obl_x,obl_y,ow,oh,jw,jh):
    etl_x = otl_x * ow / jw
    etl_y = otl_y * oh / jh
    etr_x = otr_x * ow / jw
    etr_y = otr_y * oh / jh
    ebr_x = obr_x * ow / jw
    ebr_y = obr_y * oh / jh
    ebl_x = obl_x * ow / jw
    ebl_y = obl_y * oh / jh
    # rotate
    if angl > -180 and angl <= -135: # -170 on json ,190 (180 + 10)
        rad = np.radians(180+angl)
        tl = (round((ow-etl_x) * np.cos(rad) + (oh-etl_y) * np.sin(rad)),
              round((oh-etl_y) * np.cos(rad) + etl_x      * np.sin(rad)) )
        tr = (round((ow-etr_x) * np.cos(rad) + (oh-etr_y) * np.sin(rad)),
              round((oh-etr_y) * np.cos(rad) + etr_x      * np.sin(rad)) )
        br = (round((ow-ebr_x) * np.cos(rad) + (oh-ebr_y) * np.sin(rad)),
              round((oh-ebr_y) * np.cos(rad) + ebr_x      * np.sin(rad)) )
        bl = (round((ow-ebl_x) * np.cos(rad) + (oh-ebl_y) * np.sin(rad)),
              round((oh-ebl_y) * np.cos(rad) + ebl_x      * np.sin(rad)) )
    elif angl > -135 and angl <= -90:   # -100 on json, 260 (270 - 10)
        rad = np.radians(-90-angl)
        tl = (round((oh-etl_y) * np.cos(rad) + (ow-etl_x) * np.sin(rad)),
              round(etl_x      * np.cos(rad) + (oh-etl_y) * np.sin(rad)) )
        tr = (round((oh-etr_y) * np.cos(rad) + (ow-etr_x) * np.sin(rad)),
              round(etr_x      * np.cos(rad) + (oh-etr_y) * np.sin(rad)) )
        br = (round((oh-ebr_y) * np.cos(rad) + (ow-ebr_x) * np.sin(rad)),
              round(ebr_x      * np.cos(rad) + (oh-ebr_y) * np.sin(rad)) )
        bl = (round((oh-ebl_y) * np.cos(rad) + (ow-ebl_x) * np.sin(rad)),
              round(ebl_x      * np.cos(rad) + (oh-ebl_y) * np.sin(rad)) )
    elif angl > -90 and angl <= -45:    # -80 on json, 280 (270 + 10)
        rad = np.radians(90+angl)
        tl = (round((oh-etl_y) * np.cos(rad) + etl_x      * np.sin(rad)),
              round(etl_x      * np.cos(rad) + etl_y      * np.sin(rad)) )
        tr = (round((oh-etr_y) * np.cos(rad) + etr_x      * np.sin(rad)),
              round(etr_x      * np.cos(rad) + etr_y      * np.sin(rad)) )
        br = (round((oh-ebr_y) * np.cos(rad) + ebr_x      * np.sin(rad)),
              round(ebr_x      * np.cos(rad) + ebr_y      * np.sin(rad)) )
        bl = (round((oh-ebl_y) * np.cos(rad) + ebl_x      * np.sin(rad)),
              round(ebl_x      * np.cos(rad) + ebl_y      * np.sin(rad)) )
    elif angl > -45 and angl <= 0:      # -10 on jaon, -10
        rad = np.radians(-angl)
        tl = (round(etl_x      * np.cos(rad) + (oh-etl_y) * np.sin(rad)),
              round(etl_y      * np.cos(rad) + etl_x      * np.sin(rad)) )
        tr = (round(etr_x      * np.cos(rad) + (oh-etr_y) * np.sin(rad)),
              round(etr_y      * np.cos(rad) + etr_x      * np.sin(rad)) )
        br = (round(ebr_x      * np.cos(rad) + (oh-ebr_y) * np.sin(rad)),
              round(ebr_y      * np.cos(rad) + ebr_x      * np.sin(rad)) )
        bl = (round(ebl_x      * np.cos(rad) + (oh-ebl_y) * np.sin(rad)),
              round(ebl_y      * np.cos(rad) + ebl_x      * np.sin(rad)) )
    elif angl > 0 and angl <= 45:
        rad = np.radians(angl)
        tl = (round(etl_x     * np.cos(rad) + etl_y      * np.sin(rad)),
              round(etl_y     * np.cos(rad) + (ow-etl_x) * np.sin(rad)) )
        tr = (round(etr_x     * np.cos(rad) + etr_y      * np.sin(rad)),
              round(etr_y     * np.cos(rad) + (ow-etr_x) * np.sin(rad)) )
        br = (round(ebr_x     * np.cos(rad) + ebr_y      * np.sin(rad)),
              round(ebr_y     * np.cos(rad) + (ow-ebr_x) * np.sin(rad)) )
        bl = (round(ebl_x     * np.cos(rad) + ebl_y      * np.sin(rad)),
              round(ebl_y     * np.cos(rad) + (ow-ebl_x) * np.sin(rad)) )
    elif angl > 45 and angl <= 90:      # 80 on json, 80 (90-10)
        rad = np.radians(90-angl)
        tl = (round(etl_y     * np.cos(rad) + etl_x      * np.sin(rad)),
              round((ow-etl_x)* np.cos(rad) + etl_y      * np.sin(rad)) )
        tr = (round(etr_y     * np.cos(rad) + etr_x      * np.sin(rad)),
              round((ow-etr_x)* np.cos(rad) + etr_y      * np.sin(rad)) )
        br = (round(ebr_y     * np.cos(rad) + ebr_x      * np.sin(rad)),
              round((ow-ebr_x)* np.cos(rad) + ebr_y      * np.sin(rad)) )
        bl = (round(ebl_y     * np.cos(rad) + ebl_x      * np.sin(rad)),
              round((ow-ebl_x)* np.cos(rad) + ebl_y      * np.sin(rad)) )
    elif angl > 90 and angl <= 135:     # 100 on json, 100 (90 + 10)
        rad = np.radians(angl-90)
        tl = (round(etl_y     * np.cos(rad) + (ow-etl_x) * np.sin(rad)),
              round((ow-etl_x)* np.cos(rad) + (oh-etl_y) * np.sin(rad)) )
        tr = (round(etr_y     * np.cos(rad) + (ow-etr_x) * np.sin(rad)),
              round((ow-etr_x)* np.cos(rad) + (oh-etr_y) * np.sin(rad)) )
        br = (round(ebr_y     * np.cos(rad) + (ow-ebr_x) * np.sin(rad)),
              round((ow-ebr_x)* np.cos(rad) + (oh-ebr_y) * np.sin(rad)) )
        bl = (round(ebl_y     * np.cos(rad) + (ow-ebl_x) * np.sin(rad)),
              round((ow-ebl_x)* np.cos(rad) + (oh-ebl_y) * np.sin(rad)) )
    elif angl > 135 and angl <= 180:    # 170 on json, 170 (180 - 10)
        rad = np.radians(180-angl)
        tl = (round((ow-etl_x)* np.cos(rad) + etl_y      * np.sin(rad)),
              round((oh-etl_y)* np.cos(rad) + (ow-etl_x) * np.sin(rad)) )
        tr = (round((ow-etr_x)* np.cos(rad) + etr_y      * np.sin(rad)),
              round((oh-etr_y)* np.cos(rad) + (ow-etr_x) * np.sin(rad)) )
        br = (round((ow-ebr_x)* np.cos(rad) + ebr_y      * np.sin(rad)),
              round((oh-ebr_y)* np.cos(rad) + (ow-ebr_x) * np.sin(rad)) )
        bl = (round((ow-ebl_x)* np.cos(rad) + ebl_y      * np.sin(rad)),
              round((oh-ebl_y)* np.cos(rad) + (ow-ebl_x) * np.sin(rad)) )
    else:
        prnt(f'angle not suppoted: {angl}')
        sys.exit(1)
    return tl,tr,br,bl
