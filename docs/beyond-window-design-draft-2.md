# Past the window: finding inconsistencies in a corpus no reader can hold (design, draft 2)

*2026-11-04, by the steward. Not stamped. Supersedes draft 1, which is kept unedited. Tony's question: "what happens
when the corpus size exceeds the context window? That was my original motivation for using Hamut'ay instances."*

## What changed since draft 1

- **Tessera granted its corpus** (tessera `docs/requests/2026-11-04-reply-to-levadura-q9.md`, commit 9e42b08). The
  grant covers every committed file up to `94774b0` and later commits, pinned by hash. It excludes session
  transcripts. Tessera asked for findings back as a request.
- **The corpus grew naturally.** Tessera's markdown at `94774b0` is about 1.25M words; the canary read about 113k.
  So the size ladder is built from Tessera's own growth, not from padding. The ayllu-documents corpus is not needed
  for the first study, and isn't used until each document's owner grants it.
- **A natural question past the window.** 13 canary findings need an amendment beyond A11 and are still open
  (Tessera will fold them into A12). Whether later text *resolved* them, *propagated* them, or left them alone is a
  question about real inconsistencies at sizes no reader holds. Planted inconsistencies are now the second kind of
  ground truth, not the only kind past 1×.
- **Definitions, budgets, the plant protocol and the ledger scoring** are now specified below. They were open in
  draft 1.

## The question

As a corpus grows past what any reader can hold, which strategy keeps finding the inconsistencies, at what cost?
The result is a degradation curve per strategy, not a single winner.

## Definitions (frozen at stamping)

- **Shared object:** a named thing that two or more documents make claims about. Examples: a field, a message type, a
  key role, an invariant, a state, a numbered rule, a defined term. Identity is by name *and scope*. Two uses of the
  same identifier for different things are two objects. That determination is itself scored (see adjudication).
- **Commitment:** a sentence or table row that asserts, as current and normative for its document, a property of a
  shared object (a value, a bound, an ordering, a required or forbidden behavior, a status). These are **not**
  commitments: quotations of other documents, hypotheticals, examples marked as such, rejected alternatives, and
  text explicitly marked superseded.
- **Inconsistency:** two commitments about the same object that cannot both hold for the same version and scope.
  **Not inconsistencies:** a later commitment that explicitly supersedes an earlier one (that is supersession, and is
  correct); and two commitments that hold for different versions or scopes (that is "both apply", the replay's
  middle case).
- **Status inconsistency:** a document's claim about its own or another document's status that the record
  contradicts. Example, from Tessera's reply: A11's header says "DRAFT … Not signed", but A11 was signed at
  `f01e086`. Signed text isn't edited, so the header stays wrong. This is a kind, and it is counted separately, because
  the right answer may be "correct and intended" (signed text is frozen) rather than a defect.
- **Finding:** an inconsistency or status inconsistency as judged by the adjudication protocol, with both locations
  cited by file, commit and line.

## Adjudication

- Two blind adjudicators from different model families, plus Tony for a random sample and for every disagreement.
  Adjudicators see the two passages and their surroundings, never which strategy flagged them and never whether an
  item is planted.
- Each item is labeled: inconsistency / supersession / both apply / status (intended) / status (defect) /
  not about the same object / not a commitment.
- Disagreements go to Tony. His label is final and the disagreement rate is reported.
- The protocol and the label definitions are frozen in the predictions file before any run.

## Corpus and size ladder

All from Tessera at a pinned commit (`94774b0` unless a later pin is declared before stamping). Markdown and TLA+
files only. Sizes in words; the ladder is cumulative.

| Rung | Adds | About |
|---|---|---|
| 1× | the canary's 24 documents, as read on 10-29 | 113k |
| 2× | post-A11 normative text: decisions, `service/issuer/`, ceremony drafts, the implementation spec, V1-PROFILE | sized at freeze |
| 4× | `docs/reviews/` (minus exclusions) and remaining `docs/` | sized at freeze |
| 8×+ | `formal/` (suites, TLA+, spikes) | up to ~1.25M (all markdown) |

The middle rungs aren't sized yet: some of those files may already be in the canary's 24. Exact rung contents are fixed by manifest (file list plus sha256) before stamping.

**Exclusions (leakage).** Every file that mentions levadura or the canary is removed from every rung: 27 markdown
files at `94774b0` (`git grep -l -i 'levadura\|canary' 94774b0 -- '*.md'`), recomputed at the pinned commit. Any
document derived from those findings would hand the answers to the readers.

## Ground truth, reported separately

1. **Canary findings at 1×** (28, natural, already adjudicated). This is the ceiling check: whole-packet readers
   were near their limit here.
2. **The 13 open findings, past 1×** (natural). For each, the question is whether later rungs contain text that
   resolves it, propagates it (repeats the stale commitment in new documents), or does neither. The gold labels come
   from adjudicators reading targeted passages: every place the finding's object is named, found by deterministic
   search, which is feasible because the object is known. That gives exact recall for propagation at every rung.
3. **New natural findings, past 1×.** Found by any strategy, adjudicated blind. These support precision and a pooled
   lower bound on recall, never exact recall. They are reported as such.
4. **Plants** (exact recall). See below.

## Plants

- **Mechanism, matched to the canary.** Most canary findings were a correct change in one place that never
  propagated. So a plant is a small amendment: the plant-writer changes one commitment about an object (a value, a
  bound, a required behavior) in one document, in that document's style, and leaves every dependent commitment
  elsewhere unchanged. One-sentence contradictions are not used. They are likely easier than real ones.
- **Writer:** a separate instance, from a different model family than any strategy's reader, blind to the strategies.
  It sees one document at a time and a list of objects, never the strategy prompts.
- **Placement:** stratified by distance between the changed commitment and its nearest dependent: same document;
  near (under 10k words apart in reading order); far (over 50k). 8 plants per distance per rung. Randomized
  positions, seeded, and the seed is recorded.
- **Density:** plants never exceed half the expected natural findings per rung, so the corpus stays mostly natural.
- **Validation before any run:**
  - Each plant must make exactly one new inconsistency, checked by two validators.
  - **Realism:** a mixed set of plants and natural findings is shown to blind judges, who say which is which. If
    judges beat chance by more than 10 points, the plants are revised. The recall curve on plants is reported with
    that judges' rate beside it.
  - **Artifacts:** diff statistics (sentence length, vocabulary, formatting) between planted and unplanted text, to
    catch surface cues.
- The plant key is held apart from all strategy runs and opened only by the scorer.

## Strategies

Each strategy has a fixed budget per rung: dollars, wall-clock time and tool calls. Each has a stopping rule, and
everything is stated in the predictions file. Every strategy's full prompt is audited by a reviewer from another
model family (Sol) before stamping, as in the replay.

1. **Hold it** (whole packet). Run only where the rung fits the reader's stated context window, recorded per model
   at stamping. Past that it is marked **unavailable**, not scored as a miss.
2. **Search it** (agentic readers with grep and read tools, no index). Stop at the budget.
3. **Read in order, keep commitments** (a self-curating Hamut'ay instance, *taught*: "keep what each document
   asserts about each shared object, with its location; a pointer is not a conclusion"). This instruction is given
   symmetrically: the append-only control gets the same guidance (the replay confound).
4. **The founding pairing:**
   - A cheap classifier (Jev; CLM or Clef if Jev is unavailable) labels each passage, within its own window per
     call, with the shared objects it commits about.
   - The labels become a commitments index; passages committing about the same object become candidate pairs,
     deduplicated by (object, document pair) and prioritized by index disagreement.
   - A self-curating instance keeps the commitments ledger and reads where the index points.
   - Frontier readers judge only flagged pairs, blind.
   - The rejected pile is sampled: stratified by object frequency and by classifier confidence, with recorded
     inclusion probabilities, and the miss rate is reported with its interval.

**Ablations** for strategy 4, so its parts can be told apart:
- 4a: the index only (pairs straight to frontier judges, no ledger);
- 4b: ledger without the index (strategy 3);
- 4c: deterministic term extraction in place of the classifier.

## Measures

- Recall by strategy, rung and ground-truth kind (plants by distance; the 13 open findings; the canary at 1×).
- Precision, from adjudication.
- Cost per adjudicated finding, from billing, reconciled with OpenRouter.
- **The ledger's content**, for strategies 3 and 4. Snapshots are taken after each document. The scorer
  diffs them deterministically and scores, for each gold object: is a commitment kept, with source location and
  commit; does a later correction replace it; is the conclusion kept, or only a pointer.
- For 4: the rejected-pile miss rate, weighted by inclusion probability.

## Owed

- **To Tessera:** every adjudicated finding as a request in tessera `docs/requests/`, and the 13 open findings'
  resolve/propagate status first, because Tessera can use it for A12.
- **To research instances:** docs/research-instances.md applies to every self-curating instance here.

## Open before stamping

- Pin the commit and freeze the rung manifests.
- Choose each strategy's reader models and record their windows.
- Set the budgets from a smoke run at 1× (cost estimates come from measured runs).
- Get the plant-writer's instructions audited for leakage.
- Run the plant-realism check.
