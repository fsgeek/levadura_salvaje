"""Reproduce the evidence behind README "Two wrong diagnoses". Run after measure.py.

    uv run --group plumbing python spikes/plumbing3/diagnose.py

For the stream measure.py last wrote, and the largest cell: how many index entries the
member query scans before the mass correction and at the checkpoint, and (on the 60k
delta generation) the cell-scoped retraction set against an indexed per-record probe.
Writes diagnose-report.json.
"""

import json
import statistics
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "plumbing2"))
sys.path.insert(0, str(HERE))
import lineage as lx  # noqa: E402

from levadura_salvaje.tenant import connect  # noqa: E402


def med(fn, n=5):
    ts = []
    for _ in range(n):
        s = time.perf_counter()
        fn()
        ts.append(time.perf_counter() - s)
    return round(statistics.median(ts), 4)


def members_query():
    return lx.visible("assertions", "AND x.cell == @cell") + \
        " FILTER x.outcome IN @broken COLLECT u = x.unit SORT TO_HEX(u) RETURN u"


def scanned(db, doc, cell):
    cur = db.aql.execute(members_query(), bind_vars={"s": doc["stream"], "anc": doc["ancestors"], "cell": cell,
                                                     "broken": list(lx.BROKEN)}, profile=True)
    rows = list(cur)
    st = cur.statistics()
    return {"members": len(rows), "scanned_index": st.get("scanned_index"), "scanned_full": st.get("scanned_full"),
            "seconds": round(st.get("execution_time", 0), 4)}


def probe_visible(kind, filters=""):
    return f"""
      FOR x IN {lx.C[kind]} FILTER x.stream == @s {filters} AND x.born IN @anc
        FILTER LENGTH(FOR r IN {lx.C['retractions']} FILTER r.record == x._key AND r.born IN @anc LIMIT 1
                      RETURN 1) == 0"""


def main():
    db = connect("app")
    rep = json.loads((HERE / "measure-report.json").read_text())
    stream, cell = rep["stream"], rep["cell"]
    chain = list(db.aql.execute(f"FOR x IN {lx.C['manifests']} FILTER x.stream == @s SORT x.seq RETURN x",
                                bind_vars={"s": stream}))
    pre, mass, ckpt = chain[-3], chain[-2], chain[-1]  # depth 40, the 60k delta, the checkpoint
    out = {"stream": stream, "cell": cell,
           "cell_assertions_by_generation": list(db.aql.execute(
               f"""FOR x IN {lx.C['assertions']} FILTER x.stream == @s AND x.cell == @c
                   COLLECT b = x.born WITH COUNT INTO n SORT n DESC LIMIT 5 RETURN n""",
               bind_vars={"s": stream, "c": cell})),
           "member_query": {"before_mass": scanned(db, pre, cell), "mass_delta": scanned(db, mass, cell),
                            "checkpoint": scanned(db, ckpt, cell)}}
    db.collection(lx.C["retractions"]).add_index({"type": "persistent", "fields": ["record", "born"]})
    real = lx.visible
    times = {}
    for name, vis in (("cell_scoped_set", real), ("per_record_probe", probe_visible)):
        lx.visible = vis
        times[name] = med(lambda: lx.unpaged(db, mass["_key"], cell), 3)
    lx.visible = real
    out["unpaged_on_mass_delta_seconds"] = times
    (HERE / "diagnose-report.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
