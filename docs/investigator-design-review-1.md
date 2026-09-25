# Adversarial review 1 of the investigator design

*2026-09-25. Codex (GPT family, codex-cli 0.155.0, read-only sandbox), asked to demolish
the first draft of the investigator design, preserved as
[investigator-design-draft-1.md](investigator-design-draft-1.md) (reconstructed exactly
from the session that wrote it, since it was never committed). Kept verbatim; line
references are to that draft. The redesign responds to
each point.*

**Reject this draft as a confirmatory experiment.** It can test a retrieval-and-repair system, but its proposed scores cannot establish that a persistent investigator avoids misremembering—or that the ledger vindicates the thesis.

References below use **D** = [investigator design](/home/tony/projects/levadura_salvaje/docs/investigator-design.md), **S** = [previous demolition](/home/tony/projects/hamutay/docs/split-self-recohere-design-and-demolition-20260613.md).

1. **CRITICAL — “Fidelity” rewards the intervention by definition.**  
   D:61–65 counts *uncited-but-correct* numbers as misremembering, while excluding *cited-but-wrong* numbers from that rate. B is explicitly allowed to omit citations. A receives citation enforcement plus corrective calls (D:113–119). A can therefore beat B without remembering anything better. Post-repair performance is a legitimate system outcome, but cannot establish investigator fidelity. Numeric silence also escapes the metric unless coverage is required.  
   **Fix:** Separate factual error, citation compliance, and answer coverage. Score mandatory claims before and after repair; include cited-but-wrong claims as errors. Factor citation instructions and repair into separate conditions.

2. **CRITICAL — The answer key can canonize the author’s preferred interpretation.**  
   D:27–44 treats selected historical interpretations as known truth; D:48–53 leaves “mechanically wherever possible” undefined; D:178–179 leaves probe authorship unresolved. Stamping a designer-selected key prevents later editing, not prior cherry-picking. The ledger itself labels important judgments as uncertain: [obs-0142](/home/tony/projects/levadura_salvaje/ledger/observations.jsonl:142) acknowledges circular panel evidence; [obs-0145](/home/tony/projects/levadura_salvaje/ledger/observations.jsonl:145) says truth remains model judgment and blindness rested on instructions. Reproducing those judgments is not independent vindication.  
   **Fix:** Independently author and adjudicate probes, blinded to arm identities and desired predictions. Distinguish “what this measurement reports” from warranted inference and external truth. Preserve uncertainty; add held-out investigations selected before their outcomes are known.

3. **CRITICAL — “Measurements only, never interpretation” is false.**  
   D:36–38 promises this separation, yet only `caveat` and `selected_because` are flagged for possible removal (D:176–177). Leakage also inhabits `instrument.known_limits`, `method`, quantity/value names, and filenames. Obs-0142 literally explains why the earlier reader result is biased; obs-0145 advertises the corrective blindness. [Obs-0133](/home/tony/projects/levadura_salvaje/ledger/observations.jsonl:133) supplies the interpretation of what audit agreement means. Prediction paths and hypothesis-coded fields expose the investigation’s conceptual scaffolding even without opening predictions. This contaminates thesis validation, though it need not favor A in every comparison.  
   **Fix:** Freeze an audited subject-facing schema. Preserve neutral operational definitions and necessary limitations, remove retrospective verdicts and hypothesis identifiers, pseudonymize paths, and audit result rows too. Compare annotated and neutralized versions separately.

4. **HIGH — L may be a deliberately weak opponent.**  
   D:75–80 gives A query access but specifies only ledger-in-context for L. Does L also receive raw results, querying, repair, and equivalent instructions? The draft does not say. D:150 assumes approximately 55k ledger tokens fit without specifying tokenizer, configured context, prompt/output reserve, or truncation. L is also fresh while A persists: A–L bundles memory, retrieval, and presentation.  
   **Fix:** Give L identical evidence eligibility, tools, prompts, output budgets, and repair policy; add full-context conditions both with and without persistence. Verify actual token fit on each backend and fail explicitly on truncation.

5. **HIGH — Compute differences prevent causal attribution.**  
   A receives extra repair calls; reporting tokens does not control that advantage (D:116–119). Persistent arms accumulate previous reasoning unavailable to fresh arms. State size, query limits, reasoning budgets, recall behavior, and probe-time tools are unspecified (D:55–57, 107–135). A’s advantage could be extra work or access.  
   **Fix:** Publish exact prompts and resource limits. Run both equal-budget comparisons and accuracy-versus-cost curves; provide a matched extra-call control without citation feedback. Count initialization, maintenance, retrieval, probing, and repair.

6. **HIGH — Numeric matching is not evidential support; “stale” is not yet mechanically defined.**  
   A nearby observation containing the same value (D:113–116) does not establish the right quantity, denominator, population, date, or polarity. Percentages and derived ratios may fail literal matching while incorrect claims pass. D:66–68 cannot distinguish a historical qualification from a current endorsement without structured semantics. Moreover, the designer’s former beliefs are not necessarily beliefs the investigator ever held; prediction files are withheld. A stale-looking answer may be a fresh mistake.  
   **Fix:** Require typed claims with quantity, population, time, units, derivation, and source field. Define equivalence, abstention, mixed answers, and supersession. Separately report obsolete answers and demonstrated persistence of a previously endorsed belief.

7. **HIGH — Twelve probes and three runs cannot support the advertised breadth.**  
   Repeating twelve questions over 22 epochs does not create independent investigations (D:48, 139–149). Three runs mainly sample execution variability on one chosen trajectory. No effect threshold, power justification, multiplicity rule, or uncertainty criterion defines “signal” or “L ≥ A.”  
   **Fix:** Treat this as a pilot. Specify primary endpoints and practical effect sizes, estimate variance, then power independent trajectories/reversals. Cluster inference by trajectory/run and preregister superiority or equivalence criteria.

8. **HIGH — Forking repeats two previous CRITICAL flaws.**  
   Knowing which claim is correct does **not** distinguish reasoned resolution from silent deletion (D:101–105; S:53–59). The promised mechanical claim-accounting instrument remains unspecified. Schema/prompt cues remain uncontrolled (S:61–66, 126–131). De-selfing and `seed_history` appropriately address the third flaw provisionally; they do not fix these two. “Only if primary arms show signal” adds an undefined selection gate.  
   **Fix:** Validate accounting and rationale scorers on adversarial examples first; ablate tension fields, counterbalance polarity/order/prompts, and preregister the gate and failed-contradiction reporting.

9. **MEDIUM — Contamination and thesis scope remain uncontrolled.**  
   Familiar tax text may supply pretrained answers without ledger use; existing Claude judgments may favor shared conventions. The draft establishes neither training contamination nor its absence. A docs canary (D:127) cannot certify isolation. Finally, scripted replay omits investigator-chosen hypotheses and measurements central to [seed §16](/home/tony/projects/levadura_salvaje/docs/the_seed.md:526).  
   **Fix:** Add closed-book baselines, newly generated counterfactual worlds, pinned epoch snapshots, and enforced access boundaries. Limit conclusions to replay performance until a prospective investigation succeeds.