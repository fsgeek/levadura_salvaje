"""Plumbing spike 1 (docs/plumbing-design.md, "After review 2"). Throwaway.

One vertical through every layer, for finding #1's numbers at USC 119-4:
occurrences with stable identity -> reified resolutions -> rollups by part
with per-metric merge state -> drill with keyset paging -> follow a locator
to hash-checked text. ArangoDB is the index; text stays in the CFR zip.

Hash domain: `sections.py` flat text (sha256 on file as `sha256`).
Span domain: character offsets into `citations.normalize(flat text)`.
"""

import hashlib
import json
import subprocess
import uuid
import zipfile
from collections import Counter
from functools import lru_cache
from pathlib import Path

from arango import ArangoClient

from levadura_salvaje import citations
from levadura_salvaje.sections import sections

ROOT = Path(__file__).resolve().parents[2]
CIT = ROOT / "results/cfr-usc-citations-v2-2025.jsonl"
USC = ROOT / "results/usc26-provisions-119-4.jsonl"
ZIP = ROOT / "data/cfr/CFR-2025-title-26.zip"
RP = "119-4"
BROKEN = {"repealed", "absent-section", "absent-subdivision"}
NS = uuid.UUID("6f1c2a52-5b0e-4f9e-9a57-3c1d0f5b2e11")
DB = "levadura_spike1"
PAGE = 40


def key(*parts) -> str:
    return str(uuid.uuid5(NS, "|".join(map(str, parts))))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def db():
    env = subprocess.run(["docker", "inspect", "arango-vector-sandbox", "--format",
                          "{{range .Config.Env}}{{println .}}{{end}}"], capture_output=True, text=True).stdout
    pw = next(line.split("=", 1)[1] for line in env.splitlines() if line.startswith("ARANGO_ROOT_PASSWORD="))
    client = ArangoClient(hosts="http://localhost:8530")
    sys_db = client.db("_system", username="root", password=pw)
    if not sys_db.has_database(DB):
        sys_db.create_database(DB)
    return client.db(DB, username="root", password=pw)


# --- load ---------------------------------------------------------------------

def manifest() -> dict:
    return {"_key": key("manifest", sha(CIT), sha(USC), "adapter-v1"),
            "sources": {str(CIT.relative_to(ROOT)): sha(CIT), str(USC.relative_to(ROOT)): sha(USC)},
            "adapter": "spikes/plumbing1 v1", "snapshot": RP}


def load(d) -> dict:
    """Idempotent: deterministic keys, overwrite=True on identical documents."""
    for c in ("manifests", "sections", "citations", "resolutions", "provisions", "rollups"):
        if not d.has_collection(c):
            d.create_collection(c)
    m = manifest()
    d.collection("manifests").insert(m, overwrite=True)
    rows = [json.loads(line) for line in CIT.read_text().splitlines()]
    text = {(s["volume_file"], s["ordinal"]): s for s in sections(ZIP)}
    secs, cits, ress, mismatches = [], [], [], 0
    for r in rows:
        sk = key("cfr2025", r["volume_file"], r["ordinal"])
        part = r["sectno"].split(".")[0]
        secs.append({"_key": sk, "sectno": r["sectno"], "part": part, "edition": "cfr26-2025",
                     "locator": {"uri": f"zip://{ZIP.relative_to(ROOT)}#{r['volume_file']}:{r['ordinal']}",
                                 "sha256": r["sha256"], "hash_domain": "levadura.sections.flat_v1"}})
        # identity check: the stored list must be what the extractor produces now. Re-extraction
        # also recovers `group`, which the stored file dropped: a continuation's span is only its
        # designator ("(3)"), and the group links it to its head ("section 509(a)").
        s = text[(r["volume_file"], r["ordinal"])]
        again = citations.extract(s["text"], part=part, reg_id=s["sectno"])
        if [(c["path"], list(c["span"])) for c in again] != [(c["path"], list(c["span"])) for c in r["citations"]]:
            mismatches += 1
            again = [{"group": None}] * len(r["citations"])
        for i, c in enumerate(r["citations"]):
            ck = key(sk, i)
            cits.append({"_key": ck, "section": sk, "cite_index": i, "part": part, "path": c["path"],
                         "span": c["span"], "span_domain": "levadura.citations.normalize_v2",
                         "head": c["head"], "group": again[i]["group"], "flags": c["flags"], "range": c["range"]})
            if c["path"] is None:
                continue  # an unresolvable occurrence: kept as a citation, no resolution asserted
            o = c["outcome"][RP]
            ress.append({"_key": key(ck, RP, "resolver-v2"), "citation": ck, "section": sk, "part": part,
                         "snapshot": RP, "resolver": "levadura.resolve v2", "requested": c["path"],
                         "code_section": c["path"].split("/")[0],
                         "outcome": o["outcome"], "detail": o, "section_outcome": c["section_outcome"][RP],
                         "manifest": m["_key"]})
    provs = []
    for i, line in enumerate(USC.read_text().splitlines()):
        p = json.loads(line)
        provs.append({"_key": key("usc", RP, i), "identifier": p["identifier"], "path": p["path"],
                      "level": p["level"], "status": p["status"], "line": i,
                      "locator": {"uri": f"usc-release:{RP}#{p['identifier']}", "sha256": p["text_sha256"],
                                  "hash_domain": "levadura.usc.flat_v1"}})
    for name, docs in (("sections", secs), ("citations", cits), ("resolutions", ress), ("provisions", provs)):
        for i in range(0, len(docs), 5000):
            d.collection(name).import_bulk(docs[i:i + 5000], on_duplicate="replace")
    for c, fields in (("citations", ["section"]), ("resolutions", ["part"]), ("resolutions", ["outcome"]),
                      ("provisions", ["identifier"]), ("sections", ["part"])):
        d.collection(c).add_persistent_index(fields)
    return {"sections": len(secs), "citations": len(cits), "resolutions": len(ress),
            "provisions": len(provs), "reextract_mismatches": mismatches, "manifest": m["_key"]}


# --- rollups with merge state -------------------------------------------------

SPECS = {
    # grain: citation occurrence; additive
    "broken_occurrences": "exact count of resolutions with outcome in BROKEN over all citation occurrences",
    # grain: section; merge = set union (sections partition by part, so union == sum here)
    "fossil_sections": "set of section keys with >= 1 broken resolution",
    # grain: distinct Code section; merge = union of {code_section: outcome}; NOT additive across parts
    "cited_code_sections": "map code_section -> section_outcome over all resolutions",
}


def part_states(d, m: str) -> dict:
    q = """
    FOR s IN sections
      COLLECT part = s.part INTO g
      LET keys = g[*].s._key
      LET occ = LENGTH(FOR c IN citations FILTER c.section IN keys RETURN 1)
      LET res = (FOR r IN resolutions FILTER r.part == part AND r.manifest == @m RETURN r)
      RETURN {part, sections: LENGTH(keys), occurrences: occ,
              broken: LENGTH(res[* FILTER CURRENT.outcome IN @broken]),
              fossil: UNIQUE(res[* FILTER CURRENT.outcome IN @broken].section),
              cited: MERGE(FOR r IN res RETURN {[r.code_section]: r.section_outcome})}
    """
    return {r["part"]: r for r in d.aql.execute(q, bind_vars={"m": m, "broken": sorted(BROKEN)})}


def materialize(d, m: str) -> dict:
    states = part_states(d, m)
    for part, st in states.items():
        d.collection("rollups").insert({"_key": key("rollup", m, "part", part), "manifest": m, "level": "part",
                                        "cell": part, "state": st}, overwrite=True)
    top = {"sections": sum(s["sections"] for s in states.values()),
           "occurrences": sum(s["occurrences"] for s in states.values()),
           "broken": sum(s["broken"] for s in states.values()),
           "fossil": set().union(*(s["fossil"] for s in states.values())),
           "cited": {}}
    for s in states.values():
        top["cited"].update(s["cited"])
    naive_cited_sum = sum(len(s["cited"]) for s in states.values())
    return {"broken_occurrences": [top["broken"], top["occurrences"]],
            "fossil_sections": [len(top["fossil"]), top["sections"]],
            "cited_code_sections": len(top["cited"]),
            "cited_by_outcome": dict(Counter(top["cited"].values())),
            "naive_sum_of_part_distinct_counts": naive_cited_sum,
            "parts": len(states)}


# --- tools -------------------------------------------------------------------

def drill(d, m: str, part: str, after: str | None = None, limit: int = PAGE) -> dict:
    """Members of the fossil_sections cell for one part, keyset-paged by section key."""
    q = """
    LET members = UNIQUE(FOR r IN resolutions FILTER r.manifest == @m AND r.part == @part
                         AND r.outcome IN @broken RETURN r.section)
    LET sorted = (FOR k IN members SORT k RETURN k)
    RETURN {total: LENGTH(sorted),
            page: (FOR k IN sorted FILTER @after == null OR k > @after LIMIT @limit RETURN k)}
    """
    r = next(d.aql.execute(q, bind_vars={"m": m, "part": part, "broken": sorted(BROKEN),
                                         "after": after, "limit": limit}))
    return {"population_total": r["total"], "returned": len(r["page"]), "page": r["page"],
            "truncated": len(r["page"]) == limit,
            "cursor": {"spec": "fossil_sections", "manifest": m, "cell": part,
                       "order": "section_key", "after": r["page"][-1] if r["page"] else after}}


@lru_cache(maxsize=4)
def _extracted(path: str, mtime_ns: int, size: int) -> dict:
    """Extraction cache, keyed by the file's identity on disk (review 2 #9)."""
    return {(s["volume_file"], s["ordinal"]): s for s in sections(Path(path))}


def follow(locator: dict) -> dict:
    """Bytes behind a CFR section locator, re-hashed in its declared domain."""
    uri = locator["uri"]
    assert uri.startswith("zip://")
    path, frag = uri[len("zip://"):].split("#")
    volume, ordinal = frag.rsplit(":", 1)
    zp = ROOT / path
    if not zp.exists():
        return {"status": "unreachable", "uri": uri}
    try:
        with zipfile.ZipFile(zp) as z:
            if volume not in z.namelist():
                return {"status": "unreachable", "uri": uri}
    except zipfile.BadZipFile:
        return {"status": "unreachable", "uri": uri}
    st = zp.stat()
    s = _extracted(str(zp), st.st_mtime_ns, st.st_size).get((volume, int(ordinal)))
    if s is None:
        return {"status": "unreachable", "uri": uri}
    if s["sha256"] != locator["sha256"]:
        return {"status": "stale", "uri": uri, "found_sha256": s["sha256"]}
    return {"status": "ok", "text": s["text"]}


def span_text(d, citation_key: str) -> dict:
    c = d.collection("citations").get(citation_key)
    s = d.collection("sections").get(c["section"])
    got = follow(s["locator"])
    if got["status"] != "ok":
        return got
    norm = citations.normalize(got["text"])
    a, b = c["span"]
    group = list(d.aql.execute("FOR x IN citations FILTER x.section == @s AND x.group == @g RETURN x.span",
                               bind_vars={"s": c["section"], "g": c["group"]})) if c["group"] is not None else [[a, b]]
    ga = min(x[0] for x in group)
    return {"status": "ok", "path": c["path"], "head": c["head"], "span": [a, b], "text": norm[a:b],
            "group_text": norm[ga:b], "context": norm[max(0, ga - 60):b + 60]}
