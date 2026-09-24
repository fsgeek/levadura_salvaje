# Scorecard: a small reader with and without the ledger

*Predictions: [predictions/2026-09-24-bounded-reader-claude.md](../predictions/2026-09-24-bounded-reader-claude.md).
Measurement: obs-0142, `results/bounded-reader-v1-2025.jsonl`. Evidence
packets: `results/bounded-reader-v1/`.*

This is the first direct test of the project's claim. Claude Haiku 4.5 read
60 sections of the 2025 CFR, one fresh instance per section, and answered:
*does this section state at least one rule that still operates for a 2025
taxable year?* It answered once from the text alone (**A**) and once with
the ledger's evidence packet (**B**), which lists each cited provision's
status at 119-4, its repeal year, any move or reuse, and the dated lens's
label, in about 2,000 characters at most. Ground truth is two Claude Opus
5.5 judges with the statute XML and their own knowledge; they disagreed on
2 sections, which were adjudicated.

| stratum | truly operates | A correct | B correct |
|---|---|---|---|
| unmarked fossils | 14/20 | 15/20 | **19/20** |
| dated fossils | 13/20 | 17/20 | 18/20 |
| controls (no broken citation) | 17/20 | 17/20 | 17/20 |
| **all** | 44/60 | **49/60 (82%)** | **54/60 (90%)** |

B is right where A is wrong on 6 sections, and the reverse on 1. That's
exact McNemar p = 0.125, suggestive but not significant at this size.

| | Prediction | Measured | Verdict |
|---|---|---|---|
| B1 | A on unmarked fossils ≤ 40% | 75% | **fail** |
| B2 | B − A on unmarked fossils ≥ +25 pts | +20 | **fail** |
| B3 | B on controls no worse than A − 5 | 85% vs 85% | **pass** |
| B4 | B − A overall ≥ +15 pts | +8.3 | **fail** |
| B5 | unmarked fossils that still operate: 45% (25-65) | 70% | **fail** |

## What failed, and why it matters

**My central premise was wrong: most fossils are not dead.** The panel says
70% of unmarked fossils, and 65% of dated ones, still state a rule that
operates in 2025. A broken citation usually marks a *stale reference*
inside live law: §1.193-1 still governs the tertiary-injectant deduction
while citing the repealed windfall-profit tax; §2056A regulations still
work while pointing at §2102(c), now (b). Because the right answer is mostly
"yes", a text-only reader that assumes rules are current scores well (B1),
and the room for evidence to help is small (B2, B4).

**Where the evidence helps, it helps in one direction.** All six sections
B fixed were ones where the evidence told the reader something the text
could not. Four are *dead* sections the text reader thought alive: §1.1251-4
(§1251 repealed 1984), §1.822-12, 301.9100-9T and §1.6074-2. Two are the
reverse: A read a dead citation as a dead rule, and B's packet showed the
rest of the section's statute is live. Evidence moved the reader toward the
truth both ways.

**The ledger can't see what the statute doesn't show.** Three "controls"
(no broken citation) are dead, and both readers missed all three. §1.683-1
implements the *1954* §683, and today's §683 is a different provision: the
citation resolves because the number was reused. The ERC recapture rule is
tied to 2021 wages. The oil-spill fee regulation cites Code sections that
exist while the fund it serves was replaced in 1990. Existence checks, the
ledger's main instrument, are blind to all three kinds.

## Limits

- **The panel saw the same evidence packet as reader B.** That can lean the
  ground truth toward B. It was pre-registered, but it means B's advantage
  here is an upper bound.
- The ground truth is model judgment, not a tax lawyer's.
- n = 20 per stratum; each section is one point.

## What it means for the thesis

A small reader given a small, well-chosen slice of an external ledger was
more accurate (90% vs 82%), fixed six errors for one, and lost nothing on
healthy sections. That is the claim in miniature. But the *size* of the
benefit depends on how often the text is misleading, and here it misleads
less than I thought: most dead citations sit inside live rules. The
evidence that would help most next is the kind the ledger doesn't collect
yet: whether a cited number *means the same thing* now (reuse), and whether
the program a rule serves still exists.
