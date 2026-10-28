# Predictions: how long did pre-AIA patents keep issuing? (Tony and Claude)

*Pre-registered 2026-10-28, before any first-inventor-to-file indicator but one was fetched. This commit's OTS
stamp is the proof of that order.*

## The question

The AIA's first-inventor-to-file rules apply by effective filing date (on or after 2013-03-16), not grant date.
Applications filed earlier kept issuing for years. Among the patents challenged in the PTAB final written
decisions of 2021–2026 (data/ptab/meta.jsonl), what share of those granted in each year after the effective date
are pre-AIA? The USPTO's application record gives the answer per patent (`firstInventorToFileIndicator`: N for
pre-AIA, Y for AIA).

## What we knew

- One probe: application 12978537, granted in 2014, filed 2010-12-24, indicator N.
- These are patents someone chose to challenge, not all grants. Challenged patents may skew older.

## Tony's prediction (2026-10-28, in his words)

"The USPTO issues numbers (more or less) sequentially, so I would expect that about 90% of the patents issued
after the AIA effective date were pre-AIA, with that percentage trailing off in the decades after that date."

Read as: about 90% pre-AIA among patents granted just after 2013-03-16, declining over the following years.

## Claude's prediction

Pre-AIA share (indicator N) by grant year:

| Grant year | Point | Range |
|---|---|---|
| 2013 (after 03-16) | 97% | ≥ 90% |
| 2014 | 92% | 80–99% |
| 2015 | 80% | 65–92% |
| 2016 | 62% | 45–80% |
| 2017 | 45% | 30–65% |
| 2018 | 30% | 15–50% |
| 2019 and later | 12% | 3–30% |

The share should fall every year (allowing one year of noise). Applications without the indicator are reported,
not dropped.

## Why

Typical pendency is two to three years, with a long tail of continuations claiming pre-2013 priority. These
continuations matter most in exactly the litigated, PTAB-challenged population.
