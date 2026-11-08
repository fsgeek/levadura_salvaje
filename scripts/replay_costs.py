"""Measured cost per research instance of a replay run: append-only records usage.cost, Hamut'ay records
usage.cost_usd (both priced from tokens by hamutay.anthropic_direct on --provider anthropic)."""
import json, sys
from pathlib import Path

HOME = Path.home() / ".levadura" / "research"
total = 0.0
for run in sys.argv[1:]:
    for d in sorted((HOME / run).iterdir()):
        f = d / "session.jsonl"
        if not f.exists():
            continue
        cost, wakes, unpriced = 0.0, 0, 0
        for line in f.read_text().splitlines():
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            u = r.get("usage") or {}
            c = u.get("cost_usd", u.get("cost"))
            wakes += 1
            if c is None:
                unpriced += 1
            else:
                cost += c
        total += cost
        print(f"{run}/{d.name:28s} wakes {wakes:2d} ${cost:.3f}" + (f"  UNPRICED {unpriced}" if unpriced else ""))
print(f"total ${total:.2f}")
