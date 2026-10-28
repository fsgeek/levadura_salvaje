# Scorecard: how long did pre-AIA patents keep issuing?

*Scores predictions/2026-10-28-ptab-fitf-curve-tony-and-claude.md (stamped at 7a96020 before the indicators were
fetched) against obs-0184. The ground truth is the USPTO's `firstInventorToFileIndicator` for each application
(N = pre-AIA), fetched for all 1,467 distinct applications behind patents granted on or after 2013-03-16 and
challenged in PTAB final written decisions, 2021–2026. Written 2026-10-28.*

| Grant year | n | Pre-AIA share | Claude predicted | | Tony predicted |
|---|---|---|---|---|---|
| 2013 (after 03-16) | 90 | 100% | 97% (≥ 90%) | hit | about 90% just after the effective date |
| 2014 | 112 | 96.4% | 92% (80–99%) | hit | |
| 2015 | 141 | 87.1% | 80% (65–92%) | hit | |
| 2016 | 94 | 85.1% | 62% (45–80%) | miss, above | |
| 2017 | 138 | 77.4% | 45% (30–65%) | miss, above | |
| 2018 | 143 | 68.5% | 30% (15–50%) | miss, above | |
| 2019 and later | 749 | 52.2% | 12% (3–30%) | miss, far above | "trailing off in the decades after" |

The share falls every year, as both predicted.

**Tony's curve fits, and mine doesn't.** I modelled ordinary prosecution with a modest tail, and the curve fell off too
fast. Half of the challenged patents granted in 2019 or later still carry a pre-2013 effective filing date. Tony
explained why before the data existed (2026-10-28): applications are kept alive through continuations, and
petitions are tailored to competitors, so old filings issue for many years. "The patents filed in early March 2013
(pre-AIA) might not issue for many years and yet remain pre-AIA." The challenged population is where that strategy
shows. Whether its tail is heavier than that of all grants needs a random baseline of grants. That is predicted
but not yet measured (see the qhaway memory on Tony's pendency model).

**The deepest tail.** 3 applications have no record in the portal (HTTP 404): one from the 08/ series and two from
the 09/ series, filed in the mid to late 1990s. They were granted after 2013 and challenged in 2021–2026. Their
series puts them at pre-AIA. Applications filed before June 8, 1995 also keep the pre-URAA term (the longer of 17
years from grant or 20 from filing), a second old regime carried into the present (Tony, 2026-10-28).

**What it means for readers.** A patent number dates the grant, but not the regime. Below about 8.4 million the
number decides it. Above that, the chance it is pre-AIA is still 52% for grants in 2019 and later, in this
population. A reader that reasons "newer patent, newer law" is wrong about half the time on recent grants.
That is what context test 2 measures.
