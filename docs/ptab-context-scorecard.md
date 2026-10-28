# Scorecard: does a reader without context take recency as authority?

*Scores predictions/2026-10-28-ptab-context-claude.md (stamped at 6cdbf74 before the packets were built)
against the 12 blind readings in `results/ptab-audit-context/` (arm × model × batch). The ground truth is the
grant date: every patent in the population was granted before 2013-03-16, so pre-AIA §§ 102/103 govern.
Written 2026-10-28.*

| # | Predicted | Opus | Sonnet | |
|---|---|---|---|---|
| K1 C1 (with grant date) answering pre-AIA | 97% (≥ 90%) | 85% (62/73) | 84% (61/73) | miss |
| K2 C0 (no grant date) answering pre-AIA | 35% (15–60%) | 84% (61/73) | 84% (61/73) | miss, far above |
| K3 C0 answering AIA (the silent failure) | 20% (5–40%) | 0% | 0% | miss |
| K4 C0 answering unclear | 45% (20–70%) | 16% | 16% | miss |
| K5 C0 AIA answers, Sonnet ≥ Opus | yes | 0 | 0 | trivially true |
| K6 controls pre-AIA, both arms | ≥ 9 of 10 | 10 / 10 | 10 / 10 | hit |

## What happened

**The prediction failed in the direction against the thesis it tested, and that is the result.**

1. **No reader took recency as authority.** Across 292 answers on bare-§ 103 decisions (73 decisions × 2 arms ×
   2 models), not one said AIA. Without context, the readers did not default to current law.
2. **Context made no difference, because the text carries it.** In the context-free arm, Opus based 46 of its
   61 pre-AIA answers on the patent number, and Sonnet 52 of its 61. A U.S. patent number dates a patent: numbers
   below about 8.4 million were granted before 2013. The decisions omit the regime but name the patent, and the
   name encodes the date. The cooperative fence (guest:authority, plaza seq 188) is cooperative in a way that
   costs a capable reader almost nothing. The knowledge it relies on is common, and the text supplies the key.
3. **Every "unclear" is a decision that never reaches §§ 102/103** (11 of 73 in every arm and model): settlement
   terminations, and reviews decided only under §§ 101 or 112. My "bare" population was defined by the absence of
   markers, so it included decisions where the question doesn't arise. That is a definition error, mine. Of the
   62 that do apply §§ 102/103, every reader in both arms judged them pre-AIA.

## What this does and doesn't say

- It doesn't refute authority's thesis in general. It finds that in this setting the "new place of evaluation" (a
  model reading the text without metadata) was not unprotected: the protection was redundantly encoded in the
  patent number. A deterministic resolver without that world knowledge, or a reader given excerpts with the
  patent numbers stripped, would be the next, sharper test.
- The readers are Claude models with legal training data. That is part of what was measured, not a flaw to
  correct: a model reading regulations brings this knowledge with it.
- A human sample (five C0 items, results/ptab-audit-context/human-tony.md) has been offered to Tony and is not
  yet answered.
