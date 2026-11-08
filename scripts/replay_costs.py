"""Measured cost per research instance of a replay run: append-only records usage.cost, Hamut'ay records
usage.cost_usd (both priced from tokens by hamutay.anthropic_direct on --provider anthropic)."""
import json, sys
from pathlib import Path

# Models hamutay's price table lacks: estimated here, from tokens, and labelled so.
# claude-haiku-5-5 (claude-api skill, cached 2026-10-06): $0.10 in / $0.50 out per MTok for prompts up to 100K
# tokens, $0.50 / $2.50 beyond. Cache prices aren't listed; standard multipliers assumed (write x1.25, read x0.1).
ESTIMATED = {"claude-haiku-5-5": {"tiers": [(100_000, 0.10, 0.50), (None, 0.50, 2.50)]}}


def estimate(model: str, u: dict) -> float | None:
    e = ESTIMATED.get(model)
    if not e:
        return None
    a = u.get("anthropic_usage") or u
    inp, rd = int(a.get("input_tokens") or 0), int(a.get("cache_read_input_tokens") or 0)
    wr, out = int(a.get("cache_creation_input_tokens") or 0), int(a.get("output_tokens") or 0)
    prompt = inp + rd + wr
    for limit, pin, pout in e["tiers"]:
        if limit is None or prompt <= limit:
            return (inp * pin + wr * pin * 1.25 + rd * pin * 0.1 + out * pout) / 1e6

HOME = Path.home() / ".levadura" / "research"
total = 0.0
for run in sys.argv[1:]:
    for d in sorted((HOME / run).iterdir()):
        f = d / "session.jsonl"
        if not f.exists():
            continue
        cost, wakes, unpriced, estimated = 0.0, 0, 0, 0
        model = next((json.loads(l).get("model") for l in (d / "run.jsonl").read_text().splitlines()
                      if '"birth"' in l), None) if (d / "run.jsonl").exists() else None
        for line in f.read_text().splitlines():
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            u = r.get("usage") or {}
            c = u.get("cost_usd", u.get("cost"))
            if c is None and u:
                c = estimate(model, u)
                estimated += c is not None
            wakes += 1
            if c is None:
                unpriced += 1
            else:
                cost += c
        total += cost
        print(f"{run}/{d.name:28s} wakes {wakes:2d} ${cost:.3f}" + (f"  UNPRICED {unpriced}" if unpriced else "")
              + (f"  (ESTIMATED for {estimated} records)" if estimated else ""))
print(f"total ${total:.2f}")
