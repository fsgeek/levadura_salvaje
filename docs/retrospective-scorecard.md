# Scorecard: what decay looked like before it happened (Stage 1)

*Predictions: [predictions/2026-09-28-retrospective-claude.md](../predictions/2026-09-28-retrospective-claude.md).
Design: [retrospective-design.md](retrospective-design.md), draft 3, after two Codex
reviews. Numbers: obs-0150 (B1) and obs-0151 (M0). Exploratory: the designer had
seen the turnover counts. Tony made no predictions.*

**The 1997 documents do carry a signal about 2025, and it's structural, not
textual.** From 1997 inputs alone, a logistic model on a handful of features ranks
which sections will be gone by 2025 well above chance:
- **AUC 0.74 for sections that were already fossils** (citing dead statute) in 1997;
- **0.81 for healthy sections**, but only 0.62 without the CFR part, so most of that
  is *where* a regulation sits;
- **0.80 for which healthy sections will later cite dead law.**

A reader that has absorbed the 1997 text, mini-AGI trained on 1997 alone, sees
essentially nothing. How surprising a section reads doesn't predict its fate
(AUC 0.46–0.54).

| | Prediction | Measured | Verdict |
|---|---|---|---|
| R1 | B1 AUC, fossil stratum 0.68 (0.60–0.76) | 0.741 | **pass** |
| R2 | B1 AUC, non-fossil stratum 0.66 (0.58–0.74) | 0.805 | **fail** (above range) |
| R3 | B1 beats stratum B0 in log loss, both strata | 0.744 vs 0.804; 0.534 vs 0.665 | **pass** |
| R4 | removing part lowers non-fossil AUC by ≥ 0.03 | 0.805 → 0.616 (−0.19) | **pass** |
| R5 | B1 onset AUC (broken vs clean, present non-fossils) ≥ 0.60 | 0.797 | **pass** |
| R6 | M0 AUC, fossil stratum 0.55 (0.45–0.62) | 0.512 | **pass** |
| R7 | M0 broken-vs-clean AUC among present sections 0.55 (0.48–0.62) | 0.512 fossil / 0.541 non-fossil | **pass** |
| R8 | M0 below B1 on absent-vs-present, both strata | 0.512 < 0.741; 0.459 < 0.805 | **pass** |

**7 of 8 pass.** The miss is in the useful direction: the structural signal on
healthy sections was stronger than I guessed.

Intervals, with bootstrap over sections / over citation clusters:
- B1 fossil AUC: 0.74 [0.68, 0.79] cluster.
- B1 non-fossil AUC: 0.81 [0.78, 0.83] section and [0.69, 0.86] cluster.
- The clusters are sections grouped by their most-cited Code section. The
  cluster intervals are the honest ones, since dead citations fail together.

## Stage 2 does not run

The stamped rule was that the contamination twins run only if M0's AUCs sit more
than 0.05 from 0.5. They don't:
- R6 is 0.512 and R7 is 0.512 / 0.541.
- The per-reader AUCs (5 folds × 2 seeds) range 0.47–0.61 in the fossil stratum.

With no leak-free signal in the reader, the twins would only measure how well a
reader that has read the 2025 text recognizes it. Nobody needs that measured.

## What the predictions didn't anticipate

- **In the non-fossil stratum, M0 points the other way.** The sections that
  disappear read slightly *less* surprising than the ones that survive: AUC 0.459,
  [0.43, 0.49] by section, [0.40, 0.50] by cluster. That's the reverse of the fixed
  direction, and the effect is concentrated in the middle length quintiles
  (0.39, 0.40). One possible reading: sections that vanish are boilerplate-like,
  typical 1997 regulatory prose, while survivors carry more distinctive text. It's
  small, it runs against the stamped direction, and it hasn't been checked for
  confounds, so it's recorded, not claimed.
- **Readers differ in how much they read.** The 31-minute budget gave between 9.8M
  and 12.1M characters (`reader_chars` in obs-0151), because the 4090 ran faster
  after the first fold. The design called for an equal byte budget, and this
  differs from it. Per-reader AUC correlates weakly with characters read: r = 0.37
  in the fossil stratum and 0.34 in the non-fossil stratum, over 10 readers, which
  is not significant. The reader that read the most (12.1M) gives the highest
  fossil AUC (0.61). So a longer-trained reader might find a little signal. This
  budget can't rule that out, and the Stage 2 decision rests on the pooled AUCs
  at this budget.

## What it means

For the utility question, the answer is a **triage signal, not a verdict**. A
maintainer in 1997 could have used three facts: a section's part, whether it
already leaned on dead statute, and how much it cited. Those would have ranked the
sections headed for removal or rot well above chance, and the 1997 documents alone
supply them. That transfers: the same features can be computed for today's
regulations against today's Code, to say where the next generation of fossils is
most likely.

What doesn't transfer is text familiarity. mini-AGI found 2025 fossils read like
1997 text (obs-0147), but reading like 1997 in 1997 says nothing about the future.
The earlier finding was about what fossils look like, not about foresight.

For the method, the retrospective Radiant's leakage problem is answered more
narrowly than hoped. A contaminated forecaster needs a leak-free forecaster with
real skill to be compared against, and the text reader has none. The leak-free
skill here comes from structure (part, citation state). An LLM would see the same
structure, so its backtest would need a comparison with B1, not with a reader.

## Limits

- Outcomes are literal statuses: absent (including renumbered) and extractor-detected
  broken or clean. They are not adjudicated decay.
- B1 learns other 1997 sections' 2025 outcomes. It is retrospective supervised
  prediction, not a forecast anyone could have made in 1997 without an earlier
  completed horizon.
- One corpus, one pair of editions, 3,759 sections. Part 1 holds 60% of them.
- The designer had seen the turnover counts, and the review loop was run by the same
  designer, so this is exploratory.
