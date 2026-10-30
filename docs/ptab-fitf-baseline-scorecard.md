# Scorecard: challenged patents carry a heavier pre-AIA tail than patents in general

*Scores predictions/2026-10-29-ptab-fitf-baseline-claude.md (stamped at 46f56a1 before any baseline fetch) against
obs-0186. Baseline: 900 utility patents, 100 per grant year 2014–2022, at seeded uniform random offsets in the USPTO
Open Data Portal's application search (`scripts/fetch_ptab.py baseline`). All 900 are utility patents granted in the
year sampled. Ground truth is `firstInventorToFileIndicator`. Written 2026-10-30.*

| Grant year | Baseline pre-AIA | Predicted | | Challenged (obs-0184) |
|---|---|---|---|---|
| 2014 | 99% | 90% (80–97%) | miss, above | 96% |
| 2015 | 91% | 72% (58–85%) | miss, above | 87% |
| 2016 | 57% | 50% (35–65%) | hit | 85% |
| 2017 | 46% | 32% (20–48%) | hit | 77% |
| 2018 | 31% | 20% (10–35%) | hit | 69% |
| 2019–2022 | 10.5% | 8% (2–20%) | hit | 52% (2019+) |

**B1:** the baseline is below the challenged share in every year from 2016 on. **Hit.**
**B2:** the gap is ≥ 30 points in 2018 (38) and in 2019–2022 (about 41). **Hit.** The challenged figure pools every
grant from 2019 on, so the 2019–2022 comparison is approximate.

**Tony's selection explanation holds** (2026-10-28): patents kept alive through continuations and aimed at competitors
are the ones that get challenged. Among patents granted since 2019, about 1 in 10 is pre-AIA in general, and about
half of those that reach the Board are. Early grants are pre-AIA almost universally, in both populations (my 2014–15
points were too low). The difference is all in the tail.

With 100 per year, a single year's share has about ±10 points of sampling uncertainty. The gaps from 2017 on are
well outside that.
