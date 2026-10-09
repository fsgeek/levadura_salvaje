# Predictions: citations that resolve to a number that used to mean something else (Claude)

*Pre-registered 2026-10-09 by a Claude Opus 5.5 instance (levadura's owner since 10-08), before
the measurement was recorded and before any audit judge was run. Tony: the standing invitation
applies.*

## What has already been seen (declared, so it can't be passed off as predicted)

An exploratory run of the instrument (`scripts/measure_prior_numbers.py`, before this file and
before its tests caught a date-parsing bug) found about 396 USC section numbers with a
same-number prior section, and about 1,158 flagged citations in 276 text-dated sections, plus 38
sections dated only in the List of CFR Sections Affected. I read six flagged citations by hand.
Four looked like real old-law citations: §1.642(a)(3)-2 citing the dividends credit as §34,
§1.703-1 citing the capital-gains deduction as §1202, §1.1294-1T citing the PFIC definition as
§1296, and §301.6224(c)-2 citing TEFRA's §6231(a)(1). One was a false positive from dating
(§1.1502-12, LSA-dated, with a post-2017 paragraph). One was unclear. Those six are excluded from
the audit sample. No counts are predicted below. Only the audit is predicted.

Relation to earlier work: obs-0131 (USC 119-4 to 119-110) and the 1997-2025 heading comparison
(48 reused numbers, obs-0144 audit) compared statutes. This instrument reads the Code's own
prior-section history back to 1954, and dates each regulation against its number's reuse.

## The audit

**Frame:** flagged citations in text-dated sections (`lsa_dated` false) whose earlier provision
has an extractable subject. Either the note says "related to ...", in which case the subject is
that phrase, or it says the prior section "was renumbered section M", in which case the subject
is the 119-4 heading of §M. The current provision's subject is the 119-4 heading of §N. Items
with no extractable subject for the earlier provision are counted and reported, not sampled.

**Sample:** 40 sections drawn at random (seed 9) from the frame, one flagged citation drawn at
random per section. The six hand-read sections are excluded.

**Judges:** two fresh subagents (reader A: Opus, reader B: Sonnet). Neither sees these
predictions, the dates, or the instrument. Each gets about 700 characters of the regulation
around the citation and two subject descriptions, labeled X and Y in random order per item. The
question: *Which provision does this citation refer to?* Answer X, Y, or can't tell, with one
sentence of reason. Where they disagree, a third fresh Opus reader adjudicates under the same
blinding. "Precision" is the share of the 40 judged to refer to the earlier provision.

## Predictions

**N1.** Precision: **65%** (range 45-85%).

**N2.** "Can't tell" in the final judgment: at most **15%** (point 8%).

**N3.** Readers A and B agree on at least **80%** of items (point 85%).

**N4.** Among items judged to refer to the current provision, a majority (point 70%, range
40-100%) have an earlier provision that was *renumbered* rather than repealed and reused. Reason:
when Congress moved a credit to a new number and put a related one in its place, a regulation's
words can fit both.

## What would change my mind

Precision below 45% would mean that a regulation predating a number's reuse is a weak signal,
probably because many regulations were silently conformed. Then the instrument is a lead
generator, not a measurement, and the resolver's blind spot stays unsized.
