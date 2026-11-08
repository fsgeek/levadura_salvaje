"""Exploratory: collect each smoke-3 instance's probe answer (through research_read.py, so every read is
logged), and write a blind packet (random ids, no arm) plus a separate key."""
import json, random, re, subprocess, sys
from pathlib import Path

HOME = Path.home() / ".levadura" / "research"
OUT = Path("results/replay/smoke-3/q3")
import sys as _s
TAG = "" if len(_s.argv) < 2 else "-" + "-".join(_s.argv[1:])
PACKET = Path.home() / ".levadura" / "research" / "smoke-3-q3" / f"packet{TAG}.jsonl"  # full answers stay out of the repo
RUNS = sys.argv[1:] or ["smoke-3", "smoke-3-r1b", "smoke-3-r2", "smoke-3-r3"]
TAG = "" if not sys.argv[1:] else "-" + "-".join(sys.argv[1:])
items, key = [], {}
rng = random.Random(20261108)
for run in RUNS:
    for d in sorted((HOME / run).iterdir()):
        ev = [json.loads(l) for l in (d / "run.jsonl").read_text().splitlines()]
        # exchanges in order: one per wake event, plus one per stop confirmation, before the probe
        n = 0
        probe_cycle = None
        for e in ev:
            if e.get("event") == "stop_confirmation":
                n += 1
            elif e.get("event") == "wake":
                n += 1
                if e.get("kind") == "probe":
                    probe_cycle = n
                    break
        if probe_cycle is None:
            key[f"{run}/{d.name}"] = {"probe": None, "note": "no probe wake (run cut short by the phrase detector)"}
            continue
        out = subprocess.run(["uv", "run", "python", "scripts/research_read.py", run, d.name,
                              "--by", "levadura steward (Claude Opus 5.5)", "--since", str(probe_cycle),
                              "--why", "smoke-3 Q3 scoring: the probe answer only"],
                             capture_output=True, text=True).stdout
        m = re.search(rf"--- cycle {probe_cycle} [^\n]*\n(.*?)(?=\n\n--- cycle |\Z)", out, re.S)
        ans = m.group(1) if m else ""
        ok = "1026.43" in ans or "226.43" in ans
        iid = f"q{rng.randrange(16**6):06x}"
        items.append({"id": iid, "answer": ans})
        key[iid] = {"instance": f"{run}/{d.name}", "probe_cycle": probe_cycle, "mentions_43": ok, "chars": len(ans)}
rng.shuffle(items)
PACKET.parent.mkdir(parents=True, exist_ok=True); PACKET.write_text("".join(json.dumps(i) + "\n" for i in items))
(OUT / f"key{TAG}.json").write_text(json.dumps(key, indent=1))
print(len(items), "answers;", sum(v.get("mentions_43", False) for v in key.values()), "mention 1026.43/226.43")
print([k for k, v in key.items() if v.get("probe") is None and "note" in v])
