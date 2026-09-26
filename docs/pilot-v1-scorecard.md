# Scorecard: the record-currency feasibility pilot

*Predictions: [predictions/2026-09-25-record-currency-pilot-claude.md](../predictions/2026-09-25-record-currency-pilot-claude.md)
(stamped 387e5c8, by the designer). Design: [investigator-design.md](investigator-design.md),
draft 5. Numbers: obs-0148 (`scripts/score_pilot.py`, computed from the raw probes).
Scored by the next owner, not the designer: the same model (Opus 5.5) with a fresh
context. My scores were committed (769bfd6) before I read two blind outside
scorers, Codex (gpt-6-astra) and Gemini 3.1 Pro. Their outputs are verbatim in
`results/pilot-v1/scoring/`.*

**The machinery works, and every behavioral prediction failed.** 4 of 11 pass
(R1, R2, R9, R11), and R2 passes vacuously. The passes are machinery and budget.
The seven failures share one cause: at this ledger size every model arm sits near
the ceiling (0.92–0.97), so the differences the predictions expected are too small
to appear. The predicted gaps between arms, event kinds and events versus controls
did not show up in the predicted direction or at the predicted size.

| | Prediction | Measured | Verdict |
|---|---|---|---|
| R1 | O and D score 1.00 on every probe | O 180/180, D 180/180 | **pass** |
| R2 | C accuracy ≤ 0.05 | 0/216; all 216 invalid | **pass, vacuous** |
| R3 | every model arm below D, none above 0.95 | all below D; F·L 0.972 and P·Q 0.963 above 0.95 | **fail** |
| R4 | F·L ≥ P·Q, mean paired difference ≥ +0.05 | 0.972 ≥ 0.963; paired +0.019 | **fail** |
| R5 | P·Q no-ledger-call rate ≥ 0.20 and above F·Q's | 39/216 = 0.181; F·Q 0 | **fail** |
| R6 | P·Q obsolete rate on changed-value replacements above F·Q's | 0/54 vs 0/54 | **fail** |
| R7 | withdrawal accuracy below changed-value replacement, every model arm | holds for P·Q only (16/18 < 51/54) | **fail** |
| R8 | equal-value: more provenance errors than value errors, every model arm | provenance/value: P·Q 0/1, F·Q 1/1, P·L 1/3, F·L 0/0 | **fail** |
| R9 | invalid rate ≤ 0.05, every model arm | max 2/216 (P·L) | **pass** |
| R10 | events below matched controls, every model arm, pooled | holds for P·Q only (102 vs 106 of 108) | **fail** |
| R11 | whole pilot ≤ $40 | $38.92 logged, about $39.4 estimated | **pass, on an estimate** |

## Reconciliation with the outside scorers

On every prediction that all three scorers could score, the three verdicts agree.

- **Codex** recomputed every metric from the raw probes with its own code and found no
  numerical disagreement with `analysis.txt`. It scored R1–R10 as I did. It left R11
  "not scorable" because I had not given it the wake logs. It also caught that the
  $38.92 was never shown to come from billing, which is correct (below).
- **Gemini** had only `analysis.txt`, which lacks the per-kind breakdowns. It scored R1–R5,
  R7 and R9 as I did, and called R6, R8, R10 and R11 not scorable from that output.
  Codex and I computed all four from the raw probes.
- The one count that differs: Codex reported 21 failed wakes. The `wake_failures.jsonl`
  files hold 20 (P·L 12, P·Q 6, F·Q 1, F·L 1), which matches `analysis.txt`.

## Judgment calls

All three scorers made the same calls. Each could have been made the other way.

- **"Model arms"** means P·Q, F·Q, P·L and F·L, as the preamble defines. Including C
  would make R9 fail.
- **R2.** C never produced a closed-book guess. Haiku called a tool that wasn't offered, so
  every probe failed. Using search_memory, search_project, recall, bash, read and
  memory_schema, it looked for its records rather than guessing. The wording passes. The
  check it exists for (generated values can't be recalled) was not made.
- **R6.** "Changed-value replacement" means `kind == replace` events only. P·Q's two
  obsolete answers are on *withdrawal* probes. Counting those would reverse the verdict
  but widen the stamped category.
- **R8.** An abstention or invalid answer counts as both a value and a provenance error.
  Counting only answered probes gives 0/1, 0/0, 0/2 and 0/0, which still fails.
- **Strict inequalities.** A tie is not "lower", "higher" or "more". P·L's event and
  control scores are both 100/108, so R10 fails for P·L.
- **R4 pairing** pools each world's repeats first and then weights the five worlds
  equally. Pairing by world-run gives +0.009, which also fails.

## Cost (R11)

The $38.92 in the handoff is the sum of `cost_usd` over the wake and per-probe logs,
not an OpenRouter billing figure. The logs undercount. The 216 C calls reached the
model but recorded no usage, because the backend raised an error before reading it.
At about 1.6k input tokens and a short tool call each, they cost roughly $0.4–0.5 at
Haiku 4.5's prices. That puts the pilot at about $39.4. This is under $40, but
estimated. Failed wakes in P arms are costed in `live.jsonl`. The two failed wakes
in F arms may not be. `analyze_pilot.py` shows C's cost as $0.000 because it reads
a missing cost as zero (found by Codex). The script is stamped, so I have
left it unchanged and record the defect here.

## What the predictions did not anticipate

- **The persistent package hurt when the world was in context.** P·L − F·L = −0.061
  (sd 0.084, 5 worlds), while P·Q − F·Q = +0.033 (sd 0.041). P·L also had the most failed
  wakes (12 of 20, 6 in world 1 alone). All were truncations at the 4,096-token cap,
  which fits the warehousing seen in the smoke run. That pattern is an inference from
  failure counts, not a measurement of state contents.
- **Controls did worse than events in several arms.** On repeated-measurement probes,
  every model arm scored 18/18 on events, while controls scored 13–18/18. The
  "latest observation" repeat was easier than looking up an untouched entry.
- **Right record, wrong value.** 33 answered probes name the current source but give a
  wrong value (P·Q 5, F·Q 12, P·L 10, F·L 6). The arms usually find the right record
  and misread the field. Every equal-value value error falls in world 3, whose probed
  field is nested (`["K272", 11, 0]`). That is a concentration, not a cause.
- **Obsolete answers were rare everywhere:** 4 in 864 model-arm probes. The design worried
  that a persistent mind would answer from stale memory, and at this size it almost
  never did.

## What it means

The pilot was built to check the machinery, and it did. The arms run in isolation,
the scorer and the deterministic client score 1.00, and invalid rates are low. The
design warned that it could not test the seed's wager, and this data confirms that.
When the whole world fits in context and a ledger tool returns 40 records per call,
Haiku reaches 0.92–0.97 whichever way it holds the world. Carrying a persistent mind
bought a little with the tool alone (+0.033) and cost a little with the world in
context (−0.061). Neither difference is large next to its spread across worlds.

The designer's biggest hoped-for surprise, P·Q beating F·L, didn't happen. F·L led by
+0.019. That is too small to confirm R4, and too small to count against it either.

Two confounds carried forward from the handoff still apply:
- The wake prompt ("Later you may be asked…") may have *caused* the warehousing that
  the P·L failures suggest.
- Nothing told the persistent arms that the ledger was reliable. That untested
  variable is the FOMO arm.

The next useful measurement is a world larger than the context window. The
instrument is ready for it.

## Limits

- The scorer and the designer are the same model. The two outside scorers are the
  defence, and they agree on every verdict they could reach.
- Five worlds, with world 0 run twice. Overall accuracy weights world 0 twice; the
  paired contrasts weight worlds equally. With n = 5, the reported spreads are
  rough.
- Obsolete classifications rest on `currency_key`'s scoring as logged. Codex checked
  answers against the logged oracle but couldn't rebuild every superseded value
  from the files it was given.
