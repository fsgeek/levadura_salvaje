"""Two population measurements that the first callers' readings led to. Appends to the ledger.

    uv run --group plumbing python spikes/surface1/measure_findings.py [--dry-run]

1. **Span domain.** Citation spans in results/cfr-usc-citations-v2-2025.jsonl index
   `citations.normalize(text)`, not the stored flat text. How many section-head
   citations does slicing the flat text misplace, and how many does slicing the
   normalized text? (caller-opus-1 saw "s 9" for "902".)
2. **Other-statute aliases.** 54.4980F-1 introduces "section 204(h) of ERISA" and
   then writes "section 204(h)" alone, so the extractor reads it as the Code's
   section 204 (caller-opus-1). Population: sections in which a number N appears as
   "section N... of <another statute>", and the bare citations of N in the same
   section that were extracted as Code citations. It's a probe: a bare N in such a
   section *may* still mean the Code. It is an upper bound on this alias, and it
   doesn't cover aliases defined elsewhere (for example in a definitions section).
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import surface as sf  # noqa: E402  (puts spikes/plumbing2 on the path)
import corpus as cx  # noqa: E402

from levadura_salvaje import ledger  # noqa: E402
from levadura_salvaje.citations import normalize  # noqa: E402

BROKEN = {"repealed", "absent-section", "absent-subdivision"}
OTHER = re.compile(r"\bsections? (\d{1,4}[A-Z]?)((?:\s?\([A-Za-z0-9]{1,6}\))*) of (?:the )?"
                   r"(ERISA|Employee Retirement Income Security Act|Social Security Act|Public Health Service Act"
                   r"|Railroad Retirement Act|Tariff Act|[A-Z][A-Za-z]+(?: [A-Z][A-Za-z]+)* Act)")


def main(dry: bool) -> None:
    texts = cx._cfr_texts(cx._hold(cx.CFR_ZIP))
    rows = sf._rows()
    span = Counter()
    alias = Counter()
    alias_units, by_statute, by_cell = set(), Counter(), Counter()
    for uid, r in rows.items():
        flat = texts[(r["volume_file"], r["ordinal"])]
        norm = normalize(flat)
        others = {}
        for m in OTHER.finditer(norm):
            others.setdefault(m.group(1), m.group(3))
        for c in r["citations"]:
            if not c.get("path") or not c.get("span"):
                continue
            sec = c["path"].split("/")[0]
            if c["head"] == "section":
                a, b = c["span"]
                span["section_head"] += 1
                span["flat_misplaced"] += sec not in flat[a:b]
                span["normalized_misplaced"] += sec not in norm[a:b]
            if sec in others:
                outcome = c["outcome"][cx.RP]["outcome"]
                alias["citations"] += 1
                alias["broken"] += outcome in BROKEN
                alias_units.add(uid)
                by_statute[others[sec]] += 1
                by_cell[r["sectno"].split(".")[0]] += outcome in BROKEN
    alias["units"] = len(alias_units)
    total_broken = sum(1 for r in rows.values() for c in r["citations"]
                       if c.get("path") and c["outcome"][cx.RP]["outcome"] in BROKEN)
    pop = {"citations_file": str(cx.CIT.relative_to(cx.ROOT)), "cfr_zip": str(cx.CFR_ZIP.relative_to(cx.ROOT)),
           "units": len(rows), "snapshot": cx.RP}
    entries = [
        {"observed_at": "2025-04-01", "observed_at_note": "2025 CFR edition, citation spans of extractor v2",
         "instrument": {"name": "span-domain check", "version": "1", "scripts": ["spikes/surface1/measure_findings.py"],
                        "method": "for each section-head citation, does the slice at its span contain its section "
                                  "number, in the flat text and in citations.normalize(text)",
                        "known_limits": "checks section heads only; continuation spans are not checked"},
         "population": pop, "quantity": "section-head citations misplaced by slicing each text domain",
         "value": dict(span)},
        {"observed_at": "2025-04-01", "observed_at_note": "2025 CFR edition, outcomes at 119-4",
         "instrument": {"name": "other-statute alias probe", "version": "1",
                        "scripts": ["spikes/surface1/measure_findings.py"],
                        "method": "sections where 'section N... of <another statute>' occurs; count extracted Code "
                                  "citations of the same N in the same section",
                        "known_limits": "upper bound within a section (a bare N may still mean the Code); misses "
                                        "aliases defined in another section; statute list is a regex"},
         "population": pop, "quantity": "Code citations that may be another statute's section, by alias in the same section",
         "value": {**alias, "all_broken": total_broken, "by_statute": dict(by_statute.most_common(10)),
                   "broken_by_cell": dict(by_cell.most_common(10))}},
    ]
    for e in entries:
        print(json.dumps(e["value"], indent=1))
        if not dry:
            print(ledger.append(e)["id"])


if __name__ == "__main__":
    main("--dry-run" in sys.argv)
