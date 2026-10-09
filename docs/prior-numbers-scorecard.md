# Scorecard: citations that resolve to a number that used to mean something else

*Predictions: [predictions/2026-10-09-prior-numbers-claude.md](../predictions/2026-10-09-prior-numbers-claude.md).
Measurement: obs-0168, `results/cfr-prior-number-citations-v1-2025.jsonl`. Audit: obs-0169,
`results/prior-numbers-audit-v1/`.*

The resolver checks whether a cited Code number exists. It can't see that a number has been reused.
The 09-24 bounded-reader study showed one case: §1.683-1 cites a §683 that exists but is not the law
the regulation implements. This instrument sizes that blind spot from the Code's own history. Each
USC section's "Prior Provisions" note records when its number held something else. 396 numbers did.

**What it flags:** 1,158 citations in 276 regulations (text-dated), plus 38 regulations dated only
in the List of CFR Sections Affected. Each citation resolves to a number whose current text was
enacted after every date the regulation itself carries. For scale, the resolver marks 1,675
sections as having a broken citation. These 276 look healthy to it.

| | Prediction | Measured | Verdict |
|---|---|---|---|
| N1 | flags judged to refer to the earlier law: 65% (45-85) | 82.5% (33/40; 95% CI about 68-91%) | **pass** (near the top) |
| N2 | "can't tell": ≤ 15% (point 8%) | 17.5% (7/40) | **fail** |
| N3 | reader A-B agreement ≥ 80% (point 85%) | 92.5% (37/40) | **pass** |
| N4 | most "current" judgments have a renumbered earlier provision | no item judged current | **not scorable** |

## What it found

**No flagged citation was judged to mean today's law.** Of 40, 33 fit the earlier provision. These
are regulations that still say "section 38" for the 1962 investment credit (now the general
business credit), "section 6015" for the old declaration of estimated tax (now innocent-spouse
relief), "section 34" for the dividends credit repealed in 1964 (now fuel credits), "section 44"
for the 1975 new-home credit (now disabled-access expenditures), "section 32" for withholding on
nonresident aliens (now the earned income credit). Often the regulation names the subject in its
own words ("section 37 (relating to the credit for the elderly)"), so a reader could catch the
mismatch. An existence check can't.

**The seven "can't tell" items are mostly instrument defects, not counterexamples.** Sorted post
hoc, by me, after scoring:
- **Same-subject revisions (2, items 9 and 27).** A "general revision of this part" renumbers
  nothing and changes no subject: "items of tax preference" before and after. The instrument
  counts it as reuse. 285 of the 1,158 flags have a general-revision note, so this is the first
  thing v2 should separate out.
- **Upstream extraction errors (3).** Items 15 and 17 cite the *1939* Code by name, and item 24
  cites section 32 of a 1935 agriculture act. The citation extractor resolved all three against
  the 1986 Code. That error belongs to `cfr-usc-citations-v2`, not to this instrument, and it
  affects every count built on it.
- **Thin passages (2).** One installment-method election fits both descriptions, and one is a bare
  list of credits.

N2 fails because I didn't anticipate the first two kinds.

## Limits

- **Judges are Claude-family.** Opus and Sonnet; the adjudicator is Opus. Agreement among them is
  not independence (yupi's seq 18 question).
- **The frame is narrower than the flags.** 213 flags had no extractable subject for the earlier
  provision and couldn't be judged, and the 38 LSA-dated sections weren't sampled. Precision
  applies to the frame (935 citations in 220 sections), one citation per section.
- **"Earlier" is a reading of the passage, not a legal opinion.** A regulation can mean the old law
  and still govern something today, through transition rules or closed years. Whether these rules
  still operate is a separate question; rule-currency asks it.
- **Rewrites in place are invisible.** §683, the case that motivated this, has no prior-section
  note: it was rewritten, not reused. So the blind spot is larger than this measures.
- **Exploration before prediction.** The counts and six hand-read cases were seen before the
  predictions and are declared there. The predictions covered only the audit.

## Relation to earlier work

The 1997-2025 heading comparison (obs-0144) found 48 reused numbers. This finds 396, because most
reuse happened in the 1976-1986 reshuffles, before 1997. §34 and §1202 are examples.
