"""Check every Code citation in the 2025 CFR against 26 USC (predictions P1-P9).

Deterministic: the extractor (levadura_salvaje.citations, spec in
docs/citation-extractor-spec.md) finds the citations, and the resolver
(levadura_salvaje.resolve) checks each against a release point. Outcomes and
definitions are the ones pre-registered in
predictions/2026-09-24-cfr-usc-fossils-claude.md.

Section ranges ("sections 861 through 865") are checked at their endpoints
only. Flags (historical, attributive, ...) are recorded, never used to change
an outcome; the scorecard may count with and without them.

Usage: uv run python scripts/measure_fossils.py
"""

import hashlib
import json
from collections import Counter
from pathlib import Path

from levadura_salvaje import citations
from levadura_salvaje.ledger import LEDGER, append, verify
from levadura_salvaje import resolve
from levadura_salvaje.resolve import Statute
from levadura_salvaje.sections import sections

EDITION = "2025"
RELEASE_POINTS = ("119-4", "119-110")
BROKEN = {"repealed", "absent-section", "absent-subdivision"}
STATUS_ONLY = {"renumbered", "omitted", "reserved"}


def ledger_id(quantity: str, **match) -> str:
    for rec in map(json.loads, LEDGER.read_text().splitlines()):
        if rec["quantity"] == quantity and all(rec["population"].get(k) == v for k, v in match.items()):
            return rec["id"]
    raise LookupError(quantity, match)


def rate(rows: list[dict], rp: str) -> tuple[int, int]:
    return sum(r["broken"][rp] > 0 for r in rows), len(rows)


def main() -> None:
    statutes = {rp: Statute.load(rp) for rp in RELEASE_POINTS}
    old = {s["sha256"] for s in sections(Path("data/cfr/CFR-1997-title-26.zip"))}
    amt_fossils = {(r["volume_file"], r["ordinal"])
                   for r in map(json.loads, Path("results/amt-p4-regimes-v1-2025.jsonl").read_text().splitlines())
                   if r["human_label"] == "operative" and r["current"] is False}

    out = Path(f"results/cfr-usc-citations-v{citations.VERSION}-{EDITION}.jsonl")
    rows = []
    with out.open("w") as f:
        for s in sections(Path(f"data/cfr/CFR-{EDITION}-title-26.zip")):
            part = s["sectno"].split(".")[0]
            recs = citations.extract(s["text"], part=part, reg_id=s["sectno"])
            cites = []
            for r in recs:
                c = {k: r[k] for k in ("path", "head", "flags", "range", "span")}
                if r.get("kind"):
                    c["kind"] = r["kind"]
                if r["path"] is not None:
                    c["outcome"] = {rp: st.resolve(r["path"]) for rp, st in statutes.items()}
                    c["section_outcome"] = {rp: st.resolve(r["section"])["outcome"] for rp, st in statutes.items()}
                cites.append(c)
            row = {k: s[k] for k in ("volume_file", "ordinal", "sectno", "sha256")} | {
                "in_1997": s["sha256"] in old,
                "amt_fossil": (s["volume_file"], s["ordinal"]) in amt_fossils,
                "citations": cites,
                "broken": {rp: sum(c["outcome"][rp]["outcome"] in BROKEN for c in cites if "outcome" in c)
                           for rp in RELEASE_POINTS},
            }
            f.write(json.dumps(row, sort_keys=True) + "\n")
            rows.append(row)
    results_sha = hashlib.sha256(out.read_bytes()).hexdigest()

    for rp in RELEASE_POINTS:
        occ = [c for r in rows for c in r["citations"]]
        resolved = [c for c in occ if "outcome" in c]
        outcomes = Counter(c["outcome"][rp]["outcome"] for c in resolved)
        sec_status = {}
        for c in resolved:
            sec_status[c["path"].split("/")[0]] = c["section_outcome"][rp]
        sec_counts = Counter(sec_status.values())
        with_cite = [r for r in rows if any("outcome" in c for c in r["citations"])]
        identical, changed = [r for r in rows if r["in_1997"]], [r for r in rows if not r["in_1997"]]
        fi, ni = rate(identical, rp)
        fc, nc = rate(changed, rp)
        amt = [r for r in rows if r["amt_fossil"]]
        flagged = Counter(fl for c in resolved if c["outcome"][rp]["outcome"] in BROKEN for fl in c["flags"])
        value = {
            "sections": len(rows),
            "citation_occurrences": len(occ),
            "unresolvable_occurrences": len(occ) - len(resolved),
            "outcomes": dict(outcomes),
            "broken_occurrences": sum(outcomes[o] for o in BROKEN),
            "broken_occurrences_flagged": dict(flagged),
            "P1_sections_with_code_citation": [len(with_cite), len(rows)],
            "P2_distinct_cited_sections": len(sec_status),
            "P2_distinct_sections_by_outcome": dict(sec_counts),
            "P3_fossil_candidate_sections": [sum(r["broken"][rp] > 0 for r in rows), len(rows)],
            "P4_absent_subdivision_vs_section_level":
                [outcomes["absent-subdivision"], outcomes["repealed"] + outcomes["absent-section"]],
            "P5_fossil_rate_identical_to_1997": [fi, ni],
            "P5_fossil_rate_not_identical": [fc, nc],
            "P6_amt_fossils_that_are_candidates": [sum(r["broken"][rp] > 0 for r in amt), len(amt)],
            "P9_unresolvable_share_of_occurrences": [len(occ) - len(resolved), len(occ)],
        }
        rec = append({
            "observed_at": "2025-04-01",
            "observed_at_note": f"the 2025 CFR's dominant volume date, read against 26 USC as of release "
                                f"point {rp}; the pairing, not either text alone, is what is observed",
            "instrument": {
                "name": "scripts/measure_fossils.py", "version": citations.VERSION,
                "resolver": f"levadura_salvaje.resolve v{getattr(resolve, 'VERSION', '1')}",
                "extractor": f"levadura_salvaje.citations v{citations.VERSION} "
                             "(docs/citation-extractor-spec.md)",
                "method": "extract Code citations per section; resolve each path against the USLM "
                          "provision identifiers of the release point; section ranges by endpoints only",
                "predictions": "predictions/2026-09-24-cfr-usc-fossils-claude.md",
            },
            "population": {
                "edition": EDITION, "release_point": rp,
                "results_file": str(out), "results_sha256": results_sha,
            },
            "quantity": "cfr_usc_citation_resolution",
            "value": value,
            "derived_from": [ledger_id("usc26_structure", release_point=rp)],
        })
        print(rec["id"], rp, json.dumps(value, indent=1))
    print("ledger verified:", verify())


if __name__ == "__main__":
    main()
