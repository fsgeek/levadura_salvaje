# Predictions: a byte-level reader of 1997, surprised by 2025 (Claude)

*Pre-registered 2026-09-24 by a Claude Opus 5.5 instance, before any real
training run and before any 2025 section was scored by a trained model.
Tony: the standing invitation applies. Design note:
[docs/mini-agi-as-instrument.md](../docs/mini-agi-as-instrument.md).*

## What changed from the design note

mini-AGI's weights are unpublished, and its forgetting-probe script was
never committed. The planned replication of *their* probe is not possible,
so the variance check becomes our own: **three seeds trained from scratch
on the 1997 CFR**. The spread across seeds of each section's loss is the
instrument's noise floor, the counterpart of the Jev repeatability entry.

## What I knew

- A 6-minute pilot on gazelle (RTX 3060 Laptop, 6 GB): 1.0M characters
  read, held-out 1997 loss 5.65 → 2.49 nats/byte, 1.9 GB VRAM.
- The scorer on the pilot weights: about 2.5 nats/byte on the first 60 2025
  sections.
- Group sizes of the sample below. I have not looked at any per-group loss.

## The instrument (intent only)

- **Model:** mini-AGI (volotat/mini-AGI, clone at efd4a16) with config
  changed only in `pool.resident` 32 → 16 and `model.context_end`
  4096 → 2048, to fit 6 GB.
- **Training:** from scratch, on the 1997 CFR sections flattened as the
  lenses see them, 95% of sections (seeded split `minagi-split-2026-09-24`).
  Seeds 0, 1 and 2, 60 minutes each (about 10M characters).
- **Scoring:** nats per byte for each sampled 2025 section, fresh context,
  no learning, working set chosen the way mini-AGI's evaluator chooses it.
- **Sample** (seed `minagi-sample-2026-09-24`, sections ≤ 30k characters,
  1,128 in all):
  - **G1**, all 78 2025 sections byte-identical to a *held-out* 1997
    section: unchanged text the model never read.
  - **G2**, 150 identical to a 1997 *training* section: read.
  - **G3**, 300 fossil candidates not identical to 1997.
  - **G4**, 300 non-candidates, not identical, whose number existed in 1997.
  - **G5**, 300 non-candidates whose number is new since 1997.
- The per-section loss is the mean over the three seeds. Comparisons use
  group medians.

## Predictions

**M1.** Instrument noise: the median, over sampled sections, of the spread
(max − min) of loss across the three seeds is at most **0.05** nats/byte.

**M2.** Unchanged, unseen text is easier: the G1 median is at least **10%**
below the G4 median.

**M3.** Fossils are suspiciously easy: the G3 median is at least **3%**
below the G4 median.

**M4.** New numbers are the most surprising: G5 has the highest median of
G1, G3, G4 and G5.

**M5.** Reading helps beyond style: the G2 median is at least **15%** below
G1's. This is the memorization gap.
