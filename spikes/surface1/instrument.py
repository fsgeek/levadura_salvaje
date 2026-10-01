"""The way up: a predicate the reader defines from what it read, run over a population.

Round 1 (docs/surface1-scorecard.md, S3) showed both callers going down cleanly and
never coming back up. Reading raised population questions, such as "how many of the
73 sections citing § 902 say the repeal happened?", and the surface had no way to ask them.

`measure(population, predicate)`:
- **population**: `{"cited_by": "902"}` (units citing a Code section) or `{"cell": "54"}`
  (a cell's members: units with a broken citation), or `{"cell": "54", "all": true}`
  (every unit in the cell).
- **predicate**: a regular expression over each unit's normalized text, optionally
  `near` a citation of a Code section, within `window` characters of it. Each window
  is searched as its own string, so `^` and `$` anchor at its edges. It's
  deliberately exact and cheap. A model-based predicate is the next step and needs
  the same contract.
- **result**: counts on both sides, plus a **sample from each side**, with the
  matching words for hits and the opening words for misses, so the reader can see
  where the predicate is wrong before trusting the count. That's the seed's
  "where are the counterexamples?".

Each run is a footprint, recorded with its population and predicate. Re-running the
same predicate later is how a reading becomes an instrument.
"""

import hashlib
import random
import re

import surface as sf
from surface import cx, ix, normalize

MAX_UNITS = 5000
SAMPLE = 5
WINDOW = 400


MAX_PATTERN = 500
SNIPPET = 120   # characters of context either side; a hit's own text is cut at 240
LIST = 200      # unit ids per list per call; page with list_cursor


def measure(s: "sf.Surface", population: dict, pattern: str, near: str | None = None,
            window: int = WINDOW, ignore_case: bool = True, sample: int = SAMPLE, seed: int = 0,
            list_cursor: int = 0) -> dict:
    if len(pattern) > MAX_PATTERN:
        raise ValueError(f"pattern longer than {MAX_PATTERN} characters")
    try:
        rx = re.compile(pattern, re.IGNORECASE if ignore_case else 0)
    except re.error as e:
        raise ValueError(f"bad pattern: {e}") from e
    window = max(0, min(int(window), 5000))
    sample = max(0, min(int(sample), 20))
    list_cursor = sf._offset(list_cursor)
    units = _population(s, population)
    if len(units) > MAX_UNITS:
        raise ValueError(f"population of {len(units)} units exceeds {MAX_UNITS}; narrow it")
    hits, misses, no_anchor, stale = [], [], [], []
    for u, t, citations in _evidence(s, units):
        if t is None:
            stale.append(u)
            continue
        if near is None:
            regions = [(0, len(t))]
        else:
            regions = [(max(0, c["span"][0] - window), c["span"][1] + window) for c in citations
                       if c.get("path") and c.get("span") and c["path"].split("/")[0] == near]
            if not regions:
                no_anchor.append(u)
                continue
        m, at = _first(rx, t, regions)
        if m:
            a, b = at + m.start(), at + m.end()
            hits.append((u, t[max(0, a - SNIPPET):min(b, a + 240) + SNIPPET]))
        else:
            misses.append((u, t[:240]))
    rng = random.Random(seed)
    pick = lambda xs: rng.sample(xs, min(sample, len(xs)))  # noqa: E731
    hs, ms = pick(hits), pick(misses)
    lists = {"matched_units": [u for u, _ in hits], "not_matched_units": [u for u, _ in misses],
             "no_anchor_units": no_anchor, "stale_units": stale}
    page = {k: v[list_cursor:list_cursor + LIST] for k, v in lists.items()}
    more = any(len(v) > list_cursor + LIST for v in lists.values())
    shown = {u for v in page.values() for u in v} | {u for u, _ in hs + ms}
    out = {
        "population": population, "pattern": pattern, "near": near, "window": window if near else None,
        "ignore_case": ignore_case, "population_total": len(units),
        "matched": len(hits), "not_matched": len(misses), "no_anchor": len(no_anchor), "stale": len(stale),
        "sample_requested": sample, "seed": seed,
        "matched_sample": [sf._describe(u) | {"words": w} for u, w in hs],
        "not_matched_sample": [sf._describe(u) | {"opening": w} for u, w in ms],
        **page, "list_cursor": list_cursor, "list_next": list_cursor + LIST if more else None,
        "returned": len(shown), "truncated": more,
        "caution": "a regular expression, not a reading: check both samples before trusting the counts",
    }
    return s._log("measure", {"population": population, "pattern": pattern, "near": near, "window": window,
                              "ignore_case": ignore_case, "sample": sample, "seed": seed,
                              "list_cursor": list_cursor, "matched": len(hits), "not_matched": len(misses),
                              "no_anchor": len(no_anchor), "stale": len(stale),
                              "sampled": {"matched": [u for u, _ in hs], "not_matched": [u for u, _ in ms]}},
                  out)


def _evidence(s: "sf.Surface", units: list[str]):
    """(unit, normalized text or None, citations) for each unit. The text and the sidecar row must
    both hash to the unit's locator in this manifest, or the unit is reported stale, not counted
    (review 2, #2: measure had bypassed the checks cite and follow make)."""
    want = dict(s._q("FOR u IN units FILTER u.manifest == @m AND u.unit IN @us RETURN [u.unit, u.locator.sha256]",
                     m=s.m, us=units))
    texts = cx._cfr_texts(cx._hold(cx.CFR_ZIP))
    rows = sf._rows()
    for u in units:
        r = rows.get(u)
        flat = texts.get((r["volume_file"], r["ordinal"])) if r else None
        if r is None or flat is None or r["sha256"] != want.get(u) or \
                hashlib.sha256(flat.encode()).hexdigest() != want.get(u):
            yield u, None, []
        else:
            yield u, normalize(flat), r["citations"]


def _first(rx, t: str, regions: list[tuple[int, int]]):
    """The first match in any region. Each region is searched as its own string, so `^` and `$`
    anchor at the window's edges (after round 2: `rx.search(t, a, b)` never matches `^` at a)."""
    for a, b in regions:
        m = rx.search(t[a:b])
        if m:
            return m, a
    return None, 0


def _population(s: "sf.Surface", population: dict) -> list[str]:
    if set(population) == {"cited_by"}:
        return [r["unit"] for r in s._q("""FOR x IN assertions FILTER x.manifest == @m AND x.target == @t
                                            COLLECT u = x.unit SORT u RETURN {unit: u}""",
                                         m=s.m, t=str(population["cited_by"]))]
    if "cell" in population and set(population) <= {"cell", "all"}:
        if population.get("all"):
            return s._q("FOR u IN units FILTER u.manifest == @m AND u.cell == @c SORT u.unit RETURN u.unit",
                        m=s.m, c=str(population["cell"]))
        return ix.unpaged(s._db, s.m, str(population["cell"]))
    raise ValueError('population must be {"cited_by": N} or {"cell": C} or {"cell": C, "all": true}')


def population_arg(cited_by: str | None, cell: str | None, all_units: bool) -> dict:
    """One population selector, refused if ambiguous (review 2, #10)."""
    if (cited_by in (None, "")) == (cell in (None, "")):
        raise ValueError("give exactly one of cited_by or cell")
    if cited_by not in (None, ""):
        if all_units:
            raise ValueError("all applies to a cell, not to cited_by")
        return {"cited_by": cited_by}
    return {"cell": cell, "all": bool(all_units)}
