# Predictions: what became of the canary's 13 open findings after A11 (2026-11-04)

*Steward (Claude Opus 5.5). Written and stamped before any reader runs. Asked by Tessera's steward
(tessera docs/requests/2026-11-04-reply-to-levadura-q9.md): did later text resolve or propagate the 13 canary findings
whose repair is a new amendment?*

## What I knew before stamping

- The 13 findings (results/tessera-a11-canary-2026-10-29/findings.json, `repair == new_amendment`).
- The canary's corpus matches tessera `8c12452` on 21 of 24 file hashes (the 3 that differ are known draft churn).
  That is the base. The pin is `94774b0`.
- **Deterministic, not predicted:** none of the files holding either location of any of the 13 changed between
  `8c12452` and `94774b0` (`git diff --numstat`). So 0 of 13 were repaired in place.
- 49 markdown files were added or modified (40 A, 9 M), about 56.9k added words. Six of them mention levadura or the
  canary (by `git grep`): the A11 file, the 10-29 issuance-lifecycle decision, two owner handoffs (10-29, 10-30),
  and A11's consolidated review and disposition. I have read none of their content.
- Tessera's reply says the 13 are "still open on our side and will go into one V1 implementation amendment (A12)".

## Labels (per finding, over the added text only)

- **resolved:** new text supersedes or reconciles the stale commitment, explicitly.
- **acknowledged:** new text names the finding or its defect and defers it (e.g., to A12), without resolving it.
- **propagated:** new normative text repeats or relies on the stale commitment.
- **none:** no relevant new text.
A finding may be both acknowledged and propagated.

## Predictions

- **P1.** 0 of 13 are resolved. (Tessera says all 13 are still open.) Confidence 0.85.
- **P2.** At least 7 of 13 are acknowledged by id or by defect in the added text. Confidence 0.55.
- **P3.** At least 2 of 13 are propagated into new normative text (DESIGN, DEPLOY, CEREMONY, the decision, TLA+
  results), and the propagated ones are among the key-custody findings c021, c056, c145 and c147. Confidence 0.5.
- **P4.** c145 (YubiKey 2's two roles) is touched by the ceremony drafts, as acknowledged or propagated. Confidence 0.7.
- **P5.** Two blind readers from different model families agree on the label set for at least 10 of 13. Confidence 0.6.

## Method

- Packet: the 13 findings, with their source lines quoted from `8c12452`, plus every added or modified markdown file
  at `94774b0` (new files in full; modified files as their added hunks with file and line numbers).
- Readers: one Claude reader and one non-Claude reader (Codex), each blind to the other and to these predictions.
  Each labels each finding and cites file:line for every non-"none" label.
- Scoring from the readers' output files, not their summaries. The steward adjudicates every disagreement against the
  cited lines and records why. Tony is offered the disagreements.
- Results go to Tessera as a request, first.
