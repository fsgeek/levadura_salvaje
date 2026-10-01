"""Surface spike 1: a thin tool surface over spike 2's index, for a caller who has a question.

Throwaway. The handoff of 2026-10-01 asked for this before any more storage work:
give the index to someone with a real question and watch whether they move between
scales. Every call returns bounded JSON (aggregation before pagination, totals on
every page), and every call is recorded in `queries` as a footprint, with `who`.

The tools, from the population down to the words:
- `overview()`: what is here, what the numbers mean, and one row per cell (CFR part);
- `cell(cell)`: one cell's numbers and the Code sections its broken citations name most;
- `drill(cell)`: the units (CFR sections) behind a cell's number, paged;
- `cited_by(target)`: the other direction: who cites one Code section, by cell;
- `unit(unit)`: one section's citations and what each resolved to, paged;
- `cite(unit, index)`: the sentence around one citation, and the provisions it resolves to;
- `follow(kind, id)`: the text itself, hash-checked, in slices.

The surface never hands out the database handle, and it reads only published manifests.
"""

import hashlib
import io
import json
import re
import sys
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "plumbing2"))
import corpus as cx  # noqa: E402
import index as ix  # noqa: E402

from levadura_salvaje.citations import normalize  # noqa: E402
from levadura_salvaje.sections import sections  # noqa: E402
from levadura_salvaje.tenant import connect  # noqa: E402

STREAM = "cfr26-2025@119-4/index"
USC_STREAM = "usc26"
CONTEXT = 160   # characters either side of a citation in `cite`
SLICE = 4000    # default characters per `follow` call
MAX_LIMIT = 200
# The citations sidecar supplies spans and heads, which the index doesn't store. Pinned to the file the
# index was built from (spike 2 published from it at e8691cc); a different file is refused (review 1, #1).
SIDECAR_SHA256 = "8c8d2c257f79c26355e651d899c4a932bb0927646ef99f4ca68d1742a39308c9"

ABOUT = {
    "corpus": "Title 26 of the Code of Federal Regulations (Treasury tax regulations), 2025 edition, "
              "read against Title 26 of the US Code (the Internal Revenue Code) at release 119-4.",
    "unit": "one CFR section in the 2025 edition, identified by its position (volume file, ordinal); "
            "`sectno` is its printed number, e.g. 1.61-1",
    "cell": "a CFR part: the number before the dot in sectno (part 1 holds most income tax regulations)",
    "occurrence": "one citation of the Code inside a CFR section, e.g. 'section 871(b)'",
    "outcome": "what the cited Code path resolved to at release 119-4: resolves, repealed, "
               "absent-section (no such section), absent-subdivision (the section exists, the "
               "cited subsection doesn't), renumbered, or others; computed by a resolver, not by a lawyer",
    "broken": "an occurrence whose outcome is repealed, absent-section or absent-subdivision",
    "member": "a unit with at least one broken occurrence; a cell's `members` count these units",
    "caution": "Broken is a mechanical finding about the citation's address. Many regulations cite "
               "pre-1986 numbering or provisions that were later renumbered; a broken citation is a "
               "lead, not a conclusion. The converse holds too: `resolves` means only that the address "
               "exists today. Section numbers are reused, so a citation can resolve to a different provision "
               "than the one the regulation was written against. Only 2025 is loaded; there is no history "
               "here yet.",
}


class Surface:
    def __init__(self, who: str, tier: str = "app"):
        self.who = who
        self._db = connect(tier)
        cur = ix.current(self._db, STREAM)
        if cur is None:
            raise ix.Unpublished(STREAM)
        self.m = cur["_key"]
        # The USC generation this index was resolved against, not the stream's latest (review 1, #2).
        deps = [d for d in cur["depends_on"] if ix.published(self._db, d)["stream"] == USC_STREAM]
        if len(deps) != 1:
            raise LookupError(f"{self.m}: expected one {USC_STREAM} dependency, found {deps}")
        self.um = deps[0]

    # --- footprints ------------------------------------------------------------

    def _log(self, tool: str, args: dict, result: dict) -> dict:
        self._db.collection("queries").insert({
            "at": ix.now(), "who": self.who, "tool": tool, "manifest": self.m, "args": args,
            "population_total": result.get("population_total"), "returned": result.get("returned"),
            "truncated": result.get("truncated")})
        return result

    def failed(self, tool: str, args: dict, error: str) -> None:
        """Failed calls are footprints too (review 1, #8)."""
        self._db.collection("queries").insert({"at": ix.now(), "who": self.who, "tool": tool,
                                               "manifest": self.m, "args": args, "error": error})

    def _q(self, aql: str, **bind) -> list:
        return list(self._db.aql.execute(aql, bind_vars=bind, batch_size=10000))

    # --- the population ---------------------------------------------------------

    def overview(self) -> dict:
        rows = self._q("""FOR r IN rollups FILTER r.manifest == @m AND r.spec == @spec
                          RETURN {cell: r.cell, units: r.state.units, members: LENGTH(r.state.members),
                                  occurrences: r.state.occurrences, broken: r.state.broken}""",
                       m=self.m, spec=ix.SPEC)
        rows.sort(key=lambda r: _cellkey(r["cell"]))
        for r in rows:
            r["member_share"] = round(r["members"] / r["units"], 3) if r["units"] else None
        total = {k: sum(r[k] for r in rows) for k in ("units", "members", "occurrences", "broken")}
        total["member_share"] = round(total["members"] / total["units"], 3)
        return self._log("overview", {}, {
            "about": ABOUT, "manifest": self.m, "spec": ix.SPEC, "totals": total,
            "cells": rows, "population_total": len(rows), "returned": len(rows), "truncated": False})

    def cell(self, cell: str, top: int = 15, cursor: int = 0) -> dict:
        top, cursor = _limit(top), _offset(cursor)
        st = ix.rollup(self._db, self.m, cell)
        groups = self._q("""FOR x IN assertions FILTER x.manifest == @m AND x.cell == @cell
                              AND x.outcome IN @broken
                            COLLECT target = x.target, outcome = x.outcome INTO g = x.unit
                            LET n = LENGTH(g)
                            SORT n DESC, target
                            RETURN {target, outcome, citations: n, units: LENGTH(UNIQUE(g))}""",
                         m=self.m, cell=cell, broken=list(ix.BROKEN))
        outcomes = self._q("""FOR x IN assertions FILTER x.manifest == @m AND x.cell == @cell
                              COLLECT o = x.outcome WITH COUNT INTO n SORT n DESC RETURN {outcome: o, n}""",
                           m=self.m, cell=cell)
        return self._log("cell", {"cell": cell, "top": top, "cursor": cursor}, {
            "cell": cell, "units": st["units"], "members": len(st["members"]),
            "occurrences": st["occurrences"], "broken": st["broken"], "outcomes": outcomes,
            "broken_targets": groups[cursor:cursor + top], "population_total": len(groups),
            "returned": len(groups[cursor:cursor + top]), "truncated": cursor + top < len(groups),
            "cursor": cursor + top if cursor + top < len(groups) else None, "grain": "(cited Code section, outcome) pairs among broken citations"})

    def drill(self, cell: str, cursor: str | None = None, limit: int = 40) -> dict:
        page = ix.drill(self._db, self.m, cell, cursor=cursor, limit=_limit(limit), instance=self.who)
        page["page"] = [_describe(u) for u in page["page"]]
        return page

    def cited_by(self, target: str, cursor: int = 0, limit: int = 40) -> dict:
        """Every citation of one Code section (its number, e.g. '1201'), by cell and outcome, then units."""
        limit, cursor = _limit(limit), _offset(cursor)
        rows = self._q("""FOR x IN assertions FILTER x.manifest == @m AND x.target == @t
                          COLLECT unit = x.unit, cell = x.cell INTO g = x.outcome
                          SORT unit RETURN {unit, cell, outcomes: g}""", m=self.m, t=target)
        by_cell: dict[str, dict] = {}
        for r in rows:
            c = by_cell.setdefault(r["cell"], {"cell": r["cell"], "units": 0, "citations": 0})
            c["units"] += 1
            c["citations"] += len(r["outcomes"])
        outcomes: dict[str, int] = {}
        for r in rows:
            for o in r["outcomes"]:
                outcomes[o] = outcomes.get(o, 0) + 1
        page = rows[cursor:cursor + limit]
        return self._log("cited_by", {"target": target, "cursor": cursor, "limit": limit}, {
            "target": target, "outcomes": outcomes,
            "by_cell": sorted(by_cell.values(), key=lambda c: _cellkey(c["cell"])),
            "population_total": len(rows), "returned": len(page),
            "units": [_describe(r["unit"]) | {"citations": len(r["outcomes"]), "outcomes": sorted(set(r["outcomes"]))}
                      for r in page],
            "truncated": cursor + limit < len(rows), "cursor": cursor + limit if cursor + limit < len(rows) else None,
            "grain": "units (CFR sections) citing this Code section"})

    # --- one unit ----------------------------------------------------------------

    def unit(self, unit: str, cursor: int = 0, limit: int = 50, only_broken: bool = False) -> dict:
        limit, cursor = _limit(limit), _offset(cursor)
        rows = self._citations(unit)
        counts: dict[str, int] = {}
        for r in rows:
            counts[r["outcome"] or "unparsed"] = counts.get(r["outcome"] or "unparsed", 0) + 1
        if only_broken:
            rows = [r for r in rows if r["outcome"] in ix.BROKEN]
        page = rows[cursor:cursor + limit]
        return self._log("unit", {"unit": unit, "cursor": cursor, "limit": limit, "only_broken": only_broken}, {
            **_describe(unit), "outcomes": counts, "citations": page, "population_total": len(rows),
            "returned": len(page), "truncated": cursor + limit < len(rows),
            "cursor": cursor + limit if cursor + limit < len(rows) else None})

    def _citations(self, unit: str) -> list[dict]:
        """Occurrence keys are deterministic (spike 2: key(manifest, unit, index)), so fetch by key;
        a join filtered on the occurrence's unit has no index and timed out on part 1."""
        if not self._q("FOR u IN units FILTER u.manifest == @m AND u.unit == @u RETURN 1", m=self.m, u=unit):
            raise KeyError(f"no unit {unit}")
        side = _rows()[unit]["citations"]
        occ = self._q("FOR o IN occurrences FILTER o._key IN @keys SORT o.index RETURN {index: o.index, path: o.path}",
                      keys=[ix.key(self.m, unit, i) for i in range(len(side))])
        if [o["path"] for o in occ] != [c["path"] for c in side]:
            raise LookupError(f"{unit}: the stored occurrences and the citations sidecar disagree")
        asserted = {a["occurrence"]: a for a in self._q(
            """FOR x IN assertions FILTER x.manifest == @m AND x.unit == @u
               RETURN {occurrence: x.occurrence, outcome: x.outcome, target: x.target,
                       target_outcome: x.target_outcome}""", m=self.m, u=unit)}
        for o in occ:
            a = asserted.get(ix.key(self.m, unit, o["index"]), {})
            o |= {k: a.get(k) for k in ("outcome", "target", "target_outcome")}
        return occ

    def cite(self, unit: str, index: int) -> dict:
        """The words around one citation, and the Code provisions it resolved to."""
        meta = _rows().get(unit)
        if meta is None or not 0 <= index < len(meta["citations"]):
            raise KeyError(f"no citation {index} in {unit}")
        c = meta["citations"][index]
        stored = self._db.collection("occurrences").get(ix.key(self.m, unit, index))
        if stored is None or stored["path"] != c["path"]:
            raise LookupError(f"{unit}#{index}: the stored occurrence and the citations sidecar disagree")
        got = self._follow_unit(unit)
        out = {**_describe(unit), "index": index, "path": c["path"], "head": c["head"], "status": got["status"]}
        if got["status"] == "ok" and c.get("span"):
            out |= context(got["text"], c)
        assertion = ix.key(ix.key(self.m, unit, index), cx.RP)
        out["resolves_to"] = self._q("""FOR p, e IN 1..1 OUTBOUND CONCAT("assertions/", @a) resolves_to
                                        FILTER e.manifest == @m
                                        RETURN {provision: p._key, identifier: p.identifier, address: p.address,
                                                level: p.level, status: p.status, candidates: e.fanout}""",
                                     a=assertion, m=self.m)
        a = self._q("RETURN DOCUMENT('assertions', @a)", a=assertion)[0]
        out |= {"outcome": a and a["outcome"], "target": a and a["target"],
                "target_outcome": a and a["target_outcome"],
                "population_total": 1, "returned": 1, "truncated": False}
        return self._log("cite", {"unit": unit, "index": index}, out)

    # --- the words -------------------------------------------------------------------

    def follow(self, kind: str, id: str, offset: int = 0, length: int = SLICE, from_end: bool = False) -> dict:
        """kind 'unit' (a CFR section id) or 'provision' (a key from `cite`). Hash-checked text, sliced.
        `from_end` counts `offset` back from the end (applicability paragraphs sit there)."""
        length, offset = max(1, min(int(length), 20000)), _offset(offset)
        if kind == "unit":
            got, head = self._follow_unit(id), _describe(id)
        elif kind == "provision":
            if not UUID.fullmatch(id):
                raise KeyError(f"not a provision key: {id!r}; take one from `cite` (resolves_to)")
            p = self._db.collection("provisions").get(id)
            if p is None or p["manifest"] != self.um:
                raise KeyError(f"no provision {id}")
            got = cx.follow(p["locator"])
            head = {"provision": id, "identifier": p["identifier"], "status_in_code": p["status"]}
        else:
            raise ValueError("kind must be 'unit' or 'provision'")
        out = {**head, "status": got["status"]}
        if got["status"] == "ok":
            out |= window(got["text"], offset, length, from_end)
        return self._log("follow", {"kind": kind, "id": id, "offset": offset, "length": length,
                                    "from_end": from_end}, out)

    def _follow_unit(self, unit: str) -> dict:
        u = self._q("FOR u IN units FILTER u.manifest == @m AND u.unit == @u RETURN u.locator", m=self.m, u=unit)
        if not u:
            raise KeyError(f"no unit {unit}")
        return cx.follow(u[0])


# --- helpers ---------------------------------------------------------------------

UUID = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")


def context(text: str, citation: dict) -> dict:
    """The words around a citation. Its span indexes `citations.normalize(text)`, not the stored
    flat text (normalizing collapses ' ( PRS )' and shifts every later offset). The hash check
    covers the text, not the span, so the span is checked here: a section-head citation's slice
    must contain its section number."""
    t = normalize(text)
    a, b = citation["span"]
    cited = t[a:b]
    if citation["head"] == "section" and citation["path"]:
        check = "ok" if citation["path"].split("/")[0] in cited else "mismatch"
    else:
        check = "unchecked"
    return {"text_domain": "levadura.citations.normalize", "span_check": check,
            "before": t[max(0, a - CONTEXT):a], "cited": cited, "after": t[b:b + CONTEXT]}

def window(t: str, offset: int, length: int, from_end: bool = False) -> dict:
    """A slice of a text, saying where the next one starts (after round 2: a caller didn't find paging)."""
    start = max(0, len(t) - offset - length) if from_end else offset
    end = min(len(t), start + length)
    return {"chars_total": len(t), "start": start, "end": end, "text": t[start:end],
            "population_total": len(t), "returned": end - start, "grain": "characters",
            "truncated": start > 0 or end < len(t),
            "next_offset": end if end < len(t) else None,
            "how_to_page": "call again with offset=next_offset, or from_end=true to read backwards from the end"}


def _offset(n) -> int:
    n = int(n)
    if n < 0:
        raise ValueError("cursor and offset must be non-negative")
    return n


def _limit(n) -> int:
    n = int(n)
    if n < 1:
        raise ValueError("limit must be positive")
    return min(n, MAX_LIMIT)


def _cellkey(c: str):
    return (0, int(c), "") if c.isdigit() else (1, 0, c)


@lru_cache(maxsize=1)
def _rows() -> dict[str, dict]:
    """The measured citation rows (results/cfr-usc-citations-v2-2025.jsonl), by unit id: spans and heads."""
    data = cx.CIT.read_bytes()
    if hashlib.sha256(data).hexdigest() != SIDECAR_SHA256:
        raise LookupError(f"{cx.CIT.name} is not the file the index was built from")
    out = {}
    for line in data.decode().splitlines():
        r = json.loads(line)
        out[f"cfr26-2025:{r['volume_file']}:{r['ordinal']}"] = r
    return out


@lru_cache(maxsize=1)
def _subjects() -> dict[tuple[str, int], tuple[str, str]]:
    """Section numbers and subjects, cached on disk by the archive's hash (parsing takes seconds)."""
    data = cx.CFR_ZIP.read_bytes()
    cache = cx.ROOT / "tmp" / f"surface1-subjects-{hashlib.sha256(data).hexdigest()[:16]}.json"
    if cache.exists():
        return {(v, int(o)): tuple(x) for v, o, *x in json.loads(cache.read_text())}
    out = {(s["volume_file"], s["ordinal"]): (s["sectno"], s["subject"]) for s in sections(io.BytesIO(data))}
    cache.parent.mkdir(exist_ok=True)
    cache.write_text(json.dumps([[v, o, *x] for (v, o), x in out.items()]))
    return out


def _describe(unit: str) -> dict:
    _, vol, ordinal = unit.rsplit(":", 2)
    sectno, subject = _subjects().get((vol, int(ordinal)), ("?", "?"))
    return {"unit": unit, "sectno": sectno, "subject": subject}
