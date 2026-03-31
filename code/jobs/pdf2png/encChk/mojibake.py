#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   mojibake.py     260319  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import os
import json
import re
from dataclasses    import dataclass
from datetime       import datetime

from m.prnt import prnt

@dataclass
class Config:
    DEBUG:              bool = False
    LOG_MOJIBAKE:       bool = True
    AUTO_CORRECT:       bool = True
    OUTPUT_JSON:        bool = False
    MOJIBAKE_LOG_FILE:  str  = "mojibake_patterns.json"

config = Config()

class MojibakeFixer:
    """文字化け修正エンジン"""

    PATTERNS = {
        # 完全一致パターン
        "俵俽僑僔僢僋": "MS-Gothic",
        "俵俽僐儞僉僽": "MS-Mincho",
        "俵俽儅儞儈僗": "MS-PGothic",
        "俵俽僷僀儖僟": "MS-PMincho",
        "俵俽僆僙僗":   "MS-UIGothic",
        "俵俽僆儞僉僽": "MS-UIMincho",
        "MS 柧挬":      "MS-PGothic",
        "MS 槧怤":      "MS-UIGothic",
        "MS 樠柧":      "MS-PMincho",
        # 部分置換パターン
        "俵俽":   "MS",
        "僑僔僢僋": "Gothic",
        "僐儞僉僽": "Mincho",
        "儅儞儈僗": "PGothic",
        "僷僀儖僟": "PMincho",
        "僆僙僗":   "UIGothic",
        "僆儞僉僽": "UIMincho",
        "柧挬": "PGothic",
        "槧怤": "UIGothic",
        "樠柧": "PMincho",
    }

    NORMALIZATION_RULES = [
        (r"^MS([^-])", r"MS-\1"),
        (r"^ＭＳ",     "MS"),
        (r"-([A-Z])$", r"-\1"),
        (r"\s+",        ""),
    ]

    @classmethod
    def fix(cls, text: str, context: str = "") -> str:
        if not isinstance(text, str):
            return str(text)
        original = text
        result   = text
        for pattern, replacement in sorted(cls.PATTERNS.items(), key=lambda x: -len(x[0])):
            if pattern in result:
                result = result.replace(pattern, replacement)
                if config.DEBUG and original != result:
                    prnt(f"DEBUG: Fixed '{pattern}' -> '{replacement}' in '{original}'")
        if cls._has_suspicious_chars(result):
            corrected = cls._dynamic_fix(result)
            if corrected != result:
                result = corrected
                if config.LOG_MOJIBAKE:
                    cls._log_mojibake(original, result, context)
        result = cls._normalize(result)
        result = result.lstrip("/")
        if config.LOG_MOJIBAKE and original != result and context:
            cls._log_mojibake(original, result, context)
        return result

    @staticmethod
    def _has_suspicious_chars(text: str) -> bool:
        suspicious = set("柧挬槧怤樠橲栧俵俽僑僔僢僋儅儞儈僗僐儞僉僽")
        return any(char in text for char in suspicious)

    @staticmethod
    def _dynamic_fix(text: str) -> str:
        try:
            utf8_bytes = text.encode('utf-8')
            for enc in ['shift_jis', 'cp932', 'euc_jp', 'iso-2022-jp']:
                try:
                    decoded = utf8_bytes.decode(enc, errors='strict')
                    if (decoded and len(decoded) >= 2 and
                            not MojibakeFixer._has_suspicious_chars(decoded)):
                        return decoded
                except:
                    continue
            for enc in ['latin-1', 'ascii']:
                try:
                    decoded = utf8_bytes.decode('latin-1')
                    if 'Gothic' in decoded or 'Mincho' in decoded:
                        return decoded
                except:
                    continue
        except Exception as e:
            if config.DEBUG:
                prnt(f"DEBUG: Dynamic fix failed for '{text}': {e}")
        return text

    @staticmethod
    def _normalize(text: str) -> str:
        result = text
        for pattern, replacement in MojibakeFixer.NORMALIZATION_RULES:
            result = re.sub(pattern, replacement, result)
        return result

    @staticmethod
    def _log_mojibake(original: str, fixed: str, context: str = ""):
        try:
            log_entry = {
                "timestamp":          datetime.now().isoformat(),
                "original":           original,
                "fixed":              fixed,
                "context":            context,
                "original_bytes":     original.encode('utf-8').hex() if isinstance(original, str) else "",
                "suggested_encoding": "shift_jis",
            }
            log_file = config.MOJIBAKE_LOG_FILE
            data = []
            if os.path.exists(log_file):
                try:
                    with open(log_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                except:
                    data = []
            data.append(log_entry)
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            if config.DEBUG:
                prnt(f"DEBUG: Failed to log mojibake: {e}")
