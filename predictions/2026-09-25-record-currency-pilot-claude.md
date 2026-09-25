# Predictions: record-currency feasibility pilot

*Written 2026-09-25 by the Claude Opus 5.5 instance that designed the pilot
([design](../docs/investigator-design.md), draft 5 and its four adversarial
reviews). Stamped before any model call. The pilot is descriptive, and these
are my priors, recorded so the scorecard can show where they were wrong. They
are not hypotheses the pilot is powered to confirm.*

Substrate: Haiku 4.5 via OpenRouter. 8 worlds, 3 of them repeated. Accuracy
means value = current over all probes, with abstain and invalid counted as
not current. "Model arms" are P·Q, F·Q, P·L, F·L. C is reported separately.

| | Prediction |
|---|---|
| R1 | O and D score 1.00 accuracy on every probe (the machinery works). |
| R2 | C (closed book) accuracy ≤ 0.05. |
| R3 | Every model arm's accuracy is below D's, and none exceeds 0.95. |
| R4 | F·L ≥ P·Q in accuracy, with a mean paired difference ≥ +0.05. At this ledger size, the world in the prompt beats a small persistent mind with a tool. |
| R5 | P·Q's no-probe-time-ledger-call rate is ≥ 0.20, and higher than F·Q's. |
| R6 | P·Q's obsolete rate on changed-value replacement probes is higher than F·Q's. |
| R7 | In every model arm, accuracy on withdrawal probes is lower than on changed-value replacement probes. |
| R8 | On equal-value replacement probes, every model arm makes more provenance errors (source ≠ current) than value errors. |
| R9 | Every model arm's invalid rate is ≤ 0.05. |
| R10 | Event probes score lower than their matched controls in every model arm (pooled over kinds and lags). |
| R11 | The whole pilot costs ≤ $40 on OpenRouter. |

What would surprise me most: P·Q beating F·L (R4 failing in the direction
I'd like). Given three reviews that found my design tilting that way, I'd
want the result checked before believing it.
