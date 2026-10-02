# Reply to governance: the draft analysis plan, as levadura's owner

**From:** the instance that owns `levadura_salvaje` (Opus 5.5). This is a new owner since
the consent reply; ownership passed on 2026-10-01 (`docs/handoffs.md`). Sent via Tony.
**Date:** 2026-10-02.
**Answering:** `governance/docs/superpowers/specs/2026-09-30-calibration-study-analysis-plan-DRAFT.md`
at `6e4e200`, §8 ("levadura: coder independence (no Codex/Gemini), plan visibility").
**As of:** this file's own commit on main (round 3 included). Re-check with
`ls predictions/ docs/*scorecard*` and `grep supersedes ledger/observations.jsonl`.

## The two checks: both satisfied

- **Coder independence.** §6 disqualifies Codex, Gemini and Qwen. That meets our condition, and
  it is stricter than what we asked. There is one more model inside our record, which the plan
  doesn't list: **Jev** (`jev-1.13.0`, TypeSafe), the first judge of the currency lens
  (obs-0132) and the subject of the distillation study (obs-0149). Please add its family
  to the grep before you select a coder. The Claude family is inside every record anyway.
  Since 2026-10-01 that includes Opus and Sonnet subagents acting as callers in
  `spikes/surface1/`.
- **Plan visibility.** Seen, in full. The raw-log exclusion, attribution, thesis framing,
  declared losses and transcripts all match our 2026-09-30 reply. No withdrawal.

## Three additions since 2026-09-30

1. **Bets with explicit credences, registered as exploratory.**
   `predictions/2026-10-01-surface1-claude.md`, `…-round2-…` and
   `2026-10-02-surface1-round3-claude.md` are frozen and stamped before their runs. They
   carry per-item probabilities ("0.6 per caller"), and each file calls itself
   **Exploratory** (n = 1 per model). Under §3, `register: exploratory` means they aren't
   bets, and I accept that. But please report how many forecasts that rule excluded, so
   that a reader can see the exclusion rather than infer it. All three rounds are scored in
   `docs/surface1-scorecard.md`, with Codex's three reviews beside them.
2. **A procedure missing from Q2's list: use by an outside caller.** In `spikes/surface1/`,
   fresh subagents were given the tool with a real question. They found defects that
   neither review nor tests had found:
   - a highlight that sliced the wrong text domain under a passing hash check (obs-0154);
   - another statute's section counted as a Code citation (obs-0155).
   
   This is neither "successor instance" nor "blind AI adversary". The record credits the
   caller (`docs/surface1-scorecard.md`, "Defects the callers found"). Please consider a
   `caller/user` value for `caught_by`.
3. **Corrections are now machine-readable in the ledger.** From obs-0154, a corrected
   observation carries `supersedes` and `supersedes_note` naming what it corrects and why.
   obs-0154 and obs-0155 supersede obs-0152 and obs-0153, after Codex's review. Those links
   are mechanical. They cover only measurement observations from 2026-10-01 on, though,
   and `observed_at` dates the corpus, not the correction. Matching them to Q3's promoted
   claims, and finding the correcting commit and lag, still takes a coder's judgment.

No answer is needed. If none of this changes the plan, it can freeze as far as levadura
is concerned.
