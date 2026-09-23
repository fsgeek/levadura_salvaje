"""The AMT baseline: a keyword and citation matcher, no classifier.

Defined in predictions/2026-09-23-amt-lens-claude.md before any corpus text
was searched. A section is positive if it contains one of PHRASES, or cites
Code section 53, 55, 56, 56A, 57, 58 or 59 -- any subsection, never 59A.
Citations are read from "section"/"sections" followed by a list, so
"sections 1, 55 and 56" finds 55 and 56.
"""

import re

VERSION = "1"
PHRASES = (
    "alternative minimum tax",
    "minimum taxable income",
    "tentative minimum tax",
    "minimum tax credit",
    "tax preference",
)
CODE_SECTIONS = {"53", "55", "56", "56A", "57", "58", "59"}

_PHRASE = re.compile("|".join(re.escape(p) for p in PHRASES), re.I)
_ITEM = r"[0-9][0-9A-Za-z]*(?:\([0-9A-Za-z]+\))*"
_CITES = re.compile(
    rf"\bsections?\s+({_ITEM}(?:(?:\s*,\s*(?:and\s+|or\s+)?|\s+(?:and|or|through)\s+){_ITEM})*)"
)
_HEAD = re.compile(r"[0-9][0-9A-Za-z]*")


def match(text: str) -> dict:
    """Return the phrases and AMT Code sections found in ``text``."""
    phrases = sorted({m.group(0).lower() for m in _PHRASE.finditer(text)})
    cited = set()
    for run in _CITES.finditer(text):
        for item in re.findall(_ITEM, run.group(1)):
            head = _HEAD.match(item).group(0)
            if head in CODE_SECTIONS:
                cited.add(head)
    return {"positive": bool(phrases or cited), "phrases": phrases, "cites": sorted(cited)}
