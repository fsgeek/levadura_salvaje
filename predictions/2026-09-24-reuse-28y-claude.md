# Predictions: section numbers reused between 1997 and 2025 (Claude)

*Pre-registered 2026-09-24 by a Claude Opus 5.5 instance, before comparing
section headings across the GPO 1996 and USLM 119-4 statutes. Tony: the
standing invitation applies.*

## What I knew

The bounded-reader test (obs-0142) found a dead regulation, §1.683-1, whose
citation resolves because §683 was reused. An audit control (obs-0134) found
§39 reused. The 18-month window (obs-0131) had 110 heading changes. I have
not compared 1996 and 2025 headings.

## The instrument (intent only)

For each section number in force in both the GPO 1996 statute and USLM
119-4, compare the headings (normalized: lowercase, punctuation removed,
stopwords dropped). A **reuse** is a pair whose word-set Jaccard similarity
is below 0.2, meaning the headings share almost no words. Then count the
2025 CFR sections (extractor v2) that cite a reused section and are
**byte-identical to a 1997 section**, so their text was written for, or at
least last settled under, the old meaning.

## Predictions

**U1.** Reused section numbers: **40** (15-120).

**U2.** 2025 CFR sections identical to 1997 that cite a reused section:
**20** (5-60).

**U3.** Among 2025 sections with no broken citation at 119-4, the share
citing a reused section: **3%** (1-8%). Existence checks call these healthy.
