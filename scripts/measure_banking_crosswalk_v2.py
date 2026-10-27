"""The act-section crosswalk, v2 (Jabberwock world time; unresolved "the Act" forms no class). From v1: the parity lens's equivalence classes for 12 CFR as of 1997, 2010
and 2025, compared across editions.

A class is every way the corpus writes one act section (resolved through act_names), mapped by the
corpus's own consensus to one U.S.C. address. A class held in two editions is kept if the address
is the same and moved if it differs; otherwise it is new or gone.

Deterministic; predictions in predictions/2026-10-25-banking-crosswalk-claude.md (stamped before this
ran). One act_names store serves all editions: long names resolve to one entity in every edition,
and part-scoped short names are scoped to their edition too (wabe cfr.12.<edition>.<part>), because
Jabberwock has no world time (Yanantin #41). Builds the X1 audit packet (moved classes plus blind
kept controls). One ledger entry, none with --dry-run.

v2 (2026-10-27): one wabe per part (cfr.12.<part>), each alias gyred from its edition's date to the next's,
resolved at= the edition date; pairs keyed name:act form no class. X1-X3 compare with v1's output.

Usage: uv run --with-editable ../yanantin python scripts/measure_banking_crosswalk_v2.py [--dry-run]
"""

import hashlib
import json
import random
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from levadura_salvaje import act_names, act_pairs, usc_cites
from levadura_salvaje.ledger import append, verify
from levadura_salvaje.resolve import Statute
from levadura_salvaje.sections import distinct_sections

RP, SEED = "119-120", 20261025
HELD = ("7", "12", "15", "31", "50")
EDITIONS = ("1997", "2010", "2025")
OUT = Path("results/banking-crosswalk-v2-12.jsonl")
V1 = Path("results/banking-crosswalk-12.jsonl")
PREDICTIONS = "predictions/2026-10-27-banking-crosswalk-v2-claude.md"
AT = {e: datetime(int(e), 1, 1, tzinfo=timezone.utc) for e in EDITIONS}
UNTIL = {"1997": AT["2010"], "2010": AT["2025"], "2025": None}


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
    names = act_names.ActNames()  # in memory; with Yanantin #46, crosswalk dry run 7m14s -> 96 s (file) -> 79 s (memory), 2026-10-25
    for e in EDITIONS:  # every definition first, so every pair sees every definition
        for part, s, text in secs[e]:
            names.learn("12", part, text, gyre_from=AT[e], gyre_to=UNTIL[e])

    rows, cmaps, cache, all_pairs = {}, {}, {}, {}
    for e in EDITIONS:
        rows[e] = []
        for part, s, text in secs[e]:
            for p in act_pairs.pairs(text, normalized=True, is_section=is_section):
                k = (p["act"], e, part)
                if k not in cache:
                    cache[k] = names.resolve(p["act"], "12", part, at=AT[e])
                aid = cache[k]
                a, b = p["span"]
                rows[e].append({**p, "edition": e, "sectno": s["sectno"],
                                "act_key": str(aid) if aid else "name:" + act_names.canonical(p["act"]),
                                "excerpt": text[max(0, a - 200):b + 120]})
        all_pairs[e] = len(rows[e])  # X3 counts pairing, before the v2 filter (fixed in the dry run)
        rows[e] = [r for r in rows[e] if r["act_key"] != "name:act"]  # v2: an unresolved "the Act" pools acts
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
    def classes_of(path, drop_pooled):
        out = {}
        for line in open(path):
            c = json.loads(line)
            if drop_pooled and c["act_key"] == "name:act":
                continue
            for e in EDITIONS:
                if c[e]:
                    out[(e, c["act_as_written"], c["act_section"])] = tuple(c[e]["target"])
        return out

    v1, v2 = classes_of(V1, True), classes_of(OUT, False)
    m["X1_identical_to_v1"] = {e: {k: t for k, t in v1.items() if k[0] == e} == {k: t for k, t in v2.items() if k[0] == e}
                               for e in EDITIONS}
    m["X1_only_v1"] = sorted(str(k) for k in set(v1) - set(v2))[:10]
    m["X1_only_v2"] = sorted(str(k) for k in set(v2) - set(v1))[:10]
    m["X2_consecutive_moved"] = m["C6_consecutive_moved"]
    m["X3_pairs"] = [all_pairs[e] for e in EDITIONS]
    m["pairs_after_v2_filter"] = [m["C1_pairs_1997"], m["C2_pairs_2010"], m["C3_pairs_2025"]]
    print(json.dumps(m))
    if dry:
        return
    entry = append({
        "observed_at": "2025-01-01",
        "observed_at_note": "12 CFR as of Jan 1 of 1997, 2010 and 2025, read against USC release point " + RP,
        "instrument": {
            "name": "scripts/measure_banking_crosswalk_v2.py",
            "method": f"as v1, with act_names v{act_names.VERSION}: one wabe per part, aliases gyred by edition and "
                      "resolved at= the edition date (Yanantin #41/#46/#47); pairs keyed name:act form no class",
            "known_limits": "12 CFR only; hyphenated tokens decided against the current Code; act.short shared "
                            "across editions; equivalence with v1 is the claim, not new findings",
            "predictions": PREDICTIONS,
        },
        "population": {"editions": list(EDITIONS), "titles": ["12"], "release_point": RP},
        "quantity": "banking_act_section_crosswalk_v2",
        "value": {**m, "output": str(OUT), "output_sha256": sha(OUT)},
    })
    print(entry["id"])
    print("ledger:", verify())

if __name__ == "__main__":
    main()
