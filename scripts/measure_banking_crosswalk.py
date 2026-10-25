"""The act-section crosswalk, v1: the parity lens's equivalence classes for 12 CFR as of 1997, 2010
and 2025, compared across editions.

A class is every way the corpus writes one act section (resolved through act_names), mapped by the
corpus's own consensus to one U.S.C. address. A class held in two editions is kept if the address
is the same and moved if it differs; otherwise it is new or gone.

Deterministic; predictions in predictions/2026-10-25-banking-crosswalk-claude.md (stamped before this
ran). One act_names store serves all editions: long names resolve to one entity in every edition,
and part-scoped short names are scoped to their edition too (wabe cfr.12.<edition>.<part>), because
Jabberwock has no world time (Yanantin #41). Builds the X1 audit packet (moved classes plus blind
kept controls). One ledger entry, none with --dry-run.

Usage: uv run --with-editable ../yanantin python scripts/measure_banking_crosswalk.py [--dry-run]
"""

import hashlib
import json
import random
import sys
import tempfile
from collections import Counter
from pathlib import Path

from levadura_salvaje import act_names, act_pairs, usc_cites
from levadura_salvaje.ledger import append, verify
from levadura_salvaje.resolve import Statute
from levadura_salvaje.sections import distinct_sections

RP, SEED = "119-120", 20261025
HELD = ("7", "12", "15", "31", "50")
EDITIONS = ("1997", "2010", "2025")
OUT = Path("results/banking-crosswalk-12.jsonl")
AUDIT = Path("results/banking-crosswalk-audit-x1")
PREDICTIONS = "predictions/2026-10-25-banking-crosswalk-claude.md"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    dry = "--dry-run" in sys.argv
    statutes = {t: Statute.load(RP, title=t) for t in HELD}
    headings = {}
    for t in HELD:
        for line in open(f"results/usc{t}-provisions-{RP}.jsonl"):
            p = json.loads(line)
            if p["level"] == "section":
                headings[(t, p["path"][1:].replace("–", "-"))] = p["heading"]

    def is_section(title, sec):
        return title in statutes and statutes[title].resolve(sec)["outcome"] != "absent-section"

    secs = {e: [(s["sectno"].split(".")[0], s, usc_cites.normalize(s["text"]))
                for s in distinct_sections(Path(f"data/banking/CFR-{e}-title-12.zip"))] for e in EDITIONS}
    names = act_names.ActNames(Path(tempfile.mkdtemp()) / "acts.duckdb")
    for e in EDITIONS:  # every definition first, so every pair sees every definition
        for part, s, text in secs[e]:
            names.learn(f"12.{e}", part, text)

    rows, cmaps, cache = {}, {}, {}
    for e in EDITIONS:
        rows[e] = []
        for part, s, text in secs[e]:
            for p in act_pairs.pairs(text, normalized=True, is_section=is_section):
                k = (p["act"], e, part)
                if k not in cache:
                    cache[k] = names.resolve(p["act"], f"12.{e}", part)
                aid = cache[k]
                a, b = p["span"]
                rows[e].append({**p, "edition": e, "sectno": s["sectno"],
                                "act_key": str(aid) if aid else "name:" + act_names.canonical(p["act"]),
                                "excerpt": text[max(0, a - 200):b + 120]})
        keyed = [{**r, "act": r["act_key"]} for r in rows[e]]
        keyed = act_pairs.rekey_letters(keyed, act_pairs.consensus(keyed))
        for r, k in zip(rows[e], keyed):
            r.update(act_section=k["act_section"], act_desig=k["act_desig"])
        cmaps[e] = act_pairs.consensus(keyed)

    written = {}  # class key -> how the act is most often written
    for e in EDITIONS:
        for r in rows[e]:
            written.setdefault((r["act_key"], r["act_section"]), Counter())[r["act"]] += 1

    def status(e1, e2, key):
        a, b = cmaps[e1].get(key), cmaps[e2].get(key)
        if a and b:
            return "kept" if a["target"] == b["target"] else "moved"
        return "new" if b else "gone" if a else None

    keys = sorted(set().union(*cmaps.values()))
    classes = []
    for key in keys:
        c = {"act_key": key[0], "act_section": key[1],
             "act_as_written": written[key].most_common(1)[0][0] if key in written else None}
        for e in EDITIONS:
            m = cmaps[e].get(key)
            c[e] = {"target": list(m["target"]), "n": m["n"], "share": m["share"]} if m else None
        for e1, e2 in (("1997", "2010"), ("2010", "2025"), ("1997", "2025")):
            c[f"{e1}-{e2}"] = status(e1, e2, key)
        classes.append(c)
    OUT.write_text("".join(json.dumps(c, sort_keys=True) + "\n" for c in classes))

    consecutive = [c[t] for c in classes for t in ("1997-2010", "2010-2025") if c[t] in ("kept", "moved")]
    ecoa = str(names.act("Equal Credit Opportunity Act"))
    m = {
        "C1_pairs_1997": len(rows["1997"]),
        "C2_pairs_2010": len(rows["2010"]),
        "C3_pairs_2025": len(rows["2025"]),
        "C4_classes": {e: len(cmaps[e]) for e in EDITIONS},
        "C5_classes_1997_and_2025": sum(c["1997"] is not None and c["2025"] is not None for c in classes),
        "C6_consecutive_held": len(consecutive),
        "C6_consecutive_moved": consecutive.count("moved"),
        "C6_moved_share": round(consecutive.count("moved") / len(consecutive), 4) if consecutive else None,
        "C7_ecoa_703": {e: (cmaps[e].get((ecoa, "703")) or {}).get("target") for e in EDITIONS},
        "status_counts": {t: dict(Counter(c[t] for c in classes if c[t]))
                          for t in ("1997-2010", "2010-2025", "1997-2025")},
    }
    print(json.dumps(m))
    if dry:
        return

    rng = random.Random(SEED)
    moved = [(c, t) for c in classes for t in ("1997-2010", "2010-2025") if c[t] == "moved"]
    picks = rng.sample(moved, min(30, len(moved)))
    kept = [(c, t) for c in classes for t in ("1997-2010", "2010-2025") if c[t] == "kept"]
    controls = rng.sample(kept, min(10, len(kept)))
    items = [(c, t, True) for c, t in picks] + [(c, t, False) for c, t in controls]
    rng.shuffle(items)
    AUDIT.mkdir(exist_ok=True)
    packet, key = [], []
    for i, (c, t, is_moved) in enumerate(items, 1):
        item, side = f"item-{i:02d}", {}
        for e in t.split("-"):
            target = tuple(c[e]["target"])
            ex = [r["excerpt"] for r in rows[e] if (r["act_key"], r["act_section"]) == (c["act_key"], c["act_section"])
                  and (r["title"], r["usc_section"]) == target]
            side[e] = {"address": f"{target[0]} U.S.C. {target[1]}",
                       "address_heading_2025": headings.get(target, "(no section with this number in the 2025 Code, "
                                                                     "or a title not held)"),
                       "pairs": c[e]["n"], "excerpts": rng.sample(ex, min(2, len(ex)))}
        e1, e2 = t.split("-")
        packet.append({"item": item, "act_section": f"section {c['act_section']} of the {c['act_as_written']}",
                       "earlier_edition": e1, "earlier": side[e1], "later_edition": e2, "later": side[e2]})
        key.append({"item": item, "moved": is_moved, "act_key": c["act_key"], "act_section": c["act_section"],
                    "transition": t})
    (AUDIT / "packet.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in packet))
    (AUDIT / "key.jsonl").write_text("".join(json.dumps(x) + "\n" for x in key))

    entry = append({
        "observed_at": "2025-01-01",
        "observed_at_note": "12 CFR as of Jan 1 of 1997, 2010 and 2025, read against USC release point " + RP,
        "instrument": {
            "name": "scripts/measure_banking_crosswalk.py",
            "method": f"act_pairs v{act_pairs.VERSION} over usc_cites v{usc_cites.VERSION}; one act_names "
                      f"v{act_names.VERSION} store for all editions (wabes cfr.12.<edition>.<part>, act.name, "
                      "act.short); per edition a consensus map per (resolved act, act section) at >=3 pairs and "
                      ">=75% agreement; a class held in two editions is kept (same address) or moved",
            "known_limits": "12 CFR only; hyphenated tokens decided against the current Code in every edition; "
                            "act.short shared across editions; the edition is in the wabe name because "
                            "Jabberwock has no world time; a moved class is a candidate until audited (X1)",
            "predictions": PREDICTIONS,
        },
        "population": {"editions": list(EDITIONS), "titles": ["12"], "release_point": RP,
                       "usc_titles_held": list(HELD)},
        "quantity": "banking_act_section_crosswalk",
        "value": {**m, "output": str(OUT), "output_sha256": sha(OUT),
                  "audit_packet_sha256": sha(AUDIT / "packet.jsonl")},
    })
    print(entry["id"])
    print("ledger:", verify())


if __name__ == "__main__":
    main()
