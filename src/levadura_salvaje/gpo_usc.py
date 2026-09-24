"""Read a GPO U.S. Code title 26 package (GovInfo HTML) as a set of provisions.

The output has the same shape as usc.provisions (USLM), so resolve.Statute
can load either. GPO's HTML has no identifiers below the section, so the
subdivision tree is inferred: each statute element that begins with a
designator ("(a)", "(1)", "(A)", "(i)", "(I)", "(aa)") is a provision. Its
level comes from the element's class, heads by name ("paragraph-head") and
body text by indent ("statutory-body-2em" = subparagraph). When the
designator's form does not fit that level, the nearest level it does fit is
used. The path is the chain of the most recent designator at each shallower
level, so paragraphs directly under a section (old §1221(1)) come out as
``s1221/1``, as they would in USLM.

A section's status comes from its bracketed heading ("[§4. Repealed. ...]",
"[§28. Renumbered §45C]", "[§§4471 to 4474. Repealed ...]" becomes a range
path ``s4471...4474``). A subdivision whose text is only "(3) Repealed. ..."
is marked repealed.
"""

import hashlib
import html
import re
from collections.abc import Iterator
from pathlib import Path

from levadura_salvaje.citations import fits

LEVELS = ("section", "subsection", "paragraph", "subparagraph", "clause", "subclause", "item", "subitem")
HEAD_LEVEL = {"subsection-head": 1, "paragraph-head": 2, "subparagraph-head": 3, "clause-head": 4,
              "subclause-head": 5, "item-head": 6, "subitem-head": 7}
BODY = re.compile(r"statutory-body(?:-(\d)em)?$")
DOC = re.compile(r"<!-- documentid:26_(\S+)\s[^>]*currentthrough:(\d+)")
SECHEAD = re.compile(r'<h3 class="section-head">(.*?)</h3>', re.S)
ELEM = re.compile(r'<(h4|p) class="([^"]+)">(.*?)</\1>', re.S)
LEAD = re.compile(r"^\[?\((\w{1,6})\)")
STATUS = re.compile(r"\b(Repealed|Renumbered|Omitted|Transferred|Reserved)\b")


def _text(fragment: str) -> str:
    return " ".join(html.unescape(re.sub(r"<[^>]+>", "", fragment)).split())


def _status(heading: str) -> str | None:
    m = STATUS.search(heading)
    if not m or not heading.lstrip().startswith("["):
        return None
    return {"Repealed": "repealed", "Renumbered": "renumbered", "Omitted": "omitted",
            "Transferred": "renumbered", "Reserved": "reserved"}[m.group(1)]


def _section_number(heading: str) -> str | None:
    h = heading.replace("–", "-").replace("—", "-")
    m = re.match(r"\[?§§\s*(\d+[A-Z]*(?:-\d+)?)\s+(?:to|through)\s+(\d+[A-Z]*(?:-\d+)?)", h)
    if m:
        return f"{m.group(1)}...{m.group(2)}"
    m = re.match(r"\[?§\s*(\d+[A-Z]*(?:-\d+)?)\.", h)
    return m.group(1) if m else None


def _level(cls: str, tok: str, stack: dict) -> int | None:
    if cls in HEAD_LEVEL:
        hint = HEAD_LEVEL[cls]
    elif (m := BODY.match(cls)):
        hint = int(m.group(1) or 0) + 1
    else:
        return None
    if fits(tok, hint):
        return hint
    options = [lv for lv in range(1, 7) if fits(tok, lv)]
    if not options:
        return None
    return min(options, key=lambda lv: abs(lv - hint))


def provisions(path: Path) -> Iterator[dict]:
    doc = path.read_text(errors="replace")
    starts = [m for m in DOC.finditer(doc)]
    seen = set()
    for i, m in enumerate(starts):
        block = doc[m.start(): starts[i + 1].start() if i + 1 < len(starts) else len(doc)]
        head = SECHEAD.search(block)
        if not head:
            continue
        heading = _text(head.group(1))
        sec = _section_number(heading)
        if not sec or sec in seen:
            continue
        seen.add(sec)
        status = _status(heading)
        a = block.find("field-start:statute")
        b = block.find("field-end:statute", a)
        statute = block[a:b] if a >= 0 and b > a else ""
        yield {"identifier": f"/us/usc/t26/s{sec}", "path": f"s{sec}", "level": "section", "status": status,
               "num": sec, "heading": re.sub(r"^\[?§+\s*\S+\.?\s*", "", heading).strip(" ]"),
               "chars": len(_text(statute)), "text_sha256": hashlib.sha256(_text(statute).encode()).hexdigest(),
               "current_through": m.group(2)}
        if status:
            continue
        stack: dict[int, str] = {}
        emitted = set()
        for e in ELEM.finditer(statute):
            cls, body = e.group(2), _text(e.group(3))
            lead = LEAD.match(body)
            if not lead:
                continue
            tok = lead.group(1)
            lv = _level(cls, tok, stack)
            if lv is None:
                continue
            stack = {k: v for k, v in stack.items() if k < lv}
            stack[lv] = tok
            p = "/".join([f"s{sec}", *[stack[k] for k in sorted(stack)]])
            if p in emitted:
                continue
            emitted.add(p)
            rest = body[lead.end():].strip()
            yield {"identifier": f"/us/usc/t26/{p}", "path": p, "level": LEVELS[lv], "num": tok,
                   "status": "repealed" if re.match(r"\[?Repealed\b", rest) else None,
                   "heading": rest[:120] if cls.endswith("-head") else "",
                   "chars": len(body), "text_sha256": hashlib.sha256(body.encode()).hexdigest(),
                   "current_through": m.group(2)}
