"""Score callers' moves between scales from their footprints (the `queries` documents), not their answers.

    uv run --group plumbing python spikes/surface1/footprints.py caller-opus-1 caller-sonnet-1

Grain, coarse to fine: overview 0, cell 1, drill/cited_by 2, unit 3, cite/follow 4.
A move is *down* if the next call is finer, *up* if coarser. `up_after_text` counts up
moves after the caller's first cite/follow (prediction S3). Writes footprints.json.
"""

import json
import sys
from pathlib import Path

from levadura_salvaje.tenant import connect

GRAIN = {"overview": 0, "cell": 1, "drill": 2, "cited_by": 2, "unit": 3, "cite": 4, "follow": 4}


def score(db, who: str) -> dict:
    calls = list(db.aql.execute("FOR q IN queries FILTER q.who == @w SORT q.at RETURN q", bind_vars={"w": who}))
    seq = []
    for q in calls:
        args = q.get("args") or {k: q.get(k) for k in ("cell", "after", "limit") if k in q}
        seq.append({"at": q["at"], "tool": q["tool"], "grain": GRAIN[q["tool"]], "args": args})
    down = up = up_after_text = 0
    seen_text = False
    for a, b in zip(seq, seq[1:]):
        seen_text = seen_text or a["grain"] == 4
        if b["grain"] > a["grain"]:
            down += 1
        elif b["grain"] < a["grain"]:
            up += 1
            up_after_text += seen_text
    tools: dict[str, int] = {}
    for s in seq:
        tools[s["tool"]] = tools.get(s["tool"], 0) + 1
    return {"who": who, "calls": len(seq), "first": seq[0]["tool"] if seq else None, "tools": tools,
            "down": down, "up": up, "up_after_text": up_after_text,
            "path": "".join(str(s["grain"]) for s in seq), "sequence": seq}


def main(callers: list[str]) -> None:
    db = connect("app")
    out = {w: score(db, w) for w in callers}
    Path(__file__).with_name("footprints.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    for w, s in out.items():
        print(w, {k: v for k, v in s.items() if k != "sequence"})


if __name__ == "__main__":
    main(sys.argv[1:])
