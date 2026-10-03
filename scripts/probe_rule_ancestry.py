"""Probe for rule-currency v3 (docs/rule-currency-v3-design.md): do paragraph designators parse into a
CFR hierarchy for the 73 sections citing section 902?

    uv run python scripts/probe_rule_ancestry.py

Levels: (a) 0, (1) 1, (i) 2, (A) 3, italic (1) 4 and (i) 5 (plain text loses the italics, so digits and
small romans are each tried at two levels). Designators are taken at a paragraph's start, plus one opened
inline after a heading dash or a short heading sentence. <EXAMPLE> elements and "Example N." paragraphs
number their own paragraphs. A designator fails if it neither continues a sibling at some depth nor opens
a child level.
"""
import io, json, re, zipfile, xml.etree.ElementTree as ET
from collections import Counter

ROMAN = re.compile(r"^(?=[ivxl])(x{0,3}|xl|l)(ix|iv|v?i{0,3})$")
DESIG = re.compile(r"^\(([a-z]{1,4}|[A-Z]{1,3}|\d{1,3})\)")

def kinds(tok):
    """Possible CFR levels for a token: 0 (a), 1 (1), 2 (i), 3 (A). Italic levels 4, 5 aren't in plain text."""
    out = []
    if tok.isdigit(): out += [1, 4]
    elif tok.isupper(): out.append(3)
    else:
        if ROMAN.match(tok): out += [2, 5]
        if len(tok) == 1 or (len(tok) == 2 and tok[0] == tok[1]): out.append(0)  # (a)..(z), (aa)
    return out

def nxt(tok, level):
    """The designator that follows tok at a level."""
    if level in (1, 4): return str(int(tok) + 1)
    if level == 3: return chr(ord(tok) + 1) if len(tok) == 1 else None
    if level == 0: return chr(ord(tok) + 1) if len(tok) == 1 else None
    if level in (2, 5):
        r = ["i","ii","iii","iv","v","vi","vii","viii","ix","x","xi","xii","xiii","xiv","xv","xvi","xvii","xviii","xix","xx"]
        return r[r.index(tok)+1] if tok in r[:-1] else None
    return None

LEAD = re.compile(r"^(?:\(([a-z]{1,4}|[A-Z]{1,3}|\d{1,3})\))+")
INLINE = re.compile(r"(?:—\s?|^[^.()]{0,120}?\.\s)\(([a-z]{1,4}|[A-Z]{1,3}|\d{1,3})\)\s?[A-Z]")

def designators(t):
    """Leading designators ("(c)(1)") plus one opened after a heading dash ("—(i)")."""
    out = []
    m = LEAD.match(t)
    if m:
        out += re.findall(r"\(([a-z]{1,4}|[A-Z]{1,3}|\d{1,3})\)", m.group(0))
        rest = t[m.end():m.end() + 200].lstrip()
        d = INLINE.search(rest)
        if d: out.append(d.group(1))
    return out

def first(level): return {0: "a", 1: "1", 2: "i", 3: "A", 4: "1", 5: "i"}[level]


def opens(tok, level): return tok == first(level) or (level in (1, 4) and tok == "0")

def parse(tokens):
    """Assign levels greedily: continue the current stack, a sibling at some depth, or open a child.
    Returns (levels, failures)."""
    stack, levels, fails = [], [], 0   # stack of (level, token)
    for tok in tokens:
        ks = kinds(tok); placed = None
        # child of the current top
        cand = []
        for k in ks:
            if (not stack and opens(tok, k)) or (stack and k > stack[-1][0] and opens(tok, k)):
                cand.append(("child", k))
        # sibling at some depth (pop back)
        for depth in range(len(stack) - 1, -1, -1):
            lv, t = stack[depth]
            if lv in ks and nxt(t, lv) == tok:
                cand.append(("sib", depth)); break
        if cand:
            # prefer sibling continuation for ambiguous roman/letter (e.g. (i) after (h))
            kind, v = next((c for c in cand if c[0] == "sib"), cand[0])
            if kind == "sib":
                stack = stack[:v] + [(stack[v][0], tok)]
            else:
                stack = stack + [(v, tok)]
            levels.append(stack[-1][0])
        else:
            fails += 1; levels.append(None)
    return levels, fails

rows = {(r["volume_file"], r["ordinal"]) for r in map(json.loads, open("results/rule-currency-qwen-v2-902-2025.jsonl"))}
z = zipfile.ZipFile("data/cfr/CFR-2025-title-26.zip")
stats = Counter(); worst = []
for name in sorted(n for n in z.namelist() if n.endswith(".xml")):
    want = {o for v, o in rows if v == name}
    if not want: continue
    ordinal = 0
    for _, el in ET.iterparse(io.BytesIO(z.read(name)), events=("end",)):
        if el.tag != "SECTION": continue
        ordinal += 1
        if ordinal in want:
            no = "".join(el.find("SECTNO").itertext())
            scopes = {"main": []}           # each <EXAMPLE> numbers its own paragraphs
            def walk(node, scope):
                for ch in node:
                    if ch.tag == "EXAMPLE":
                        key = f"ex{len(scopes)}"; scopes[key] = []; walk(ch, key)
                    elif ch.tag == "P":
                        t = " ".join("".join(ch.itertext()).split())
                        if re.match(r"^Example\s*\(?\d+\)?\.", t):
                            scope = f"ex{len(scopes)}"; scopes[scope] = []
                        scopes[scope] += designators(t)
                    else:
                        walk(ch, scope)
            walk(el, "main")
            toks = [t for v in scopes.values() for t in v]
            fails = sum(parse(v)[1] for v in scopes.values())
            stats["sections"] += 1; stats["designated_P"] += len(toks); stats["failed"] += fails
            stats["sections_clean"] += fails == 0
            worst.append((fails, no, len(toks)))
            stats["toc_failed"] += fails if no.strip().endswith("-0") else 0
        el.clear()
print(dict(stats)); print(sorted(worst, reverse=True)[:10])
