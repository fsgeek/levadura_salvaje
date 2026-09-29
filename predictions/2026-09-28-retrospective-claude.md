# Predictions: a retrospective forecast on 26 CFR, Stage 1

*Written 2026-09-28 by the owning instance (Claude Opus 5.5), after the feature
table was frozen (`results/retro-features-v1-1997.jsonl`) and before the label
table was built or joined. Design: [retrospective-design.md](../docs/retrospective-design.md),
draft 3. **Exploratory:** I've already seen the turnover counts (obs-0141), so
these record priors and aren't a confirmatory test.*

AUC means absent-vs-present per 1997 stratum unless stated. B1 is 5-fold
cross-validated (folds stratified by 1997 stratum × 2025 status, seed 0), with
part one-hot, `last_fr_year` missing-indicated, and default L2 regularization.

| | Prediction |
|---|---|
| R1 | B1 AUC, fossil stratum: 0.68 (range 0.60–0.76) |
| R2 | B1 AUC, non-fossil stratum: 0.66 (range 0.58–0.74) |
| R3 | B1 beats stratum B0 in multiclass log loss in both strata |
| R4 | removing `part` from B1 lowers AUC by ≥ 0.03 in the non-fossil stratum. Churn is structural. |
| R5 | B1, onset (present-broken vs present-clean, non-fossil stratum, present only): AUC ≥ 0.60 |
| R6 | M0 AUC (higher surprise → absent), fossil stratum: 0.55 (range 0.45–0.62); weak or none |
| R7 | M0 broken-vs-clean AUC among present sections (lower surprise → broken): 0.55 (range 0.48–0.62) |
| R8 | M0 is below B1 on absent-vs-present in both strata |

If R6 and R7 both sit within 0.05 of 0.5, Stage 2 (the contamination twins) does
not run.
