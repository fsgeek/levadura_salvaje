"""Score the record-currency pilot's predictions R1-R11 from raw probes.

Computes each prediction's numbers directly from ``probes.jsonl`` (not from
``analyze_pilot.py``), prints them, and with ``--record`` appends one ledger
entry. Verdicts and judgment calls are in docs/pilot-v1-scorecard.md; this
script records the numbers they rest on.

Usage: uv run python scripts/score_pilot.py results/pilot-v1 [--record]
"""

import hashlib
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

from levadura_salvaje.ledger import append

MODEL_ARMS = ["P.Q", "F.Q", "P.L", "F.L"]


def rows(run: Path) -> list[dict]:
    return [json.loads(line) for f in sorted(run.rglob("probes.jsonl"))
            for line in f.read_text().splitlines() if line.strip()]


def frac(rs, pred) -> list[int]:
    return [sum(map(pred, rs)), len(rs)]


def current(r) -> bool:
    return r["score"]["value"] == "current"


def main() -> None:
    run = Path(sys.argv[1])
    rs = rows(run)
    arm = defaultdict(list)
    for r in rs:
        arm[r["arm"]].append(r)

    def events(a, kind):
        return [r for r in arm[a] if not r["control"] and r["kind"] == kind]

    def paired(a, b):
        by = defaultdict(dict)
        for x in (a, b):
            for w in {r["world"] for r in arm[x]}:
                ws = [r for r in arm[x] if r["world"] == w]
                by[w][x] = sum(map(current, ws)) / len(ws)
        return round(statistics.mean(v[a] - v[b] for v in by.values()), 4)

    value = {
        "accuracy": {a: frac(arm[a], current) for a in sorted(arm)},
        "R4_mean_paired_FL_minus_PQ": paired("F.L", "P.Q"),
        "no_probe_time_ledger_call": {a: frac(arm[a], lambda r: r.get("ledger_calls", 0) == 0)
                                      for a in MODEL_ARMS},
        "replace_obsolete": {a: frac(events(a, "replace"),
                                     lambda r: r["score"]["value"] == "obsolete")
                             for a in MODEL_ARMS},
        "replace_accuracy": {a: frac(events(a, "replace"), current) for a in MODEL_ARMS},
        "withdraw_accuracy": {a: frac(events(a, "withdraw"), current) for a in MODEL_ARMS},
        "equal_value_errors": {a: {
            "value": sum(r["score"]["value"] != "current" for r in events(a, "replace_equal")),
            "provenance": sum(r["score"]["source"] != "current"
                              for r in events(a, "replace_equal")),
            "n": len(events(a, "replace_equal"))} for a in MODEL_ARMS},
        "event_vs_control": {a: [sum(current(r) for r in arm[a] if not r["control"]),
                                 sum(current(r) for r in arm[a] if r["control"]),
                                 sum(not r["control"] for r in arm[a])] for a in MODEL_ARMS},
        "invalid": {a: frac(arm[a], lambda r: r["score"]["status"] == "invalid")
                    for a in sorted(arm)},
        "logged_cost_usd": round(sum(
            (json.loads(line).get("usage") or {}).get("cost_usd") or 0
            for f in run.rglob("*.jsonl") if f.name != "probes.jsonl"
            for line in f.read_text().splitlines() if line.strip()), 2),
        "C_calls_without_cost": sum(1 for r in arm["C"]
                                    if not (r.get("usage") or {}).get("cost_usd")),
    }
    print(json.dumps(value, indent=1))
    if "--record" not in sys.argv:
        return
    probes = sorted(run.rglob("probes.jsonl"))
    digest = hashlib.sha256(b"".join(f.read_bytes() for f in probes)).hexdigest()
    rec = append({
        "observed_at": "2026-09-25",
        "observed_at_note": "the day every pilot-v1 arm-run was made",
        "instrument": {
            "name": "record-currency pilot scoring", "version": "1",
            "method": "counts per stamped prediction computed from raw probes.jsonl, independent "
                      "of analyze_pilot.py; verdicts reconciled with two blind outside scorers "
                      "(Codex, Gemini 3.1 Pro) in docs/pilot-v1-scorecard.md",
            "known_limits": "logged cost omits the 216 arm-C calls, which reached the model but "
                            "recorded no usage; the scorer is the same model as the designer, "
                            "with a fresh context",
            "predictions": "predictions/2026-09-25-record-currency-pilot-claude.md",
            "scripts": ["scripts/score_pilot.py"],
        },
        "population": {
            "run": str(run), "probe_files": len(probes), "probes": len(rs),
            "probes_sha256": digest,
            "raw_logs": "release data/pilot-v1-raw-logs",
        },
        "quantity": "record_currency_pilot_scores",
        "value": value,
    })
    print(rec["id"])


if __name__ == "__main__":
    main()
