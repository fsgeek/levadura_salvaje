"""The parity lens, v2: act names resolved through Yanantin's Jabberwock (act_names), whole-act and list
citations unpaired (act_pairs v2). Otherwise as scripts/measure_banking_parity.py (v1).

Deterministic; predictions in predictions/2026-10-16-banking-parity-v2-claude.md (stamped before v2 ran;
comparison). Builds the corpus's own consensus map (act as written, act section) -> (title, U.S.C.
section), flags pairs that disagree, and builds the A3 audit packet (flagged pairs plus blind
controls). One ledger entry.

Usage: uv run --with-editable ../yanantin python scripts/measure_banking_parity_v2.py
"""

import hashlib
import json
import random
import tempfile
from pathlib import Path

from levadura_salvaje import act_names, act_pairs, usc_cites
from levadura_salvaje.ledger import append, verify
from levadura_salvaje.resolve import Statute
from levadura_salvaje.sections import distinct_sections

RP, SEED = "119-120", 20261016
HELD = ("12", "15", "31")
OUT = Path("results/banking-parity-v2-2025.jsonl")
AUDIT = Path("results/banking-parity-audit-a3")
PREDICTIONS = "predictions/2026-10-16-banking-parity-v2-claude.md"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    statutes = {t: Statute.load(RP, title=t) for t in HELD}
    headings = {}
    for t in HELD:
        for line in open(f"results/usc{t}-provisions-{RP}.jsonl"):
            p = json.loads(line)
            if p["level"] == "section":
                headings[(t, p["path"][1:].replace("–", "-"))] = p["heading"]

    def in_force(title, sec):
        if title not in statutes:
            return None
        return statutes[title].resolve(sec)["outcome"] == "resolves"

    secs = []
    for t in ("12", "31"):
        for s in distinct_sections(Path(f"data/banking/CFR-2025-title-{t}.zip")):
            secs.append((t, s["sectno"].split(".")[0], s, usc_cites.normalize(s["text"])))
    names = act_names.ActNames(Path(tempfile.mkdtemp()) / "acts.duckdb")
    for t, part, s, text in secs:  # definitions first, so every pair sees every definition
        names.learn(t, part, text)
    rows, texts, cache = [], {}, {}
    for t, part, s, text in secs:
        for p in act_pairs.pairs(text, normalized=True):
            k = (p["act"], t, part)
            if k not in cache:
                cache[k] = names.resolve(p["act"], t, part)
            aid = cache[k]
            rows.append({**p, "cfr_title": t, "sectno": s["sectno"], "volume_file": s["volume_file"],
                         "ordinal": s["ordinal"], "act_entity": str(aid) if aid else None,
                         "act_key": str(aid) if aid else "name:" + act_names.canonical(p["act"])})
            texts[(t, s["volume_file"], s["ordinal"])] = text
    keyed = [{**r, "act": r["act_key"]} for r in rows]
    cmap = act_pairs.consensus(keyed)
    for r in rows:
        c = cmap.get((r["act_key"], r["act_section"]))
        r["covered"] = c is not None
        r["consensus"] = list(c["target"]) if c else None
        r["disagrees"] = bool(c) and (r["title"], r["usc_section"]) != c["target"]
        r["own_in_force"] = in_force(r["title"], r["usc_section"])
    OUT.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in rows))

    covered = [r for r in rows if r["covered"]]
    flagged = [r for r in covered if r["disagrees"]]
    rated_flags = [r for r in flagged if r["own_in_force"] is not None]
    targets = {tuple(v["target"]) for v in cmap.values()}
    rated_targets = [x for x in targets if x[0] in statutes]
    m = {
        "pairs": len(rows),
        "V2_resolved_share": round(sum(r["act_entity"] is not None for r in rows) / len(rows), 4),
        "V3_names_per_key": round(len({r["act"] for r in rows}) / len({r["act_key"] for r in rows}), 4),
        "consensus_keys": len(cmap),
        "V4_covered_share": round(len(covered) / len(rows), 4),
        "flagged": len(flagged),
        "V5_disagree_share": round(len(flagged) / len(covered), 4),
        "flagged_in_held_titles": len(rated_flags),
        "P3_flag_own_in_force_share": round(sum(r["own_in_force"] for r in rated_flags) / len(rated_flags), 4)
        if rated_flags else None,
        "targets_in_held_titles": len(rated_targets),
        "P4_targets_in_force_share": round(sum(bool(in_force(*x)) for x in rated_targets) / len(rated_targets), 4)
        if rated_targets else None,
    }

    rng = random.Random(SEED)
    picks = rng.sample(flagged, min(40, len(flagged)))
    controls = rng.sample([r for r in covered if not r["disagrees"]], 20)
    items = [(r, True) for r in picks] + [(r, False) for r in controls]
    rng.shuffle(items)
    AUDIT.mkdir(exist_ok=True)
    packet, key = [], []
    for i, (r, is_flag) in enumerate(items, 1):
        text = texts[(r["cfr_title"], r["volume_file"], r["ordinal"])]
        a, b = r["span"]
        cons = tuple(r["consensus"])
        item = f"item-{i:02d}"
        packet.append({
            "item": item, "cfr": f"{r['cfr_title']} CFR {r['sectno']} (2025)",
            "excerpt": text[max(0, a - 250):b + 150], "pair_as_read": text[a:b],
            "act_section": f"section {r['act_section']} of the {r['act']}",
            "cited_usc": f"{r['title']} U.S.C. {r['usc_path']}",
            "cited_usc_heading": headings.get((r["title"], r["usc_section"]), "(no section with this number in the titles held, or a title not held)"),
            "reference_usc": f"{cons[0]} U.S.C. {cons[1]}",
            "reference_usc_heading": headings.get(cons, "(title not held)"),
        })
        key.append({"item": item, "flagged": is_flag, "sectno": r["sectno"], "span": r["span"]})
    (AUDIT / "packet.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in packet))
    (AUDIT / "key.jsonl").write_text("".join(json.dumps(x) + "\n" for x in key))

    entry = append({
        "observed_at": "2025-01-01",
        "observed_at_note": "2025 CFR titles 12 (as of Jan 1) and 31 (as of Jul 1), read against USC release point "
                            f"{RP}",
        "instrument": {
            "name": "scripts/measure_banking_parity.py",
            "method": f"act_names v{act_names.VERSION} (Yanantin Jabberwock: wabes cfr.<title>.<part>, act.name, "
                      "act.short) keys acts; "
                      f"act_pairs v{act_pairs.VERSION} over usc_cites v{usc_cites.VERSION}: 'section N of the <Name> "
                      "Act' immediately followed by a U.S.C. citation; consensus map per (resolved act, act "
                      "section) at >=3 pairs and >=75% agreement; a pair disagrees when its (title, U.S.C. "
                      "section) differs from the consensus target",
            "known_limits": "unresolved acts keyed by canonical name; definitions read by two regexes (X means Y; "
                            "Y (X)); singular 'section' only; section-level map; a disagreement is "
                            "a candidate until audited (A3)",
            "predictions": PREDICTIONS,
        },
        "population": {"edition": "2025", "titles": ["12", "31"], "release_point": RP},
        "quantity": "banking_act_usc_parity",
        "value": {**m, "output": str(OUT), "output_sha256": sha(OUT),
                  "audit_packet_sha256": sha(AUDIT / "packet.jsonl")},
    })
    print(entry["id"], json.dumps(m))
    print("ledger:", verify())


if __name__ == "__main__":
    main()
