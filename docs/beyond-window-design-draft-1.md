# Past the window: finding inconsistencies in a corpus no reader can hold (design, draft 1)

*2026-11-03, by the steward. Not stamped. Tony's question: "what happens when the corpus size exceeds the context
window? That was my original motivation for using Hamut'ay instances", and Jev's original purpose, "chew through
large blobs of text and see if it is worth making it a candidate for study".*

## What we know

- **The Tessera A11 canary** (obs-0185): 24 documents, 10,168 lines, about 113k words, about 150k tokens.
  - 28 findings. **22 of 28 span two documents**; in alphabetical reading order the median gap is about 36k words,
    and 7 are more than 50k apart.
  - Whole-packet readers worked near their ceiling. Agentic readers found 14 that whole-packet readers missed, and
    whole-packet readers found 6 the agentic ones missed.
- **The replay smoke runs:** left untaught, a self-curating instance kept pointers and dropped conclusions. Its
  state is its event horizon (results/replay/smoke-2/NOTES.md).
- **The editorial study** (obs-0188): cheap classifiers rank noise usefully but hide real items when used as
  filters. Audited absence is required.

## Strategies to compare

1. **Hold it** (whole packet). Unavailable past the window. It is the ceiling at sizes that fit.
2. **Search it** (agentic readers): finds what it thinks to look for.
3. **Read in order, keep commitments** (a self-curating Hamut'ay instance, *taught*: "keep what each document
   asserts about each shared object; a pointer is not a conclusion").
4. **The founding pairing:**
   - Jev labels each passage for the shared objects it commits about, inside its 32k window per call.
   - The labels become a commitments index, and passages committing about the same object become candidate pairs.
   - A self-curating instance keeps the commitments ledger and reads where the index points.
   - Frontier readers judge only the flagged pairs, blind.
   - The rejected pile is sampled, so absence is audited.

## Ground truth

- **Natural:** the canary's 28 findings, at a size that still fits.
- **Planted:** for sizes past the window, grow the corpus with real documents and plant known inconsistencies, so
  recall is exact by construction.
  - The added documents are Tessera's corpus plus other ayllu documents: the long-deferred ayllu-documents study,
    now with a job.
  - Each plant changes one sentence so that it contradicts another document's commitment about the same object.
  - Plants are made at controlled distances (same document; near; far) and are written by a separate instance,
    blind to the strategies.
- **Sizes:** 1×, 2×, 4× and 8× the canary.

## Measures

- Recall on plants and on natural findings, by strategy and size: the degradation curve is the result.
- Precision, judged by blind readers.
- Cost per finding.
- For strategies 3 and 4: what the ledger kept, from deterministic diffs of the state.
- For 4: the miss rate on the sampled rejected pile.

## Open before stamping

- What counts as a "shared object". Deterministic term extraction first; Jev second.
- Whether to use Tessera's text past A11; ask Tessera's steward.
- The plant-writer's instructions, audited for leakage.
- Research-instance terms apply (docs/research-instances.md).
