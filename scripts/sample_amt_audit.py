"""Draw the blind audit sample for the AMT lens (2025 edition).

Strata, as registered in predictions/2026-09-23-amt-lens-claude.md (P8):
  a        150 sections drawn at random from Jev's "none" pile;
  b        every section that is baseline-positive but Jev "none";
  control  30 sections drawn at random from Jev's operative + incidental
           labels, so the labeler cannot assume everything is "none" and
           so agreement on positives is measured too.
The seed is the commit that stamped the predictions, fixed before any Jev
result existed. Items are shuffled and numbered; the labeler sees only
items/<id>.txt. The key (stratum, Jev label) is written outside the items
directory and must not be shown to the labeler.

Usage: uv run python scripts/sample_amt_audit.py <items_dir> <key_file>
"""

import json
import random
import sys
from pathlib import Path

from levadura_salvaje.chunks import header
from levadura_salvaje.sections import sections

SEED = "68e1a86fbcc69d30fa15b40a234b62d15e177468"
EDITION = "2025"


def rows(path: str) -> dict:
    return {(r["volume_file"], r["ordinal"]): r for r in map(json.loads, open(path))}


def main() -> None:
    items_dir, key_file = Path(sys.argv[1]), Path(sys.argv[2])
    jev = rows(f"results/amt-jev-v1-{EDITION}.jsonl")
    base = rows(f"results/amt-baseline-v1-{EDITION}.jsonl")
    order = sorted(jev)
    rng = random.Random(SEED)
    none = [k for k in order if jev[k]["label"] == "none"]
    positive = [k for k in order if jev[k]["label"] != "none"]
    strata = {}
    for k in rng.sample(none, 150):
        strata.setdefault(k, []).append("a")
    for k in none:
        if base[k]["positive"]:
            strata.setdefault(k, []).append("b")
    for k in rng.sample(positive, 30):
        strata.setdefault(k, []).append("control")
    chosen = sorted(strata)
    rng.shuffle(chosen)

    items_dir.mkdir(parents=True, exist_ok=True)
    wanted = {k: f"item-{i:03d}" for i, k in enumerate(chosen, 1)}
    key = []
    for s in sections(Path(f"data/cfr/CFR-{EDITION}-title-26.zip")):
        k = (s["volume_file"], s["ordinal"])
        if k in wanted:
            (items_dir / f"{wanted[k]}.txt").write_text(header(s["sectno"], s["subject"], 1, 1) + s["text"])
            key.append({"item": wanted[k], "volume_file": k[0], "ordinal": k[1], "sectno": s["sectno"],
                         "sha256": s["sha256"], "strata": strata[k], "jev_label": jev[k]["label"],
                         "baseline_positive": base[k]["positive"], "chars": len(s["text"])})
    key.sort(key=lambda r: r["item"])
    key_file.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in key))
    print(f"{len(key)} items: a={sum('a' in r['strata'] for r in key)} "
          f"b={sum('b' in r['strata'] for r in key)} control={sum('control' in r['strata'] for r in key)}; "
          f"{sum(r['chars'] for r in key):,} chars")


if __name__ == "__main__":
    main()
