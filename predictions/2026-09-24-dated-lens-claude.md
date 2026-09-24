# Predictions: do fossil candidates name a period that has ended? (Claude)

*Pre-registered 2026-09-24 by a Claude Opus 5.5 instance, before any call
for this lens. Tony: the standing invitation applies.*

## What I knew when writing this

The currency scorecard (obs-0132/0133): of 1,675 fossil candidates, Jev
labels 1,500 current, 149 historical and 26 no_rules, and the hand audit
agrees on 56/60. "Current" there means *at least one* undated rule, so it
mixes sections that never mention time with sections full of past dates
plus one undated clause. The misses were all sections of that second kind.
I have not asked any model the question below.

## The lens (intent only)

One Jev Choice question per chunk of each fossil candidate (same population
and chunking as the currency lens), judged from the text alone:

- **names_ended_period**: the text limits at least one of its rules to a
  period, date range or class of events that ended before 2025. Examples:
  "taxable years beginning before January 1, 1987", "property placed in
  service before 1981", "for 1975 and 1976", "amounts paid before the
  enactment of the Tax Reform Act of 1986". A start date alone ("after
  1986") is not an ended period;
- **silent**: the text states rules but limits none of them to an ended
  period. It may give start dates, or no dates at all;
- **no_rules**: the text states no rules (a table of contents, a reserved
  section, or pure cross-references).

A section's label is the strongest of its chunks: names_ended_period >
silent > no_rules. The label says whether a reader gets **any** textual cue
that some of the section is stale, which the currency lens could not
separate.

**Separation of duties**: a separate instance writes the question from this
intent section alone. The model is pinned (jev-1.13.0).

## Predictions

**D1.** Share of the 1,675 labeled silent: **55%** (40-70%).

**D2.** Share labeled names_ended_period: **42%** (28-58%).

**D3.** Among sections the currency lens labeled current, the share that
name an ended period: **38%** (25-55%).

**D4.** Among sections byte-identical to a 1997 section, the
names_ended_period rate is at least **1.3x** the rate among the rest.

**D5.** A blind hand audit (20 sections per Jev label, labelers see text and
definitions only) agrees with Jev on **88%** (fails below 80%).
