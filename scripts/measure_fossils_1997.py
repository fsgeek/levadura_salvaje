"""The 1997 CFR against the statute in force on its date (predictions H1-H5).

1. Validate the GPO reader (levadura_salvaje.gpo_usc): parse USCODE-2023
   (current through 2024-01-03) and compare its provision paths with OLRC
   USLM at 119-4 (2025-03-15). Little tax law passed in between, so the
   overlap bounds the reader's recall and precision.
2. Parse USCODE-1996 (current through 1997-01-06) into
   results/usc26-provisions-gpo-1996.jsonl.
3. Extract Code citations from the 1997 CFR (extractor v2) and resolve them
   against it with resolver v2, writing results/cfr-usc-citations-v2-1997.jsonl.
4. Compare with 2025 on the 1,343 sections byte-identical in both editions.

Usage: uv run python scripts/measure_fossils_1997.py
"""

import hashlib
import json
from collections import Counter
from pathlib import Path

from levadura_salvaje import citations, resolve
from levadura_salvaje.gpo_usc import provisions as gpo_provisions
from levadura_salvaje.ledger import append, verify
from levadura_salvaje.resolve import DASHES, Statute
from levadura_salvaje.sections import sections

BROKEN = {"repealed", "absent-section", "absent-subdivision"}
GPO = Path("data/uscode-gpo")
TAG = "corpus/uscode-gpo-1996-1997"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def write(rows: list[dict], out: Path) -> None:
    out.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in rows))


def validate() -> dict:
    g = {p["path"].translate(DASHES) for p in gpo_provisions(GPO / "USCODE-2023-title26.htm")}
    u = {json.loads(l)["path"].translate(DASHES)
         for l in Path("results/usc26-provisions-119-4.jsonl").read_text().splitlines()}
    u = {p for p in u if " " not in p}  # two malformed USLM identifiers
    both = g & u
    return {"gpo_2023_paths": len(g), "uslm_119_4_paths": len(u), "both": len(both),
            "recall_vs_uslm": round(len(both) / len(u), 4), "precision_vs_uslm": round(len(both) / len(g), 4),
            "uslm_only_by_depth": dict(Counter(p.count("/") for p in u - g)),
            "gpo_only_by_depth": dict(Counter(p.count("/") for p in g - u)),
            "gpo_2023_sha256": sha(GPO / "USCODE-2023-title26.htm")}


def main() -> None:
    check = validate()
    src = GPO / "USCODE-1996-title26.htm"
    stat_rows = list(gpo_provisions(src))
    stat_out = Path("results/usc26-provisions-gpo-1996.jsonl")
    write(stat_rows, stat_out)
    statute = Statute.load("gpo-1996", stat_out)
    through = Counter(r["current_through"] for r in stat_rows).most_common(1)[0][0]

    old_sha = {}
    out = Path(f"results/cfr-usc-citations-v{citations.VERSION}-1997.jsonl")
    rows = []
    for s in sections(Path("data/cfr/CFR-1997-title-26.zip")):
        recs = citations.extract(s["text"], part=s["sectno"].split(".")[0], reg_id=s["sectno"])
        cites = []
        for r in recs:
            c = {k: r[k] for k in ("path", "head", "flags", "range", "span")}
            if r["path"] is not None:
                c["outcome"] = statute.resolve(r["path"])
                c["section_outcome"] = statute.resolve(r["section"])["outcome"]
            cites.append(c)
        rows.append({k: s[k] for k in ("volume_file", "ordinal", "sectno", "sha256")} | {
            "citations": cites,
            "broken": sum(c["outcome"]["outcome"] in BROKEN for c in cites if "outcome" in c)})
        old_sha[s["sha256"]] = rows[-1]
    write(rows, out)

    occ = [c for r in rows for c in r["citations"] if "outcome" in c]
    outcomes = Counter(c["outcome"]["outcome"] for c in occ)
    sec_status = {c["path"].split("/")[0]: c["section_outcome"] for c in occ}

    new = {json.loads(l)["sha256"]: json.loads(l)
           for l in Path("results/cfr-usc-citations-v2-2025.jsonl").read_text().splitlines()}
    identical = [h for h in new if h in old_sha]
    fossil_97 = sum(old_sha[h]["broken"] > 0 for h in identical)
    fossil_25 = sum(new[h]["broken"]["119-4"] > 0 for h in identical)
    # H4: citation occurrences in identical sections broken in 2025 -- were they broken in 1997?
    b25 = b25_and_97 = 0
    for h in identical:
        c97 = {tuple(c["span"]): c for c in old_sha[h]["citations"] if "outcome" in c}
        for c in new[h]["citations"]:
            if "outcome" in c and c["outcome"]["119-4"]["outcome"] in BROKEN:
                b25 += 1
                o = c97.get(tuple(c["span"]))
                b25_and_97 += bool(o and o["outcome"]["outcome"] in BROKEN)

    rec = append({
        "observed_at": "1997-04-01",
        "observed_at_note": f"the 1997 CFR's dominant volume date, read against 26 USC as published by GPO, "
                            f"current through {through}",
        "instrument": {
            "name": "scripts/measure_fossils_1997.py", "version": "1",
            "extractor": f"levadura_salvaje.citations v{citations.VERSION}",
            "resolver": f"levadura_salvaje.resolve v{resolve.VERSION}",
            "statute_reader": "levadura_salvaje.gpo_usc v1 (subdivisions inferred from HTML classes)",
            "statute_reader_validation": check,
            "predictions": "predictions/2026-09-24-fossils-1997-claude.md",
        },
        "population": {
            "edition": "1997", "statute": "USCODE-1996-title26 (GPO)", "archived_on_tag": TAG,
            "statute_sha256": sha(src), "statute_results_file": str(stat_out),
            "statute_results_sha256": sha(stat_out),
            "results_file": str(out), "results_sha256": sha(out),
        },
        "quantity": "cfr_usc_citation_resolution",
        "value": {
            "sections": len(rows), "citation_occurrences": len(occ), "outcomes": dict(outcomes),
            "broken_occurrences": sum(outcomes[o] for o in BROKEN),
            "P1_sections_with_code_citation": [sum(any("outcome" in c for c in r["citations"]) for r in rows), len(rows)],
            "H1_distinct_cited_sections": len(sec_status),
            "H1_distinct_sections_by_outcome": dict(Counter(sec_status.values())),
            "H2_fossil_candidate_sections": [sum(r["broken"] > 0 for r in rows), len(rows)],
            "H3_identical_sections": len(identical),
            "H3_fossil_candidates_identical_1997": fossil_97,
            "H3_fossil_candidates_identical_2025": fossil_25,
            "H4_broken_2025_also_broken_1997": [b25_and_97, b25],
            "statute_sections_by_status": dict(Counter(r["status"] or "in_force" for r in stat_rows if r["level"] == "section")),
            "statute_provisions": len(stat_rows),
        },
    })
    print(rec["id"], json.dumps(rec["value"], indent=1))
    print(json.dumps(check, indent=1))
    print("ledger verified:", verify())


if __name__ == "__main__":
    main()
