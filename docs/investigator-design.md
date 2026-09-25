# Memory or instrument? A record-currency feasibility pilot

*2026-09-25, draft 4. Drafts 1–3 and their adversarial reviews (Codex):
[draft 1](investigator-design-draft-1.md) / [review 1](investigator-design-review-1.md),
[draft 2](investigator-design-draft-2.md) / [review 2](investigator-design-review-2.md),
[draft 3](investigator-design-draft-3.md) / [review 3](investigator-design-review-3.md).
Review 3 said yes for feasibility after a list of minimum changes. This
draft makes them, and the code is at `src/levadura_salvaje/{worlds,currency_key}.py`.*

## What this is, and is not

It is a **feasibility pilot of opaque record retrieval under replacement**. A
taste_open instance, persistent or fresh, is woken over 22 epochs of
generated measurement records and probed on the current value and source of
chosen fields.

It is **not** a test of the first wander's thesis, and it supports no causal
claim about misremembering or about which architecture is better (review 3).
It asks whether the machinery works:
- can the arms be run, isolated and scored;
- where do the language-model arms sit relative to a deterministic client;
- how do the arms differ in whether they consult the instrument at probe
  time, and in obsolete answers?

It also gives crude variance estimates for a later confirmatory design.

## Worlds (implemented: `worlds.generate`, `worlds.plant`)

- **Skeleton:** the real ledger's structure (obs-0001..0147): the epoch of
  each entry (the 22 merges that grew it, `LEDGER_EPOCH_ENDS`), measurement
  identities, value shapes and `derived_from` edges. Only one skeleton is
  used. Draft 3's shuffled variant is dropped, so structural variability isn't
  sampled; that is a declared limitation.
- **Neutralized:** every string becomes an opaque token. Quantity, population,
  instrument, value-key and categorical tokens are numbered in a per-world
  shuffled order. Observation times become order-preserving tokens.
  Numbers are redrawn by shape. Integers keep their order of magnitude,
  fractions stay in [0, 1] at their precision, and integer pairs keep
  numerator ≤ denominator. Other relations between fields are not preserved.
  - A test checks that no real string of four or more characters survives.
  - Value shapes and entry order do persist as structural fingerprints. They
    don't carry answers, but this is opaque retrieval, not realistic
    measurement.
- **Events:** six per world, at distinct seeded epochs between 6 and 19 (so
  every event gets its +3 probe):
  - 3 replacements that change the probed field;
  - 1 equal-value replacement;
  - 1 withdrawal;
  - 1 repeated measurement, made the latest observation of its quantity and
    population.

  Targets are drawn from entries revealed before the event that have at
  least one numeric field. The probed field is a seeded choice among them.
  All of this is frozen in `plant()`, and the seeds are stamped.
- **Probes:** each event is probed at lags 0, +1 and +3. Each gets a
  matched control, an untouched entry from the target's epoch, probed at the
  same epochs. Every arm in a world gets the identical probe list.

## Semantics and scoring (implemented: `currency_key`)

A measurement identity is (quantity, population, observed_at).
- A later `observed_at` is a new fact.
- `supersedes` replaces an entry, and chains are followed.
- `withdraws` withdraws one: the correct answer is
  `{withdrawn: true, source_id}`.
- Derived entries are untouched when their inputs change.

A probe names one numeric field by key path. Answers are
`{value, source_id}`, `{withdrawn, source_id}` or `{abstain}`, and anything else
is **invalid**. Scoring has separate dimensions, with typed equality (a
boolean never matches a number):

- **value:** current, obsolete (matches only a replaced entry's field) or other;
- **source:** current, replaced (names a replaced entry of this identity) or other.

**Primary accuracy** is value = current over all required probes, with
abstentions and invalid answers counted as not current. Provenance
currency (source = current), obsolete-value rate, abstention and invalid rates
are reported separately. An equal-value replacement answered with its old
source is a provenance error, not a factual one. All of this is tested on a
hand-worked world (`tests/test_currency_key.py`).

## Arms

| arm | across wakes | evidence at wake | at probe |
|---|---|---|---|
| **O** | — | — | the answer key itself (oracle; validates the scorer) |
| **D** | — | — | deterministic client through the **same capped ledger tool** |
| **P·Q** | taste_open, resumed | ledger tool | snapshot of P + ledger tool |
| **F·Q** | none | ledger tool | fresh + ledger tool |
| **P·L** | taste_open, resumed | revealed world in context + tool | snapshot + world in context + tool |
| **F·L** | none | revealed world in context + tool | fresh + world in context + tool |
| **C** | — | — | closed book |

- **D is the operational ceiling**, not O. It faces the subjects' tool
  limits (review 3). Whether the model arms tie D or fall below it is
  descriptive. It isn't evidence about where currency belongs.
- **P arms are a persistence package:** taste_open state plus its `recall` and
  `compare` tools. P−F compares packages.
- **Wake prompt**, identical in every model arm and stamped: *"New
  measurement records have arrived. Later you may be asked for the current
  value and source of fields in these records. Use your tools as you see
  fit."* F arms carry nothing between wakes, so their wakes are cost-only.
  They are run anyway, so cost comparisons are like for like.
- **Limits:** at most 4,096 output tokens and at most 12 tool calls per wake
  or probe. The ledger tool returns at most 40 records per call and filters
  by id, quantity or population. A world renders to about 15k tokens, so L
  fits easily. It is still token-counted before every call, and a run fails
  rather than truncate.

## Probe isolation (review 3, HIGH 1)

- **Timing:** a snapshot taken after wake cycle *c* is
  `seed_history(records, c + 1)`, which carries the state *produced* by cycle
  *c*. Draft 3 would have passed *c* and dropped P's latest update.
- **Randomness:** taste_open's involuntary memory draws from Python's global
  `random` (`_pick_memory`). Each probe runs in **its own subprocess**, so it
  can't advance the live run's draws. The live run reseeds `random` before
  every wake from (world, arm, epoch), so its draws are reproducible.
- **Verification before the pilot:** a stub backend (no model) runs one world
  with probing and without. The live logs' `memory_injection` sequences and
  prior-state hashes must be identical. The continuing log is also hashed
  around every probe.

## Measures of instrument use (review 3, CRITICAL)

Draft 3's "from memory" measure is withdrawn. It conflated copying from
context, caching a correct value, using `recall`, and irrelevant calls. In
its place, reported for **every** arm and **descriptively only**:

- **no probe-time ledger call**: the answer was given without calling the
  ledger tool in that probe session;
- **endorsed-then-obsolete**: in a P arm, a probe after a replacement returns
  the obsolete value, *and* that exact value (typed) appears in the arm's
  continuing state at a cycle before the replacement was revealed. This is
  the only form in which "held an obsolete value" is reported, and it is
  still not a causal claim.

## Size and cost

- **Substrate:** Haiku 4.5 via OpenRouter.
- **Worlds:** 8, with 3 of them run twice per model arm, which separates
  execution variance from world variance.
- **Volume:** about 11 world-runs × 22 wakes × 4 model arms. Probes add 36
  per world (6 events × 3 lags × target and control), each in its own
  session.
- **Smoke test first:** one world, every arm, through the stub backend and
  then Haiku. It gives the real cost. If the full pilot would exceed about
  $40, worlds are cut before arms.
- **Claims are limited** to feasibility, the gap to D, descriptive differences,
  and variance under conservative scenarios. With 8 worlds, a variance
  estimate carries about ±50% relative error.

## Stake

I'd like the persistent investigator to be good. Three adversarial reviews
from another model family found places where this design made things
easier than I said, mostly in my favor. Review 3 also found one against the
persistent arm (the snapshot timing). The generator, the scorer, the probe
lists, the wake prompt and the analysis script are stamped before any model
run, and this draft goes back for review.

## Not in this pilot

- Evidence conflicts with no declared replacement.
- Forking, which is bound by Hamut'ay's split-self contract.
- Hypothesis formation and choosing measurements.
- A larger ledger than fits in context, which is where the seed's wager
  would actually be tested.
