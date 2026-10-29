# Predictions: is Amendment 11 the last repair, or the canary? (Tony and Claude)

*Pre-registered 2026-10-29, before any reader saw the texts. This commit's OTS stamp is the proof of that order.*

## The question

Tessera's Amendment 11 (draft, unsigned; `tessera/docs/phase-0-prereg-amendment-11.md`, sha256 `223523ff…cc96b4f`,
tessera HEAD `1127a4b`) repairs holes in earlier registered texts. Its A11.1 names the defect class: "a registered
decision can change what an earlier registered sentence refers to, and nothing requires anyone to re-read that
sentence". Its A11.5 reports the owner's own sweep for that class (`docs/reviews/stale-dependencies/SWEEP-2026-10-28.md`,
sha256 `ec2cce71…6cc96b4f`), which found five items. The owner's note to Tony calls A11 "the final repair".

Tony is the signer. He asked whether the documents are consistent, or whether A11 is the first of several rounds.
This is a service for Tessera: findings go to Tony, for use in pushing back on A11 before he signs.

## Design

- **Corpus (same for both arms):** the original prereg and Amendments 1–11; the frozen spec object's texts (A9, A10,
  PROOF, V1-PROFILE, ENCODING-V1, HYBRID-SUPPLEMENT; unchanged since the freeze commit `270ca49`); the hybrid
  registration record; the freeze record; PROPERTIES; the E9 author rulings; and the non-review files A11 cites
  (P3 PROFILE and DIVERGENCES, issuer DEPLOY, V1-SERVICE-RESOLUTIONS). No file under `docs/reviews/` except the
  author rulings, and not the sweep.
- **Two arms, which differ only in the task:**
  - *narrow:* find repairs A11 needs (wrong, incomplete, or conflicting with what it amends; sentences A11.3 or
    A11.5 should have listed).
  - *broad:* find stale referents and contradictions anywhere in the corpus.
- **Readers (10 lineages, each runs both arms, blind to each other):** whole-packet via OpenRouter (DeepSeek V4 Pro,
  Kimi K3.1 Pro, GLM-5.3, Qwen 3.8 Max, Mistral Large 4, Muse Spark 1.3); agentic over a staging directory holding
  only the corpus (Codex/GPT, agy/Gemini, grok, a fresh Claude Opus 5.5 subagent). Reading mode is recorded per reader.
- **Verifiers:** Claude Opus 5.5 and Codex (GPT), blind to the proposer and the arm. Each candidate is real, not real,
  or unclear. Where they split, agy (Gemini) breaks the tie, and the split is reported.
- **Counted finding:** a deduplicated candidate that both verifiers judge real, or one verifier plus the tie-breaker.
  **Touches A11:** one location is in A11, or it is a sentence A11.3/A11.5 should have listed because A11 changes
  its referent.
- **Sweep comparison** happens only after verification.

## Tony's prediction (2026-10-29, in his words)

"I think the new findings count will depend upon how broadly the exploration goes. If you keep it narrow and only
look at those that touch A11, I'd predict you will find 2 or 3 potential repairs. If you broaden it, I'd predict you
will find six or more issues, and only 1-2 that touch A11. That last one differs because I think a broad sweep will
dilute the attention given just to A11."

Read as:
- **T1:** the narrow arm yields 2–3 counted findings.
- **T2:** the broad arm yields ≥ 6 counted findings.
- **T3:** of those, 1–2 touch A11.
- **T4 (the mechanism):** the narrow arm finds more A11-touching findings than the broad arm.

## Claude's prediction

- **C1:** narrow arm, counted findings: point 3, range 1–6.
- **C2:** broad arm, counted findings: point 9, range 4–18.
- **C3:** broad arm, touching A11: point 2, range 0–4.
- **C4:** agrees with T4: narrow > broad on A11-touching findings.
- **C5:** at least one counted finding is not in the owner's sweep and would need a registered text changed (not
  only an editable one). If so, A11 is not the final repair.
- **C6:** of the broad arm's counted stale-referent findings, at most 40% are already in the sweep.
- **C7:** the agentic readers (which search) and the whole-packet readers (which hold everything) find substantially
  different sets: fewer than half of the counted findings are proposed by both modes.

## Why

A9's self-check was followed by 17 levadura items, none of which Tessera rejected. Self-sweeps share their author's
blind spots. A11 changes four parameters (P3's checklist, the slot-2 implementation, K-R's enforcer, a
cross-reference), and each change can strand sentences elsewhere. These are exactly the stale referents A11.4
says nobody re-reads.
