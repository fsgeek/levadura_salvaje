# Predictions: patents v2, citations read at the date they state (Claude)

*Pre-registered 2026-10-27 by the Claude Opus 5.5 owner, before the dated-citation instrument or the
condition count ran. This commit's OTS stamp is the proof of that order.*

## Why

v1 (docs/patents-transfer-scorecard.md) found that the 2025 patent rules write applicability into
their citations: "35 U.S.C. 102(g) as in effect on March 15, 2013". A ChatGPT reading Tony shared
proposed three levels for any citation finding:
1. referential validity: did the cited provision exist in the version named?
2. temporal applicability: was that version in force for this case?
3. interpretive correctness: does the document use it rightly?

It also said the coexistence of old and new law can be finer than a date. I checked that at the
source today: MPEP 2159.03 [R-01.2024] says pre-AIA 102(g) applies to an AIA application that
"contains or contained at any time" a claim with an effective filing date before March 16, 2013.

v2 adds two instruments and keeps v1's resolver unchanged, as the control:
- **Dated resolver.** A title-35 citation marked as old law, either by a stated date before
  2013-03-16 ("as in effect on…", "in effect prior to…") within 150 characters after it, or by
  "pre-AIA" within 20 characters before it, is resolved against 35 U.S.C. as of 2010 (GPO
  USCODE-2010-title35, current through 2011-01-07, before the AIA). Every other citation is
  resolved against the current Code, as in v1.
- **Transition count.** In 2025 37 CFR, every mention of "March 16, 2013" or "March 15, 2013" is
  classed as **date-only** or **conditioned**. Conditioned means it states an applicability test
  within its sentence: "effective filing date", "claimed invention", "contains or contained",
  "at any time", "ever contained".

## What I knew when writing this

- v1's results, including the audit notes. 14 of 15 non-resolving 2025 title-35 citations are
  dated or pre-AIA references, so **D2 is not blind**.
- The MPEP 2159.03 text above.
- Today the GPO reader (`gpo_usc`) failed to read title 35, because "26" was hard-coded. Fixed
  test-first (two lines; title 26's output is unchanged record for record). It gives 862 provisions
  for 35 U.S.C. as of 2010.
- Nothing about how many 2025 citations carry old-law markers, or about the transition mentions,
  has been counted.

## Predictions

| # | Quantity | Point | Range |
|---|---|---|---|
| D1 | 2025 title-35 citations marked as old law | 60 | 25–150 |
| D2 | Of v1's 15 non-resolving, marked (not blind) | 14 | ≥ 13 |
| D3 | Marked citations that resolve against the 2010 Code | 97% | ≥ 90% |
| D4 | Marked citations that **also** resolve against the current Code (v1 passed them; the text they mean is different) | 70% | 50–90% |
| C1 | 2025 sections mentioning March 15 or 16, 2013 | 30 | 15–70 |
| C2 | Share of those mentions that are conditioned | 50% | 30–80% |
| C3 | Sections that state the hybrid rule ("contains or contained at any time" or similar) | 3 | ≥ 1 |

**Audit (Z2).** Read blind by two readers (Opus and Sonnet), plus a Hamut'ay door if one has taken up
the offer at plaza seq 179.
- 20 marked citations and 10 unmarked title-35 citations, shuffled. Does the rule refer to pre-AIA
  law here?
  - At least 90% of marked judged yes.
  - At most 1 of 10 unmarked judged yes.
- 20 transition mentions, sampled across both classes. Is an applicability condition stated beyond
  the date?
  - The readers agree with the mechanical class on at least 80%.

**Transfer cost** is counted from this commit, and includes today's GPO reader fix, which is the
first change to an existing `src/` module in the patents work.

## Why these numbers

Pre-AIA references in the rules should mostly name sections that still exist (102, 103), so most
are invisible to v1. That is D4, the claim that matters. The rules on statements under §§ 1.55 and
1.78 should carry the hybrid test, and the interference rules (part 41, subpart D) should be
date-only, which gives C2 near half.
