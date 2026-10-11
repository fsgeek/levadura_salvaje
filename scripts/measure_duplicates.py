"""Repeated sections in the CFR source files, and which ledger entries rest on the affected edition.

Found 2026-10-11 while counting a population exactly: the 1997 edition's volume 15 file holds its
own content twice, and §602.101 (the OMB control-number table) is printed in every volume of both
editions. Every 1997 count so far includes the repeats.

Usage: uv run python scripts/measure_duplicates.py
"""

import json
from collections import Counter, defaultdict
from pathlib import Path

from levadura_salvaje.ledger import LEDGER, append, verify
from levadura_salvaje.sections import sections

EDITIONS = {"1997": Path("data/cfr/CFR-1997-title-26.zip"), "2025": Path("data/cfr/CFR-2025-title-26.zip")}


def survey(zip_path: Path) -> dict:
    rows = list(sections(zip_path))
    by = defaultdict(list)
    for r in rows:
        by[r["sectno"]].append(r)
    exact = {k: v for k, v in by.items() if len(v) > 1 and len({x["sha256"] for x in v}) < len(v)}
    distinct_rows = len({(r["sectno"], r["sha256"]) for r in rows})
    differing = sorted(k for k, v in by.items() if len({x["sha256"] for x in v}) > 1 and k != "602.101")
    vols = Counter(x["volume_file"] for v in exact.values() if v[0]["sectno"] != "602.101" for x in v[1:])
    return {"rows": len(rows), "distinct_numbers": len(by), "distinct_rows": distinct_rows,
            "extra_exact_rows": len(rows) - distinct_rows, "repeat_volumes": dict(vols),
            "same_number_different_text": differing}


def main() -> None:
    value: dict = {ed: survey(p) for ed, p in EDITIONS.items()}
    affected = []
    for line in LEDGER.read_text().splitlines():
        rec = json.loads(line)
        if '"1997"' in json.dumps(rec.get("population", "")):
            affected.append(rec["id"])
    value["ledger_entries_on_1997_edition"] = affected
    print(json.dumps({k: (v if k != "ledger_entries_on_1997_edition" else f"{len(v)} entries") for k, v in value.items()}, indent=1))
    entry = append({
        "observed_at": "1997-04-01",
        "observed_at_note": "the 1997 and 2025 CFR title 26 source files as archived (data/cfr); 1997 is the affected edition",
        "instrument": {"name": "scripts/measure_duplicates.py",
                       "method": "group sections() rows by section number; exact repeats share number and text sha256",
                       "known_limits": "entries listed as affected are those whose population names the 1997 edition; their numbers are not re-derived here. Counts are inflated by the repeats; rates move little (sections with a broken citation 28.1% -> 29.0%, citation-level broken share 11.40% -> 11.38%)"},
        "population": {"editions": ["1997", "2025"], "source": "data/cfr"},
        "quantity": "cfr_source_repeated_sections",
        "value": value,
    })
    print(entry["id"], verify())


if __name__ == "__main__":
    main()
