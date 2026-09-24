# Scorecard: do fossil candidates name a period that has ended?

*Predictions: [predictions/2026-09-24-dated-lens-claude.md](../predictions/2026-09-24-dated-lens-claude.md).
Lens: `src/levadura_salvaje/lenses/dated.py`, written by a separate instance
from the intent section alone and frozen before any call. Jev labels:
obs-0135. Blind hand audit: obs-0136.*

The currency lens found that about 91% of the 1,675 fossil candidates read
as current. That count mixed two kinds of section: those that never mention
time, and those full of dates with one undated clause. This lens separates
them.

| | Prediction | Measured | Verdict |
|---|---|---|---|
| D1 | silent: 55% (40-70) | 46.0% (771) | **pass** |
| D2 | names an ended period: 42% (28-58) | 52.3% (876) | **pass** |
| D3 | currency-current sections that name an ended period: 38% (25-55) | 48.5% (728/1,500) | **pass** |
| D4 | named-period rate, identical-to-1997 ≥ 1.3x the rest | 36.8% vs 55.2% = 0.67x | **fail** |
| D5 | hand audit agrees with Jev ≥ 80% (point 88) | 95% (57/60) | **pass** |

**4 of 5 pass.** The three audit misses are all Jev saying silent where one
buried clause names an ended period: a 1993 bond-indenture cutoff, a pointer
to the 2014 CFR for requests filed in 2013-14, and "prior to its amendment
… January 3, 1975". About 15% of the silent stratum is therefore really
dated. The corrected estimate is **about 39% silent**, roughly 650 sections.

## What it means

Of the regulations that cite dead statute:

- **About half give the reader some textual cue** that part of them is
  stale: a period that has plainly ended. The cue is often one clause among
  current-looking rules, which is why the currency lens called 1,500 of them
  current.
- **About two in five give no cue at all.** They state rules, cite repealed
  or missing statute, and never mention a date that has passed. Nothing in
  the text tells a reader the ground has moved. The only evidence is outside
  it: the statute, the ledger, the citation check.

## D4 fails for the same reason P5 did

D4 predicted that sections unchanged since 1997 would name ended periods
more often. They do so *less* often (0.67x). The confound is length, as it
was for P5 in the fossil scorecard. Unchanged sections are always a single
chunk and carry 9.8 citations on average. The rest average 1.22 chunks and
42.5 citations. A longer section has more places for a dated clause. I made
the same per-section mistake twice. The lesson is now recorded twice: when
the unit is a section, control for length before predicting a direction.
