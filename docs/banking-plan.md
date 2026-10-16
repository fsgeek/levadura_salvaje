# Banking regulation: the first corpus that isn't the tax code

The method has run only on 26 CFR against 26 USC. Whether it transfers to another body of law is
the real test of it (memory, 2026-09-29). This is that transfer: four texts of US banking
regulation, run through the same instruments, aiming at a visual demo with honest caveats by
mid-November 2026. Started 2026-10-15.

## The corpus

| Text | Where | Sections (2025 ed.) | Explicit U.S.C. cites | "section N of the … Act" cites |
|---|---|---|---|---|
| OCC rules | 12 CFR parts 1–199 | 1,123 | 1,248 | 429 |
| Regulation B | 12 CFR part 1002 | 30 (+ Supplement I, not yet counted) | 9 | 5 |
| FinCEN AML rules | 31 CFR parts 1000–1099 | 316 | 269 | 57 |
| Model risk guidance | OCC 2011-12 / SR 11-7 (PDF bulletins) | needs its own ingestion | | |

Counts as of 2026-10-15. To re-check, count `SECTION` elements by part number in
`data/banking/CFR-2025-title-{12,31}.zip`, matching cites with
`\b\d+ U\.S\.C\.? ?\d` and
`\bsection \d+[A-Za-z]*(?:\([^)]*\))* of the [A-Z][A-Za-z ]+Act\b`.

**Statute side:** US Code titles 12, 15 and 31 at release point **119-120**.
- The tax work used 119-4 and 119-110. On 2026-10-15 the OLRC returned HTTP 500 for titles 12,
  15 and 31 at both of those releases. It still served title 26, and it served every title at
  the current release, 119-120.
- So the banking corpus is read against 119-120. Releases evidently disappear, which is why
  originals are archived; see below.
- Checksums: `data/banking/SHA256SUMS`. Originals are on the signed tag
  `corpus/banking-2025-usc-119-120`.

## Time: three editions of 12 CFR (added 2026-10-16)

The plan above reads one year. Comparing agencies within 2025 can't see what banking was chosen
for: rules whose meaning changes over time while the statute stays put. So 12 CFR is now held at
three points in time:

| Edition | Fetched | Regulation B |
|---|---|---|
| 1997 | 2026-10-16 | Part 202 (Fed), 15 sections |
| 2010 | 2026-10-16 | Part 202 (Fed), 16 sections |
| 2025 | 2026-10-15 | Part 202 (Fed), 17 sections, **and** Part 1002 (CFPB), 30 sections, both headed "(REGULATION B)" |

Section counts are distinct `SECTNO` values. Each appears twice in the XML, as the tax corpus's
1997 volume did, so count distinct values. Checksums: `docs/banking-editions-SHA256SUMS`.
Originals are on the signed tag `corpus/banking-cfr12-1997-2010`.

**A comparison over time needs a crosswalk first.** After Dodd-Frank, rules moved between agencies
and parts. A diff without a map from old location to new would report every move as a change of
meaning. The crosswalk is written and stamped with the predictions, before any diff runs.

**Seen while checking, not yet measured or in the ledger: Regulation B forked.**
- 12 U.S.C. 5519(a) (at 119-120) bars the CFPB from authority over motor vehicle dealers
  predominantly engaged in sale, servicing or leasing. Section 5519(c) preserves the Board's.
- 15 U.S.C. 1691b(a) gives ECOA rulemaking to the Bureau. Section 1691b(f), added by Pub. L.
  111-203 § 1085, gives the Board rulemaking only "with respect to a person described in section
  5519(a) of title 12".
- § 1002.1(a) (2025) applies to all creditors except persons excluded by section 1029 of the
  Consumer Financial Protection Act.
- § 202.1 in 2025 is word for word the 2010 text. After markup is stripped, both are 1,628
  characters. It still says the regulation "applies to all persons who are creditors".

So one regulation became two, and the older one's stated scope was never rewritten to match its
narrower reach. This is the kind of finding the tax corpus produced: a rule that still reads as
current. It is one example found by hand. Whether it is a class is for the instrument.

## What counts as a finding (proposed 2026-10-15)

1. **Mechanical breaks**, deterministic:
   - a cited Code section that is repealed, renumbered or missing at 119-120;
   - a CFR cross-reference to a section that doesn't exist.

   This is the tax corpus's strongest result carried over.
2. **Definitions that differ across texts:** the same term defined differently by the OCC, by
   FinCEN, by Regulation B and by the guidance. This is the definitions-diff instrument already
   queued for tax.
3. **Deferred: obligations that one text makes impossible to meet under another.** This needs
   legal judgement, so at most it is presented as labelled candidates.

## The repeatability rule

- Mechanical findings are deterministic, so the same inputs give the same output.
- For any model-read lens, three independent runs per passage. Report only items where at least
  two of three agree. The lens and the sample are fixed and stamped before the first run, as in
  rule-currency v4.
- A demo must show the same thing every time it is opened.

## Porting work, known now

- **The citation extractor is IRC-specific.** In 26 CFR "section 56(b)" means the Internal Revenue
  Code; banking rules don't share that convention. Three forms need handling:
  - explicit `12 U.S.C. 1818` citations;
  - CFR cross-references (`§ 1020.320`);
  - named acts ("section 8 of the Federal Deposit Insurance Act"). These need a map from act to
    Code location, and that map is the main new work.
- Regulation B's substance is largely in Supplement I (the Official Interpretations), which isn't
  in `SECTION` elements.
- The model risk guidance exists only as PDF.

## Order of work

1. Ingest the corpus and get the mechanical findings.
2. The definitions diff.
3. The model risk guidance, and links across texts.
4. The demo and a short write-up of what it shows and what it can't tell you.

## Spending

The mechanical work is free. Any model-read pass gets a measured smoke run first, and its cost
goes to Tony before the larger run.
