# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**ccocr** is a Python-based OCR document processing system. It reads PDF/image documents, sends them to Azure Cognitive Services (Computer Vision + Document Intelligence APIs), and extracts structured data defined by an Excel configuration file. Output is written to SQLite databases and Excel files.

## Repository Structure

```
ccocr/
├── code/               main.py から始まる一連の処理
├── dist/
│   ├── launcher/       ccocr.exe 生成材料一式 (ccocr.ps1, make_exe.ps1, make_ico.ps1, MinGit/)
│   ├── sample/         サンプル設定Excel・帳票・テスト画像
│   └── doc/            取扱説明書・プログラム仕様書
├── CLAUDE.md
└── .gitignore
```

## Running the Application

All code lives under `code/`. The entry point is `code/main.py`.

**Standalone mode** (interactive, Windows-targeted):
```
python main.py <sysFld> <flwid> <appname>
```

**Embedded mode** (called as subprocess):
```
python main.py --sysFld <path> --flwid <id> --appname <name> [--mymail <email>] [--jobid <id>] [--flwd <path>] [--logd <path>] [--logf <path>] [--idx <n>] [--config <path>] [--embedded]
```

- `sysFld`: root system folder (contains `log/`, `output/`, etc.)
- `flwid`: flow ID identifying which form definition to use
- `appname`: application name
- Credentials for Azure APIs are stored in Windows keyring and loaded during `setup_flds()`

## Installing Dependencies

```
pip install -r code/requirements.txt
```

Poppler binaries for PDF conversion are bundled at `code/poppler/` (Windows).

## Code Style

Every file uses this vim modeline convention (4-space indent, Unix line endings, UTF-8):
```
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
```

Dates in comments use YYMMDD format (e.g., `260224` = 2026-02-24).

## Architecture

### Global State

Two class-based singletons hold all runtime state (no instances — class attributes used directly):

- **`m.env.D`** — system-level: `sysFld`, `flwid`, `jobid`, `logd`, `logf`, `EMBEDDED`, etc.
- **`jobs.env.DD`** — job-level: `jobtyp` (`'frm'`/`'txt'`), API engine config, all working directory paths (`inputd`, `pngPRE`, `pngUP`, `jsn`, `dbf`, etc.)

Both are populated progressively as the pipeline stages execute.

### Pipeline (form mode `frm`)

```
loadxl()        → parse Excel config → DD.jobtyp, DD.engines, form definitions
mv2input()      → copy user files to /input/, parse _dd sheet → returns msconf
setup_flds()    → create working dirs, load Azure credentials into DD
docopy()        → check cache; if False, run:
  pdf2png()     → convert PDFs to PNGs into pngPRE/, pngUP/
  svjsn()       → call Azure CV + DI APIs, save responses to jsnRAW/
aby(msconf)     → main processing:
  sorter()      → match pages to document definitions, build sorter.db
  oos()         → mark out-of-scope pages
  digdb()       → extract structured data → SQLite db
  writexl_*()   → generate output Excel (debug, macro, plain)
  flsk_xl()     → launch Flask viewer
```

For text mode (`txt`): `setup_flds → mv2input → pdf2png → svjsn → jsn2txt`

### Module Map

| Path | Responsibility |
|------|---------------|
| `m/prnt.py` | Unified logging to console + `D.logf` file |
| `m/setup.py` | Parse CLI args, initialize `D`, create log dir |
| `m/msg.py` | GUI dialogs: `finish()`, `abend()` (tkinter, Windows) |
| `m/toys.py` | Interactive file/folder selection dialogs |
| `m/kickPS.py` | Execute PowerShell scripts and capture stdout |
| `jobs/control.py` | Top-level pipeline orchestrator |
| `jobs/loadxl/` | Read Excel config file |
| `jobs/mv2input/` | Copy input files, parse form sheet (`_dd`) |
| `jobs/setup_flds/` | Create directory tree, load Azure credentials |
| `jobs/pdf2png/` | PDF → PNG via pdf2image/poppler |
| `jobs/docopy/` | Cache check — copy prior results to skip re-OCR |
| `jobs/util/svjsn/` | Azure API calls: `updn_cv.py` (Vision), `updn_di.py` (DI) |
| `jobs/util/svjsn/chk_cv/` | Validate Vision API JSON structure |
| `jobs/util/svjsn/chk_di/` | Validate Document Intelligence JSON structure |
| `jobs/aby/sorter/` | Identify documents and page ranges from OCR results |
| `jobs/aby/digdb/` | Extract structured form fields into SQLite |
| `jobs/aby/digdb/digin/` | Input processing: top-level (`d_top/`) and nested fields (`d_blw/`) |
| `jobs/aby/use_web/` | Flask web interface for visual review |
| `jobs/aby/writexl_*.py` | Excel output generators (debug/macro/plain) |
| `jobs/txtmode/` | Text-only mode: `jsn2txt.py`, `twoup.py` (two-page spreads) |

### Azure API JSON Schemas

`jobs/env.py` defines `jkvs.CV` and `jkvs.DI` — these document the exact JSON key structure expected from Azure Vision API v3.2.0 and Document Intelligence API v2024-11-30 (`prebuilt-read` model). The `chk_cv/` and `chk_di/` validators enforce these schemas.

### Logging

All output goes through `m.prnt.prnt()`. Logs are written to `<sysFld>/log/<jobid>/<jobid>.txt`. Console output is color-coded with ANSI codes.
