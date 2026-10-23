"""Act-section citations paired with the U.S.C. citation written right after them.

Banking rules often cite both ways at once: "section 8(b) of the Federal Deposit Insurance Act
(12 U.S.C. 1818(b))". The two halves should name the same law. The map from an act's section
to its Code section is taken from the corpus itself: for each (act as written, act section), the
consensus U.S.C. section across every pair. A pair that disagrees with a strong consensus is a
candidate wrong address. A blind audit decides whether it is one.

v2 (after audit A2): a U.S.C. citation marked "et seq." or "note" names a whole act, so it doesn't
pair with one section; nor does a U.S.C. citation that is one item of a list, since the program
can't tell which item the act section means; and "the Act" is read (resolved per part, by
act_names).

v3 (after audit A3): a range names the whole act too. "50 U.S.C. 1701 through 1706" never pairs;
a hyphenated token ("1701-1706", but also "78o-11") pairs only if ``is_section`` says the statute
has it as one section, so a range in a title not held is left unpaired. And "section 4(s)" is
re-keyed as section 4s where it would otherwise disagree and the corpus itself maps 4s to the
cited U.S.C. section (``rekey_letters``).

Limits: only singular "section N of the <Name> Act|Code"; the act is keyed as written
(locally defined short names such as "the Bank Act" are not merged with their long forms);
the map is at section level, not subdivision.
"""

import re
from collections import Counter

from levadura_salvaje import usc_cites

VERSION = "3"

_WORD = r"(?:[A-Z][\w.'&-]*|of|and|for|the|on|to|in)"
ACT_CITE = re.compile(
    r"\b[Ss]ection\s+(\d+[A-Za-z]{0,3}(?:-\d+)?)((?:\([A-Za-z0-9]{1,6}\))*)\s+of\s+the\s+"
    rf"((?:[A-Z][\w.'&-]*(?:,?\s+{_WORD})*?\s+)?(?:Act|Code)(?:\s+of\s+\d{{4}})?)(?![\w-])")
BRIDGE = re.compile(r"\s*,?\s*\(?\s*")
WORDED_RANGE = re.compile(r"\s*(?:through|to|thru)\s+\d")


def pairs(text: str, normalized: bool = False, is_section=None) -> list[dict]:
    """``is_section(title, section) -> bool`` decides hyphenated tokens (v3). Without it they
    pair as in v2."""
    if not normalized:
        text = usc_cites.normalize(text)
    out = []
    for m in ACT_CITE.finditer(text):
        b = BRIDGE.match(text, m.end()).end()
        cites = usc_cites.extract(text[b:b + 200], normalized=True)
        if not cites or cites[0]["span"][0] != 0:
            continue
        c = cites[0]
        if c["et_seq"] or c["note"] or (len(cites) > 1 and cites[1]["group"] == c["group"]):
            continue
        if WORDED_RANGE.match(text, b + c["span"][1]):
            continue
        if is_section is not None and "hyphen" in c["flags"] and not is_section(c["title"], c["section"]):
            continue
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


def rekey_letters(ps: list[dict], cons: dict) -> list[dict]:
    """Read "section 4(s)" as section 4s where the pair disagrees with the consensus for (act, "4")
    and the consensus for (act, "4s") is the very U.S.C. section it cites. Only a disagreement is
    re-read: "section 10(a)" of HOLA at 1467a(a) is subsection (a) of section 10, and stays so
    (found in v3's dry run, before any ledger entry). Everything else is returned unchanged."""
    out = []
    for p in ps:
        d = p["act_desig"]
        if d and re.fullmatch(r"[a-z]{1,2}", d[0]):
            here = (p["title"], p["usc_section"])
            base = cons.get((p["act"], p["act_section"]))
            c = cons.get((p["act"], p["act_section"] + d[0]))
            if base and base["target"] != here and c and c["target"] == here:
                p = dict(p, act_section=p["act_section"] + d[0], act_desig=d[1:], rekeyed=True)
        out.append(p)
    return out
