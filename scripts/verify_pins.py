"""Check that every file a ledger entry pins by sha256 still hashes to what it recorded.

    uv run python scripts/verify_pins.py [--since obs-0152]

`ledger.verify()` checks the hash chain of the entries themselves; this checks the files they point
to. An entry superseded by a later one may legitimately mismatch: the later entry records why. Those
are reported apart, and only unexplained mismatches fail. Written 2026-10-03, after I extended a
pinned file in place and broke an earlier entry's pin without noticing until I checked by hand.
"""

import hashlib
import json
import sys
from pathlib import Path

LEDGER = Path("ledger/observations.jsonl")


def pins(entry: dict) -> list[tuple[str, str]]:
    pop = entry.get("population", {})
    out = [(pop[f"{k}_file"], pop[f"{k}_sha256"]) for k in ("results", "citations")
           if f"{k}_file" in pop and f"{k}_sha256" in pop]
    if "partial_sha256" in pop and "results_file" in pop:
        out.append((pop["results_file"].replace(".jsonl", ".partial.jsonl"), pop["partial_sha256"]))
    if isinstance(pop.get("files"), dict) and isinstance(pop.get("sha256"), dict):
        out += [(pop["files"][n], pop["sha256"][n]) for n in pop["files"] if n in pop["sha256"]]
    if isinstance(pop.get("access_log"), dict):
        out.append((pop["access_log"]["file"], pop["access_log"]["sha256"]))
    return out


def main(since: int) -> int:
    entries = [json.loads(line) for line in LEDGER.read_text().splitlines()]
    superseded = {s for e in entries for s in e.get("supersedes", [])}
    ok, explained, bad = 0, [], []
    for e in entries:
        if int(e["id"][4:]) < since:
            continue
        for f, h in pins(e):
            p = Path(f)
            got = hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
            if got == h:
                ok += 1
            elif e["id"] in superseded:
                explained.append((e["id"], f))
            else:
                bad.append((e["id"], f, "missing" if got is None else "mismatch"))
    print(f"pins verified: {ok}; superseded mismatches: {explained}; unexplained: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    args = sys.argv[1:]
    sys.exit(main(int(args[args.index("--since") + 1][4:]) if "--since" in args else 1))
