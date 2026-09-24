"""Jev repeatability: did byte-identical questions get identical answers?

The AMT lens asked Jev about every chunk of every section in two editions.
Many chunks were sent more than once with exactly the same wire state (the
section header plus text; sha256 recorded per call as ``state_sha256``):
sections unchanged between 1997 and 2025, and repeated sections within an
edition. Same model (pinned), same question, same input -- so any spread in
the answers is the instrument's own noise, measured at no extra cost.

No new Jev calls. Reads the per-call partial files; writes one results line
per repeated wire state and one ledger entry.

Run: uv run python scripts/measure_jev_repeat.py
"""

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

from levadura_salvaje.ledger import LEDGER, append

EDITIONS = ("1997", "2025")
THRESHOLDS = (0.01, 0.05, 0.1, 0.2)


def lens_entries() -> list[str]:
    """The ledger entries that published the per-section lens labels."""
    return [rec["id"] for rec in map(json.loads, LEDGER.read_text().splitlines())
            if rec["quantity"] == "amt_lens_section_labels"]


def main() -> None:
    sources, calls = {}, defaultdict(list)
    for edition in EDITIONS:
        partial = Path(f"results/amt-jev-v1-{edition}.partial.jsonl")
        sources[str(partial)] = hashlib.sha256(partial.read_bytes()).hexdigest()
        for line in partial.read_text().splitlines():
            r = json.loads(line)
            if "probabilities" in r:  # refusals carry no answer
                calls[r["state_sha256"]].append(r | {"edition": edition})

    models = Counter(r["model"] for rs in calls.values() for r in rs)
    lens = {r["lens_version"] for rs in calls.values() for r in rs}
    assert len(models) == 1 and lens == {"1"}, (models, lens)

    rows = []
    for state, rs in sorted(calls.items()):
        if len(rs) < 2:
            continue
        labels = Counter(r["label"] for r in rs)
        spread = max(max(r["probabilities"][k] for r in rs) - min(r["probabilities"][k] for r in rs)
                     for k in rs[0]["probabilities"])
        rows.append({
            "state_sha256": state, "calls": len(rs),
            "editions": sorted({r["edition"] for r in rs}),
            "keys": [r["key"] for r in rs], "request_ids": [r["request_id"] for r in rs],
            "labels": dict(labels), "label_flip": len(labels) > 1,
            "max_prob_spread": round(spread, 2),
            "probabilities": [r["probabilities"] for r in rs],
        })

    out = Path("results/jev-repeat-v1.jsonl")
    out.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in rows))
    cross = [r for r in rows if len(r["editions"]) > 1]

    def summary(rs: list[dict]) -> dict:
        return {
            "wire_states": len(rs), "calls": sum(r["calls"] for r in rs),
            "any_prob_change": sum(r["max_prob_spread"] > 0 for r in rs),
            **{f"spread_ge_{t}": sum(r["max_prob_spread"] >= t for r in rs) for t in THRESHOLDS},
            "label_flips": sum(r["label_flip"] for r in rs),
        }

    rec = append({
        "observed_at": "2026-09-23",
        "observed_at_note": "the day the AMT lens calls were made (both editions); "
                            "per-call times were not recorded",
        "instrument": {
            "name": "Jev repeat comparison", "version": "1",
            "method": "group AMT-lens calls by the sha256 of the exact wire state; for each state "
                      "asked two or more times, compare labels and the widest per-label "
                      "probability spread; no new calls",
            "known_limits": "probabilities are rounded to 2 decimals by the API, so spreads under "
                            "0.01 are invisible; repeats are not independent draws scheduled for the "
                            "purpose, they are whatever repetition the corpus contained",
        },
        "population": {
            "model": next(iter(models)), "lens_version": "1",
            "sources": sources,
            "results_file": str(out),
            "results_sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
        },
        "quantity": "jev_repeat_consistency",
        "value": {
            "all": summary(rows),
            "cross_edition": summary(cross),
            "label_flip_states": [
                {"keys": r["keys"], "labels": r["labels"], "probabilities": r["probabilities"]}
                for r in rows if r["label_flip"]],
        },
        "derived_from": lens_entries(),
    })
    print(json.dumps(rec["value"], indent=1)[:1500])
    print(rec["id"])


if __name__ == "__main__":
    main()
