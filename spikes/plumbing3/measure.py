"""Spike 3 on the real corpus: what a correction costs, and what depth costs readers.

    uv run --group plumbing python spikes/plumbing3/measure.py

Uses the tenant's app database and a fresh stream name per run, so it doesn't disturb
spike 2's manifests (which are the full-copy baseline for read timings). Writes
measure-report.json. Every generation is checked against fixture.expected(rows).
"""

import copy
import json
import random
import statistics
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "plumbing2"))
sys.path.insert(0, str(HERE))
import corpus as cx  # noqa: E402
import fixture as fx  # noqa: E402
import index as ix  # noqa: E402
import lineage as lx  # noqa: E402

from levadura_salvaje.tenant import connect  # noqa: E402

ME = "levadura-owner-2026-09-30"
REPORT = HERE / "measure-report.json"
report = {"corrections": [], "reads": [], "checks": {}}


def t(fn, *a, **k):
    s = time.perf_counter()
    out = fn(*a, **k)
    return out, time.perf_counter() - s


def flip(rows, rng, k):
    """k corrections: flip the outcome of k random resolvable occurrences."""
    rows = copy.deepcopy(rows)
    occ = [o for r in rows for o in r["occurrences"] if o["path"]]
    for o in rng.sample(occ, k):
        o["outcome"] = "in-force" if o["outcome"] in fx.BROKEN else "repealed"
    return rows


def verify(db, m, rows, cells=None) -> bool:
    exp = fx.expected(rows)
    states = lx.cell_states(db, m)
    ok = ix.merge(list(states.values()))["members"] == exp["top"]["members"]
    ok &= {c: s["members"] for c, s in states.items()} == {c: e["members"] for c, e in exp["cells"].items()}
    for c in cells or []:
        ok &= lx.rollup(db, m, c)["members"] == exp["cells"][c]["members"]
        ok &= [u for p in lx.drill_all(db, m, c) for u in p["page"]] == exp["cells"][c]["members"]
    return ok


def reads(db, m, cell, n=5) -> dict:
    """Median seconds for each published reader on one cell (and cell_states over all)."""
    out = {}
    for name, fn in (("drill_first_page", lambda: lx.drill(db, m, cell)), ("rollup", lambda: lx.rollup(db, m, cell)),
                     ("unpaged", lambda: lx.unpaged(db, m, cell)), ("cell_states_all", lambda: lx.cell_states(db, m))):
        out[name] = round(statistics.median(t(fn)[1] for _ in range(n)), 4)
    return out


def reads_full_copy(db, m, cell, n=5) -> dict:
    out = {}
    for name, fn in (("drill_first_page", lambda: ix.drill(db, m, cell)), ("rollup", lambda: ix.rollup(db, m, cell)),
                     ("unpaged", lambda: ix.unpaged(db, m, cell)), ("cell_states_all", lambda: ix.cell_states(db, m))):
        out[name] = round(statistics.median(t(fn)[1] for _ in range(n)), 4)
    return out


def baseline(db, rows, tag) -> str:
    """Spike 2's full-copy layout holding exactly these rows: the fair comparison."""
    return ix.publish(db, f"baseline/{tag}", cx.RP, rows, ME)


def main():
    db = connect("app")
    lx.ensure(db)
    stream = f"cfr26-2025@119-4/lineage/{int(time.time())}"
    rng = random.Random(0)
    rows, _ = cx.cfr_rows()
    big = max(fx.expected(rows)["cells"].items(), key=lambda kv: len(kv[1]["members"]))[0]
    report["stream"], report["cell"] = stream, big

    m, secs = t(lx.publish, db, stream, cx.RP, rows, ME)
    report["corrections"].append({"depth": 1, "changed": "all (first)", "seconds": round(secs, 2),
                                  "written": db.collection(lx.C["manifests"]).get(m)["written"]})
    chain = [(m, rows)]
    for k in (1, 100, 5000):
        rows = flip(rows, rng, k)
        m, secs = t(lx.publish, db, stream, cx.RP, rows, ME)
        chain.append((m, rows))
        report["corrections"].append({"depth": len(chain), "changed": k, "seconds": round(secs, 2),
                                      "written": db.collection(lx.C["manifests"]).get(m)["written"]})
        print(report["corrections"][-1])
    tag = stream.rsplit("/", 1)[-1]
    report["reads"].append({"layout": "full copy, same rows", "depth": len(chain),
                            **reads_full_copy(db, baseline(db, rows, f"{tag}-d{len(chain)}"), big)})
    report["reads"].append({"layout": "lineage", "depth": len(chain), **reads(db, chain[-1][0], big)})
    for depth in (5, 10, 20, 40):
        while len(chain) < depth:
            rows = flip(rows, rng, 10)
            m, secs = t(lx.publish, db, stream, cx.RP, rows, ME)
            chain.append((m, rows))
            report["corrections"].append({"depth": len(chain), "changed": 10, "seconds": round(secs, 2),
                                          "written": db.collection(lx.C["manifests"]).get(m)["written"]})
        report["reads"].append({"layout": "lineage", "depth": depth, **reads(db, chain[-1][0], big)})
        if depth == 40:
            report["reads"].append({"layout": "full copy, same rows", "depth": depth,
                                    **reads_full_copy(db, baseline(db, rows, f"{tag}-d40"), big)})
        print(report["reads"][-1])
    # a new statute release: about half the outcomes change at once. First as a plain delta
    # (checkpoints off), to measure cell-scoped retractions alone ...
    policy, lx.CHECKPOINT = lx.CHECKPOINT, float("inf")
    rows = flip(rows, rng, 60000)
    m, secs = t(lx.publish, db, stream, cx.RP, rows, ME)
    chain.append((m, rows))
    report["corrections"].append({"depth": len(chain), "changed": 60000, "seconds": round(secs, 2),
                                  "checkpoint": False, "written": db.collection(lx.C["manifests"]).get(m)["written"]})
    report["reads"].append({"layout": "full copy, same rows", "depth": len(chain), "after": "60k-row delta",
                            **reads_full_copy(db, baseline(db, rows, f"{tag}-mass"), big)})
    report["reads"].append({"layout": "lineage", "depth": len(chain), "after": "60k-row delta",
                            **reads(db, m, big)})
    print(report["corrections"][-1], report["reads"][-1])
    # ... then policy on: the next small correction finds the threshold passed and writes a checkpoint
    lx.CHECKPOINT = policy
    rows = flip(rows, rng, 10)
    m, secs = t(lx.publish, db, stream, cx.RP, rows, ME)
    chain.append((m, rows))
    doc = db.collection(lx.C["manifests"]).get(m)
    report["corrections"].append({"depth": len(chain), "changed": 10, "seconds": round(secs, 2),
                                  "checkpoint": doc["checkpoint"], "written": doc["written"]})
    report["reads"].append({"layout": "lineage", "depth": len(chain), "after": "checkpoint", **reads(db, m, big)})
    print(report["corrections"][-1], report["reads"][-1])
    sample = rng.sample(sorted(fx.expected(chain[0][1])["cells"]), 5) + [big]
    report["checks"]["every generation: all cells' members and the merged top"] = all(
        verify(db, m, r) for m, r in chain)
    report["checks"]["first, middle, last: rollup and pages for 6 cells"] = all(
        verify(db, m, r, sample) for m, r in (chain[0], chain[len(chain) // 2], chain[-1]))
    storage = {}
    for c in list(lx.C.values()) + ["units", "occurrences", "assertions"]:
        st = db.collection(c).statistics()
        storage[c] = {"docs": db.collection(c).count(), "documents_size": st.get("documents_size")}
    report["storage_bytes"] = storage
    REPORT.write_text(json.dumps(report, indent=1) + "\n")
    print(json.dumps(report["checks"]), json.dumps(storage))
    sys.exit(0 if all(report["checks"].values()) else 1)


if __name__ == "__main__":
    main()
