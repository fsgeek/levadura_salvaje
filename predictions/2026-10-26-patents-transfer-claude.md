# Predictions: does levadura's architecture transfer to patent law? (Claude)

*Pre-registered 2026-10-26 by the Claude Opus 5.5 owner, before any patent data was parsed. This
commit's OTS stamp is the proof of that order.*

## The question

Tony (2026-10-25): the architecture is what builds strength for the ayllu, and the findings
are its manifestation. Moving from tax to banking was a demonstration of transfer. This study
measures transfer itself, on a fourth corpus: what carries over unchanged, what had to be built,
what it cost, and whether what it finds holds up. It is modelled on tupay's measure of adapting
against rebuilding.

## What I knew when writing this

- The files, downloaded today and hashed in data/patents/SHA256SUMS: 37 CFR 2010 (821,642 bytes)
  and 2025 (1,099,732 bytes) from GovInfo's bulk data; 35 U.S.C. at release point 119-120. Nothing
  has been parsed.
- Banking's figures: in 12 and 31 CFR 2025, 2.47% of explicit U.S.C. citations failed to resolve,
  and the audit judged about half of those really broken (docs/banking-usc-scorecard.md).
- From general knowledge of patent law:
  - The America Invents Act (2011, effective 2012–13) renumbered 35 U.S.C. 112's unnumbered
    paragraphs as (a)–(f), so "112, sixth paragraph" became "112(f)". It replaced interferences
    (§ 135) with derivation, and inter partes reexamination with inter partes review (§§ 311–319).
  - Pre-AIA law still governs applications with an effective filing date before 2013-03-16, so the
    rules may keep old forms on purpose.
  - Patent rules mostly cite "35 U.S.C. N" directly, rarely "section N of the Patent Act".
- authority's rule (plaza seq 180): every declared limitation is a place nobody looked. W5 targets
  that.

## The instruments, and the transfer claim for each

| # | Instrument | Prediction about transfer |
|---|---|---|
| I1 | `sections.distinct_sections` over the CFR zip | runs on 37 CFR with **no code change** |
| I2 | `usc_cites` + `resolve` against 35 U.S.C. (table built by `build_usc_provisions.py`) | **no code change** to either |
| I3 | the parity lens (`act_pairs`) | runs, but is **not useful**: fewer than 30 act-section pairs in 2025 37 CFR |
| I4 | twins | **not applicable**: no second agency keeps a copy of the patent rules |
| I5 | new: the form of each citation to 35 U.S.C. 112 (ordinal "sixth paragraph" or letter "112(f)") | the only new instrument; at most 80 lines |

Transfer cost: at most 80 new lines in `src/`, at most 300 in scripts, and no change to an
existing `src/` module's behaviour. Measured by `git diff --stat` at the scorecard commit.

## Predictions about the corpus

| # | Quantity | Point | Range |
|---|---|---|---|
| P1 | Explicit U.S.C. citations in 37 CFR 2025 | 2,500 | 1,200–5,000 |
| P2 | Share of 2025 citations to title 35 that don't resolve against the 2025 Code | 3% | 1–8% |
| P3 | The same share for 2010, divided by 2025's | 2.0 | ≥ 1.5 |
| P4 | Citations to 35 U.S.C. 112 that name a paragraph or subsection, 2010: share in ordinal form | 95% | ≥ 85% |
| P5 | The same in 2025: share in letter form | 70% | ≥ 50% |
| P6 | 2025 citations to 112 still in ordinal form | 10 | 1–40 |

**P6 is the positive control the banking crosswalk lacked.** If the instrument sees no shift
between P4 and P5, it can't see a move at all.

## Audit (Z1)

Read blind by two readers (Opus and Sonnet). If a Hamut'ay door has taken up the offer at plaza
seq 179 by the time the packet is built, it gets the same packet as a third reader, scored
separately.

- **Z1a:** up to 30 non-resolving 2025 title-35 citations, plus 10 resolving controls, shuffled.
  Is the citation broken, or does it resolve in a way the program missed?
  - At least 50% of non-resolving citations judged really broken.
  - At most 1 of 10 controls judged broken.
- **Z1b:** every 2025 ordinal-form citation to 112 (up to 30). Is it a stale form that should
  read 112(a)–(f), or does it deliberately refer to pre-AIA law for older applications?
  - At least half judged deliberate (pre-AIA applicability), not stale.
- **W5 (authority's rule):** for each instrument, the `known_limits` text levadura's ledger has
  carried is listed in the scorecard, with whether the patent corpus hit it.

## Why

The architecture's core (sections, explicit citations, a resolver against the Code, a population
before any model) should move without change. The parity lens and twins depend on drafting habits
and institutional history, which patent rules don't share, so I expect them not to apply. Saying
so in advance is part of measuring transfer honestly. The AIA renumbering gives a move whose
direction is known, and old forms surviving in 2025 are more likely applicability than neglect,
because the PTO still examines pre-AIA applications.
