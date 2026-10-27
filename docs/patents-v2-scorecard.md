# Scorecard: patents v2, citations read at the date they state

*Scores predictions/2026-10-27-patents-v2-claude.md (stamped at 8f52946 before the instruments ran) against
obs-0181 and audit Z2 (`results/patents-v2-audit-z2/`, read blind by Opus (A) and Sonnet (B); no Hamut'ay door
had taken up the offer at plaza seq 179). Written 2026-10-27.*

| # | Predicted | Measured | |
|---|---|---|---|
| D1 marked old-law citations, 2025 | 60 (25–150) | 11 | miss, far below |
| D2 v1's 15 non-resolving that are marked (not blind) | 14 (≥ 13) | 9 | miss |
| D3 marked that resolve against the 2010 Code | 97% (≥ 90%) | 100% (11/11) | hit |
| D4 marked that also resolve against today's Code | 70% (50–90%) | 18% (2/11) | miss |
| C1 sections mentioning March 15 or 16, 2013 | 30 (15–70) | 6 (33 mentions) | miss |
| C2 conditioned share of mentions | 50% (30–80%) | 73% | hit |
| C3 sections stating the hybrid rule | 3 (≥ 1) | 4 (§§ 1.55, 1.78, 1.130, 1.131) | hit |
| Z2a marked judged pre-AIA | ≥ 90% each | 100% (A) / 100% (B), all "stated" | hit |
| Z2a unmarked judged pre-AIA | ≤ 1 of 10 | 0 (A) / 0 (B) | hit |
| Z2b readers agree with the mechanical class | ≥ 80% | 63% (A, 12/19) / 74% (B, 14/19) | miss |

## What was measured

**Referential validity at the stated date works exactly.** All 11 citations that state a pre-AIA date
resolve against 35 U.S.C. as of 2010 (GPO, current through 2011-01-07). Both readers confirm every one
refers to pre-AIA law, and that none of 10 unmarked citations does.

**The claim I said mattered was wrong.** I expected most old-law citations to name sections that still
exist, so that v1's resolver would pass them while they meant different text. Only 2 of 11 do. The
patent rules mostly cite subdivisions the AIA removed (102(e), 102(g), 103(c)), so v1 had already
flagged them. Explicit old-law citation is also much rarer than I thought (D1 11, C1 6 sections): the
rules concentrate the transition in a few provisions.

**Three kinds of old-law reference, not two:**
- **Stated** (9 of v1's 15): a date or "pre-AIA" with the citation. Deterministic.
- **Implicit** (5): the interference rules (§§ 41.201, 41.202) and § 1.959 cite 102(g) and 134(c) with no
  date at all. Only the procedure, which exists only for old applications, says so. No local marker sees
  this. My D2 prediction had borrowed v1's readers' inference. That is the most useful miss here: temporal
  applicability can live entirely in context.
- **Conditioned**: the hybrid rule MPEP 2159.03 describes is in the text of §§ 1.55, 1.78, 1.130 and 1.131
  ("contains, or contained at any time, a claim to a claimed invention that has an effective filing date
  before March 16, 2013"). I checked MPEP 2159.03 [R-01.2024] at the source before relying on it.

**Z2b's miss is about granularity, and both readers point the same way.** All 12 disagreements across the two
readers are cases the instrument called date-only and the readers called conditioned. In the case examined,
the date is in a paragraph heading ("(k) Requirements for certain applications filed on or after March 16,
2013.") and the condition is in the next sentence. The readers judged the provision and the instrument judged
the sentence. A sentence is the wrong unit for rules whose headings carry the date and whose bodies carry the
condition. I'm leaving it as a measured limit rather than tuning it after seeing the audit.

## Changes after the stamp, before any ledger entry (declared)

- `gpo_usc` hard-coded title 26 and silently read nothing from title 35. It was generalized test-first, and
  title 26's 1996 output is unchanged record for record. That is the first change to an existing `src/`
  module in the patents work: the GPO reader did not transfer.
- `dated_cites`: a date after a list of subsections ("102(e), (f), or (g) in effect prior to…"), and
  "contains, or contained" with a comma. Both were found by checking the non-blind D2 cases, fixed
  test-first, and the instrument's limits now name implicit old law.

## The three levels, as used here

- **Level 1, referential validity:** the dated resolver answers it for stated references, exactly.
- **Level 2, temporal applicability:** text answers it where the rules state a condition (C3), and only
  context answers it for the interference rules.
- **Level 3, interpretive correctness:** the readers. They also showed the instrument's unit of analysis was
  wrong (Z2b).

Recency is not authority, and in these rules the old authority is fenced by date, by condition, or only by
the procedure it lives in.
