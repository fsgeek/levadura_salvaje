# Scorecard: a reader of 1997, surprised by 2025

*Predictions: [predictions/2026-09-24-minagi-claude.md](../predictions/2026-09-24-minagi-claude.md).
Design: [docs/mini-agi-as-instrument.md](mini-agi-as-instrument.md).
Measurement: obs-0147, `results/minagi-v1/`.*

**The instrument.** [mini-AGI](https://github.com/volotat/mini-AGI) (at
efd4a16), a byte-level continual learner, trained from scratch on 95% of
the 1997 CFR's sections and nothing else. Three seeds each read for 60
minutes (9.8M characters apiece) on gazelle, a spare RTX 3060 Laptop (6 GB).
Held-out 1997 loss ended at 1.18, 1.19 and 1.18 nats/byte. Each model then
read 1,128 sampled 2025 sections without learning, and a section's score is
its mean loss per byte over the three seeds. The model has no notion of
citations, statutes or dates. Its blind spots are not the ledger's, Jev's
or Qwen's.

| group (n) | median nats/byte |
|---|---|
| G2: identical to a 1997 section it read (150) | 1.094 |
| **G3: fossil candidates, changed since 1997 (300)** | **1.088** |
| G1: identical to a 1997 section it did *not* read (78) | 1.110 |
| G4: changed non-fossils, number existed in 1997 (300) | 1.147 |
| G5: section number new since 1997 (300) | 1.175 |

| | Prediction | Measured | Verdict |
|---|---|---|---|
| M1 | median seed spread ≤ 0.05 nats/byte | 0.042 | **pass** |
| M2 | G1 ≥ 10% below G4 | 3.2% (p = 0.08) | **fail** |
| M3 | G3 ≥ 3% below G4 | 5.1% (rank p ≈ 10⁻¹⁰) | **pass** |
| M4 | G5 the most surprising of G1, G3, G4, G5 | yes (vs G4: p = 0.003) | **pass** |
| M5 | G2 ≥ 15% below G1 | 1.5% (p = 0.37) | **fail** |

**3 of 5 pass.**

## Fossils read like 1997

The design note's hypothesis was that fossils would be *suspiciously easy*
for a reader of 1997. They are: 5.1% easier than other changed sections
whose numbers existed in 1997, in every seed separately (−0.068, −0.053,
−0.059). They are easier even than unchanged 1997 text the model never
saw.

**It is not length.** I've been caught by this twice (P5, D4), so this time
I checked before writing anything. Fossils are longer (median 8.1k bytes
against 5.1k), but per-byte loss barely depends on length (slope −0.012 per
log-byte). Within each of five length bins, fossils sit 0.05–0.10 below
changed non-fossils. After adjusting for length, fossils (−0.076) sit
beside unchanged unseen 1997 text (−0.069), while changed non-fossils
(−0.013) and new numbers (+0.001) do not.

That is independent corroboration. The ledger found the fossils by
checking citations against the statute. Jev and Qwen found that their text
presents them as current. This model knows none of that. It has only read
1997, and to it, the 2025 fossils read like 1997.

## The failures

**M5 (memorization) and M2 fail for the same reason.** Each model read 9.8M
characters, sampled as random windows from a 38M-character corpus, so it saw
about a quarter of the text once. That is too little to memorize: the sections it
read are only 1.5% easier than the ones it didn't. What it learned is the
*style and substance of 1997 regulation*, which is what the instrument
needs. It isn't a record of specific sections. G1's small sample (78, most
of them very short) makes M2 weak as well.

## Limits

- One corpus pass is not complete, and longer training could sharpen or
  shift the picture. The seeds agree closely (median spread 0.042), so the
  measurement is stable at this length.
- The config was reduced to fit 6 GB: `pool.resident` 16 instead of 32, and
  `model.context_end` 2048 instead of 4096.
- A first seed-0 run was damaged when the laptop suspended for 47 of its 60
  minutes. It was set aside, not scored, and the pipeline was restarted
  after sleep was disabled.
