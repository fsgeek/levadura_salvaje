# Scorecard: is the rule that depends on a repealed citation presented as live?

*The rule-currency lens asks the question three callers of the tool surface had
(docs/surface1-scorecard.md, round 3). The currency lens asked only whether a
section states *any* untimed rule. This lens asks whether *the rule a citation sits
in* is limited to the past. Population: the 548 resolved § 902 reference records in the
pinned citations sidecar (547 distinct spans; two inverted records share one), in 73
sections of the 2025 CFR. § 902 was repealed by Pub. L. 115-97 for years beginning after
2017. Citations inside ranges such as "sections 901 through 905" are outside the frame.
Reviewed by Codex: [rule-currency-review-1.md](rule-currency-review-1.md). Judge: Qwen3.8-27B
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
- Qwen: `not_a_rule` on 12 of 18, 5 `untimed`, 1 `time_limited`. Qwen gives only labels, so
  "because an example isn't a rule" is my inference, not its reason.

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

**The number, audit-adjusted (obs-0161, superseding obs-0159).** Each Qwen stratum's
population count is reallocated by the audit's labels in that stratum. The readers'
six disagreements matter, so the estimate is shown under every rule for them
(`scripts/audit_rule_currency.py adjust`):

| `untimed` share | |
|---|---|
| Qwen v2, unadjusted | 61.5% |
| consensus items only (disagreements excluded) | 82.1% |
| reader A alone, all items | 68.1% |
| reader B alone, all items | 82.6% |
| **disputed items counted out / in** | **65.8% – 84.9%** |
| bootstrap over the consensus items, conditional on them | 72.9% – 90.9% |

An earlier version of this scorecard gave "82% (73–91)" as a population estimate with a 95%
interval. That excluded the disagreements, which concern exactly the hard cases
(headings, applicability, past-period inputs). Its bootstrap treated Qwen's 337
`untimed` labels as certain (12 of 12 agreed) and covered only resampling of agreed items.
The review was right on both counts.

**So, of the § 902 citations in the 2025 regulations, between about two-thirds and
five-sixths sit in rules that state no time limit in the surrounding text.** Qwen alone
undercounts: it calls rules on past-period amounts time-limited. The section-level gap
between the two lenses stays small, at 4 of 59 sections (V3), but that compares model
labels and is not proof that a section is "current only because of other rules".

**What "untimed" does not mean, either.** It means the rule is live as written. It doesn't mean
the rule misleads. 1.367(b)-7's 21 citations are all `untimed`, including "As a result of
the repeal of section 902 effective for taxable years ... beginning on or after January 1,
2018, ...": a live rule that *acknowledges* the repeal. A lens that separates
"depends on the repealed provision" from "acknowledges its repeal" would be v3, a
different question, with its own predictions.

**"No time limit visible", not "still applies".** The excerpt (1,500 characters before,
700 after) can miss the governing limit. In the v2 audit sample, two example headings sit
2,584 and 4,251 characters before their citations. Both readers saw the same excerpt, so
their agreement can't detect a limit that neither could see. A v3 would retrieve the
paragraph's ancestry and the section's applicability paragraph.

**One consensus label is probably wrong.** Item 21 (1.902-3) carries an exception that
lets the section apply until ownership requirements are first met after 1986, with no
calendar end. Both readers said `time_limited`; the text supports `untimed`. Moving it
shifts the consensus estimate by 2.9 points.

**Blinding, verified.** Each of the four readers' tool calls was extracted from its
subagent transcript (`results/rule-currency-audit-access-log.json`). Each read its
instructions and its packet, then wrote its answers, and opened nothing else: no key, no
Qwen labels, not the other reader's file. Three items appear in both the v1 and v2
samples. With fresh readers and these access logs, that isn't a leak.

**Limits.** Claude-family readers (Opus and Sonnet), the same family that designed the
lens. Strata of 12 to 15 consensus items. `not_a_rule` was oversampled (15 of its 23). The
adjustment assumes the sample's per-stratum precision holds across the population. One
Code section, § 902; whether the shape holds for § 1201, § 46 or § 167 is untested.

## Review 1 (Codex) → changes

| # | Finding | Change |
|---|---|---|
| 1, 2 HIGH | 82% excluded disagreements; the "95% interval" treated Qwen's `untimed` stratum as certain | headline replaced by the range 65.8–84.9% under every disagreement rule; bootstrap relabelled as conditional; `adjust` computes all of it (obs-0161 supersedes obs-0159) |
| 3 HIGH | excerpt absence read as currency | "no time limit visible in the excerpt"; v3 named |
| 4 | resume and `record` lacked invariants | malformed, invalid-label or other-model cached rows are distrusted; `check_final` requires the exact population, once each, matching excerpts and valid labels, at write and at record (tests; mutants caught) |
| 5 | item 21's consensus contradicted by its exception | flagged above and in obs-0161 |
| 6 | blinding asserted, not shown | readers' tool calls extracted from transcripts; all four opened only instructions and packet |
| 7 | V4/V6 improvement confounded; 7/7 is weak | V4 and V6 stand as threshold checks only; the wording and the sample both changed, and v2's seven examples all illustrate live rules |
| 8 | scorer accepted inconsistent answers | answers must match the packet's items exactly, once each, with valid labels; `score` reports the packet's hash (tests; mutants caught) |
| 9 | 548 is records, not occurrences; range interiors excluded | population described as such; obs-0160 records 547 distinct spans |
| 10 | obs-0158 cited the v1 predictions; Qwen's "example isn't a rule" was inferred | obs-0160 supersedes obs-0158; the v1 section's explanation is marked as an inference below |
