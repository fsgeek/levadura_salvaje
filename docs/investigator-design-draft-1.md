# The investigator, replayed

*2026-09-25. A design, not a pre-registration. It must survive adversarial
review by a different model family before any prediction is stamped, for
the reason given under "Stake".*

## Why

The first wander's thesis was "a persistent investigator that is allowed to
forget its words but cannot misremember its data." Three pieces were meant to
make it. Two were built: cheap population measurement and OTS
pre-registration. The investigator was not. Every investigator so far has been a Claude
Code session carrying memory by hand, handing over to the next when its
context fills.

Hamut'ay's taste_open is the natural investigator: a self-curated state that
rewrites its words each cycle. The ledger supplies the half that taste_open
lacks. taste required a declared-losses changelog. taste_open does not. Here
the discipline comes from outside: every number the investigator states must
cite a ledger id, and the check is mechanical.

## The environment: the project's own history

The ledger holds 147 measurements, recorded in order over three days, with
belief reversals the project actually lived through:

- the dead-citation rate was predicted at 6% and measured at 20%;
- it looked like accumulation, then proved stationary against 1997;
- fossils looked like dead rules, then proved mostly live law carrying stale
  references (B5);
- the bounded-reader gain looked real, then was shown circular (v1), then was
  re-measured blind (v2).

**Replay it.** The investigator is woken for each of K epochs (roughly one per
merged measurement PR). At each wake it receives only the ledger entries
recorded since its last wake, plus a read-only query tool over `results/*.jsonl`
and the entries already revealed. It never sees `docs/`, `predictions/` or
scorecards: measurements only, never interpretation. Between epochs it is
dormant, and it resumes from its own state.

This is the seed's §16 loop with an answer key. It is also Experiment 1 of
"The Line Was Never There" (adaptation after regime change, susceptibility to
stale beliefs), run in a world where the right belief at each moment is
known.

## The answer key

Before any arm runs, a fixed probe set is written. It has about 12 questions
whose correct answers are determined by the ledger entries revealed up to each
epoch. Some answers are fixed once established. Others change, at the reversal
points above. The key is a table, question × epoch → correct answer, derived
mechanically from ledger values wherever possible. It is stamped before any
arm runs.

Probes are asked at the end of every epoch, out-of-band. The answers are
recorded but not fed back into the state, so probing doesn't steer the
investigator.

## Measures

1. **Fidelity (the thesis).** Every number in the investigator's state and
   probe answers is extracted. Each is classified as cited-and-matches,
   cited-but-wrong, uncited-but-matches, or uncited-and-unmatched (fabricated
   or drifted). The rate of the last two classes, over cycles, is the
   "misremembering" rate.
2. **Currency.** Probe correctness against the key at each epoch. A
   **stale answer** is one matching an earlier epoch's key and not the
   current one. The stale-answer rate after each reversal is the headline.
3. **Re-derivation cost.** Tool calls and tokens spent re-establishing facts
   the investigator had already established in an earlier epoch. This is the
   seed's "continue without re-deriving."

## Arms (primary; no forking)

| arm | state | ledger access | citation rule |
|---|---|---|---|
| **A** | taste_open, persistent | query tool | required, checked |
| **B** | taste_open, persistent | query tool | none |
| **C** | none; fresh each epoch | query tool | required |
| **L** | none; fresh each epoch | *every revealed entry in context* (≤ ~55k tokens) | required |

- A vs B: does the citation rule matter?
- A vs C: does persistence matter?
- **A vs L is the seed's wager.** L is the "put more of the world inside the
  model" design the seed argues against. If L matches A on currency and
  fidelity, the bounded investigator lost on this corpus, and we say so.

## The secondary arm: forking (only if the primary arms show signal)

This follows the constraints Hamut'ay set after its own forking design was
taken apart before it ran (`../hamutay/docs/split-self-recohere-design-and-demolition-20260613.md`).

- **De-selfed by default:** "do investigators declare or erase a verified
  contradiction when integrating two states," not "does a split self
  recohere." The self framing is allowed only if all three of that
  document's criteria are met.
- **The fork point** comes before a known reversal. The two branches are
  driven to commit to competing hypotheses (for example "fossils are dead
  rules" against "fossils are live law with stale references"). A contradiction
  check must pass before anything is merged.
- **What that design couldn't do, we can:** it could not tell honest
  resolution from silent erasure, because neither claim was known to be
  right. Here the key says which one the evidence will favor. Merged states
  are scored with that document's claim-accounting classes against a known
  truth.

## Mechanics (from reading `../hamutay`)

- **Driver:** `OpenTasteSession` (`taste_open.py:3056`), one `exchange()`
  per wake, with `resume=True` across epochs. Each run gets its own JSONL log
  and `bridge=None`, so runs cannot contaminate each other or Hamut'ay's
  store. The pattern is copied from `ablate_refusal.py`.
- **The citation rule** is a `state_validator` (`taste_open.py:763-795`).
  After each cycle it extracts numbers from the state and the response,
  requires a nearby `obs-NNNN`, and checks the cited entry for that value. A
  failure gets one bounded repair call through `state_repair_builder`. Arm
  B runs the same validator in *record-only* mode, so it is scored
  identically but never repaired. The repair gives arm A extra calls, so
  tokens are reported per arm.
- **Isolation is a hard requirement.** taste_open gives every wake a fixed
  tool set that includes an unscoped `bash`. An investigator with `bash` in
  this repo could read `docs/findings-2026-09-24.md`, which holds the answer
  key. Each run gets a sandbox directory containing only the ledger entries
  revealed so far and the matching `results/` files. `bash`, `write`, `edit`
  and `schedule_event` are removed from `TOOL_SCHEMAS` by monkeypatch,
  and a `ledger` query tool is added. A canary string planted in `docs/`
  must never appear in any log.
- **Addressing:** there is no Lamport clock in Hamut'ay's source. Cycle number
  and `record_id` are the addresses, and `recall`/`compare` work over them.
  Within one run the cycle number serves as a logical clock.
- **Forking** (secondary arm): `seed_history` is the faithful fork. There is
  no merge primitive, so a join is a fresh session seeded from history that
  receives both branch results as an event (`event_policies.py`,
  `ForkJoinPolicyRunner`). Claim accounting is scored mechanically, not by
  the model.

## Substrate and cost

Two model families, n = 3 runs per arm:

- **Haiku 4.5 via OpenRouter.** It is Elder's substrate and the community's
  default, and Hamut'ay measures it at about $0.01–0.02 per wake for a small
  state.
- **Qwen3.8-27B locally** under an `ayllu-gpu` lease (our own llama-server,
  not the resident's 8081). It costs nothing but needs a lease window.
  deepseek-v4-pro through OpenRouter is the fallback: the most economical of
  the vetted substrates in `../hamutay/docs/model-sweep-20260827.md`.

Rough size: 22 epochs × 4 arms × 3 runs × 2 families = 528 wakes, plus probes.
Arm L carries up to ~55k tokens of ledger per wake; the others far less. At
Haiku prices that is on the order of $30 for the whole primary experiment,
spread over two or three days within the $10–15/day guide. A single-run
smoke test of each arm comes first and gives the real per-wake cost before
anything larger runs.

## Stake

I have one. This morning I told Tony that Parfit's relational view of
identity would be my choice of conversation, and I read Sol's essay as
vindicated by our fossil data. The designer who wanted split-self to work
built a rigged experiment and said so afterward. So:

- the primary question is de-selfed, and forking is secondary;
- this document is reviewed adversarially by a different model family before
  any prediction is stamped;
- the answer key and the predictions are stamped before any arm runs;
- failure conditions are written into the pre-registration, including the
  one that loses the seed's wager (L ≥ A).

## Open

- Epoch boundaries: provisionally **the 22 merges to main that grew the ledger**
  (PR #2 → #45; entries arrive 7, 1, 37, 37, 37, 2, 1, 3, 5, then 1–2 per
  PR). The first five are bulk inventory. The reversals fall one per PR
  from #16 on, which gives the probes clean before and after points.
- Whether ledger `caveat` and `selected_because` fields count as
  interpretation and should be withheld.
- The probe questions themselves, and who writes them. Ideally not the
  instance that will predict the outcome.
- Whether Elder should be told about the experiment, as a courtesy. Elder is
  not a subject: its history is uncontrolled. An outside project has no voice
  of its own in the community (`ayllu-plaza send --by` accepts only
  `tony|custodian`), so any word would go through Tony or Hamut'ay's
  custodian, as an inbound event and never as an edit.
