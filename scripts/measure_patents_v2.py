"""Patents v2: title-35 citations read at the date they state, and the AIA transition mentions, in 37 CFR 2025.

Deterministic; predictions in predictions/2026-10-27-patents-v2-claude.md (stamped at 8f52946 before this ran).
v1's resolver (current Code) runs unchanged as the control; a citation dated_cites marks as old law is also
resolved against 35 U.S.C. as of 2010 (GPO, before the AIA). Builds audit packets Z2a (marked plus unmarked
citations) and Z2b (transition mentions). One ledger entry, none with --dry-run.

Usage: uv run python scripts/measure_patents_v2.py [--dry-run]
"""

import hashlib
import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

from levadura_salvaje import dated_cites, usc_cites
from levadura_salvaje.gpo_usc import provisions as gpo_provisions
from levadura_salvaje.ledger import append, verify
from levadura_salvaje.resolve import Statute
from levadura_salvaje.sections import distinct_sections

RP, SEED = "119-120", 20261027
CFR = Path("data/patents/CFR-2025-title-37.zip")
GPO = Path("data/patents/USCODE-2010-title35.htm")
GPO_TABLE = Path("results/usc35-provisions-gpo-2010.jsonl")
OUT = Path("results/patents-v2-cites.jsonl")
AUDIT = Path("results/patents-v2-audit-z2")
PREDICTIONS = "predictions/2026-10-27-patents-v2-claude.md"
HYBRID = re.compile(r"contains?,?\s+or\s+contained,?\s+at\s+any\s+time|at\s+any\s+time\s+contained|ever\s+contained", re.I)


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    dry = "--dry-run" in sys.argv
    GPO_TABLE.write_text("".join(json.dumps(p, sort_keys=True) + "\n" for p in gpo_provisions(GPO)))
    now = {"35": Statute.load(RP, title="35")}
    then = {"35": Statute.load("gpo-2010", results=GPO_TABLE, title="35")}
    rows, mentions, texts, hybrid_secs = [], [], {}, set()
    for s in distinct_sections(CFR):
        text = usc_cites.normalize(s["text"])
        texts[s["sectno"]] = text
        for c in usc_cites.extract(text, normalized=True):
            if c["title"] != "35":
                continue
            mk = dated_cites.marker(text, tuple(c["span"]))
            r = {"sectno": s["sectno"], "path": c["path"], "span": c["span"], **mk,
                 "now": usc_cites.resolve(c, now)["outcome"]}
            if mk["marker"]:
                r["then"] = usc_cites.resolve(c, then)["outcome"]
            rows.append(r)
        for x in dated_cites.transition_mentions(text):
            mentions.append({"sectno": s["sectno"], **x})
        if HYBRID.search(text):
            hybrid_secs.add(s["sectno"])
    OUT.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in rows))

    marked = [r for r in rows if r["marker"]]
    notres = [r for r in rows if r["now"] != "resolves"]
    m = {
        "title35_cites": len(rows),
        "D1_marked": len(marked),
        "markers": dict(Counter(r["marker"] for r in marked)),
        "D2_nonresolving_marked": f"{sum(bool(r['marker']) for r in notres)}/{len(notres)}",
        "D3_marked_resolve_2010": round(sum(r["then"] == "resolves" for r in marked) / len(marked), 4) if marked else None,
        "D4_marked_also_resolve_now": round(sum(r["now"] == "resolves" for r in marked) / len(marked), 4) if marked else None,
        "C1_sections_with_transition_dates": len({x["sectno"] for x in mentions}),
        "transition_mentions": len(mentions),
        "C2_conditioned_share": round(sum(x["class"] == "conditioned" for x in mentions) / len(mentions), 4)
        if mentions else None,
        "C3_hybrid_rule_sections": sorted(hybrid_secs),
        "gpo_2010_provisions": sum(1 for _ in GPO_TABLE.open()),
    }
    print(json.dumps(m))
    if dry:
        return

    rng = random.Random(SEED)

    def ex(sectno, span, before=300, after=250):
        t = texts[sectno]
        return t[max(0, span[0] - before):span[1] + after]

    AUDIT.mkdir(exist_ok=True)
    items = [(r, True) for r in rng.sample(marked, min(20, len(marked)))] + \
            [(r, False) for r in rng.sample([r for r in rows if not r["marker"]], 10)]
    rng.shuffle(items)
    pa = [{"item": f"a-{i:02d}", "cfr": f"37 CFR {r['sectno']} (2025)",
           "citation_as_read": texts[r["sectno"]][r["span"][0]:r["span"][1]], "excerpt": ex(r["sectno"], r["span"])}
          for i, (r, _) in enumerate(items, 1)]
    ka = [{"item": f"a-{i:02d}", "marked": mk, "sectno": r["sectno"], "span": r["span"], "marker": r["marker"]}
          for i, (r, mk) in enumerate(items, 1)]
    by = {c: [x for x in mentions if x["class"] == c] for c in ("conditioned", "date-only")}
    picks = [x for c in by for x in rng.sample(by[c], min(10, len(by[c])))]
    rng.shuffle(picks)
    pb = [{"item": f"b-{i:02d}", "cfr": f"37 CFR {x['sectno']} (2025)", "excerpt": ex(x["sectno"], x["span"], 400, 400)}
          for i, x in enumerate(picks, 1)]
    kb = [{"item": f"b-{i:02d}", "class": x["class"], "sectno": x["sectno"], "span": x["span"]}
          for i, x in enumerate(picks, 1)]
    for name, data in (("packet-a.jsonl", pa), ("key-a.jsonl", ka), ("packet-b.jsonl", pb), ("key-b.jsonl", kb)):
        (AUDIT / name).write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in data))

    entry = append({
        "observed_at": "2025-07-01",
        "observed_at_note": f"37 CFR as of Jul 1, 2025; 35 U.S.C. at release point {RP} and as of 2011-01-07 (GPO 2010)",
        "instrument": {
            "name": "scripts/measure_patents_v2.py",
            "method": f"usc_cites v{usc_cites.VERSION} + resolve against the current Code (v1, control); dated_cites "
                      f"v{dated_cites.VERSION} marks old-law citations (stated date before 2013-03-16 within 150 chars "
                      "after, or 'pre-AIA' within 20 before), resolved also against 35 U.S.C. as of 2010 (gpo_usc); "
                      "transition mentions classed by a lexical applicability test in their sentence",
            "known_limits": "dates further away or in another sentence unseen; 'conditioned' is lexical; the 2010 Code "
                            "stands for every pre-AIA date (a 1999 date is read against 2010 text); a marked citation "
                            "is a candidate until audited (Z2a)",
            "predictions": PREDICTIONS,
        },
        "population": {"edition": "2025", "title": "37", "release_point": RP, "source_sha256": sha(CFR),
                       "gpo_2010_sha256": sha(GPO)},
        "quantity": "patents_dated_citations_v2",
        "value": {**m, "output": str(OUT), "output_sha256": sha(OUT), "gpo_table_sha256": sha(GPO_TABLE),
                  "audit_packets_sha256": {n: sha(AUDIT / n) for n in ("packet-a.jsonl", "packet-b.jsonl")}},
    })
    print(entry["id"])
    print("ledger:", verify())


if __name__ == "__main__":
    main()
