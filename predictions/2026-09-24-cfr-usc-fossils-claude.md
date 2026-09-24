# Predictions: regulations that cite statute that isn't there (Claude)

*Pre-registered 2026-09-24 by a Claude Opus 5.5 instance, before any
citation was extracted from the CFR and before any CFR citation was checked
against the statute. This commit's OTS stamp is the proof of that order.*

**Tony: this is an explicit invitation.** If you want to predict any of these
quantities (or others), write them in a separate file, stamp it, and I will
not read it until the scorecard. Leaving it blank is fine too. It is a choice,
not an oversight.

## What I knew when writing this

- The ledger's CFR structure (obs-0009..0045), the AMT lens and its audit
  (obs-0046..0121), and Jev repeatability (obs-0122).
- While writing the USC reader I saw these counts for release point 119-4:
  57,176 identified provisions, 2,142 section elements, of which 243 are
  repealed, 17 renumbered, 2 reserved and 2 omitted, plus 14 identifiers
  that appear more than once (OLRC encodes two versions of a provision).
  I saw that §56 exists and runs to about 13k characters. For 119-110 I saw
  only the same summary counts (58,388 provisions, 2,162 section elements).
  I have not diffed the two release points or looked at which sections are
  repealed.
- From the AMT work: 18 of the 22 confirmed-operative 2025 AMT sections
  govern no current tax year (obs-0121). Those are my prior for what a fossil
  looks like.

## The instrument (intent only)

**Citation extraction** (deterministic code, no model): in every 2025 CFR
section, find citations to sections of the Internal Revenue Code, written as
"section N", "sections N and M", "section N(a)(1)(A)", "§ N", and so on,
including list forms ("section 1 or 55"). A citation is to the Code unless it
names another source: another act ("section 7 of the Tax Reform Act of
1986"), the 1939 Code, or a regulation (numbers like 1.56-1, which have a
dot and a hyphen). Citations that are explicitly to the 1954 Code count as
Code citations, because the 1986 Code is the 1954 Code redesignated.

**Resolution** against release point 119-4, the statute in force on
2025-04-01. Each citation gets one outcome:

- **resolves**: the cited provision exists, and neither it nor its section
  is marked repealed;
- **repealed**: the cited section, or the cited provision, is marked repealed;
- **absent-section**: no section with that number exists;
- **absent-subdivision**: the section exists, but the cited subdivision path
  (for example (b)(3)(C)) does not;
- **unresolvable**: the extractor cannot map the citation to a path (for
  example a bare "(a)" referring to an earlier citation). Counted and
  reported, never folded into the other outcomes.

A citation is **broken** if it is repealed, absent-section or
absent-subdivision. A CFR section is a **fossil candidate** if it has at
least one broken citation. "Candidate" is deliberate: a regulation can cite a
repealed provision legitimately (for example a transition rule), so broken
does not mean wrong.

**Audit**: a random sample of broken citations goes to separate blind
readers, who see the CFR passage and the statute as of 119-4 and judge
whether the citation really points at something missing. They do not see
these predictions or the extractor's outcome.

## Predictions

Each has a point estimate and a range. It fails if the measured value falls
outside the range.

**P1. Coverage.** The share of 2025 CFR sections with at least one Code
citation: **70%** (55-85%).

**P2. Section-level breaks.** Among distinct cited Code section numbers, the
share that are repealed or absent: **6%** (3-12%).

**P3. Fossil candidates.** The share of 2025 CFR sections with at least one
broken citation: **20%** (12-30%).

**P4. Where breaks happen.** Absent-subdivision breaks outnumber
repealed + absent-section breaks (counted per citation occurrence):
**yes, by about 2x** (fails unless the ratio is at least 1.3).

**P5. Old text is where fossils live.** Among 2025 sections byte-identical to
a 1997 section, the fossil-candidate rate is at least **2x** the rate among
2025 sections with no identical 1997 counterpart. Point estimate 2.5x
(fails below 2x).

**P6. The AMT fossils.** Of the 18 not-current operative AMT sections from
obs-0121, **12** are fossil candidates (range 9-18).

**P7. The statute keeps moving.** Checking the same 2025 CFR against 119-110
instead of 119-4 increases the number of broken citation occurrences by
**4%** (1-10%). OBBBA falls between the two release points, and it rewrote
much, but mostly by amending text inside provisions that keep their
identifiers.

**P8. The extractor is mostly right.** In the blind audit, at least **80%**
of sampled broken citations are confirmed as genuinely pointing at a
repealed or missing provision. Point estimate 85%. I expect most errors to
come from citations of other acts that the extractor mistakes for Code
citations.

**P9. Unresolvable is small.** Unresolvable citations are under **5%** of
all extracted citation occurrences. Point estimate 3%.

## Why these could be wrong

Most of my confidence comes from one small sample: the AMT sections. If the
AMT area is unusually fossil-rich (old add-on-tax rules in a Code that kept
changing), P2, P3 and P5 will all come in too high. P4 rests on an
assumption that the Code is amended in place more than it is repealed
outright. P8 assumes I can write an extractor whose main failure mode I can
name in advance; the AMT audit showed that readers share blind spots with the
instruments they check.
