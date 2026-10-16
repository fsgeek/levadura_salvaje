"""Act-section citations paired with the U.S.C. citation written right after them.

Banking rules often cite both ways at once: "section 8(b) of the Federal Deposit Insurance Act
(12 U.S.C. 1818(b))". The two halves should name the same law. The map from an act's section
to its Code section is taken from the corpus itself: for each (act as written, act section), the
consensus U.S.C. section across every pair. A pair that disagrees with a strong consensus is a
candidate wrong address. A blind audit decides whether it is one.

v1 limits: only singular "section N of the <Name> Act|Code"; the act is keyed as written
(locally defined short names such as "the Bank Act" are not merged with their long forms);
"the Act" is not read; the map is at section level, not subdivision.
"""

import re
from collections import Counter

from levadura_salvaje import usc_cites

VERSION = "1"

_WORD = r"(?:[A-Z][\w.'&-]*|of|and|for|the|on|to|in)"
ACT_CITE = re.compile(
    r"\b[Ss]ection\s+(\d+[A-Za-z]{0,3}(?:-\d+)?)((?:\([A-Za-z0-9]{1,6}\))*)\s+of\s+the\s+"
    rf"([A-Z][\w.'&-]*(?:\s+{_WORD})*?\s+(?:Act|Code)(?:\s+of\s+\d{{4}})?)(?![\w-])")
BRIDGE = re.compile(r"\s*,?\s*\(?\s*")


def pairs(text: str, normalized: bool = False) -> list[dict]:
    if not normalized:
        text = usc_cites.normalize(text)
    out = []
    for m in ACT_CITE.finditer(text):
        b = BRIDGE.match(text, m.end()).end()
        cites = usc_cites.extract(text[b:b + 200], normalized=True)
        if not cites or cites[0]["span"][0] != 0:
            continue
        c = cites[0]
        out.append({"act": m.group(3), "act_section": m.group(1),
                    "act_desig": re.findall(r"\(([^)]+)\)", m.group(2)),
                    "title": c["title"], "usc_section": c["section"], "usc_path": c["path"],
                    "span": [m.start(), b + c["span"][1]], "flags": c["flags"]})
    return out


def consensus(ps: list[dict], min_n: int = 3, min_share: float = 0.75) -> dict:
    """{(act, act_section): {"target": (title, usc_section), "n", "share"}} where a strong
    majority of at least min_n pairs agree."""
    groups: dict[tuple, Counter] = {}
    for p in ps:
        groups.setdefault((p["act"], p["act_section"]), Counter())[(p["title"], p["usc_section"])] += 1
    out = {}
    for key, cnt in groups.items():
        n = sum(cnt.values())
        target, k = cnt.most_common(1)[0]
        if n >= min_n and k / n >= min_share:
            out[key] = {"target": target, "n": n, "share": round(k / n, 4)}
    return out
