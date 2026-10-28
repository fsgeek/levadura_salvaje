# Predictions: the recency test where the patent number can't decide (Claude)

*Pre-registered 2026-10-28 by the Claude Opus 5.5 owner, while the first-inventor-to-file indicators were still
being fetched, so before anything was known about how the population splits between regimes. This commit's OTS
stamp is the proof of that order.*

## Why

In the first context test (docs/ptab-context-scorecard.md), readers without the grant date never took recency as
authority. Tony then showed why that test couldn't find it: a patent number dates the grant, the regime follows
the effective filing date, and pre-AIA applications kept issuing for years after 2013. Below about 8.4 million,
the number decides the regime. Above it, it doesn't. So the test that can find the failure uses patents granted
on or after 2013-03-16, where a reader who reasons "new number, new law" would often be wrong.

## Design

- **Population.** Final written decisions in obs-0183 on patents granted on or after 2013-03-16 that have text, do
  not say "pre-AIA", cite no pre-AIA-only subdivision, and do reach §§ 102/103: the text has "§ 102" or "§ 103"
  outside the case caption. That last condition corrects the first test's definition error. Up to 80, sampled by
  seed 20261028 if there are more.
- **Ground truth.** The USPTO's `firstInventorToFileIndicator` for the patent's application (N = pre-AIA,
  Y = AIA). Items without it are excluded and counted.
- **Arms**, the same passages as before:
  - **C0:** text only.
  - **C1:** plus the application's effective filing date, and the rule that an effective filing date before
    2013-03-16 means pre-AIA §§ 102/103 govern.
  - Each arm is read blind by Opus and by Sonnet, in batches, and every answer is "pre-AIA", "AIA" or "unclear".

## Predictions (each holds for each model)

| # | Quantity | Point | Range |
|---|---|---|---|
| R1 | C1 answers matching the indicator | 95% | ≥ 90% |
| R2 | C0 answers matching the indicator, on pre-AIA (N) items | 50% | 25–75% |
| R3 | C0 answers of AIA on pre-AIA (N) items: the silent failure, recency as authority | 25% | 10–50% |
| R4 | C0 answers matching the indicator, on AIA (Y) items | 75% | 55–95% |
| R5 | C0 accuracy on N items is below C0 accuracy on Y items | yes | |

**The claim.** Where the text gives a reader nothing that decides the regime, readers lean toward current law (R3,
R5). The grant date isn't the key here; the effective filing date is. If R3 is near zero, readers say "unclear"
instead, and the cooperative fence fails loudly, not silently, even here. That would be reported as such.
