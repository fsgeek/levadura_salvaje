# Predictions: twin regulations in 2025 12 CFR (Claude)

*Pre-registered 2026-10-25 by the Claude Opus 5.5 owner, before any twin except Regulation B was
measured. This commit's OTS stamp is the proof of that order.*

## The idea

Dodd-Frank moved the consumer financial regulations to the CFPB, which reissued them in chapter X
(parts 1002, 1005, 1013, 1016, 1022, 1026). The original agencies kept their copies with narrowed
scope. So 2025's 12 CFR holds pairs of copies of one regulation, kept by different agencies. A
**stale twin** is a copy whose text predates an amendment that the other copy took, while it is
still in force for whoever that agency still covers. Regulation B's § 202.1 (the 10-20 handoff) is
one such fork.

## What I knew when writing this

- Regulation B, sized today: 16 section pairs (202.x and 1002.x, matched by section number), plus
  202.17 with no twin and 1002.101–114 (small-business lending data) only in the CFPB's copy.
  Difflib ratios, with part numbers masked: 11 pairs ≥ 0.95. 202.1 0.881, 202.5 0.649, 202.13
  0.865, 202.14 0.421 (appraisals) and 202.16 0.929 fall below.
- Which twin parts exist in 2025 (section counts, nothing else): 202/1002 (17/30), 205/1005
  (19/28), 213/1013 (9/9), 222/1022 (30/43), 226/1026 (56/66), and FDIC 332 against 1016 (18/17).
  Part 203 (C), 216 (Board P), 230 (DD) and OCC part 40 are gone.
- Background knowledge: the CFPB's own large amendments since 2011 include Regulation Z (ability to
  repay and qualified mortgages, servicing, TILA-RESPA integrated disclosures), Regulation E
  (remittance transfers, prepaid accounts), and Regulation B (§ 1002.14 appraisals 2013, the
  § 1071 small-business data rule 2023).

## The instrument (twins v1)

- Twins: B (202/1002), E (205/1005), M (213/1013), V (222/1022), Z (226/1026) and P (FDIC
  332/1016), all 2025 editions.
- Sections are paired by their number after the part (202.14 with 1002.14). A section with no
  partner is **only-old** or **only-new**.
- Similarity is difflib's ratio on whitespace-collapsed text after masking part numbers and
  agency names (Board, Bureau, Corporation, FDIC, CFPB, "Federal Reserve System"). A pair is
  **diverged** below 0.95.

## Predictions

| # | Quantity | Point | Range |
|---|---|---|---|
| T1 | Section pairs across the six twins, Regulation B included | 140 | 110–170 |
| T2 | Share of pairs diverged, Regulation B excluded | 25% | 10–45% |
| T3 | The twin with the highest diverged share | Z | |
| T4 | The twin with the lowest diverged share | M | |
| T5 | Only-new sections, Regulation B excluded | 30 | 10–60 |

**Audit (W1).**
- Every diverged pair (up to 40; seed 20261025) and 10 non-diverged controls, shuffled together
  and read blind by two readers (Opus and Sonnet).
- Each item shows both texts, unattributed as A and B, and a line diff. The question: is the
  difference editorial, an intended scope difference, one copy stale (missing an amendment that
  the other took), or both amended differently?
- At least 40% of diverged pairs judged **stale** by each reader.
- At most 1 of 10 controls judged anything but editorial.

## Why

The CFPB amended its copies heavily after 2011. The old agencies narrowed their scope, but by
2025 they had little reason to keep the copies current, because few institutions remain under
them. Regulation Z took the most amendment and Regulation M the least.
