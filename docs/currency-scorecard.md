# Scorecard: do dead regulations say they are dead?

*Predictions: [predictions/2026-09-24-currency-lens-claude.md](../predictions/2026-09-24-currency-lens-claude.md).
Lens: `src/levadura_salvaje/lenses/currency.py`, written by a separate
instance from the intent section alone and frozen before any call. Jev
labels: obs-0132. Blind hand audit: obs-0133. Tony made no predictions.*

**Almost none do.** Of the 1,675 sections of the 2025 CFR that cite at least
one repealed or missing Code provision, Jev labels **1,500 (89.6%) current**:
their own text states at least one rule with no time limit, or one that
reaches 2025. 149 (8.9%) are historical, meaning every rule is limited by its
own words to the past. 26 (1.6%) state no rules. The blind audit agrees with
Jev on 56 of 60. All four misses are Jev saying historical where the hand
labels say current, so the true share of **unmarked fossils** is, if
anything, higher: about 91%.

| | Prediction | Measured | Verdict |
|---|---|---|---|
| C1 | historical: 40% (25-55) | 8.9% | **fail** |
| C2 | current: 55% (40-70) | 89.6% | **fail** |
| C3 | no_rules: 5% (1-12) | 1.6% | **pass** |
| C4 | historical rate, broken ≥ half of citations vs rest: ≥ 1.5x | 16.5% vs 6.6% = 2.5x | **pass** |
| C5 | AMT fossils labeled historical: ≥ 9 of 14 | 2 of 14 | **fail** |
| C6 | current share, subdivision-only breaks minus section-level: ≥ +15 pts | 91.3% vs 88.6% = +2.7 | **fail** |
| C7 (Q) | Jev-Qwen agreement | not run | **not scored** |
| C8 | hand audit agrees with Jev: 75% (60-90) | 93% (56/60) | **fail** (above the range) |

**2 of 7 scored predictions pass.** My model of the corpus was wrong in one
consistent way. I expected regulations to carry their own expiry dates. They
mostly don't.

## Why C5 failed, and what it corrects

C5 rested on a sentence in the pre-registration: "the AMT sections I read
then said so plainly in their text". That was wrong. obs-0121 labeled 18 AMT
sections as governing no current year, and the labeler reached that from
knowledge of the law: the add-on minimum tax was repealed in 1986. The texts
don't say it. Judged from text alone, the blind labelers call 13 of the 14
current (Jev: 12). §57 and §58 regulations such as §1.58-5 and §1.57-1 state
their rules without a sunset. A reader who trusts the regulation would think
they still apply. That is the definition of an unmarked fossil, and the AMT
corner of the CFR is full of them.

## The disagreements are all on one edge

The four C8 misses (1.614-2, 1.615-6, 1.1402(e)(2)-1, 1.683-2) and the one
AMT miss (7.57(d)-1) are all mostly-dated sections with one undated clause:
"the definitions … shall apply both before and after such amendment", or
"the election is made separately for each well". Under the intent, one
undated rule makes a section current. The hand labelers applied that
strictly, and Jev sometimes let the dated majority win. The only
disagreement between the two blind passes (sec-043) sat on the same edge.

## Limits

- **The labelers are Claude instances reading the definitions Jev's lens
  was written from.** High agreement shows the lens is faithful to the
  intent. It doesn't show the intent is the right question.
- "Current" is generous by design: one undated rule is enough. The lens
  author flagged that undated definitions push chunked sections toward
  current. The audit suggests the push is real but small: every miss went
  the other way.
- C6 was about *which kind* of break goes with marked sections. There is
  almost no difference. Whether the break is a whole repealed section or a
  missing subparagraph, about 9 in 10 texts carry on as if nothing
  happened.

## What this means

The fossil finding (20% of cited Code sections are dead) could have been
harmless if the regulations had marked themselves. They don't. For the
1,500 unmarked fossil candidates, the only signals that the text is dead are
outside it: the statute, the citation check, or a reader's memory of 1986.
That is the case for an instrument that keeps statute and regulation side by
side over time, which is what this ledger is becoming.

**Next for this lens:** the second judge (C7, Hamut'ay's Qwen) waits on
Tony's decision about GPU use. A stricter variant, "does the text *name* a
period that has ended", would separate "silent" from "explicitly dated past".
It would be a new lens, with its own predictions.
