"""Section numbers reused between the 1997 and 2025 statutes (predictions U1-U3).

For each section in force in both GPO USCODE-1996 (current through
1997-01-06) and USLM 119-4 (2025-03-15), compare headings as word sets
(lowercase, punctuation removed, stopwords dropped). Word-set Jaccard below
0.2 marks a reuse. Then count 2025 CFR sections citing a reused section.

Usage: uv run python scripts/measure_reuse_28y.py
"""

import hashlib
import json
import re
from pathlib import Path

from levadura_salvaje.ledger import LEDGER, append, verify
from levadura_salvaje.resolve import DASHES

STOP = set("a an and the of for in on to by or with from under certain other than as at".split())
THRESHOLD = 0.2


def headings(path: str) -> dict:
    out = {}
    for line in Path(path).read_text().splitlines():
        p = json.loads(line)
        if p["level"] == "section" and not p["status"] and "..." not in p["path"]:
            out[p["path"].translate(DASHES)[1:]] = p["heading"]
    return out


def words(h: str) -> set:
    return {w for w in re.findall(r"[a-z0-9]+", h.lower()) if w not in STOP}


def main() -> None:
    old = headings("results/usc26-provisions-gpo-1996.jsonl")
    new = headings("results/usc26-provisions-119-4.jsonl")
    pairs = []
    for sec in sorted(old.keys() & new.keys()):
        a, b = words(old[sec]), words(new[sec])
        j = len(a & b) / len(a | b) if a | b else 1.0
        pairs.append({"section": sec, "jaccard": round(j, 3), "heading_1997": old[sec], "heading_2025": new[sec],
                      "reused": j < THRESHOLD})
    reused = {p["section"] for p in pairs if p["reused"]}
    out = Path("results/usc26-reuse-1997-2025.jsonl")
    out.write_text("".join(json.dumps(p, sort_keys=True, ensure_ascii=False) + "\n" for p in pairs if p["jaccard"] < 0.5))

    old_sha = {json.loads(l)["sha256"] for l in Path("results/cfr-usc-citations-v2-1997.jsonl").read_text().splitlines()}
    hits, healthy, healthy_citing = [], 0, 0
    for line in Path("results/cfr-usc-citations-v2-2025.jsonl").read_text().splitlines():
        r = json.loads(line)
        cited = {c["path"].translate(DASHES).split("/")[0] for c in r["citations"] if c.get("path")}
        through = sorted(cited & reused)
        if r["broken"]["119-4"] == 0:
            healthy += 1
            healthy_citing += bool(through)
        if through:
            hits.append({"sectno": r["sectno"], "reused_cited": through, "identical_to_1997": r["sha256"] in old_sha,
                         "fossil_candidate": r["broken"]["119-4"] > 0})
    cites = Path("results/cfr-cites-reused-1997-2025.jsonl")
    cites.write_text("".join(json.dumps(h, sort_keys=True) + "\n" for h in hits))
    src = [rec["id"] for rec in map(json.loads, LEDGER.read_text().splitlines())
           if rec["quantity"] in ("usc26_structure",) and rec["population"].get("release_point") == "119-4"
           or (rec["quantity"] == "cfr_usc_citation_resolution" and rec["population"].get("edition") == "1997")]

    rec = append({
        "observed_at": "2025-03-15",
        "observed_at_note": "headings compared between 26 USC current through 1997-01-06 (GPO) and 2025-03-15 (USLM 119-4)",
        "instrument": {
            "name": "scripts/measure_reuse_28y.py", "version": "1",
            "method": f"section headings as word sets (lowercase, punctuation and stopwords removed); reuse = "
                      f"Jaccard < {THRESHOLD}; sections in force at both; CFR citations by section",
            "known_limits": "a heavy rewrite of a heading can read as reuse; a reuse that keeps heading words is "
                            "missed; reuses before 1997 (e.g. section 39) are out of scope",
            "predictions": "predictions/2026-09-24-reuse-28y-claude.md",
        },
        "population": {"statutes": ["USCODE-1996-title26 (GPO)", "USLM 119-4"],
                       "results_file": str(out), "results_sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
                       "citations_file": str(cites), "citations_sha256": hashlib.sha256(cites.read_bytes()).hexdigest()},
        "quantity": "usc26_section_reuse_28y",
        "value": {
            "sections_in_force_both": len(pairs),
            "U1_reused": len(reused),
            "reused_sections": sorted(reused, key=lambda s: (int(re.match(r"\d+", s).group()), s)),
            "U2_identical_1997_sections_citing_reused": sum(h["identical_to_1997"] for h in hits),
            "U3_healthy_sections_citing_reused": [healthy_citing, healthy],
            "cfr_sections_citing_reused": len(hits),
        },
        "derived_from": src,
    })
    print(rec["id"], json.dumps(rec["value"], indent=1)[:2500])
    print("ledger verified:", verify())


if __name__ == "__main__":
    main()
