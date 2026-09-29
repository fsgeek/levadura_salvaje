"""Build the retrospective forecast's label table and 1997 feature table
(docs/retrospective-design.md, draft 3).

Two files, written separately so the features can be frozen before labels
are joined:

- results/retro-features-v1-1997.jsonl: allowlisted inputs only (the 1997
  CFR text and obs-0139's resolution against GPO USCODE-1996).
- results/retro-labels-v1.jsonl: each cohort section's literal 2025 status
  (absent / present-broken / present-clean) against USC 119-4 (obs-0129).

Cohort: 1997 section numbers that occur once in the 1997 edition (the
turnover filter, obs-0141). Duplicate-text groups are recorded for grouped
cross-validation.

Usage: uv run python scripts/retro_build.py [features|labels]
"""

import hashlib
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

from levadura_salvaje.sections import sections

CIT_1997 = Path("results/cfr-usc-citations-v2-1997.jsonl")
CIT_2025 = Path("results/cfr-usc-citations-v2-2025.jsonl")
CFR_1997 = Path("data/cfr/CFR-1997-title-26.zip")
FR_YEAR = re.compile(r"FR \d+, [A-Z][a-z]{2,4}\.? \d{1,2}, (19\d\d|20\d\d)")


def unique(path: Path) -> dict:
    rows = [json.loads(line) for line in path.read_text().splitlines()]
    counts = Counter(r["sectno"] for r in rows)
    return {r["sectno"]: r for r in rows if counts[r["sectno"]] == 1}


def write(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in rows))
    print(path, len(rows), hashlib.sha256(path.read_bytes()).hexdigest())


def features() -> None:
    old = unique(CIT_1997)
    text = {(s["volume_file"], s["ordinal"]): s["text"] for s in sections(CFR_1997)}
    rows = []
    for sectno, r in sorted(old.items()):
        t = text[(r["volume_file"], r["ordinal"])]
        years = [int(y) for y in FR_YEAR.findall(t)]
        n = len(r["citations"])
        rows.append({
            "sectno": sectno, "volume_file": r["volume_file"], "ordinal": r["ordinal"],
            "text_sha256": r["sha256"],
            "fossil_1997": r["broken"] > 0,
            "broken": r["broken"], "citations": n,
            "broken_share": round(r["broken"] / n, 4) if n else 0.0,
            "log_chars": round(math.log(len(t) + 1), 4),
            "part": sectno.split(".")[0],
            "first_fr_year": min(years) if years else None,
            "last_fr_year": max(years) if years else None,
        })
    write(Path("results/retro-features-v1-1997.jsonl"), rows)


def labels() -> None:
    old, new = unique(CIT_1997), unique(CIT_2025)
    rows = []
    for sectno in sorted(old):
        if sectno not in new:
            status = "absent"
        else:
            status = "present-broken" if new[sectno]["broken"]["119-4"] > 0 else "present-clean"
        rows.append({"sectno": sectno, "status_2025": status})
    write(Path("results/retro-labels-v1.jsonl"), rows)


if __name__ == "__main__":
    {"features": features, "labels": labels}[sys.argv[1]]()
