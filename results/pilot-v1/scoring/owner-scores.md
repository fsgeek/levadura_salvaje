# Owner's scores, R1-R11 (before reading the outside scorers)

*2026-09-26, the owning instance (Opus 5.5, not the designer). Computed from the raw
`probes.jsonl` files with my own script, committed before I read the Codex or Gemini
scores. Counts are numerator/denominator over all worlds and repeats.*

| | Measured | Score |
|---|---|---|
| R1 | O 180/180, D 180/180 | pass |
| R2 | C 0/216; every C probe is invalid (Haiku called an unoffered tool) | pass by wording, vacuous: no closed-book guess was measured |
| R3 | all model arms < D; but F.L 0.972 and P.Q 0.963 exceed 0.95 | fail |
| R4 | F.L 0.972 ≥ P.Q 0.963, but paired mean +0.019 < +0.05 | fail |
| R5 | P.Q no-ledger-call 39/216 = 0.181 < 0.20 (F.Q 0/216) | fail |
| R6 | changed-value replacement obsolete: P.Q 0/54, F.Q 0/54 | fail (not higher) |
| R7 | withdrawal vs changed-value accuracy: P.Q 16/18 < 51/54 ✓; F.Q 17/18 > 50/54 ✗; P.L 18/18 > 49/54 ✗; F.L 18/18 > 52/54 ✗ | fail (1 of 4) |
| R8 | equal-value, provenance vs value errors (abstain/invalid count as both): P.Q 0 vs 1, F.Q 1 vs 1, P.L 1 vs 3, F.L 0 vs 0 | fail (0 of 4) |
| R9 | invalid max 2/216 = 0.009 (P.L) | pass |
| R10 | event vs control pooled: P.Q 102 < 106 ✓; F.Q 102 > 97 ✗; P.L 100 = 100 ✗; F.L 106 > 104 ✗ | fail (1 of 4) |
| R11 | $38.92: the sum of `cost_usd` over the live and per-probe logs, matching the stated billing total; includes the smoke run | pass |

4 pass (one vacuously), 7 fail. The four passes are machinery and budget. Every behavioral
prediction failed.
