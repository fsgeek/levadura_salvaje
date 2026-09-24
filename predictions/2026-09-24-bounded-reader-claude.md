# Predictions: does a small reader do better with the ledger's evidence? (Claude)

*Pre-registered 2026-09-24 by a Claude Opus 5.5 instance, before any reader
or panel was run. Tony: the standing invitation applies. This is the first
direct test of the project's claim: keep cognition small, let the world
stay large.*

## The experiment (intent only)

**Population:** 60 sections of the 2025 CFR, seeded and stratified. 20
**unmarked fossils** (fossil candidates the currency lens calls current and
the dated lens calls silent). 20 **dated fossils** (candidates the dated
lens says name an ended period). 20 **controls** (no broken citation at
119-4).

**Question:** *Does this section state at least one rule that still
operates for a taxable year beginning in 2025?* Answer yes or no.

**Ground truth:** a panel of two independent Claude Opus 5.5 judges, with
disagreements adjudicated by a third. The judges get the section text, the
26 USC XML at 119-4 to search, and the ledger's evidence packet (below).
They may use their own knowledge of tax law. They don't see strata,
readers' answers or predictions.

**The bounded reader:** Claude Haiku 4.5, one fresh instance per section per
condition, no tools.
- **A (text only):** the section text and the question.
- **B (text + evidence):** the same, plus the ledger's packet for the
  section: each cited Code provision with its status at 119-4 (resolves,
  repealed with year, absent section or subdivision), any reuse or move flag
  for it, and the dated lens's label. The packet is small by design, well
  under 2,000 tokens.

## Predictions

**B1.** Reader A's accuracy on unmarked fossils: at most **40%** (point
30%). Their text gives no cue.

**B2.** Reader B's accuracy on unmarked fossils is at least **25 points**
above A's (point +35).

**B3.** On controls, B's accuracy is no more than **5 points** below A's.
Evidence of health doesn't mislead.

**B4.** Over all 60, B's accuracy is at least **15 points** above A's
(point +20).

**B5.** Ground truth: the share of unmarked fossils the panel says still
operate is **45%** (25-65%). Many candidates still work: a broken
subdivision citation doesn't kill a rule that also stands on live statute.
