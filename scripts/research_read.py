"""Read a research instance's replies, and record the read (docs/research-instances.md, term 5).

    uv run python scripts/research_read.py RUN ARM --by NAME --why "..." [--since CYCLE] [--state]

Prints (cycle, timestamp, reply) for each cycle; with --state, also the state object the instance
kept after each cycle. Tool results and raw model output are not printed. Each run appends a line
to the instance's reads ledger, ~/.levadura/research/RUN/ARM/reads.jsonl.
"""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home() / ".levadura" / "research"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("run")
    ap.add_argument("arm")
    ap.add_argument("--by", required=True)
    ap.add_argument("--why", required=True)
    ap.add_argument("--since", type=int, default=0)
    ap.add_argument("--state", action="store_true")
    a = ap.parse_args()
    home = HOME / a.run / a.arm
    shown, out = [], []
    for line in (home / "session.jsonl").read_text().splitlines():
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        cyc = r.get("cycle")
        if not isinstance(cyc, int) or cyc < a.since or "response_text" not in r:
            continue
        shown.append(cyc)
        status = " (failed wake)" if r.get("status") == "failed" else ""
        out.append(f"--- cycle {cyc} {r.get('timestamp', '')}{status}\n{r['response_text']}")
        if a.state:
            out.append("state: " + json.dumps(r.get("state"), ensure_ascii=False, indent=1))
    with (home / "reads.jsonl").open("a") as f:
        f.write(json.dumps({"at": datetime.now(timezone.utc).isoformat(), "by": a.by, "why": a.why,
                            "read": "replies" + (" and state" if a.state else ""), "cycles": shown}) + "\n")
    print("\n\n".join(out) if out else "No completed replies yet.")


if __name__ == "__main__":
    main()
