# Scorecard: regulations that cite statute that isn't there

*Predictions: [predictions/2026-09-24-cfr-usc-fossils-claude.md](../predictions/2026-09-24-cfr-usc-fossils-claude.md),
stamped before any citation was extracted. Tony made no predictions for this one.*

| Entry | What |
|---|---|
| obs-0123..0125 | 26 USC structure at 119-4 and 119-110, and the diff |
| obs-0126, obs-0127 | v1 extractor + v1 resolver, 2025 CFR against 119-4 / 119-110 |
| obs-0128 | blind audit of v1 (100 broken + 30 controls, two passes, adjudicated) |
| obs-0129, obs-0130 | v2 extractor + v2 resolver, same populations |

v1 was frozen and stamped before the corpus run (commit 5a3278d). v2 fixes
what the audit and a look at the v1 output found (below). Predictions are
scored on both; no verdict changes between them.

## Results

| | Prediction | v1 (119-4) | v2 (119-4) | Verdict |
|---|---|---|---|---|
| P1 | sections citing the Code: 70% (55-85) | 84.7% | 84.7% | **pass** (at the edge) |
| P2 | cited sections repealed or absent: 6% (3-12) | 22.9% (396/1,733) | 20.1% (336/1,673) | **fail** |
| P3 | fossil-candidate sections: 20% (12-30) | 28.0% | 27.2% | **pass** |
| P4 | absent-subdivision ≥ 1.3 × section-level breaks | 0.58 | 0.64 | **fail** |
| P5 | fossil rate, identical-to-1997 ÷ other ≥ 2 | 0.65 | 0.66 | **fail** (reversed) |
| P6 | AMT fossils that are candidates: 12 (9-18) | 14/18 | 14/18 | **pass** |
| P7 | broken occurrences, 119-110 over 119-4: +4% (1-10) | +1.2% | +1.4% | **pass** |
| P8 | audited broken citations confirmed: ≥80% | 82/100 | — | **pass** (point estimate was 85) |
| P9 | unresolvable occurrences < 5% | 0.04% | 0.04% | **pass** |

**6 of 9 pass.** The three failures are the predictions about *how much* and
*where*, and they fail in the same direction: the regulations carry far more
dead statute than I expected, and it is dead in bigger pieces.

## What the numbers say

**One in five Code sections the regulations cite is gone** (P2). v2 counts
1,673 distinct cited section numbers. 336 of them are repealed or have no
element at all at 119-4, and another 13 are renumbered, omitted or reserved.
The heaviest by occurrence are §902 (the deemed-paid credit), §1201, §§810
and 815 and §71 (alimony), all repealed in 2017; §936 (2018); §809 (2004);
§1251 (1984); and §615, repealed in 1976 and still cited 258 times. I
predicted 6%, extrapolating from the AMT sections. Those turned out to be
typical, not unusually rich in fossils.

**Whole sections die more often than their parts** (P4). Section-level
breaks outnumber missing subdivisions about 3 to 2. I assumed Congress mostly
amends in place. It does. But the regulations cite the repealed wholes
thousands of times, and nothing removes those citations.

**P5 fails as registered, and the reason is a confound.** Per section,
sections unchanged since 1997 are fossil candidates less often (19.4% vs
29.4%). Per *citation* the direction flips: 13.9% of their citations are
broken, against 8.0% in other sections, which is 1.7×. Unchanged sections
are short (4.5 citations each against 24.7), so each has fewer chances to
contain a broken one. This is post hoc and does not rescue the prediction. It
does say what the next prediction of this kind should count: citations, not
sections.

**The statute keeps moving, slowly** (P7). Against 119-110, 151 citations
that resolved at 119-4 are broken. Most point into §951A, which OBBBA
rewrote (GILTI became net CFC tested income), and §45Q. That is the fossil
process observed in progress: the regulations did not change, and the ground
under them did.

**Some "healing" is number reuse.** 11 citations broken at 119-4 resolve at
119-110: §168(n), now "special allowance for qualified production
property", and §6659, now a penalty for improper Trump account pilot-program
credit claims. OBBBA re-used both numbers.
The citations now resolve, to different law. A resolver that checks
existence will never catch this. This is the section-number reuse from the
AMT work (old §53, §56A) again, seen this time as it happens.

## The instrument

**Extractor spec from a blind survey.** Eight readers each catalogued
citation forms in 30 random 2025 sections. A ninth merged the catalogues into
[docs/citation-extractor-spec.md](citation-extractor-spec.md), including 74
test snippets. I implemented the spec and all 74 pass.

**v1 resolver bugs, found by looking at the v1 output:**
- USLM writes `1400Z–2` with an en dash and the CFR writes `1400Z-2`. 617
  occurrences read as absent-section.
- The range element `s1400L...1400U–3` did not parse, so §§1400L-1400U-3
  read as absent, not repealed.

**The audit** (obs-0128): 130 items, unlabeled and shuffled. Two
independent passes, then an adjudicator for the 5 disagreements. All 30
controls were confirmed in force. Of the 100 v1-broken items:

| Final judgment | n | Cause |
|---|---|---|
| genuinely broken | 82 | 3 with a wrong extracted path, but broken either way |
| not a Code citation | 10 | ERISA §204(h)/§4048 (6), PHS Act (1), Tax Reform Act of 1984 (1), 1939 Code via "such Code" (1), a regulation paragraph "(b)(2)(vii) of this section" (1) |
| renumbered | 5 | §§822/826, renumbered as §§834/835 in 1986; USLM keeps no element for the old numbers |
| in force | 3 | 2 from the en-dash bug; 1 is a typo in the CFR itself (§416(i)(B)(i) for §416(i)(1)(B)(i)) |

My P8 guess about the dominant error was right: other statutes mistaken for
the Code, 8 of the 10. **v2** handles the forms the audit found: acronym
qualifiers and prefixes ("of ERISA", "of TRA", "ERISA section", "PHS Act
section"), "of such Code" when the nearest Code named is the 1939 Code, and
sibling designators that belong to "... of this section". Eight new tests
cover them. v2 has **not** been audited. Its error rate is unknown, not
"fixed".

**Known limits that remain:**
- An unqualified "section 204(h)" in a part-54 regulation that means ERISA
  is still read as the Code. Only document context can tell.
- Section ranges are checked at their endpoints only.
- "Renumbered" sections with no USLM element read as absent-section.
- The CFR's own typos (§48(a)(1)(e)) are extracted as written. That is
  arguably right: the citation as printed points nowhere.

## What this changes

- The AMT lens finding (18 of 22 operative sections govern no current year)
  was not special to AMT. It is what the whole corpus looks like at the
  citation level.
- Existence checks overstate health: a reused number resolves. The next
  instrument should compare the *heading or text* of the cited provision at
  the regulation's date with its text now. Where the text is available (for
  1997 we have no statute), that detects reuse directly.
- The candidate next lens is still "is this fossil still operative?" The
  population is now concrete: 1,675 sections with at least one broken
  citation.

## Addendum: audit of v2 (obs-0134)

Same protocol, new seed, 100 v2-broken and 30 v2-resolving occurrences.
**94 of 100 confirmed genuinely broken** (v1: 82). 29 of 30 controls hold.
The two passes disagreed on 2 items.

- **An artifact of the audit, not the extractor:** interior items of an
  expanded range ("section 3121(a)(1) through (20)") were shown to readers
  with the range endpoint's span, so readers judged the endpoint. That
  affected 5 items. One of them flips: §3121(a)(3) is repealed, §3121(a)(20)
  is in force. Judged on their own paths, 95/100.
- **Residual extractor errors (3):** "section 31(g)(20)(B) of TRA" and "Act
  sections" still get through when the qualifier sits after a designator
  chain, and a table cell "0 (h)" reads as a citation.
- **A resolver limit (1):** §3231(e)(1)(iii) is an inline clause that USLM
  gives no identifier, so it reads as absent.
- **The failing control is number reuse:** a citation of the 1954 Code's §39
  (gasoline and lubricating oil) resolves to today's §39 (carrybacks of the
  general business credit). The reuse scorecard predicted exactly this kind
  of silent success.

## Addendum: how long the dead citations have been dead (obs-0138)

*Predictions: [predictions/2026-09-24-fossil-age-claude.md](../predictions/2026-09-24-fossil-age-claude.md).
The repeal year is the latest date in the repealed section element's USLM
heading, covering 5,222 occurrences and 189 distinct sections, all dated.*

| | Prediction | Measured | Verdict |
|---|---|---|---|
| A1 | median repeal year over occurrences: 1990 (1980-2005) | 2000 | **pass** |
| A2 | repealed by 2005: 60% (40-80) | 61.5% | **pass** |
| A3 | repealed in 2017: 20% (8-35) | 27.2% | **pass** |
| A4 | most common decade among distinct sections: 1970s | 2010s (47; 1980s 42, 1970s 40) | **fail** |

**Death is spread across seventy years.** By occurrence, the heaviest
decade is the 2010s (2,008, mostly the 2017 act), then the 1980s (1,104).
The oldest fossils are §452 (prepaid income) and §462 (reserves for
estimated expenses). Both were enacted in 1954 and repealed retroactively in
1955, and the 2025 CFR still cites them 126 times. The deadwood never gets
cleared: each major tax act adds a layer, and the layers stay.
