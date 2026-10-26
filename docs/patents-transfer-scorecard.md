# Scorecard: does levadura's architecture transfer to patent law? v1

*Scores predictions/2026-10-26-patents-transfer-claude.md (stamped at 64a6f4b before any patent data
was parsed) against obs-0180 and audit Z1a (`results/patents-transfer-audit-z1/`: 15 non-resolving
2025 citations to title 35 and 10 resolving controls, read blind by Opus (A) and Sonnet (B)).
Written 2026-10-26.*

## Transfer

| # | Instrument | Predicted | Measured | |
|---|---|---|---|---|
| I1 | sections loader on 37 CFR | no code change | no change; 1,185 sections (2010), 1,315 (2025) | hit |
| I2 | usc_cites + resolve against 35 U.S.C. | no code change | no change; table built by the existing builder | hit |
| I3 | parity lens | runs, < 30 pairs, not useful | runs, 12 pairs | hit |
| I4 | twins | not applicable | not applicable | hit |
| I5 | citation form of 35 U.S.C. 112 (new) | ≤ 80 lines in `src/` | 37 lines | hit |
| | scripts | ≤ 300 lines | 132 | hit |
| | existing `src/` modules changed | none | none | hit |

Everything levadura built for tax and banking ran on patent law unchanged. The one new instrument
is 37 lines. One defect in it was found in the dry run, before any ledger entry: "35 U.S.C. 112(6)"
(37 CFR 41.110, 2010) is a paragraph number in parentheses, not a letter subsection. It was fixed
test-first and is declared here.

## The corpus

| # | Predicted | Measured | |
|---|---|---|---|
| P1 explicit U.S.C. citations, 2025 | 2,500 (1,200–5,000) | 1,746 | hit |
| P2 title-35 citations not resolving, 2025 | 3% (1–8%) | 1.84% (15 / 814) | hit |
| P3 2010 rate ÷ 2025 rate | 2.0 (≥ 1.5) | 2.54 (4.67% / 1.84%) | hit |
| P4 ordinal share of 112 citations, 2010 | 95% (≥ 85%) | 100% (14 / 14) | hit |
| P5 letter share of 112 citations, 2025 | 70% (≥ 50%) | 100% (13 / 13) | hit |
| P6 ordinal forms surviving in 2025 | 10 (1–40) | 0 | miss |
| Z1a non-resolving judged broken as written | ≥ 50% each | 93% (A, 14/15) / 93% (B, 14/15) | hit |
| Z1a controls judged broken | ≤ 1 of 10 | 0 (A) / 0 (B) | hit |
| Z1b ordinal forms judged deliberate | ≥ half | no items (P6 = 0) | not testable |

The readers agree on all 25 items.

**The positive control works.** The banking crosswalk found no moves, and it couldn't be told
whether it was able to see one. Here the move is total: every paragraph-level citation to § 112 is
ordinal in 2010 and a letter in 2025. The PTO converted all of them, so P6 missed.

## The finding: the same signal means opposite things

- 14 of the 15 non-resolving citations really do point at provisions that don't exist in today's
  Code: pre-AIA 102(e), 102(g), 103(c), the repealed § 104, and § 134(c).
- Both readers judged **all 14 deliberate**: the rules date the citation in their own text, as in
  "35 U.S.C. 102(g) as in effect on March 15, 2013" or "103(c) in effect prior to March 16, 2013".
  They are interference and pre-AIA examination rules that still govern older applications.
- The 15th, § 202(b)(4), exists. That is a miss by levadura's resolver.

In banking, a citation that didn't resolve, or a copy that disagreed, marked an error or a stale
text with no date to tell a reader which rule governs (docs/banking-twins-scorecard.md). Patent
rules solve the applicability problem in the text itself: they write the date into the citation.
The mechanical signal transferred unchanged, but its meaning did not. That is the seed's §8 in
practice: bind evidence early and interpretation late. An instrument's output is evidence, and
what it means has to be read in the domain.

## Declared limits as targets (W5; authority, plaza seq 180)

- **"2010 resolved against the current Code (pre-AIA sections read as absent)."** Written about 2010,
  this limit turned out to be where the 2025 meaning was: the current rules cite pre-AIA sections
  on purpose. Next: resolve each citation against the Code in force at the date the citation
  itself states.
- **"An ordinal far from its citation is not seen."** Not tested: there were no ordinal forms in
  2025.
- **"Explicit 'N U.S.C.' citations only."** Patent rules also cite pre-AIA law in prose ("as in
  effect on…"). Those were seen only where an explicit citation sat nearby.

## For Tony's question about transfer

The architecture transferred. Population first, cheap deterministic instruments, models only on
what's flagged, stamped predictions, blind audits with controls: none of it needed changing, and
the one new instrument was small. What doesn't transfer is the interpretation of what an
instrument flags. In each new domain that has to be found by reading, which is what the audit
does. The architecture keeps that step and doesn't automate it away.

**Cost.** The measurement takes seconds. Two Claude subagent readings, no OpenRouter spend. No
Hamut'ay door had taken up the reader offer (plaza seq 179) when the packet was built.
