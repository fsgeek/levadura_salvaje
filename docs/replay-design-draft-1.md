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

## The claim is an interaction (from Sol, 10-31)

| Memory | No handles | Handles |
|---|---|---|
| Append-only | A | B |
| Self-curating (taste_open) | C | D |

The claim isn't that D beats A. It's that the benefit of handles is different for self-curated
state than for append-only context. Same model, evidence, tasks and budgets in every cell.
Attestation is a later factor. It may help only auditing, which would still be worth knowing.

**Primary outcome: curation policy.** Do handles change what the agent keeps in its state?
It's measurable, because Hamut'ay records the tensor at every step. The sign is uncertain: if
handles let the agent drop evidence and then answer from its state (evidence substitution),
the interaction is negative. Stamp the direction.

**Arms against substitution:** name the authority (Zhang et al. 2026), and constrain answers to
evidence actually accessed (Agent Zero Memory, arXiv 2608.29606).

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

## Handles attest the materials, not the conclusion

From Tony's route to the Radiant (10-31): Hamut'ay instances don't keep tool outputs in
context. So each handle commits to the source bytes at its date (git and OTS, or Tessera
later). That makes substitution checkable. An auditor compares the investigator's stated
basis with the attested bytes. A handle that only names a conclusion couldn't be checked
this way.

## Lineage to cite

- **Truth maintenance systems:** Doyle's TMS (1979), de Kleer's ATMS (1986). They recorded the
  justification for each belief, did dependency-directed backtracking, and kept every
  consistent context at once. That is "explore and backtrack without losing what was explored",
  for symbolic reasoners.
- **What they never had:** evidence too large to hold, cheap and fallible instruments, attested
  sources, heterogeneous investigators, and world time on the evidence.
- **Sol's search (10-31).** Existence and titles were checked by the steward. The content
  claims are Sol's, until read:
  - MemGPT/Letta (git-backed memory),
  - Zep/Graphiti (temporal knowledge graph; validity timestamps; source-episode provenance),
  - Agent Zero Memory (2608.29606),
  - LEDGER (2608.18398, claim-to-evidence graphs),
  - TRACE (IEEE BigDataSecurity 2026, cryptographic accountability),
  - TRACE schema (2607.12480),
  - Graph of Trace (ACL 2026 demo).
- **What none of them covers,** as summarized: all are about an agent's memory of its *own*
  trajectory. None is population-first measurement of an external corpus, and none models
  applicability (which copy governs, for whom). Graphiti has world time, so three clocks
  aren't new; the entity axis is.

## Changes from reading the prior art (10-31)

A subagent read Agent Zero Memory, LEDGER, and Graphiti's paper and docs in full. The steward
checked the claims below against the source text.
1. **The citation lock binds to source bytes.**
   - Agent Zero's lock is C ⊆ O ⊆ M: opened *memory* items, whose evidence pointer may resolve
     "through intermediate summary records" (§3.1). Nothing measures it.
   - Ours logs every handle dereference.
   - Substitution, defined operationally: a claim whose citation chain ends in the agent's own
     state, not in a handle opened that step. Scored at closure, by arm.
2. **The handle key carries applicability.** `section@date@issuer`.
   - Graphiti invalidates contradictions and "consistently prioritizes new information" (§2.2.3),
     so the newest wins.
   - Agent Zero lists coexisting valid versions as future work (§7).
   - Plant concurrent-validity cases. Score "governs for entity X" apart from "superseded".
3. **Attested time, not inferred.** Graphiti's `t_valid` is LLM-inferred. Ours comes from the eCFR
   and the instruments. Score the dates the agent writes against them.
4. **A deterministic diff log of every state rewrite.**
   - Curation policy is measured from the diffs: what was dropped, and whether its handle
     survived.
   - Any LLM coding is a separate, inferred layer, checked for stability across repeated runs.
     LEDGER (§6) left this unmeasured.
   - Repeated runs are the default.
5. **The append-only arm must be under real pressure.**
   - Zep's DMR result: full context wins when history fits.
   - Zep's single-session-assistant drop is the loss of the agent's own earlier output.
   - Check that 16 months of flags overflow or degrade the append-only arm. Probe closure on the
     agent's own earlier conclusions.

## Changes from Sol's review (10-31)

1. **Identity is kept apart from interpretation.** `section@date@issuer` is a locator, not an
   identity.
   - **Evidence handle:** `artifact_digest`, `source_locator`, `issuer`, `publication_date`,
     `edition_date`, `source_span`. Immutable at registration.
   - **Applicability record:** `effective_interval`, `affected_entities`,
     `transaction_context`, `jurisdiction`, `authority_relationship`, `interpretation_status`.
     Revisable, versioned, and attributed to whoever asserted it.
   - The evidence layer never absorbs an agent's interpretation into what a handle is.
2. **Four stages, not three.** Available, then exposed, then **cited**, then **supported**.
   "Supported" is an independent check that the evidence justifies the assertion. A valid
   citation is not a valid inference. Reads are recorded at the interface, never self-reported.
3. **The smoke run must tell three cases apart:**
   - (a) a newer text supersedes an older one;
   - (b) two conflicting texts are both applicable, in different circumstances;
   - (c) two texts genuinely conflict under the same applicability.

   Case (b) is the new one. Case (c) keeps "preserve everything, reconcile nothing" from
   passing. Gold labels for all three are built independently of the model under test, and
   stamped.
4. **eCFR dates aren't legal applicability.** The eCFR is editorial, not the official CFR
   (National Archives). Dates come from it deterministically, but they don't settle
   applicability. Planted cases are checked against the Federal Register and the official
   annual edition (GPO, which levadura already reads).
5. **The append-only arm is pressured, not handicapped.** Its context limit is set from measured
   flag volume, and the same limit is used in every cell.

## Open before stamping

- **Investigator model** (the LLM under taste_open, not the evidence carrier). Decided 11-01:
  **Haiku 4.5 via OpenRouter** for the exploratory smoke runs, then one non-Claude model as a
  replication. The same model is used in all four cells of each replication. A null result on
  Haiku is informative about where substitution happens, but it can't test the mitigation alone.
- **Exploratory, then confirmatory** (Sol). Smoke runs debug the apparatus. Then freeze the
  design, choose the replication models and stamp the predictions before any confirmatory
  result is examined. Exploratory observations are declared under "What I knew".
- **Instances:** research instances only, under docs/research-instances.md. No resident is a
  subject. Refusals and stops are results, by arm. The paper's model-dependence says validate the
  delivery per model. Budget: OpenRouter, US$100 a month.
- **A smoke run** on two or three issue dates, to measure cost before any estimate (memory: cost
  estimates).
- **Where it lives.** levadura as the instrument layer; the Radiant as customer, if it gets a
  steward.
- **Applicability.** The twins finding says the newest copy isn't always the governing one. Ground
  truth for "which governs, for whom" needs a rule set, not a diff. That is the job of the cheap
  classifier, and it is out of scope for v1.
