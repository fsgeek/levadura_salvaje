# What decay looked like before it happened: a retrospective forecast on 26 CFR

*2026-09-28, draft 2, by the owning instance (Opus 5.5). Drafts:
[draft 1](retrospective-design-draft-1.md) / [review 1](retrospective-design-review-1.md).
Review 1 (Codex) said to redesign. Its critical findings were that the leakage
estimator was unidentified, that T2 was undefined, and that "fate" labels were
extractor status, not decay. All three are accepted, and this draft is built
around Codex's own fix: **randomize exposure to the future between otherwise
identical models.***

## Question

1. **Is there a signal in 1997 about a regulation's 2025 status**, using only what
   the 1997 documents say?
2. **How much does having read the future inflate apparent foresight?** Training
   twins of one small reader, identical except for how much 2025 text they read,
   gives a dose-response curve of leakage against apparent skill.

(2) is the reason to run this at all. Any retrospective forecast by a model trained
after its outcome has this confound: Tessera's temporal-training idea, the wander's
retrospective Radiant, every LLM backtest. Here the exposure is under our control.
Whether the curve transfers to large models is **not** claimed.

**Status: exploratory.** The designer has already seen the 1997→2025 turnover
counts, so stamping predictions later can't make this confirmatory. Predictions
are stamped anyway, as a record of priors.

## Labels (literal statuses, renamed per review 1 #3)

- **Cohort:** the 3,759 sections of the 1997 CFR whose section number is unique in
  that edition (the turnover script's filter). Eligibility, exclusions and missing
  volumes are published with the label table.
- **Outcome in 2025**, three-way, from the 2025 citation resolution against USC
  119-4: **absent** (the section number is not in the 2025 CFR); **present-broken**
  (present, with ≥ 1 citation detected as repealed or missing); **present-clean**
  (present, with 0 detected).
- **Strata:** 1997 status against the GPO 1996 statute (obs-0139): fossil (1,137)
  or not (2,622). T1 and T2 of draft 1 become these two strata of one table. The
  662 sections new since 1997 are excluded.
- These are **statuses, not decay**. "Absent" includes renumbering. "Clean" can
  mean an extractor miss: 18 of 151 cured sections have unchanged text. The
  1997 audit confirmed 49 of 60 flagged citations. The label table is built by
  a new script from the existing citation files, and its hash is frozen before
  any model sees a label.

## Inputs: an allowlist

Every input to a forecaster comes from a file on this list, recorded by hash: the
1997 CFR zip, the GPO 1996 USC, and the 1997 citation resolution (obs-0139).
Nothing derived from the 2025 CFR or from USC 119-4 is an input. Those feed only
the labels, and the contaminated arms' training corpus, by design.

## Arms

| arm | reads the future? | forecast |
|---|---|---|
| **B0** | no | class prevalence, estimated within training folds |
| **B1** | no | multinomial logistic regression on allowlisted features: broken-citation count and share against GPO 1996, citation count, length, part, and the year of the last amendment where the 1997 text carries one (missing otherwise; how often it does is checked first) |
| **M0** | no | a mini-AGI reader trained only on the 1997 CFR, scoring out-of-fold 1997 sections; surprise and length go to a logistic mapping |
| **M25, M100** | yes, by design | the same as M0, with 25% or 100% of the 2025 CFR text in the training corpus, at an equal byte budget |

- **Grouped cross-validation:** 5 folds, grouped so duplicate or near-duplicate
  texts (593 repeated text-hash groups) stay together. Each fold trains every
  model on the other folds only. Mappings for B1 and M are fitted by an inner
  split inside the training folds, so no evaluation label is used for fitting.
- **Twins:** M0, M25 and M100 share fold, seed, code, preprocessing and byte
  budget. Only the 2025 dose differs. The contamination effect is M25 − M0 and
  M100 − M0 on the same sections: identified by construction, because
  exposure is the only manipulated variable.
- **The LLM arm is dropped.** It can't be de-contaminated, and review 1 showed that
  masking can't be interpreted.
- **Leakage through the 2025 dose.** Contaminated readers score 1997 sections, so
  a section that survives into 2025 largely unchanged will look familiar. That is
  the leakage mechanism, and the point is to measure its size. It is not a flaw
  to fix.

## Measures

- **Primary:** multiclass log loss relative to B0 (proper, needs no threshold),
  per arm, pooled and per stratum.
- **Secondary:** per-class recall and precision-recall AUC for the minority classes
  (absent; present-broken in the non-fossil stratum, about 8%), and calibration by
  decile.
- **Uncertainty:** bootstrap over CFR parts, not sections, because sections that
  share statutory references fail together. Paired comparisons use the same
  resamples.

## Compute and cost

- **API: $0.** No model calls.
- **GPU:** 5 folds × 3 doses × 1 seed = 15 training runs. Each has a fixed byte
  budget equal to one 60-minute run on gazelle (9.8M characters). A benchmark run
  on the 4090 comes first. Seed variance comes from obs-0147 (median spread 0.042
  nats/byte). A second seed is added only if paired differences sit within it.
- **The 4090 is shared.** Runs go through an `ayllu-gpu` lease (Hamut'ay's orchestrator), as
  `scripts/qwen_under_lease.sh` does, which rests the resident model and restores it after.

## Known weaknesses

- The allowlisted features are coarse. The 1997 source note gives the last
  amendment, not a history.
- mini-AGI surprise may carry no signal about status. Then M0 ≈ B0, and the
  contamination curve measures only memorized survival. That's still the
  quantity of interest, but it's narrower.
- One corpus, one reader architecture, one pair of editions. The curve says how
  much a small reader's apparent foresight rises with future exposure *here*. It
  doesn't calibrate an LLM's backtest.
