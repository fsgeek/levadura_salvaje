# Predictions: how PTAB final written decisions mark the law they apply (Claude)

*Pre-registered 2026-10-27 by the Claude Opus 5.5 owner, after the metadata was fetched and before any
decision's text was downloaded or parsed. This commit's OTS stamp is the proof of that order.*

## Why

Patents v1 and v2 found the rules fencing old law in three ways: stated, conditioned and implicit. The
adjudication layer applies that law to particular patents. Do the Board's final written decisions say
which regime they apply, or do they cite "35 U.S.C. § 103" and leave the reader to know? This is levadura's
first corpus of decisions rather than rules, and it reaches it through an API key Tony obtained with
identity verification on 2026-10-27.

## What I knew when writing this

- Metadata only, from the USPTO Open Data Portal (data/ptab/meta.jsonl): 2,388 final written decisions
  issued 2021–2026 (2,283 original, 79 on remand from the Federal Circuit, 18 on rehearing, 8 on
  Director remand; 2,278 IPR, 97 PGR, 12 CBM, 1 derivation).
- Grant dates: 621 before 2013-03-16 (certainly examined under pre-AIA law), 548 in 2013–2016, 1,219 in
  2017 or later.
- The text in search results is cut at about 500 characters. The full text comes from each decision's PDF
  through `pdftotext`. No decision text has been read.
- Background knowledge: AIA § 103 has no subsections, so "§ 103(a)" names pre-AIA law. Pre-AIA 102(e), (f)
  and (g) have no AIA counterpart of that form. Board decisions often footnote which version applies.

## The instrument (ptab v1)

For each decision's text (pdftotext; whitespace collapsed):
- **marked:** "pre-AIA" appears at least once (any dash).
- **basis:** "March 16, 2013" or "effective filing date" appears.
- **old_subdivision:** a citation of 35 U.S.C. § 103(a), or § 102(e), (f) or (g).

Bands come from the patent's grant date in the metadata: pre (< 2013-03-16), mid (2013–2016), late (2017+).

## Predictions

| # | Quantity | Point | Range |
|---|---|---|---|
| Q1 | Pre-band decisions that are marked | 85% | 65–97% |
| Q2 | Mid-band decisions that are marked | 55% | 35–75% |
| Q3 | Late-band decisions that are marked | 25% | 10–45% |
| Q4 | Pre-band decisions that state a basis | 60% | 35–85% |
| Q5 | Pre-band unmarked decisions that cite an old subdivision | 60% | 30–90% |
| Q6 | Pre-band marked share, 2025–26 decisions against 2021–22 | not lower by more than 10 points | |
| Q7 | PDFs with no extractable text | 1% | ≤ 5% |

**Audit (P1).** Two blind readers (Opus and Sonnet), plus a Hamut'ay door if one has taken up the offer at
plaza seq 179.
- Up to 30 pre-band unmarked decisions, and 10 pre-band marked controls, shuffled.
- Each item gives the patent's grant date and up to eight passages around the decision's "35 U.S.C." citations.
- The question: does the decision apply pre-AIA law, and does it say so?
- At least 70% of unmarked decisions judged to apply pre-AIA law implicitly (that is, without saying so).
- At most 10% of unmarked decisions judged to apply the wrong regime.
- At most 1 of 10 controls judged not to apply pre-AIA law.

## Why these numbers

The Board deals with the transition every day, and its decisions usually footnote the version applied when
it matters, so marking should be high in the pre band. It falls with grant date, because later patents are
mostly AIA patents. Where a pre-band decision doesn't mark, it should still often cite a pre-AIA-only
subdivision such as 103(a). That is implicit fencing at the adjudication layer, the counterpart of the
interference rules' bare 102(g).
