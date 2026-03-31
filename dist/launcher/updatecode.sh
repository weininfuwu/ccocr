#!/bin/bash
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 :
#
#   updatecode.sh   260318  cy
#
#   Usage: place this script in the same folder as mkzip.sh
#           (i.e. alongside code/)
#   Run  : ./updatecode.sh <zipfilename>
#   Ex   : ./updatecode.sh ccocr.zip
#
#--------1---------2---------3---------4---------5---------6---------7---------8
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DOWNLOAD_DIR="$HOME/Downloads"
CODE_DIR="$SCRIPT_DIR/code"
TMP_DIR="/tmp/updatecode_tmp"

# 1) ZIP filename from argument
if [ -z "$1" ]; then
    echo "Usage: $0 <zipfilename>"
    echo "  ex : $0 ccocr.zip"
    exit 1
fi
ZIPPATH="$DOWNLOAD_DIR/$1"
if [ ! -f "$ZIPPATH" ]; then
    echo "ERROR: $ZIPPATH not found."
    exit 1
fi

# 2) Extract ZIP into temp folder (/tmp = outside Box Drive, fast)
rm -rf "$TMP_DIR"
mkdir -p "$TMP_DIR"
echo "Extracting: $1"
unzip -q "$ZIPPATH" -d "$TMP_DIR" -x "code/poppler/*"

# 3) Restore from code/ anything not in ZIP (poppler, b64.py, etc.)
if [ -d "$CODE_DIR" ]; then
    if [ -d "$CODE_DIR/poppler" ]; then
        mkdir -p "$TMP_DIR/code/poppler"
        cp -r "$CODE_DIR/poppler/." "$TMP_DIR/code/poppler/"
    fi
    for item in "$CODE_DIR"/*; do
        name="$(basename "$item")"
        [ "$name" = "poppler" ]      && continue
        [ "$name" = ".DS_Store" ]    && continue
        [ -e "$TMP_DIR/code/$name" ] && continue
        cp -r "$item" "$TMP_DIR/code/$name"
    done
fi

# 4) Apply only changed files to code/ via rsync
#    --checksum : compare by content not timestamp (reliable on Box Drive)
#    --delete   : remove files from code/ that no longer exist in ZIP
#    -i         : show only changed/new/deleted files (suppress unchanged)
echo "Applying diff to code/ ..."
rsync -ai --checksum --delete \
    --exclude="poppler/" \
    --exclude=".DS_Store" \
    "$TMP_DIR/code/" "$CODE_DIR/" | grep -v '^\.' || true

# 5) Clean up temp folder
rm -rf "$TMP_DIR"
echo "Done."
