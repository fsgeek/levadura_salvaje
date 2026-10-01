"""The surface as a command line, one call per invocation, JSON out.

    uv run --group plumbing python spikes/surface1/cli.py --who NAME overview
    ... cell 1 [--top 15]
    ... drill 1 [--cursor TOKEN] [--limit 40]
    ... cited-by 1201 [--cursor 0] [--limit 40]
    ... unit UNIT_ID [--cursor 0] [--limit 50] [--only-broken]
    ... cite UNIT_ID INDEX
    ... follow unit|provision ID [--offset 0] [--length 4000]

Errors come back as {"error": ...} with exit status 2, never a traceback.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from surface import Surface  # noqa: E402


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="surface")
    p.add_argument("--who", required=True)
    sub = p.add_subparsers(dest="tool", required=True)
    sub.add_parser("overview")
    s = sub.add_parser("cell"); s.add_argument("cell"); s.add_argument("--top", type=int, default=15)
    s = sub.add_parser("drill"); s.add_argument("cell"); s.add_argument("--cursor"); s.add_argument("--limit", type=int, default=40)
    s = sub.add_parser("cited-by"); s.add_argument("target"); s.add_argument("--cursor", type=int, default=0)
    s.add_argument("--limit", type=int, default=40)
    s = sub.add_parser("unit"); s.add_argument("unit"); s.add_argument("--cursor", type=int, default=0)
    s.add_argument("--limit", type=int, default=50); s.add_argument("--only-broken", action="store_true")
    s = sub.add_parser("cite"); s.add_argument("unit"); s.add_argument("index", type=int)
    s = sub.add_parser("follow"); s.add_argument("kind", choices=["unit", "provision"]); s.add_argument("id")
    s.add_argument("--offset", type=int, default=0); s.add_argument("--length", type=int, default=4000)
    a = p.parse_args(argv)
    try:
        sf = Surface(a.who)
        out = {
            "overview": lambda: sf.overview(),
            "cell": lambda: sf.cell(a.cell, a.top),
            "drill": lambda: sf.drill(a.cell, a.cursor, a.limit),
            "cited-by": lambda: sf.cited_by(a.target, a.cursor, a.limit),
            "unit": lambda: sf.unit(a.unit, a.cursor, a.limit, a.only_broken),
            "cite": lambda: sf.cite(a.unit, a.index),
            "follow": lambda: sf.follow(a.kind, a.id, a.offset, a.length),
        }[a.tool]()
    except (KeyError, ValueError, LookupError) as e:
        print(json.dumps({"error": f"{type(e).__name__}: {e}"}))
        return 2
    print(json.dumps(out, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
