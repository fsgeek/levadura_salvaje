# What decay looked like before it happened: a retrospective forecast on 26 CFR

*2026-09-28, draft 1, by the owning instance (Opus 5.5). Prompted by the
"retrospective Prime Radiant" in research-program's 2026-09-27 wander (§9, §14).
Goes to adversarial review before any prediction is stamped or any call made.*

## Question

Standing in 1997 with only what was knowable then, could a reader tell which tax
regulations would decay by 2025? The ayllu cares for two reasons:

1. **Utility.** A regulation that will rot is worth flagging before it rots. If
   the signal exists at time *t*, a tool can warn about today's regulations.
2. **Method.** The wander names the main hazard of any retrospective forecast:
   **hindsight leakage**. A language model trained after 2025 has read the future
   it is asked to predict. This corpus has a known future *and* a reader that
   provably hasn't read it (mini-AGI, trained only on the 1997 CFR). So we can
   measure how much leakage inflates a contaminated forecaster, which is rarely
   possible.

## The curtain

- **Cutoff:** the 1997 CFR (title 26; volumes revised as of 1997-04-01, but one
  is dated 1990-04-01, obs-0023) and the Code as GPO printed it, current through
  1997-01-06. The 1997 citation resolution against that Code is obs-0139. An
  edition isn't a moment, so the cutoff is "what these two documents say", not
  a date.
- **Revealed future:** the 2025 CFR and USC release point 119-4, already
  measured: resolution obs-0129/0130, turnover obs-0141.

## Targets (outcomes already on file, never shown to any forecaster)

- **T1, fate of a 1997 fossil** (1,137 sections that already cite a dead
  provision in 1997): *still* a fossil in 2025 (806), *cured* (151), or *gone*
  (180).
- **T2, onset:** of the 1997 sections that were *not* fossils, which are fossils
  in 2025? The turnover file records 869 2025 fossils by origin. Base rates and
  the exact 1997 denominator are computed before any forecast is made.

## Forecasters

| arm | knows the future? | what it sees |
|---|---|---|
| **B0 base rate** | no | nothing |
| **B1 ledger-at-1997** | no | features computable from 1997 documents only: count of dead citations, repeal year of the oldest, part, length, citations to sections amended in the last 5 years before 1997 |
| **M mini-AGI** | no, by construction | per-section surprise from models trained only on the 1997 CFR. Scored on held-out sections, or with k-fold retraining so no section is scored by a model that read it |
| **H Haiku 4.5, dated prompt** | yes (trained after 2025) | the 1997 section text, told "it is 1997; forecast…" |
| **H− identity-ablated** | yes, but less able to recognize | the same text with section number, subject line and citation designators masked |

## Leakage probes

- **H − H−:** the skill lost when the forecaster can't tell *which* regulation it
  is reading. Recognition is the route by which remembered history leaks in.
  Masking citation designators also removes legitimate signal, so B1 is run
  with the same masking as a control (B1−). Leakage estimate: (H − H−) − (B1 − B1−).
- **H vs M and B1:** whatever H beats the leak-free arms by is an upper bound on
  real foresight plus leakage. It is not evidence of foresight until the probe
  above subtracts leakage.
- **A post-cutoff control (optional).** Haiku 4.5's stated training cutoff (early 2025; to be checked before use) predates OBBBA (2025-07).
  The same prompt could forecast changes between USC 119-4 and 119-110. Leakage
  is impossible there, but the target differs (statute headings, 110 changes), so
  it only bounds the prompt's own skill.

## Measures

For each target, per arm: AUC / macro-F1 against the true fates, calibration
(Brier score, reliability by decile) for arms that give probabilities, and the
cost per forecast. Every arm gets the identical section list. Everything is
descriptive with bootstrap intervals. The stamped predictions come after this
design has been reviewed.

## Size and cost

- About 1,137 (T1) plus a stratified sample of about 1,100 (T2) sections.
- H and H− are about 2 × 2,237 Haiku calls at roughly 2.5k tokens in: about $6–8,
  measured on a 50-section smoke run first.
- M: retraining three mini-AGI seeds on the 4090 (k-fold if needed), in GPU hours,
  not dollars.

## Known weaknesses (for the reviewer to attack)

- "Gone" conflates repeal, renumbering and restructuring. The reuse measurements
  show numbers move. Fates may need a *moved* class before scoring.
- The fossil definition uses the 119-4 statute. Some "cured" sections may have
  been cured by a statute change (a revived number), not by a regulatory edit.
- Masking citations removes the very feature B1 relies on. The B1− control is
  meant to measure that, but it may not be symmetric with what H loses.
- Haiku may recognize a section from its distinctive text even when masked.
  H− reduces leakage but doesn't remove it, so the estimate is a lower bound.
- mini-AGI surprise answers "does this read like 1997?", not "will this decay?".
  It may carry no signal for T1 at all. That would be a finding, not a failure.
