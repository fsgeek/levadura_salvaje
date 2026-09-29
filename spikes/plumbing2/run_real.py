"""Spike 2 item 4 on the real corpus, in the tenant's app database. Idempotent.

    uv run --group plumbing python spikes/plumbing2/run_real.py

Writes real-report.json next to this file. Each check is recorded, pass or fail;
the script exits non-zero if any fails.
"""

import json
import random
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import corpus as cx  # noqa: E402
import index as ix  # noqa: E402

from levadura_salvaje.tenant import connect  # noqa: E402

ME = "levadura-owner-2026-09-29"
REPORT = Path(__file__).with_name(sys.argv[1] if len(sys.argv) > 1 else "real-report.json")
checks, facts, timings = {}, {}, {}


def check(name, ok, detail=None):
    checks[name] = {"pass": bool(ok), **({"detail": detail} if detail is not None else {})}
    print(("PASS " if ok else "FAIL ") + name + (f"  {detail}" if detail is not None else ""))


def timed(name, fn, *a, **k):
    t = time.perf_counter()
    out = fn(*a, **k)
    timings[name] = round(time.perf_counter() - t, 2)
    return out


def main():
    db = connect("app")
    ix.ensure(db)

    # provisions: loaded from the archive, cross-checked against the measured results file
    um = timed("publish_provisions", cx.publish_provisions, db, ME)
    stored = list(db.aql.execute("""FOR p IN provisions FILTER p.manifest == @m SORT p.position
                                    RETURN [p.identifier, p.locator.sha256]""", bind_vars={"m": um},
                                 batch_size=20000))
    with open(str(cx.USC_RESULTS).format(rp=cx.RP)) as f:
        measured = [[r["identifier"], r["text_sha256"]] for r in map(json.loads, f)]
    check("provisions match the measured file row for row", stored == measured, len(stored))
    ids = Counter(i for i, _ in stored)
    collided = sorted(i for i, n in ids.items() if n > 1)
    facts["provisions"] = {"rows": len(stored), "identifiers": len(ids), "collided_identifiers": len(collided),
                           "extra_rows": len(stored) - len(ids)}
    check("57,176 rows, 57,161 identifiers", (len(stored), len(ids)) == (57176, 57161), facts["provisions"])

    # the CFR with resolve.py's labels, then resolved inside the index
    rows_a, _ = timed("rows_imported", cx.cfr_rows)
    ma = timed("publish_imported", ix.publish, db, "cfr26-2025@119-4/resolve.py-v2", cx.RP, rows_a, ME)
    paths = {o["path"] for r in rows_a for o in r["occurrences"] if o["path"]}
    paths |= {p.split("/")[0] for p in paths}
    resolver = timed("load_resolver", cx.IndexResolver, db, um, paths)
    rows_b, targets = timed("rows_index", cx.cfr_rows, resolver)
    edge_inputs = sorted([u, i, t] for (u, i), t in targets.items())
    mb = timed("publish_index", ix.publish, db, "cfr26-2025@119-4/index", cx.RP, rows_b, ME,
               depends_on=(um,), extra=cx.edge_writer(db, targets, ME), extra_inputs=edge_inputs)
    facts["manifests"] = {"usc": um, "imported": ma, "index": mb}

    # the two resolvers, occurrence by occurrence
    diff, compared, aligned = Counter(), 0, len(rows_a) == len(rows_b)
    for ra, rb in zip(rows_a, rows_b):
        aligned &= ra["unit"] == rb["unit"] and len(ra["occurrences"]) == len(rb["occurrences"])
        for oa, ob in zip(ra["occurrences"], rb["occurrences"]):
            aligned &= oa["path"] == ob["path"]
            if oa["path"] is None:
                continue  # neither resolver sees these
            compared += 1
            if (oa["outcome"], oa["target_outcome"]) != (ob["outcome"], ob["target_outcome"]):
                diff[(oa["outcome"], ob["outcome"], oa["target_outcome"], ob["target_outcome"])] += 1
    n_occ = sum(len(r["occurrences"]) for r in rows_a)
    check("index resolver agrees with resolve.py on every resolvable occurrence", aligned and not diff,
          {"occurrences": n_occ, "compared": compared, "null_paths": n_occ - compared, "aligned": aligned,
           "disagreements": [[*k, v] for k, v in diff.most_common(10)]})

    # finding #1 from both manifests, per cell and merged
    for name, m in (("imported", ma), ("index", mb)):
        states = ix.cell_states(db, m)
        top = ix.merge(list(states.values()))
        facts[name] = {"broken": top["broken"], "occurrences": top["occurrences"], "units": top["units"],
                       "fossil_units": len(top["members"]), "cited_distinct": len(top["cited"]),
                       "naive_sum": sum(len(s["cited"]) for s in states.values()),
                       "conflicts": len(top["conflicts"]), "cells": len(states)}
        check(f"{name}: finding #1 (obs-0129)",
              (top["broken"], top["occurrences"], len(top["members"]), top["units"], len(top["cited"]))
              == (10300, 124993, 1675, 6158, 1673), facts[name])
    sa, sb = ix.cell_states(db, ma), ix.cell_states(db, mb)
    check("per cell, both manifests have the same members", {c: s["members"] for c, s in sa.items()}
          == {c: s["members"] for c, s in sb.items()})
    bad = [c for c in sorted(sb) if [u for p in ix.drill_all(db, mb, c) for u in p["page"]]
           != ix.rollup(db, mb, c)["members"]]
    check("per cell, concatenated drill pages equal the persisted rollup", not bad, bad[:5])

    # edges: fan-out where addresses collide
    fan = {f: n for f, n in db.aql.execute("""FOR e IN resolves_to FILTER e.manifest == @m
                                              COLLECT f = e.fanout WITH COUNT INTO n RETURN [f, n]""",
                                           bind_vars={"m": mb})}
    multi = list(db.aql.execute("""FOR e IN resolves_to FILTER e.manifest == @m AND e.fanout > 1
                                   LET a = DOCUMENT(e._from) LET p = DOCUMENT(e._to)
                                   COLLECT unit = a.unit, path = a.target, ident = p.identifier
                                   WITH COUNT INTO n RETURN {unit, ident, n}""", bind_vars={"m": mb}))
    facts["resolves_to"] = {"edges_by_fanout": fan, "collided_citations": multi[:10], "n_collided": len(multi)}
    want_edges = {(f"assertions/{ix.key(ix.key(mb, u, i), cx.RP)}", f"provisions/{k}")
                  for (u, i), keys in targets.items() for k in keys}
    got_edges = {(e[0], e[1]) for e in db.aql.execute(
        "FOR e IN resolves_to FILTER e.manifest == @m RETURN [e._from, e._to]", bind_vars={"m": mb},
        batch_size=50000)}
    dangling = next(db.aql.execute("""RETURN LENGTH(FOR e IN resolves_to FILTER e.manifest == @m
        LET a = DOCUMENT(e._from) LET p = DOCUMENT(e._to)
        FILTER a == null OR p == null OR a.manifest != @m OR p.manifest != @um RETURN 1)""",
                                   bind_vars={"m": mb, "um": um}))
    check("edge endpoints are exactly the resolver's targets, one per provision version",
          got_edges == want_edges and dangling == 0,
          {"edges": len(got_edges), "missing": len(want_edges - got_edges), "unexpected": len(got_edges - want_edges),
           "dangling_or_foreign": dangling, "edges_by_fanout": fan})

    # follow: drill members -> their citations -> provisions, in two hash domains
    rng = random.Random(0)
    sample_units = rng.sample(sorted(u for s in sb.values() for u in s["members"]), 20)
    outcomes = Counter()
    for uid in sample_units:
        u = next(db.aql.execute("FOR u IN units FILTER u.manifest == @m AND u.unit == @u RETURN u",
                                bind_vars={"m": mb, "u": uid}))
        outcomes["cfr:" + cx.follow(u["locator"])["status"]] += 1
        for p in db.aql.execute("""FOR a IN assertions FILTER a.manifest == @m AND a.unit == @u
                                   FOR p IN OUTBOUND a resolves_to RETURN p""", bind_vars={"m": mb, "u": uid}):
            outcomes["usc:" + cx.follow(p["locator"])["status"]] += 1
    collided_docs = list(db.aql.execute("""FOR p IN provisions FILTER p.manifest == @m AND p.identifier IN @ids
                                           RETURN p""", bind_vars={"m": um, "ids": collided}))
    both = Counter(cx.follow(p["locator"])["status"] for p in collided_docs)
    facts["follow"] = {"sampled_units": 20, "statuses": dict(outcomes), "collided_versions": dict(both)}
    check("followed locators verify in their own hash domain",
          set(outcomes) <= {"cfr:ok", "usc:ok"} and outcomes["cfr:ok"] == 20 and outcomes["usc:ok"] >= 20,
          dict(outcomes))
    check("every version of a collided identifier verifies separately",
          both == {"ok": len(collided_docs)} and len(collided_docs) == 29, dict(both))
    p = collided_docs[0]
    check("a wrong hash is stale", cx.follow(p["locator"] | {"sha256": "0" * 64})["status"] == "stale")
    check("an undeclared hash domain is refused",
          cx.follow(p["locator"] | {"hash_domain": "levadura.usc.flat_v0"})["status"] == "unknown-domain")
    check("a missing release is unreachable",
          cx.follow(p["locator"] | {"uri": p["locator"]["uri"].replace(cx.RP, "118-1")})["status"] == "unreachable")

    storage = {}
    for c in ("units", "occurrences", "assertions", "rollups", "provisions", "resolves_to", "queries", "manifests"):
        st = db.collection(c).statistics()
        storage[c] = {"docs": db.collection(c).count(), "documents_size": st.get("documents_size"),
                      "indexes_size": st.get("indexes", {}).get("size")}
    REPORT.write_text(json.dumps({"checks": checks, "facts": facts, "timings_s": timings,
                                  "storage_bytes": storage}, indent=1, default=str) + "\n")
    failed = [k for k, v in checks.items() if not v["pass"]]
    print(f"{len(checks) - len(failed)}/{len(checks)} checks pass; timings {timings}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
