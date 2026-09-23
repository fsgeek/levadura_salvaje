# The First Wander

*2026-09-22. Written after the seed was committed unedited (`a71f301`) and
before anything was measured. It records how the seed was challenged, what
survived, what didn't, and why.*

The wander had three voices. Tony asked the questions. Sol (ChatGPT 5.6)
expanded each one generously. A Claude Opus 5.5 instance sifted the result.
Sol's example numbers were illustrations, not data, and are not carried
forward here.

## What the seed was challenged on

1. **The wager is less contrarian than it claims.** Tools, retrieval and
   agents are already mainstream. The claim that is new is narrower:
   *population-level semantic measurement* (asking every document a question
   and getting back a distribution, not a top-k list), and *instances that
   specialize through accumulated experience*.
2. **The instruments need falsifying too.** §10 turns falsification on
   hypotheses, but the cheap classifiers in §3 are the measuring devices. A
   distribution of uncalibrated guesses over ten million documents looks more
   authoritative than five retrieved ones without being any more true.
3. **"Same genome, different lives" (§4) is testable, and should be tested
   early.** Does an experienced instance beat a fresh one given the same
   tools and the same index?
4. **The Radiant (§12–14) comes later.** It is aspirational, and it is the
   most enjoyable thing here to design and the least necessary. Tessera is
   the cautionary case: the comfort of designing in a complex space.
5. **§17 had no failure condition.** "Something unexpected will glow" cannot
   fail. The loop in §16 can: hypothesis → test on the population → found
   incomplete → remember why → suspended → woken → continue without
   re-deriving.

## What survived

**The thesis, in one sentence:**

> A persistent investigator that is allowed to forget its words but cannot
> misremember its data.

It combines three pieces, and to our knowledge nothing else combines them
yet:

- Hamut'ay's rewrite-memory, with its declared-losses changelog;
- cheap measurement of the whole population
  ([Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev),
  released 2026-09-15);
- OTS pre-registration, applied by the investigator to itself.

**The structure:** many stateless observers feed one stateful inquirer.
Bulk computation stays with the data, and cognition works on measurements
of the data. Measurements go into an **append-only, timestamped ledger**.
The investigator's working state may rewrite its *interpretations* freely,
but it must *cite ledger entries*, never restate numbers from memory. Drift
between a claim and the entry it cites can then be detected by machine.

The seed's §8 maps almost exactly onto a Jev call. Lens L is an output type,
question Q is a field description, model M is a version string, and P is the
probabilities it returns. The observation record *is* the request and the
response.

**Tiny context as an advantage** is an open hypothesis worth testing. An
investigator holding only hypotheses and ledger references may reason better
than one given a larger desk.

## The recurring weakness

It surfaced four times: in deciding which metadata to surface, in claims of
absence, in routing, and in `falsify()`. **When a cheap judgment selects what
gets examined, its errors hide in whatever wasn't selected.**

- **Exploration budget.** A small random share of every selection decision
  (sources, instruments, routes, the "no" pile) gets the unselected treatment
  anyway, and the outcome is logged.
- **Audited absence.** No absence claim is made without a measured miss rate
  from a hand-labeled sample of the rejected set. When a property is rare,
  classifier false negatives can outnumber the true positives.
- **Separation of duties.** The proposer stamps the hypothesis. A different
  instance, or a lens written blind, turns it into the falsification test.
  Otherwise the proposer picks a test it can pass.

The feedback loop also has a sampling bias. You learn whether a source helped
only when you consulted it. Without exploration, the logs confirm the
classifier's existing biases.

## Caveats about Jev, from the vendor's own materials

- "Calibrated" is measured against reference probabilities from frontier
  models, not against ground truth.
- "0% hallucination" means the output always matches the schema, not that the
  answers are correct. In their words, the number "is not empirical."
- `confidence` is a margin from the decision threshold, not P(correct).
- The window is 32k tokens per call for the state plus the longest question.
  Outputs cannot be free text.

Scale, meaning throughput and rate limits, is a production question and is
deliberately deferred. The goal is to show the potential first.

## What didn't survive

- **"There's no way to do this with current frameworks."** You can bolt
  DuckDB onto an agent today. What is missing is the boundary as a basic
  abstraction: cognition works on measurements, not on data.
- **Provenance as the novelty.** Databricks has lineage. What remains ours is
  the investigator that *remembers why it asked*.
- **"Learned semantic query optimizer."** Jev's weights are fixed. Any
  learning happens in our layer: budget allocation, source descriptions,
  thresholds.
- **A reading of two remembered numbers as drift.** Retracted the same
  afternoon. The instance had actually changed. See
  [The Fossil Was Mine](https://wamason.com/ayllu/the-fossil-was-mine/).
  Lesson: a number with no time of measurement cannot tell drift from change,
  so the ledger records *when measured* next to *what*.

## The first rung

One lens, one small population, and results that must survive a Hamut'ay
rewrite cycle without drifting from the ledger. Before that comes the ledger
itself, tested on data that needs no classifier. Predictions are
pre-registered and stamped before Jev is touched: Tony's and Claude's,
separately.

*If this document has drifted from the conversation it records, the
conversation is in llm-memory under `levadura-salvaje`. Believe the record.*
