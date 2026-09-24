# Predictions: do fossil-candidate regulations present themselves as current? (Claude)

*Pre-registered 2026-09-24 by a Claude Opus 5.5 instance, before any call
for this lens. This commit's OTS stamp is the proof of that order.*

**Tony: an explicit invitation, as before.** Predict any of these, or
anything else about this lens, in your own stamped file if you want to. I
won't read it until the scorecard.

## What I knew when writing this

The fossil scorecard (obs-0126..0130): 1,675 of 6,158 2025 CFR sections
have at least one Code citation that is repealed or absent at 119-4. The AMT
regimes pass (obs-0121): 18 of 22 operative AMT sections govern no current
tax year. The AMT sections I read then said so plainly in their text ("for
taxable years beginning before January 1, 1987"). I have not asked any model
about currency, and I haven't read the text of candidate sections other than
the AMT ones.

## The lens (intent only)

One Jev Choice question per chunk of each fossil-candidate section (v2,
119-4; `broken["119-4"] > 0` in results/cfr-usc-citations-v2-2025.jsonl).
Judged **from the section's own text alone**:

- **current**: the section states rules that, on its own terms, apply to
  taxable years (or events, returns, or periods) in 2025 or later. That
  includes rules with no stated time limit;
- **historical**: every rule the section states is limited, by its own
  terms, to earlier years, events or periods (for example "taxable years
  beginning before 1987", "property placed in service before 1981",
  transition or effective-date rules that have run out);
- **no_rules**: the section states no rules (a table of contents, a
  reserved section, or pure cross-references).

A section's label is the strongest of its chunks' labels: current >
historical > no_rules.

The question tests the text, not the law. A section whose text states no
time limit is "current" even if the Code section it implements was repealed.
**That is the point.** A fossil candidate the text presents as current is an
**unmarked fossil**, the kind that misleads a reader who trusts the
regulation.

**Separation of duties**: a different instance writes the Jev question
(instructions and criteria) from this intent section alone, without seeing
the predictions below. The model is pinned (jev-1.13.0).

A second judge (Hamut'ay's local Qwen) is planned, pending Tony's decision on
GPU use. The predictions that need it are marked **(Q)** and are scored only
if it runs.

## Predictions

**C1.** Share of the 1,675 candidates labeled historical: **40%** (25-55%).

**C2.** Share labeled current, the unmarked-fossil rate: **55%** (40-70%).

**C3.** Share labeled no_rules: **5%** (1-12%).

**C4.** Candidates whose broken citations are at least half of all their
Code citations are labeled historical at least **1.5x** as often as the
rest. Point estimate 2x.

**C5.** Of the 14 AMT-fossil candidates (obs-0121, all not current by hand
label), Jev labels at least **9** historical (point 11).

**C6.** Among candidates whose only broken citations are absent-subdivision
(no repealed or absent section), the current share is at least **15 points**
higher than among candidates citing a repealed section.

**C7 (Q).** Jev and Qwen agree on the label for **75%** of candidates
(60-88%).

**C8.** A blind hand audit of 60 candidates (20 per Jev label, stratified;
readers see the text and the intent definition only) agrees with Jev on
**75%** (60-90%).
