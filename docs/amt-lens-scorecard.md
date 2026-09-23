# The AMT lens: scorecard

*2026-09-23. Scores the predictions stamped in
[`predictions/2026-09-23-amt-lens-claude.md`](../predictions/2026-09-23-amt-lens-claude.md)
(commit `68e1a86`, before any Jev call) against the ledger. Every number
here cites a ledger entry; if this document and the ledger disagree, the
ledger is right.*

| Measurement | Ledger |
|---|---|
| Baseline (keyword + citation), per volume | obs-0046..0082 |
| AMT lens (Jev, `jev-1.13.0`), per volume | obs-0083..0119 |
| Blind audit of the 2025 lens | obs-0120 |
| Regimes of the 2025 operative set (P4) | obs-0121 |

## Scores

| | Prediction | Measured | |
|---|---|---|---|
| P1 | 1997 operative 15–55, incidental 25–130 | 31, 56 | pass |
| P1 | 2025 operative 18–65, incidental 50–220 | 28, 102 | pass |
| P2 | incidental/operative ratio rises | 1.81 → 3.64 | pass |
| P3a | the listed core exists in both editions | §1.56-1 is gone from 2025 | **fail** (my memory) |
| P3b | the core that exists is labeled operative | all of it | pass |
| P4 | ≥ half of 2025 operative sections are fossils | 18 of 22 reader-confirmed operative (82%); 18 of 28 lens-operative (64%) | pass |
| P5 | no 2025 section operative for §56A | 0 | pass |
| P6 | fewer than half of §1.59A (BEAT) operative | 0 of 11 | pass |
| P7 | baseline catches ≥ 85% of lens positives | 93.8% | pass |
| P7 | lens labels ≥ 80% of baseline positives | 81.3% | pass, narrowly |
| P7 | disagreement is mostly "tax preference" false positives | it is mostly citations the lens reads past | **fail** |
| P8a | ≤ 2 AMT-bearing in 150 random "none" | 2 raw, 3 adjudicated | **fail** by one |
| P8b | stratum (b) ≤ 30, ≥ a third AMT-bearing | 28; 22 of them | pass |
| P9 | incidental has the lowest median confidence | 0.93 / 0.95 (1997 / 2025) vs 0.97 and 1.00 | pass, weakly |
| P10 | ≤ 10% of sections change label across editions | 0.7% | pass, trivially |

**The method-level failures did not happen.** Stratum (a) stayed well under
the 5-in-150 line, and the lens held BEAT apart (P6). By the terms I
registered, the lens is an instrument, not yet something to calibrate first.

## What the misses taught

**The lens's blind spot is a bare citation.** Every section the lens called
"none" that the audit found AMT-bearing (22 in stratum b) was *incidental*;
none was operative. They mention the minimum tax only as a Code number —
"the tax imposed by section 1 or 55", "an election under section 59(e)",
"other than by section 56". The lens's own criterion for none ("does not
mention the minimum tax") reads past a number. A lens v2 could name the
Code sections explicitly; it would then need its own audit.

**The auditors had the same blind spot.** The labelers were told to read
every short section in full; all five reported that they searched instead,
and their search (`section 5[3-9]`) missed list-form citations. Five
"none" labels were overturned on the matched text (obs-0120 records both
the raw and the adjudicated labels). A broader mechanical sweep of stratum
(a) found nothing further. The first wander's recurring weakness — *when a
cheap judgment selects what gets examined, its errors hide in what wasn't
selected* — showed up in the audit of the instrument, not just in the
instrument. Auditors need auditing too, and a different selection method
than the thing they audit.

**Section numbers are reused, and that fools keywords.** "Section 53" in
§§1.44B-1, 1.52-1, 1.53-1..3 is the pre-1986 jobs-credit limit, not the
minimum tax credit; §1.56A in 1997 is the 1969 add-on tax under old
§56(a), while §56A today is the 2022 corporate AMT. These are the baseline's
real false positives. A number is not a meaning; its date is part of it.

**The edition keeps what the regulation lost.** §1.56-1 (the 1987–89 book
income adjustment) was removed, but §1.56-0, its table of contents, is still
in the 2025 edition, and the lens calls it operative. §1.58-1 is
"[Reserved]". These are exactly the fossils the ledger was built to find:
text that outlived the thing it describes.

**Most of the AMT in the regulations is dead.** Of the 22 sections a reader
confirmed as stating AMT rules in the 2025 edition, 18 govern no tax year
that begins in 2025: 13 are the 1969 add-on minimum tax, and the rest are
the 1987–2017 corporate AMT (adjusted current earnings, the controlled-group
exemption split, the consolidated credit limit). Only 4 govern current
years. The individual AMT, the regime individuals still pay, has almost
no operative regulations; the corpus that looks like "AMT regulations" is
mostly archaeology. This was the prediction (P4, point estimate 60%), and
it was an underestimate.

**Where the lens and the readers disagree on positives, it is the
operative/incidental line.** Of 30 controls, 29 are AMT-bearing to the
readers; exact agreement is 22 of 30. The lens calls tables of contents
operative (§1.56-0, §1.56(g)-0); the readers call a section operative when
one paragraph of an otherwise unrelated section sets an AMT amount
(§1.443-1(d), §1.460-6, §1.30-1). The one outright false positive is
§1.4-2, the optional tax tables.

## About my predictions

P10 was nearly unfalsifiable as written: most sections are "none" in both
editions, so the rate over all sections could not approach 10%. Among
sections positive in either edition, 24 of 81 changed label. P9 compares
medians of a statistic rounded to two decimals, and is weak for the same
kind of reason. The failures I registered as "me being wrong" (P3a, P7
third clause, P8a by one) are the informative ones.

## What this does not show

- Recall on AMT content that uses none of the words or numbers anyone
  searched for. The broad sweep bounds it; nothing measured it.
- Anything about 1997 beyond counts: the audit was of 2025 only.
- Accuracy of the lens against a tax professional. The readers are Claude
  instances, blind to the lens but not independent of the model family.
