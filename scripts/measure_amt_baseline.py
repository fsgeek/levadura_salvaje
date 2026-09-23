"""Run the AMT baseline (keyword + citation, no classifier) over 26 CFR editions.

Per-section results go to results/amt-baseline-v<version>-<edition>.jsonl,
one line per section. The ledger gets one entry per volume, because a volume
is the unit that has a date. Each entry takes its observed_at from that
volume's structure entry and cites it as ``derived_from`` rather than
restating it, and records the sha256 of the results file.

Usage: uv run python scripts/measure_amt_baseline.py 1997 2025
"""

import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

from levadura_salvaje import baseline
from levadura_salvaje.ledger import LEDGER, append, verify
from levadura_salvaje.sections import sections

INSTRUMENT = {
    "name": "levadura_salvaje.baseline",
    "version": baseline.VERSION,
    "method": (
        f"case-insensitive phrases {list(baseline.PHRASES)}, or a Code citation "
        f"'section(s) <list>' whose item heads include {sorted(baseline.CODE_SECTIONS)} "
        "(never 59A); text = all text of the SECTION element, whitespace-normalized"
    ),
    "defined_in": "predictions/2026-09-23-amt-lens-claude.md",
}


def structure_entries(edition: str) -> dict:
    found = {}
    for line in LEDGER.read_text().splitlines():
        rec = json.loads(line)
        if rec["quantity"] == "cfr26_volume_structure" and rec["population"]["edition"] == edition:
            found[rec["population"]["volume_file"]] = rec
    return found


def main() -> None:
    Path("results").mkdir(exist_ok=True)
    for edition in sys.argv[1:]:
        zip_path = Path(f"data/cfr/CFR-{edition}-title-26.zip")
        structure = structure_entries(edition)
        out = Path(f"results/amt-baseline-v{baseline.VERSION}-{edition}.jsonl")
        per_volume = defaultdict(list)
        with out.open("w") as f:
            for s in sections(zip_path):
                m = baseline.match(s["text"])
                row = {k: s[k] for k in ("volume_file", "ordinal", "sectno", "sha256")} | m
                f.write(json.dumps(row, sort_keys=True) + "\n")
                per_volume[s["volume_file"]].append(row)
        results_sha = hashlib.sha256(out.read_bytes()).hexdigest()
        for volume_file, rows in per_volume.items():
            src = structure[volume_file]
            positives = [r for r in rows if r["positive"]]
            rec = append({
                "observed_at": src["observed_at"],
                "derived_from": src["id"],
                "instrument": INSTRUMENT,
                "population": {
                    "edition": edition,
                    "volume_file": volume_file,
                    "sha256": src["population"]["sha256"],
                    "results_file": str(out),
                    "results_sha256": results_sha,
                },
                "quantity": "amt_baseline_positive_sections",
                "value": {
                    "sections": len(rows),
                    "positive": len(positives),
                    "by_phrase": dict(Counter(p for r in positives for p in r["phrases"])),
                    "by_cite": dict(Counter(c for r in positives for c in r["cites"])),
                    "positive_sections": [[r["ordinal"], r["sectno"]] for r in positives],
                },
            })
            print(rec["id"], edition, volume_file.split("-")[-1], f"{len(positives)}/{len(rows)}")
    print("ledger verified:", verify(), "entries")


if __name__ == "__main__":
    main()
