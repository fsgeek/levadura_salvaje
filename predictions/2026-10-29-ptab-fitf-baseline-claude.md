# Predictions: do challenged patents carry a heavier pre-AIA tail than patents in general? (Claude, after Tony)

*Pre-registered 2026-10-29, before any baseline data was fetched. This commit's OTS stamp is the proof of that order.*

## The question

Tony (2026-10-28): patents kept alive through continuations and then asserted against competitors are the ones that
get challenged, so "the patents filed in early March 2013 (pre-AIA) might not issue for many years and yet remain
pre-AIA". The challenged-patent curve (docs/ptab-fitf-curve-scorecard.md, obs-0184) is 2013 100%, 2014 96%, 2015
87%, 2016 85%, 2017 77%, 2018 69%, 2019+ 52%. Is that tail a property of patents in general, or of the patents that
get challenged?

## Design (baseline v1)

- **Sample.** A random sample of utility patents granted in each year 2014–2022: 100 per year, drawn through the
  USPTO Open Data Portal's application search by grant-date range, with seeded random offsets.
- **Ground truth.** `firstInventorToFileIndicator` for each. The `effectiveFilingDate` field is never used: it is the
  application's own date for continuations (docs/ptab-context-2-scorecard.md).
- **Comparison.** For each grant year, the baseline's pre-AIA share against the challenged population's.
- **Exclusions.** Design and plant patents are excluded. Reissues are reported, not dropped.
- If the portal's search can't draw a fair random sample by grant date, that is reported and the study stops. It is
  not replaced with a convenience sample.

## Predictions

| Grant year | Baseline pre-AIA (point) | Range | Challenged (measured) |
|---|---|---|---|
| 2014 | 90% | 80–97% | 96% |
| 2015 | 72% | 58–85% | 87% |
| 2016 | 50% | 35–65% | 85% |
| 2017 | 32% | 20–48% | 77% |
| 2018 | 20% | 10–35% | 69% |
| 2019–2022 (pooled) | 8% | 2–20% | 52% (2019+) |

- **B1:** The baseline share is below the challenged share in every year from 2016 on.
- **B2:** The gap is at least 30 points in 2018 and in 2019–2022.

## Why

Ordinary prosecution takes two to three years, and most grants carry no continuation lineage. The challenged
population is selected for long-lived families, so its tail should be several times heavier. If B1 fails, the heavy
tail is a property of patenting itself, and Tony's selection explanation isn't needed for it.
