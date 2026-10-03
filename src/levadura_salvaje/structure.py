"""The paragraph structure of a 26 CFR section, in the coordinates citation spans use.

Rule-currency v3 (docs/rule-currency-v3-design.md) gives the judge the rule a citation sits in:
its paragraph, the paragraph's ancestors, the example it belongs to, and the section's
applicability paragraph. Citation spans index `citations.normalize(flat)`, where `flat` is
`sections._flat(SECTION)`. This module reproduces that flattening while recording where each
`<P>` starts and ends, so a span maps to its paragraph.

Paragraph levels follow the CFR: (a) 0, (1) 1, (i) 2, (A) 3, and the italic (1) 4 and (i) 5,
which plain text can't tell from levels 1 and 2. Designators are taken at a paragraph's start,
plus one opened inline after a heading dash or a short heading sentence. `<EXAMPLE>` elements and
"Example N." paragraphs number their own paragraphs. scripts/probe_rule_ancestry.py measured this
on the 73 sections citing § 902: 3.4% of designators outside tables of contents fail to place.
A paragraph whose chain passes through a failure has `ancestry = None`.
"""

import re
from dataclasses import dataclass, field

from levadura_salvaje.citations import _DOUBLED, _ITALIC, _SPACES, normalize

ROMAN = re.compile(r"^(?=[ivxl])(x{0,3}|xl|l)(ix|iv|v?i{0,3})$")
_TOK = r"([a-z]{1,4}|[A-Z]{1,3}|\d{1,3})"
LEAD = re.compile(rf"^(?:\({_TOK}\))+")
INLINE = re.compile(rf"(?:—\s?|^[^.()]{{0,120}}?\.\s)\({_TOK}\)\s?[A-Z]")
EXAMPLE = re.compile(r"^Example\s*\(?\d+\)?\.")
APPLIES = re.compile(r"\b(effective|applicability)\b", re.IGNORECASE)
BLOCKS = ("P", "FP")   # paragraph elements; FP is a flush (undesignated) paragraph
ROMANS = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x", "xi", "xii", "xiii", "xiv", "xv",
          "xvi", "xvii", "xviii", "xix", "xx", "xxi", "xxii", "xxiii", "xxiv", "xxv"]


@dataclass
class Para:
    index: int
    start: int               # in normalized text
    end: int
    text: str                # normalized
    designators: list[str]
    scope: str               # "main" or "exN"
    example_heading: str | None = None
    level: int | None = None
    parent: int | None = None   # index of the parent paragraph
    failed: bool = False
    ancestry: list[int] | None = field(default=None)


# --- flattening with offsets -----------------------------------------------------------------

def _itertext_marked(el, marks: list, raw: list[str], pos: list[int]):
    """ET.itertext order, recording each <P>'s raw start/end and each <EXAMPLE>'s span."""
    if el.tag in BLOCKS:
        marks.append(("P", pos[0], el))
    if el.tag == "EXAMPLE":
        marks.append(("EX+", pos[0], el))
    if el.text:
        raw.append(el.text)
        pos[0] += len(el.text)
    for ch in el:
        _itertext_marked(ch, marks, raw, pos)
        if ch.tail:
            raw.append(ch.tail)
            pos[0] += len(ch.tail)
    if el.tag in BLOCKS:
        marks.append(("/P", pos[0], el))
    if el.tag == "EXAMPLE":
        marks.append(("EX-", pos[0], el))


def _raw_to_flat(raw: str) -> list[int]:
    """For each raw offset, the flat offset of the first non-space character at or after it."""
    out, flat, in_word, seen = [0] * (len(raw) + 1), 0, False, False
    for i, ch in enumerate(raw):
        if ch.isspace():
            if in_word:
                in_word = False
            out[i] = flat + (1 if seen else 0)
        else:
            if not in_word and seen:
                flat += 1           # the single space between words
            in_word, seen = True, True
            out[i] = flat
            flat += 1
    out[len(raw)] = flat
    return [min(x, flat) for x in out]      # whitespace after the last word maps to the end


def tracked_normalize(text: str) -> tuple[str, list[int]]:
    """citations.normalize(), also returning each output character's position in the input."""
    def sub(rx, repl, t, origin):
        out, org, last = [], [], 0
        for m in rx.finditer(t):
            out.append(t[last:m.start()]); org.extend(origin[last:m.start()])
            r, o = repl(m, origin)
            out.append(r); org.extend(o)
            last = m.end()
        out.append(t[last:]); org.extend(origin[last:])
        return "".join(out), org

    t, o = sub(_SPACES, lambda m, og: (" ", [og[m.start()]]), text, list(range(len(text))))
    lead = len(t) - len(t.lstrip())
    t, o = t.strip(), o[lead:lead + len(t.strip())]
    t, o = sub(_ITALIC, lambda m, og: ("(" + m.group(1) + ")",
                                       [og[m.start()], *og[m.start(1):m.end(1)], og[m.end() - 1]]), t, o)
    t, o = sub(_DOUBLED, lambda m, og: ("§", [og[m.end() - 1]]), t, o)
    return t, o


# --- levels ----------------------------------------------------------------------------------

def designators(t: str) -> list[str]:
    out = []
    m = LEAD.match(t)
    if m:
        out += re.findall(rf"\({_TOK}\)", m.group(0))
        d = INLINE.search(t[m.end():m.end() + 200].lstrip())
        if d:
            out.append(d.group(1))
    return out


def _kinds(tok: str) -> list[int]:
    if tok.isdigit():
        return [1, 4]
    if tok.isupper():
        return [3]
    out = []
    if ROMAN.match(tok):
        out += [2, 5]
    if len(tok) == 1 or (len(tok) == 2 and tok[0] == tok[1]):
        out.append(0)
    return out


def _next(tok: str, level: int) -> str | None:
    if level in (1, 4):
        return str(int(tok) + 1)
    if level in (0, 3):
        return chr(ord(tok) + 1) if len(tok) == 1 else None
    return ROMANS[ROMANS.index(tok) + 1] if tok in ROMANS[:-1] else None


def _opens(tok: str, level: int) -> bool:
    return tok == {0: "a", 1: "1", 2: "i", 3: "A", 4: "1", 5: "i"}[level] or (level in (1, 4) and tok == "0")


def _place(stack: list, tok: str) -> list | None:
    """The new stack after tok, or None if tok neither continues a sibling nor opens a child."""
    ks = _kinds(tok)
    for depth in range(len(stack) - 1, -1, -1):
        lv, t, _ = stack[depth]
        if lv in ks and _next(t, lv) == tok:
            return stack[:depth] + [(lv, tok, None)]
    for k in ks:
        if (not stack and _opens(tok, k)) or (stack and k > stack[-1][0] and _opens(tok, k)):
            return stack + [(k, tok, None)]
    return None


# --- the structure -----------------------------------------------------------------------------

def paragraphs(section_el) -> tuple[str, list[Para]]:
    """(normalized section text, its paragraphs with ranges, levels and ancestry)."""
    marks, raw_parts, pos = [], [], [0]
    _itertext_marked(section_el, marks, raw_parts, pos)
    raw = "".join(raw_parts)
    r2f = _raw_to_flat(raw)
    flat = " ".join(raw.split())
    norm, origin = tracked_normalize(flat)
    # flat offset -> first normalized offset at or after it
    f2n = [len(norm)] * (len(flat) + 1)
    for n_i in range(len(norm) - 1, -1, -1):
        f2n[origin[n_i]] = n_i
    for f_i in range(len(flat) - 1, -1, -1):
        f2n[f_i] = min(f2n[f_i], f2n[f_i + 1])

    paras, open_p, ex_depth, ex_count, ex_heading = [], {}, 0, 0, None
    scope = "main"
    for kind, at, el in marks:
        if kind == "EX+":
            ex_depth += 1; ex_count += 1; scope = f"ex{ex_count}"
            hd = el.find("HD")
            ex_heading = " ".join("".join(hd.itertext()).split()) if hd is not None else None
        elif kind == "EX-":
            ex_depth -= 1
            if ex_depth == 0:
                scope, ex_heading = "main", None
        elif kind == "P":
            open_p[id(el)] = at
        elif kind == "/P":
            a, b = f2n[r2f[open_p.pop(id(el))]], f2n[r2f[at]]
            text = norm[a:b].strip()
            if ex_depth == 0 and EXAMPLE.match(text):
                ex_count += 1; scope = f"ex{ex_count}"; ex_heading = text.split(".")[0] + "."
            paras.append(Para(len(paras), a, b, text, designators(text), scope, ex_heading))
    _levels(paras)
    return norm, paras


def _levels(paras: list[Para]) -> None:
    stacks: dict[str, list] = {}
    for p in paras:
        stack = stacks.setdefault(p.scope, [])
        before, failed = list(stack), False
        for tok in p.designators:
            new = _place(stack, tok)
            if new is None:
                failed = True        # this paragraph's chain is unknown; the stack reverts and carries on,
                stack = before       # as in the probe, so one bad designator doesn't break the rest
                break
            stack = new
        if failed:
            pass                                                # ancestry stays None
        elif p.designators:
            # every level this paragraph opened ("(c)(1) ...") belongs to it
            stack = [(lv, t, p.index if node is None else node) for lv, t, node in stack]
            p.level = stack[-1][0]
            p.parent = stack[-2][2] if len(stack) > 1 else None
            p.ancestry = [s[2] for s in stack[:-1] if s[2] != p.index]   # not itself, for "(2) ... —(i)"
        elif not p.designators and stack and stack[-1][2] is not None:
            p.level, p.parent = stack[-1][0], stack[-1][2]     # an undesignated continuation
            p.ancestry = [s[2] for s in stack]
        elif not p.designators:
            p.ancestry = []                                     # top of a scope: no ancestors
        p.failed = failed
        stacks[p.scope] = stack


def containing(paras: list[Para], at: int) -> Para | None:
    """The paragraph whose normalized range contains offset `at`."""
    for p in paras:
        if p.start <= at < p.end:
            return p
    return None


def enclosing(paras: list[Para], at: int) -> tuple[Para | None, bool]:
    """(paragraph, exact). The containing paragraph if there is one; otherwise the nearest paragraph
    before `at` in document order, which is how a table or extract inside an example keeps the
    example's scope. exact is False for that attachment."""
    p = containing(paras, at)
    if p is not None:
        return p, True
    before = [q for q in paras if q.end <= at]
    return (before[-1], False) if before else (None, False)


def applicability(paras: list[Para]) -> Para | None:
    """The section's applicability paragraph: a main-scope paragraph whose heading (its first 120
    characters) speaks of an effective or applicability date."""
    for p in paras:
        if p.scope == "main" and p.designators and APPLIES.search(p.text[:120]):
            return p
    return None


__all__ = ["Para", "paragraphs", "containing", "enclosing", "applicability", "designators", "tracked_normalize", "normalize"]
