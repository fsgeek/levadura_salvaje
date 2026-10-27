"""Citations marked as old law, and mentions of the AIA's transition dates (patents v2).

A citation is marked as old law by a stated date before the AIA's effective date for 102/103
(2013-03-16), "as in effect on/prior to/before <date>" within 150 characters after it, or by
"pre-AIA" within 20 characters before it. A mention of March 15 or 16, 2013 is "conditioned" if its
sentence states an applicability test (effective filing date, claimed invention, contains or
contained, at any time, ever contained), else "date-only". v1 fixes from its dry run, before any ledger entry: a date after a list of subsections ("102(e), (f),
or (g) in effect prior to…"); "contains, or contained" with a comma. Deterministic. Limits: a date stated
further away, or in another sentence, isn't seen; nor is old law implied only by context
(the interference rules cite 102(g) with no date); "conditioned" is lexical.
"""

import re
from datetime import date

VERSION = "1"
AIA_102 = date(2013, 3, 16)
_MONTHS = {m: i for i, m in enumerate(("January", "February", "March", "April", "May", "June", "July", "August",
                                       "September", "October", "November", "December"), 1)}
_DATE = r"(" + "|".join(_MONTHS) + r")\s+(\d{1,2}),\s+(\d{4})"
STATED = re.compile(r"(?:,?\s*(?:or|and)?\s*\([a-z0-9]{1,3}\))*[\s,]*(?:\([^)]{0,40}\)\s*)?(?:as\s+)?in\s+effect\s+(on|prior\s+to|before)\s+" + _DATE)
PRE_AIA = re.compile(r"pre-AIA\s*$")
TRANSITION = re.compile(r"March\s+1[56],\s+2013")
CONDITION = re.compile(r"effective\s+filing\s+date|claimed\s+invention|contains?,?\s+or\s+contained|at\s+any\s+time|"
                       r"ever\s+contained", re.I)


def marker(text: str, span: tuple[int, int]) -> dict:
    a, b = span
    m = STATED.match(text[b:b + 150])
    if m:
        d = date(int(m.group(4)), _MONTHS[m.group(2)], int(m.group(3)))
        if d < AIA_102 or (d == AIA_102 and m.group(1) != "on"):
            return {"marker": "date", "date": d.isoformat()}
    if PRE_AIA.search(text[max(0, a - 20):a]):
        return {"marker": "pre-AIA", "date": None}
    return {"marker": None, "date": None}


def transition_mentions(text: str) -> list[dict]:
    out = []
    for m in TRANSITION.finditer(text):
        s = text.rfind(". ", 0, m.start()) + 1
        e = text.find(". ", m.end())
        sentence = text[s:e if e >= 0 else len(text)]
        out.append({"span": [m.start(), m.end()], "class": "conditioned" if CONDITION.search(sentence) else "date-only"})
    return out
