# Scorecard: banking crosswalk v2, on Jabberwock's world time

*Scores predictions/2026-10-27-banking-crosswalk-v2-claude.md (stamped at e6900f6a before v2's code was written)
against obs-0182. Written 2026-10-27.*

| # | Predicted | Measured | |
|---|---|---|---|
| X1 classes identical to v1's (pooled `name:act` removed), every edition | identical | identical in 1997, 2010 and 2025; none only in v1, none only in v2 | hit |
| X2 classes held in consecutive editions that moved | 0 | 0 (110 held) | hit |
| X3 pairs per edition equal to v1's | 668, 1,127, 2,275 | 668, 1,127, 2,275 | hit, after a declared fix |

**What it shows.** yanantin's world time, built at levadura's request (`galumph(..., at=)`, Yanantin #41), with the
gyre-less default fixed (#47) and resolution pushed down to the store (#46), gives exactly the result of the
edition-in-the-wabe workaround it replaces, in levadura's production path. One wabe per part now holds every
edition's aliases, each valid from its edition's date to the next. Excluding the pooled unresolved "the Act"
(94, 151 and 31 pairs in 1997, 2010 and 2025) removes all three of v1's false moves. Act-section addresses in
12 CFR did not move between 1997, 2010 and 2025.

**Declared fix, in the dry run before the ledger entry.** The first dry run counted pairs after the `name:act`
filter (574, 976, 2,244). X3 is about pairing, which v2 doesn't change, so it is now counted before the filter.
That was a counting error, not an instrument change.

**Timing, not a finding.** The run took 9 min 46 s against v1's 79 s. The profile shows the same number of
store queries (8,764) at about twice the cost each, and every store operation slowed alike. The machine's load
average was 22 at the time, with another project's job at about 600% CPU. The comparison is confounded, and
nothing is attributed to `at=`.
