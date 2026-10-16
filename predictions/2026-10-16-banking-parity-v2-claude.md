# Predictions: the parity lens, v2 (Claude)

*Pre-registered 2026-10-16 by the Claude Opus 5.5 owner, before v2 ran on the corpus. This
commit's OTS stamp is the proof of that order.*

## What I knew when writing this

- Everything in docs/banking-parity-scorecard.md. v1 found 2,496 pairs, consensus for 81.8% of
  them, and 43 flags (2.11%). A2 judged about half the flags real, and 0 or 1 of 20 controls
  misaddressed. 13 of the 18 false flags paired an act section with a whole-act "et seq."
  citation, and 3 took the first item of a list.
- Surveys of 2025 12 and 31 CFR: 88 "X means the Y Act" definitions and 370 inline "the Y Act
  (X)" definitions, with 110 distinct inline forms.
- v2's code and tests (`act_pairs` v2, `act_names` v1 on Jabberwock). It has not run on the
  corpus.

## The instrument

- `act_pairs` v2 skips "et seq." and "note" citations and list items, and reads "the Act".
- Act names resolve through `act_names` in three wabes: the part's own short names, then long
  names, then short names every definition agrees on.
- The consensus is keyed by (resolved act, act section). An act that doesn't resolve is keyed by
  its canonical name as written.
- Otherwise as v1: at least 3 pairs, 75% agreement, 2025 editions of 12 and 31 CFR.

## Predictions

| # | Quantity | Point | Range |
|---|---|---|---|
| V1 | Pairs (fewer than v1's 2,496: whole-act and list citations drop out; "the Act" adds some) | 2,300 | 1,900–2,600 |
| V2 | Share of pairs whose act name resolves to an entity | 85% | 70–95% |
| V3 | Distinct act names as written, divided by distinct keys after resolution | 1.4 | ≥1.2 |
| V4 | Share of pairs with a consensus | 85% | 80–92% |
| V5 | Share of covered pairs that disagree | 1.2% | 0.6–2.0% |

**Audit (A3):** as A2. Up to 40 flags and 20 agreeing controls, seed 20261016, shuffled
together, with the same instructions and packet fields, read blind by two readers.
- At least 75% of flags judged misaddressed, and at least 85% judged not misread by the program.
- At most 10% of controls judged misaddressed.

## Why

The two fixes remove the dominant false-flag mechanism. Pooling names should raise coverage,
and it may surface wrong addresses that v1's split keys hid: a pair under "FDI Act" that
disagrees with the long-name consensus.
