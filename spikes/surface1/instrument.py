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

import random
import re

import surface as sf
from surface import cx, ix, normalize

MAX_UNITS = 5000
SAMPLE = 5
WINDOW = 400


def measure(s: "sf.Surface", population: dict, pattern: str, near: str | None = None,
            window: int = WINDOW, ignore_case: bool = True, sample: int = SAMPLE, seed: int = 0) -> dict:
    try:
        rx = re.compile(pattern, re.IGNORECASE if ignore_case else 0)
    except re.error as e:
        raise ValueError(f"bad pattern: {e}") from e
    window = max(0, min(int(window), 5000))
    sample = max(0, min(int(sample), 20))
    units = _population(s, population)
    if len(units) > MAX_UNITS:
        raise ValueError(f"population of {len(units)} units exceeds {MAX_UNITS}; narrow it")
    texts = cx._cfr_texts(cx._hold(cx.CFR_ZIP))
    rows = sf._rows()
    hits, misses, no_anchor = [], [], []
    for u in units:
        r = rows[u]
        t = normalize(texts[(r["volume_file"], r["ordinal"])])
        if near is None:
            regions = [(0, len(t))]
        else:
            regions = [(max(0, c["span"][0] - window), c["span"][1] + window) for c in r["citations"]
                       if c.get("path") and c.get("span") and c["path"].split("/")[0] == near]
            if not regions:
                no_anchor.append(u)
                continue
        m, at = _first(rx, t, regions)
        if m:
            hits.append((u, t[max(0, at + m.start() - 120):at + m.end() + 120]))
        else:
            misses.append((u, t[:240]))
    rng = random.Random(seed)
    pick = lambda xs: rng.sample(xs, min(sample, len(xs)))  # noqa: E731
    out = {
        "population": population, "pattern": pattern, "near": near, "window": window if near else None,
        "ignore_case": ignore_case, "population_total": len(units),
        "matched": len(hits), "not_matched": len(misses), "no_anchor": len(no_anchor),
        "matched_sample": [sf._describe(u) | {"words": w} for u, w in pick(hits)],
        "not_matched_sample": [sf._describe(u) | {"opening": w} for u, w in pick(misses)],
        "matched_units": [u for u, _ in hits][:200], "not_matched_units": [u for u, _ in misses][:200],
        "no_anchor_units": no_anchor[:200],
        "truncated": max(len(hits), len(misses), len(no_anchor)) > 200,
        "returned": min(len(hits), 200) + min(len(misses), 200) + min(len(no_anchor), 200),
        "caution": "a regular expression, not a reading: check both samples before trusting the counts",
    }
    return s._log("measure", {"population": population, "pattern": pattern, "near": near, "window": window,
                              "ignore_case": ignore_case, "matched": len(hits), "not_matched": len(misses)}, out)


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
