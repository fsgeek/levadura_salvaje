# Predictions: the 1997 regulations against the 1997 statute (Claude)

*Pre-registered 2026-09-24 by a Claude Opus 5.5 instance, before the GPO
statute was parsed and before any 1997 citation was resolved. Tony: the
standing invitation applies.*

## What I knew

All the 2025 results: 20% of distinct cited Code sections dead, 27% of
sections fossil candidates, median repeal year 2000, and a 1955 repeal still
cited. The GPO package USCODE-1996-title26 is current through 1997-01-06
(archived on tag corpus/uscode-gpo-1996-1997). Its HTML marks sections with
documentid comments and subdivisions with classed heads and body paragraphs.
I have looked at §56 only.

## The instrument (intent only)

Parse USCODE-1996 into provisions in the same shape as the USLM reader:
section status from the heading (Repealed, Renumbered, Omitted), and
subdivisions from heads and body paragraphs that begin with a designator.
Run extractor v2 over the 1997 CFR and resolve each citation with the same
resolver and outcomes as 2025.

## Predictions

**H1.** Distinct cited Code sections that are repealed or absent in the
1997 pairing: **12%** (6-18%). That is lower than 2025's 20%, because
fossils accumulate.

**H2.** 1997 sections that are fossil candidates: **18%** (10-26%), against
27% in 2025.

**H3.** Among the 1,343 sections byte-identical in both editions, the
fossil-candidate share is at least **5 points** higher in 2025 than in 1997.
The same words, read against a later statute, break more often.

**H4.** Among citation occurrences in those identical sections that are
broken in 2025, at least **50%** were already broken in 1997 (point 60%).

**H5.** A blind audit of 60 broken 1997 citations confirms at least **75%**
(point 82%). The parser's subdivision tree is inferred from formatting, so
I expect it to be weaker than USLM's.
