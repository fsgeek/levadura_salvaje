"""PTAB FITF: the pre-AIA share of challenged patents by grant year (predictions/2026-10-28-ptab-fitf-curve-tony-and-claude.md,
stamped at 7a96020), and the packets for context test 2 (predictions/2026-10-28-ptab-context-2-claude.md, stamped at
c5d4d1e). Ground truth is the USPTO's firstInventorToFileIndicator (data/ptab/fitf.jsonl). One ledger entry for the
curve, none with --dry-run.

Usage: uv run python scripts/measure_ptab_fitf.py [--dry-run]
"""

import hashlib
import json
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from levadura_salvaje.ledger import append, verify

DIR = Path("data/ptab")
AUDIT = Path("results/ptab-audit-context-2")
CITE = re.compile(r"35\s+U\.\s?S\.\s?C\.")
GROUND = re.compile(r"§+\s*10[23]\b")
RULE = ("This patent's application has the effective filing date given. If that date is before March 16, 2013, the "
        "pre-AIA versions of 35 U.S.C. 102 and 103 govern; if on or after, the AIA versions do.")


def main():
    dry = "--dry-run" in sys.argv
    fitf = {x["app"]: x for x in map(json.loads, (DIR / "fitf.jsonl").open())}
    meta = [json.loads(x) for x in (DIR / "meta.jsonl").open()]
    fw = [r for r in meta if (r["documentData"].get("documentTypeDescriptionText") or "").startswith("Final Written Decision")]
    seen, curve = set(), defaultdict(Counter)
    for r in fw:
        po = r["patentOwnerData"]
        app, g = po.get("applicationNumberText"), po.get("grantDate") or ""
        if g < "2013-03-16" or app in seen:
            continue
        seen.add(app)
        year = "2019+" if g[:4] >= "2019" else g[:4]
        curve[year][(fitf.get(app) or {}).get("fitf") or "missing"] += 1
    shares = {y: {"n": sum(c.values()), "pre_aia_share": round(c["N"] / (c["N"] + c["Y"]), 4) if c["N"] + c["Y"] else None,
                  "missing": c["missing"]} for y, c in sorted(curve.items())}
    print(json.dumps(shares))

    rows = {x["doc"]: x for x in map(json.loads, open("results/ptab-applicability.jsonl"))}
    pop = []
    for r in fw:
        d = rows.get(r["documentData"]["documentIdentifier"])
        app = r["patentOwnerData"].get("applicationNumberText")
        if not d or d["no_text"] or d["marked"] or d["old_subdivision"] or (r["patentOwnerData"].get("grantDate") or "") < "2013-03-16":
            continue
        t = re.sub(r"\s+", " ", (DIR / "txt" / f"{d['doc']}.txt").read_text())
        if len(GROUND.findall(t[3000:])) == 0 or (fitf.get(app) or {}).get("fitf") not in ("N", "Y"):
            continue
        pop.append((d, fitf[app], t))
    print("context-2 population:", len(pop), dict(Counter(f["fitf"] for _, f, _ in pop)))
    if dry:
        return

    rng = random.Random(20261028)
    pick = rng.sample(pop, min(80, len(pop)))
    AUDIT.mkdir(exist_ok=True)
    for arm, seed in (("c0", 1), ("c1", 2)):
        items = pick[:]
        random.Random(20261028 + seed).shuffle(items)
        packet, key = [], []
        for i, (d, f, t) in enumerate(items, 1):
            ps = [t[max(0, a - 400):a + 400] for a in [m.start() for m in CITE.finditer(t)][:8]]
            it = {"item": f"{arm}-{i:02d}", "passages": ps}
            if arm == "c1":
                it = {"item": it["item"], "effective_filing_date": f["effective_filing_date"], "rule": RULE, "passages": ps}
            packet.append(it)
            key.append({"item": f"{arm}-{i:02d}", "doc": d["doc"], "fitf": f["fitf"], "grant": d["grant"],
                        "effective_filing_date": f["effective_filing_date"]})
        for b in range(3):
            (AUDIT / f"{arm}-batch-{b}.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in packet[b::3]))
        (AUDIT / f"{arm}-key.jsonl").write_text("".join(json.dumps(x) + "\n" for x in key))

    entry = append({
        "observed_at": "2026-10-28",
        "observed_at_note": "USPTO application records (first-inventor-to-file indicator) for patents challenged in PTAB final "
                            "written decisions 2021-2026, granted on or after 2013-03-16, as fetched 2026-10-28",
        "instrument": {"name": "scripts/measure_ptab_fitf.py",
                       "method": "per distinct application: firstInventorToFileIndicator from api.uspto.gov applications "
                                 "meta-data; share N by grant year",
                       "known_limits": "challenged patents, not all grants; an application without the indicator is "
                                       "counted as missing",
                       "predictions": "predictions/2026-10-28-ptab-fitf-curve-tony-and-claude.md"},
        "population": {"fitf_sha256": hashlib.sha256((DIR / "fitf.jsonl").read_bytes()).hexdigest()},
        "quantity": "ptab_fitf_curve_v1",
        "value": {"by_grant_year": shares, "context2_population": len(pop), "context2_sampled": len(pick)},
    })
    print(entry["id"])
    print("ledger:", verify())


if __name__ == "__main__":
    main()
