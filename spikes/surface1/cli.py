"""The surface as a command line, one call per invocation, JSON out.

    uv run --group plumbing python spikes/surface1/cli.py --who NAME overview
    ... cell 1 [--top 15] [--cursor 0]
    ... drill 1 [--cursor TOKEN] [--limit 40]
    ... cited-by 1201 [--cursor 0] [--limit 40]
    ... unit UNIT_ID [--cursor 0] [--limit 50] [--only-broken]
    ... cite UNIT_ID INDEX
    ... follow unit|provision ID [--offset 0] [--length 4000]
    ... measure (--cited-by N | --cell C [--all]) --pattern REGEX [--near N] [--window 400] [--case-sensitive]

Every error, argument errors included, comes back as {"error": ...} with exit status 2.
Failed calls are recorded as footprints too.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import instrument  # noqa: E402
from surface import Surface  # noqa: E402


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(f"arguments: {message}")


def _parser() -> argparse.ArgumentParser:
    p = _Parser(prog="surface")
    p.add_argument("--who", required=True)
    sub = p.add_subparsers(dest="tool", required=True, parser_class=_Parser)
    sub.add_parser("overview")
    s = sub.add_parser("cell"); s.add_argument("cell"); s.add_argument("--top", type=int, default=15)
    s.add_argument("--cursor", type=int, default=0)
    s = sub.add_parser("drill"); s.add_argument("cell"); s.add_argument("--cursor"); s.add_argument("--limit", type=int, default=40)
    s = sub.add_parser("cited-by"); s.add_argument("target"); s.add_argument("--cursor", type=int, default=0)
    s.add_argument("--limit", type=int, default=40)
    s = sub.add_parser("unit"); s.add_argument("unit"); s.add_argument("--cursor", type=int, default=0)
    s.add_argument("--limit", type=int, default=50); s.add_argument("--only-broken", action="store_true")
    s = sub.add_parser("cite"); s.add_argument("unit"); s.add_argument("index", type=int)
    s = sub.add_parser("follow"); s.add_argument("kind", choices=["unit", "provision"]); s.add_argument("id")
    s.add_argument("--offset", type=int, default=0); s.add_argument("--length", type=int, default=4000)
    s = sub.add_parser("measure", help="run a regular expression over a population; counts and samples of both sides")
    g = s.add_mutually_exclusive_group(required=True)
    g.add_argument("--cited-by", help="population: units citing this Code section")
    g.add_argument("--cell", help="population: a cell's members (units with a broken citation)")
    s.add_argument("--all", action="store_true", help="with --cell: every unit in the cell, not just members")
    s.add_argument("--pattern", required=True, help="a Python regular expression over each unit's text")
    s.add_argument("--near", help="only within --window characters of a citation of this Code section")
    s.add_argument("--window", type=int, default=instrument.WINDOW)
    s.add_argument("--case-sensitive", action="store_true")
    s.add_argument("--sample", type=int, default=instrument.SAMPLE)
    return p


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    sf, tool = None, None
    try:
        a = _parser().parse_args(argv)
        tool = a.tool
        sf = Surface(a.who)
        out = {
            "overview": lambda: sf.overview(),
            "cell": lambda: sf.cell(a.cell, a.top, a.cursor),
            "drill": lambda: sf.drill(a.cell, a.cursor, a.limit),
            "cited-by": lambda: sf.cited_by(a.target, a.cursor, a.limit),
            "unit": lambda: sf.unit(a.unit, a.cursor, a.limit, a.only_broken),
            "cite": lambda: sf.cite(a.unit, a.index),
            "follow": lambda: sf.follow(a.kind, a.id, a.offset, a.length),
            "measure": lambda: instrument.measure(
                sf, {"cited_by": a.cited_by} if a.cited_by else {"cell": a.cell, "all": a.all},
                a.pattern, a.near, a.window, not a.case_sensitive, a.sample),
        }[a.tool]()
    except Exception as e:  # noqa: BLE001 -- the contract is JSON out, whatever failed
        err = f"{type(e).__name__}: {e}"
        if sf is not None:
            try:
                sf.failed(tool, {"argv": argv}, err)
            except Exception:  # noqa: BLE001
                pass
        print(json.dumps({"error": err}))
        return 2
    print(json.dumps(out, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
