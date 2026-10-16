# Predictions: banking regulations that cite statute that isn't there (Claude)

*Pre-registered 2026-10-16 by a Claude Opus 5.5 instance (the owner who took the seat on
2026-10-15), before any banking citation was resolved against the statute. This commit's OTS
stamp is the proof of that order.*

**Tony: this is an explicit invitation.** If you want to predict any of these quantities, write
them in a separate file and stamp it; I won't read it until the scorecard. Leaving it blank is
fine too.

## What I knew when writing this

- The tax corpus's results: about 20% of cited Code sections dead, 11.4% of citations broken,
  27–29% of sections with a broken citation, and a blind audit confirming 94% of flags
  (docs/findings-2026-09-24.md).
- From building the extractor (`src/levadura_salvaje/usc_cites.py` v1), over 12 CFR 1997, 2010
  and 2025 and 31 CFR 2025, distinct sections: 17,797 explicit citations. By title: 12: 9,826;
  15: 2,369; 5: 1,748; 31: 835. 202 "U.S.C." occurrences not captured, mostly chapters,
  "scattered sections" and appendices. Flags: et seq. 1,590, hyphen 1,236, irregular chain 715.
  These counts are across all four texts, not per edition.
- Section elements at release point 119-120: title 12 has 1,685 in force, 254 repealed, 50
  omitted, 9 transferred, 1 reserved. Title 15 has 2,504 in force, 153 repealed, 33 omitted, 11
  transferred. Title 31 has 489 in force, 9 repealed.
- By hand: Regulation B forked (docs/banking-plan.md). § 202.1 (2025) is the 2010 text.
- I have not resolved a single banking citation, or looked at which sections are repealed.

## The instrument

- **Extraction:** `usc_cites.extract` v1, explicit citations only. Bare "section N" and named-act
  citations are later steps.
- **Resolution:** `usc_cites.resolve` against titles 12, 15 and 31 at release point 119-120.
  - Other titles are `title-not-held`, and pre-1958 appendices are `appendix`. Both are excluded
    from the rates below.
  - A hyphenated token is tried as a section first, then as a range.
- **Population:** distinct sections of the 2025 editions of 12 CFR and 31 CFR.
  - 1997 and 2010 are measured too, but read against a 2026 statute. That shows how stale the
    old text would be today; it says nothing about what was broken then. Only the trend is
    predicted.
  - The editions are a year apart from the statute, which favours "broken". That limit is
    declared, not corrected.

**Broken** means repealed, absent-section, absent-subdivision, omitted, transferred, renumbered
or reserved.

## Predictions (2025, held titles)

| # | Quantity | Point | Range |
|---|---|---|---|
| P1 | Share of citations broken | 7% | 4–12% |
| P2 | Share of distinct cited sections (title, section) that are dead (section-level outcome not `resolves`) | 10% | 6–18% |
| P3 | Share of CFR sections with ≥1 held-title citation that have ≥1 broken one | 14% | 8–25% |
| P4 | `absent-subdivision` as a share of broken citations | 40% | 25–60% |
| P5 | 31 CFR's P1 is lower than 12 CFR's | yes | |
| P6 | Share of hyphen-flagged citations in held titles that resolve as a range rather than a section | 60% | 40–85% |
| P7 | P1 for 1997 12 CFR is at least 1.5 times P1 for 2025 12 CFR | yes | |

**Audit (A1):** a blind reader gets 40 broken 2025 citations, sampled at random with seed 20261016.
For each, it sees the citing sentence and the statute's status for the cited path. It judges
whether the text really cites that provision and whether the provision really is gone at
119-120. Prediction: at least 85% confirmed. The reader gets no outcome label it could anchor on
beyond the statute's own record.

## Why these numbers

Banking's statute churned hard: FIRREA in 1989 and Dodd-Frank in 2010 abolished whole agencies.
That pulls toward more dead citations than in tax. But explicit U.S.C. citations are written by
drafters who looked the Code up, which pulls the other way. I expect fewer breaks than in tax,
not more, and I am least sure of P3.
