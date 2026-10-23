# Predictions: the parity lens, v3 (Claude)

*Pre-registered 2026-10-23 by the Claude Opus 5.5 owner, before v3 ran on the corpus. This
commit's OTS stamp is the proof of that order.*

## What I knew when writing this

- Everything in docs/banking-parity-v2-scorecard.md. v2 produced 2,607 pairs and 31 flags, and
  every flag was read in A3. Reader A judged 24 of the 31 flags misaddressed; reader B judged 23.
  The 7 false flags were 6 cases of IEEPA § 206 cited as the range "50 U.S.C. 1701-1706" and one
  "section 4(s) of the Commodity Exchange Act" cited at 7 U.S.C. 6s.
- Sizing done on v2's output file (results/banking-parity-v2-2025.jsonl) before writing:
  - 266 v2 pairs carry a hyphenated U.S.C. token.
  - With U.S.C. titles 7 and 50 now held (release point 119-120, the same as 12, 15 and 31), 239
    of those resolve as one section, 23 don't, and 4 are in titles still not held (25, 42, 21).
  - Commodity Exchange Act pairs: 8 cite "section 4s" at 7 U.S.C. 6s, 5 cite "section 4" at
    7 U.S.C. 6, and 1 cites "section 4(s)" at 7 U.S.C. 6s.
- v3's code and tests (`act_pairs` v3). It has not run on the corpus.

## The instrument

- `act_pairs` v3:
  - A hyphenated U.S.C. token pairs only if the statute has it as one section, so a token in a
    title not held doesn't pair.
  - "N through M", "N to M" and "N thru M" don't pair.
  - `rekey_letters` reads "section 4(s)" as section 4s when the corpus's own consensus for 4s is
    the U.S.C. section cited. It runs once after a first consensus; the consensus is then built
    again.
- Held U.S.C. titles: 7, 12, 15, 31 and 50, all at release point 119-120. Otherwise as v2.
- Adding titles 7 and 50 also moves v2's in-force figures (P3, P4), so I make no prediction for
  them.

## Predictions

| # | Quantity | Point | Range |
|---|---|---|---|
| W1 | Pairs (v2's 2,607 less 27 hyphenated, less a few worded ranges) | 2,575 | 2,540–2,600 |
| W2 | Flags | 24 | 22–27 |
| W3 | A3 flags reader A judged misaddressed that are still flagged in v3 | 24 of 24 | ≥ 23 |
| W4 | A3 false flags (the 6 IEEPA ranges and the 4(s)) still flagged in v3 | 0 | ≤ 1 |
| W5 | v3 flags with no A3 item at the same section and span (new flags) | 0 | ≤ 2 |

**Audit (A4):**
- Flags that match an A3 item carry A3's judgments; they aren't read again.
- New flags, plus 20 fresh agreeing controls (seed 20261023, drawn from pairs not in A3), are
  shuffled together and read blind by two readers (Opus and Sonnet), with A3's instructions and
  packet fields unchanged.
- At most 10% of controls judged misaddressed by either reader.
- Taking A3 labels for carried flags and A4 labels for the rest, at least 90% of v3 flags judged
  misaddressed by each reader.

## Why

v3 removes exactly the two mechanisms behind A3's false flags. Holding titles 7 and 50 lets the
resolver distinguish a range from a hyphenated section instead of dropping all of them. Dropping
pairs can still move a consensus in other groups, which is why W2 and W5 are ranges and not
exact numbers.
