# Scorecard: the parity lens, v2

*Scores predictions/2026-10-16-banking-parity-v2-claude.md (stamped before v2 ran) against
obs-0176 and audit A3 (`results/banking-parity-audit-a3/`, 31 flags and 20 controls, read blind
by Opus (A) and Sonnet (B)). Written 2026-10-16.*

| # | Predicted | Measured | |
|---|---|---|---|
| V1 pairs | 2,300 (1,900–2,600) | 2,607 | miss, just above |
| V2 act names resolved | 85% (70–95%) | 81.7% | hit |
| V3 names per key | 1.4 (≥1.2) | 1.15 | miss |
| V4 pairs with a consensus | 85% (80–92%) | 85.8% | hit |
| V5 covered pairs that disagree | 1.2% (0.6–2.0%) | 1.39% (31) | hit |
| A3 flags misaddressed | ≥75% | 77.4% (A) / 74.2% (B) | hit (A) / miss (B) by one item |
| A3 flags not misread | ≥85% | 77.4% (both) | miss |
| A3 controls misaddressed | ≤10% | 0% (both) | hit |

The two readers agree on 50 of 51 items.

**What changed from v1.** The flagged pairs that were real went from about half to three
quarters, and the controls stayed clean. "Misread" over-counts: 6 of the 7 "misread" flags are
"80-b-2(a)", a typo in the rule itself that the program cut short. That is a defect the lens
found, not a false flag. I framed the prediction badly.

**The remaining false flags.**
- 6 of 7 are one form: IEEPA § 206 cited with the range "50 U.S.C. 1701-1706". A range names the
  whole act, as "et seq." does. v3 should not pair ranges.
- The seventh is "section 4(s) of the CEA", read as section 4 when it means section 4s.

**New because of Jabberwock.** "Section 21B of the Act", in a rule whose part defines "the Act"
as the Federal Home Loan Bank Act, is cited at 12 U.S.C. 1421b. Section 21B is at 1441b. v1 could
not pair "the Act". So were Investment Company Act § 3 cited at 80a-5 (it is 80a-3), and the
wrong addresses already tabled in docs/banking-parity-scorecard.md, all confirmed again.

**Cost.** The run took 90 s, mostly in `Brillig.galumph`, which loads every Tove on each call.
That's fine at this scale. If levadura's use grows, it goes upstream to Yanantin as an issue.
