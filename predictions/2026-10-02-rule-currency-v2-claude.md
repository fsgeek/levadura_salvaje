# Predictions: rule-currency lens v2, after the v1 audit

*Written 2026-10-02 by the owning instance (Claude Opus 5.5), after scoring v1 (obs-0156)
and its blind audit (obs-0157), and before any v2 call. v2 adds three rules, all in
[src/levadura_salvaje/lenses/rule_currency.py](../src/levadura_salvaje/lenses/rule_currency.py):
worked examples take the timing of the rule they illustrate; carryovers with no end date
are untimed; pointers are not_a_rule. These are decisions about what the lens should mean,
made after seeing the audit, so v2 is not a confirmatory test of v1. The predictions are
about whether the decisions *take*: whether a model and blind readers apply them the
same way.*

Same population (548 citations of § 902), judge, settings and excerpts as v1. A fresh
blind audit: 45 citations, 15 per v2 label (seed 1), two new readers (fresh subagents,
one Opus and one Sonnet) given the v2 instructions only.

| | Prediction |
|---|---|
| V1 | Of v1's 59 `not_a_rule` citations, at least half move to `untimed` or `time_limited` under v2. p = 0.7 |
| V2 | overall `untimed` rises from 50.2% to 60% (52–72) |
| V3 | the section-level gap (R4) stays small: at most 6 of the 59 sections current by both currency judges have no `untimed` § 902 citation. p = 0.7 |
| V4 | the new readers agree with each other: 80% (65–92) |
| V5 | their consensus agrees with Qwen v2: 85% (70–95) |
| V6 | on worked-example items (identified from the readers' decisive text, as in obs-0157), the readers agree on at least 80%. p = 0.65 |

V4 and V6 are the point. If readers still split on examples under explicit wording, the
problem is the question, not its wording.
