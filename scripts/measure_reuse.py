"""Number reuse between 26 USC release points, and the CFR citations it touches.

Predictions R1-R5: predictions/2026-09-24-usc-reuse-claude.md.

A reuse candidate is an identifier present at both release points whose
heading changed (both non-empty, compared whitespace-normalized and
case-insensitive), or a revival: absent or repealed at the old release point,
in force at the new. Existence checks cannot see either: a citation through
such a provision resolves, to whatever the number means now.

Usage: uv run python scripts/measure_reuse.py
"""

import hashlib
import json
from collections import Counter
from pathlib import Path

from levadura_salvaje.ledger import append, verify
from levadura_salvaje.resolve import DASHES

OLD, NEW = "119-4", "119-110"
CITATIONS = Path("results/cfr-usc-citations-v2-2025.jsonl")


def load(rp: str) -> dict[str, dict]:
    """path (en dashes normalized, no leading 's') -> provision; in-force versions win."""
    out = {}
    for line in Path(f"results/usc26-provisions-{rp}.jsonl").read_text().splitlines():
        p = json.loads(line)
        key = p["path"].translate(DASHES)[1:]
        if key not in out or p["status"] is None:
            out[key] = p
    return out


def norm(h: str) -> str:
    return " ".join(h.lower().split()).rstrip(".")


def main() -> None:
    old, new = load(OLD), load(NEW)
    changed = {k for k in old.keys() & new.keys()
               if norm(old[k]["heading"]) and norm(new[k]["heading"])
               and norm(old[k]["heading"]) != norm(new[k]["heading"])
               and not old[k]["status"] and not new[k]["status"]}
    revived = {k for k in new if not new[k]["status"] and "..." not in k
               and (k not in old or old[k]["status"])}
    reuse = changed | revived
    # The registered R3 definition also counts brand-new provisions. The intended
    # meaning -- a number coming back -- is reported alongside: repealed at the old
    # release point, or absent there yet cited by the 2025 CFR (so it existed before).
    cited = {c["path"].translate(DASHES) for line in CITATIONS.read_text().splitlines()
             for c in json.loads(line)["citations"] if c.get("path")}
    cited_prefixes = {"/".join(p.split("/")[:i]) for p in cited for i in range(1, p.count("/") + 2)}
    returned = {k for k in revived if (k in old and old[k]["status"]) or k in cited_prefixes}
    narrow = changed | returned

    out = Path("results/usc26-reuse-119-4-119-110.jsonl")
    rows = [{"path": k, "kind": "heading-changed" if k in changed else "revived",
             "level": new[k]["level"],
             "old_heading": old[k]["heading"] if k in old else None,
             "old_status": old[k]["status"] if k in old else "absent",
             "new_heading": new[k]["heading"]} for k in sorted(reuse)]
    out.write_text("".join(json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n" for r in rows))

    hits, by_section, narrow_hits = [], Counter(), []
    for line in CITATIONS.read_text().splitlines():
        sec = json.loads(line)
        for c in sec["citations"]:
            if not c.get("path"):
                continue
            parts = c["path"].translate(DASHES).split("/")
            through = [p for p in ("/".join(parts[:i]) for i in range(1, len(parts) + 1)) if p in reuse]
            if through:
                hits.append((sec["sectno"], c["path"], through))
                by_section[parts[0]] += 1
            if [p for p in through if p in narrow]:
                narrow_hits.append((sec["sectno"], c["path"]))
    top3 = sum(n for _, n in by_section.most_common(3))

    rec = append({
        "observed_at": "2026-09-16",
        "observed_at_note": f"reuse between release points {OLD} (2025-03-15) and {NEW} (2026-09-16); "
                            "CFR citations are the 2025 edition's",
        "instrument": {
            "name": "scripts/measure_reuse.py", "version": "1",
            "method": "identifiers in force at both release points with a changed non-empty heading "
                      "(normalized, case-insensitive), plus revivals (absent or repealed, then in force); "
                      "CFR citation occurrences whose path or an ancestor is a candidate",
            "known_limits": "a heading change can be an edit, not a reuse; a reuse that keeps the "
                            "heading (or has none) is invisible here",
            "predictions": "predictions/2026-09-24-usc-reuse-claude.md",
        },
        "population": {
            "title": "26 USC", "release_points": [OLD, NEW],
            "results_file": str(out), "results_sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
            "citations_file": str(CITATIONS),
            "citations_sha256": hashlib.sha256(CITATIONS.read_bytes()).hexdigest(),
        },
        "quantity": "usc26_number_reuse",
        "value": {
            "R1_heading_changed": len(changed),
            "R2_heading_changed_by_level": dict(Counter(new[k]["level"] for k in changed)),
            "R3_revived": len(revived),
            "R3_revived_by_level": dict(Counter(new[k]["level"] for k in revived)),
            "R4_cfr_occurrences_through_candidates": len(hits),
            "R4_cfr_sections_affected": len({s for s, _, _ in hits}),
            "R5_top3_sections": by_section.most_common(3),
            "R5_top3_share": round(top3 / len(hits), 3) if hits else None,
            "cited_sections": dict(by_section.most_common()),
            "variant_returned_numbers": sorted(returned),
            "variant_R3_returned": len(returned),
            "variant_R4_occurrences_through_changed_or_returned": len(narrow_hits),
            "variant_R4_cfr_sections_affected": len({s for s, _ in narrow_hits}),
        },
    })
    print(rec["id"], json.dumps(rec["value"], indent=1)[:2500])
    print("ledger verified:", verify())


if __name__ == "__main__":
    main()
