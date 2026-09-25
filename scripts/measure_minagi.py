"""Score predictions M1-M5 from the mini-AGI instrument's per-section losses.

Inputs (copied from gazelle): results/minagi-v1/score-seed{0,1,2}.jsonl,
each line one sampled 2025 section's nats/byte under one seed's weights;
results/minagi-v1/seed{n}.log for the training record. The sample and its
groups: data/minagi/sample-2025.json (predictions/2026-09-24-minagi-claude.md).

Usage: uv run python scripts/measure_minagi.py
"""

import hashlib
import json
import re
import statistics
from collections import defaultdict
from pathlib import Path

from levadura_salvaje.ledger import append, verify

D = Path("results/minagi-v1")
SEEDS = (0, 1, 2)
GROUPS = ("G1_identical_unseen", "G2_identical_seen", "G3_fossil_changed", "G4_changed_existing", "G5_new_number")


def main() -> None:
    sample = {(x["volume_file"], x["ordinal"]): x["group"] for x in json.loads(Path("data/minagi/sample-2025.json").read_text())}
    loss = defaultdict(dict)
    meta = {}
    for s in SEEDS:
        for r in map(json.loads, (D / f"score-seed{s}.jsonl").read_text().splitlines()):
            k = (r["volume_file"], r["ordinal"])
            loss[k][s] = r["nats_per_byte"]
            meta[k] = r
    complete = [k for k in sample if len(loss[k]) == len(SEEDS)]
    mean = {k: statistics.fmean(loss[k].values()) for k in complete}
    spread = {k: max(loss[k].values()) - min(loss[k].values()) for k in complete}
    med = {g: statistics.median(mean[k] for k in complete if sample[k] == g) for g in GROUPS}
    n = {g: sum(sample[k] == g for k in complete) for g in GROUPS}
    training = {}
    for s in SEEDS:
        log = (D / f"seed{s}.log").read_text()
        m = re.search(r"read ([\d.]+)M characters in ([\d.]+)m", log)
        a = re.findall(r"after:\s+([\d.]+)", log)
        training[f"seed{s}"] = {"read_M_chars": float(m.group(1)), "minutes": float(m.group(2)),
                                "heldout_1997_after": float(a[-1])}
    rows = [{"volume_file": k[0], "ordinal": k[1], "sectno": meta[k]["sectno"], "group": sample[k],
             "bytes": meta[k]["bytes"], "loss_by_seed": [loss[k][s] for s in SEEDS],
             "mean": round(mean[k], 5), "spread": round(spread[k], 5)} for k in complete]
    out = D / "sections.jsonl"
    out.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in rows))
    rel = lambda a, b: round(1 - med[a] / med[b], 4)  # noqa: E731
    value = {
        "sections_scored": len(complete), "per_group_n": n, "training": training,
        "group_median_nats_per_byte": {g: round(v, 4) for g, v in med.items()},
        "M1_median_seed_spread": round(statistics.median(spread.values()), 4),
        "M2_G1_below_G4": rel("G1_identical_unseen", "G4_changed_existing"),
        "M3_G3_below_G4": rel("G3_fossil_changed", "G4_changed_existing"),
        "M4_highest_of_G1_G3_G4_G5": max(("G1_identical_unseen", "G3_fossil_changed", "G4_changed_existing",
                                          "G5_new_number"), key=med.get),
        "M5_G2_below_G1": rel("G2_identical_seen", "G1_identical_unseen"),
    }
    rec = append({
        "observed_at": "2025-04-01",
        "observed_at_note": "2025 CFR sections read by models trained only on the 1997 CFR",
        "instrument": {
            "name": "mini-AGI surprise (volotat/mini-AGI efd4a16, trained from scratch)", "version": "1",
            "method": "3 seeds x 60 min (~9.8M chars) of reading 95% of 1997 CFR sections on gazelle (RTX 3060 "
                      "Laptop 6GB); config changed only pool.resident 32->16, model.context_end 4096->2048; "
                      "per-section nats/byte with fresh context, no learning; stratified sample of 1,128 2025 sections",
            "known_limits": "a first attempt at seed 0 was damaged by laptop suspend (47 min asleep inside its 60) "
                            "and discarded before scoring was used; mini-AGI dispatch is not deterministic on CUDA",
            "scripts": ["scripts/minagi_pipeline.sh", "scripts/minagi_score.py", "scripts/measure_minagi.py"],
            "predictions": "predictions/2026-09-24-minagi-claude.md",
        },
        "population": {"edition": "2025", "sample": "data/minagi/sample-2025.json (seed minagi-sample-2026-09-24)",
                       "results_file": str(out), "results_sha256": hashlib.sha256(out.read_bytes()).hexdigest()},
        "quantity": "minagi_section_surprise",
        "value": value,
    })
    print(rec["id"], json.dumps(value, indent=1))
    print("ledger verified:", verify())


if __name__ == "__main__":
    main()
