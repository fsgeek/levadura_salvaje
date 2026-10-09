"""Citations that resolve to a section number which held a different law when the regulation was
written (predictions: predictions/2026-10-09-prior-numbers-claude.md).

The existence check (resolve.py) scores a citation healthy if its number exists today. But 26 USC
numbers get reused: §34 was a dividends credit until 1964 and is now a fuel credit. The Code
records this itself, in each section's "Prior Provisions" note ("A prior section 34 ... was
repealed by ..."). This reads those notes at 119-4, works out when each number took its current
text (the last "renumbered § N" in its source credit, else its first enactment date), and flags
every resolving 2025 CFR citation to such a number from a regulation whose own dates (every
Federal Register date in the section, CITA included) all precede that.

Known limits, before measuring: a section rewritten in place leaves no prior-section note (§683);
regulations whose amendment history is only in the List of CFR Sections Affected can't be dated
from their text, so they are reported separately; a flagged regulation may still mean the current
law (it can be read either way until a reader checks); a reuse that predates the regulation is
not flagged at all.

Usage: uv run python scripts/measure_prior_numbers.py
"""

import glob
import hashlib
import json
import re
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter
from datetime import date
from pathlib import Path

from levadura_salvaje.ledger import append, verify
from levadura_salvaje.resolve import DASHES

U = "{http://xml.house.gov/schemas/uslm/1.0}"
USC = Path("data/usc/xml_usc26@119-4.zip")
CFR = "data/cfr/2025/CFR-2025-title26-vol*.xml"
CITATIONS = Path("results/cfr-usc-citations-v2-2025.jsonl")
OUT = Path("results/cfr-prior-number-citations-v1-2025.jsonl")

MONTHS = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "June": 6, "Jul": 7, "July": 7,
          "Aug": 8, "Sep": 9, "Sept": 9, "Oct": 10, "Nov": 11, "Dec": 12}
DATE = re.compile(r"\b(Jan|Feb|Mar|Apr|May|June?|July?|Aug|Sept?|Oct|Nov|Dec)\.? (\d{1,2}), (\d{4})")
FR_DATE = re.compile(r"\d+ FR \d+,? ([^;\]\)]{0,20})")
LSA = "List of CFR Sections Affected"


def dates(text: str) -> list[date]:
    return [date(int(y), MONTHS[m], int(d)) for m, d, y in DATE.findall(text)]


def _text(el) -> str:
    return "".join(el.itertext())


def number_acquired(num: str, source_credit: str) -> date | None:
    """When section `num` took its current text: the date of the last act that renumbered
    something into it, else the first date in its source credit."""
    at = None
    for m in re.finditer(rf"renumbered §\s*{re.escape(num)}\b", source_credit):
        before = dates(source_credit[:m.start()])
        if before:
            at = before[-1]
    if at is None:
        first = dates(source_credit)
        at = first[0] if first else None
    return at


def prior_numbers(usc_root) -> dict[str, dict]:
    """Section number -> {acquired, prior}: numbers whose Prior Provisions note names an earlier
    section with the same number."""
    out = {}
    for sec in usc_root.iter(U + "section"):
        m = re.fullmatch(r"/us/usc/t26/s([0-9A-Za-z]+)", sec.get("identifier") or "")
        if not m:
            continue
        num = m.group(1)
        prior = [_text(p).strip() for note in sec.iter(U + "note") if note.get("topic") == "priorProvisions"
                 for p in note.iter(U + "p") if re.search(rf"\bprior section {re.escape(num)}\b", _text(p), re.I)]
        credit = sec.find(U + "sourceCredit")
        acquired = number_acquired(num, _text(credit) if credit is not None else "")
        if prior and acquired:
            out[num] = {"acquired": acquired, "prior": prior[0]}
    return out


def regulation_dates(section_el) -> tuple[list[date], bool]:
    """Every Federal Register date in a CFR section, and whether its history is only in the LSA."""
    t = " ".join(_text(section_el).split())
    found = [d for m in FR_DATE.finditer(t) for d in dates(m.group(1))]
    cita = section_el.find("CITA")
    if cita is not None:
        found += dates(_text(cita))
    return sorted(set(found)), LSA in t


def classify(reg: list[date], acquired: date) -> str:
    if not reg:
        return "undated"
    if max(reg) < acquired:
        return "older_than_number"
    if min(reg) < acquired:
        return "amended_across"
    return "newer_than_number"


def main() -> None:
    with zipfile.ZipFile(USC) as z, z.open(z.namelist()[0]) as f:
        prior = prior_numbers(ET.parse(f).getroot())
    regs = {}
    for path in sorted(glob.glob(CFR)):
        for s in ET.parse(path).getroot().iter("SECTION"):
            no = (s.findtext("SECTNO") or "").replace("§", "").strip()
            if no:
                regs[no] = regulation_dates(s)

    rows, counts = [], Counter()
    for line in CITATIONS.read_text().splitlines():
        r = json.loads(line)
        reg, lsa = regs.get(r["sectno"], ([], False))
        for c in r["citations"]:
            if c.get("outcome", {}).get("119-4", {}).get("outcome") != "resolves":
                continue
            num = c["path"].translate(DASHES).split("/")[0]
            if num not in prior:
                continue
            kind = classify(reg, prior[num]["acquired"])
            counts[kind] += 1
            if kind == "older_than_number":
                rows.append({"sectno": r["sectno"], "volume_file": r["volume_file"], "span": c["span"],
                             "path": c["path"], "number": num, "lsa_dated": lsa,
                             "reg_first": str(min(reg)), "reg_last": str(max(reg)),
                             "number_acquired": str(prior[num]["acquired"]), "prior_note": prior[num]["prior"]})
    OUT.write_text("".join(json.dumps(x, sort_keys=True, ensure_ascii=False) + "\n" for x in rows))

    clean = [x for x in rows if not x["lsa_dated"]]
    measured = {
        "usc_numbers_with_prior_section": len(prior),
        "resolving_citations_to_such_numbers": sum(counts.values()),
        "by_dating": dict(counts),
        "flagged_citations": len(rows),
        "flagged_sections": len({x["sectno"] for x in rows}),
        "flagged_citations_text_dated": len(clean),
        "flagged_sections_text_dated": len({x["sectno"] for x in clean}),
        "flagged_sections_lsa_dated": len({x["sectno"] for x in rows if x["lsa_dated"]}),
    }
    print(json.dumps(measured, indent=1))
    entry = append({
        "observed_at": "2025-04-01",
        "observed_at_note": "2025 CFR title 26 edition, read against USC release point 119-4 (2025-03-15)",
        "instrument": {
            "name": "scripts/measure_prior_numbers.py",
            "method": "USC 119-4 Prior Provisions notes naming a same-number prior section; number's current text dated by last 'renumbered § N' in sourceCredit, else first date; regulation dated by every FR date in the section (CITA included); flag when all regulation dates precede the number's date",
            "known_limits": "in-place rewrites leave no prior-section note (§683); LSA-only amendment histories reported separately; a flag is a candidate, not a reading; exploratory counts were seen before the predictions (declared there)",
            "predictions": "predictions/2026-10-09-prior-numbers-claude.md",
        },
        "population": {"edition": "2025", "release_point": "119-4", "citations": str(CITATIONS),
                       "scope": "citations that resolve at 119-4"},
        "quantity": "cfr_citation_prior_number",
        "value": {**measured, "output": str(OUT), "output_sha256": hashlib.sha256(OUT.read_bytes()).hexdigest()},
    })
    print(entry["id"], "ledger entries:", verify())


if __name__ == "__main__":
    main()
