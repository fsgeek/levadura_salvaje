"""Spike 2, brief item 4: the real corpus, resolved inside the index.

- 26 USC at 119-4 is loaded as provisions under its own manifest. Identifiers
  collide (57,176 rows, 57,161 identifiers), so a provision's key is its position
  in the release, and its locator names the identifier *and* which occurrence.
- The 2025 CFR citations are published twice, as two streams: once with the
  labels `levadura.resolve` v2 computed (imported), once resolved here against
  the loaded provisions by a resolver that shares no code with resolve.py.
  Each assertion the index resolves gets a `resolves_to` edge to every provision
  at its address: two edges where the address collides.
- `follow` dispatches on the locator's declared hash domain, and caches
  extraction by the archive's content hash, not its path or mtime.
"""

import hashlib
import json
import uuid
import xml.etree.ElementTree as ET
import zipfile
from collections import defaultdict
from functools import lru_cache
from pathlib import Path

from arango.database import StandardDatabase

import index as ix
from levadura_salvaje import usc
from levadura_salvaje.sections import sections

ROOT = Path(__file__).resolve().parents[2]
CIT = ROOT / "results/cfr-usc-citations-v2-2025.jsonl"
USC_RESULTS = ROOT / "results/usc26-provisions-{rp}.jsonl"
USC_ZIP = ROOT / "data/usc/xml_usc26@{rp}.zip"
CFR_ZIP = ROOT / "data/cfr/CFR-2025-title-26.zip"
RP = "119-4"
DASHES = str.maketrans({"–": "-", "—": "-", "‑": "-"})
USC_DOMAIN = "levadura.usc.flat_v1"      # sha256 of usc._flat(element), notes excluded
CFR_DOMAIN = "levadura.sections.flat_v1"  # sha256 of sections.py flat text


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# --- provisions ---------------------------------------------------------------

@lru_cache(maxsize=4)
def _usc_texts(zip_sha: str, zip_path: str) -> dict[tuple[str, int], str]:
    """(identifier, occurrence) -> flat text. Keyed by the archive's content hash."""
    out, seen = {}, defaultdict(int)
    with zipfile.ZipFile(zip_path) as z, z.open("usc26.xml") as f:
        for _, el in ET.iterparse(f, events=("end",)):
            ident = el.get("identifier", "")
            if el.tag not in usc.TAGS or not ident.startswith(usc.PREFIX):
                continue
            out[(ident, seen[ident])] = usc._flat(el)
            seen[ident] += 1
            if usc.TAGS[el.tag] == "section":
                el.clear()
    return out


def provision_docs(m: str, rp: str = RP) -> list[dict]:
    seen, docs = defaultdict(int), []
    for n, p in enumerate(usc.provisions(Path(str(USC_ZIP).format(rp=rp)))):
        occ = seen[p["identifier"]]
        seen[p["identifier"]] += 1
        head, *rest = p["path"].translate(DASHES).split("/")
        docs.append({"_key": ix.key(m, "provision", n), "manifest": m, "position": n,
                     "identifier": p["identifier"], "occurrence": occ,
                     "address": "/".join([head[1:], *rest]), "level": p["level"], "status": p["status"],
                     "locator": {"uri": f"usc-release:{rp}#{p['identifier']}@{occ}",
                                 "sha256": p["text_sha256"], "hash_domain": USC_DOMAIN}})
    return docs


def publish_provisions(db: StandardDatabase, instance: str, rp: str = RP) -> str:
    """Same discipline as ix.publish: data, count check, then the manifest."""
    stream, zp = "usc26", Path(str(USC_ZIP).format(rp=rp))
    m = ix.key("manifest", stream, rp, ix.ADAPTER, sha(zp))
    if db.collection("manifests").has(m):
        return m
    docs = provision_docs(m, rp)
    for i in range(0, len(docs), 5000):
        r = db.collection("provisions").import_bulk(docs[i:i + 5000], on_duplicate="replace")
        if r["errors"]:
            raise RuntimeError(f"provisions: {r['errors']} import errors")
    n = next(db.aql.execute("RETURN LENGTH(FOR p IN provisions FILTER p.manifest == @m RETURN 1)",
                            bind_vars={"m": m}))
    if n != len(docs):
        raise RuntimeError(f"provisions: stored {n}, expected {len(docs)}")
    prior = ix.current(db, stream)
    db.collection("manifests").insert({
        "_key": m, "stream": stream, "snapshot": rp, "adapter": ix.ADAPTER, "counts": {"provisions": n},
        "sources": {str(zp.relative_to(ROOT)): sha(zp)}, "seq": (prior["seq"] + 1) if prior else 1,
        "supersedes": prior["_key"] if prior else None, "published_at": ix.now(),
        "provenance": ix.envelope(instance, f"publish {stream} at {rp}")})
    return m


# --- resolution inside the index ----------------------------------------------

class IndexResolver:
    """Resolves Code paths against provisions *as loaded in the index* for manifest um.

    Rules, restated from the outcome definitions rather than from resolve.py's code:
    an address is in force if any version of it is; a section's own status wins;
    a missing section may be covered by a range element (4471...4474); below the
    section, the first missing level is absent-subdivision and a repealed level
    makes the path repealed."""

    def __init__(self, db: StandardDatabase, um: str, paths: set[str]):
        ix.published(db, um)
        addrs = set()
        for p in paths:
            parts = p.translate(DASHES).split("/")
            addrs.update("/".join(parts[:d]) for d in range(1, len(parts) + 1))
        self.rows: dict[str, list[dict]] = defaultdict(list)
        for r in db.aql.execute("""FOR a IN @addrs FOR p IN provisions FILTER p.manifest == @m AND p.address == a
                                   RETURN {address: a, key: p._key, status: p.status, position: p.position}""",
                                bind_vars={"addrs": sorted(addrs), "m": um}, batch_size=10000):
            self.rows[r["address"]].append(r)
        self.ranges = [(lo, hi, r) for r in db.aql.execute(
            """FOR p IN provisions FILTER p.manifest == @m AND CONTAINS(p.address, "...")
               RETURN {address: p.address, key: p._key, status: p.status}""", bind_vars={"m": um})
            for lo, hi in [[_seckey(x) for x in r["address"].split("...")]] if lo and hi]

    def status(self, address: str) -> tuple[bool, str | None]:
        rows = self.rows.get(address)
        if not rows:
            return False, None
        if any(r["status"] is None for r in rows):
            return True, None
        return True, min(rows, key=lambda r: r["position"])["status"]

    def resolve(self, path: str) -> dict:
        sec, *subs = path.translate(DASHES).split("/")
        found, st = self.status(sec)
        if not found:
            k = _seckey(sec)
            for lo, hi, r in self.ranges:
                if k and lo <= k <= hi:
                    return {"outcome": r["status"] or "absent-section", "targets": [r["key"]]}
            return {"outcome": "absent-section", "targets": []}
        if st:
            return {"outcome": st, "targets": [r["key"] for r in self.rows[sec]]}
        for d in range(1, len(subs) + 1):
            a = "/".join([sec, *subs[:d]])
            found, st = self.status(a)
            if not found:
                return {"outcome": "absent-subdivision", "targets": []}
            if st == "repealed":
                return {"outcome": "repealed", "targets": [r["key"] for r in self.rows[a]]}
        a = "/".join([sec, *subs])
        return {"outcome": "resolves", "targets": [r["key"] for r in self.rows[a]]}


def _seckey(no: str):
    import re
    m = re.match(r"^(\d+)([A-Z]*)(?:-(\d+))?$", no)
    return (int(m.group(1)), m.group(2), int(m.group(3) or 0)) if m else None


# --- the CFR, twice -------------------------------------------------------------

def cfr_rows(resolver: IndexResolver | None = None) -> tuple[list[dict], dict[tuple[str, int], list[str]]]:
    """Rows for ix.publish. Without a resolver, outcomes are resolve.py's stored labels."""
    rows, targets = [], {}
    for line in CIT.read_text().splitlines():
        r = json.loads(line)
        uid = f"cfr26-2025:{r['volume_file']}:{r['ordinal']}"
        occs = []
        for i, c in enumerate(r["citations"]):
            if c["path"] is None:
                occs.append({"path": None, "target": None, "outcome": None, "target_outcome": None})
                continue
            sec = c["path"].split("/")[0]
            if resolver:
                got = resolver.resolve(c["path"])
                outcome, target_outcome = got["outcome"], resolver.resolve(sec)["outcome"]
                targets[(uid, i)] = got["targets"]
            else:
                outcome, target_outcome = c["outcome"][RP]["outcome"], c["section_outcome"][RP]
            occs.append({"path": c["path"], "target": sec, "outcome": outcome, "target_outcome": target_outcome})
        rows.append({"unit": uid, "cell": r["sectno"].split(".")[0], "occurrences": occs,
                     "locator": {"uri": f"zip://{CFR_ZIP.relative_to(ROOT)}#{r['volume_file']}:{r['ordinal']}",
                                 "sha256": r["sha256"], "hash_domain": CFR_DOMAIN}})
    return rows, targets


def edge_writer(db: StandardDatabase, targets: dict, instance: str):
    def write(m: str) -> dict:
        env, edges = ix.envelope(instance, "levadura.plumbing2 index resolver"), []
        for (uid, i), keys in targets.items():
            a = ix.key(ix.key(m, uid, i), RP)
            for k in keys:
                ek = ix.key("resolves_to", a, k)
                edges.append({"_key": ek, "_from": f"assertions/{a}", "_to": f"provisions/{k}",
                              "id": str(uuid.UUID(ek)), "created_at": ix.now(), "provenance": env,
                              "manifest": m, "fanout": len(keys)})
        for j in range(0, len(edges), 5000):
            r = db.collection("resolves_to").import_bulk(edges[j:j + 5000], on_duplicate="replace")
            if r["errors"]:
                raise RuntimeError(f"resolves_to: {r['errors']} import errors")
        return {"resolves_to": len(edges)}
    return write


# --- following locators -----------------------------------------------------------

def follow(locator: dict) -> dict:
    handler = {USC_DOMAIN: _follow_usc, CFR_DOMAIN: _follow_cfr}.get(locator.get("hash_domain"))
    if handler is None:
        return {"status": "unknown-domain", "hash_domain": locator.get("hash_domain")}
    return handler(locator)


def _check(locator: dict, text: str | None) -> dict:
    if text is None:
        return {"status": "unreachable", "uri": locator["uri"]}
    got = hashlib.sha256(text.encode()).hexdigest()
    if got != locator["sha256"]:
        return {"status": "stale", "uri": locator["uri"], "found_sha256": got}
    return {"status": "ok", "text": text}


def _follow_usc(locator: dict) -> dict:
    rest = locator["uri"].removeprefix("usc-release:")
    rp, target = rest.split("#", 1)
    ident, occ = target.rsplit("@", 1)
    zp = Path(str(USC_ZIP).format(rp=rp))
    if not zp.exists():
        return _check(locator, None)
    return _check(locator, _usc_texts(sha(zp), str(zp)).get((ident, int(occ))))


@lru_cache(maxsize=2)
def _cfr_texts(zip_sha: str, zip_path: str) -> dict:
    return {(s["volume_file"], s["ordinal"]): s["text"] for s in sections(Path(zip_path))}


def _follow_cfr(locator: dict) -> dict:
    path, frag = locator["uri"].removeprefix("zip://").split("#")
    volume, ordinal = frag.rsplit(":", 1)
    zp = ROOT / path
    if not zp.exists():
        return _check(locator, None)
    return _check(locator, _cfr_texts(sha(zp), str(zp)).get((volume, int(ordinal))))
