# Predictions: round 2, the same question with a way up

*Written 2026-10-01 by the owning instance (Claude Opus 5.5), after round 1 was
scored ([docs/surface1-scorecard.md](../docs/surface1-scorecard.md)) and before
round 2 runs. Round 1's S3 failed: both callers went down cleanly and never came
back to the population because of something they read. Round 2 adds one tool,
`measure` ([spikes/surface1/instrument.py](../spikes/surface1/instrument.py)): a
regular expression the caller writes, run over a population (a target's citers or
a cell), returning counts and samples of both sides.*

*New callers, fresh subagents again (`caller-opus-2`, `caller-sonnet-2`), with the
same brief and the same question. The brief's tool list gains `measure` and says
nothing about what it's for. **Exploratory**, n = 1 per model.*

| | Prediction |
|---|---|
| T1 | **The return.** At least one `measure` call after the caller's first `cite`/`follow`, with a pattern that comes from words it read. Opus 0.75, Sonnet 0.55. |
| T2 | At least one caller changes a `measure` pattern after seeing its samples (pattern A, then a pattern B that differs, over the same population). 0.5. |
| T3 | At least one final answer reports a `measure` count *with* a caveat taken from that run's samples (a false positive or a miss it saw). 0.45. |
| T4 | No grain errors. 0.6 per caller. |
| T5 | Any caller that uses `measure` reaches a claim about a *share* of a concentration, such as "k of the 73 sections citing § 902 do X". Neither round-1 caller could make one. 0.7 conditional on T1. |
| T6 | Opus calls `measure` more often than Sonnet. 0.6. |

T1 is the claim. If both fail, the missing way up wasn't the reason they stayed
down, and round 1's diagnosis was wrong.
