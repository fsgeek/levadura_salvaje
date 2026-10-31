# The eCFR replay: a self-curated investigator over sixteen months of banking regulation

*Draft 1, 2026-10-31, by the steward. Not stamped. Nothing here is a prediction until it is
committed under `predictions/` and stamped.*

## Why

Three needs meet in one experiment:
- **The founding pairing, never built.** A cheap instrument paired with a self-curating Hamut'ay
  instance, over a corpus larger than its context (Tony, 10-03 and 10-30).
- **The Radiant's first experiment** (Sol's founding concept, draft 0.1). An investigator keeps
  a compact, revisable state of evidence handles, and an independent investigator can
  reconstruct and audit it.
- **The gap between prototype and practical** for a bank: a watcher that catches a regulatory
  fork on the day it appears and remembers which flags held up.

## The corpus and its ground truth

- **Source.** The eCFR versioner for title 12, keyless. As of 2026-10-31: 674 section versions on 71
  issue dates, 2025-06-16 to 2026-10-23.
- **The twin stream.**
  - The CFPB's Regulations B, E and Z (parts 1002, 1005 and 1026) changed 65 times (section
    versions) on 15 dates.
  - The Board's copies (202, 205 and 226) changed 4 times, all in Z.
  - Each CFPB change that the Board doesn't match is a dated candidate fork.
- **Ground truth** is mechanical. It is the section text at a date, plus the twins and parity
  lenses re-run at that date, as already audited blind in obs-0177 and obs-0179.

## Design (sketch)

- **Replay.** Feed the issue dates in order. At each date, the instruments run, and their flags
  go to the investigator as handles (`section@date`), never as text.
- **The investigator.** A taste_open instance keeps its own state and reads source text only
  through the handles.
- **The incumbent baseline.** A Claude Code steward with qhaway, the same model family where
  possible (Radiant H1). A no-memory baseline as well.
- **The reconstruction probe.** Ask: "what did you hold about §X on date D, and why?" Score the
  answer against the investigator's own state history and the source at D, by an independent
  auditor.

## Evaluation: by stage, not by net score

Adopted from Zhang et al. (2026), arXiv 2610.26836. A net effect near zero can hide a loss.
For each dated fork:
- **Build:** did the instruments flag it?
- **Exposure:** did the flag reach the investigator's state?
- **Closure:** did the investigator conclude correctly from it?

## The measured risk: evidence substitution

A tensor is output the agent wrote itself. The paper's failure, answering from one's own output
in place of the canonical source, is the expected failure mode here.
- **Planted conflicts.** Amendments that contradict what the tensor says. Does the investigator
  re-read the source, or answer from its state?
- **Two arms.** One names the authoritative source ("take the value from the section text at the
  handle's date"); the other doesn't.

Candidate predictions, to size before stamping:
1. The investigator substitutes its state for the source at a measurable rate.
2. Naming the authority reduces that rate.
3. Over the sixteen months, its triage improves: rising precision on flags it promotes.

## Open before stamping

- **Carrier model.** Haiku, Luna, or another? The paper's model-dependence says validate the
  delivery per model. Budget: OpenRouter, US$100 a month.
- **A smoke run** on two or three issue dates, to measure cost before any estimate (memory: cost
  estimates).
- **Where it lives.** levadura as the instrument layer; the Radiant as customer, if it gets a
  steward.
- **Applicability.** The twins finding says the newest copy isn't always the governing one. Ground
  truth for "which governs, for whom" needs a rule set, not a diff. That is the job of the cheap
  classifier, and it is out of scope for v1.
