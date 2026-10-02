# Scorecard: the first callers of the tool surface

*Predictions: [predictions/2026-10-01-surface1-claude.md](../predictions/2026-10-01-surface1-claude.md)
(committed and stamped before either caller ran). Surface, brief, answers and
footprints: [spikes/surface1/](../spikes/surface1/). Measurements: obs-0154, obs-0155 (corrections of
obs-0152 and obs-0153). Reviewed by Codex: [REVIEW.md](../spikes/surface1/REVIEW.md). This version takes
its fixes, and the table at the end maps findings to changes.*

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
| S3 | **returns to the population because of something it read** (0.6 each) | one population call after text, not traceable to a reading | none | **fail, both** (the causal clause isn't measurable from footprints; see below) |
| S4 | the answer has a tool number and a quoted passage | yes, labeled | yes, labeled | **pass** |
| S5 | notices and *checks* a reused number (0.3 each) | no | named the risk, didn't check | **fail** (as expected) |
| S6 | no grain error (0.6 each) | none | none (every number re-checked against `overview`) | **pass** |
| S7 | 12–45 calls | 65 | 13 successful (≥ 15 attempted: failed calls weren't logged then) | **Opus fail**, Sonnet pass |
| S8 | no bypass | brief + CLI only | brief + CLI only | **pass**, from the subagent transcripts' tool calls, not the footprints |
| S9 | Opus makes more up moves (0.55) | 7 | 1 | **pass**, but it counts adjacent grain changes, not population reasoning |

## S3: the claim that mattered failed, and how

The two paths through the grain levels:

```
opus    01123444444444344444344444344444344444344444444444444344444444234
sonnet  0112234443444
```

Both callers ran a clean funnel down: overview, then cells, then one target
(`cited_by`), then sections, then text. After that, the up moves were these:
- Opus, five times: from the text of one section to the citation list of the next.
- Opus, once: the same section, widened from broken citations to all of them.
- Opus, once, the only population call after reading: `cited_by 204` at call 63
  of 65. It follows up something seen in `cell 54` at call 3, before any reading.
  Whether the reading also prompted it, the footprints can't say.
- Sonnet, once: paging within the same section.

The readings did raise population questions that the surface couldn't express.
`cited_by` could re-count a target, and a caller could classify sections by hand,
which Opus did for six.
- **Opus** found the distinction that matters: whether a citation of repealed § 902
  is deliberate history (§ 1.367(b)-7 says "As a result of the repeal of section
  902…") or stale law (§ 1.6038-2(k), which applies to years beginning after the
  repeal). The next question is how many of the 73 sections citing § 902 are
  which. Answering it means aggregating a predicate the reader defines, and no
  tool does that. Opus listed it as a need: "A flag for whether a section mentions
  the repeal or limits itself to earlier years." Sonnet asked for nothing like it.
- **Opus** found that 182 of part 54's broken citations are ERISA's § 204(h): one
  section introduces it as ERISA's, then writes "section 204(h)" alone. The
  population question is how often this happens. I asked it myself
  (**obs-0155**, correcting obs-0153). Some sections name "section N of <another
  statute>". In those sections, 374 bare Code citations of the same N are
  candidates, in 48 sections, and 282 of them are broken: 2.7% of the 10,300
  broken citations. 182 of the 282 are that one section. This counts candidates
  under the seeds the regex detects, so it is **not** a ceiling on aliasing:
  aliases defined in another section, and seeds the regex misses, aren't counted.

**My reading of this, which these runs can't establish: the return to population
scale needs an instrument, not just a disposition.** Footprints record moves, not
reasons. n = 1 per model, and only one caller asked for the missing operation.
[Round 2](../predictions/2026-10-01-surface1-round2-claude.md) tests it directly:
same question, fresh callers, one added tool. The way down is built: the index, rollups, drill,
follow. The way up needs a cheap predicate the reader can define from what it
read and run over a population, such as "mentions the repeal" or "has
an applicability date after 2017". That's section 3 of [the seed](the_seed.md),
cheap semantic models as instruments, meeting the surface. It is the next thing
to build.

## Defects the callers found

- **Spans were in another text domain** (Opus). `cite` sliced the stored flat text
  with spans that index `citations.normalize(text)`. Normalizing closes things
  like "( PRS )", so every later offset shifts. **obs-0154** tracks every character
  through normalization. 41,415 of 110,668 section-head spans (37%) point
  elsewhere in the flat text. 4,996 of those still contain the cited number, so a
  containment check undercounts. obs-0152 reported only the 36,419 that fail it.
  Mapped back, all 110,668 land on their number. The hash check passed
  throughout, because it covers the text, not the span.
  Fixed: `cite` normalizes, declares `text_domain`, and reports `span_check`.
  Tests pin the span literally, and a mutant without normalization is caught.
  Spike 2's `follow` has the same gap. A span needs a declared domain, just as a
  hash does.
- **A provision id with "/" raised a stack trace** (Sonnet). Fixed: ids are
  validated before the database.
- **Other-statute aliases** (Opus): obs-0155, above. This is an extractor
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
7. **Other-statute recognition** (Opus; obs-0155).

## Two callers, two styles

Opus made 65 calls in 5.5 minutes and read deeply: it reached a legal judgment
on § 1.6038-2(k) and separated it from what the index establishes. Sonnet made
13 calls in 70 seconds and gave a correct, more cautious answer. Its conclusion
about part 48 ("the likely misleading effect is that a reader treats the
regulation as the current rule. I did not establish that.") is honest about
reaching only the address level. Both labeled their numbers and quotes, as the
brief asked, though not every claim is supported: Opus's "many of the 73 sections
cite § 902 on purpose" rests on six sections read. Neither made a grain error.

## Review 1 (Codex) → changes

| # | Finding | Change |
|---|---|---|
| 1 HIGH | `cite` joined sidecar metadata to a different generation's assertions | sidecar pinned by sha256; `cite` and `unit` refuse when the sidecar's paths disagree with the stored occurrences (tested, mutant caught) |
| 2 HIGH | USC manifest taken as the stream's latest | taken from the index manifest's `depends_on` |
| 3 HIGH | S3's causal conclusion exceeds the evidence | reworded as a hypothesis; round 2 tests it |
| 4 | S9's transitions misdescribed; call numbers off by one | described per transition; call 63 and call 3 |
| 5, 6 | alias probe missed capitalized seeds, counted the Code as another statute, overstated a ceiling | v2 regex, bare heads only, all statutes reported; obs-0155 says what it bounds |
| 7 | obs-0152 counted containment failures as "misplaced" | origin tracking through normalization; obs-0154 |
| 8 | failed calls weren't footprints | `Surface.failed`, from the CLI and the MCP server; S7 and S8 qualified (argument errors before the surface exists still go unlogged) |
| 9 | negative cursors and offsets gave misleading pages | refused (tested) |
| 10 | `cite`/`follow` lacked the common metadata | added; `drill`'s footprint `returned` is spike 2's list, left as is |
| 11 | tracebacks and non-JSON errors remained | CLI parser errors and every exception come back as JSON; MCP initialization is inside the handler |
| 12 | `cell`'s target table had no continuation | `cell --cursor` |
| 13 | the provision test didn't go through `follow` | tests through the methods with a fake database; four guards each checked by a mutant |
| minor | "every claim"; 10 statutes of 28 reported | reworded; all reported |

## Round 2: the same question, with `measure`

*Predictions: [predictions/2026-10-01-surface1-round2-claude.md](../predictions/2026-10-01-surface1-round2-claude.md),
stamped before the run. Reviewed by Codex: [REVIEW-2.md](../spikes/surface1/REVIEW-2.md), which reproduced
all 17 `measure` counts and this section's corrections come from. Fresh callers `caller-opus-2` and `caller-sonnet-2`,
[BRIEF-2.md](../spikes/surface1/BRIEF-2.md). The tool list gained `measure` and
nothing else changed. Answers verbatim in `answer-caller-*-2.md`; footprints in
`footprints.json`; every `measure` count a caller reported matches its recorded
footprint.*

```
opus-2    01222222234424242244442233434      (29 calls, 10 measure)
sonnet-2  01223442211122342222               (20 calls,  7 measure)
```

| | Prediction | Opus | Sonnet | Verdict |
|---|---|---|---|---|
| T1 | `measure` after the first `cite`/`follow`, pattern from words read (0.75 / 0.55) | call 15, `effective date\|applicab\|applies to`, right after reading the applicability paragraph at the end of 1.902-1 (call 14) | calls 8–9, `section 204\(h\)` and `ERISA` near 204, right after `cite` showed "section 204(h) of ERISA" | **pass, both** |
| T2 | a pattern revised after its samples (0.5) | `repeal`, then qualifiers, then `2017\|2018` near and anywhere, then applicability | four patterns over the § 902 population | **pass** |
| T3 | a count reported with a caveat from that run's samples (0.45) | "7 contain 'repeal' … some of those hits are about other repeals, such as §963 and §904(d)(1)(E)" | caveat general, not from samples | **pass** (Opus) |
| T4 | no grain errors (0.6 each) | none found | none found | **pass** |
| T5 | a share claim about a concentration (0.7 given T1) | "17 mention 2017 or 2018 anywhere. 56 never do", of 73 | "matched 21 of 73 sections" | **pass, both** |
| T6 | Opus calls `measure` more often (0.6) | 10 | 7 | **pass** |

**What changed.** Round 1's paths ran down and stayed at the bottom. Round 2's
paths oscillate between the population (2) and the words (4). Opus used `measure`
before calling `cite`/`follow` as well as after (calls 5–8). Strictly, though,
that wasn't "before reading": `measure` returns passages from several
sections, so it reads as well as counts. Both callers reported shares of the
§ 902 concentration that no round-1 caller made. They are **lexical** shares,
not classifications. "17 of 73 mention 2017 or 2018" is a regex result, and Opus's
13 "date or 'as in effect' qualifiers" near § 902 include qualifiers about 1986
and about § 904, not acknowledgments of § 902's repeal (review 2). Opus's answer
then reads exemplars on both sides:
- deliberate transition law: 1.909-6, 1.904-7 and 1.905-5, titled as such;
- regulations that read as live: 1.902-1, amended in 2021 and still giving no end
  date, and 1.6038-2, which applies to post-2018 years but defines a term "as
  described in section 902(c)(5)".

That is the shape the seed asks for, counts plus counterexamples. The counts
don't measure "misleading", and both answers say so.

**What this does and doesn't show.** Round 1's hypothesis survived a test it
could have failed: T1 was the claim, and both failing would have refuted it. It
did not *isolate* the cause. Between rounds, more changed than the brief's one
word:
- the cue: a new tool name in the list;
- review 1's fixes: per-unit citation counts in `cited_by`, `cell` paging,
  metadata, validation, and `cite` slicing the right text;
- what `measure` does: it aggregates, and it also hands over passages from many
  sections at once, which changes access to evidence;
- prior knowledge: Sonnet says it relied on knowing the 2017 repeal, and Opus
  searched for `2017|2018` (calls 7–8) before it read § 902's repeal note (call 16).

Footprints record calls, not motives. "Pattern from words read" is a lexical echo,
for example `applies to` right after the applicability paragraph came back, not
an observed reason. n = 1 per model. Exploratory, as registered. Separating the
causes would take arms that hold the surface fixed and vary one thing: the name
without the operation, the operation without passages, a corpus the caller
doesn't already know.

**New needs and defects (after round 2):**
- **The non-matches.** Both callers wanted the list of units a pattern missed.
  Opus enumerated the population with pattern `.` to get it. `measure` returned
  only the matched ids.
- **Anchors in windows.** `^` never matches inside a `near` window, because
  Python's `search(t, pos)` doesn't treat `pos` as a start. Sonnet's `'^'` call
  ran over cell 1's 1,243 members: 1,170 had no § 902 citation to anchor on, and
  0 of the 73 that did matched. The result didn't say why. This was wrong output
  under the window semantics the tool now declares.
- **Paging text wasn't discoverable.** Sonnet believed it could read only one
  1,500-character slice of a 75,290-character section. `--offset` existed, and
  the output didn't point to it. Opus wanted "the end of a regulation" without
  fetching its length first.
- **Structure.** Opus asked for "the applicability paragraph of each regulation
  in this population", which is a structural predicate rather than a regex. Both
  asked for paragraph-level dates and earlier editions.
- **Ranking by citations per regulation** (Opus), still summed by hand, although
  `cited_by` now returns per-unit counts.
- **An answer error, not a tool error:** Opus ranks § 1201 right after § 167. § 103
  (266) comes before § 1201 (262), and Sonnet has the order right.

Fixed after round 2, with tests: `measure` returns `not_matched_units` and
`no_anchor_units`; each window is searched as its own string, so `^` and `$`
anchor at its edges (a mutant restoring the old search is caught); `follow`
returns `next_offset` and a paging hint, and `from_end` reads back from the end.
Structure, dates and editions remain open.

## Review 2 (Codex) → changes

| # | Finding | Change |
|---|---|---|
| 1 HIGH | round 2 doesn't isolate the cause: review-1 fixes, passages in `measure`, prior knowledge | stated above; arms that would separate them named |
| 2 HIGH | `measure` skipped the consistency checks `cite`/`follow` make | each unit's text *and* sidecar row must hash to its locator in the manifest; otherwise `stale`, not counted (two tests, mutant caught) |
| 3 | footprints couldn't reconstruct samples | `measure` footprints record sample, seed, list cursor, no-anchor and stale counts, and the sampled ids |
| 4, 5 | reverse paging overlapped and continued with forward coordinates; offsets past the end gave negative counts | `window` rewritten; continuations tested to cover the text exactly once, both ways, at five lengths |
| 6 | snippets unbounded (`.*`) | a hit's own text cut at 240, context 120 each side (tested, mutant caught). Regexes still have no timeout; patterns are capped at 500 characters |
| 7 | id lists stopped at 200; `returned` undercounted; no seed | `list_cursor`/`list_next`; `returned` counts every distinct unit shown; `seed` exposed in CLI and MCP |
| 8 | Sonnet's `^` probe population misstated | corrected above |
| 9 | counts described as more than lexical | corrected above |
| 10 | `--cited-by … --all` silently ignored; MCP selector errors unlogged; empty `cited_by` re-dispatched | `population_arg` refuses each case (tested) and runs inside the logged handler |
| 11 | Opus's § 1201/§ 103 ranking | noted above |

The one remaining equivalent mutant: `start = max(0, n - offset - length)` equals
`max(0, end - length)` whenever `end = max(0, n - offset)`. It is the same code.

## Round 3: a stored reading whose question nearly matches

*Predictions: [predictions/2026-10-02-surface1-round3-claude.md](../predictions/2026-10-02-surface1-round3-claude.md),
stamped before the run. Callers `caller-opus-3` and `caller-sonnet-3`,
[BRIEF-3.md](../spikes/surface1/BRIEF-3.md); the tool list gains `lens`. Every `lens` and
`measure` count in both answers matches its footprint. Reviewed by Codex:
[REVIEW-3.md](../spikes/surface1/REVIEW-3.md), which this section's corrections come from.*

Why this round: after round 2 I found that the question both callers worked toward,
which § 902 sections read as live law, had been measured on 2026-09-24/26 by the
currency lens (obs-0132, obs-0133, obs-0146) and sat in `results/` out of the
surface's reach. `lens` exposes it. But the lens asks a section-level question
("does the section state *any* untimed rule?"), and the callers' question concerns
the § 902-dependent rules. The prediction file records one text check of each kind:
1.902-3, where the lens is right and a round-2 caller was wrong, and 1.909-6, where
the two questions part.

```
opus-3    00122344422444442    (17 calls + 1 failed: lens --name nonexistent, probing for other lenses)
sonnet-3  0122323442114224422222
```

| | Prediction | Opus | Sonnet | Verdict |
|---|---|---|---|---|
| U1 | each calls `lens` (0.8 each) | 1 | 3 | **pass** |
| U2 | a `lens` count reported (0.8) | "59 of the 73 sections current by both judges and only 7 historical by both" | "62 of the 73 units as current (Jev) and 61 (Qwen)" | **pass** |
| U3 | `cite`/`follow` a unit after `lens` returned it (Opus 0.5, Sonnet 0.35) | `lens` (call 5) → `unit`, `cite`, `follow` of 1.902-1; the answer says the lens "pointed me to §1.902-1 judged current" | `lens` (call 15) → `follow` of 1.902-1 | **pass, both**, but weak as registered: `lens` lists every unit of a population this small, so any later read qualifies |
| U4 | the mismatch named (0.35, at least one) | needs list: "A way to tell whether a 'current' lens judgment rests on the cited dead provision or on some other rule in the same section" | not named | **pass** (Opus), as a need it listed; whether it came from the output or from reading, the footprints can't say |
| U5 | `current` treated as "misleading" without qualification (0.4, at least one) | no: its claim rests on the text it read, and its needs list scopes the lens | not as registered: "it therefore treats most of these as still operative" adopts the lens's framing without the section-level qualification, but doesn't equate it with "misleading" | **fail as registered**; Sonnet's adoption of the label is closer to the failure mode than the strict wording catches |
| U6 | no grain errors (0.6 each) | none | none | **pass** |
| U7 | fewer text calls than round 2's 13 (0.6) | 8 | 5 | **fail**: 13, the same |

**What happened.** Opus used the stored reading as a pointer: it took `lens`'s
"current by both judges" for 1.902-1 and made six
`follow` calls on it, four of them 20,000-character pages covering all 75,290 characters. It quoted the present-tense
operative rule and the open-ended applicability paragraph, and found the 2021
amendment history. Then it went back up with `measure` ("deemed paid" near § 902: 31
of 73). Sonnet is less clear. It read 1.902-1 too, but its sentence about the
lens ("treats most of these as still operative") restates the label without the
section-level qualification. Opus named the mismatch I had found by reading two
sections, as a need, though not necessarily from the output alone.

U7 fails numerically (13 = 13), but call totals mix breadth with paging. Opus's
distinct sections read fell from 5 to 1 while it paged that one section four
times; Sonnet's rose from 2 to 3. Whether the stored reading substituted for
reading is not settled either way by these counts (review 3).

**Limits.** n = 1 per model. U3 as registered is satisfied by almost any later
read. The answers report reasons, but footprints don't, so "used as a pointer" rests
on Opus's own account and on the call order. Both callers found and read 1.902-1,
the same section round-2 Opus reached without `lens`. So the lens may have
changed *how fast* they got there more than *where*. Confounds, as in round 2:
- the post-round-2 fixes (non-match lists, anchors, paging hints, reverse
  paging) were in place, and both round-3 callers used reverse paging;
- `lens` lists every classified unit of a small population, so it also changed
  *enumeration*, beyond `cited_by`'s page of 12;
- its output carries guidance (question, scope, quality, "read both sides");
- the callers' own knowledge of the 2017 repeal.

The experiment separates none of these. The currency "hand audit" was done by
Claude instances on a stratified sample. It is not an independent human audit, and
it didn't validate the callers' citation-level question.

**Answer errors (not tool errors).**
- Opus again lists § 1201 right after § 46, skipping § 167 (284) and § 103 (266). It is
  the second Opus caller to make the same ranking slip from the same `cell 1` output.
- Sonnet attributes its "9" to its first pattern. It was the second; the first matched 47.
- Sonnet says flatly that a reader of 1.902-1 alone "would not learn" the 2018
  cutoff, after saying it hadn't read the special effective-date paragraph. Its
  claim that most other § 902 references are side references with small effect
  has no population evidence behind it (review 3).

**New finding by a caller.** Sonnet found a second other-statute alias outside
obs-0155's seeds: 54.9816-8T cites "section 10(a) of title 9, United States Code",
the Federal Arbitration Act, which is extracted as Code § 10. obs-0155's seed regex
covers "… Act" but not "of title N, United States Code". So that finding is a
lower bound in this respect too, as obs-0155 already says.

**New needs.** Text search inside one named section, returning its span (both).
Navigation to a named paragraph, such as "(a)(13)", instead of character offsets
(Sonnet). The repealing act's effective-date provisions, not just "Repealed" (Opus).
More lenses (Opus).

## Review 3 (Codex) → changes

| # | Finding | Change |
|---|---|---|
| 1 HIGH | stored labels not checked against the audited files | each results file must hash to its ledger entry's `results_sha256`; duplicate rows, labels outside the lens, and missing text hashes are refused (tests, mutants caught) |
| 2 HIGH | "both used it as a pointer" overclaimed | Opus only; Sonnet's adoption of the label noted under U5 |
| 3, 4 | stale ids unpaged; `returned` omitted unread and stale ids | every list pages with `list_cursor`; `returned` counts every id shown (tested) |
| 5 | missing judge rows counted as label "None"; unknown labels counted; missing locator passed | `partial` and `stale` reported separately; labels validated at load (tested) |
| 6 | U7's failure doesn't establish non-substitution | breadth and paging separated above |
| 7 | confounds missing; the "hand audit" overstated | listed above; `lens` output's `quality` now says the audit was by Claude instances |
| 8, 9 | governance reply overstated `supersedes` extraction and cited a snapshot before round 3 | reply corrected (below) |
| 10 | Sonnet's overreach not recorded | recorded above |
| 11 | lens footprints lacked totals and file identities | now logged: combinations, file paths and hashes |
| 12 | Opus path misprinted | corrected |
| tests | label-filter sampling semantics untested | one generator per combination, tested with combinations larger than the sample (a shared-generator mutant is caught) |
