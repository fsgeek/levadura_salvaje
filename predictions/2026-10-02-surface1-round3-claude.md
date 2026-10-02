# Predictions: round 3, a stored reading whose question nearly matches

*Written 2026-10-02 by the owning instance (Claude Opus 5.5), after rounds 1 and 2
were scored ([docs/surface1-scorecard.md](../docs/surface1-scorecard.md)) and before
round 3 runs. **Exploratory**, n = 1 per model.*

Round 3 adds one tool, `lens`
([spikes/surface1/instrument.py](../spikes/surface1/instrument.py)). It counts a
stored reading over a population. The only lens is `currency` (obs-0132 Jev,
obs-0146 Qwen, obs-0133 hand audit). Its question is section-level: does the section
state *any* rule with no time limit? The callers' question is closer to "are the
rules that depend on the repealed provision presented as live?". These differ.
Before writing this, I checked one case of each kind in the text:
- 1.909-6 ("Pre-2011 foreign tax credit splitting events") is `current` under the
  lens's definition, because its applicability paragraph is open-ended. Opus-2
  read it as transition law. Both are defensible, under different questions.
- 1.902-3 is `historical`, and its title limits it to years "beginning before
  January 1, 1987". Opus-2 had put it with the live ones. The lens was right and
  the caller wrong.

Over the 73 sections citing § 902, the lens says: Jev 62 current, 9 historical,
2 no_rules; Qwen 61, 7, 5; the judges agree on 68.

New callers `caller-opus-3` and `caller-sonnet-3` get the same question and
[BRIEF-3.md](../spikes/surface1/BRIEF-3.md), whose tool list gains `lens` and nothing else.

| | Prediction |
|---|---|
| U1 | Each caller calls `lens` at least once. 0.8 each. |
| U2 | Any caller that uses `lens` reports one of its counts in the answer. 0.8. |
| U3 | **The check.** A caller `cite`s or `follow`s a unit *after* `lens` has returned that unit, in a sample or a list. Opus 0.5, Sonnet 0.35. |
| U4 | **The mismatch named.** At least one answer says that the lens's question differs from the caller's: section-level "any untimed rule" against whether the § 902-dependent rules are live. 0.35. |
| U5 | **The failure mode.** At least one answer treats `current` as "misleading" or "relies on dead law" without saying the lens doesn't measure that. 0.4. |
| U6 | No grain errors. 0.6 each. |
| U7 | Fewer text calls (`cite` + `follow`) in total than round 2's 13 (Opus 10, Sonnet 3). A stored reading substitutes for reading. 0.6. |

U3 and U4 together are the point. A tool that hands over earlier readings is useful
only if callers treat a reading as a claim with a question attached, not as a fact.
U5 is the opposite outcome, written down so that it can be seen if it happens.
