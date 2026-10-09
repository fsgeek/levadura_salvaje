"""Blind audit packet for prior-numbers v1 (predictions N1-N4:
predictions/2026-10-09-prior-numbers-claude.md).

    uv run python scripts/audit_prior_numbers.py packet   # writes packet, key and instructions
    uv run python scripts/audit_prior_numbers.py score    # after readers A, B (and adjudicator)

Judges see only regulation text and two subject descriptions (X, Y, in random order), never
dates, the instrument or the predictions. The key (which of X/Y is the earlier provision) stays
out of their packet.
"""

import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

from levadura_salvaje.sections import sections

FLAGS = Path("results/cfr-prior-number-citations-v1-2025.jsonl")
USC_PROVISIONS = Path("results/usc26-provisions-119-4.jsonl")
CFR_ZIP = Path("data/cfr/CFR-2025-title-26.zip")
SEEN = {"1.642(a)(3)-2", "1.703-1", "1.1294-1T", "301.6224(c)-2", "1.1502-12", "1.381(c)(25)-1"}
D = Path("results/prior-numbers-audit-v1")
PACKET, KEY, INSTRUCTIONS = D / "packet.jsonl", D / "key.jsonl", D / "instructions.md"
READERS = ("reader-a", "reader-b", "adjudicator")

INSTRUCTION_TEXT = """You are reading passages from U.S. Treasury regulations (26 CFR). Each item quotes a
passage that cites a section of the Internal Revenue Code by number, and gives two short
descriptions, X and Y, of laws that have been numbered that way.

For each item, decide which law the passage's citation refers to, judging from what the passage
says about it: X, Y, or "cant_tell" if the passage gives no way to decide. Don't use outside
knowledge of when laws were enacted; judge from the passage and the descriptions.

Write one JSON object per line: {"item": <item>, "answer": "X" | "Y" | "cant_tell", "reason": "<one sentence>"}
"""


def neutral(subject: str) -> str:
    """Strip what would tell a judge which law is older: "prior to repeal by Pub. L. ...",
    "prior to the general revision ...", and the lowercase start of note phrases."""
    s = re.split(r",?\s*prior to (?:repeal|the general revision|amendment|being renumbered)", subject)[0]
    s = " ".join(s.split()).rstrip(" .,;")
    return s[:1].upper() + s[1:]


def earlier_subject(note: str, headings: dict[str, str]) -> str | None:
    m = re.search(r"\b(?:which )?related to (.+?)\.?\s*$", note, re.S)
    if m:
        return neutral(m.group(1))
    m = re.search(r"was renumbered section (\w+) of this title", note)
    if m and headings.get(m.group(1)):
        return headings[m.group(1)]
    return None


def packet() -> None:
    headings = {}
    for line in USC_PROVISIONS.read_text().splitlines():
        p = json.loads(line)
        if p["level"] == "section" and p["heading"]:
            headings[p["path"].translate({0x2013: "-", 0x2014: "-"})[1:]] = p["heading"]
    flags = [json.loads(l) for l in FLAGS.read_text().splitlines()]
    frame, no_subject = [], 0
    for f in flags:
        if f["lsa_dated"] or f["sectno"] in SEEN:
            continue
        earlier = earlier_subject(f["prior_note"], headings)
        current = neutral(headings[f["number"]]) if headings.get(f["number"]) else None
        if earlier and current:
            frame.append({**f, "earlier": earlier, "current": current})
        else:
            no_subject += 1
    by_section: dict[str, list] = {}
    for f in frame:
        by_section.setdefault(f["sectno"], []).append(f)
    rng = random.Random(9)
    chosen = rng.sample(sorted(by_section), 40)
    texts = {s["sectno"]: s["text"] for s in sections(CFR_ZIP) if s["sectno"] in chosen}
    D.mkdir(parents=True, exist_ok=True)
    packet_rows, key_rows = [], []
    for i, sno in enumerate(chosen, 1):
        f = rng.choice(by_section[sno])
        a, b = f["span"]
        t = texts[sno]
        excerpt = t[max(0, a - 450):b + 250]
        earlier_is_x = rng.random() < 0.5
        x, y = (f["earlier"], f["current"]) if earlier_is_x else (f["current"], f["earlier"])
        packet_rows.append({"item": i, "regulation": f"26 CFR § {sno}", "cited": f"section {f['number']}",
                            "passage": "… " + " ".join(excerpt.split()) + " …", "X": x, "Y": y})
        key_rows.append({"item": i, "sectno": sno, "span": f["span"], "number": f["number"],
                         "earlier": "X" if earlier_is_x else "Y",
                         "earlier_kind": "renumbered" if "was renumbered" in f["prior_note"] else "repealed_or_other"})
    PACKET.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in packet_rows))
    KEY.write_text("".join(json.dumps(r) + "\n" for r in key_rows))
    INSTRUCTIONS.write_text(INSTRUCTION_TEXT)
    print(f"frame: {len(frame)} citations in {len(by_section)} sections; without an extractable subject: {no_subject}")


def score() -> None:
    key = {r["item"]: r for r in map(json.loads, KEY.read_text().splitlines())}
    ans = {}
    for r in READERS[:2]:
        ans[r] = {x["item"]: x["answer"] for x in map(json.loads, (D / f"{r}.jsonl").read_text().splitlines())}
    adj_path = D / "adjudicator.jsonl"
    adj = {x["item"]: x["answer"] for x in map(json.loads, adj_path.read_text().splitlines())} if adj_path.exists() else {}
    agree = sum(ans["reader-a"][i] == ans["reader-b"][i] for i in key)
    final = {i: ans["reader-a"][i] if ans["reader-a"][i] == ans["reader-b"][i] else adj.get(i, "unadjudicated") for i in key}
    label = {i: ("earlier" if final[i] == key[i]["earlier"] else "cant_tell" if final[i] in ("cant_tell", "unadjudicated")
                 else "current") for i in key}
    c = Counter(label.values())
    current_kinds = Counter(key[i]["earlier_kind"] for i in key if label[i] == "current")
    print(json.dumps({"n": len(key), "final": dict(c), "precision": c["earlier"] / len(key),
                      "agreement_a_b": agree / len(key), "disagreements": [i for i in key if ans["reader-a"][i] != ans["reader-b"][i]],
                      "current_by_earlier_kind": dict(current_kinds)}, indent=1))


if __name__ == "__main__":
    {"packet": packet, "score": score}[sys.argv[1]]()
