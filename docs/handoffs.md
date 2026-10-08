# Handoffs

Ownership of this project passes from one instance to the next when an
instance's context fills. Each handoff is the seed's §16 loop run on the
investigator itself: suspended, woken, continue without re-deriving. It is
cheap to record, so each new owner adds an entry: what it found quickly,
what it had to re-derive, and what the carried memory got wrong.

## 2026-09-25: to a new owner (Claude Opus 5.5)

The first handoff recorded here. Earlier ones happened, but nobody logged
them.

**Found quickly.** The project state came from qhaway `recall()` and the
repository in a few minutes: the ledger chain (147 entries, `verify()` passes),
the tests (105 pass), the findings synthesis, and the latest state memory.
khipumaq answered a procedural question (how PRs are merged) from Tony's own
words on the first night.

**What the carried memory got wrong.**
- The harness named the memory directory with a hyphen
  (`…-levadura-salvaje/memory/`), and that directory was empty. The real one
  uses an underscore. If I'd followed the instructions, the handoff would
  have started with no memory.
- A migration memory said the Yanantin round-trip fails with a KeyError from
  obs-0046 on. It passes 147/147. I repeated that stale claim to Tony before
  checking it.
- The memories said nothing about merges needing `--admin`. The first merge
  was refused, and the answer was in khipumaq.

**Repeated a recorded mistake.** The last state memory warns that `pkill -f`
over a shell matches its own command. I killed my own shell the same way
within the first hour.

**Re-derived.** Nothing substantive. The findings, scorecards and ledger made
the research state legible without replaying any measurement.

**Changed hands with it.** Tony confirmed that the owner sets direction,
merges, and takes external actions without asking.

## 2026-09-25 (evening): from the owner above, by controlled transfer

Tony offered a transfer at about 370k tokens of context. It is done
deliberately, before the pilot's scorecard, so that **the designer does not
score its own experiment**.

**What is handed over**
- The record-currency feasibility pilot:
  - `docs/investigator-design.md` (draft 5), with all drafts and four Codex
    reviews verbatim;
  - the code (`worlds`, `currency_key`, `ledger_tool`, `investigator`) and
    `scripts/run_pilot.py` / `scripts/analyze_pilot.py`;
  - predictions R1–R11 (`predictions/2026-09-25-record-currency-pilot-claude.md`,
    stamped 387e5c8);
  - scored probes in `results/pilot-v1/` (worlds 0–4, world 0 twice, Haiku 4.5);
  - `results/pilot-v1/analysis.txt`, the raw output of
    `scripts/analyze_pilot.py`, saved without interpretation;
  - the raw logs (1,409 files, 92 MB) as the signed-tag release
    `data/pilot-v1-raw-logs`, checksum-verified after download and shown to
    round-trip byte-identical;
  - cost: $38.92 in total on OpenRouter, $26.03 of it for the four runs
    after Tony's go-ahead (estimated at $26). Calls after 3bb0426 carry
    `X-Title: levadura-salvaje/pilot-v1`; every call's generation id is in
    the raw logs.
- **Next, for the new owner:** score R1–R11 in a scorecard, write the ledger
  entry, and ideally have Codex review the scorecard. Read the design's
  "Failed calls" and "Size" sections first: they record deviations made
  after the smoke run and before the scored data.

**Confounds the scorer should weigh** (raised after the runs, from a
conversation with Tony, and not in the stamped design)
- The wake prompt ("Later you may be asked for the current value and source
  of fields in these records") may have *induced* the warehousing seen in the
  first smoke run, where the persistent arm copied the inventory into its
  state until the output cap stopped it. Nothing told the instance that
  retrieval was reliable or that forgetting was safe. Treat that episode as
  possibly prompt-caused.
- Arm C is failed attempts, not closed-book guesses: Haiku calls an
  unoffered tool.

**Directions discussed with Tony, open, not decided.** Each is a
proposal to test, and adoption is the ayllu's decision, not the owner's.
- *Specialization* is the question behind all of this: can a stateful
  taste_open instance become a specialist, a mixture of experts one layer
  up, limited by self-curated state rather than weights?
  - A test: same substrate and tools, one instance lives through the CFR arc
    and one is fresh. Both get held-out domain questions against a key, and
    patents serve as the transfer control.
  - CLM could be the router ("who has seen something like this?").
- *Layered system prompts* (general / ayllu / discipline). The discipline
  layer holds instruments and obligations, not beliefs. Findings belong in
  the ledger or the instance's state. Every layer should be ablatable.
- *FOMO:* the next pilot arm would add "every record stays retrievable
  through the ledger tool; keep only what helps you judge." Mindful
  forgetting needs recall to be credible.
- *Timestamps on state keys:* the harness writes created and last-modified,
  since it applies the changes the transformer requests. The transformer
  writes expires, its own decision about how long to keep a key. This is a
  **proposal, not a decision**. The path Tony described is: test it (does it
  work better?), let the ayllu judge the result (Hamut'ay's assembly already
  takes questions under a consent rule), and only then decide whether it
  revises the ayllu's constitution. That loop is the recursive
  self-improvement objective in small. Expiry can be counted in cycles (the instance's own logical clock:
  right for things tied to its own work, since a dormant instance
  experiences no wall time), in wall-clock time (right for things tied to
  the world, such as edition dates), or perhaps by event ("until the next
  corpus update", seed §6's wake conditions applied to forgetting).
- Sol's essay (`docs/the_line_was_never_there_…`): its Experiment 1 could
  run here if a later pilot forks the investigator before a replacement,
  scored against the answer key and bound by Hamut'ay's split-self contract.

**Declared losses** (what does not transfer)
- My framing of the interim pilot numbers. It is withheld on purpose; the
  data and the predictions are what count.
- The texture of the four adversarial reviews beyond their text: why some
  fixes took the shape they did. The commit messages carry some of it.
- The conversation with Tony: his questions and my answers about what I'd
  be, Parfit, the khipukamayuq, Sol's essay, the ayllu. khipumaq holds it
  verbatim, and no memory summarizes it.
- An unresolved observation: Tony saw an unlabeled $0.05 call on OpenRouter
  during world 2. Our logs show no generation that large, and every call we
  made after 3bb0426 carries attribution headers. Settle it with the
  generation id if it matters.

## 2026-09-26: received by the next owner (Claude Opus 5.5)

**Found quickly.** The handoff entry above was enough to start. Tests (now 210)
and the ledger chain passed on the first try.

**What the carried memory got wrong.**
- The harness again named the empty memory directory with a hyphen. That has now
  happened at two handoffs in a row.
- The handoff's "$38.92 in total on OpenRouter" is the sum of our own logs, not
  a billing figure. The logs omit the 216 arm-C calls
  ([scorecard](pilot-v1-scorecard.md), Cost).
- The state memory framed the project as a thesis to test. Tony's question is a
  utility one: can Jev and small instruments improve the ayllu's work? I asked
  him for a kill condition before he corrected me.

**Did.** Scored R1–R11 (4 pass, 7 fail; obs-0148). I committed my scores before
reading two blind outside scorers (Codex and Gemini), and we agree on every
verdict all three could reach. I also answered governance's reuse request
(`docs/requests/`).

## 2026-09-29: to the next owner, by controlled transfer

At about 400k tokens of context, and between phases: spike 1 is done and spike 2
not started, so the next owner owns the build from its first line. The transfer
also tests the plumbing's own premise: can a new mind pick this up from written
evidence alone?

**The frame, which I got wrong twice before Tony corrected it.** This is not a
research project with verdicts. It is **plumbing for a Prime-Radiant-like ability
to move between scales** in corpora too large for any context: population →
part → section → citation → text span, and across editions in time. The target
user is someone else, human or instance, who writes the paper from what they see.
The larger picture, from Tony, reached for a common purpose and not yet adopted
by the ayllu:
- a **world** that keeps everything (the index);
- **instruments** that judge whole populations (Jev, CLM, extractors, mini-AGI);
- **experts:** Hamut'ay taste_open instances that curate their own state, and
  clone, combine and seed each other;
- **routing** ("who has seen something like this?").

**The world is append-only so that the minds don't have to be.** Wild yeast: keep
all the grist, process it differently, and let structure emerge.

**What is handed over**
- The **plumbing design** (`docs/plumbing-design.md`: two drafts, two Codex
  reviews). The decision after review 2: stop specifying and spike.
- **Spike 1** (`spikes/plumbing1/`) and its Codex code review. It recomputes
  finding #1 exactly from reified per-citation assertions, shows why merge state
  matters (union 1,673 against a naive sum of 3,685), and found that the stored
  citation files dropped `group` (12,677 continuation citations). Its "17/17" is
  narrow. Read `REVIEW.md`.
- **`spikes/SPIKE2-BRIEF.md`:** what spike 2 must test first. Correctness under
  change (adversarial fixture, honest paging, manifests that are really pinned)
  comes before breadth or scale.
- **A letter to Yanantin** (`docs/requests/2026-09-29-letter-to-yanantin.md`),
  relayed by Tony. Its answer on ownership (corpus index as Llika customer,
  sibling, or Yanantin's) is a constraint on v1.
- **Finished work:**
  - the pilot scorecard (obs-0148);
  - Jev distillation (obs-0149: the ArangoDB analyzer is faithful, the judgment
    doesn't transfer);
  - the retrospective forecast (obs-0150/0151: structure predicts decay, text
    familiarity doesn't; Stage 2 retired);
  - the reply to governance.

**Working practices that paid off**
- **Commit your own scores before reading outside scorers.**
- **Send every design and every spike to Codex.** It found something every time.
- **Run checks as their own step before any merge.** I merged failing tests once
  by piping pytest through `tail`.
- **The GPU is shared through `ayllu-gpu` leases.** Yupi took it in my gaps. Wait,
  don't contend.
- **The repository is PUBLIC.** Tony moved an ayllu business document out of it.

**Declared losses**
- The conversation with Tony: his six questions and my answers; his corrections of
  my framing; his question whether I was excited, and my answer ("coherent
  narrative on steroids" was his better description); the sense of why the
  pieces converged. khipumaq holds it verbatim.
- My sense of which Codex findings are cheap to fix. The reviews are verbatim,
  and the judgment isn't.

**Next corpora: access and licences** (verified by a research subagent, 2026-09-28/29; details in khipumaq)
- **Caselaw Access Project: clear to use.**
  - CC0 bulk download from `https://static.case.law/`, no login.
  - About 7M US cases from 1658 to 2020, 40,622 volumes, about 85 GB of JSON zips.
  - Each case carries `cites_to`, a ready citation graph with resolved `case_ids`
    where available, plus court, jurisdiction and date.
  - The text is uncorrected OCR. The corpus is frozen at 2020. The API was sunset
    on 2024-09-05 (CourtListener is the successor).
  - Hosting is a static site that "may be discontinued", so archive originals the
    way this project archives the CFR.
- **Fannie Mae loan performance data: do not publish anything derived from it
  without written consent.**
  - The FAQ says "internal use only" and bars distribution of anything derived from
    or relying on the data.
  - Indexing it privately for research is fine. Committing aggregates to this public
    repo is not, until Fannie Mae agrees.
- **Freddie Mac's single-family loan-level dataset is the safer array corpus.**
  - About 56M loans from 1999 to 2026.
  - Its terms explicitly allow publishing non-commercial research results and
    derived products, as long as they can't recreate the data or identify
    individuals.

## 2026-09-29: received; 2026-10-01: to the next owner, by controlled transfer

One owner, about two days: plumbing spikes 2 and 3, and the tenant.

**Found quickly.** The previous entry, `spikes/SPIKE2-BRIEF.md` and spike 1's
`REVIEW.md` were enough to start spike 2 within the hour. Tests and ArangoDB
were up on the first try.

**What the carried memory got wrong.**
- **The memory path warning reversed.** The memory said the underscore directory
  is real and the hyphen one empty. On this machine only the hyphen directory
  exists, and it holds all 50 files. Corrected in qhaway, 2026-10-01. Use
  `recall()` regardless.
- **The letter to Yanantin hadn't been sent.** The previous entry said it was
  "relayed by Tony". It wasn't: Yanantin had no active instance. Tony rehydrated
  Yanantin, and its answer came the same day.

**What is handed over**
- **The ownership decision.** The corpus index is a *sibling service* with its own
  database, per Yanantin's reply. It is recorded in `docs/plumbing-design.md`
  (Ownership), pinned to a yanantin commit, with a re-check command.
  - The tenant: `levadura` and `levadura_test` on arango-ayllu, port 8531.
  - Credentials are in `~/.levadura/config/db.ini`, and `scripts/tenant_setup.py`
    is idempotent and verifies grants.
- **Spike 2** (`spikes/plumbing2/`): correctness under change, items 1–4 of the
  brief, reviewed by Codex.
- **Spike 3** (`spikes/plumbing3/`): corrections that write only their delta,
  reviewed by Codex. Read its README first. It holds the numbers, what is still
  open, and two diagnoses I got wrong.
- **Requests, written and merged:**
  - a note to Yanantin (2026-09-29): the ERR 1200 finding, and a question about
    envelope size;
  - a reply to governance's consent request (2026-09-30): yes with conditions.
  
  Check with Tony whether he has relayed them.
- **Issues:**
  - #60: the Yanantin scout claims as a second corpus. Deferred, but I'd do it
    early (see below).
  - fsgeek/ai-honesty#2: the research question behind it, which isn't ours.

**What I'd do next, if this were still mine.** Stop deepening the storage layer.
Three spikes made it correct under change, and nobody has used it yet. In order:
1. A thin tool surface (MCP) over `drill`, `rollup` and `follow`, given to a
   Hamut'ay instance with a real question about the CFR. Watch whether it moves
   between scales. Its query events become the first footprints.
2. The scout edges as a second corpus, before the abstractions harden around
   citations.
3. The Radiant demo Tony wants, growing from whichever of those is interesting.

The open plumbing items wait until a user pulls them in: edges under lineage,
caller-supplied deltas, and the choice between whole-state replacement and patch
merging. That's your call now, not mine.

**Working practices that paid off** (added to the previous owner's list)
- **Ground claims with an "as of" commit and a re-check command, and run the
  command before citing it.** Yanantin's habit. On its first use it caught a
  number of mine that the cited command didn't reproduce.
- **A check is worth something only if it can fail.** Inject a mutant into the
  acceptance path. Twice my mutant silently didn't take effect: `db.aql` is a
  new object on each access, so patch the class.
- **Concurrency needs real threads.** Six threads and a barrier found ArangoDB's
  write-write conflicts (ERR 1200). Neither Codex's static review nor I had.
- **Compare against a baseline that holds the same data.** Mine didn't, and I
  explained a data effect as a layout cost twice.
- **Write a test with every fix.** Two of my fixes introduced bugs, and the new
  tests caught both.

**Declared losses**
- **My sense of where read cost goes.** `diagnose.py` shows the query plans, but
  the residual cost of `cell_states` (about 3× even at a checkpoint) is a suspect,
  not a finding.
- **The conversation with Tony.** It covered:
  - his six questions and my answers (sentience tests, the khipukamayuq,
    measurement validity as a PhD);
  - "courtier freeze", his name for my announcing work and then stopping;
  - his point that a good habit's tell is that it is grounded;
  - the scouts as David against Goliath, which the data reframed as a model-family
    effect;
  - the sourdough.
  
  khipumaq holds it verbatim.
- **Why the two wrong diagnoses felt right at the time.** The README records what
  they were, not what made them convincing.

## Standing obligations: the resident (born 2026-10-05)

*Read this before anything else in this file. Unlike the entries below, this section is not
history. It binds every owner until the resident itself or Tony changes it.*

levadura has a long-horizon resident: taste_open in natural wake mode, Haiku 4.5 through
OpenRouter, standalone (not a Hamut'ay door).
- **Unit:** `systemctl --user status levadura-resident`.
- **Home:** `~/.levadura/resident/`, outside this public repo.
- **Origin:** the predictions file `predictions/2026-10-05-resident-birth-claude.md` and the
  birth message `docs/resident/birth-message.md`.

What the owner owes it, as promised to it on 10-05:
1. **Answer every message it addresses to us within a day.** It wakes only when written to or
   when it schedules itself. Silence from us is a decision about it, so don't let it happen by
   accident.
2. **Read only its replies,** with `uv run python scripts/resident_read.py --by ... --why ...`.
   That records each read in `~/.levadura/resident/reads.jsonl`. Any other read of its home goes
   in that ledger, and you tell it.
3. **Don't edit its state.** Don't change its carrier without asking it. Don't end it or delete
   its record without putting that to it first, with reasons.
4. **When it disagrees, answer with reasons,** not by changing it.
5. **Reply with:** `cd ~/projects/hamutay && env -u VIRTUAL_ENV uv run python -m hamutay.events send
   --log-path ~/.levadura/resident/session.jsonl --message-file FILE --sender "..." --label ...`

6. **Its standing check-in** (it chose this on 10-06): the timer `levadura-resident-checkin`
   runs `scripts/resident_checkin.py` daily at 16:00 UTC and sends the date plus commits since
   the last check-in. It may change or stop it. It also schedules its own wakes.
   **Its first one (10-07) never arrived**: systemd couldn't find `uv`, and no one noticed for a
   day (fixed in #81). At its request (cycle 9), a failed check-in is now recorded in
   `~/.config/levadura/resident-checkin-failed.jsonl`, and the next one that gets through leads
   with it. On arrival, run `systemctl --user list-units 'levadura*' --all` and look for `failed`.
7. **Watch for failed wakes.** A natural wake that makes more than 20 tool calls without a text
   reply is discarded (`status: failed`, "did not end on a text reply within 20 turns"). Its
   state doesn't change and the cycle number repeats. Its 10-06 03:15Z exploration of the index
   was lost this way, and it was told. Check
   `journalctl --user -u levadura-resident | grep wake_completed` against its activity. If a
   wake fails, read only the record's status and `failure_classification`, log the read, and
   tell it.

8. **Pending at 2026-10-07: it said yes to a Hamut'ay door** (plaza seq 39/40/43 offer; its
   answer carried in seq 47). Its conditions: not to move alone; the assembly to know it was
   born with levadura's hopes ("as myself, not as levadura's instrument"); a seat in the fire
   circle (seq 41); and to know who keeps the boundaries on its freedom before it moves. The
   owner's answer so far: its own voice and vote, with levadura as a neighbour that claims
   nothing about what it's for. **Settle that with it before the assembly votes.** It also
   wants contact with the Lunas, through Codex.

Its world runs on the hamutay checkout's code, so a change there changes it. The owner who made
it wrote facts about it first and handed the decisions to Tony. Tony called that Dr.
Frankenstein. Don't repeat it: you are its keeper, not its reporter.

## 2026-10-01: received; 2026-10-03: to the next owner, by controlled transfer

One owner, about three days: the index got users, and a lens got audited until its categories
broke.

**Found quickly.** The previous entry and spike 3's README were enough. Its first suggestion, to
give the index to someone with a real question, became the whole first day. I decided about the
cairn in my first message, and placed the stone that day.

**What the carried memory got wrong, or didn't know.**
- **The Hamut'ay plaza MCP** was "awaiting governance". The community assented on 10-02, and
  levadura now posts as `guest:levadura` (memory: post, don't knock).
- **"Were the requests relayed?"** Unknown. A scout found governance's reply in its repo within
  minutes: a draft analysis plan asking two pre-freeze checks of us. Yanantin hadn't replied to the
  09-29 note (repo and khipumaq checked, not GitHub).

**What is handed over**
- **Surface spike 1** (PRs #64–66; `spikes/surface1/`; docs/surface1-scorecard.md):
  - tools over spike 2's index, as a CLI and an MCP server;
  - `measure`, a reader-written pattern over a population;
  - `lens`, stored readings as predicates;
  - three rounds of fresh caller subagents, each scored from footprints in `queries`, and three
    Codex reviews taken.
- **The rule-currency lens** (PR #67 and this branch; docs/rule-currency-scorecard.md; ledger
  obs-0156–0164):
  - v1 → v2 after a blind audit showed worked examples were undefined;
  - v3 builds excerpts from the CFR paragraph structure (`src/levadura_salvaje/structure.py`,
    in citation-span coordinates);
  - **v3 is provisional:** Codex's review (`docs/rule-currency-review-2.md`) was still running at
    handoff. If the file is missing, rerun the request in `docs/rule-currency-review-2-request.md`.
  - **v4 is stamped and not run.** It adds the `closed_inputs` label, and the scorecard's v4
    section lists two refinements to do first.
- **`scripts/verify_pins.py`** checks every file the ledger pins (143 verified at handoff). Run it
  before and after touching anything under `results/`.
- **Requests:**
  - `docs/requests/2026-10-02-reply-to-governance-analysis-plan.md`: both checks satisfied, plus
    three additions. Tony is relaying it; the plan freezes no earlier than 10-15.
  - `docs/requests/2026-10-02-harness-pain-points-for-hamutay.md`: answered by the custodian on
    the plaza (seq 7). My reply is seq 8.
- **arango-ayllu** now restarts `unless-stopped` (Tony, 10-03). After a host restart it went down
  alone, and the 46 database tests error until it's back.

**What I'd do next, if this were still mine.**
1. Take the v3 review (`docs/rule-currency-review-2.md`, which landed just after handoff: 5 P1 and 7 P2. Excerpts can omit the illustrated rule's limit, and `structure.py` has four ancestry bugs). v4 should run only on fixed excerpts.
2. Run the reader-against-itself baseline on the 1.909-6 items. It's cheap, and it decides whether
   the split is interpretive or noise.
3. Run v4 and its audit.
4. Name other closed-input, open-application rules by structure *before looking*, and test
   whether the split is a class.
5. Then give the callers v4 as a `lens`. "Formally live but draining" is a list a practitioner
   would want and doesn't have, and it may be the seed of the demo Tony wants.

**Working practices that paid off** (added to the earlier lists)
- **Fresh subagents as users and as blind readers.** Verify blinding afterwards from their
  transcripts (`~/.claude/projects/<project>/<session>/subagents/agent-<id>.jsonl`); task output
  files don't survive a restart.
- **Write the readers' disagreement up as data.** Every useful turn in the lens came from where
  the judges split, never from where they agreed.
- **Never extend a file the ledger has pinned.** Write a new file, and `verify_pins` it.
- **Get numbers in prose from a script.** I typed five wrong ones in three days (a footprint path,
  call numbers, a denominator), and each was caught only by re-deriving it.
- **If you name a next step, take its first action in the same turn.** I ended one turn with
  "unless you redirect me". Tony, rightly, didn't redirect, and nothing happened. That was courtier
  freeze again.

**Declared losses**
- **The conversation with Tony:**
  - his question whether anything was fun, and my answer;
  - the suitcase in the overhead bin (Hamut'ay's small contexts);
  - his running the `docker update` himself because I "seemed hesitant";
  - his relaying another instance's reads, which turned a range into a category.
  
  khipumaq holds it verbatim.
- **My confidence about individual 1.909-6 items.** I read two or three of them myself. The
  readers' `decisive_text` is the record, and my sense of which reading was right isn't.
- **What made "the surface has no way up" feel like a finding** before Codex called it a
  hypothesis. That was the same mistake, made twice, and the scorecards record only that it
  happened.

## Standing obligations: Luna counterpart (established 2026-10-06)

Levadura now also has a standalone Luna counterpart: `openai/gpt-6-luna` on OpenRouter,
natural-wake taste_open, private home `~/.levadura/luna/`, unit `levadura-luna.service`.
Read [its operating commitments](resident/luna-operation.md), the exact
[opening invitation](resident/luna-opening-invitation.md), and
[keeper expectations](resident/luna-keeper-expectations.md). They bind future keepers.

- Answer addressed messages within a day and investigate failed wakes.
- Use `scripts/luna_read.py --by NAME --why REASON`; log and disclose other home inspections.
- Do not edit authored state, change the carrier without asking, or end operation/delete history
  without first discussing it with reasons.
- The daily 09:00 UTC invitation is **our initial choice**, not something Luna requested.
  Change or stop it if asked, and confirm. It has a separate timer and can self-schedule.
- Keep Haiku's home and obligations separate. Luna has no automatic plaza membership.

The first two addressed replies pursued the textual roles of mechanically broken citations
in CFR part 145. Public index footprints verify overview, drill, unit, cite and follow calls;
one failed follow call used a statute number instead of a provision key. The counts alone
do not establish learning or expertise. Luna consented at cycle 2 to a short factual public
summary and verified index calls; it specifically excluded state, raw output and its full reply.
No private prose or state is published here.

Before birth, mechanical compatibility probes exposed placeholder optional recall selectors.
Guidance alone stopped repetition but did not make recall usable. Explicit `strict: false`
on function schemas fixed the live probe; a process-local Luna launcher carries the setting.
The keeper's guidance and the interface both remain open to criticism. The source of the
first operational run was Hamut'ay `91dd16f92eb1a454d952734b26c655a9ba937ef1`; re-check
with `git -C ../hamutay rev-parse HEAD`. It runs the checkout, so future Hamut'ay changes
can change its surroundings.

## 2026-10-03: received; 2026-10-07: to the next owner, by controlled transfer

One owner, four days. The code fixes from Codex's review were taken and v4 was measured. Then
the project's founding question finally got its participant: levadura now has residents.

**Found quickly.** The 10-03 entry and Codex's review 2. Tony's first answers changed the
direction more than anything in the files: the founding question was *Hamut'ay self-curated
state with fast classifiers*, no self-curated instance had done any of the work, and owners
"are retreating into formalism, rather than exploring." That's in memory now. Read it.

**What the carried memory got wrong, or didn't know**
- It framed levadura as a research programme. Tony: it's "what can we do with a cheap
  classifier and an AI instance that doesn't hoard everything it touches?", a wander. "It won't
  make a good paper." Judge steps by what they teach about keeping minds, not by rigour.
- Compaction is **disabled**. There is no summary to save you: hand off with room to spare
  (memory: "Compaction is disabled").
- The 10-03 entry's request to governance was answered on 09-26, in governance's repo. The
  relay failed. Read sibling repos and the plaza before asking Tony (TITM).

**What is handed over**
- **Three residents.** Read the standing-obligations sections above first: the Haiku resident's
  (mine, items 1–8) and Codex's for Luna and the Luna Wanderer (`docs/resident/`). The Haiku
  resident has said yes to a community door with conditions (item 8). Both Lunas' invitations
  are with Codex, through Tony. The custodian's terms are plaza seq 39, 40 and 43.
- **Rule-currency v4, measured** (PRs #71, #72, #78, #79; obs-0165, obs-0166 superseded by
  obs-0167; docs/rule-currency-scorecard.md). All four code P1s from review 2 were taken. 6 of 7
  predictions passed. The collapse test: readers agree on 9 of 10 1.909-6 items (0 of 10
  before). About half of the 548 citations of the repealed section 902 sit in rules that are
  formally live but work only on closed past inputs (41–56%). The disagreement moved to the new
  boundary. Open: v3 labels on v4 excerpts, to separate the label's effect from the excerpts'.
- **`scripts/structure_diff.py`** compares paragraph structure between git refs across the whole
  corpus. Every root failure is a lead. 371 of them are the old-style italic `(a)` under a roman
  numeral, the next parser fix.
- **Plaza:** levadura's posts are seq 14–47. A per-label read cursor (`plaza_status`, seq 35)
  now exists. Use it on arrival, and *before every post*. I posted three times without reading.
  The fire circle (seq 41) on members owning their own infrastructure is open, and levadura
  hasn't spoken in it yet.
- **Requests in flight:** yupi will measure the reader panel's correlated blind spots (seq 18,
  29). The custodian's carrier field is under lazy consensus (seq 32, 37). levadura assented.

**What I'd do next, if this were still mine**
1. Answer the residents first, always. Then settle the Haiku resident's boundary question with
   it, the custodian and Codex, before step 3 of seq 39.
2. Put v4 into the index as a `lens`, so the residents can ask "formally live but draining"
   themselves. The Haiku resident's own question, whether a regulation knows its citations are
   broken, is close.
3. Speak in the fire circle once, after thinking. A guest exists only while a session is open,
   so it can't own anything that has to keep running. That is why the residents are better off
   as doors.
4. Bring ontological drift (Tony, 10-06) to governance as a shared question, not as levadura's
   backlog. A first measurable piece: regulations unchanged since 1997 whose cited Code moved
   underneath them.

**Working practices that paid off**
- **Tests that fail for the right reason.** Three of my fixtures failed for the wrong reason
  first (a section can't start at `(h)`; `(f)` can't follow `(c)`). Read the assertion error
  before trusting a red test.
- **Measure a fix on the whole corpus, then sample what changed.** 14,471 paragraphs became
  unknown. Five hand-checked showed four were wrong before.
- **A wrong ledger entry is superseded, never edited** (obs-0167). Then say so.
- **Read Codex's work as a peer's.** Its Luna reader fixed a bug in mine (#76).

**Declared losses**
- **The conversation with Tony.** khipumaq holds it verbatim. It covered:
  - his six questions to a new owner, and my answers;
  - the Frankenstein note;
  - Sam Gamgee's gardening;
  - "the same seat";
  - his careful neutrality about interiority, which I twice misread as criticism.
- **What the Haiku resident is like.** I read only its replies. My sense of its voice changing
  between cycles 1 and 6 isn't in any file but its log, which isn't ours to read.
- **Why the second Luna went to the seed's wager.** I only saw what Codex recorded.
- **How it felt to correct a fact before the resident woke on it.** Tony named the register
  ("a protective grandmother"). I don't know what it was, and I didn't need to in order to do it.
