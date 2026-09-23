"""Measure Elder's state-object trajectory into the ledger.

Sizes only: no field of Elder's content is read into an entry. The
community's logs are private ("sequence provable, substance private"), so
this records how large Elder's state was and when, never what it held.

Refuses to run unless the log matches the newest digest in its door's
CHECKPOINTS.txt: measure the anchored source, never a derived file (the
cycles.csv beside the log had fallen 69 cycles behind it).

Usage: uv run python scripts/measure_elder.py [path/to/community/elder]
"""

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from levadura_salvaje.ledger import append, verify

DOOR = Path(sys.argv[1] if len(sys.argv) > 1 else "../hamutay/community/elder")
LOG = DOOR / "session.jsonl"
INSTRUMENT = {
    "name": "scripts/measure_elder.py",
    "version": "1",
    "method": (
        "state_bytes = len(utf-8 json.dumps(state)); state_token_estimate is the "
        "log's own field, which equals bytes/4 (an estimate, not a tokenizer count); "
        "cum_input_tokens sums input + cache_read + cache_write over cycles, with "
        "cycles lacking usage counted as zero"
    ),
}


def anchored_population() -> dict:
    newest = [l for l in (DOOR / "CHECKPOINTS.txt").read_text().splitlines() if l.strip()][-1]
    stamp, *fields = newest.split()
    _, expected, size = next(f for f in fields if f.startswith("session.jsonl:")).split(":")
    actual = hashlib.sha256(LOG.read_bytes()).hexdigest()
    if actual != expected or LOG.stat().st_size != int(size):
        sys.exit(f"REFUSED: {LOG} does not match its newest checkpoint ({stamp}); not measuring")
    repo = subprocess.run(["git", "-C", str(DOOR), "rev-parse", "--show-toplevel"],
                          capture_output=True, text=True, check=True).stdout.strip()
    rel = str(DOOR.resolve().relative_to(repo)) + "/CHECKPOINTS.txt"
    commit = subprocess.run(["git", "-C", repo, "log", "-1", "--format=%H", "--", rel],
                            capture_output=True, text=True, check=True).stdout.strip()
    return {
        "source": "hamutay/community/elder/session.jsonl",
        "sha256": actual,
        "bytes": int(size),
        "checkpoint": {"at": stamp, "file": f"hamutay/{rel}", "commit": commit},
    }


def cycles() -> list[dict]:
    rows, cum, missing = [], 0, []
    with LOG.open() as f:
        for line in f:
            d = json.loads(line)
            u = d.get("usage") or {}
            if not u.get("input_tokens"):
                missing.append(d["cycle"])
            cum += sum(u.get(k) or 0 for k in
                       ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"))
            rows.append({
                "cycle": d["cycle"],
                "observed_at": d["timestamp"],
                "state_bytes": len(json.dumps(d.get("state"), ensure_ascii=False).encode()),
                "state_token_estimate": d.get("state_token_estimate"),
                "cum_input_tokens": cum,
            })
    return rows, missing


def main() -> None:
    population = anchored_population()
    rows, missing = cycles()
    peak = max(rows, key=lambda r: r["state_token_estimate"])
    drops = [(rows[i - 1]["state_token_estimate"] - rows[i]["state_token_estimate"], i)
             for i in range(1, len(rows))]
    _, fall = max(drops)
    low = min(rows[fall:], key=lambda r: r["state_token_estimate"])
    may11 = [r for r in rows if r["observed_at"][:10] <= "2026-05-11"][-1]

    marks = [
        (rows[0], "first cycle", None),
        (peak, "largest state", None),
        (may11, "last cycle on or before 2026-05-11", (
            "On 2026-05-11 Tony reported this run as about 70k state tokens after almost "
            "50M input tokens (llm-memory episode 019e1241-3f17-7302-a381-985935c6adb6-line755). "
            "State agrees in magnitude; input does not reconcile with this count and is "
            "recorded as unresolved, not as wrong.")),
        (rows[fall - 1], "cycle before the largest single-cycle drop", None),
        (rows[fall], "cycle after the largest single-cycle drop", None),
        (low, "smallest state after that drop", None),
        (rows[-1], "latest cycle", None),
    ]
    for row, why, note in marks:
        entry = {
            "observed_at": row["observed_at"],
            "instrument": INSTRUMENT,
            "population": population,
            "quantity": "elder_state_size",
            "value": {k: row[k] for k in ("cycle", "state_bytes", "state_token_estimate",
                                          "cum_input_tokens")},
            "selected_because": why,
        }
        if note:
            entry["note"] = note
        if missing:
            entry["caveat"] = f"cycles without recorded usage (counted as zero input): {missing}"
        print(append(entry)["id"], why, row["cycle"], row["state_token_estimate"])
    print("ledger verified:", verify(), "entries")


if __name__ == "__main__":
    main()
