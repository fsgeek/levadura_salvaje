# Predictions: the parity lens on banking citations (Claude)

*Pre-registered 2026-10-16 by the Claude Opus 5.5 owner, before any act-section pair was
compared with another. This commit's OTS stamp is the proof of that order.*

**Tony: this is an explicit invitation.** If you want to predict any of these, write them in a
separate file and stamp it. Leaving it blank is fine too.

## What I knew when writing this

- Everything in docs/banking-usc-scorecard.md, including A1's wrong addresses: GLBA § 509 cited
  as 12 U.S.C. 6809, BSA 5318(g) in title 12, APA § 553 in title 12, and 1842(c)(8) for
  1843(c)(8).
- A survey regex, not the instrument, counted 3,528 "section N of the X Act" citations in 2025
  12 and 31 CFR. 2,365 of them are followed at once by a U.S.C. citation. The most cited acts are
  the FDI Act (423, plus 234 as "FDI Act") and the BHC Act (224, plus 176 as "BHC Act").
- "the Bank Act" is a locally defined name for the Federal Home Loan Bank Act.
- I have not built the map from act section to Code section, or compared any pair with it.

## The instrument

- `act_pairs` v1 reads "section N of the <Name> Act" followed immediately by a U.S.C. citation.
- The map is the corpus's own consensus. For each (act as written, act section), the U.S.C.
  section at least 75% of at least 3 pairs agree on.
- A pair **disagrees** when its (title, U.S.C. section) differs from the consensus target.
- Population: 2025 editions of 12 and 31 CFR, distinct sections.

## Predictions

| # | Quantity | Point | Range |
|---|---|---|---|
| P1 | Share of pairs whose (act, section) has a consensus | 60% | 40–80% |
| P2 | Share of covered pairs that disagree | 3% | 1–8% |
| P3 | Share of disagreeing pairs whose own U.S.C. section is in force at 119-120 (wrong address, not dead law) | 50% | 25–75% |
| P4 | Share of consensus targets in force at 119-120 | ≥95% | |

**Audit (A2):**
- Up to 40 disagreeing pairs (all of them, if fewer), sampled with seed 20261016.
- Mixed with 20 agreeing pairs as blind controls, sampled with the same seed and shuffled
  together.
- For each item, the reader sees the regulation text and the headings at 119-120 of the cited
  U.S.C. section and of the consensus target. Nothing says which items were flagged.
- The reader judges whether the U.S.C. citation is the right address for the act section the
  regulation names.
- Predictions:
  - at least 70% of flagged pairs are judged misaddressed;
  - at most 10% of controls are.

## Why these numbers

Drafters usually copy a citation pair from an earlier rule, so most pairs should agree, and
consensus should be strong for the common acts. A1 found wrong addresses in about a third of the
real breaks. But a pair that disagrees with consensus can also be correct: an act renumbered
over time, or the same short name used for two different acts. So I expect flags to be fewer and
noisier than the controls are clean.
