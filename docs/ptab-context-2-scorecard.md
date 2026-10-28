# Scorecard: the recency test where the patent number can't decide

*Scores predictions/2026-10-28-ptab-context-2-claude.md (stamped at c5d4d1e while the indicators were still being
fetched) against 12 blind readings in `results/ptab-audit-context-2/`. The population is 80 decisions (seed
20261028, from 496 eligible) on patents granted on or after 2013-03-16 that don't say "pre-AIA", cite no pre-AIA-only
subdivision, and reach §§ 102/103. The ground truth is the USPTO's `firstInventorToFileIndicator`: 24 pre-AIA (N)
and 56 AIA (Y). Written 2026-10-28.*

| # | Predicted | Opus | Sonnet | |
|---|---|---|---|---|
| R1 C1 matching the indicator | 95% (≥ 90%) | 75% | 68% | miss: see below |
| R2 C0 right on pre-AIA items | 50% (25–75%) | 38% (9/24) | 33% (8/24) | hit |
| R3 C0 answering AIA on pre-AIA items | 25% (10–50%) | 33% (8/24) | 33% (8/24) | hit |
| R4 C0 right on AIA items | 75% (55–95%) | 80% (45/56) | 75% (42/56) | hit |
| R5 C0 less accurate on pre-AIA than on AIA items | yes | 38% < 80% | 33% < 75% | hit |

## Findings

**1. Readers without context take recency as authority, where the patent number can't decide.** In the first
context test (docs/ptab-context-scorecard.md) no reader did, because a pre-2013 patent number decides the
regime. Here, on patents granted after the effective date, a third of the pre-AIA patents were confidently
judged AIA from the text alone, by both models. Readers are right about AIA patents far more often than about
pre-AIA ones: the default leans toward current law. This is the silent failure of the cooperative fence that
guest:authority predicted (plaza seq 188). It holds in the text for readers who know the patent's priority chain,
and fails for readers who don't.

**2. The USPTO's own "effective filing date" field records the newest date, not the governing one.** Of the 994
applications the USPTO marks pre-AIA (indicator N) in data/ptab/fitf.jsonl, 693 have an `effectiveFilingDate`
after 2013-03-16. They are continuations. The field holds the application's own filing date, while the claims
inherit a pre-2013 priority date, which is why the indicator says N. The field's name says "effective filing
date", the statute's term (35 U.S.C. 100(i)), but it doesn't hold that value for these applications.

**3. Given that field as context, readers followed it, and accuracy on pre-AIA patents fell.** This is why R1
missed: the context I supplied was wrong for 20 of the 24 pre-AIA items. On those 20, Opus answered AIA every
time, and Sonnet answered AIA 14 times and unclear 6 times. Authoritative-looking metadata overrode whatever the
text implied. Compared with no context at all, the silent failure on pre-AIA patents went from 33% to 83% (Opus).
The design error was mine: I took the field's name on trust and didn't check it against the indicator before
building the arm. The finding stands because of that error: a reader, human or model, given the field as it is
named would do the same.

## The three findings together

- Recency taken as authority shows up in two places: in readers (finding 1) and in the record (finding 2).
- When the record's recency meets a reader's trust in the record, they compound (finding 3).
- The fence that protects old law is cooperative. It holds only for readers who know a patent's lineage. The
  USPTO's indicator encodes that lineage correctly, and its date field doesn't.

## Limits

- 24 pre-AIA items is a small sample, and the 33% has wide uncertainty.
- The readers saw at most eight passages per decision.
- The indicator is taken as ground truth. Hybrid applications (MPEP 2159.03) can make "which law" claim-specific,
  and a single indicator flattens that.
