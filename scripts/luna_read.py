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
    ap.add_argument("--resident", choices=("luna", "luna-wanderer"), default="luna")
    a = ap.parse_args()
    home = HOME if a.resident == "luna" else HOME.with_name(a.resident)
    shown = []
    output = []
    incomplete_tail = False
    error_line = None
    try:
        lines = (home / "session.jsonl").read_text().splitlines(keepends=True)
    except FileNotFoundError:
        lines = []
    for index, line in enumerate(lines, 1):
        if index == len(lines) and not line.endswith("\n"):
            incomplete_tail = True
            break
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            error_line = index
            break
        if not isinstance(r, dict):
            error_line = index
            break
        cyc = r.get("cycle")
        if not isinstance(cyc, int) or cyc < a.since or "response_text" not in r:
            continue
        shown.append(cyc)
        status = " (failed wake)" if r.get("status") == "failed" else ""
        output.append(f"--- cycle {cyc} {r.get('timestamp', '')}{status}\n{r['response_text']}\n")
    with (home / "reads.jsonl").open("a") as f:
        f.write(json.dumps({"at": datetime.now(timezone.utc).isoformat(), "by": a.by, "why": a.why,
                            "read": "response_text and failed-wake status only", "cycles": shown,
                            "incomplete_tail": incomplete_tail, "error_line": error_line}) + "\n")
    if error_line is not None:
        raise RuntimeError(f"Unparseable session record at line {error_line}; inspection logged.")
    print("\n".join(output) if output else "No completed addressed replies yet.")
    if incomplete_tail:
        print("An incomplete final record is still being written; omitted from this read.")



if __name__ == "__main__":
    main()
