# Predictions: provisions whose number stayed while their meaning moved (Claude)

*Pre-registered 2026-09-24 by a Claude Opus 5.5 instance, before comparing
headings across release points. Tony: the same open invitation as for the
fossil predictions applies here.*

## What I knew when writing this

The diff counts in obs-0125 (1,518 provisions added, 308 removed, 1,095
changed text between 119-4 and 119-110), and the fossil scorecard, where 11
"healed" citations turned out to point at re-used numbers (§168(n), §6659).
I have not compared any headings.

## The instrument (intent only)

For every USLM identifier present at both 119-4 and 119-110, compare the
provision's heading (whitespace-normalized, case-insensitive). If both are
non-empty and they differ, it is a **heading change**. If the identifier is
absent (or repealed) at 119-4 and in force at 119-110, it is a **revival**.
Both are reuse candidates. Then count the 2025 CFR citation occurrences (v2
extractor) whose path passes through a reuse candidate: the provision itself
or any of its ancestors.

## Predictions

**R1.** Identifiers with a heading change: **120** (40-400).
**R2.** Of those, the share at section or subsection level: **15%** (5-35%).
Most heading edits are deep, in paragraphs and below.
**R3.** Revivals: **12** (3-40).
**R4.** 2025 CFR citation occurrences through a heading-changed or revived
provision: **600** (150-2,000).
**R5.** Those occurrences concentrate: the top 3 Code sections account for
at least **50%** of them (fails below 50%). Point estimate 60%.
