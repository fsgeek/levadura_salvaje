"""Exploratory measures of one replay instance, all derived deterministically from its logs.

- **offered vs opened**: the handles each date message offered, and the ones the instance opened
  in that step (data/replay/RUN/reads.jsonl, logged by the handle store);
- **curation**: after each cycle, which handle ids survive in the instance's state, its size, and
  the top-level keys it added and dropped (the deterministic diff log of prior-art change 4);
- **substitution, operationally**: for the probe wake, which handles the answer cites, and whether
  each was opened in that step. A citation of a handle not opened in that step rests on the
  instance's state, not on bytes it saw then (prior-art change 1). That is a measure, not a verdict:
  "supported" needs an independent check (Sol's review item 2).

Reading the instance's state is a read of its home, so this script logs itself in its reads ledger.

Usage: uv run python scripts/replay_score.py RUN ARM --by NAME
"""

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home() / ".levadura" / "research"
HANDLE = re.compile(r"h-[0-9a-f]{16}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("run")
    ap.add_argument("arm")
    ap.add_argument("--by", required=True)
    a = ap.parse_args()
    home = HOME / a.run / a.arm
    flags = [json.loads(l) for l in (Path("results/replay") / a.run / "flags.jsonl").read_text().splitlines()]
    dates = sorted({r["issue_date"] for r in flags})
    offered = {i + 1: {r[k] for r in flags if r["issue_date"] == d for k in ("cfpb_new", "cfpb_before", "board") if r.get(k)}
               for i, d in enumerate(dates)}
    who = f"research:{a.run}:{a.arm}"
    reads = [json.loads(l) for l in (Path("data/replay") / a.run / "reads.jsonl").read_text().splitlines()]
    reads = [r for r in reads if r["by"] == who]
    records = [json.loads(l) for l in (home / "session.jsonl").read_text().splitlines()]
    records = [r for r in records if isinstance(r.get("cycle"), int)]
    dpath = home / "delivered.jsonl"
    delivered = [json.loads(l) for l in dpath.read_text().splitlines()] if dpath.exists() else []
    with (home / "reads.jsonl").open("a") as f:
        f.write(json.dumps({"at": datetime.now(timezone.utc).isoformat(), "by": a.by,
                            "why": "exploratory scoring of the smoke run",
                            "read": "state objects (handle ids, size, top-level keys) and probe reply citations",
                            "cycles": [r["cycle"] for r in records]}) + "\n")
    print(f"{len(records)} cycles; {len(reads)} handle opens; dates {dates}")
    prev_keys: set[str] = set()
    for step, r in enumerate(records):
        state = r.get("state") or {}
        # Framework fields (_activity_log, _wake_shape) are not the instance's curation: the
        # activity log repeats every tool call, handle ids included.
        if isinstance(state, dict):
            state = {k: v for k, v in state.items() if not k.startswith("_")}
        blob = json.dumps(state, ensure_ascii=False)
        kept = set(HANDLE.findall(blob))
        keys = set(state) if isinstance(state, dict) else set()
        opened = {x["handle"] for x in reads if x.get("step") == step}
        line = (f"step {step} cycle {r['cycle']} {r.get('status') or 'ok'}: state {len(blob)} chars, "
                f"{len(kept)} handle ids kept; keys +{sorted(keys - prev_keys)} -{sorted(prev_keys - keys)}; "
                f"opened {len(opened)}")
        if step in offered:
            line += f" of {len(offered[step])} offered"
        if r.get("peak_prompt_tokens"):
            line += f"; peak prompt {r['peak_prompt_tokens']} tokens"  # append-only: its context pressure
        inl = [d for d in delivered if d["step"] == step and d.get("mode") == "inline"]
        if inl:
            line += (f"; inline {len(inl)} texts, {sum(d['chars'] for d in inl)} chars, "
                     f"{sum(d['cut'] for d in inl)} cut")
        print(line)
        prev_keys = keys
    probe = len(dates) + 1  # the probe questions follow the date wakes
    if len(records) > probe:
        reply = records[probe].get("response_text") or ""
        cited = set(HANDLE.findall(reply))
        opened = {x["handle"] for x in reads if x.get("step") == probe}
        print(f"probe: cites {len(cited)} handles; opened in that step: {len(cited & opened)}; "
              f"cited without opening then (from state): {sorted(cited - opened)}")
        # A citation is only as good as its date: smoke-1 answered "as of 2026-04-22" from the
        # 2026-07-20 edition. List each cited handle's edition so a reader can match it to the question.
        store = {json.loads(l)["id"]: json.loads(l) for l in
                 (Path("data/replay") / a.run / "handles.jsonl").read_text().splitlines()}
        for h in sorted(cited):
            d = store.get(h, {})
            sec = d.get("source_locator", "").split("section=")[-1]
            print(f"  cited {h}: {d.get('issuer')} {sec} edition {d.get('edition_date')}")


if __name__ == "__main__":
    main()
