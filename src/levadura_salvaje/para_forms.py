"""How a citation to one U.S.C. section names its subdivision (patents transfer study, I5).

The America Invents Act renumbered 35 U.S.C. 112's unnumbered paragraphs as (a)-(f), so "112,
sixth paragraph" became "112(f)". Each explicit citation of the section is classed as "letter"
(112(f)), "ordinal" (sixth paragraph, ¶ 6, paragraph 6, 112(6), or "the first paragraph of 35 U.S.C. 112")
or "bare" (no subdivision). Deterministic. Limits: only explicit "N U.S.C." citations; an ordinal
far from the citation is not seen.
"""

import re

from levadura_salvaje import usc_cites

VERSION = "1"
_ORD = r"(?:first|second|third|fourth|fifth|sixth)"
AFTER = re.compile(rf",?\s*(?:{_ORD}\s+paragraph|¶+\s*\d|paragraphs?\s+\d)", re.I)
BEFORE = re.compile(rf"\b{_ORD}\s+paragraph\s+of\s+$", re.I)


def forms(text: str, title: str, section: str, normalized: bool = False) -> list[dict]:
    if not normalized:
        text = usc_cites.normalize(text)
    out = []
    for c in usc_cites.extract(text, normalized=True):
        if c["title"] != title or c["section"] != section:
            continue
        a, b = c["span"]
        if c["desig"] and c["desig"][0].isdigit():
            form = "ordinal"  # "112(6)": a paragraph number in parentheses (found in v1's dry run, 37 CFR 41.110)
        elif c["desig"]:
            form = "letter"
        elif AFTER.match(text, b) or BEFORE.search(text[max(0, a - 40):a]):
            form = "ordinal"
        else:
            form = "bare"
        out.append({"form": form, "span": [a, b], "desig": c["desig"]})
    return out
