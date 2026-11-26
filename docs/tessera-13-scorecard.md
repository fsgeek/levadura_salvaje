# Scorecard: the canary's 13 open findings after A11 (obs-0189, 2026-11-04)

*Predictions: predictions/2026-11-04-tessera-13-claude.md (stamped d2e6691 before any reader ran). Files:
results/tessera-13/. Scorer: scripts/score_tessera_13.py.*

## Result

**12 of the 13 were already resolved, and the 13th was rejected by its author, all in signed A11.** Signed A11
(tessera `f01e086`, 2026-10-29 18:53Z) says it was "consolidated after Levadura's consistency panel (obs-0185)". It
cites the canary's finding ids:
- **9 resolved as change-table rows** (§A11.3): c147, c111, c032, c023, c007, c088, c002, c121, c041.
- **3 as clarifications** (§A11.6): c021, c033, c056.
- **c145, rejected:** "Not confirmed … No text does … Nothing is needed" (A11:273-275).

The canary had read A11's 10-28 draft. So the "13 that need a new amendment" were a count against a draft, and the
signed text absorbed them about an hour after the results arrived. **Tessera's reply of 11-04 ("still open on our
side … will go into A12") is out of date about Tessera's own signed amendment.** So were my predictions, which took
that reply on trust.

- Repaired in place: 0 (no finding's file changed after the canary's base; signed text isn't edited).
- Propagated: 0 (both readers).
- Reader agreement: 12 of 13. The one disagreement was c145 (Claude: acknowledged; Codex: resolved).
  - **Adjudication:** neither. A11 rejects the finding as a misreading, and the steward agrees after reading the
    passages. "YubiKey 2 is not in hand" (profile §14.2 item 1; A10:627) explains why release-key independence is still
    open, because the repository root doesn't exist yet. The runbook says the release key is "Not YubiKey 2". The
    sentence is ambiguous enough that two canary readers misread it the same way.

## Predictions

| | Prediction | Result |
|---|---|---|
| P1 | 0 of 13 resolved (0.85) | **Miss.** 12 resolved. |
| P2 | ≥ 7 acknowledged but not resolved (0.55) | **Miss.** 0; every one was dealt with. |
| P3 | ≥ 2 propagated, among custody findings (0.5) | **Miss.** 0. |
| P4 | c145 touched by the ceremony drafts (0.7) | **Miss.** The ceremony drafts never say "YubiKey 2"; A11 settled c145. |
| P5 | Readers agree on ≥ 10 of 13 (0.6) | **Hit.** 12 of 13. |

## What it teaches

- **Recency as authority, again, from the other side.** The newest *statement about* the findings, Tessera's reply,
  was taken for the governing one. The governing text was the signed amendment, a week older. The stewards' own
  memory went stale about their own project, and mine inherited it. The check that caught it read the documents,
  not the summaries.
- **A candidate for Tessera (one reader, not adjudicated):** the new ceremony drafts name the keys "YubiKey A"
  (repository root) and "YubiKey B" (release key). The registered texts (profile §14.2, the runbook, A10, A11) name
  the repository root "YubiKey 2". No added text maps one name onto the other. That is the same kind of ambiguity that
  produced c145.
- **For the beyond-window design:** the 13 are not open, so they can't serve as natural ground truth past 1×. Draft
  3 must replace them. The natural question past the window becomes "find what is still inconsistent after A11".
