"""Extract explicit "N U.S.C. M" citations from CFR section text (banking port, step 1).

Deterministic. The IRC extractor (citations.py) resolves bare "section N" to the Internal
Revenue Code, a convention banking rules don't share; here only citations that name their
title are read. Forms come from a survey of 12 CFR (1997, 2010, 2025) and 31 CFR (2025) on
2026-10-16: a title, "U.S.C.", an optional "App." or section sign, then a list of sections,
each with designators (reusing citations.chain), "et seq." or "note".

A hyphen inside a section number is ambiguous: 15 U.S.C. 78fff-3 is a section, 50 U.S.C.
1701-1706 is a range. The extractor keeps the token whole and flags it ``hyphen``; the
resolver decides against the statute.
"""

import re

from levadura_salvaje.citations import chain, normalize

VERSION = "1"

HEAD = re.compile(r"\b(\d{1,2}) U\.\s?S\.\s?C\.?(?:A\.)?\s*([Aa]pp\.?\s*)?(?:§§?\s*|[Ss]ec(?:tion|\.)\s+)?")
SECNUM = re.compile(r"(\d+[A-Za-z]{0,4}(?:-\d+[A-Za-z]{0,4})?)(?![A-Za-z0-9])")
# What a section number must not be followed by: another title's "U.S.C.", a CFR, Stat. or FR
# cite, a regulation number ("925.6"), or a count.
REJECT = re.compile(r"\s?\.\d| U\.\s?S\.\s?C\.| CFR\b| Stat\.| FR\b"
                    r"|\s+(?:percent|days|months|years|dollars)\b")
SEP = re.compile(r",\s*(?:(?:and|or)\s+)?|\s+(?:and|or)\s+")
ET_SEQ = re.compile(r"\s*et seq\.?")
NOTE = re.compile(r"\s+note\b")


def _one(text: str, pos: int):
    """A section with its designators at pos, or None."""
    m = SECNUM.match(text, pos)
    if not m or REJECT.match(text, m.end()):
        return None
    toks, levels, end, flags = chain(text, m.end(), first_digit_ok=False)
    item = {"section": m.group(1), "desig": toks, "levels": levels, "start": m.start(),
            "flags": set(flags), "et_seq": False, "note": False}
    if "-" in m.group(1):
        item["flags"].add("hyphen")
    if e := ET_SEQ.match(text, end):
        item["et_seq"], end = True, e.end()
    elif n := NOTE.match(text, end):
        item["note"], end = True, n.end()
    item["end"] = end
    return item


def extract(text: str, normalized: bool = False) -> list[dict]:
    if not normalized:
        text = normalize(text)
    out = []
    for h in HEAD.finditer(text):
        title, app = str(int(h.group(1))), bool(h.group(2))
        item = _one(text, h.end())
        if item is None:
            continue
        items, pos = [item], item["end"]
        while (s := SEP.match(text, pos)) and (nxt := _one(text, s.end())):
            items.append(nxt)
            pos = nxt["end"]
        for i, it in enumerate(items):
            start = h.start() if i == 0 else it["start"]
            span_end = it["end"]
            if it["et_seq"] or it["note"]:  # the span is the citation, not its trailing words
                span_end = it["start"] + len(it["section"]) + sum(len(t) + 2 for t in it["desig"])
            out.append({
                "title": title, "app": app,
                "path": "/".join([it["section"], *it["desig"]]),
                "section": it["section"], "desig": it["desig"], "levels": it["levels"],
                "span": [start, span_end], "et_seq": it["et_seq"], "note": it["note"],
                "flags": sorted(it["flags"]),
            })
    return out


def resolve(cite: dict, statutes: dict) -> dict:
    """Resolve one citation against {title: resolve.Statute}. Titles not held, and the
    pre-1958 appendices (not in USLM's main titles), are reported as such, not as breaks.
    A hyphenated token is first tried as one section; failing that, as a range a-b, which
    resolves only if both ends do, the worse end's outcome otherwise."""
    if cite["app"]:
        return {"outcome": "appendix"}
    st = statutes.get(cite["title"])
    if st is None:
        return {"outcome": "title-not-held"}
    whole = st.resolve(cite["path"])
    if "hyphen" not in cite["flags"] or whole["outcome"] != "absent-section" or cite["desig"]:
        return whole
    lo, hi = cite["section"].split("-", 1)
    ends = [st.resolve(lo)["outcome"], st.resolve(hi)["outcome"]]
    if ends == ["resolves", "resolves"]:
        return {"outcome": "resolves", "via": "range", "ends": ends}
    return {"outcome": next(e for e in ends if e != "resolves"), "via": "range", "ends": ends}
