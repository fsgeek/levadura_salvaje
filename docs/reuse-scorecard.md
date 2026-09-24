# Scorecard: numbers that stayed while their meaning moved

*Predictions: [predictions/2026-09-24-usc-reuse-claude.md](../predictions/2026-09-24-usc-reuse-claude.md).
Measurement: obs-0131, `results/usc26-reuse-119-4-119-110.jsonl`.*

| | Prediction | Measured | Verdict |
|---|---|---|---|
| R1 | heading changes: 120 (40-400) | 110 | **pass** |
| R2 | section/subsection share: 15% (5-35%) | 34.5% (38/110) | **pass** (at the edge) |
| R3 | revivals: 12 (3-40) | 1,518 as registered; 7 as intended | **fail** |
| R4 | CFR occurrences through candidates: 600 (150-2,000) | 756 in 134 sections | **pass** |
| R5 | top 3 sections ≥ 50% of R4 | 83.6% (§951A 400, §250 166, §181 66) | **pass** |

**R3 fails on my own wording.** I defined a revival as "absent or repealed at
119-4, in force at 119-110". That also counts every brand-new provision, and
OBBBA added 1,518. I meant numbers that come back. That narrower count is
reported alongside in obs-0131: 7 identifiers that were repealed at 119-4,
or absent there but cited by the 2025 CFR, so they must have existed
earlier. They are §128, §168(n), §168(n)(4), §6659 and its (a) and (a)(1),
and §951(a)(3). The prediction still fails as registered. The lesson is to
write the instrument so that a sentence I didn't mean can't satisfy it.

## What the heading changes are

Reading the 38 section- and subsection-level changes by hand (post hoc)
sorts them into three kinds:

- **Renames that keep the slot.** §951A "global intangible low-taxed
  income" became "net CFC tested income", and §250(b) "foreign-derived
  intangible income" became "foreign-derived deduction eligible income".
  Also the "2018 through 2025" to "beginning after 2017" edits in §§1(j),
  24(h), 217(k). A citation still lands on the right rule, now under a
  different name.
- **Re-lettering.** A new subsection was inserted and the later ones moved
  down. §951A(c) was "net CFC tested income" and is now "determination of pro
  rata share". §951A(d) was QBAI and is now subpart F treatment. §7508A(c),
  (d) and (e) shifted. §4968(b), (c) and (d) shifted. §181(f) and (g)
  shifted. A 2025 regulation citing §951A(d) still resolves, **to a
  different rule**. This is the invisible fossil: an existence check scores
  it healthy.
- **Slot reuse.** Cross-reference and termination subsections were replaced
  by new substance: §224 "cross reference" became "qualified tips", §67(g)
  became "educator expenses", and §199A(i) "termination" became "minimum
  deduction".

The CFR citations through these provisions (756) are concentrated where
OBBBA re-lettered international tax. §951A alone accounts for 400, which
makes the GILTI regulations the place where the 2025 CFR most often cites a
letter that now means something else.

## Limits

- A heading change is not proof of reuse (renames), and a reuse that keeps
  the heading, or has none, is invisible here. Telling re-lettering apart
  from renaming needs the text, not the heading. Matching old headings to
  their new position would catch the moves, and is the obvious v2.
- One window only: March 2025 to September 2026. We have no statute for
  1997.

## Addendum: where the re-lettered provisions went (obs-0137)

*Predictions: [predictions/2026-09-24-moves-claude.md](../predictions/2026-09-24-moves-claude.md).*

| | Prediction | Measured | Verdict |
|---|---|---|---|
| L1 | heading changes that are moves: 35% (15-60) | 33.6% (37/110) | **pass** |
| L2 | citations through a moved provision: 45% (20-70) | 17.7% (134/756) | **fail** |
| L3 | §951A ≥ half of move-affected citations (point 70%) | 70.1% (94/134) | **pass** |

A move is an old heading found at exactly one other identifier under the
same parent. The 37 moves include §951A(c) → (b) ("net CFC tested income"),
§4968(b)-(d) → (c), (f), (g), the §45X(c)(6)(R)-(Z) run, which shifted one
letter to make room, §163(j)(10)-(11) → (12)-(13), and §7508A(c) → (d). For
132 of the 134 affected CFR citations the rule still exists at its new
address, recorded in `results/cfr-moved-citations-v2-2025.jsonl`. A reader
following the old citation finds a different rule. A reader following the
map finds the right one.

L2 fails because most of the 756 citations go through provisions that were
replaced, not moved: 73 of the 110 heading changes. The biggest block is
§951A's other subsections, rewritten in place when GILTI became net CFC
tested income. Moves are the minority, but they are the dangerous kind,
because an existence check passes them.

## Addendum: 28 years of reuse, 1997 to 2025 (obs-0143, obs-0144)

*Predictions: [predictions/2026-09-24-reuse-28y-claude.md](../predictions/2026-09-24-reuse-28y-claude.md).
This compares section headings in force in both GPO USCODE-1996 (through
1997-01-06) and USLM 119-4 (1,623 sections). A reuse candidate is a pair
whose heading word sets have Jaccard < 0.2.*

| | Prediction | Measured | Verdict |
|---|---|---|---|
| U1 | reused section numbers: 40 (15-120) | 48 | **pass** |
| U2 | 2025 sections identical to 1997 that cite one: 20 (5-60) | 12 | **pass** |
| U3 | healthy 2025 sections (no broken citation) citing one: 3% (1-8) | 4.1% (184/4,483) | **pass** |

A blind classification (obs-0144; two readers who checked both statutes'
texts, 7 disagreements adjudicated) sorts the 48:

- **31 reuse, a different subject.** Old cross-reference slots became
  substantive law: §221 is now student-loan interest, §7436 Tax Court
  employment-status cases, §1061 carried interest. §59A went from the
  Superfund environmental tax to the 2017 BEAT. The alcohol occupational-tax
  block (§§5111-5132) was emptied and refilled with drawback and
  recordkeeping rules. PFIC rules swapped places between §§1296 and 1297.
- **11 restructure, same area but old citations reach different rules.**
  The TEFRA partnership-audit block (§§6223-6233) was rebuilt in 2015 as the
  BBA regime, §960 was rewritten in 2017, and §§6111-6112 in 2004.
- **6 rename, same subject.** §220 medical savings accounts became Archer
  MSAs, and §743 was extended.

**293 sections of the 2025 CFR cite a section number that was reused or
restructured since 1997, and 147 of them have no broken citation at all.**
An existence check, the ledger's main instrument until now, calls those 147
healthy. Some are healthy: a new regulation citing the new §59A is correct.
The ones to worry about are those whose text predates the change. Ten are
byte-identical to their 1997 text, among them §1.35-2 and §1.1402(a)-5 citing
§35, and §301.6231(a)(7)-2 citing TEFRA's §6231. The rest were amended
since, and whether the amendment caught up with the new meaning is the next
question.

The bounded-reader test (obs-0142) missed a dead §1.683-1 whose citation
resolved through reuse. This instrument is the kind of evidence that would
have flagged it. §683 itself was reused before 1997, so this window doesn't
catch it. Neither does it catch §39. Both need an older statute.
