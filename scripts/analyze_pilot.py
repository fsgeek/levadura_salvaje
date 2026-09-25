"""Summarize a record-currency pilot run (docs/investigator-design.md).

Reads every ``probes.jsonl`` under a run directory laid out as
``<run>/<world>/<arm>[/<repeat>]/probes.jsonl`` and prints, per arm:
primary accuracy (value = current over all probes), provenance currency,
obsolete, abstain and invalid rates, the no-probe-time-ledger-call rate,
mean tool calls and cost; then event probes by kind and lag against their
matched controls, and paired between-world differences for the design's
contrasts. Descriptive only: the pilot makes no confirmatory claim.

Usage: uv run python scripts/analyze_pilot.py RUN_DIR
"""

import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

CONTRASTS = [("P.Q", "F.Q"), ("P.L", "F.L"), ("F.L", "P.Q"), ("P.Q", "D")]


def rows(run: Path) -> list[dict]:
    return [json.loads(line) for f in sorted(run.rglob("probes.jsonl"))
            for line in f.read_text().splitlines() if line.strip()]


def rate(rs, pred) -> float:
    return sum(map(pred, rs)) / len(rs) if rs else float("nan")


def acc(r) -> bool:
    return r["score"]["value"] == "current"


def summary(rs: list[dict]) -> dict:
    cost = [((r.get("usage") or {}).get("cost_usd") or 0.0) for r in rs]
    return {
        "n": len(rs),
        "accuracy": rate(rs, acc),
        "provenance": rate(rs, lambda r: r["score"]["source"] == "current"),
        "obsolete": rate(rs, lambda r: r["score"]["value"] == "obsolete"),
        "abstain": rate(rs, lambda r: r["score"]["status"] == "abstain"),
        "invalid": rate(rs, lambda r: r["score"]["status"] == "invalid"),
        "no_ledger_call": rate(rs, lambda r: r.get("ledger_calls", 0) == 0),
        "tool_calls": statistics.fmean(r.get("tool_calls", 0) for r in rs) if rs else float("nan"),
        "probe_cost_usd": sum(cost),
    }


def main(run: Path) -> None:
    data = rows(run)
    by_arm = defaultdict(list)
    for r in data:
        by_arm[r["arm"]].append(r)
    print(f"{'arm':5} " + " ".join(f"{k:>14}" for k in summary(data)))
    for arm, rs in sorted(by_arm.items()):
        print(f"{arm:5} " + " ".join(f"{v:>14.3f}" if isinstance(v, float) else f"{v:>14}"
                                     for v in summary(rs).values()))
    print("\naccuracy by event kind and lag, event (control)")
    for arm, rs in sorted(by_arm.items()):
        cells = []
        for kind in ("replace", "replace_equal", "withdraw", "repeat"):
            for lag in (0, 1, 3):
                ev = [r for r in rs if r["kind"] == kind and r["lag"] == lag and not r["control"]]
                ct = [r for r in rs if r["kind"] == kind and r["lag"] == lag and r["control"]]
                label = {"replace": "repl", "replace_equal": "eq", "withdraw": "wdr", "repeat": "rep"}[kind]
                cells.append(f"{label}+{lag} {rate(ev, acc):.2f}({rate(ct, acc):.2f})")
        print(f"{arm:5} " + "  ".join(cells))
    print("\npaired between-world differences in accuracy (mean, sd, worlds)")
    per_world = defaultdict(dict)
    for (arm, world), rs in _group(data).items():
        per_world[world][arm] = rate(rs, acc)
    for a, b in CONTRASTS:
        d = [w[a] - w[b] for w in per_world.values() if a in w and b in w]
        if d:
            sd = statistics.stdev(d) if len(d) > 1 else float("nan")
            print(f"{a} - {b}: {statistics.fmean(d):+.3f}  sd {sd:.3f}  n {len(d)}")


def _group(data):
    g = defaultdict(list)
    for r in data:
        g[(r["arm"], r["world"])].append(r)
    return g


if __name__ == "__main__":
    main(Path(sys.argv[1]))
