#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   conv.py     260322  cy
#   updated: 260322 bad font PDF: pdftocairo via subprocess (not pdf2image)
#   updated: 260322 add POPPLER_DATADIR / FONTCONFIG_FILE / cwd=ppld
#   updated: 260322 zero-pad page number in rename (pdftocairo -1.png -> .01.png)
#
#   Convert input files to pngPRE (canvas) and pngUP (API input).
#
#   pdf2api  = send PDF as-is  to API  (usepng=False / BOTH)
#   png2api  = send PNG        to API  (usepng=True  / BOTH)
#
#   PDF only:
#     encChk when png2api=True.
#     bad font -> pngPRE only for PNG; PDF to pngUP if pdf2api.
#     good font / no encChk -> PNG to pngPRE (+pngUP if png2api);
#                               PDF to pngUP if pdf2api.
#
#   non-PDF (jpg/png/gif/...):
#     no encChk.
#     PNG to pngPRE always.
#     PNG to pngUP if png2api.
#     original to pngUP as STRAIGHT if pdf2api.
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import os
import shutil
import cv2

from pdf2image      import convert_from_path
from PIL            import Image

from m.prnt         import prnt
from m.env          import D
from m.cv2read      import cv2read
from m.cv2write     import cv2write
from jobs.env       import DD
from jobs.util.usepng import (
    use_straight, use_png_conversion, straight_name)
from jobs.util.msg  import jpeg2000
from .encChk.encChk import encChk


# ---------------------------------------------------------------------------
# public entry points
# ---------------------------------------------------------------------------

def conv(itm, bn, pngPRE, pngUP, dpi, qlty):
    """Route one input file to the appropriate handler."""
    ext = os.path.splitext(bn)[1].lower()
    if ext == '.pdf':
        _conv_pdf(itm, bn, pngPRE, pngUP, dpi, qlty)
    else:
        _conv_img(itm, bn, pngPRE, pngUP)


# ---------------------------------------------------------------------------
# internal helpers
# ---------------------------------------------------------------------------

def _png_to_pre(pages, bn, pngPRE, qlty, apply_qlty=True):
    """Save pdf2image pages to pngPRE as hoge.ext.NN.png."""
    for pgnum, pg in enumerate(pages):
        tmp = os.path.join(pngPRE, f'{bn}.{pgnum+1:02}.png')
        pg.save(tmp)
        prnt(f'saved at pngPRE  {tmp.replace(D.logd, "")}')
        if apply_qlty:
            _apply_qlty(tmp, qlty)


def _pdftocairo_to_pre(itm, bn, pngPRE, ppld, dpi):
    """
    Call pdftocairo.exe directly to convert bad-font PDF to PNG.
    pdftocairo writes: <prefix>-01.png, <prefix>-02.png, ...
    Rename to:         <bn>.01.png,      <bn>.02.png, ...
    """
    import subprocess
    import glob as _glob
    exe     = os.path.join(ppld, 'pdftocairo.exe')
    prefix  = os.path.join(pngPRE, bn)   # pdftocairo adds -NN.png
    env     = os.environ.copy()
    env['PATH'] = ppld + os.pathsep + env.get('PATH', '')
    poppler_share = os.path.normpath(
        os.path.join(ppld, '..', 'share', 'poppler'))
    env['POPPLER_DATADIR'] = poppler_share
    prnt(f'POPPLER_DATADIR: {poppler_share}')
    fc_dir  = os.path.normpath(os.path.join(ppld, '..', 'etc', 'fonts'))
    fc_file = os.path.join(fc_dir, 'fonts.conf')
    env['FONTCONFIG_PATH'] = fc_dir
    env['FONTCONFIG_FILE'] = fc_file
    prnt(f'FONTCONFIG_PATH: {fc_dir}')
    prnt(f'FONTCONFIG_FILE: {fc_file}')
    prnt(f'fonts.conf exists: {os.path.isfile(fc_file)}')
    cmd = [exe, '-png', '-r', str(dpi), itm, prefix]
    prnt(f'pdftocairo cmd: {" ".join(cmd)}')
    result = subprocess.run(
        cmd, env=env, cwd=ppld,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = result.stdout.decode(errors='replace').strip()
    stderr = result.stderr.decode(errors='replace').strip()
    if stdout:
        prnt(f'pdftocairo stdout: {stdout}')
    if stderr:
        prnt(f'pdftocairo stderr: {stderr}')
    prnt(f'pdftocairo returncode: {result.returncode}')
    if result.returncode != 0:
        raise Exception(f'pdftocairo failed (rc={result.returncode})')
    # check output files exist
    generated = sorted(_glob.glob(f'{prefix}-*.png'))
    if not generated:
        raise Exception(
            f'pdftocairo succeeded (rc=0) but no PNG generated: {prefix}-*.png')
    prnt(f'pdftocairo generated {len(generated)} file(s)')
    # rename prefix-1.png / prefix-01.png -> bn.01.png
    # pdftocairo uses no zero-padding for single pages (-1.png)
    # normalize to 2-digit zero-padded page number
    for src in generated:
        raw_sfx = os.path.basename(src)[len(bn)+1:]  # e.g. '1.png' or '01.png'
        pg_str  = os.path.splitext(raw_sfx)[0]       # '1' or '01'
        pg_pad  = pg_str.zfill(2)                     # '01'
        dst     = os.path.join(pngPRE, f'{bn}.{pg_pad}.png')
        os.rename(src, dst)
        prnt(f'saved at pngPRE  {dst.replace(D.logd, "")}')


def _pdf_to_up(itm, bn, pngUP):
    """Copy PDF as-is to pngUP as STRAIGHT."""
    dst = os.path.join(pngUP, straight_name(bn))
    shutil.copy(itm, dst)
    prnt(f'PDF -> pngUP STRAIGHT  {os.path.basename(dst)}')


def _apply_qlty(tmp, qlty):
    """Apply image quality filter (lv1/lv2/lv3)."""
    if qlty not in ['lv1', 'lv2', 'lv3']:
        return
    img = cv2read(tmp)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    prnt('qlty lv1')
    if qlty in ['lv2', 'lv3']:
        img = cv2.bilateralFilter(img, 9, 75, 75)
        prnt('qlty lv2')
    if qlty == 'lv3':
        th, img = cv2.threshold(
            img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        prnt(f'qlty lv3 threshold {th}')
    cv2write(tmp, img, allow_overwrite=True)
    prnt('imgfile overwritten')


# ---------------------------------------------------------------------------
# PDF handler
# ---------------------------------------------------------------------------

def _conv_pdf(itm, bn, pngPRE, pngUP, dpi, qlty):
    ppld    = os.path.join(
        D.sysFld, 'code', 'poppler', 'Library', 'bin')
    pdf2api = use_straight()
    png2api = use_png_conversion()

    # PDF only to API (usepng=False)
    if pdf2api and not png2api:
        _pdf_to_up(itm, bn, pngUP)
        pg = convert_from_path(
            itm, poppler_path=ppld, use_cropbox=True, dpi=dpi)
        _png_to_pre(pg, bn, pngPRE, qlty, apply_qlty=False)
        return

    # PNG (and optionally PDF) to API -- encChk required
    result = encChk(itm)
    bad    = (result[0] == False)

    if bad:
        # bad font: call pdftocairo.exe directly via subprocess
        # avoids pdf2image's LD_LIBRARY_PATH-only env handling on Windows
        prnt(f'enc issue: pdftocairo -> pngPRE (no qlty)  {bn}')
        _pdftocairo_to_pre(itm, bn, pngPRE, ppld, dpi)
        if pdf2api:
            _pdf_to_up(itm, bn, pngUP)
        return

    # good font
    pg = convert_from_path(
        itm, poppler_path=ppld, use_cropbox=True, dpi=dpi)
    _png_to_pre(pg, bn, pngPRE, qlty, apply_qlty=True)
    if pdf2api:
        _pdf_to_up(itm, bn, pngUP)
    # png2api: pngPRE -> pngUP copy handled by pdf2png() loop


# ---------------------------------------------------------------------------
# non-PDF handler (jpg / png / gif / bmp / etc.)
# ---------------------------------------------------------------------------

def _conv_img(itm, bn, pngPRE, pngUP):
    prnt(f'converting to png  {bn}')
    im = Image.open(itm)
    if im.format == 'JPEG2000':
        jpeg2000(bn)
        quit()
    prnt(f'image format: {im.format:<8}  {bn}')

    pdf2api = use_straight()
    png2api = use_png_conversion()

    # PNG to pngPRE (always)
    dst_pre = os.path.join(pngPRE, f'{bn}.01.png')
    im.save(dst_pre, 'png')
    prnt(f'saved at pngPRE  {bn}.01.png')

    # original as STRAIGHT to pngUP (if pdf2api)
    if pdf2api:
        dst = os.path.join(pngUP, straight_name(bn))
        shutil.copy(itm, dst)
        prnt(f'original -> pngUP STRAIGHT  {os.path.basename(dst)}')

    # png2api: pngPRE -> pngUP copy handled by pdf2png() loop
