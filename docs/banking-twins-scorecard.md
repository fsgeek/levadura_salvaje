# Scorecard: twin regulations in 2025 12 CFR, v1

*Scores predictions/2026-10-25-banking-twins-claude.md (stamped at 5ff4c09 before any twin but
Regulation B was measured) against obs-0179 and audit W1 (`results/banking-twins-audit-w1/`: 40
diverged pairs and 10 controls, with the copies shown as unattributed A and B in random order,
read blind in five batches by Opus (A) and Sonnet (B)). Written 2026-10-25.*

| # | Predicted | Measured | |
|---|---|---|---|
| T1 section pairs | 140 (110–170) | 137 | hit |
| T2 diverged share, B excluded | 25% (10–45%) | 48.8% | miss, above |
| T3 most diverged | Z | E (0.58; Z 0.57) | miss |
| T4 least diverged | M | M (0.11) | hit |
| T5 only-new sections, B excluded | 30 (10–60) | 34 | hit |
| W1 diverged judged stale | ≥ 40% each | 62.5% (A, 25/40) / 65% (B, 26/40) | hit |
| W1 controls not editorial | ≤ 1 of 10 | 0 (A) / 2 (B) | hit (A) / miss (B) |

The readers agree on 44 of 50 items. 24 pairs are judged stale by both.

**The finding.** In 2025, 24 sections of the Board's copies of Regulations Z, E and B carry text
the CFPB's copies have since amended (14 in Z, 5 in E, 5 in B). Both readers named which copy was
older without knowing which agency's it was, and in 50 of their 51 stale judgments the older copy
was the old agency's. Examples:
- § 226.20 keeps the 1987 adjustable-rate adjustment notice (25 to 120 days); § 1026.20 has the
  2013 ARM disclosure rules.
- §§ 226.34 and 226.35 are the 2008 HOEPA and higher-priced mortgage rules; §§ 1026.34 and
  1026.35 are the 2013 rewrites.
- § 202.14 is the pre-2013 appraisal rule, under which a copy is given on request; § 1002.14
  requires copies of all appraisals.
- § 205.18 is the 2006 payroll-card rule; § 1005.18 is the 2016 prepaid-account rule.
- §§ 226.55 and 226.59 lack the LIBOR-transition amendments of 2021 to 2023.
- § 202.16 still lists the Office of Thrift Supervision.

**What it means, and doesn't.** The Board's copies remain law for the institutions Dodd-Frank
left with the Board, chiefly certain motor-vehicle dealers (§ 1029), so most stale mortgage and
credit-card text has little practical reach. The audit doesn't say anyone is harmed. It says that
12 CFR, read as text, gives two answers to one question, that one of them is out of date, and
that nothing in the section itself says which. A system that retrieves "12 CFR 226.20" gets the
1987 rule.

**Differences from the prediction's frame.**
- Similarity is computed over words, not the characters used to size Regulation B, because some
  Regulation Z sections run to tens of thousands of characters.
- "Diverged" over-counts staleness: 10 (A) and 8 (B) of the 40 were intended scope differences, as
  in §§ 222.40 and 1022.40.
- Reader B's two non-editorial controls (§§ 222.41 and 332.15, ratios 0.97 and 0.98) are real but
  minor differences, which reader A also noted and called editorial.
- T2 was set too low: the CFPB amended more than I expected, and Regulation E's prepaid and
  remittance rules put it just ahead of Z.

**Where this goes.** This is the kind of change over time that the crosswalk couldn't see
(docs/banking-crosswalk-scorecard.md): not where the law lives, but which version of it a copy
holds. Next steps:
- Date each stale twin by the amendment it lacks.
- Read the 1997 and 2010 editions to show when the copies forked.
- Ask the same question of other agencies' twins (OCC, FDIC, NCUA).

**Cost.** About 4 s mechanical. Ten Claude subagent readings, no OpenRouter spend.
