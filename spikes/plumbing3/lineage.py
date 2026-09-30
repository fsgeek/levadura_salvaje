"""Plumbing spike 3: corrections that don't copy the corpus. Throwaway.

Spike 2 keyed every record by its manifest, so a one-row correction republished
125k occurrences (spikes/plumbing2/README.md, "Hard"). Here a generation writes only
what changed:

- A record lives in a *slot*: a unit (`unit`), an occurrence (`unit#i`) or an
  assertion (`unit#i@snapshot`). Its key is (born, slot), where `born` is the
  generation that wrote it. Content alone can't be the key: a crashed, never
  published generation would then own a record a later generation needs, and
  insert-only writes would silently inherit an invisible record.
- A child generation writes the slots whose content changed, and a *retraction*
  (born = child) for every record it replaces or removes. Nothing is updated.
- A manifest records its parent and its whole ancestry. A reader for manifest m
  sees records born in m's ancestry and not retracted by any generation in it:
  the bitemporal pattern of Yanantin's Jabberwock aliases, with generations for
  time.
- Rollups are rewritten only for cells a correction touched. A reader takes the
  rollup from the most recent ancestor that wrote one for that cell.
- The commit is spike 2's compare-and-swap, plus: the parent must still be
  current. A publisher that loses the race rebases on the new current and
  republishes. Its orphaned writes are invisible, because no committed
  ancestry contains them.
"""

import hashlib
import json
import sys
import time
from pathlib import Path

from arango.database import StandardDatabase
from arango.exceptions import DocumentInsertError

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "plumbing2"))
import index as ix  # noqa: E402  (key, envelope, merge, cursors, _insert, errors)

BROKEN = ix.BROKEN
SPEC, ORDER, PAGE = ix.SPEC, ix.ORDER, ix.PAGE
KINDS = ("units", "occurrences", "assertions")
C = {k: f"l_{k}" for k in (*KINDS, "retractions", "rollups", "manifests", "queries")}

REGISTRY = {
    C["manifests"]: [["unique", "stream", "seq"]],
    C["units"]: [["stream", "cell", "born"]],
    C["occurrences"]: [["stream", "cell", "born"]],
    C["assertions"]: [["stream", "born", "cell", "outcome"]],
    C["retractions"]: [["stream", "born"], ["stream", "cell", "born"]],
    C["rollups"]: [["stream", "cell"]],
    C["queries"]: [["manifest", "cell"]],
}


def ensure(db: StandardDatabase) -> None:
    for name, indexes in REGISTRY.items():
        if not db.has_collection(name):
            db.create_collection(name)
        for fields in indexes:
            unique = fields[0] == "unique"
            db.collection(name).add_index({"type": "persistent", "fields": fields[unique:], "unique": unique})


def truncate(db: StandardDatabase) -> None:
    for name in REGISTRY:
        db.collection(name).truncate()


def h(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()[:32]


# --- rows -> slots ------------------------------------------------------------------

def slots(rows: list[dict], snapshot: str) -> dict[str, dict[str, dict]]:
    """kind -> slot -> content. Content is what a correction can change."""
    out = {k: {} for k in KINDS}
    for r in rows:
        out["units"][r["unit"]] = {"unit": r["unit"], "cell": r["cell"], "locator": r.get("locator")}
        for i, o in enumerate(r["occurrences"]):
            s = f"{r['unit']}#{i}"
            out["occurrences"][s] = {"unit": r["unit"], "cell": r["cell"], "index": i, "path": o["path"]}
            if o["path"] is not None:
                out["assertions"][f"{s}@{snapshot}"] = {
                    "unit": r["unit"], "cell": r["cell"], "occurrence": s, "snapshot": snapshot,
                    "target": o["target"], "outcome": o["outcome"], "target_outcome": o["target_outcome"]}
    return out


# --- reading a generation -------------------------------------------------------------

def visible(kind: str, filters: str = "") -> str:
    """AQL for the records of `kind` visible in ancestry @anc of stream @s, bound as `x`.

    A read of one cell (filters mention @cell) builds only that cell's retraction set:
    a retraction carries the cell of the record it retracts."""
    scope = ("AND r.cell IN @cells" if "@cells" in filters else
             "AND r.cell == @cell" if "@cell" in filters else "")
    return f"""
      LET gone = (FOR r IN {C['retractions']} FILTER r.stream == @s {scope} AND r.born IN @anc RETURN r.record)
      LET goneset = ZIP(gone, gone)
      FOR x IN {C[kind]} FILTER x.stream == @s {filters} AND x.born IN @anc AND NOT HAS(goneset, x._key)"""


def manifest(db: StandardDatabase, m: str) -> dict:
    doc = db.collection(C["manifests"]).get(m)
    if doc is None:
        raise ix.Unpublished(m)
    return doc


def current(db: StandardDatabase, stream: str) -> dict | None:
    return next(db.aql.execute(f"FOR x IN {C['manifests']} FILTER x.stream == @s SORT x.seq DESC LIMIT 1 RETURN x",
                               bind_vars={"s": stream}), None)


def _view(db, stream, anc) -> dict[str, dict[str, tuple[str, str]]]:
    """kind -> slot -> (record key, content hash), for a whole generation."""
    out = {}
    for kind in KINDS:
        q = visible(kind) + " RETURN [x.slot, x._key, x.h]"
        out[kind] = {s: (k, hh) for s, k, hh in db.aql.execute(q, bind_vars={"s": stream, "anc": anc},
                                                                   batch_size=50000)}
    return out


def _states(db, stream, anc, cells=None) -> dict[str, dict]:
    """Per-cell merge state over ancestry anc; `cells` limits it to those cells."""
    cf = "AND x.cell IN @cells" if cells is not None else ""
    bind = {"s": stream, "anc": anc} | ({"cells": sorted(cells)} if cells is not None else {})
    units = {c: n for c, n in db.aql.execute(visible("units", cf) + " COLLECT c = x.cell WITH COUNT INTO n RETURN [c, n]",
                                             bind_vars=bind)}
    occs = {c: n for c, n in db.aql.execute(visible("occurrences", cf) +
                                            " COLLECT c = x.cell WITH COUNT INTO n RETURN [c, n]", bind_vars=bind)}
    out = {c: {"cell": c, "units": n, "occurrences": occs.get(c, 0), "broken": 0, "members": [], "cited": []}
           for c, n in units.items()}
    for c in (cells or ()):
        out.setdefault(c, {"cell": c, "units": 0, "occurrences": 0, "broken": 0, "members": [], "cited": []})
    q = visible("assertions", cf) + """
        COLLECT c = x.cell INTO g = x
        LET bad = g[* FILTER CURRENT.outcome IN @broken]
        RETURN {c, broken: LENGTH(bad), members: SORTED_UNIQUE(bad[*].unit),
                cited: (FOR y IN g COLLECT t = y.target INTO o = y.target_outcome RETURN [t, SORTED_UNIQUE(o)])}"""
    for r in db.aql.execute(q, bind_vars=bind | {"broken": list(BROKEN)}):
        out[r["c"]] |= {"broken": r["broken"], "members": r["members"], "cited": r["cited"]}
    return out


# --- publication ------------------------------------------------------------------------

STAGES = ("records", "retractions", "rollups", "verify", "commit")
CHECKPOINT = 0.25  # retractions accumulated since the last checkpoint, as a share of the corpus


def publish(db: StandardDatabase, stream: str, snapshot: str, rows: list[dict], instance: str,
            crash_at: str | None = None, max_rebases: int = 20) -> str:
    """Publish rows as a child of the stream's current generation, writing only the delta."""
    want = slots(rows, snapshot)
    for _ in range(max_rebases):
        parent = current(db, stream)
        m = ix.key("lineage-manifest", stream, snapshot, ix.ADAPTER, h(rows), parent["_key"] if parent else None)
        if db.collection(C["manifests"]).has(m):
            return m
        if parent and parent.get("content") == h(rows):
            return parent["_key"]  # nothing changed
        try:
            return _publish_on(db, stream, snapshot, rows, want, parent, m, instance, crash_at)
        except _Rebase:
            continue
    raise RuntimeError(f"{stream}: rebased {max_rebases} times without committing")


class _Rebase(Exception):
    pass


def _publish_on(db, stream, snapshot, rows, want, parent, m, instance, crash_at) -> str:
    def stage(name):
        if crash_at == name:
            raise SystemExit(f"simulated crash after {name}")

    anc_parent = parent["ancestors"] if parent else []
    have = _view(db, stream, anc_parent) if parent else {k: {} for k in KINDS}
    size = sum(len(v) for v in want.values())
    new, gone, touched = {k: [] for k in KINDS}, [], set()
    for kind in KINDS:
        for s, content in want[kind].items():
            hh = h(content)
            old = have[kind].get(s)
            if old and old[1] == hh:
                continue  # inherited, not rewritten
            if old:
                gone.append(old[0])
            new[kind].append({"_key": ix.key(m, kind, s), "stream": stream, "born": m, "slot": s, "h": hh,
                              **content})
            touched.add(content["cell"])
        for s, (k, _) in have[kind].items():
            if s not in want[kind]:
                gone.append(k)
    gone_cell = {}
    if gone:
        # a retracted record's cell is touched too (a unit may have moved or vanished)
        for kind in KINDS:
            gone_cell |= dict(db.aql.execute(f"FOR x IN {C[kind]} FILTER x._key IN @g RETURN [x._key, x.cell]",
                                             bind_vars={"g": gone}))
        touched |= set(gone_cell.values())
    since = (parent.get("retracted_since_checkpoint", 0) if parent else 0) + len(gone)
    checkpoint = parent is not None and since > CHECKPOINT * size
    if checkpoint:
        # a fresh root: every slot written again, no ancestry, reads as fast as a full copy
        anc, gone, since = [m], [], 0
        new = {k: [{"_key": ix.key(m, k, s), "stream": stream, "born": m, "slot": s, "h": h(c), **c}
                   for s, c in want[k].items()] for k in KINDS}
        touched = {c["cell"] for c in want["units"].values()}
    else:
        anc = anc_parent + [m]
    for kind in KINDS:
        for i in range(0, len(new[kind]), 5000):
            ix._insert(db, C[kind], new[kind][i:i + 5000])
    stage("records")
    ret = [{"_key": ix.key(m, "retract", g), "stream": stream, "born": m, "record": g, "cell": gone_cell[g]}
           for g in gone]
    for i in range(0, len(ret), 5000):
        ix._insert(db, C["retractions"], ret[i:i + 5000])
    stage("retractions")
    states = _states(db, stream, anc, touched)
    ix._insert(db, C["rollups"], [{"_key": ix.key(m, "rollup", SPEC, c), "stream": stream, "born": m, "cell": c,
                                   "spec": SPEC, "state": st} for c, st in states.items()])
    stage("rollups")
    written = {k: len(v) for k, v in new.items()} | {"retractions": len(ret), "rollups": len(states)}
    stored = {}
    for kind, coll in [(k, C[k]) for k in KINDS] + [("retractions", C["retractions"]), ("rollups", C["rollups"])]:
        stored[kind] = next(db.aql.execute(f"RETURN LENGTH(FOR x IN {coll} FILTER x.born == @m RETURN 1)",
                                           bind_vars={"m": m}))
    if stored != written:
        raise RuntimeError(f"{m}: stored {stored}, wrote {written}")
    stage("verify")
    seq = (parent["seq"] + 1) if parent else 1
    try:
        db.collection(C["manifests"]).insert({
            "_key": m, "stream": stream, "snapshot": snapshot, "adapter": ix.ADAPTER, "seq": seq,
            "parent": parent["_key"] if parent else None, "ancestors": anc, "content": h(rows),
            "written": written, "touched": sorted(touched), "published_at": ix.now(),
            "checkpoint": checkpoint, "retracted_since_checkpoint": since,
            "provenance": ix.envelope(instance, f"publish {stream} at {snapshot} (delta)")})
    except DocumentInsertError as e:
        if e.error_code not in (1200, 1210):
            raise
        if db.collection(C["manifests"]).has(m):
            return m
        time.sleep(0.02)
        raise _Rebase() from e  # seq taken: our parent is no longer current
    stage("commit")
    return m


# --- published readers --------------------------------------------------------------------

def cell_states(db: StandardDatabase, m: str) -> dict[str, dict]:
    doc = manifest(db, m)
    return {c: st for c, st in _states(db, doc["stream"], doc["ancestors"]).items() if st["units"]}


def rollup(db: StandardDatabase, m: str, cell: str) -> dict:
    doc = manifest(db, m)
    r = next(db.aql.execute(f"""FOR r IN {C['rollups']} FILTER r.stream == @s AND r.cell == @cell AND r.born IN @anc
                                SORT POSITION(@anc, r.born, true) DESC LIMIT 1 RETURN r.state""",
                            bind_vars={"s": doc["stream"], "cell": cell, "anc": doc["ancestors"]}), None)
    if r is None or not r["units"]:
        raise KeyError(f"no cell {cell} in manifest {m}")
    return r


def unpaged(db: StandardDatabase, m: str, cell: str) -> list[str]:
    doc = manifest(db, m)
    return list(db.aql.execute(visible("assertions", "AND x.cell == @cell") +
                               " FILTER x.outcome IN @broken COLLECT u = x.unit SORT u RETURN u",
                               bind_vars={"s": doc["stream"], "anc": doc["ancestors"], "cell": cell,
                                          "broken": list(BROKEN)}))


def drill(db: StandardDatabase, m: str, cell: str, cursor: str | None = None, limit: int = PAGE,
          instance: str = "anonymous") -> dict:
    if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1:
        raise ValueError(f"limit must be a positive integer, got {limit!r}")
    doc = manifest(db, m)
    binding = {"spec": SPEC, "manifest": m, "cell": cell, "order": ORDER}
    after = None
    if cursor is not None:
        c = ix.decode_cursor(cursor)
        if {k: c.get(k) for k in binding} != binding:
            raise ix.CursorRejected(f"bound to {({k: c.get(k) for k in binding})}, asked for {binding}")
        after = c["after"]
    bind = {"s": doc["stream"], "anc": doc["ancestors"], "cell": cell}
    members = unpaged(db, m, cell)
    denominator = next(db.aql.execute(visible("units", "AND x.cell == @cell") + " COLLECT WITH COUNT INTO n RETURN n",
                                      bind_vars=bind), 0)
    rest = [u for u in members if after is None or u > after][:limit + 1]
    page, truncated = rest[:limit], len(rest) > limit
    db.collection(C["queries"]).insert({"at": ix.now(), "who": instance, "tool": "drill", **binding,
                                        "after": after, "limit": limit, "returned": page,
                                        "population_total": len(members), "truncated": truncated})
    return {"spec": SPEC, "manifest": m, "cell": cell, "population_total": len(members), "denominator": denominator,
            "returned": len(page), "page": page, "truncated": truncated,
            "cursor": ix.encode_cursor(binding | {"after": page[-1]}) if truncated else None}


def drill_all(db: StandardDatabase, m: str, cell: str, limit: int = PAGE) -> list[dict]:
    pages = [drill(db, m, cell, limit=limit)]
    while pages[-1]["truncated"]:
        pages.append(drill(db, m, cell, cursor=pages[-1]["cursor"], limit=limit))
    return pages
