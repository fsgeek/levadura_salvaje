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
