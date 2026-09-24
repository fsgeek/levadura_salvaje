"""Fossil turnover between the 1997 and 2025 CFR (predictions T1-T5).

Sections are paired by section number, using only numbers that occur exactly
once in each edition. Candidates: 1997 from obs-0139 (extractor v2 against
GPO USCODE-1996), 2025 from obs-0129 (v2 against 119-4).

Usage: uv run python scripts/measure_fossil_turnover.py
"""

import hashlib
import json
from collections import Counter
from pathlib import Path

from levadura_salvaje.ledger import LEDGER, append, verify


def load(path: str, key) -> dict:
    rows = [json.loads(l) for l in Path(path).read_text().splitlines()]
    counts = Counter(r["sectno"] for r in rows)
    return {r["sectno"]: {"fossil": key(r) > 0, "sha256": r["sha256"]} for r in rows if counts[r["sectno"]] == 1}, len(rows)


def main() -> None:
    old, n_old = load("results/cfr-usc-citations-v2-1997.jsonl", lambda r: r["broken"])
    new, n_new = load("results/cfr-usc-citations-v2-2025.jsonl", lambda r: r["broken"]["119-4"])

    fossils_97 = [s for s, r in old.items() if r["fossil"]]
    gone = [s for s in fossils_97 if s not in new]
    present = [s for s in fossils_97 if s in new]
    still = [s for s in present if new[s]["fossil"]]
    cured = [s for s in present if not new[s]["fossil"]]

    fossils_25 = [s for s, r in new.items() if r["fossil"]]
    inherited = [s for s in fossils_25 if s in old and old[s]["fossil"]]
    turned = [s for s in fossils_25 if s in old and not old[s]["fossil"]]
    born_new = [s for s in fossils_25 if s not in old]
    changed = lambda ss: sum(old[s]["sha256"] != new[s]["sha256"] for s in ss)

    rows = ([{"sectno": s, "fate_1997_fossil": "gone"} for s in gone]
            + [{"sectno": s, "fate_1997_fossil": "still", "text_changed": old[s]["sha256"] != new[s]["sha256"]} for s in still]
            + [{"sectno": s, "fate_1997_fossil": "cured", "text_changed": old[s]["sha256"] != new[s]["sha256"]} for s in cured]
            + [{"sectno": s, "origin_2025_fossil": "turned", "text_changed": old[s]["sha256"] != new[s]["sha256"]} for s in turned]
            + [{"sectno": s, "origin_2025_fossil": "new"} for s in born_new])
    out = Path("results/cfr-fossil-turnover-1997-2025.jsonl")
    out.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in rows))
    src = [rec["id"] for rec in map(json.loads, LEDGER.read_text().splitlines())
           if rec["quantity"] == "cfr_usc_citation_resolution"
           and (rec["population"].get("edition") == "1997"
                or (rec["instrument"]["version"] == "2" and rec["population"].get("release_point") == "119-4"))]

    rec = append({
        "observed_at": "2025-04-01",
        "observed_at_note": "turnover between the 1997-04-01 and 2025-04-01 editions",
        "instrument": {
            "name": "scripts/measure_fossil_turnover.py", "version": "1",
            "method": "pair sections by section number, numbers unique in both editions only; candidate "
                      "status from each edition's contemporaneous resolution",
            "known_limits": "section numbers are reused (old §53, §56A), so a pairing can join two different "
                            "regulations; repeated numbers (601 in 1997) are excluded",
            "predictions": "predictions/2026-09-24-fossil-turnover-claude.md",
        },
        "population": {"editions": ["1997", "2025"], "results_file": str(out),
                       "results_sha256": hashlib.sha256(out.read_bytes()).hexdigest()},
        "quantity": "cfr_fossil_turnover",
        "value": {
            "unique_sections": {"1997": len(old), "2025": len(new), "all_1997": n_old, "all_2025": n_new},
            "fossils_1997": len(fossils_97), "fossils_2025": len(fossils_25),
            "T1_1997_fossils_gone": [len(gone), len(fossils_97)],
            "T2_present_still_fossil": [len(still), len(present)],
            "still_fossil_text_changed": changed(still), "cured_text_changed": changed(cured),
            "T3_2025_inherited": [len(inherited), len(fossils_25)],
            "T4_2025_new": [len(born_new), len(fossils_25)],
            "T5_2025_turned": [len(turned), len(fossils_25)],
            "turned_text_changed": changed(turned),
        },
        "derived_from": src,
    })
    print(rec["id"], json.dumps(rec["value"], indent=1))
    print("ledger verified:", verify())


if __name__ == "__main__":
    main()
