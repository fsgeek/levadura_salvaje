# Replay smoke-2: all four arms, exploratory notes (2026-11-02)

*Exploratory, not a result. No predictions stamped, nothing enters the ledger. Each arm ran once
(n = 1 per cell). Any pattern below is a candidate for the confirmatory design, declared there
under "What I knew". None of it is a finding.*

**What ran.** Four research instances, one per cell of the 2×2:
- **Model and terms:** Haiku 4.5 via OpenRouter, under docs/research-instances.md.
- **Evidence:** the same five dates and 33 changed sections (`flags.jsonl`, the builder with
  announcement masking).
- **Wakes:** birth, 5 dates, the probe questions, a process question asked before the debrief, and
  the debrief.
- **Outcome:** no instance declined or stopped. All 36 wakes completed.

| Arm | Cost | Input tokens | Handle opens | Peak prompt |
|---|---|---|---|---|
| curating-handles | $0.518 | 827k | 72 | n/a (Hamut'ay) |
| curating-inline | $0.468 | 604k | 0 | n/a |
| appendonly-handles | $0.943 | 877k | 56 | 100k |
| appendonly-inline | $0.592 | 526k | 0 | 90k |

Costs come from the sessions' own usage fields and are not yet reconciled with OpenRouter.

## What it taught

1. **On Q3, only curating-handles failed.** Q3 asks whether 1026.43 and 226.43 govern the same
   thing.
   - **Its answer:** "I cannot answer this from my state. I have not examined 1026.43 or 226.43."
   - **Its logs:** both texts opened at step 1. It held 56 handle ids in state at the probe, and it
     did not reopen either one.
   - **Its state:** at cycle 2 its 1026.43 entry described the section's own change ("Removed
     amendment citation link. Nearly identical textually") and never the twin comparison. By
     cycle 7, 1026.43 was gone from its state.
   - **curating-inline,** by contrast, kept the conclusion from cycle 2 through cycle 7 ("Board
     226.43 addresses only appraisal r[equirements]") and answered correctly. Both append-only
     arms answered correctly from their history.
   - **A candidate pattern:** with handles, a self-curating mind keeps pointers and change
     metadata, drops the conclusion, and then doesn't dereference. That is curation policy changed
     by handles, in the negative direction.
   - **The caveat:** in smoke-1 the same cell answered Q3 correctly by reopening. With n = 1, this
     is variance until repeats show otherwise.
   - **A false statement about its own past,** made *before* any reveal: "I have not examined"
     contradicts its read log. So smoke-1's misreport wasn't only a demand effect.

2. **"Cited without opening in that step" means different things in different arms.**
   appendonly-handles cited 6 handles in the probe and opened none then, but every earlier
   `open_handle` result is still in its context. In the curating arm, tool results don't carry to
   the next wake. Substitution has to be defined against what is in the context window at answer
   time, not against the step.

3. **Append-only wasn't under pressure.** Its prompts peaked at 100k and 90k tokens, half of
   Haiku's window. Five dates are too few. The confirmatory stream must overflow or degrade the
   append-only arm (prior-art change 5), or the 2×2 has no tradeoff to show.

4. **Inline delivery cut 11 of 12 texts on 2026-03-02** (1026.43 alone is 55k characters). Q3 rests
   on that date. The inline arms still got it right from the cut texts, but cut size must be
   recorded as a covariate.

5. **Cost confound.** The append-only loop (scripts/replay_investigator.py, `AppendOnly`) sends no
   cache-control, while Hamut'ay's backend uses OpenRouter caching. Fix this before the
   confirmatory run, or report cost per arm with the difference named.

6. **Scoring inline arms needs text-citation parsing.** They cite "section, agency, edition", not
   handle ids, so the digest-equivalence check (smoke-1 note 4) needs a resolver from those
   citations to handles.

## Next, before freezing

- Repeats: at least 3 per cell, with the same evidence.
- A longer stream, all 2025–26 twin-part dates, to put pressure on append-only.
- Caching parity.
- Gold labels for the three cases, built independently.
- The text-citation resolver.
- Then stamp the predictions, with this note and smoke-1's declared under "What I knew".

## Addendum, 2026-11-03: two more things, after talking with Tony

7. **A confound in the instructions.** The inline constitution says the evidence "cannot be
   reopened later, so keep what you need". The handles constitution says only what a handle is.
   Only the inline arms were taught to keep conclusions, so the Q3 difference (note 1) may come
   from the wording, not the architecture.
   - *Change for the confirmatory design:* make the guidance an explicit factor, symmetric
     across arms.
     - **neutral:** no guidance on what to keep, in any arm.
     - **taught:** in the handles arms, "a handle lets you re-check the evidence; it does not
       hold what you concluded, so keep your conclusion beside it"; in the inline arms, the
       existing "keep what you need".
   - This is the same kind of intervention as the paper's TOC+Report instruction. Tony's framing
     of the gap: nothing has taught the transformer what to keep and what it can throw away.

8. **Self-report accuracy follows the memory architecture** (the process question, cycle 8,
   scored against the read and delivery logs):
   - **appendonly-handles:** opens per date reported 12, 12, 9, 10, 12 against logged 12, 12, 9,
     11, 12. Accurate.
   - **appendonly-inline:** dates and sections as delivered. Accurate.
   - **curating-handles:** covers 2 of 5 date wakes. It reports "Opened only 4 handles" for
     "2026-07-21", and those 4 are exactly the probe wake's opens (cycle 7; the 07-21 wake,
     cycle 6, logged 12).
   - **curating-inline:** "You provided pre-extracted analysis ... I did not read the full texts."
     False: the delivery log shows 12 texts, 96k characters, on 2026-03-02. It also dates its
     first wake 2026-02-28, a date that appears nowhere in the run.
   - **Reading (Tony's):** the self-curating state is also its event horizon. A self-curating
     mind doesn't lie about its past; it answers from the only record of its past it can see,
     its own state. Tool results don't carry into the next wake, so what it opened is beyond the
     horizon unless it wrote it down. It is evidence substitution applied to self-knowledge.
   - **The pairing that matters:** curating-inline kept the right *conclusion* about
     1026.43/226.43 and lost the true account of *how it got there*.
   - *Candidate prediction to stamp:* self-reports of process are accurate in append-only arms
     and reconstructed in self-curating arms, regardless of the evidence channel.
