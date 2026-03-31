#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   ext.py      260319  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import os
import glob
import json
from pathlib    import Path

from m.prnt         import prnt
from .mojibake      import config
from .pdf_analyzer  import PDFAnalyzer

def analyze_pdf_detailed(pdf_path: str, output_json: bool = False) -> dict:
    analyzer = PDFAnalyzer(pdf_path)
    results  = analyzer.analyze_all_pages()
    if output_json:
        json_file = f"{Path(pdf_path).stem}_analysis.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        prnt(f"Analysis saved to: {json_file}")
    prnt(f"\n{'='*60}")
    prnt(f"PDF Analysis Summary: {os.path.basename(pdf_path)}")
    prnt(f"{'='*60}")
    prnt(f"Total pages: {results['total_pages']}")
    prnt(f"Has 90ms-RKSJ-H: {results['summary']['has_90ms_rksj']}")
    prnt(f"Has CID fonts: {results['summary']['has_cid_fonts']}")
    prnt(f"Unique encodings: {', '.join(sorted(results['summary']['unique_encodings']))}")
    prnt(f"Unique fonts: {', '.join(sorted(results['summary']['unique_fonts']))}")
    prnt(f"{'='*60}")
    return results

def batch_analyze(pattern: str = "*.pdf", output_dir: str = "pdf_reports"):
    import csv
    os.makedirs(output_dir, exist_ok=True)
    pdf_files = glob.glob(pattern)
    if not pdf_files:
        prnt(f"No PDF files found matching pattern: {pattern}")
        return
    results_summary = []
    for pdf_file in pdf_files:
        try:
            prnt(f"\nAnalyzing: {pdf_file}")
            results = analyze_pdf_detailed(pdf_file, output_json=False)
            summary = {
                "file":          os.path.basename(pdf_file),
                "pages":         results["total_pages"],
                "has_90ms_rksj": results["summary"]["has_90ms_rksj"],
                "has_cid_fonts": results["summary"]["has_cid_fonts"],
                "encodings":     ";".join(sorted(results["summary"]["unique_encodings"])),
                "fonts":         ";".join(sorted(results["summary"]["unique_fonts"])),
            }
            results_summary.append(summary)
        except Exception as e:
            prnt(f"Error analyzing {pdf_file}: {e}")
    if results_summary:
        csv_file = os.path.join(output_dir, "pdf_analysis_summary.csv")
        with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
            fieldnames = ["file", "pages", "has_90ms_rksj", "has_cid_fonts", "encodings", "fonts"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results_summary)
        prnt(f"\nSummary saved to: {csv_file}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="PDFフォントエンコーディング分析ツール")
    parser.add_argument("input",     nargs="?",          help="入力PDFファイル")
    parser.add_argument("--batch",                        help="バッチ処理（例: '*.pdf'）")
    parser.add_argument("--detailed", action="store_true", help="詳細分析")
    parser.add_argument("--json",     action="store_true", help="JSON出力")
    parser.add_argument("--debug",    action="store_true", help="デバッグモード")
    parser.add_argument("--output",                        help="出力ディレクトリ")
    args = parser.parse_args()
    if args.debug:
        config.DEBUG = True
    if args.output:
        config.MOJIBAKE_LOG_FILE = os.path.join(args.output, "mojibake_patterns.json")
    if args.batch:
        batch_analyze(args.batch, args.output or "pdf_reports")
    elif args.input:
        if args.detailed:
            analyze_pdf_detailed(args.input, args.json)
        else:
            from .encChk import encChk
            result = encChk(args.input)
            prnt(f"\n最終結果: {result[0]}")
    else:
        parser.print_help()
