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

## v3: excerpts from paragraph structure (obs-0162, audit obs-0164)

> **Provisional at handoff (2026-10-03): the review has landed and is not yet taken.** Codex's
> review of v3 (`docs/rule-currency-review-2.md`) reproduces the numbers but finds 5 P1 and 7 P2 issues.
> - **The excerpts can omit the illustrated rule's own limit.** In 1.902-4 #4, a pre-1978 limit
>   dropped out of context and Qwen moved the citation from `time_limited` to `untimed`. So the
>   reading of W3 below, that structure "removed apparent limits", is partly wrong: some of those
>   52 changes are real limits that disappeared.
> - **Four `structure.py` ancestry bugs:** sibling preference over inline Roman children,
>   discarded failures, applicability selection, and self-parents from combined designators.
> - **"Reader A applied the carryover criterion" is not supported item by item.**
> - **`verify_pins` doesn't check every pinned file**, and it waives superseded entries
>   unconditionally.
>
> Until these are taken, treat v3's range, W3's interpretation and the 1.909-6 reading as
> provisional, and don't run v4 on v3's excerpts.

*Predictions: [predictions/2026-10-03-rule-currency-v3-claude.md](../predictions/2026-10-03-rule-currency-v3-claude.md),
stamped before any v3 call. Design: [rule-currency-v3-design.md](rule-currency-v3-design.md).* The
question and labels are v2's. The judge now sees the section heading, the opening of each
ancestor paragraph, the worked example and what introduces it, the citation's own paragraph and
the applicability paragraph, all rebuilt from the CFR XML by `src/levadura_salvaje/structure.py`
in the same coordinates as the citation spans. Excerpt modes for the 548 records: 476 from
structure, 28 with a table or extract attached to the paragraph before it, and 44 on v2's window
as a declared fallback (43 failed designator chains, 1 table-of-contents heading).

| | Prediction | Measured | Verdict |
|---|---|---|---|
| W1 | Qwen v3 `untimed` 58% (45–70) | 66.6% (365) | **pass**, but in the opposite direction to my reasoning: up from v2's 61.5%, not down |
| W2 | **what the window hid**: v2 `untimed` → v3 `time_limited`, 10% (3–20) | **8.0%** (27 of 337) | **pass** |
| W3 | v2 `time_limited` → v3 `untimed`, 15% (5–30) | 27.7% (52 of 188) | **pass**, near the top |
| W4 | readers agree 85% (75–95) | 34 of 45 (75.6%) | **pass**, at the edge |
| W5 | consensus agrees with Qwen 80% (65–92) | 31 of 34 (91%) | **pass** |
| W6 | adjusted `untimed` midpoint below v2's 75.4% (p 0.6) | range 57.3–82.1%, midpoint 69.7% | **pass** |
| W7 | probe 1.902-3 #49 gets an `untimed` (p 0.6) | reader A `untimed`, reader B `time_limited`, Qwen `time_limited` | **pass** |

**Structure cuts both ways, and more often toward `untimed`.** Seeing the governing structure
revealed limits the window hid: 27 citations, W2. It also removed apparent limits that the
window had shown out of context: 52 citations, W3. Only 1 of the 44 window-fallback citations
changed label, so the instrument is stable where its input didn't change.

**The remaining disagreement is one ambiguity, concentrated in one section.** Nine of the
eleven disagreements are reader A `untimed` against reader B `time_limited`, and seven of the
eleven are in 1.909-6. Each is a rule whose *inputs* are from the past (pre-2011 split taxes,
pre-2018 years) but whose *application* is open-ended: "in taxable years ... ending after
February 9, 2015", "redeterminations ... that occur in taxable years ... ending on or after
November 2, 2020". The lens's carryover criterion says such a rule is `untimed`, and reader A
applied it. Reader B, and mostly Qwen, read the input period as the limit. That is my reading of
the criterion, not an adjudication, so the range below keeps both. This is the case I first
noticed on 2026-10-02, when the section-level lens and a caller disagreed about 1.909-6. It has
recurred at every grain since.

| `untimed` share, v3 | |
|---|---|
| Qwen v3, unadjusted | 66.6% |
| consensus items only | 71.5% |
| reader A alone | 77.7% |
| reader B alone | 61.7% |
| **disputed items counted out / in** | **57.3% – 82.1%** |
| bootstrap over consensus items, conditional | 56.2% – 86.6% |

**So, with the governing structure visible: between about three in five and four in five of the
§ 902 citations sit in rules that state no time limit.** v2's range was 65.8–84.9%. The
interval moved down a little and widened, because v3's audit found disagreement concentrated in
a heavy section (1.909-6 holds 84 of the 548 citations). The width now comes mainly from one
question: should a rule that applies past inputs in open-ended future years count as live? The
lens says yes, and half the judges don't follow it.

**Blinding** is verified as before: both readers' tool calls are in
`results/rule-currency-audit-v3-access-log.json`. A pinned-file check now runs over the whole
ledger (`scripts/verify_pins.py`; 143 pins verified, and the one mismatch is the superseded
obs-0163). I wrote that check after extending a pinned file in place and breaking obs-0161's pin.

**Next, if the lens continues:** the ambiguity has become the lens's open question. Either make
"past inputs, open-ended application" a fourth label, or adjudicate the criterion with a reader
who isn't Claude.

## v4: a label for closed inputs (stamped, not run)

*Predictions: [predictions/2026-10-03-rule-currency-v4-claude.md](../predictions/2026-10-03-rule-currency-v4-claude.md),
stamped before any v4 call, with one clarification also before any call.* v4 adds `closed_inputs`:
a rule with no end date of its own that applies only to amounts or events from periods that
ended before 2025. It never expires on paper, but it runs out of things to apply to. The idea
came from a second Opus instance's read of the v3 result, relayed by Tony. The run waits for the
v3 review's fixes.

**Two refinements from the same instance, to do before or alongside the v4 run:**
1. **A reader against itself.** Rerun fresh readers of the same model on the same 1.909-6 items
   (v2's 3 and v3's 7). If each model is stable in its own reading and they still differ,
   the split is interpretive. If a model flips on rerun, the "disagreement" is run-to-run noise
   that this section happens to show. This is the analogue of governance's
   bagging-variance baseline for a Rashomon set (governance, `rashomon-routed-decision-methodology.md`).
   It tests the instrument, not the hypothesis, so it can run without touching the stamped
   predictions.
2. **A class, or one drafter's idiom?** The ten 1.909-6 items share a section, a drafter and an
   idiom, so they are closer to one observation than ten. And "0 of 10 inside against about 90%
   outside" is exploratory by construction, because the stratum was found by the disagreement it
   then measured. To claim a *class* of rule: name other transition rules with closed inputs and
   open application by their structure, *before looking at any labels*, and predict that readers
   split there too. If only 1.909-6 splits, it's a quirk of that section's wording.
