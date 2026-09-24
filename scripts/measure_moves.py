"""Track re-lettered 26 USC provisions to their new positions (predictions L1-L3).

For each identifier whose heading changed between 119-4 and 119-110
(results/usc26-reuse-119-4-119-110.jsonl, kind heading-changed), look for its
old heading at a different identifier under the same parent at 119-110:
exactly one match is a move, several are ambiguous, none is replaced. Then,
for every 2025 CFR citation whose path passes through a moved provision,
record where the cited rule lives now.

Usage: uv run python scripts/measure_moves.py
"""

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

from levadura_salvaje.ledger import append, verify
from levadura_salvaje.resolve import DASHES

REUSE = Path("results/usc26-reuse-119-4-119-110.jsonl")
CITATIONS = Path("results/cfr-usc-citations-v2-2025.jsonl")


def norm(h: str | None) -> str:
    return " ".join((h or "").lower().split()).rstrip(".")


def main() -> None:
    new = {}
    for line in Path("results/usc26-provisions-119-110.jsonl").read_text().splitlines():
        p = json.loads(line)
        key = p["path"].translate(DASHES)[1:]
        if key not in new or p["status"] is None:
            new[key] = p
    children = defaultdict(list)
    for k in new:
        if "/" in k:
            children[k.rsplit("/", 1)[0]].append(k)

    changed = [r for r in map(json.loads, REUSE.read_text().splitlines()) if r["kind"] == "heading-changed"]
    moves, rows = {}, []
    for r in changed:
        path = r["path"]
        parent = path.rsplit("/", 1)[0] if "/" in path else None
        siblings = children.get(parent, []) if parent else []
        hits = [s for s in siblings if s != path and norm(new[s]["heading"]) == norm(r["old_heading"])]
        kind = "move" if len(hits) == 1 else "ambiguous" if hits else "replaced"
        if kind == "move":
            moves[path] = hits[0]
        rows.append({"path": path, "kind": kind, "to": hits, "old_heading": r["old_heading"],
                     "new_heading": r["new_heading"], "level": r["level"]})

    out = Path("results/usc26-moves-119-4-119-110.jsonl")
    out.write_text("".join(json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n" for r in rows))

    through_candidates, affected, by_section = 0, [], Counter()
    changed_paths = {r["path"] for r in changed} | {r["path"] for r in map(json.loads, REUSE.read_text().splitlines())}
    for line in CITATIONS.read_text().splitlines():
        sec = json.loads(line)
        for c in sec["citations"]:
            if not c.get("path"):
                continue
            parts = c["path"].translate(DASHES).split("/")
            prefixes = ["/".join(parts[:i]) for i in range(1, len(parts) + 1)]
            if any(p in changed_paths for p in prefixes):
                through_candidates += 1
            moved = [p for p in prefixes if p in moves]
            if moved:
                p = moved[-1]
                now = moves[p] + c["path"].translate(DASHES)[len(p):]
                affected.append({"sectno": sec["sectno"], "cited": c["path"], "now": now,
                                 "now_exists": now in new})
                by_section[parts[0]] += 1
    aff = Path("results/cfr-moved-citations-v2-2025.jsonl")
    aff.write_text("".join(json.dumps(a, sort_keys=True) + "\n" for a in affected))

    kinds = Counter(r["kind"] for r in rows)
    rec = append({
        "observed_at": "2026-09-16",
        "observed_at_note": "moves between release points 119-4 (2025-03-15) and 119-110 (2026-09-16)",
        "instrument": {
            "name": "scripts/measure_moves.py", "version": "1",
            "method": "old heading (normalized) searched among the 119-110 siblings of each heading-changed "
                      "identifier; one match = move; citations mapped through the deepest moved prefix",
            "known_limits": "moves across parents, or with an edited heading, are missed (counted as "
                            "replaced); identical headings among siblings are ambiguous",
            "predictions": "predictions/2026-09-24-moves-claude.md",
        },
        "population": {
            "title": "26 USC", "release_points": ["119-4", "119-110"],
            "results_file": str(out), "results_sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
            "citations_file": str(aff), "citations_sha256": hashlib.sha256(aff.read_bytes()).hexdigest(),
        },
        "quantity": "usc26_moves",
        "value": {
            "heading_changes": len(rows),
            "kinds": dict(kinds),
            "L1_move_share": [kinds["move"], len(rows)],
            "L2_occurrences_through_moved": [len(affected), through_candidates],
            "L3_by_section": dict(by_section.most_common()),
            "moved_citation_target_exists_at_119_110": sum(a["now_exists"] for a in affected),
            "moves": {k: v for k, v in sorted(moves.items())},
        },
    })
    print(rec["id"], json.dumps(rec["value"], indent=1)[:3000])
    print("ledger verified:", verify())


if __name__ == "__main__":
    main()
