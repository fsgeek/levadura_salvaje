"""How long have the 2025 CFR's dead citations been dead? (predictions A1-A4)

For each citation occurrence (extractor v2) whose section is repealed at
119-4, directly or through a repealed range element, the repeal year is the
latest date in that section element's heading ("Repealed. Pub. L. 94-455,
... Oct. 4, 1976"). Repealed subdivisions of in-force sections carry no date
in USLM and are excluded.

Usage: uv run python scripts/measure_fossil_age.py
"""

import hashlib
import json
import re
import statistics
from collections import Counter
from pathlib import Path

from levadura_salvaje.ledger import append, verify
from levadura_salvaje.resolve import DASHES, section_key

RP = "119-4"
CITATIONS = Path("results/cfr-usc-citations-v2-2025.jsonl")
DATE = re.compile(r"(?:Jan|Feb|Mar|Apr|May|June|July|Aug|Sept|Oct|Nov|Dec)\.? \d{1,2}, (\d{4})")


def repeal_years() -> tuple[dict, list]:
    exact, ranges = {}, []
    for line in Path(f"results/usc26-provisions-{RP}.jsonl").read_text().splitlines():
        p = json.loads(line)
        if p["level"] != "section" or p["status"] != "repealed":
            continue
        years = [int(y) for y in DATE.findall(p["heading"])]
        sec = p["path"].translate(DASHES)[1:]
        if "..." in sec:
            lo, hi = (section_key(x) for x in sec.split("..."))
            ranges.append((lo, hi, max(years) if years else None, p["heading"]))
        else:
            exact[sec] = (max(years) if years else None, p["heading"])
    return exact, ranges


def main() -> None:
    exact, ranges = repeal_years()
    occ, per_section = [], {}
    for line in CITATIONS.read_text().splitlines():
        row = json.loads(line)
        for c in row["citations"]:
            if c.get("section_outcome", {}).get(RP) != "repealed":
                continue
            sec = c["path"].translate(DASHES).split("/")[0]
            if sec in exact:
                year = exact[sec][0]
            else:
                k = section_key(sec)
                year = next((y for lo, hi, y, _ in ranges if k and lo <= k <= hi), None)
            occ.append({"sectno": row["sectno"], "cited": c["path"], "section": sec, "repeal_year": year})
            per_section[sec] = year
    out = Path("results/cfr-fossil-age-v2-2025.jsonl")
    out.write_text("".join(json.dumps(o, sort_keys=True) + "\n" for o in occ))

    years = [o["repeal_year"] for o in occ if o["repeal_year"]]
    decades = Counter(f"{y // 10 * 10}s" for y in per_section.values() if y)
    rec = append({
        "observed_at": "2025-04-01",
        "observed_at_note": "2025 CFR citations read against 26 USC at 119-4; ages are relative to 2025",
        "instrument": {
            "name": "scripts/measure_fossil_age.py", "version": "1",
            "method": "repeal year = latest 'Mon. D, YYYY' date in the repealed section element's heading "
                      "(or its range element's); occurrences via repealed subdivisions excluded",
            "predictions": "predictions/2026-09-24-fossil-age-claude.md",
        },
        "population": {"edition": "2025", "release_point": RP,
                       "results_file": str(out), "results_sha256": hashlib.sha256(out.read_bytes()).hexdigest()},
        "quantity": "cfr_fossil_repeal_age",
        "value": {
            "occurrences": len(occ), "occurrences_dated": len(years),
            "distinct_repealed_sections_cited": len(per_section),
            "A1_median_repeal_year": statistics.median(years),
            "A2_repealed_by_2005": [sum(y <= 2005 for y in years), len(years)],
            "A3_repealed_2017": [sum(y == 2017 for y in years), len(years)],
            "A4_distinct_sections_by_decade": dict(sorted(decades.items())),
            "occurrences_by_decade": dict(sorted(Counter(f"{y // 10 * 10}s" for y in years).items())),
            "oldest": sorted({(y, s) for s, y in per_section.items() if y})[:10],
        },
    })
    print(rec["id"], json.dumps(rec["value"], indent=1))
    print("ledger verified:", verify())


if __name__ == "__main__":
    main()
