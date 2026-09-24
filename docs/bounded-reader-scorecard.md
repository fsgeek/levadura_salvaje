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

## v2: the circularity removed (obs-0145)

*Predictions: [predictions/2026-09-24-bounded-reader-v2-claude.md](../predictions/2026-09-24-bounded-reader-v2-claude.md).
120 fresh sections, disjoint from v1. **The panel never saw the evidence
packet.** It judged from the text, both statutes (1997 and 2025) and its own
knowledge. The packet adds 28-year reuse flags. There is a new stratum:
reuse-exposed sections (no broken citation, but citing a number reused or
restructured since 1997).*

| stratum | truly operates | A (text) | B (text + packet) |
|---|---|---|---|
| unmarked fossils | 22/30 | 22/30 | **28/30** |
| dated fossils | 18/30 | 22/30 | **26/30** |
| controls | 24/30 | 26/30 | 26/30 |
| reuse-exposed | 29/30 | 29/30 | 29/30 |
| **all** | 93/120 | **99 (82.5%)** | **109 (90.8%)** |

**B fixes 13 sections for 3 new errors, exact McNemar p = 0.021.** With the
circularity gone, the v1 result replicates almost exactly (+8.3 points
both times) and is now significant.

| | Prediction | Measured | Verdict |
|---|---|---|---|
| V1 | B − A overall ≥ +5 (point +7) | +8.3 | **pass** |
| V2 | B − A on reuse-exposed ≥ +10 | 0 | **fail** |
| V3 | reuse-exposed that don't operate: 20% (8-35) | 3.3% (1/30) | **fail** |
| V4 | B on controls ≥ A − 5 | 0 | **pass** |
| V5 | unmarked fossils that operate: 65% (50-80) | 73% | **pass** |

**Reuse exposure is mostly harmless.** 29 of 30 reuse-exposed sections still
operate. A regulation citing a reused number usually cites its *new*
meaning, because it was written or updated after the change: the BBA
partnership regulations cite the new §6223, and the BEAT regulations cite
the new §59A. The ten 1997-identical citers in obs-0143 are the dangerous
minority, and a random draw from the 94 exposed sections rarely hits them.
So the reuse flags had nothing to fix here (V2, V3).

**Where the evidence helps is the fossils.** 11 of the 13 fixes are fossil
candidates the text reader called alive and the panel calls dead:
§1.826-3, §1.1342-1, §1.812-6, §1.802-3, §301.6223(f)-1 (TEFRA),
§1.965-6, and others. The 3 new errors are fossils the packet made look
dead while a rule still operates (§1.167(l)-3, §1.267(d)-2), plus one
control.

**For the thesis:** twice now, on 180 sections in total, a small reader with
a ~2,000-character slice of an external ledger beats the same reader
without it by 8 points. The whole gain comes from exactly the sections the
ledger was built to see. Nothing is lost on healthy ones.
