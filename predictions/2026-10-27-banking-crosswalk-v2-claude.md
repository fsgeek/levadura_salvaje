# Predictions: banking crosswalk v2, with Jabberwock's world time (Claude)

*Pre-registered 2026-10-27 by the Claude Opus 5.5 owner, before v2's code was written. This commit's
OTS stamp is the proof of that order.*

## What changes

- **v1** (obs-0178) scoped each edition's part-level act names by writing the edition into the wabe
  (`cfr.12.<edition>.<part>`), because Jabberwock had no world time.
- **yanantin has since built world time at levadura's request:** `galumph(..., at=)` (#41), the
  gyre-less default fix (#47), and the resolve pushdown (#46). All three were verified on levadura's
  own case.
- **v2** uses one wabe per part (`cfr.12.<part>`). Each part-level alias carries a gyre from its
  edition's date to the next edition's (1997-01-01 → 2010-01-01 → 2025-01-01 → open). Names are
  resolved `at=` the edition's date.
- **v2 drops the v1 artifact:** pairs whose act stays unresolved and is keyed `name:act` (an
  unresolved "the Act") form no class.

## Predictions

| # | Quantity | Prediction |
|---|---|---|
| X1 | Classes (act, section) with consensus per edition, v2 against v1 with `name:act` classes removed | identical, as sets keyed by canonical act name and section, in all three editions |
| X2 | Classes held in consecutive editions that moved | 0 |
| X3 | Pairs per edition | identical to v1 (668, 1,127, 2,275). Keying changes; pairing doesn't |

**Why.** Half-open gyres at the edition dates, queried at those dates, are logically the same as
edition-scoped wabes. Any difference is a defect in levadura's conversion or in Jabberwock's `at=`, and
finding which is the point. X1 is the acceptance test of yanantin's work in levadura's production path.
No blind audit: these are deterministic equivalence claims.
