# Scorecard: explicit U.S.C. citations in banking regulation

*Scores predictions/2026-10-16-banking-usc-claude.md (stamped before any resolution) against
obs-0171..0174 and audit A1 (`results/banking-usc-audit-a1/`). Written 2026-10-16 by the owner
who made the predictions.*

## Declared before the numbers

- **Extractor v1 → v2 after the predictions, before any ledger write.** The dry run showed the
  CFR XML sets letter suffixes apart ("15 U.S.C. 78 o -11"), which made 49 citations read as a
  nonexistent § 78. v2 closes those gaps. Every v1/v2 difference across all four texts (28
  sections) was checked by hand, and all are correct. The predictions were not changed.
- **A packet defect in A1.** The packet's statute record didn't translate USLM's en dash, so item
  11 (12 U.S.C. 2279aa-6) showed the reader a range split that the resolver never made.
- **An ambiguous instruction in A1.** "Provision gone, as the regulation wrote it" was read
  literally by reader A (Opus). Reader B (Sonnet) read it as "the provision the drafter meant",
  and said so. The two are reported separately.

## Predictions (2025, 12 and 31 CFR, titles 12, 15 and 31 at 119-120)

| # | Predicted | Measured | |
|---|---|---|---|
| P1 broken share of citations | 7% (4–12%) | 2.47% (168 / 6,799) | miss |
| P2 dead share of cited sections | 10% (6–18%) | 6.80% (54 / 794) | hit |
| P3 CFR sections with ≥1 break | 14% (8–25%) | 6.86% (142 / 2,071) | miss |
| P4 absent-subdivision share of breaks | 40% (25–60%) | 34.5% (58 / 168) | hit |
| P5 31 CFR lower than 12 CFR | yes | no: 3.46% vs 2.35% | miss |
| P6 hyphen tokens that are ranges | 60% (40–85%) | 20.4% (113 / 554) | miss |
| P7 1997 ≥ 1.5 × 2025 (12 CFR) | yes | 4.65% vs 2.35%, 1.98× | hit |
| A1 audit confirms ≥ 85% | yes | **50% (A) / 27.5% (B)** | miss |

3 of 8. Every miss leans the same way: banking's explicit citations are healthier than I
expected, and less healthy-looking breaks are real than in tax (94% confirmed there).

## What A1 found

**The instrument's false breaks** (reader A's "no"s; B agrees on all but the unclear ones):

- **Whole-act shorthand.** "15 U.S.C. 78" and "15 U.S.C. 80a" mean the Exchange Act or the
  Investment Company Act as a whole (items 3, 4, 22, 26).
- **Ranges with a dead endpoint.** "78a-78jj" and "1702-1706" span law that is in force (items
  17, 32, 35). The resolver takes the worse endpoint. It should ask whether the range still
  holds law.
- **Subdivisions USLM doesn't tag.** 12 U.S.C. 1842(a)'s closing (A)–(C) clauses, 1843(c)(1)(D),
  24 "Seventh", 1703(d)(3)(B) and 1681g(f)(2)(A) all exist in the statute's text but not as
  elements (items 1, 6, 8, 25, 34, 37, 39). absent-subdivision is unreliable wherever OLRC
  leaves structure untagged. Title 26 is tagged more thoroughly, which may be why tax didn't
  show this.
- **Source typos the extractor took literally:** "78(f)(a)", "80-b-2", "78 1 (g)" (items 15, 20,
  23, 29). These are real defects in the regulations, a different finding from a dead
  citation.
- An abbreviated range, "1667-67f" (item 27), and the packet defect at item 11.

**The real breaks come in two kinds**, and the second is new:

1. **Fossils**, where the cited section was repealed or recodified. 31 U.S.C. 483a, 231, 424 and
   1026 are pre-1982 locations of title 31 (the False Claims Act's is now § 3729). Also 12
   U.S.C. 377 and 78 (repealed), and 4619(b).
2. **Wrong addresses**, where the provision exists elsewhere and the reader could name it.
   - Gramm-Leach-Bliley § 509 is cited as 12 U.S.C. 6809, but it is 15 U.S.C. 6809.
   - The Bank Secrecy Act's 5318(g) is cited in title 12 instead of title 31.
   - The APA's § 553 is cited in title 12 instead of title 5.
   - 1842(c)(8) should be 1843(c)(8); 5136A should be 24a; and 4626 should be 4636.
   - Two cite subdivisions that were later renumbered: 77d(5) is now 77d(a)(5), and
     1693a(6)(E) is now (7)(E).

   Reader B scores these as not gone, because the law exists. That disagreement is the point:
   the citation is broken and the law isn't. This is the parity lens Tony asked for on
   2026-10-09, showing up unprompted. The error is detectable, and the correction can often be
   inferred.

## What it means for the plan

- The tax corpus's headline (dead citations everywhere) doesn't transfer at the same scale. On
  the A-reader count, about 1.2% of explicit banking citations are really broken
  (2.47% × 50%).
- What does transfer is the kind of finding: rules citing law that moved, and rules citing the
  wrong address. Together with the Regulation B fork, that points the demo at change over time
  and misaddressing, not at a count of breaks.
- **v3 of the resolver, before any further measurement:**
  - whole-act shorthand as its own outcome;
  - ranges judged by whether they still hold law;
  - absent-subdivision checked against the section's text, not only its tagged elements;
  - the en dash fixed in the packet.

  v3 gets new predictions. These entries stand as measured.
