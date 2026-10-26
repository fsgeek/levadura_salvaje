"""The patents transfer study, v1: levadura's instruments on 37 CFR (2010 and 2025) against 35 U.S.C.

Deterministic; predictions in predictions/2026-10-26-patents-transfer-claude.md (stamped at 64a6f4b
before any patent data was parsed). I1 (sections), I2 (usc_cites + resolve) and I3 (act_pairs) run
unchanged; I5 (para_forms) is the one new instrument. Builds audit packets Z1a (non-resolving title-35
citations plus resolving controls) and Z1b (2025 ordinal-form citations to 112). One ledger entry, none
with --dry-run.

Usage: uv run python scripts/measure_patents_transfer.py [--dry-run]
"""

import hashlib
import json
import random
import sys
from collections import Counter
from pathlib import Path

from levadura_salvaje import act_pairs, para_forms, usc_cites
from levadura_salvaje.ledger import append, verify
from levadura_salvaje.resolve import Statute
from levadura_salvaje.sections import distinct_sections

RP, SEED = "119-120", 20261026
EDITIONS = ("2010", "2025")
OUT = Path("results/patents-transfer-cites.jsonl")
AUDIT = Path("results/patents-transfer-audit-z1")
PREDICTIONS = "predictions/2026-10-26-patents-transfer-claude.md"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    dry = "--dry-run" in sys.argv
    statutes = {"35": Statute.load(RP, title="35")}
    rows, texts, m = [], {}, {}
    for e in EDITIONS:
        zp = Path(f"data/patents/CFR-{e}-title-37.zip")
        n_cites, n_pairs, forms = 0, 0, Counter()
        for s in distinct_sections(zp):
            text = usc_cites.normalize(s["text"])
            texts[(e, s["sectno"])] = text
            cites = usc_cites.extract(text, normalized=True)
            n_cites += len(cites)
            n_pairs += len(act_pairs.pairs(text, normalized=True))
            for c in cites:
                if c["title"] == "35":
                    r = usc_cites.resolve(c, statutes)
                    rows.append({"edition": e, "sectno": s["sectno"], "path": c["path"], "span": c["span"],
                                 "flags": c["flags"], "outcome": r["outcome"]})
            for x in para_forms.forms(text, title="35", section="112", normalized=True):
                forms[x["form"]] += 1
                if x["form"] == "ordinal":
                    rows.append({"edition": e, "sectno": s["sectno"], "path": "112", "span": x["span"],
                                 "flags": [], "outcome": "ordinal-112"})
        t35 = [r for r in rows if r["edition"] == e and r["outcome"] != "ordinal-112"]
        named = forms["letter"] + forms["ordinal"]
        m[e] = {"explicit_usc_cites": n_cites, "act_pairs": n_pairs, "title35_cites": len(t35),
                "title35_not_resolving": sum(r["outcome"] != "resolves" for r in t35),
                "outcomes": dict(Counter(r["outcome"] for r in t35)), "forms_112": dict(forms),
                "letter_share_112": round(forms["letter"] / named, 4) if named else None,
                "ordinal_share_112": round(forms["ordinal"] / named, 4) if named else None}
        m[e]["not_resolving_share"] = round(m[e]["title35_not_resolving"] / len(t35), 4) if t35 else None
    OUT.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in rows))
    a, b = m["2010"]["not_resolving_share"], m["2025"]["not_resolving_share"]
    metrics = {**m, "P1": m["2025"]["explicit_usc_cites"], "P2": b, "P3": round(a / b, 3) if a and b else None,
               "P4": m["2010"]["ordinal_share_112"], "P5": m["2025"]["letter_share_112"],
               "P6": m["2025"]["forms_112"].get("ordinal", 0), "I3_pairs_2025": m["2025"]["act_pairs"]}
    print(json.dumps(metrics))
    if dry:
        return

    rng = random.Random(SEED)

    def excerpt(r):
        t = texts[(r["edition"], r["sectno"])]
        x, y = r["span"]
        return t[max(0, x - 300):y + 200], t[x:y]

    AUDIT.mkdir(exist_ok=True)
    t35 = [r for r in rows if r["edition"] == "2025" and r["outcome"] not in ("ordinal-112",)]
    bad = rng.sample([r for r in t35 if r["outcome"] != "resolves"],
                     min(30, sum(r["outcome"] != "resolves" for r in t35)))
    good = rng.sample([r for r in t35 if r["outcome"] == "resolves"], 10)
    items = [(r, True) for r in bad] + [(r, False) for r in good]
    rng.shuffle(items)
    pa, ka = [], []
    for i, (r, flagged) in enumerate(items, 1):
        ex, cite = excerpt(r)
        pa.append({"item": f"a-{i:02d}", "cfr": f"37 CFR {r['sectno']} (2025)", "citation_as_read": cite,
                   "excerpt": ex})
        ka.append({"item": f"a-{i:02d}", "flagged": flagged, "sectno": r["sectno"], "span": r["span"],
                   "outcome": r["outcome"]})
    ords = [r for r in rows if r["edition"] == "2025" and r["outcome"] == "ordinal-112"]
    ords = rng.sample(ords, min(30, len(ords)))
    pb, kb = [], []
    for i, r in enumerate(ords, 1):
        ex, cite = excerpt(r)
        pb.append({"item": f"b-{i:02d}", "cfr": f"37 CFR {r['sectno']} (2025)", "citation_as_read": cite,
                   "excerpt": ex})
        kb.append({"item": f"b-{i:02d}", "sectno": r["sectno"], "span": r["span"]})
    for name, data in (("packet-a.jsonl", pa), ("key-a.jsonl", ka), ("packet-b.jsonl", pb), ("key-b.jsonl", kb)):
        (AUDIT / name).write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in data))

    entry = append({
        "observed_at": "2025-07-01",
        "observed_at_note": "37 CFR as of Jul 1 of 2010 and 2025 (GovInfo annual edition), read against USC release "
                            f"point {RP}",
        "instrument": {
            "name": "scripts/measure_patents_transfer.py",
            "method": f"sections; usc_cites v{usc_cites.VERSION} + resolve against 35 U.S.C.; act_pairs "
                      f"v{act_pairs.VERSION} (count only); para_forms v{para_forms.VERSION} (citations to 35 U.S.C. "
                      "112 as letter, ordinal or bare)",
            "known_limits": "explicit 'N U.S.C.' citations only; 2010 resolved against the current Code (pre-AIA "
                            "sections read as absent); an ordinal far from its citation is not seen; a non-resolving "
                            "citation is a candidate until audited (Z1a); an ordinal form may be deliberate (Z1b)",
            "predictions": PREDICTIONS,
        },
        "population": {"editions": list(EDITIONS), "title": "37", "release_point": RP,
                       "source_sha256": {e: sha(Path(f"data/patents/CFR-{e}-title-37.zip")) for e in EDITIONS}},
        "quantity": "patents_transfer_v1",
        "value": {**metrics, "output": str(OUT), "output_sha256": sha(OUT),
                  "audit_packets_sha256": {n: sha(AUDIT / n) for n in ("packet-a.jsonl", "packet-b.jsonl")}},
    })
    print(entry["id"])
    print("ledger:", verify())


if __name__ == "__main__":
    main()
