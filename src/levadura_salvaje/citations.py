"""Extract citations of the Internal Revenue Code from 26 CFR section text.

Deterministic; implements docs/citation-extractor-spec.md (v1), written from
a blind survey of 240 random 2025 sections. Section references (§N) point
there. Each record's ``path`` is a Code section plus its designators in
order (``56/b/1/A``), checked against USLM as ``/us/usc/t26/s`` + path.

v2 adds three forms found by the blind audit of v1: citations qualified by
or prefixed with another statute's acronym or name ("of ERISA", "of TRA",
"ERISA section 4044", "PHS Act section 2793"); "of such Code" when the
nearest Code named before it is the 1939 Code; and sibling designators that
belong to "... of this section", which are dropped.

Known departures from the spec: the GLOSS skip uses a balanced-parenthesis
scan (any depth) rather than the spec's one-level regex, and section ranges
are resolved by their endpoints only (the interior is not enumerated here or
by the checker).
"""

import re

VERSION = "2"

# --- §1 normalization -------------------------------------------------------

_SPACES = re.compile(r"[\s  -​  　]+")
_ITALIC = re.compile(r"\(\s+([A-Za-z0-9]{1,6})\s+\)")
_DOUBLED = re.compile(r"\b[Ss]ection\s+§")


def normalize(text: str) -> str:
    text = _SPACES.sub(" ", text).strip()
    text = _ITALIC.sub(r"(\1)", text)
    return _DOUBLED.sub("§", text)


# --- §2.1-2.2 tokens and the chain grammar ------------------------------------

SECNUM = re.compile(r"(\d{1,4}(?:[A-Z]{1,2}(?:-\d{1,2})?)?)(?![A-Za-z0-9])")
DESIG = re.compile(r"( ?)\(([a-z]{1,6}|[A-Z]{1,6}|\d{1,3}[A-Z]?)\)")
_ROMAN = re.compile(r"^(?=[ivxl])(x{0,3}|xl|l)(ix|iv|v?i{0,3})$")


def _roman(tok: str) -> bool:
    return bool(_ROMAN.match(tok))


def fits(tok: str, level: int) -> bool:
    if level == 1:
        return len(tok) == 1 and tok.islower()
    if level == 2:
        return bool(re.fullmatch(r"\d{1,3}[A-Z]?", tok))
    if level == 3:
        return bool(re.fullmatch(r"([A-Z])\1?", tok))
    if level == 4:
        return tok.islower() and _roman(tok)
    if level == 5:
        return tok.isupper() and _roman(tok.lower())
    if level == 6:
        return bool(re.fullmatch(r"([a-z])\1", tok))
    return False


def _order(tok: str, level: int) -> int | None:
    """Position of a designator within its level, for range enumeration."""
    if level == 2 and tok.isdigit():
        return int(tok)
    if level in (1, 3) and len(tok) == 1:
        return ord(tok.lower()) - 96
    if level in (4, 5):
        vals = {"i": 1, "v": 5, "x": 10, "l": 50}
        t = tok.lower()
        return sum(-vals[c] if i + 1 < len(t) and vals[c] < vals[t[i + 1]] else vals[c]
                   for i, c in enumerate(t))
    return None


def _emit_order(n: int, level: int) -> str:
    if level == 2:
        return str(n)
    if level in (1, 3):
        c = chr(96 + n)
        return c if level == 1 else c.upper()
    table = [(50, "l"), (40, "xl"), (10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")]
    out = ""
    for v, s in table:
        while n >= v:
            out, n = out + s, n - v
    return out if level == 4 else out.upper()


def chain(text: str, pos: int, level: int = 1, first_digit_ok: bool = True):
    """Parse designators at pos. Return (tokens, levels, end, flags).

    ``level`` is the level expected for the first designator."""
    toks, levels, flags = [], [], set()
    while True:
        m = DESIG.match(text, pos)
        if not m:
            break
        spaced, tok = bool(m.group(1)), m.group(2)
        expected = levels[-1] + 1 if levels else level
        if fits(tok, expected):
            got = expected
        elif not levels and expected == 1 and first_digit_ok and fits(tok, 2):
            got = 2
            flags.add("irregular_chain")
        elif not spaced and (alts := [lv for lv in range(1, 7) if fits(tok, lv)]):
            got = min(alts, key=lambda lv: abs(lv - expected))
            flags.add("irregular_chain")
        else:
            break
        toks.append(tok)
        levels.append(got)
        pos = m.end()
    return toks, levels, pos, flags


# --- helpers ----------------------------------------------------------------------

def skip_parens(text: str, pos: int) -> int:
    """If a balanced parenthetical that is not a lone designator starts at pos
    (after optional spaces), return the position after it; else pos."""
    p = pos
    while p < len(text) and text[p] == " ":
        p += 1
    if p >= len(text) or text[p] != "(" or DESIG.match(text, p):
        return pos
    depth = 0
    for i in range(p, len(text)):
        if text[i] == "(":
            depth += 1
        elif text[i] == ")":
            depth -= 1
            if depth == 0:
                return i + 1
    return pos


SEP = re.compile(r",\s*(?:(?:and|or|and/or)\s+)?|\s+(?:and|or|and/or)\s+")
RSEP = re.compile(r"\s+(?:through|to)\s+|-")
HEAD = re.compile(r"\b[Ss]ections?\b\s*|\b[Ss]ec\.\s*|§(?!§)\s*|\b26 U\.S\.C\.\s*\(?")
BARE_REJECT = re.compile(r"\s?\.\d|,\d|\s?-\s?\d| U\.S\.C\.| Stat\.| CFR| FR\b"
                         r"|\s+(?:percent|days|months|years|dollars)\b")
INVERTED = re.compile(r"\b(?:sub)?(?:section|paragraph|subparagraph|clause|subclause)s?\s+(?=\()")

_CODE_ACRONYMS = r"(?:IRC|FICA|FUTA|SECA|RRTA)\b"
# v2: a head directly after another statute's name ("ERISA section", "PHS Act section")
OTHER_PREFIX = re.compile(rf"\b(?:(?!{_CODE_ACRONYMS})[A-Z]{{2,}}[A-Za-z]*|Act)\s+$")
_ACT = (r"of (?:title [IVXLC\d]+ of )?(?:the )?[A-Z][\w.'&-]*\s+"
        r"(?:(?:[A-Z][\w.'&-]*|of|and|for|the|\d{4})\s+)*Act\b")
EXCLUDE = re.compile(
    r"(?:of the Internal Revenue Code of 1939|,\s*(?:the )?Internal Revenue Code of 1939"
    rf"|{_ACT}|of the Act\b|of (?:Public Law|Pub\. ?L\.)|of the Revised Statutes"
    r"|of title (?!26\b)\d+ of the United States Code|of the convention|of the treaty"
    rf"|of (?:the )?(?!{_CODE_ACRONYMS})[A-Z]{{2,}}[A-Za-z0-9]*\b)")  # v2: "of ERISA", "of TRA"
CHAPTER_SKIP = re.compile(r",?\s*(?:and|or)\s+(?:chapter|subchapter|title|part)\s+[\wIVXLC]+\s+")
CODE_1954 = re.compile(r"\s*(?:of (?:the )?Internal Revenue Code of 1954|,\s*(?:the )?Internal Revenue Code of 1954)")
HISTORICAL_AFTER = re.compile(
    r"\s*(?:of prior law|as in effect (?:on|before|prior)|prior to (?:amendment|repeal)|before amendment"
    r"|\(as in effect before the effective date of its repeal\))")
ATTR_BEFORE = re.compile(r"\b(?:a|an|the|each|any|no|every|its|their|such)\s+$")
STOP = set("and or of to for in on at is are was were be been applies apply applied provides provide "
           "provided does do did shall will may must as with by under through relating concerning "
           "including that which if unless except has have had not requires require described "
           "defined thereunder".split())


class _Group:
    def __init__(self, head: str, start: int):
        self.head, self.start, self.items, self.end = head, start, [], start


def _item(sec: str, toks: list, levels: list, span: tuple, head: str, flags=()) -> dict:
    return {"path": "/".join([sec, *toks]), "section": sec, "desig": list(toks), "levels": list(levels),
            "span": list(span), "head": head, "range": None, "flags": set(flags)}


# --- §2.3-2.4 a group starting at a head --------------------------------------------

def _parse_group(text: str, head_m: re.Match) -> tuple[_Group | None, int]:
    head_txt = head_m.group(0).strip()
    head = ("usc26" if head_txt.startswith("26") else "sign" if head_txt.startswith("§")
            else "sec_abbrev" if head_txt.lower().startswith("sec.") else "section")
    pos = head_m.end()
    m = SECNUM.match(text, pos)
    if not m:
        return None, pos
    after = text[m.end():]
    if re.match(r"\s?\.\d|,\d", after):  # E1: a regulation number
        return None, m.end()
    toks, levels, end, flags = chain(text, m.end())
    g = _Group(head, head_m.start())
    if toks and re.match(r"\s?-\s?\d", text[end:]):  # E2: part prefix missing
        return None, end
    if not toks and (r := re.match(r"-(\d{1,4})(?![A-Za-z0-9.])", text[end:])):
        a, b = m.group(1), r.group(1)
        if head == "section" and a.isdigit() and int(b) > int(a):
            g.items += [_item(a, [], [], (m.start(), m.end()), head),
                        _item(b, [], [], (end + 1, end + r.end()), head)]
            g.items[-1]["range"] = {"from": a, "to": b, "level": "section"}
            g.end = end + r.end()
            return _continue(text, g), g.end
        return None, end
    g.items.append(_item(m.group(1), toks, levels, (m.start(), end), head, flags))
    g.end = end
    return _continue(text, g), g.end


def _siblings(text: str, pos: int, prev: dict):
    """A sibling designator chain at pos, attached under prev (§2.4a)."""
    m = DESIG.match(text, pos)
    if not m or not prev["levels"]:
        return None
    tok = m.group(2)
    attach = next((lv for lv in range(len(prev["levels"]), 0, -1)
                   if fits(tok, prev["levels"][lv - 1])), None)
    if attach is None:
        return None
    base_toks, base_levels = prev["desig"][:attach - 1], prev["levels"][:attach - 1]
    toks, levels, end, flags = chain(text, pos, prev["levels"][attach - 1], first_digit_ok=False)
    if not toks:
        return None
    return base_toks + toks, base_levels + levels, end, flags


def _continue(text: str, g: _Group) -> _Group:
    while True:
        prev = g.items[-1]
        # (e) designator range / (d) section range, directly after the previous item
        r = RSEP.match(text, g.end)
        if r:
            if (sib := _siblings(text, r.end(), prev)) and prev["desig"]:
                toks, levels, end, flags = sib
                lv = levels[-1]
                if len(toks) == len(prev["desig"]) and levels[:-1] == prev["levels"][:-1] \
                        and toks[:-1] == prev["desig"][:-1] and lv == prev["levels"][-1]:
                    a, b = _order(prev["desig"][-1], lv), _order(toks[-1], lv)
                    if a is not None and b is not None and a < b and b - a <= 60:
                        for n in range(a + 1, b + 1):
                            t = toks[:-1] + [_emit_order(n, lv)]
                            g.items.append(_item(prev["section"], t, levels, (r.end(), end), "continuation",
                                                 {"range_expanded"} if n < b else set()))
                        g.end = end
                        continue
                g.items.append(_item(prev["section"], toks, levels, (r.end(), end), "continuation",
                                     flags | {"range_unexpanded"}))
                g.end = end
                continue
            s = SECNUM.match(text, r.end())
            if s and not prev["desig"] and g.head == "section" and r.group(0) != "-":
                b = s.group(1)
                g.items.append(_item(b, [], [], (s.start(), s.end()), "continuation"))
                g.items[-1]["range"] = {"from": prev["section"], "to": b, "level": "section"}
                g.end = s.end()
                continue
        if re.match(r"\s+and following\b", text[g.end:]):
            prev["flags"].add("open_range")
            g.end += len(re.match(r"\s+and following\b", text[g.end:]).group(0))
            continue
        p = skip_parens(text, g.end)
        sep = SEP.match(text, p)
        if not sep:
            return g
        q = sep.end()
        if HEAD.match(text, q):  # (c) a repeated keyword starts a new group
            return g
        if sib := _siblings(text, q, prev):  # (a)
            toks, levels, end, flags = sib
            g.items.append(_item(prev["section"], toks, levels, (q, end), "continuation", flags))
            g.items[-1]["_sibling"] = True
            g.end = end
            continue
        s = SECNUM.match(text, q)  # (b)
        if s and g.head in ("section", "sec_abbrev", "sign", "usc26") and text[q - 1:q] != "$":
            toks, levels, end, flags = chain(text, s.end())
            if BARE_REJECT.match(text, end if toks else s.end()) or \
                    (toks and re.match(r"\s?-\s?\d", text[end:])):
                return g
            g.items.append(_item(s.group(1), toks, levels, (s.start(), end), "continuation", flags))
            g.end = end
            continue
        return g


# --- §2.5 the inverted form ---------------------------------------------------------

def _parse_inverted(text: str, m: re.Match):
    """'paragraphs (1) through (3) of section 152(a)'. Returns (items, consumed_span) or None."""
    pos, items = m.end(), []
    while True:
        toks, levels, end, flags = chain(text, pos, 1)
        if not toks:
            return None
        items.append((toks, pos, end))
        r = RSEP.match(text, end)
        if r and DESIG.match(text, r.end()):
            items.append(("RANGE", None, None))
            pos = r.end()
            continue
        s = SEP.match(text, end)
        if s and DESIG.match(text, s.end()):
            pos = s.end()
            continue
        break
    tail = re.compile(r"\s+of\s+(?:(section)\s+|(such|that|said)\s+section\b)").match(text, end)
    if not tail:
        return None
    if tail.group(2):
        return [{"path": None, "kind": "anaphor", "section": None, "desig": [], "levels": [],
                 "span": [m.start(), tail.end()], "head": "inverted", "range": None, "flags": set()}], \
            (m.start(), tail.end())
    s = SECNUM.match(text, tail.end())
    if not s or re.match(r"\s?\.\d|,\d", text[s.end():]):
        return None
    btoks, blevels, bend, bflags = chain(text, s.end())
    if re.match(r"\s?-\s?\d", text[bend:]):
        return None
    sec, out, base = s.group(1), [], len(blevels)
    pending_range = False
    for toks, a, b in items:
        if toks == "RANGE":
            pending_range = True
            continue
        levels, flags = [], set(bflags)
        for i, t in enumerate(toks):
            lv = base + 1 + i
            if not fits(t, lv):
                flags.add("irregular_chain")
            levels.append(lv)
        if pending_range and out and len(toks) == 1 and len(out[-1]["desig"]) == base + 1:
            lv = levels[0]
            x, y = _order(out[-1]["desig"][-1], lv), _order(toks[0], lv)
            if x is not None and y is not None and x < y and y - x <= 60:
                for n in range(x + 1, y):
                    out.append(_item(sec, btoks + [_emit_order(n, lv)], blevels + levels,
                                     (a, b), "inverted", flags | {"range_expanded"}))
        pending_range = False
        out.append(_item(sec, btoks + toks, blevels + levels, (s.start(), bend), "inverted", flags))
    return out, (m.start(), bend)


# --- qualifiers, flags, and the whole section --------------------------------------

def _qualify(text: str, items: list, start: int, end: int) -> bool:
    """Apply §3.2 exclusions and §2.6/§4 flags to a group. False drops it."""
    p = end
    while (q := skip_parens(text, p)) != p:
        p = q
    tail = text[p:]
    if re.match(r"\s*of such Code\b", tail):  # v2: which Code "such Code" is
        named = re.findall(r"Internal Revenue Code of (\d{4})", text[:start])
        if named and named[-1] == "1939":
            return False
    if re.match(r"\s*of this section\b", tail):  # v2: siblings belong to the regulation
        items[:] = [it for it in items if not it.get("_sibling")]
        if not items:
            return False
    ch = CHAPTER_SKIP.match(tail)
    if EXCLUDE.match(tail.lstrip()) or (ch and EXCLUDE.match(tail[ch.end():])):
        return False
    flags = set()
    if CODE_1954.match(tail):
        flags.add("code_1954")
    if HISTORICAL_AFTER.match(tail) or re.search(r"\b(?:former|old)\s+$", text[:start]):
        flags.add("historical")
    if re.match(r"\s+of this section\b", tail):
        flags.add("self_ref_qualifier")
    if re.search(r"flush language of\s+$", text[:start]):
        flags.add("flush")
    nxt = re.match(r"\s+([a-z]+)\b", text[end:])
    if ATTR_BEFORE.search(text[:start]) or (nxt and nxt.group(1) not in STOP):
        flags.add("attributive")
    for it in items:
        it["flags"] |= flags
    return True


def _authority_segment(text: str, start: int) -> tuple[int, int]:
    nxt = re.compile(r"\b[Ss]ec\.\s").search(text, start + 4)
    depth, end = 0, len(text)
    for i in range(start, len(text)):
        if text[i] == "(":
            depth += 1
        elif text[i] == ")":
            depth -= 1
            if depth < 0:
                end = i
                break
    return start, min(end, nxt.start() if nxt else len(text))


def extract(text: str, part: str | None = None, reg_id: str | None = None,
            truncated: bool = False) -> list[dict]:
    text = normalize(text)
    records, consumed = [], set()
    groups = []
    for m in INVERTED.finditer(text):
        got = _parse_inverted(text, m)
        if not got:
            continue
        items, (a, b) = got
        consumed.update(range(a, b))
        groups.append((m.start(), items, a, b, "inverted"))
    for m in HEAD.finditer(text):
        if m.end() in consumed or m.start() in consumed:
            continue
        if m.group(0).lower().startswith("section") and OTHER_PREFIX.search(text[:m.start()]):
            continue  # v2
        g, _ = _parse_group(text, m)
        if not g or not g.items:
            continue
        if any(it["span"][0] in consumed for it in g.items):
            g.items = [it for it in g.items if it["span"][0] not in consumed]
            if not g.items:
                continue
        groups.append((m.start(), g.items, g.start, g.end, g.head))
    groups.sort(key=lambda t: t[0])

    authority = []
    for n, (_, items, a, b, head) in enumerate(groups):
        if head != "inverted" and not _qualify(text, items, a, b):
            continue
        if head == "inverted" and items[0]["path"] is not None and not _qualify(text, items, a, b):
            continue
        if head == "sec_abbrev":
            s, e = _authority_segment(text, a)
            seg = text[s:e]
            ok = "68A Stat." in seg or re.search(r"Internal Revenue Code(?! of 1939)", seg) or \
                re.search(rf"26 U\.S\.C\. {re.escape(items[0]['section'])}\b", seg)
            if not ok:
                continue
            authority.append((s, e, {it["path"] for it in items}))
        for it in items:
            it["group"] = n
            records.append(it)

    keep = []
    for r in records:
        if r["head"] == "usc26" and any(s <= r["span"][0] < e and r["path"] in paths
                                        for s, e, paths in authority):
            continue
        if part == "57" and r["section"] == "9010":
            continue
        if truncated and (r["span"][1] >= len(text) - 2):
            continue
        if reg_id and reg_id.endswith("-0"):
            r["flags"].add("toc")
        keep.append(r)
    keep.sort(key=lambda r: r["group"])  # stable: items keep their order within a group
    for r in keep:
        r["flags"] = sorted(r["flags"])
        r.pop("levels", None)
        r.pop("_sibling", None)
    return keep
