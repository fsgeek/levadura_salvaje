# Scorecard: is the rule that depends on a repealed citation presented as live?

*The rule-currency lens asks the question three callers of the tool surface had
(docs/surface1-scorecard.md, round 3). The currency lens asked only whether a
section states *any* untimed rule. This lens asks whether *the rule a citation sits
in* is limited to the past. Population: the 548 citations of § 902, repealed by Pub. L.
115-97 for years beginning after 2017, in 73 sections of the 2025 CFR. Judge: Qwen3.8-27B
under an `ayllu-gpu` lease.*

## v1 (obs-0156, audit obs-0157)

*Predictions: [predictions/2026-10-02-rule-currency-claude.md](../predictions/2026-10-02-rule-currency-claude.md),
stamped before any call.*

| | Prediction | Measured | Verdict |
|---|---|---|---|
| R1 | `untimed` 50% (30–70) | 50.2% (275) | **pass** |
| R2 | `time_limited` 35% (20–55) | 39.1% (214) | **pass** |
| R3 | `not_a_rule` 15% (5–30) | 10.8% (59) | **pass** |
| R4 | **the gap**: sections current by both currency judges with no `untimed` § 902 citation, 30% (15–50) | **8.5%** (5 of 59: 1.367(b)-10, 1.901(m)-1, 1.905-5, 1.960-3, 1.960-4) | **fail, low** |
| R5 | 1.902-1 ≥ 70% `untimed` (p 0.75) | 63% (34 of 54; 12 `not_a_rule`) | **fail** |
| R6 | 1.902-3 ≥ 70% `time_limited` (p 0.75) | 100% (17 of 17) | **pass** |
| R7 | 1.904-7 ≥ 60% `time_limited` (p 0.6) | 68% (65 of 96) | **pass** |
| R8 | blind consensus agrees with Qwen, 75% (60–88) | 20 of 21 consensus items (95%) | **fail, high**, and not meaningful: the consensus is the 21 easy items |
| R9 | the two blind readers agree, 85% (70–95) | **21 of 45 (47%)** | **fail** |

**The audit's finding: v1 doesn't say what a worked example is.** 18 of the 45 sampled
citations sat in worked examples ("Example 4. ... In 1992, Corporation M ..."), and each
of the three judges applied its own consistent rule to them:
- reader A (Opus): `untimed` on 17 of 18, judging the rule illustrated;
- reader B (Sonnet): `time_limited` on 18 of 18, judging the example's dated facts;
- Qwen: `not_a_rule` on 12 of 18, because an example isn't a rule.

On the 27 non-example items, the readers agree on 20 (74%), and Qwen agrees with reader B
on 25 (93%). The remaining splits are the same kind of gap, smaller: transition
carryovers in 1.904-7, and "see § 1.909-6T for rules applicable to ..." pointers.

So R9's failure isn't noise. The instrument was underspecified, and the audit located
the gap exactly. I had looked at three of Qwen's 1.367(b)-7 labels while the readers
worked, and suspected examples. My check, the word "Example" within 400 characters,
found only 4 of the 24 disagreements, because the example headings sit further back.
The readers' own `decisive_text` found 17.

**R4.** Taking v1 at face value, the section-level lens was a better proxy for the
callers' question than I expected. Only 5 of the 59 "current" sections have no untimed
§ 902 rule. Since examples were judged three ways, R4 depends on how examples are read,
which v2 has to settle first.

**Audit limits.** Both readers are Claude subagents, so not independent of the family
that designed the lens. Examples were identified after the fact from the readers'
decisive text.

## v2

*Predictions: [predictions/2026-10-02-rule-currency-v2-claude.md](../predictions/2026-10-02-rule-currency-v2-claude.md),
stamped before any v2 call.* v2 decides the three open cases. Examples take the timing of
the rule they illustrate. Carryovers with no end date are untimed. Pointers are
`not_a_rule`. Those are decisions about meaning, made after the audit, chosen for the
callers' question: an example computing a § 902 credit under a rule with no end date
teaches a live computation.

| | Prediction | Measured | Verdict |
|---|---|---|---|
| V1 | at least half of v1's 59 `not_a_rule` move (p 0.7) | 38 of 59 moved, all to `untimed` (the examples) | **pass** |
| V2 | `untimed` 60% (52–72) | 61.5% (337; obs-0158) | **pass** |
| V3 | gap at most 6 of 59 (p 0.7) | 4 (1.367(b)-10, 1.905-5, 1.960-3, 1.960-4) | **pass** |
| V4 | new blind readers agree, 80% (65–92) | **39 of 45 (87%)**, up from 47% | **pass** |
| V5 | consensus agrees with Qwen, 85% (70–95) | 30 of 39 (77%) | **pass** |
| V6 | readers agree on worked examples ≥ 80% (p 0.65) | 7 of 7 | **pass** |

**The wording took for the readers.** They went from 47% to 87% agreement, and from three
rules for examples to one. **It didn't fully take for Qwen.** Where Qwen said
`time_limited`, the blind consensus said `untimed` 7 times in 12. Each time, the rule
*operates on amounts from a past period*: "pre-1987 accumulated profits", carryforwards of
unused taxes, recapture of old separate-limitation loss accounts. But the rule itself
applies today with no end date. That is v2's carryover case, and the readers applied it
while Qwen didn't. Where Qwen said `untimed`, the consensus agreed 12 of 12.

**The number, audit-adjusted (obs-0159).** Reallocating each Qwen stratum by its consensus
labels, with the 6 disagreements excluded and a within-stratum bootstrap:

| | Qwen v2 | audit-adjusted share, 95% interval |
|---|---|---|
| `untimed` | 337 (61.5%) | **82% (73–91)** |
| `time_limited` | 188 (34.3%) | 14% (6–23) |
| `not_a_rule` | 23 (4.2%) | 4% (3–4) |

**So about four in five citations of the repealed § 902 in the 2025 regulations sit in
rules that, by their own words, still apply.** This is the citation-level counterpart of
the currency lens's section-level "about nine in ten unmarked fossils" (obs-0132/0146).
At citation level the gap between the two lenses stays small: 4 of 59 sections (V3).

**What "untimed" does not mean.** It means the rule is live as written. It doesn't mean
the rule misleads. 1.367(b)-7's 21 citations are all `untimed`, including "As a result of
the repeal of section 902 effective for taxable years ... beginning on or after January 1,
2018, ...": a live rule that *acknowledges* the repeal. A lens that separates
"depends on the repealed provision" from "acknowledges its repeal" would be v3, a
different question, with its own predictions.

**Limits.** Claude-family readers (Opus and Sonnet), the same family that designed the
lens. Strata of 12 to 15 consensus items. `not_a_rule` was oversampled (15 of its 23). The
adjustment assumes the sample's per-stratum precision holds across the population. One
Code section, § 902; whether the shape holds for § 1201, § 46 or § 167 is untested.
