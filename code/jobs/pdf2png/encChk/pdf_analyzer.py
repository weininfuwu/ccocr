#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   pdf_analyzer.py     260319  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

from dataclasses    import dataclass
from typing         import Any, Dict, Optional

from pypdf          import PdfReader
from pypdf.generic  import IndirectObject

from m.prnt         import prnt
from .mojibake      import config, MojibakeFixer

@dataclass
class FontInfo:
    name:            str
    subtype:         str
    encoding:        str
    base_font:       str
    cid_system_info: Optional[Dict] = None
    is_type0:        bool = False
    is_cid:          bool = False

class PDFAnalyzer:
    """PDF解析クラス"""

    def __init__(self, pdf_path: str):
        self.pdf_path   = pdf_path
        self.reader     = PdfReader(pdf_path, strict=False)
        self.font_cache: Dict[str, FontInfo] = {}

    def analyze_page(self, page_num: int) -> Dict[str, Any]:
        if page_num < 0 or page_num >= len(self.reader.pages):
            return {"error": f"Invalid page number: {page_num}"}
        page   = self.reader.pages[page_num]
        result = {
            "page_number":   page_num + 1,
            "fonts":         [],
            "encodings":     set(),
            "has_90ms_rksj": False,
            "has_cid_fonts": False,
        }
        resources = self._dereference(page.get("/Resources"))
        if not resources:
            return result
        fonts = self._dereference(resources.get("/Font"))
        if not fonts:
            return result
        for font_key, font_ref in fonts.items():
            font_info = self._analyze_font(font_key, font_ref, page_num)
            if font_info:
                result["fonts"].append(font_info)
                if font_info["encoding"]:
                    result["encodings"].add(font_info["encoding"])
                if font_info["encoding"] == "90ms-RKSJ-H":
                    result["has_90ms_rksj"] = True
                if font_info["is_cid"]:
                    result["has_cid_fonts"] = True
        return result

    def analyze_all_pages(self) -> Dict[str, Any]:
        results = {
            "pdf_path":    self.pdf_path,
            "total_pages": len(self.reader.pages),
            "pages":       [],
            "summary": {
                "has_90ms_rksj":    False,
                "has_cid_fonts":    False,
                "unique_encodings": set(),
                "unique_fonts":     set(),
                "fonts_by_page":    {},
            }
        }
        for page_num in range(len(self.reader.pages)):
            page_result = self.analyze_page(page_num)
            results["pages"].append(page_result)
            if page_result.get("has_90ms_rksj"):
                results["summary"]["has_90ms_rksj"] = True
            if page_result.get("has_cid_fonts"):
                results["summary"]["has_cid_fonts"] = True
            results["summary"]["unique_encodings"].update(page_result.get("encodings", set()))
            for font in page_result.get("fonts", []):
                font_name = font.get("base_font", "")
                if font_name:
                    results["summary"]["unique_fonts"].add(font_name)
            fonts_on_page = [f.get("base_font", "") for f in page_result.get("fonts", [])]
            results["summary"]["fonts_by_page"][page_num + 1] = fonts_on_page
        results["summary"]["unique_encodings"] = list(results["summary"]["unique_encodings"])
        results["summary"]["unique_fonts"]     = list(results["summary"]["unique_fonts"])
        return results

    def _dereference(self, obj: Any) -> Any:
        if isinstance(obj, IndirectObject):
            return obj.get_object()
        return obj

    def _get_string(self, obj: Any, context: str = "") -> str:
        if obj is None:
            return ""
        obj = self._dereference(obj)
        raw_str = ""
        if hasattr(obj, "name"):
            name_obj = obj.name
            if isinstance(name_obj, bytes):
                try:
                    raw_str = name_obj.decode('shift_jis', errors='replace')
                except:
                    try:
                        raw_str = name_obj.decode('utf-8', errors='replace')
                    except:
                        raw_str = str(name_obj)
            else:
                raw_str = str(name_obj)
        elif isinstance(obj, (str, bytes)):
            if isinstance(obj, bytes):
                try:
                    raw_str = obj.decode('shift_jis', errors='replace')
                except:
                    try:
                        raw_str = obj.decode('utf-8', errors='replace')
                    except:
                        raw_str = str(obj)
            else:
                raw_str = obj
        else:
            raw_str = str(obj)
        if config.AUTO_CORRECT:
            return MojibakeFixer.fix(raw_str, context)
        return raw_str.lstrip("/")

    def _analyze_font(self, font_key: str, font_ref: Any, page_num: int) -> Optional[Dict]:
        font_dict = self._dereference(font_ref)
        if not hasattr(font_dict, "get"):
            return None
        subtype   = self._get_string(font_dict.get("/Subtype"),  f"Subtype on page {page_num+1}")
        base_font = self._get_string(font_dict.get("/BaseFont"), f"BaseFont on page {page_num+1}")
        encoding  = self._get_string(font_dict.get("/Encoding"), f"Encoding on page {page_num+1}")
        is_type0  = (subtype == "Type0")
        is_cid    = False
        cid_info  = None
        if is_type0:
            desc = self._dereference(font_dict.get("/DescendantFonts"))
            if isinstance(desc, list) and desc:
                cid_font = self._dereference(desc[0])
                if hasattr(cid_font, "get"):
                    cid_info = {}
                    is_cid   = True
                    cid_system = self._dereference(cid_font.get("/CIDSystemInfo"))
                    if cid_system and hasattr(cid_system, "get"):
                        cid_info["registry"]   = self._get_string(cid_system.get("/Registry"))
                        cid_info["ordering"]   = self._get_string(cid_system.get("/Ordering"))
                        cid_info["supplement"] = self._get_string(cid_system.get("/Supplement"))
        cache_key = f"{base_font}:{subtype}:{encoding}"
        if cache_key in self.font_cache:
            font_info = self.font_cache[cache_key]
        else:
            font_info = FontInfo(
                name=font_key, subtype=subtype, encoding=encoding,
                base_font=base_font, cid_system_info=cid_info,
                is_type0=is_type0, is_cid=is_cid)
            self.font_cache[cache_key] = font_info
        return {
            "key":             font_key,
            "subtype":         font_info.subtype,
            "base_font":       font_info.base_font,
            "encoding":        font_info.encoding,
            "is_type0":        font_info.is_type0,
            "is_cid":          font_info.is_cid,
            "cid_system_info": font_info.cid_system_info,
        }
