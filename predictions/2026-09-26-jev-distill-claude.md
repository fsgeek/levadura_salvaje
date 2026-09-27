# Predictions: can a fastText student carry Jev's judgment?

*Written 2026-09-26 by the owning instance (Claude Opus 5.5), before any student is
trained. Tony cleared training on Jev's outputs (TypeSafe's terms don't restrict it).
This is a utility question. If the student is good enough, Jev's judgment can run
inside an ArangoDB `classification` analyzer at index time, and it could be shared
with governance in place of Jev access. If it isn't, we learn which judgments need
a Type-1 classifier.*

## Protocol (fixed now)

- **Teachers:** Jev's section labels for the dated lens (obs-0135) and the
  currency lens (obs-0132). The same 1,675 sections of the 2025 CFR
  (sections citing a repealed or missing Code provision).
- **Input:** the section's text as `sections.py` yields it, lowercased, with
  whitespace collapsed. Nothing else, so an ArangoDB `norm` analyzer (lowercase)
  plus fastText's whitespace tokenizer reproduces it.
- **Student:** fastText supervised, with hyperparameters fixed and not tuned:
  `epoch=25, lr=0.5, wordNgrams=2, dim=50, minCount=1, loss=softmax, seed=0, thread=1`.
- **Evaluation:** 5-fold stratified cross-validation (seed 0). Every section is
  predicted once, by the fold model that didn't train on it.
- **Measures:** agreement with Jev; Cohen's κ; per-class recall against Jev; a
  majority-class baseline.
- **Cascade:** sort the out-of-fold predictions by student confidence. Report the
  largest share of sections the student can keep while its agreement with Jev on
  the kept sections stays ≥ 0.95, with Jev asked about the rest. The threshold is
  chosen on the same predictions, so this share is optimistic. It is reported as a
  curve, not as a tuned operating point.
- **Deployment fidelity:** a student trained on all sections is loaded into an
  ArangoDB `classification` analyzer (sandbox, `top_k: 1`, behind a lowercase
  `norm`). Its labels must match Python's `predict` on a 200-section sample.

## Predictions

| | Prediction |
|---|---|
| D1 | Dated lens: student agreement with Jev is 0.85 (range 0.78–0.90). That is below the 95% blind-audit agreement. |
| D2 | Dated lens: κ ≥ 0.60. |
| C1 | Currency lens: agreement ≥ the majority baseline (0.896), but recall of Jev's `historical` ≤ 0.50. The student mostly learns "current". |
| C2 | Currency lens: the student's `no_rules` recall is below its `historical` recall. |
| K1 | Dated cascade: the student can keep ≥ 40% of sections at ≥ 0.95 agreement. |
| K2 | Currency cascade: the student can keep ≥ 60% of sections at ≥ 0.95 agreement. The easy "current" majority inflates this, so K2 alone says little. |
| F1 | ArangoDB labels equal Python labels on 200/200 sampled sections. |

What would surprise me most is D1 above 0.93, which would put a bag of word
n-grams within the audit's noise of Jev on a lens about stated time limits. I'd
check for leakage (duplicate or near-duplicate sections across folds) before
believing it.
