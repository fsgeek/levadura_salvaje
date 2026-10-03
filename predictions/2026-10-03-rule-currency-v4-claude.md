# Predictions: rule-currency lens v4, a label for closed inputs

*Written 2026-10-03 by the owning instance (Claude Opus 5.5), before any v4 call. v4 keeps v3's
structured excerpts and adds a fourth label, `closed_inputs`: a rule with no end date of its
own that applies only to amounts, items or events from periods that ended before 2025. It drops
v2's clause that put carryovers under `untimed`. Origin: two blind audits found the readers
agreeing on 0 of 10 items in 1.909-6, against about 90% elsewhere, with the direction
flipping between the audits. A second instance (relayed by Tony) read this as a hole in the
categories, not ambiguity in the law. It proposed exactly this test: state the
inputs-versus-application distinction and see whether the disagreement collapses.*

*The run waits for Codex's review of v3, because its fixes may change the excerpts. If they
do, v4 runs on the fixed excerpts, and these predictions still apply.*

Same 548 records, Qwen settings and lease. A fresh blind audit with two new readers (fresh
subagents, one Opus and one Sonnet): 15 per v4 label (seed 3), plus the 1.902-3 #49 probe,
plus a fixed extra stratum of ten 1.909-6 citations (seed `extra-3`) for X1. The probe and the extra stratum are kept out of X2, X6 and the population adjustment. *(Clarified 2026-10-03, before any v4 call: the first version said "every 1.909-6 citation in the sample", which a random draw might leave at two or three.)*

| | Prediction |
|---|---|
| X1 | **The collapse test.** On the audit's 1.909-6 items, the readers agree on at least 60%. (Two earlier audits: 0 of 10.) p = 0.65 |
| X2 | overall reader agreement, excluding 1.909-6 items: 85% (75–95), so the new label doesn't break agreement elsewhere |
| X3 | Qwen v4 `closed_inputs`: 15% of the 548 (5–30) |
| X4 | at least half of 1.909-6's 84 citations are `closed_inputs` in Qwen v4. p = 0.6 |
| X5 | Qwen v4 `untimed`: 50% (35–62), down from v3's 66.6% as carryovers leave |
| X6 | the consensus agrees with Qwen v4: 75% (60–90) |
| X7 | the probe, 1.902-3 #49, the ownership exception: at least one reader says `closed_inputs` or `untimed`. p = 0.7 |

If X1 fails, the disagreement isn't about the categories. It sits in the text, or in how
readers resolve it, and the next step is a reader who isn't Claude.
