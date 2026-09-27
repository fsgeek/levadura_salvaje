# Scorecard: can a fastText student carry Jev's judgment?

*Predictions: [predictions/2026-09-26-jev-distill-claude.md](../predictions/2026-09-26-jev-distill-claude.md)
(stamped af20a2b, before any training). Numbers: obs-0149 (`scripts/measure_distill.py`).
Deployment check: `scripts/check_distill_arango.py`. Tony made no predictions.*

**Not on these lenses.** The plumbing works: a fastText model loaded into an ArangoDB
`classification` analyzer gives exactly the labels Python gives. The judgment doesn't
transfer. On the dated lens, the balanced test, the student agrees with Jev on
**72.6%** of sections (κ 0.46), against a 52.3% majority baseline and a 95% blind
audit. On the currency lens it reaches 90.8%, barely above the 89.6% you'd get by
always saying "current". It finds only 28% of Jev's historical sections, and those
are the unmarked-fossil finding's whole point.

| | Prediction | Measured | Verdict |
|---|---|---|---|
| D1 | dated agreement 0.85 (0.78–0.90) | 0.726 | **fail** (below the range) |
| D2 | dated κ ≥ 0.60 | 0.463 | **fail** |
| C1 | currency agreement ≥ 0.896, historical recall ≤ 0.50 | 0.9075; 0.275 | **pass** |
| C2 | currency: no_rules recall < historical recall | 0.269 < 0.275 | **pass** (by one section's worth) |
| K1 | dated cascade keeps ≥ 40% at ≥ 0.95 agreement | 15.6% | **fail** |
| K2 | currency cascade keeps ≥ 60% at ≥ 0.95 agreement | 80.9% | **pass**, but inflated by the majority class |
| F1 | ArangoDB labels = Python labels, 200/200 | 200/200 | **pass** |

4 of 7 pass. The passes are the predictions I made *against* the student (C1, C2),
the one that majority-class inflation makes easy (K2), and the plumbing (F1). The
three predictions about how good the student would be all failed: I overestimated it.

## What the errors look like

- **Dated:** the errors are almost all confusions between `names_ended_period` and
  `silent`, which is the lens's core distinction. 190 sections go one way and 251
  the other; only 18 errors involve `no_rules`. The student hasn't learned the
  distinction, only a lean.
- **Currency:** 108 of Jev's 149 historical sections become current. A bag of word
  n-grams can't tell "applied to taxable years before 1987" in a section where
  every rule is dated from the same phrase next to one undated rule.
- **Exploratory, not predicted:** on the dated lens the student does better on short
  sections. Agreement by length quartile is 0.80, 0.77, 0.64 and 0.70. fastText
  averages over the whole text, so one dated sentence in a long section is diluted.
  Even the shortest quarter reaches only 0.80.
- **The cascade doesn't rescue it.** On the dated lens the student is confident
  *and* right with Jev on only 15.6% of sections, so Jev would still be asked about
  84%. On the currency lens it could keep 81% of sections, but those are mostly the
  easy "current" ones. The hard cases would still go to Jev.

## What it means

The ArangoDB path is real and faithful. A classifier in the index gives the database's
labels exactly as trained, with no drift across the deployment boundary. But Jev's
lenses ask about what a text *says about time*, and at this size, with fixed
settings and no tuning, a bag of n-grams doesn't carry that. That is itself the
utility answer: **Jev's judgment on these lenses is not cheaply distillable, so the
Type-1 classifier is doing work a surface model can't.** For governance, a
distilled student is not a substitute for Jev access. Qwen, which agrees with Jev on
96.6% of the currency lens, remains the substitute.

What I didn't try, and why I stopped: tuning hyperparameters, chunking sections
before classifying, or a stronger student such as a small fine-tuned encoder. The
first two might gain a few points on the dated lens. A 25-point gap to the audit
is not a tuning problem. A small encoder might close it, but it couldn't run inside
an ArangoDB analyzer. It would then be a separate service beside the index, and
storing its labels as indexed fields (route 1) is the simpler design.

## Limits

- One corpus (the 2025 CFR sections citing a broken Code provision), one edition,
  1,675 sections. The minority classes are small: 28 and 26 `no_rules`, 149 `historical`.
- Fixed settings from the predictions; nothing was tuned. That was deliberate, and it
  puts a floor on fastText, not a ceiling.
- Jev's own noise (obs-0122: 7% of repeated questions moved a probability, 2 labels
  flipped) is not subtracted. It's small next to the gaps here.
- **The model is large.** A student with `wordNgrams=2` and fastText's default 2M hash
  buckets is 420 MB. Quantization would shrink it. It doesn't matter at this
  accuracy, but it would for deployment.
- **The deployment check makes one assumption.** Whitespace is collapsed before text
  reaches ArangoDB (at ingest, in Python), because the `norm` analyzer only lowercases.
