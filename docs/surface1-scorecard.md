# Scorecard: the first callers of the tool surface

*Predictions: [predictions/2026-10-01-surface1-claude.md](../predictions/2026-10-01-surface1-claude.md)
(committed and stamped before either caller ran). Surface, brief, answers and
footprints: [spikes/surface1/](../spikes/surface1/). Measurements: obs-0152, obs-0153.*

Two fresh subagents with no project context, one Opus 5.5 and one Sonnet 5.5, got
[the brief](../spikes/surface1/BRIEF.md) and the CLI. The question came from a
practitioner: where does reliance on Code provisions that no longer exist
concentrate, and what would a reader of those regulations be misled about? I score
moves from the footprints in `queries` (`footprints.json`), not from what the
callers said they did. Grain runs from overview 0 to cell 1, drill/cited_by 2,
unit 3 and cite/follow 4.

| | Prediction | Opus | Sonnet | Verdict |
|---|---|---|---|---|
| S1 | first call is `overview` | yes | yes | **pass** |
| S2 | reaches the words (`cite`/`follow`) | 52 calls | 6 calls | **pass** |
| S3 | **returns to the population because of something it read** (0.6 each) | no, see below | no | **fail, both** |
| S4 | the answer has a tool number and a quoted passage | yes, labeled | yes, labeled | **pass** |
| S5 | notices and *checks* a reused number (0.3 each) | no | named the risk, didn't check | **fail** (as expected) |
| S6 | no grain error (0.6 each) | none | none (every number re-checked against `overview`) | **pass** |
| S7 | 12–45 calls | 65 | 13 | **Opus fail**, Sonnet pass |
| S8 | no bypass | brief + CLI only | brief + CLI only | **pass** |
| S9 | Opus makes more up moves (0.55) | 7 | 1 | **pass, but empty** (see S3) |

## S3: the claim that mattered failed, and how

The two paths through the grain levels:

```
opus    01123444444444344444344444344444344444344444444444444344444444234
sonnet  0112234443444
```

Both callers ran a clean funnel down: overview, then cells, then one target
(`cited_by`), then sections, then text. Every "up" move after that was sideways at
the bottom, from the text of one section to the citation list of the next. Opus's
one population call after reading (call 62, `cited_by 204`) chased something it
had seen in `cell 54` at call 2, before it read anything.

The readings did raise population questions, and neither caller could ask them.
- **Opus** found the distinction that matters: whether a citation of repealed § 902
  is deliberate history (§ 1.367(b)-7 says "As a result of the repeal of section
  902…") or stale law (§ 1.6038-2(k), which applies to years beginning after the
  repeal). The next question is how many of the 73 sections citing § 902 are
  which. The surface has no operation that takes something learned by reading
  back to the population. Opus answered it by hand for six sections and listed it
  as a need: "A flag for whether a section mentions the repeal or limits itself to
  earlier years."
- **Opus** found that 182 of part 54's broken citations are ERISA's § 204(h): one
  section introduces it as ERISA's, then writes "section 204(h)" alone. The
  population question is how often this happens. I asked it myself
  (**obs-0153**): at most 392 citations in 48 sections, 283 of them broken. That
  is ≤ 2.7% of the 10,300 broken citations, and 182 of the 283 are that one
  section. It's an upper bound within a section only.

**So the return to population scale isn't a disposition the caller has or lacks.
It needs an instrument.** The way down is built: the index, rollups, drill,
follow. The way up needs a cheap predicate the reader can define from what it
read and run over a population, such as "mentions the repeal" or "has
an applicability date after 2017". That's section 3 of [the seed](the_seed.md),
cheap semantic models as instruments, meeting the surface. It is the next thing
to build.

## Defects the callers found

- **Spans were in another text domain** (Opus). `cite` sliced the stored flat text
  with spans that index `citations.normalize(text)`. Normalizing closes things
  like "( PRS )", so every later offset shifts. **obs-0152:** 36,419 of 110,668
  section-head spans (33%) were misplaced. With the normalized text, none are.
  The hash check passed throughout, because it covers the text, not the span.
  Fixed: `cite` normalizes, declares `text_domain`, and reports `span_check`.
  Tests pin the span literally, and a mutant without normalization is caught.
  Spike 2's `follow` has the same gap. A span needs a declared domain, just as a
  hash does.
- **A provision id with "/" raised a stack trace** (Sonnet). Fixed: ids are
  validated before the database.
- **Other-statute aliases** (Opus): obs-0153, above. This is an extractor
  limitation, recorded and not patched. Patching it would change the measured
  citation set behind earlier ledger entries.
- **One citation of "section 4016(a)"** in § 48.4061(a)-1 is probably a typo for
  4061(a) in the regulation itself (Sonnet). That's a corpus defect, so the index
  correctly scores it absent-section.

Before either caller ran, my own smoke test found one more: one section's citation
list timed out at 60 s, a join with no usable index. Three storage spikes had
checked correctness under change, cell by cell, and none of them asked that.

## What the callers needed (merged, deduplicated)

1. **A way back up:** a predicate over a population, defined by the reader (see
   S3).
2. **Per-section counts** in `drill` and `cited_by`, so a list can be ranked
   without opening each section (both callers).
3. **Code text by section number.** `follow provision` took only a key reached
   through `cite` (Sonnet).
4. **History:** successor provisions for repealed sections, amendment dates, and
   earlier CFR editions (both). The index holds one snapshot. Earlier editions are
   in `data/`, so this is a loading job, not a research one.
5. **Search inside a section's text**, and the paragraph and applicability date a
   citation sits in (Opus).
6. **Severity:** whether a citation is the operative authority or a passing
   cross-reference (Sonnet).
7. **Other-statute recognition** (Opus; obs-0153).

## Two callers, two styles

Opus made 65 calls in 5.5 minutes and read deeply: it reached a legal judgment
on § 1.6038-2(k) and separated it from what the index establishes. Sonnet made
13 calls in 70 seconds and gave a correct, more cautious answer. Its conclusion
about part 48 ("the likely misleading effect is that a reader treats the
regulation as the current rule. I did not establish that.") is honest about
reaching only the address level. Both labeled every claim as a tool number or a
quote, as the brief asked. Neither made a grain error.
