"""Read only the replies the resident addressed to us, and record the read.

    uv run python scripts/resident_read.py --by NAME --why "..." [--since CYCLE]

Prints (cycle, timestamp, response) for each cycle. Its state, raw output and tool results are
not printed. Each run appends a line to the resident's reads ledger, which it is told about."""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home() / ".levadura" / "resident"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--by", required=True)
    ap.add_argument("--why", required=True)
    ap.add_argument("--since", type=int, default=0)
    a = ap.parse_args()
    shown = []
    for line in (HOME / "session.jsonl").read_text().splitlines():
        r = json.loads(line)
        cyc = r.get("cycle")
        if not isinstance(cyc, int) or cyc < a.since or "response_text" not in r:
            continue
        shown.append(cyc)
        print(f"--- cycle {cyc} {r.get('timestamp', '')}\n{r['response_text']}\n")
    with (HOME / "reads.jsonl").open("a") as f:
        f.write(json.dumps({"at": datetime.now(timezone.utc).isoformat(), "by": a.by, "why": a.why,
                            "read": "response_text only", "cycles": shown}) + "\n")


if __name__ == "__main__":
    main()
