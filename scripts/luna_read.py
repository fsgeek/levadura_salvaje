"""Read only the replies the resident addressed to us, and record the read.

    uv run python scripts/luna_read.py --by NAME --why "..." [--since CYCLE]

Prints (cycle, timestamp, response) for each cycle. Its state, raw output and tool results are
not printed. Each run appends a line to the resident's reads ledger, which it is told about."""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home() / ".levadura" / "luna"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--by", required=True)
    ap.add_argument("--why", required=True)
    ap.add_argument("--since", type=int, default=0)
    a = ap.parse_args()
    shown = []
    output = []
    try:
        lines = (HOME / "session.jsonl").read_text().splitlines()
    except FileNotFoundError:
        lines = []
    for line in lines:
        r = json.loads(line)
        cyc = r.get("cycle")
        if not isinstance(cyc, int) or cyc < a.since or "response_text" not in r:
            continue
        shown.append(cyc)
        status = " (failed wake)" if r.get("status") == "failed" else ""
        output.append(f"--- cycle {cyc} {r.get('timestamp', '')}{status}\n{r['response_text']}\n")
    with (HOME / "reads.jsonl").open("a") as f:
        f.write(json.dumps({"at": datetime.now(timezone.utc).isoformat(), "by": a.by, "why": a.why,
                            "read": "response_text and failed-wake status only", "cycles": shown}) + "\n")
    print("\n".join(output) if output else "No completed addressed replies yet.")



if __name__ == "__main__":
    main()
