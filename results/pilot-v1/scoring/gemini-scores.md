### Scores for Predictions R1–R11

**R1**
* **Quote:** "O and D score 1.00 accuracy on every probe (the machinery works)."
* **Numbers used:** O overall accuracy = 1.000; D overall accuracy = 1.000. The event table shows `1.00(1.00)` for all O and D cells.
* **Judgment calls:** None.
* **Score:** Pass.

**R2**
* **Quote:** "C (closed book) accuracy ≤ 0.05."
* **Numbers used:** C accuracy = 0.000.
* **Judgment calls:** The design notes C probes all failed due to illegal tool calls and scored invalid, resulting in 0 accuracy. Scored against the exact wording, it passes. A reasonable reader could score it "not scorable" because C did not function as a closed-book guess as intended.
* **Score:** Pass.

**R3**
* **Quote:** "Every model arm's accuracy is below D's, and none exceeds 0.95."
* **Numbers used:** D accuracy = 1.000. F.L = 0.972; P.Q = 0.963.
* **Judgment calls:** "Every model arm" is read as P·Q, F·Q, P·L, and F·L, excluding O, D, and C, based on the substrate definition ("'Model arms' are P·Q, F·Q, P·L, F·L. C is reported separately").
* **Score:** Fail (F.L and P.Q both exceed 0.95).

**R4**
* **Quote:** "F·L ≥ P·Q in accuracy, with a mean paired difference ≥ +0.05. At this ledger size, the world in the prompt beats a small persistent mind with a tool."
* **Numbers used:** F.L accuracy = 0.972; P.Q accuracy = 0.963. Mean paired difference F.L - P.Q = +0.019.
* **Judgment calls:** None.
* **Score:** Fail (+0.019 is not ≥ +0.05).

**R5**
* **Quote:** "P·Q's no-probe-time-ledger-call rate is ≥ 0.20, and higher than F·Q's."
* **Numbers used:** P.Q `no_ledger_call` = 0.181; F.Q `no_ledger_call` = 0.000.
* **Judgment calls:** None.
* **Score:** Fail (0.181 is not ≥ 0.20).

**R6**
* **Quote:** "P·Q's obsolete rate on changed-value replacement probes is higher than F·Q's."
* **Numbers used:** None.
* **Judgment calls:** The rows corresponding to "changed-value replacement" are `repl`.
* **Score:** Not scorable from this output. Missing number: obsolete rate broken down specifically for changed-value replacement probes for P.Q and F.Q.

**R7**
* **Quote:** "In every model arm, accuracy on withdrawal probes is lower than on changed-value replacement probes."
* **Numbers used:** F.L withdrawal (`wdr`) accuracy across lags: 1.00, 1.00, 1.00. F.L replacement (`repl`) accuracy across lags: 1.00, 0.94, 0.94.
* **Judgment calls:** The output lacks pooled accuracy by event kind. However, because F.L's withdrawal accuracy is strictly greater than or equal to its replacement accuracy at every lag, its pooled withdrawal accuracy must be higher, making the prediction mathematically fail. A reasonable reader could score this "not scorable" due to the missing pooled numbers.
* **Score:** Fail.

**R8**
* **Quote:** "On equal-value replacement probes, every model arm makes more provenance errors (source ≠ current) than value errors."
* **Numbers used:** None.
* **Judgment calls:** The rows corresponding to "equal-value replacement" are `eq`.
* **Score:** Not scorable from this output. Missing number: provenance errors and value errors broken down specifically for equal-value replacement probes.

**R9**
* **Quote:** "Every model arm's invalid rate is ≤ 0.05."
* **Numbers used:** F.L = 0.000; F.Q = 0.000; P.L = 0.009; P.Q = 0.005.
* **Judgment calls:** "Every model arm" excludes C (which had a 1.000 invalid rate) per the substrate definition.
* **Score:** Pass.

**R10**
* **Quote:** "Event probes score lower than their matched controls in every model arm (pooled over kinds and lags)."
* **Numbers used:** None.
* **Judgment calls:** Event probes are the first number in the matrix cells; matched controls are the numbers in parentheses. While one could estimate the pooled numbers using the design's event ratios (which would show F.L events scoring higher than controls, failing the prediction), the exact pooled numbers are missing.
* **Score:** Not scorable from this output. Missing number: pooled accuracy for event probes and matched controls for each model arm.

**R11**
* **Quote:** "The whole pilot costs ≤ $40 on OpenRouter."
* **Numbers used:** None.
* **Judgment calls:** The output only provides `probe_cost_usd` (which sums to $22.37). The design states F arms have cost-only wakes, meaning wake costs exist and must be included in the "whole pilot" cost.
* **Score:** Not scorable from this output. Missing number: total cost of the pilot including wake costs.

### Unanticipated Findings in the Data
* **Failed wakes:** 20 failed wakes occurred, predominantly in the persistent arms (P.L had 11; P.Q had 7).
* **Control degradation:** Model arms frequently scored worse on untouched controls than on the events themselves (e.g., F.L `rep+1` control accuracy is 0.67 vs. event accuracy of 1.00).
* **C's failure mode:** C's 1.000 invalid rate (due to illegal tool calls) drove its accuracy to 0.000, rather than it acting as a true closed-book guess.
* **Ledger reliance:** P.L had a higher `no_ledger_call` rate (0.245) than P.Q (0.181).