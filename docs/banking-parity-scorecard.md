# Scorecard: the parity lens on banking citations

*Scores predictions/2026-10-16-banking-parity-claude.md (stamped before any comparison) against
obs-0175 and audit A2 (`results/banking-parity-audit-a2/`). Written 2026-10-16 by the owner who
made the predictions.*

## Predictions (2025, 12 and 31 CFR)

| # | Predicted | Measured | |
|---|---|---|---|
| P1 pairs with a consensus | 60% (40–80%) | 81.8% (2,496 pairs, 184 act sections) | miss, just above |
| P2 covered pairs that disagree | 3% (1–8%) | 2.11% (43) | hit |
| P3 flags whose own cite is in force | 50% (25–75%) | 69.4% (25 / 36 in held titles) | hit |
| P4 consensus targets in force | ≥95% | 99.2% | hit |
| A2 flags judged misaddressed | ≥70% | **55% (A, Opus) / 50% (B, Sonnet)** | miss |
| A2 controls judged misaddressed | ≤10% | 0% (A) / 5% (B) | hit |

4 of 6. The two readers agreed on 57 of 60 items. Both called 22 of 40 flagged pairs misread by
the program, and none of the controls.

## What A2 found

**The lens is specific.** Pairs that agree with the corpus's consensus are right: 0 of 20
controls are misaddressed by reader A, 1 of 20 by reader B. The consensus map is a usable
reference.

**The false flags are mostly one bug.** When a regulation writes "section 10 of the Home Owners'
Loan Act (12 U.S.C. 1461 et seq.)", the U.S.C. citation names the whole act, not section 10. v1
paired them anyway. This accounts for 13 of the 18 false flags: HOLA, the Investment Company
Act, ERISA, the CEA, the BHC Act and the Exchange Act. In three more, the program paired the act
section with the first item of a list (items 19, 52, 58). And one cut "78q- l" to 78q (item 57).

**The real wrong addresses** (both readers, unless noted):

| Act section as written | U.S.C. as written | Where it is |
|---|---|---|
| FDI Act § 10 | **18** U.S.C. 1820(d), the criminal code | 12 U.S.C. 1820(d) |
| Exchange Act § 3 | **17** U.S.C. 78c(a)(29), the copyright title | 15 U.S.C. 78c |
| FDI Act § 18(a)(4) (two rules) | 12 U.S.C. 1818(a)(4), which is FDI § 8 | 12 U.S.C. 1828(a)(4) |
| FDI Act § 18(c), the Bank Merger Act | 12 U.S.C. 1823, which is FDI § 13 | 12 U.S.C. 1828(c) |
| BHC Act § 4 (four rules) | 12 U.S.C. 1842(c)(8) or 1842(k), which is BHC § 3 | 12 U.S.C. 1843 |
| FDI Act § 44 | 12 U.S.C. 1831a(u) | 12 U.S.C. 1831u |
| FDI Act § 38 | 12 U.S.C. 1831(o) | 12 U.S.C. 1831o |
| Exchange Act § 3 | 15 U.S.C. 78(a)(12) | 15 U.S.C. 78c(a)(12) |
| Exchange Act § 6 (three rules) | 15 U.S.C. 78(f)(a) | 15 U.S.C. 78f(a) |
| Advisers Act § 202 (three rules) | 15 U.S.C. 80-b-2(a) | 15 U.S.C. 80b-2(a) |
| Agricultural Marketing Act § 15(a) | 12 U.S.C. 1141(a) | 12 U.S.C. 1141j(a) |
| Small Business Investment Act § 102 (two rules; reader A only) | 15 U.S.C. 662 | 15 U.S.C. 661, or the act section is wrong |

Each row is a detected error with its correction attached, found by machinery that never read
the law. That is the error-correction lens Tony proposed on 2026-10-09. These pairs are cheap
to verify by eye, and they are the demo's best material so far.

## What changes in v2

- A U.S.C. citation marked "et seq." or "note" does not pair with an act section.
- A pair takes the U.S.C. citation whose position matches the act section's place in a list, or
  none if that can't be told.
- Act names resolve through Yanantin's Jabberwock: aliases are namespaced by CFR part, and
  observations come from the "X means Y" definitions. That pools evidence across "FDI Act" and
  "Federal Deposit Insurance Act", and keeps locally defined names local.

v2 gets new predictions. obs-0175 stands as measured.
