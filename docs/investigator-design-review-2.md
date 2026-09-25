# Adversarial review 2 of the investigator design

*2026-09-25. Codex (GPT family, codex-cli 0.155.0, read-only sandbox), on draft 2
(commit 2efe386). Kept verbatim; line references are to that commit's
`docs/investigator-design.md`. Before reading it, the author wrote down a guess at its
main finding: triviality, because explicit `supersedes` plus exact lookup reduces the task to one tool call. That
guess matched the CRITICAL below; the other HIGH findings were not anticipated.*

**Not acceptable yet as the proposed variance-estimation pilot.** It is substantially less biased than draft 1 and could become a useful retrieval-system pilot. Calling it a test of the investigator thesis still exceeds its mechanics.

All line references below refer to [draft 2](/home/tony/projects/levadura_salvaje/docs/investigator-design.md).

**Review-1 disposition**

| Point | Verdict | What remains |
|---|---|---|
| 1. Intervention-defined fidelity | **Partially fixed** | Equal citation instructions, separate accuracy, and no repair fix the central bias. Abstention still escapes error without a defined coverage denominator (87–95). |
| 2. Interpretive answer key | **Fixed for the narrowed task** | Generated reported values eliminate adjudication of historical interpretations (46–68). Generator/task selection can still predetermine usefulness. |
| 3. Interpretation leakage | **Partially fixed** | Neutralization helps, but nested value keys and categorical strings need explicit treatment; “quantity names” does not clearly cover them (58–68). |
| 4. Weak L opponent | **Mostly fixed** | Factorial arms, shared query access, and context checks are real improvements (100–124). Resource and tool equivalence remain overstated. |
| 5. Compute confounds | **Partially fixed** | Repair disappears, but numerical budgets, state limits, query payload limits, and matched total work remain unspecified (110–117). |
| 6. Support/staleness semantics | **Partially fixed** | Typed output helps; withdrawal, repeated measurements, derived dependencies, and demonstrated prior belief remain unresolved (61–95). |
| 7. Insufficient replication | **Papered over for the promised output** | “Pilot” appropriately removes confirmatory claims, but does not make eight runs a dependable basis for power planning (126–137). |
| 8. Forking flaws | **Fixed by removal** | No inherited fork claims remain. |
| 9. Contamination/scope | **Mostly fixed** | Generated values, restricted access, and replay-only scope address the main objections (24–28, 107–108, 141–149). Closed-book failure cannot certify every aspect of isolation. |

**CRITICAL — The redesign risks measuring database access while retaining investigator rhetoric (19–22, 61–68, 79–83, 112–124).**

Opaque Q/P identifiers, explicit `supersedes`, and exact-match retrieval make a deterministic policy sufficient: fetch the matching records, follow replacement links, copy the terminal value and ID. Depending on the tool response, even following links may be unnecessary. Neither persistence nor investigation is required.

This repeats the split-self failure pattern: put the relevant judgment into the schema, then credit the subject for using it. Explicit supersession is legitimate operational metadata, but success demonstrates compliance with declared updates, not discovery that evidence overturns a belief.

**Fix:** Add a deterministic lookup baseline and fully specify query responses. Call this a *record-currency benchmark*. If broader inference matters, separately test operationally defined evidence conflicts requiring resolution; simply hiding `supersedes` would create ambiguity, not intelligence.

**HIGH — “Current” is not a complete answer-key specification (50–68, 85–95, 169–171).**

The real ledger contains repeated measurements, not just replacement records: obs-0001/0002 share quantity and population but describe different cycles. Obs-0142/0145 have different samples; a newer experiment does not automatically invalidate the older report. Preserving shapes and edges does not preserve these distinctions.

After withdrawal without replacement, what is correct? Abstention? A withdrawal status? Does retracting an ancestor invalidate derived entries, or do they remain historical reports? The design provides no rule.

**Fix:** Define measurement identity, observation time, replacement chains, withdrawal answers, and dependency behavior. Validate generator and scorer with hand-worked cases before subjects run.

**HIGH — Probe weighting can manufacture the headline (82–83, 89–98).**

Probing every later epoch gives early supersessions more weight and lets long periods of easy recovery drown immediate update failures. Unspecified oversampling permits convenient endpoint selection. Forced unequal values makes change detection unusually clean and excludes unchanged-value/new-source cases that separate factual currency from provenance currency. This does not necessarily favor P; it favors whichever strategy exploits this artificial distribution.

**Fix:** Freeze S, sampling probabilities, and identical probes across arms. Weight supersession events equally; report fixed post-update lags and unchanged controls. Include equal-value source replacements. Define accuracy over all required probes, plus coverage and conditional accuracy.

**HIGH — Persistence and assessment are not operationally isolated (75–77, 110–117, 141–151).**

“Not fed back” does not establish that probe queries, answers, tool results, or rewritten state cannot enter persistent history. Equal per-wake ceilings also do not equate cumulative work. Removing general tools is defensible isolation; leaving only P with `recall`/`compare` makes this a persistence-package comparison, not a pure state effect. Its direction is uncertain.

**Fix:** Probe disposable snapshots; verify unchanged continuing state/history. Publish prompts, numerical limits, state/history bounds, query payload limits, and total costs. Label the package comparison honestly.

**HIGH — Eight worlds give a fragile variance estimate (50–53, 130–136).**

Eight independent worlds can estimate variability of **paired arm differences**, but only crudely. Even under ideal normal assumptions, sample variance with seven degrees of freedom has roughly 53% relative standard error. One run per world cannot separate execution variability from world variability; one shared skeleton excludes structural variability. Repeated epochs do not increase independent-world replication. Ceiling performance can produce a misleading zero estimate.

**Fix:** Use paired world contrasts, repeat some worlds, vary trajectories, and power across conservative variance scenarios. A second family requires its own calibration.

**MEDIUM — Full-context success is a legitimate outcome, not a design defect (118–124, 165).**

A fitting ledger may make F·L easy; Q lookup may make F·Q equally easy. That is fair at this size, but cannot settle a scaling wager. Report accuracy–cost tradeoffs and define practical equivalence. Add larger ledgers only as a separately declared regime.

**Verdict:** Fix the semantics and assessment protocol, add the deterministic baseline, and narrow the claims. Then eight worlds are acceptable for feasibility and detecting ceiling effects—not dependable confirmatory power estimation.