"""Plumbing spike 2: correctness under change (spikes/SPIKE2-BRIEF.md). Throwaway.

Corpus-neutral names: a *unit* (a CFR section) sits in one *cell* (a CFR part) and
holds *occurrences* (citations). An *assertion* records what one occurrence
resolved to at one snapshot: its own `outcome`, the `target` it names (a Code
section) and the target's `target_outcome`.

What spike 1 got wrong and this one tests (spikes/plumbing1/REVIEW.md):
- every record is keyed by its manifest, so a corrected import adds a generation
  instead of overwriting one, and denominators are pinned with the members;
- publication is atomic: data, then rollups, then a count check, then the
  manifest document. A manifest that doesn't exist is unpublished, and nothing
  answers for it;
- merge state keeps every outcome per target, and conflicts are reported, never
  collapsed; merges are unions and sums, so order can't matter;
- paging fetches limit + 1, reports totals on every page, and its cursors are
  signed and bound to (spec, manifest, cell, order);
- every drill page is recorded as a query event (Yanantin's reply: record the
  event, derive `visited` edges from it).

The tenant is our own database (src/levadura_salvaje/tenant.py); `ensure` below
is the only code that creates collections or indexes.
"""

import base64
import hashlib
import hmac
import json
import uuid
from datetime import datetime, timezone

from arango.database import StandardDatabase
from tiksi.provenance import ProvenanceEnvelope, SourceIdentifier

from levadura_salvaje.tenant import settings

NS = uuid.UUID("0b8a7f3e-2c61-4d0a-9f1e-5a4c3b2d1e0f")
BROKEN = ("absent-section", "absent-subdivision", "repealed")
SPEC = "fossil_units"
ORDER = "unit"
PAGE = 40
ADAPTER = "spikes/plumbing2 v1"

# The registry: the one place that owns collections and indexes (Yanantin's Khipu.watay).
REGISTRY = {
    "manifests": ("document", [["stream", "seq"]]),
    "units": ("document", [["manifest", "cell"]]),
    "occurrences": ("document", [["manifest", "cell"]]),
    "assertions": ("document", [["manifest", "cell", "outcome"], ["manifest", "unit"]]),
    "rollups": ("document", [["manifest"]]),
    "queries": ("document", [["manifest", "cell"]]),
}


class Unpublished(LookupError):
    """The manifest has no published document; nothing answers for it."""


class CursorRejected(ValueError):
    """The cursor is forged, malformed, or bound to a different query."""


class MergeConflict(ValueError):
    """Cell states can't be merged without losing information."""


def key(*parts) -> str:
    return str(uuid.uuid5(NS, "|".join(map(str, parts))))


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def envelope(instance: str, description: str) -> dict:
    return ProvenanceEnvelope(source=SourceIdentifier(identifier=uuid.uuid5(NS, ADAPTER), description=description),
                              author_model_family="claude-opus-5-5", author_instance_id=instance,
                              interface_version="levadura.plumbing2.v1").model_dump(mode="json")


def ensure(db: StandardDatabase) -> None:
    for name, (kind, indexes) in REGISTRY.items():
        if not db.has_collection(name):
            db.create_collection(name, edge=kind == "edge")
        for fields in indexes:
            db.collection(name).add_index({"type": "persistent", "fields": fields})


def truncate(db: StandardDatabase) -> None:
    for name in REGISTRY:
        db.collection(name).truncate()


# --- publication --------------------------------------------------------------

def manifest_id(stream: str, snapshot: str, rows: list[dict]) -> str:
    """Content-derived: the same rows under the same adapter are the same manifest."""
    digest = hashlib.sha256(json.dumps(rows, sort_keys=True).encode()).hexdigest()
    return key("manifest", stream, snapshot, ADAPTER, digest)


def documents(m: str, snapshot: str, rows: list[dict]) -> dict[str, list[dict]]:
    units, occs, asserts = [], [], []
    for r in rows:
        units.append({"_key": key(m, r["unit"]), "manifest": m, "unit": r["unit"], "cell": r["cell"],
                      "locator": r.get("locator")})
        for i, o in enumerate(r["occurrences"]):
            ok = key(m, r["unit"], i)
            occs.append({"_key": ok, "manifest": m, "unit": r["unit"], "cell": r["cell"], "index": i,
                         "path": o["path"]})
            if o["path"] is None:
                continue  # unresolvable: an occurrence with no assertion
            asserts.append({"_key": key(ok, snapshot), "manifest": m, "occurrence": ok, "unit": r["unit"],
                            "cell": r["cell"], "snapshot": snapshot, "target": o["target"],
                            "outcome": o["outcome"], "target_outcome": o["target_outcome"]})
    return {"units": units, "occurrences": occs, "assertions": asserts}


def cell_states(db: StandardDatabase, m: str) -> dict[str, dict]:
    """Per-cell merge state for manifest m, read from the assertions themselves."""
    q = """
    FOR u IN units FILTER u.manifest == @m
      COLLECT cell = u.cell WITH COUNT INTO n
      LET a = (FOR x IN assertions FILTER x.manifest == @m AND x.cell == cell RETURN x)
      LET bad = a[* FILTER CURRENT.outcome IN @broken]
      RETURN {cell, units: n,
              occurrences: LENGTH(FOR o IN occurrences FILTER o.manifest == @m AND o.cell == cell RETURN 1),
              broken: LENGTH(bad),
              members: SORTED_UNIQUE(bad[*].unit),
              cited: (FOR x IN a COLLECT t = x.target INTO g = x.target_outcome
                      RETURN [t, SORTED_UNIQUE(g)])}
    """
    return {r["cell"]: r for r in db.aql.execute(q, bind_vars={"m": m, "broken": list(BROKEN)})}


def merge(states: list[dict]) -> dict:
    """Unions and sums only, so any order gives the same answer. A unit claimed by two
    cells is refused; a target with several outcomes is kept and reported."""
    owner: dict[str, str] = {}
    cited: dict[str, set[str]] = {}
    total = {"units": 0, "occurrences": 0, "broken": 0}
    for s in states:
        for k in total:
            total[k] += s[k]
        for u in s["members"]:
            if owner.setdefault(u, s["cell"]) != s["cell"]:
                raise MergeConflict(f"unit {u} is a member of {owner[u]} and {s['cell']}")
        for t, outcomes in s["cited"]:
            cited.setdefault(t, set()).update(outcomes)
    return {**total, "members": sorted(owner), "cited": {t: sorted(o) for t, o in sorted(cited.items())},
            "conflicts": sorted(t for t, o in cited.items() if len(o) > 1)}


def publish(db: StandardDatabase, stream: str, snapshot: str, rows: list[dict], instance: str,
            fail_before_manifest: bool = False) -> str:
    """Data first, the manifest last. Idempotent, and safe to retry after a crash."""
    m = manifest_id(stream, snapshot, rows)
    if db.collection("manifests").has(m):
        return m
    docs = documents(m, snapshot, rows)
    for name, batch in docs.items():
        for i in range(0, len(batch), 5000):
            r = db.collection(name).import_bulk(batch[i:i + 5000], on_duplicate="replace")
            if r["errors"]:
                raise RuntimeError(f"{name}: {r['errors']} import errors")
    states = cell_states(db, m)
    for cell, st in states.items():
        db.collection("rollups").insert({"_key": key("rollup", SPEC, m, cell), "manifest": m, "spec": SPEC,
                                         "cell": cell, "state": st}, overwrite=True)
    counts = next(db.aql.execute("""
        RETURN {units: LENGTH(FOR x IN units FILTER x.manifest == @m RETURN 1),
                occurrences: LENGTH(FOR x IN occurrences FILTER x.manifest == @m RETURN 1),
                assertions: LENGTH(FOR x IN assertions FILTER x.manifest == @m RETURN 1),
                rollups: LENGTH(FOR x IN rollups FILTER x.manifest == @m RETURN 1)}""", bind_vars={"m": m}))
    want = {k: len(v) for k, v in docs.items()} | {"rollups": len({r["cell"] for r in rows})}
    if counts != want:
        raise RuntimeError(f"manifest {m}: stored {counts}, expected {want}")
    if fail_before_manifest:
        raise SystemExit("simulated crash between data and manifest")
    prior = current(db, stream)
    db.collection("manifests").insert({
        "_key": m, "stream": stream, "snapshot": snapshot, "adapter": ADAPTER, "counts": counts,
        "seq": (prior["seq"] + 1) if prior else 1, "supersedes": prior["_key"] if prior else None,
        "published_at": now(), "provenance": envelope(instance, f"publish {stream} at {snapshot}")})
    return m


def current(db: StandardDatabase, stream: str) -> dict | None:
    """Selection rule: the published manifest with the highest seq in its stream."""
    return next(db.aql.execute("FOR x IN manifests FILTER x.stream == @s SORT x.seq DESC LIMIT 1 RETURN x",
                               bind_vars={"s": stream}), None)


def published(db: StandardDatabase, m: str) -> dict:
    doc = db.collection("manifests").get(m)
    if doc is None:
        raise Unpublished(m)
    return doc


# --- reading -----------------------------------------------------------------

def rollup(db: StandardDatabase, m: str, cell: str) -> dict:
    published(db, m)
    r = db.collection("rollups").get(key("rollup", SPEC, m, cell))
    if r is None:
        raise KeyError(f"no cell {cell} in manifest {m}")
    return r["state"]


def _secret() -> bytes:
    return bytes.fromhex(settings()["cursor_secret"])


def encode_cursor(binding: dict) -> str:
    body = base64.urlsafe_b64encode(json.dumps(binding, sort_keys=True).encode()).decode()
    return body + "." + hmac.new(_secret(), body.encode(), "sha256").hexdigest()


def decode_cursor(token: str) -> dict:
    try:
        body, sig = token.rsplit(".", 1)
        if not hmac.compare_digest(sig, hmac.new(_secret(), body.encode(), "sha256").hexdigest()):
            raise CursorRejected("signature")
        return json.loads(base64.urlsafe_b64decode(body))
    except (ValueError, json.JSONDecodeError) as e:
        if isinstance(e, CursorRejected):
            raise
        raise CursorRejected(f"malformed: {e}") from e


def drill(db: StandardDatabase, m: str, cell: str, cursor: str | None = None, limit: int = PAGE,
          instance: str = "anonymous") -> dict:
    """One page of the members of (fossil_units, m, cell), ordered by unit id."""
    published(db, m)
    binding = {"spec": SPEC, "manifest": m, "cell": cell, "order": ORDER}
    after = None
    if cursor is not None:
        c = decode_cursor(cursor)
        if {k: c.get(k) for k in binding} != binding:
            raise CursorRejected(f"bound to {({k: c.get(k) for k in binding})}, asked for {binding}")
        after = c["after"]
    r = next(db.aql.execute("""
        LET members = (FOR x IN assertions FILTER x.manifest == @m AND x.cell == @cell
                       AND x.outcome IN @broken RETURN DISTINCT x.unit)
        RETURN {total: LENGTH(members),
                units: LENGTH(FOR u IN units FILTER u.manifest == @m AND u.cell == @cell RETURN 1),
                page: (FOR u IN members FILTER @after == null OR u > @after SORT u LIMIT @n RETURN u)}""",
                             bind_vars={"m": m, "cell": cell, "broken": list(BROKEN), "after": after,
                                        "n": limit + 1}))
    page, truncated = r["page"][:limit], len(r["page"]) > limit
    out = {"spec": SPEC, "manifest": m, "cell": cell, "population_total": r["total"],
           "denominator": r["units"], "returned": len(page), "page": page, "truncated": truncated,
           "cursor": encode_cursor(binding | {"after": page[-1]}) if truncated else None}
    db.collection("queries").insert({"at": now(), "who": instance, "tool": "drill", **binding,
                                     "after": after, "limit": limit, "returned": page,
                                     "population_total": r["total"], "truncated": truncated})
    return out


def drill_all(db: StandardDatabase, m: str, cell: str, limit: int = PAGE) -> list[dict]:
    pages = [drill(db, m, cell, limit=limit)]
    while pages[-1]["truncated"]:
        pages.append(drill(db, m, cell, cursor=pages[-1]["cursor"], limit=limit))
    return pages


def unpaged(db: StandardDatabase, m: str, cell: str) -> list[str]:
    published(db, m)
    return list(db.aql.execute("""
        FOR x IN assertions FILTER x.manifest == @m AND x.cell == @cell AND x.outcome IN @broken
          COLLECT u = x.unit SORT u RETURN u""", bind_vars={"m": m, "cell": cell, "broken": list(BROKEN)}))
