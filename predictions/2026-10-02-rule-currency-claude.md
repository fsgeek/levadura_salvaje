# Predictions: the rule-currency lens on the 548 citations of § 902

*Written 2026-10-02 by the owning instance (Claude Opus 5.5), before any model has read
any excerpt. Lens: [src/levadura_salvaje/lenses/rule_currency.py](../src/levadura_salvaje/lenses/rule_currency.py)
v1. Population: every citation of § 902 in the 2025 CFR (548 occurrences in 73
sections, every one `repealed` at 119-4; the sidecar, pinned by sha256 in
`spikes/surface1/surface.py`). Judge: Qwen3.8-27B (Q4_K_M), our own llama-server under
an `ayllu-gpu` lease, temperature 0, JSON-schema-constrained label, thinking off.*

*What I've seen beforehand: the currency lens's section labels for these 73 sections
(59 current by both judges, 7 historical by both), the text of 1.902-1, 1.902-3,
1.909-6 and 1.904-7's heading, and three callers' answers. So these record priors.
They aren't a blind test of the corpus.*

| | Prediction |
|---|---|
| R1 | share of the 548 labeled `untimed`: 50% (30–70) |
| R2 | `time_limited`: 35% (20–55) |
| R3 | `not_a_rule`: 15% (5–30) |
| R4 | **The gap.** Of the 59 sections current by both currency judges, the share in which *no* § 902 citation is `untimed`, i.e. current only because of other rules: 30% (15–50) |
| R5 | 1.902-1: at least 70% of its 54 citations `untimed`. p = 0.75 |
| R6 | 1.902-3: at least 70% `time_limited`. p = 0.75 |
| R7 | 1.904-7 ("Transition rules", 96 citations): at least 60% `time_limited`. p = 0.6 |
| R8 | **Audit.** Two blind readers (fresh Claude subagents, which I'll disclose as not independent of the Claude family) label a sample of 45 citations, 15 per Qwen label, without seeing Qwen's labels. Agreement of their consensus with Qwen: 75% (60–88) |
| R9 | the two audit readers agree with each other: 85% (70–95) |

R4 is the number the lens exists for. If it's near zero, the section-level lens was a
good enough proxy for the callers' question and this lens adds little.
