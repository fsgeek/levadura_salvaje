# Scorecard: the act-section crosswalk, v1

*Scores predictions/2026-10-25-banking-crosswalk-claude.md (stamped at fbfca3b before any
cross-edition code ran) against obs-0178 and audit X1 (`results/banking-crosswalk-audit-x1/`: 3
moved classes and 10 kept controls, read blind by Opus (A) and Sonnet (B)). Written 2026-10-25.*

| # | Predicted | Measured | |
|---|---|---|---|
| C1 1997 pairs | 1,000 (600–1,500) | 668 | hit |
| C2 2010 pairs | 1,300 (800–1,900) | 1,127 | hit |
| C3 2025 pairs = v3's | 2,275 exactly | 2,275 | hit |
| C4 classes 1997 / 2010 / 2025 | 60 / 80 / 150 | 52 / 90 / 158 | hit, all three |
| C5 classes in 1997 and 2025 | 45 (25–70) | 42 | hit |
| C6 consecutive classes moved | 5% (1–12%) | 2.6% (3 / 116), all artifacts; corrected **0 / 110** | hit on the number, miss on what it measures |
| C7 Regulation B's fork not visible | yes | ECOA § 703 has no class in any edition | not testable |
| X1 moved judged real | ≥ 30% each | 0% (A) / 0% (B): all 3 "misread" | miss |
| X1 controls judged changed | ≤ 1 of 10 | 0 (A) / 0 (B) | hit |

**The three moves are one defect.** When "the Act" can't be resolved for a part, the pair is
keyed by its name as written, `name:act`. That key pools every unresolved "the Act" from every
act into one class. In 1997 "section 10 of the Act" means the FDI Act (12 U.S.C. 1820); in 2010 it
means the FHLB Act (1430). Both readers named this mechanism on their own. 18 of the 182 classes
are keyed `name:act`. None of v3's 24 flags is (32 of its 2,580 pairs are), so v3's results stand.
Crosswalk v2 and parity v4 must not let an unresolved "the Act" form a class.

**The finding: where the law lives didn't move.** Without the artifact there are 164 classes,
110 of them held in consecutive editions. Not one moved. As 12 CFR cites them, the U.S.C.
addresses of the acts' sections are the same in 1997, 2010 and 2025. Dodd-Frank added classes
(1997→2010: 45 new; 2010→2025: 87 new) but moved none.

**What that means for the demo.** Change over time in banking rules isn't in their addresses. It
is in what the rules say: definitions, scope, who is covered. Regulation B's fork is that kind of
change, and C7 shows this instrument can't see it. ECOA § 703 isn't even cited in the "section N of
the Act (U.S.C.)" form often enough to make a class. The definitions diff is the instrument for it,
and the crosswalk is now its stable frame of reference: 110 classes of act sections that mean the
same address in every edition.

**Process notes.**
- Reader B's summary reply misstated its own file (9 "same" and 4 "misread"). The file says 10 and
  3, matching A. Scores are taken from the files.
- The run took 7 minutes, almost all of it in `Brillig.galumph` (Yanantin #46). The edition is
  written into the wabe name because Jabberwock has no world time (Yanantin #41).
