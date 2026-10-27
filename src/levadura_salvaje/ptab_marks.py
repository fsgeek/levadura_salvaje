"""How a PTAB decision marks the patent law it applies (ptab v1).

"marked": "pre-AIA" appears (any dash). "basis": "March 16, 2013" or "effective filing date" appears.
"old_subdivision": a citation of 35 U.S.C. § 103(a), or § 102(e), (f) or (g): forms that exist only in
pre-AIA law (AIA § 103 has no subsections). Deterministic, over pdftotext output with whitespace collapsed.
Limits: lexical; "§ 103(a)" in a quotation of old law counts; an OCR-damaged citation is missed.
"""

import re

VERSION = "1"
MARKED = re.compile(r"\bpre\s?[-‐‑–—]\s?AIA\b", re.I)
BASIS = re.compile(r"March\s+16,\s+2013|effective\s+filing\s+date", re.I)
OLD = re.compile(r"35\s+U\.\s?S\.\s?C\.\s*§§?\s*(?:103\s*\(a\)|102\s*\([efg]\)|[\d()a-z\s,§]*?\b102\s*\([efg]\))")


def marks(text: str) -> dict:
    return {"marked": bool(MARKED.search(text)), "basis": bool(BASIS.search(text)),
            "old_subdivision": bool(OLD.search(text))}
