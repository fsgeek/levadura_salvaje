# Predictions: the AMT lens over 26 CFR (Claude)

*Pre-registered 2026-09-23 by a Claude Opus 5.5 instance, before any Jev call
and before any search of the corpus for AMT content. This commit's OTS stamp
is the proof of that order. Tony's predictions, if he makes any, are stamped
separately; I have not seen them.*

## What I knew when writing this

I have not grepped, parsed or read the CFR text for anything to do with AMT.
I do know the structural facts already in the ledger: 4,983 sections in the
1997 edition (volumes 3, 6 and 17 missing from the zip), 6,158 in 2025, and
the per-volume dates (obs-0009..obs-0045). Everything below about *which*
AMT regulations exist comes from training data, not from the corpus. Where
that memory is wrong, the prediction should fail, and that failure is data
about me as an instrument.

## The lens (intent only)

For every section of both editions, one question with three answers:

- **operative**: the section states rules that determine alternative
  minimum taxable income, the tentative minimum tax, AMT adjustments or
  preferences, the AMT exemption, the minimum tax credit, or the AMT
  foreign tax credit, for some regime of the minimum tax (the 1969 add-on
  minimum tax, the individual AMT, the 1987-2017 corporate AMT, or the
  2022 corporate AMT on adjusted financial statement income);
- **incidental**: the section mentions the minimum tax (for example, "this
  deduction is also allowed for AMT purposes") but is about something else;
- **none**.

The base erosion and anti-abuse tax (§59A) is **not** AMT for this lens.
It is a minimum tax by design, so it is the planted near-miss.

**Separation of duties.** The Jev output type and field descriptions will be
written by a different instance, from this intent section alone, without
seeing the predictions below. The hand audit will be labeled by a separate
instance that does not see Jev's labels.

**Sections longer than Jev's window** are split at paragraph boundaries. A
section's label is the strongest label of any of its chunks, in the order
operative > incidental > none, and the chunk count is recorded.

## The baseline instrument (no classifier)

A section is **baseline-positive** if its text matches, case-insensitively,
any of "alternative minimum tax", "minimum taxable income", "tentative
minimum tax", "minimum tax credit", "tax preference", or a citation to
section 53, 55, 56, 56A, 57, 58 or 59 of the Code (any subsection, but
**not** 59A). The baseline is recorded in the ledger as its own instrument.

## Predictions

Counts are for sections Jev reads. Each has a point estimate and a range.
The prediction fails if the measured value falls outside the range.

### P1. How many sections, by label

| | operative | incidental |
|---|---|---|
| 1997 | 30 (15–55) | 60 (25–130) |
| 2025 | 35 (18–65) | 110 (50–220) |

### P2. Incidental mentions grew faster than operative rules

The incidental-to-operative ratio is higher in 2025 than in 1997. Reasoning:
new regulations (bonus depreciation, consolidated returns, international
rules) mention the AMT in passing far more often than they amend its core.

### P3. The core exists, in both editions, and is labeled operative

From memory, I expect these to be present in both editions and labeled
operative: §1.55-1, §1.56-1, §1.56(g)-1, and at least three sections each
in §1.57-x and §1.58-x. A section that is missing counts against my memory
(P3a). A section that is present but not labeled operative counts against
the lens (P3b). The two are scored separately.

### P4. Fossils

At least half of the 2025 operative sections (point estimate 60%) describe
a regime that governs no current tax year: the pre-1987 add-on minimum tax,
the 1987-1989 book income adjustment, or the adjusted current earnings
(ACE) adjustment of the 1990-2017 corporate AMT. This is hand-labeled over
the operative set, which is small enough to read in full.

### P5. The 2022 corporate AMT has no regulations here

No 2025 section is labeled operative *for* §56A / adjusted financial
statement income (point 0, range 0–2). Proposed regulations are not
codified in the CFR, and as far as I know none were final by the edition
date.

### P6. The near-miss

Fewer than half of the §1.59A sections (BEAT) are labeled operative. If
half or more are, the lens is reading "minimum tax" as a keyword, and I
will treat every other result as suspect until that is explained.

### P7. Baseline and lens mostly agree

In 2025:

- Of the sections Jev labels operative or incidental, the baseline catches
  at least 85%.
- Of the baseline-positive sections, Jev labels at least 80% operative or
  incidental.
- Most of the disagreement comes from "tax preference" appearing in non-AMT
  contexts (a baseline false positive), not from AMT content that the
  baseline cannot see.

### P8. The audit of the "none" pile finds almost nothing

There are two strata, both from 2025, labeled blind:

- (a) 150 sections sampled at random from Jev's "none" pile;
- (b) every section that is baseline-positive but labeled "none" by Jev.

Stratum (a) finds at most 2 AMT-bearing sections. Stratum (b) holds 30 or
fewer sections, and at least a third of them turn out to be AMT-bearing.
This would make stratum (b), not (a), the place where the lens's misses
are concentrated. Stratum (a) is underpowered by design at this base rate
(about 2-3%); it bounds a gross failure and cannot show a subtle one.

### P9. Jev's confidence

The median confidence margin is lower for incidental labels than for
either operative or none.

### P10. The same section, two editions

Among sections whose section number appears in both editions, at most 10%
change label between 1997 and 2025.

## What would show the approach is wrong, not just my numbers

If the audit strata find AMT-bearing sections at rates that make any
absence claim meaningless (stratum (a) above 5 of 150), or if the lens
fails P6, then this lens is not yet an instrument, and the next rung is
calibrating it, not measuring with it. A wrong P1 or P3a is only me being
wrong. A failed P6 or P8 is the method being wrong.
