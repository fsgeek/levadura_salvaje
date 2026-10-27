# Scorecard: how PTAB final written decisions mark the law they apply, v1

*Scores predictions/2026-10-27-ptab-applicability-claude.md (stamped at f810f93 after the metadata was fetched
and before any decision text was read) against obs-0183 and audit P1 (`results/ptab-audit-p1/`: 30 unmarked and
10 marked decisions on pre-AIA patents, read blind by Opus (A) and Sonnet (B); no Hamut'ay door had taken up
the offer at plaza seq 179). Written 2026-10-27.*

The corpus is every final written decision the USPTO Open Data Portal holds, 2021–2026: 2,388 decisions. They
were fetched with an API key Tony obtained with identity verification, using 2,487 requests in all, a very small
fraction of the weekly limits. 30 PDFs have no text layer (1.3%).

| # | Predicted | Measured | |
|---|---|---|---|
| Q1 pre-band (granted < 2013-03-16) marked "pre-AIA" | 85% (65–97%) | 74.2% (of 612) | hit |
| Q2 mid-band (2013–2016) marked | 55% (35–75%) | 71.8% (of 542) | hit |
| Q3 late-band (2017+) marked | 25% (10–45%) | 47.9% (of 1,203) | miss, above |
| Q4 pre-band stating a basis (date or "effective filing date") | 60% (35–85%) | 67.3% | hit |
| Q5 pre-band unmarked citing a pre-AIA-only subdivision (103(a), 102(e)/(f)/(g)) | 60% (30–90%) | 53.8% (of 158) | hit |
| Q6 pre-band marking 2025–26 against 2021–22 | not lower by > 10 points | 79.2% against 75.3% | hit |
| Q7 PDFs without text | 1% (≤ 5%) | 1.26% | hit |
| P1 unmarked judged to apply pre-AIA law implicitly | ≥ 70% each | 73% (A, 22/30) / 77% (B, 23/30) | hit |
| P1 unmarked judged to apply the wrong regime | ≤ 10% | 0% (A; 8 unclear) / 0% (B) | hit |
| P1 controls judged not pre-AIA | ≤ 1 of 10 | 0 (A) / 0 (B; 1 unclear) | hit |

## What it shows

- **The Board usually says which law it applies, and when it doesn't, it still applies the right one.**
  Three quarters of decisions on certainly pre-AIA patents say "pre-AIA". Of those that don't, about half still
  cite a subdivision that exists only in pre-AIA law, such as § 103(a). Neither reader found a decision applying
  the wrong regime.
- **About a quarter of unmarked pre-band decisions can't be checked from their own words** (A 8 of 30, B 7 of
  30, with 7 in common). Their grounds are listed as bare "§ 103" or "§§ 102, 103", with no subsection, no
  statutory text and no statement of version. The law applied is fixed only by what every competent reader
  knows: a patent granted in 2012 is pre-AIA. That is the cooperative fence guest:authority named (plaza seq
  188): it holds in the readers, not in the text. A reader without that context, such as a resolver or a model
  given only the decision, cannot recover it.
- **The mark spreads beyond its band.** 48% of decisions on patents granted in 2017 or later still say
  "pre-AIA" (Q3 missed). Grant date is a coarse proxy: later patents can be continuations with pre-2013 claims,
  and "pre-AIA" also names the § 112 paragraph forms. The text was not tuned after this was seen.
- **Marking is steady over time** (75% → 79%). The Board is not getting less explicit as pre-AIA patents age.

## Limits

- The mark is lexical. 5 (A) and 6 (B) "unmarked" decisions do state the version in other words. That is
  counted as found by the readers, and is the instrument's recall limit.
- The readers saw at most eight passages around "35 U.S.C." citations, not whole decisions, so "unclear" can
  mean only that the passages shown were silent.
- Grant date stands in for effective filing date.
