# Scorecard: the 1997 regulations against the 1997 statute

*Predictions: [predictions/2026-09-24-fossils-1997-claude.md](../predictions/2026-09-24-fossils-1997-claude.md).
Statute: GPO U.S. Code title 26, current through 1997-01-06 (signed tag
`corpus/uscode-gpo-1996-1997`). Measurement: obs-0139. Blind audit:
obs-0140.*

## A statute for 1997

OLRC's USLM release points start in 2013, so until now the 1997 CFR had no
contemporaneous statute. GovInfo's USCODE collection has one: the title as
GPO published it, as HTML with classed headings and paragraphs but no
identifiers below the section. `gpo_usc.py` infers the subdivision tree.
Run on GPO's 2023 edition and compared with USLM at 119-4, it recovers
**98.2%** of USLM's provision paths, and **99.3%** of its own paths are in
USLM. The blind audit found one provision it missed in 60 items.

## Results

| | Prediction | Measured | Verdict |
|---|---|---|---|
| H1 | distinct cited sections dead in 1997: 12% (6-18) | 19.0% (274/1,441) | **fail** |
| H2 | fossil-candidate sections in 1997: 18% (10-26) | 28.1% (1,398/4,983) | **fail** |
| H3 | identical sections: 2025 fossil share ≥ 1997 + 5 pts | 18.3% → 19.4% (+1.1) | **fail** |
| H4 | broken in 2025 (identical sections) already broken in 1997: ≥ 50% | 76.9% (639/831) | **pass** |
| H5 | audit confirms ≥ 75% (point 82%) | 81.7% (49/60); controls 20/20 | **pass** |

## The finding: the fossil rate is stationary

| | 1997 | 2025 |
|---|---|---|
| distinct cited Code sections dead | 19.0% | 20.1% |
| sections citing at least one dead provision | 28.1% | 27.2% |
| audit-confirmed share of flagged citations | 82% | 94% (v2) |

Across 28 years and several major tax acts (1997, 2001, 2017, 2022), the
share of the regulations that cites dead statute stayed where it was. I
predicted accumulation (H1-H3), and all three fail the same way. The corpus
isn't filling up with deadwood. It holds a steady load: new fossils form as
the Code changes, and old ones leave only when their regulation is rewritten
or removed.

H4 shows what the steady state is made of in text that didn't change. For
the 1,343 sections identical in both editions, 77% of the citations broken
in 2025 were already broken in 1997. The unchanged text wasn't decaying
fast; most of its dead citations were dead a generation ago.

The 1997 audit is weaker (82% vs 94%) mostly because of the extractor, not
the statute reader. The 1997 text more often cites other statutes in forms
v2 doesn't know: "section 5312(a)(2) of Title 31, United States Code",
"section 303(e) of REA 1984", "section 1111(e) of the 1986 Act", and a Food,
Drug, and Cosmetic Act section. Correcting for the confirmed rate (82% of
flagged), the true 1997 share would be a little lower than measured.
Corrected the same way, 2025 barely moves (94%). The stationarity claim
survives either way: roughly one cited section in five and one regulation
in four, then and now.

## Addendum: turnover (obs-0141)

*Predictions: [predictions/2026-09-24-fossil-turnover-claude.md](../predictions/2026-09-24-fossil-turnover-claude.md).
Sections are paired by number, using only numbers that occur once in each
edition (3,759 in 1997, 6,136 in 2025).*

| | Prediction | Measured | Verdict |
|---|---|---|---|
| T1 | 1997 fossils whose number is gone by 2025: 20% (8-35) | 15.8% (180/1,137) | **pass** |
| T2 | surviving 1997 fossils still fossils: 75% (60-90) | 84.2% (806/957) | **pass** |
| T3 | 2025 fossils inherited from 1997: 55% (40-70) | 48.1% (806/1,675) | **pass** |
| T4 | 2025 fossils with numbers new since 1997: 15% (5-25) | 39.5% (662/1,675) | **fail** |
| T5 | 2025 fossils that turned (present in 1997, not a fossil then): 25% (12-40) | 12.4% (207/1,675) | **pass** |

**T4 is inflated by the 1997 source, and it fails as registered anyway.**
Of the 662 "new" numbers, 110 exist in 1997 but repeat there, so the
pairing excluded them. Another 135 fall in the section ranges of 1997
volumes 3 and 6, which are missing from the GovInfo zip. Volume 17 is
missing too and its range can't be bounded from the neighbours. At most 417
(24.9%) are new, right at the top of the predicted range. That adjusted
figure is post hoc and does not change the verdict.

**How the stationary rate is maintained.** Fossils mostly *persist*: 84% of
1997 fossils that still exist in 2025 are still fossils, and they make up
nearly half of 2025's load. **615 of those 806 had their text amended between
the two editions and kept their dead citations.** Being edited does not
clean a regulation. Deaths come mostly from removal (180 numbers gone) and
from cures (151 present but no longer candidates, 133 of them with changed
text). Births come from new sections that cite already-dead or soon-dead
statute, and from 207 sections the statute moved under (171 of them also
edited, so their own amendments sometimes introduced the dead cite).
