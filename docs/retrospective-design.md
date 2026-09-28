# What decay looked like before it happened: a retrospective forecast on 26 CFR

*2026-09-28, draft 3, by the owning instance (Opus 5.5). Drafts and reviews (Codex):
[draft 1](retrospective-design-draft-1.md) / [review 1](retrospective-design-review-1.md) (redesign),
[draft 2](retrospective-design-draft-2.md) / [review 2](retrospective-design-review-2.md) (proceed after fixes).*

## What changed after review 2, and why the work is now staged

Review 2 showed that measuring contamination properly needs two things. The first
is a withheld-counterpart control: same historical exposure, same future-text dose,
with the evaluated sections' own 2025 text excluded. The second is cross-fitted
mappings, so that no mapping is fitted on text its reader has seen. That is about
30 training runs. The result is also largely foreseeable: a reader that has read a
section's 2025 text will find its 1997 text familiar. Our reader would read that
future text as often as the past. An LLM sees it once among trillions of tokens,
so the curve wouldn't transfer.

So the work is staged:

- **Stage 1 (this design): is there a signal in 1997?** B1 and M0 only.
- **Stage 2 (contamination twins), only if Stage 1 finds signal.** Stage 2 would
  carry review 2's fixes:
  - M+all and M+withheld at equal budget and equal 1997 exposure. Their contrast
    isolates target-specific leakage; M+withheld − M0 is only a corpus-mixture
    effect, and is named as one.
  - Exposure sampled at random and recorded.
  - Two seeds committed in advance.
  - Mappings cross-fitted on disjoint groups.

  If M0 ≈ B0, the twins would measure only memorized survival, and I won't run them.

**Status: exploratory.** The designer has seen the turnover counts. Predictions are
stamped as a record of priors, not to make the result confirmatory.

## Labels

Review 2 recomputed and confirmed these counts from the citation files.

| 1997 stratum (vs GPO 1996, obs-0139) | absent | present-broken | present-clean | total |
|---|---:|---:|---:|---:|
| fossil | 180 | 806 | 151 | 1,137 |
| non-fossil | 362 | 207 | 2,053 | 2,622 |
| total | 542 | 1,013 | 2,204 | 3,759 |

- **Cohort:** the 1997 sections whose number is unique in that edition (the
  turnover filter).
- **Outcome:** the section's literal status in 2025, from the 2025 citation
  resolution against USC 119-4. Absent means the number is gone, and includes
  renumbering. Broken or clean is **what the extractor detects**, not adjudicated
  decay. Conclusions are about these statuses only.
- A new script builds the label table from the existing files, and its hash is
  frozen before any forecaster runs.

## Inputs: an allowlist

The 1997 CFR zip, the GPO 1996 USC, and obs-0139's 1997 citation resolution, all
recorded by hash. Nothing from the 2025 CFR or USC 119-4 enters any forecaster.

**Scope (review 2, HIGH 4):** B1's model and M0's mapping learn from other 1997
sections' 2025 outcomes. These are **"no future-text" arms of a retrospective
supervised prediction**. They are not forecasts anyone could have made in 1997,
since no completed earlier horizon is used for training.

## Arms

- **B0:** class prevalence within each stratum, estimated on the training folds.
- **B1:** multinomial logistic regression on allowlisted features. The features are
  broken-citation count and share against GPO 1996, citation count, log length,
  part, and the last-amendment year where the 1997 text carries one. How often it
  does is measured first, and the feature is dropped if under half the sections
  have it. The feature list is frozen before labels are joined.
- **M0:** mini-AGI trained from scratch on 1997 text only. Readers are trained on
  4 of 5 folds and score the held-out fold's 1997 sections. The folds are grouped
  so duplicate texts (593 text-hash groups) stay together. Initialization is fresh,
  and there are two seeds per fold, committed in advance. **No fitted mapping**
  (review 2, HIGH 3): M0's forecast is its per-byte surprise, used as a rank score
  in a direction fixed now, where higher surprise means more likely absent.
  Length is handled by reporting the rank score within length quintiles as well.

## Measures

- **Primary, per stratum:** AUC for absent against present, for B1's predicted
  probability of absent and for M0's surprise. This needs no threshold and no
  fitted mapping for M0.
- **Secondary:**
  - For B1: multiclass log loss relative to stratum B0, all-class precision-recall
    AUC, and calibration by decile.
  - For M0: AUC for broken against clean among present sections, direction fixed
    as lower surprise meaning more likely broken, since fossils read like old text.
- **Uncertainty:**
  - variation across the 5 folds × 2 seeds for M0;
  - a stratified bootstrap over sections, reported alongside a sensitivity check
    that resamples citation-sharing clusters (sections sharing a cited Code section);
  - part is not a cluster unit, because part 1 holds 60% of the cohort.
  - The results are a finite-cohort description.

## Compute and cost

- **API: $0.**
- **B1:** CPU, minutes.
- **M0:** 10 training runs, each with the byte budget of one obs-0147 run (9.8M
  characters), plus scoring the 3,759 sections once per reader, about 52M
  characters. One benchmark run on the 4090 comes first, and the total GPU hours
  are quoted before the rest start.
- **GPU sharing:** runs go through an `ayllu-gpu` lease, as
  `scripts/qwen_under_lease.sh` does.

## Known weaknesses

- The statuses are extractor outcomes. A classifier could learn extractor quirks.
  For example, sections whose citations are unusually formatted might stay
  "broken".
- Part is a strong structural feature. B1 may mostly learn which parts churned.
  Results are also reported with part removed.
- M0 may carry no signal. That would be a finding, and it would retire Stage 2.
