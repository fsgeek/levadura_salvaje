Read only the permitted files. I wrote and ran independent Python via stdin; I did not import `analyze_pilot.py`. All 40 probe files contain 36 rows, with no duplicate `(world, arm, run, index)` keys.

**Recomputed metrics**

Cells are count/denominator (percentage). Invalids and abstentions remain in all denominators.

| Arm | Accuracy | Obsolete | Invalid | No probe-time ledger call |
|---|---:|---:|---:|---:|
| O | 180/180 (100%) | 0/180 | 0/180 | 180/180 (100%) |
| D | 180/180 (100%) | 0/180 | 0/180 | 0/180 |
| C | 0/216 | 0/216 | 216/216 (100%) | 216/216 (100%) |
| P·Q | 208/216 (96.296%) | 2/216 (0.926%) | 1/216 (0.463%) | 39/216 (18.056%) |
| F·Q | 199/216 (92.130%) | 0/216 | 0/216 | 0/216 |
| P·L | 200/216 (92.593%) | 1/216 (0.463%) | 2/216 (0.926%) | 53/216 (24.537%) |
| F·L | 210/216 (97.222%) | 1/216 (0.463%) | 0/216 | 2/216 (0.926%) |

**R6/R7/R8/R10 breakdowns**

“Replacement” below means **non-control `kind=="replace"`**, excluding equal-value replacements, withdrawals and repeated measurements. All three lags are pooled.

| Arm | Replacement obsolete | Replacement accuracy | Withdrawal accuracy | Equal-value provenance errors | Equal-value value errors | Event accuracy | Control accuracy |
|---|---:|---:|---:|---:|---:|---:|---:|
| P·Q | 0/54 | 51/54 | 16/18 | 0/18 | 1/18 | 102/108 | 106/108 |
| F·Q | 0/54 | 50/54 | 17/18 | 1/18 | 1/18 | 102/108 | 97/108 |
| P·L | 1/54 | 49/54 | 18/18 | 1/18 | 3/18 | 100/108 | 100/108 |
| F·L | 1/54 | 52/54 | 18/18 | 0/18 | 0/18 | 106/108 | 104/108 |

**Agreement and analysis bug**

- No numerical disagreement with `analysis.txt`: all summary columns, event/lag cells, failed-wake counts and paired contrasts agree at displayed precision.
- Independently checking answer validity and checking current value/source against the logged O answers produced **zero mismatches**. Obsolete classifications were aggregated from logged scores; the permitted files lack the underlying worlds needed to independently reconstruct every superseded value.
- **Cost-reporting bug:** `summary()` converts absent costs to zero. Thus C’s displayed `$0.000` represents **216 missing costs**, not established free calls. One failed P·L probe also lacks cost. The script also ignores `cost_turns_unreported`, although all present counters here are zero.
- No accuracy-aggregation bug found. Overall accuracy weights world 0 twice; paired contrasts weight each of five worlds equally after pooling its repeats. That difference is legitimate but needs disclosure.

**Prediction scores**

Judgments throughout: “every model arm” means exactly P·Q, F·Q, P·L, F·L, as explicitly defined in the prediction preamble. Strict “higher,” “lower,” and “more” exclude ties. I score the actual reduced pilot; results do not establish outcomes for the originally proposed 11 world-runs.

| ID | Exact stamped wording | Score and basis |
|---|---|---|
| R1 | “O and D score 1.00 accuracy on every probe (the machinery works).” | **Pass.** Each is 180/180. Judgment: applies to recorded probes; O/D were not repeated for world 0. This establishes their logged accuracy, not exhaustive machinery correctness. |
| R2 | “C (closed book) accuracy ≤ 0.05.” | **Pass, operationally.** 0/216, because failed probes count as invalid and remain in the denominator. **Reasonable alternative: not scorable** as a prediction about closed-book guessing: all 216 attempts failed before producing admissible guesses. Zero accuracy does not establish inability to recall generated values. |
| R3 | “Every model arm's accuracy is below D's, and none exceeds 0.95.” | **Fail.** All are below D=1.00, but P·Q=0.962963 and F·L=0.972222 exceed 0.95. Judgment: conjunction; both clauses must hold. |
| R4 | “F·L ≥ P·Q in accuracy, with a mean paired difference ≥ +0.05. At this ledger size, the world in the prompt beats a small persistent mind with a tool.” | **Fail.** F·L exceeds P·Q overall by 2/216=0.009259; equal-world mean paired difference is **+0.019444**, below +0.05. Judgment: pair within world, pooling repeats first. Equal-weight world-run/probe pairing gives +0.009259 and also fails. The failure is insufficient magnitude, **not P·Q beating F·L**. |
| R5 | “P·Q's no-probe-time-ledger-call rate is ≥ 0.20, and higher than F·Q's.” | **Fail.** 39/216=0.180556 versus F·Q=0. Both clauses required. Uses recorded ledger-call counts across all probes, including failures. |
| R6 | “P·Q's obsolete rate on changed-value replacement probes is higher than F·Q's.” | **Fail.** 0/54 versus 0/54. Judgment: the designated changed-value replacement events only. P·Q’s two obsolete answers are **withdrawals**; including them would reverse the verdict but would broaden the stamped category. |
| R7 | “In every model arm, accuracy on withdrawal probes is lower than on changed-value replacement probes.” | **Fail.** Holds only for P·Q: 16/18 < 51/54. F·Q: 17/18 > 50/54; P·L: 18/18 > 49/54; F·L: 18/18 > 52/54. Judgment: event targets only, pooled over lags and runs. |
| R8 | “On equal-value replacement probes, every model arm makes more provenance errors (source ≠ current) than value errors.” | **Fail.** Provenance/value error counts: P·Q **0/1**, F·Q **1/1**, P·L **1/3**, F·L **0/0**. Judgment: non-current includes missing dimensions from abstention/invalidity. Restricting to answered probes gives **0/1, 0/0, 0/2, 0/0**; still fails. Zero-versus-zero is not “more.” |
| R9 | “Every model arm's invalid rate is ≤ 0.05.” | **Pass.** P·Q 1/216; F·Q 0/216; P·L 2/216; F·L 0/216. C is explicitly outside “model arms”; including it would fail but contradict the preamble. |
| R10 | “Event probes score lower than their matched controls in every model arm (pooled over kinds and lags).” | **Fail.** Event/control correct counts out of 108: P·Q **102/106**, F·Q **102/97**, P·L **100/100**, F·L **106/104**. Only P·Q satisfies it. Judgment: “score” means primary accuracy; pool individual matched probes, thereby retaining three times as many changed-replacement events as each other kind. |
| R11 | “The whole pilot costs ≤ $40 on OpenRouter.” | **Not scorable from permitted evidence.** Reported probe costs total **$22.37393285**, with missing failed-probe costs and no wake costs in the permitted logs. Accepting the supplied billing total of **$38.92** would make this **pass**, but raw confirmation is unavailable. |

The permitted `docs/investigator-design.md` does **not** actually contain `$38.92`; it contains the `$6.97` smoke cost and projected costs. I therefore treat `$38.92` as supplied in your request, not independently documented billing evidence.

Reported probe costs: P·Q **$3.89852045**, F·Q **$1.55578250**, P·L **$9.98443780**, F·L **$6.93519210**. The wake-failure files contain epoch, cycle and error only.

**Additional findings the predictions did not specify**

- **21 failed wakes**, all truncations: P·Q 6, F·Q 1, P·L 13, F·L 1. P·L world 1 alone has six. The amended design anticipates failures; the predictions do not quantify their incidence.
- **33 answered probes have wrong values but current sources:** P·Q 5, F·Q 12, P·L 10, F·L 6. Three of four obsolete answers also cite current sources. Source correctness cannot substitute for value correctness.
- All four model arms achieve **18/18 on repeated-measurement event targets**, while their matched controls yield P·Q 18/18, F·Q 13/18, P·L 13/18, F·L 14/18.
- Every equal-value target value error occurs in **world 3**, whose probed field is nested (`["K272",11,0]`). This is a concentration, not evidence that nesting caused the errors.
- C’s failure mode is broader than the design’s `search_memory` example: attempted calls also include `search_project`, `recall`, `bash`, `read` and `memory_schema`. These are recorded attempted calls, not evidence of execution.