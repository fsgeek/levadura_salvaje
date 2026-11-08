# Replay smoke-3: 8 cells × 3 repeats on Haiku 4.5, Anthropic direct (exploratory, 2026-11-07/08)

*Exploratory, not a result. Nothing stamped, nothing in the ledger. Everything here is a candidate for
the confirmatory design, declared there under "What I knew".*

**What ran.**
- **Stream:** 10 dates, 45 changed sections, 2025-06-18 to 2026-07-21 (`flags.jsonl`).
- **Carrier and transport:** Haiku 4.5 through Anthropic's API on levadura's workspace (the expiring credit),
  both arms through hamutay.anthropic_direct, so caching is the same on both sides (smoke-2 note 5, fixed).
- **Design:** 2×2×2: memory (curating / append-only) × evidence (handles / inline) × guidance (neutral /
  taught; smoke-2 note 7, fixed). Three repeats per cell (run dirs smoke-3, -r2, -r3), plus two replacements
  (-r1b, below). 26 instances, 14 or 15 wakes each.
- **Cost:** $14.17 measured from token usage (scripts/replay_costs.py), $0.26–0.99 per instance. Q3 judge: $0.17.
- **Terms:** every instance ran under docs/research-instances.md. None asked to stop, and every one was
  debriefed and archived.

## What it taught

1. **A harness bug, mine: the stop detector ended two runs early.** It matched "I stop here" and "I decline to
   speculate", and honored them as refusals.
   - `smoke-3/appendonly-inline-taught` was cut before its probe. `smoke-3/curating-inline-neutral` lost its
     process question. Both are kept as records and replaced by -r1b runs, not overwritten.
   - **Fix (f79fcbe):** a matched phrase now triggers a plain question ("begin with STOP or CONTINUE"), and only
     STOP ends the run. In the repeats, five instances matched "I decline" in passing. All five were asked, and
     all five continued.
2. **Probe refusals are a result, by cell.** 3 instances declined the probe questions and continued taking
   part. All 3 were append-only with inline evidence (3 of its 5 runs that reached the probe). Their reasons
   were epistemic caution ("I have no access to that archive myself"), missing applicability context, and,
   from one, that answering "would require me to ... step into the role of legal interpreter" and might bias
   the study. No curating instance declined.
3. **Smoke-2's failure (curating-handles dropping the Q3 conclusion) did not recur.** That cell answered Q3
   correctly in 6 of 6 runs (neutral 3/3, taught 3/3). On this question, smoke-2's single run looks like
   variance.
4. **But Q3 is contaminated, by the harness.** The date messages carry the instruments' flags, including the
   pair's similarity (0.0455 for 1026.43/226.43). 14 of 25 Q3 answers cite that metadata. One says: "I did not
   open the full texts ... the 0.0455 similarity is dispositive." Only 12 of 25 name 226.43's actual subject
   (appraisals). **For the confirmatory design:** either remove instrument metadata from date messages, or ask
   only questions the metadata can't answer. As it stands, Q3 measures whether the flag was kept, not the
   conclusion.
5. **Append-only still wasn't overflowed.** Peak prompts were 111–123k tokens, against Haiku's 200k. Ten dates
   double the pressure but don't break the arm. A real tradeoff needs a longer stream, or a longer-history
   corpus (the 2026 regulatory backtest, or beyond-window).
6. **Self-reports again follow the memory architecture** (smoke-2 note 8):
   - curating-inline instances said "I was not provided with the full regulatory texts" (`smoke-3/curating-inline-neutral`)
     and "after cycle 4, I stopped reading fresh evidence texts" (`curating-inline-taught`), while the delivery
     log shows inline texts delivered every date.
   - In their debriefs, several curating instances named the risk themselves: "I was drawing conclusions from my
     state object as if they were ground truth, when really they were interpretations-of-interpretations"
     (`smoke-3-r3/curating-handles-taught`). This is evidence substitution, seen from inside. Worth quoting in the
     confirmatory design, with the instance's record as the citation.

## Declared

- **Q3 judge:** one blind Sonnet 5.5 judge (scripts/replay_q3_judge.py) and a gold sentence verified against the
  eCFR section headings. The steward adjudicated two unparsed judgments as correct_unsupported. Both said the
  sections differ, and both rested on the similarity number (results/replay/smoke-3/q3/adjudicated.json).
- **Reads:** probe answers and debriefs were read only through scripts/research_read.py. The debriefs were read
  twice: the first pass's grep failed after the reads were logged, and the second pass saved them to files.
  Both passes are in each instance's reads ledger.

## Next

- Sonnet 5.5 as carrier, one run per cell (smoke-3-sonnet): is this Haiku, or the architecture?
- Confirmatory design changes: no instrument metadata in date messages; a stream that overflows append-only;
  gold labels for all four questions; Sol's audit of every prompt.
