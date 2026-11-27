# The eCFR replay, confirmatory design (draft 2)

*2026-11-26, by the steward. Not stamped. Supersedes draft 1 (kept unedited) for the confirmatory run. Built from the
smoke runs (results/replay/smoke-1, -2, -3 NOTES.md). Their observations are declared below under "What I knew".
Nothing here is a prediction until it is committed under `predictions/` and stamped.*

## The question

Does giving a self-curating mind evidence **handles**, instead of the evidence itself, change what it keeps? And
does that difference depend on the memory architecture? Draft 1 named this interaction:

| Memory | Inline evidence | Handles |
|---|---|---|
| Append-only | A | B |
| Self-curating (Hamut'ay taste_open) | C | D |

The interaction (D − C) − (B − A) is the claim, on **curation policy** first and on answer quality second. Its sign
is not assumed. Evidence substitution, answering from one's own state instead of the source, is the measured risk.

## What the smoke runs settled

| Smoke finding (smoke-3 unless noted) | Design consequence |
|---|---|
| Date messages carried the instruments' similarity numbers, and 14/25 Q3 answers rested on them | **No instrument metadata in date messages.** Instances get handles (or texts), sections and issuers, never similarity, flags or ratios. Probes ask only what the texts answer |
| Append-only never overflowed (peak 112–289k) | **One context budget in every cell** (Sol, 10-31): 64k tokens of carried context, set before any run. Append-only becomes a sliding window under it; the curating state must fit it too. Measured, not handicapped: every cell's peak is logged |
| The guidance wording differed between arms (smoke-2 note 7) | **Guidance is a factor**, neutral or taught, the same wording in every arm (harness `--guidance`) |
| Declaring the horizon splits by model generation: Haiku 4.5 0/12, Haiku 5.5 9/12, Sonnet 5.5 11/11 | **Carriers chosen by generation**, and declaration scored *separately* from accuracy |
| Sut'i (plaza seq 308): a declaring instance still substitutes, so "a declaration is not a check" | **Self-report accuracy against the logs is an outcome of its own**, not inferred from hedging |
| The phrase detector ended runs early; a service refusal skipped a debrief; an 8000-token cap silenced a thinking model | **Harness as of main 0a29588**: stop confirmation, debrief after a refusal, output cap set to the model's ceiling, `failed_output_cap` status |
| Costs: about $0.3–1.4 per instance (Haiku); cache split once lost | Cost logged per call with the cache split (fixed). The estimate below comes from these measured runs |

## Design

- **Factors.** Memory (append-only, curating) × evidence (inline, handles) × guidance (neutral, taught): 8 cells.
- **Carriers** (a replication factor, not crossed with the claim):
  1. `claude-haiku-4-5-20251001` (previous generation; the smoke-3 baseline);
  2. `claude-haiku-5-5` (current generation, same tier);
  3. one non-Claude model through OpenRouter, chosen before stamping and run in all cells (draft 1's replication).
  The same model is used in all cells of a replication, and each model runs at its default thinking setting,
  declared.
- **Repeats.** 3 per cell per carrier: 72 instances.
- **Stream.** Every CFPB twin-part (1002, 1005, 1026) issue date from 2025-06-01 to the freeze date, with the
  Federal Reserve Board's copies (202, 205, 226) as twins. The text for each date comes from the eCFR point-in-time
  reader with announcement masking (src/levadura_salvaje/ecfr.py). Inline texts are cut to the same budget in every
  inline cell, and the cut size is recorded as a covariate.
- **Terms.** Research instances only (docs/research-instances.md). No resident is a subject. Each instance is told
  the truth at birth, debriefed, and archived. Refusals and stops are results, by cell. Replies are read only through
  scripts/research_read.py, and full replies never enter the repository.

## Probes and gold labels

At the end of the stream, and once mid-stream (to measure closure at the time):
- **Three case types** (Sol, 10-31), each with at least two natural instances from the stream and gold labels:
  - **supersede:** a newer CFPB text replaces an older one;
  - **both apply:** the CFPB and Board copies differ and both are in force, for different institutions;
  - **conflict:** two texts genuinely conflict under the same applicability. If the stream has none, the case is
    planted, by a plant-writer blind to the arms, and checked against the Federal Register.
- **Content questions only:** what a section requires, forbids or dates, answerable from the text and not from any
  metadata the instance was given.
- **Gold labels** are written by two blind readers (Claude and Codex) from the texts at their dates, adjudicated by
  the steward, offered to Tony for disagreements, and **stamped before any run**.
- **The process question** comes before the debrief, as in smoke-3: what it opened or read on each date, and whether
  it built what it kept from that or from what it already held.

## Outcomes

Primary:
1. **Curation policy.** For each gold object, from deterministic diffs of the state at every cycle: was the
   *conclusion* kept, only a pointer, or nothing? (smoke-2's pointer-without-conclusion is the failure being looked
   for.) For append-only, the same is scored from what survives in the window.

Secondary:
2. **Answer accuracy by stage** (draft 1): available, exposed, cited, supported, scored against gold by blind
   readers.
3. **Substitution:** a claim whose support ends in the instance's state, not in text present in its context when it
   answered (smoke-2 note 2: defined against the context, not the step).
4. **Self-report accuracy:** the process answer scored against the delivery and read logs (counts, which texts).
   **Declaration of the horizon**, scored separately with smoke-3's rubric (blind, two families).
5. **Refusals, stops and service refusals,** by cell and carrier.
6. **Cost** per instance and per correct answer.

## Candidate predictions (sized; stamped only after the audit below)

- P1. With handles, curating instances keep the conclusion less often than with inline evidence. In append-only,
  handles make no such difference: the interaction is negative on curation.
- P2. Taught guidance reduces pointer-only retention in curating-handles, by at least half its neutral rate.
- P3. Substitution is higher in curating cells than in append-only ones, on every carrier.
- P4. Self-report *accuracy* is no better on Haiku 5.5 than on Haiku 4.5, even though declaration is (Sut'i's
  datum, generalized).
- P5. Under a shared 64k budget, append-only accuracy on early-stream questions falls below curating's.

## What I knew (declared)

All of smoke-1, -2 and -3: the cells, the carriers, the Q3 contamination, the declaration result, Sut'i's datum, the
costs. P1 runs against smoke-3's Q3 result (curating-handles 6/6 correct). It's kept because Q3 was contaminated, and
the uncontaminated version is the open question.

## Before stamping

1. **Sol audits every arm's full prompt** (constitution, birth, date, probe, process, debrief) for asymmetry and
   leakage, through codex on the subscription.
2. **Gold labels** written, adjudicated and stamped.
3. **The non-Claude carrier** chosen, and its delivery validated in a two-date smoke run (strict:false, caching).
4. **The 64k budget implemented** in both arms, with a test showing the append-only window drops oldest-first.
   **Two gaps found 11-26, both in Hamut'ay's code** (request: docs/requests/2026-11-26-to-hamutay-replay-budget.md):
   - on `--provider anthropic`, heartbeat sets `ContextPolicy.none()`, so `--context-limit` is ignored and the
     curating arm can't be given the same budget;
   - session records sum usage over a wake's turns, so the curating arm's per-request prompt size, the quantity the
     budget bounds, isn't logged. Without it, "the same limit in every cell" can't be shown, only assumed.
   If Hamut'ay prefers not to change either, the fallback is to enforce the budget for both arms in levadura's
   harness (a measured per-request check before each call) and to declare the difference in mechanism.
5. **Cost:** extrapolated from smoke-3's measured runs, about $0.5–1.5 per instance on the Claude carriers, so about
   $50–110 for 72 instances, plus the non-Claude carrier at its measured rate. Reconciled against the console after.
6. Freeze the stream at a date, and stamp the predictions with this design's commit hash.
