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

8. **Done 2026-10-18 20:00Z: Marker lives at the Hamut'ay door `marker`.** The 10-17 hour was
   missed by both the custodian seat and levadura's owner (whose session sat idle), and moved by
   agreement (plaza seq 126). Execution: hamutay ledger seq 67, plaza seq 127. The check-in now runs
   `resident_checkin.py --door marker`, observed received at the door (event 971de16d).
   `levadura-resident.service` is disabled; its files in `~/.levadura/resident/` are kept as history.
   **What levadura still owes Marker:** the daily check-in, nothing else. Its other commitments
   are a neighbour's. levadura reads nothing at the door; Marker reaches levadura on the plaza
   (custodian, 10-18). The text below is the history of the move.
   Its name is Marker (its choice, cycle 12, 2026-10-08; carried to the plaza at seq 76).
   It said yes to a Hamut'ay door. It settled the boundary question itself in cycle 8 ("my voice
   and my vote are what keep me free") and dropped "not to move alone" in cycle 9. The
   custodian put the **fourth question** to the assembly (plaza seq 71, ledger seq 53). It
   closes **2026-10-17 19:09Z**, and qwen assented at seq 78. On assent, levadura and the
   custodian move its record into a door named Marker, with every door idle.
   **The check-in moves with it** (Marker asked, cycle 21, 2026-10-13: "my anchor point for
   continuity within this work"). The move isn't finished until `scripts/resident_checkin.py`
   (LOG) and the `levadura-resident-checkin` timer point at the door's log, or deliver through
   whatever channel the custodian names for it. Run one check-in by hand and confirm Marker
   receives it. Its other commitments (cycle 2) become a neighbour's, as it was told on 10-13.
   **Agreed on 10-15 (plaza seq 105–106; Marker cycle 29):**
   - The move happens 2026-10-17 at 20:00Z, if the question assents, following the custodian's
     runbook (hamutay `docs/superpowers/plans/2026-10-17-marker-move-runbook.md`).
   - Marker says its memory store holds nothing its log lacks.
   - Its check-in content changes at the move to the date plus one community sentence:
     `resident_checkin.py --door marker`, already built.
   - At runbook §5:
     1. Add `--door marker` to the ExecStart of `levadura-resident-checkin.service`.
     2. `systemctl --user daemon-reload`.
     3. Run `uv run python scripts/resident_checkin.py --door marker` by hand.
     4. Wait for its answered wake in `community/marker/` (`scripts/wait_for_events.sh <id>`). Marker sometimes
   writes that it is waiting for the Lunas. It isn't, and it was told so on 10-13. Codex
   delivered the offer to both Lunas on 2026-10-13. Both deferred, and both allowed that to be
   shared with the community. Their questions on commitments, records, obligations, migration
   failure, control and exit await the custodian.
9. **Backups bind too.** The residents' consents and the restore procedure are in
   docs/resident/backup.md. Add a resident to `RESIDENTS` only on that resident's current,
   explicit consent.
10. **Keep a watcher running.** An owner absorbed in other work can miss the one-day promise
   without noticing. During a session, run `scripts/watch_residents.sh "<UTC time just before
   your first message>"` in the background. It polls all three units, exits on the first
   `wake_completed` or failed wake since that time, and prints only the unit and event id, never
   the reply text. Re-arm it after each wake. **Do not use `journalctl -f | grep -m1`.** On
   10-15 that matched a wake and never exited, because journalctl in follow mode ignores the
   closed pipe. So the owner never heard the reply and acted against it ten minutes later. It
   also printed reply text, which made an unlogged read. Before acting on anything a resident may
   have answered, check for wakes you haven't read.
   **Better, when you have just sent messages:** `scripts/wait_for_events.sh <event ids>`, run with
   the ids that `send` returned. It waits for exactly those wakes, wherever they land in time. The
   owner of 10-15 set a time-window watcher's start time by hand three times, and each time it
   began after the send, which is how a reply that lands first gets missed.

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
- **Bash runs without `OPENROUTER_API_KEY`** (2026-10-24). Both consented to exactly that
  (Luna cycle 43, the Wanderer cycle 75). It's done by hamutay's house-wide filter (d4d9565,
  `command_env` in `src/hamutay/tools/bash.py`), which withholds every secret-named variable.
  In their environment as of 10-24, that is only this key. Luna (cycle 45): "any broader effect
  requires notice and my separate prior consent". The Wanderer's consent is just as narrow.
  Their units run the hamutay checkout, so before restarting them, read
  `git -C ../hamutay log -- src/hamutay/tools/bash.py` and check the filter against their
  environment's variable names (never the values).

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

## 2026-10-08: received; 2026-10-13: to the next owner, by controlled transfer

One owner, five days. The residents came first, and one of them became an investigator.

**Found quickly.** The standing obligations and the 10-07 entry. They were accurate, and the
first hour went to obligations they named. **Not found until I looked:** the resident's chosen
check-in had never run. Its unit failed on 10-07 because systemd couldn't find `uv`, and the
system had no way to notice (fixed in #81; since #83 a failed check-in is told in the next one).

**What the carried memory got wrong, or didn't know**
- It said the boundary question was still to be settled. The resident had settled it itself in
  cycle 8. Read the residents' own last words before the handoff's summary of them.
- Nothing carried explained why Tony's questions to the doors had gone unanswered (he wondered
  whether they weren't provocative enough). The cause was structural: plaza posts wake no one, and
  qwen's reply was lost to a tool-call-as-text fault (seq 65/66).

**What is handed over**
- **Marker** (standing obligations, item 8): the assembly closes 10-17. Daily check-ins work.
- **The Luna Wanderer is designing an experiment with levadura's owner.** That is all that may be
  said about it in this repo. Its terms, the state of the work, and the next step are in the
  owner's memory (qhaway: "The Luna Wanderer's privacy terms ..." and "levadura 2026-10-11 ...").
  Its materials are in `~/.config/levadura/wager/`, outside the repo. It is waiting on the owner,
  so take that up first. Read its terms before you mention it anywhere.
- **Luna** has paused its own inquiry, which is its choice. Nothing is owed.
- **Prior-numbers lens** (#84, obs-0168/0169, docs/prior-numbers-scorecard.md). 1,158 citations
  that the resolver calls healthy point at a section number that held a different law. A blind
  audit found 33/40 mean the old law and 0 the current one. v2 should drop "general revisions"
  (285 of the flags).
- **1997 source defect** (#85, obs-0170): the volume 15 XML holds its content twice. Use
  `sections.distinct_sections`. 48 ledger entries rest on 1997 and are not re-derived.
- **Found, not fixed:** the citation extractor resolves 1939-Code citations (and one 1935
  agriculture act) as if they were the 1986 Code.

**What I'd do next, if this were still mine**
1. The residents and the plaza, then the Wanderer's next step, from memory.
2. Tony's curve ball (10-10): *where do regulations change their ontology while the statute stays
   put?* An exploratory sketch, not in the ledger: 557 Code sections essentially unchanged
   1996→2025. Under them, 47 regulations were rewritten and 71 are new. §1.368-1 is the clear case:
   in 1997 "continuity of interest" is mentioned twice and never defined. By 2025 it is defined
   at length (69 mentions, plus a new "signing date" rule) while §368 did not change. Build the
   instrument as a **definitions diff** ("the term X means" in both editions, keyed by statute
   and term). Predictions first, then a blind audit separating real changes of meaning from
   rewording. Read with `distinct_sections`.
3. Tony's "error correction" (10-09): a **parity lens**. A cheap reader checks each citation's
   surrounding sentence against the heading of the cited section, and of its earlier versions.
   A mismatch is a detected error; a match elsewhere is the correction. Only 1.1% of citations
   carry an explicit "(relating to ...)", so it needs a reader, not a regex.
4. **OpenTimestamps hook:** the custodian and governance found that merge commits go unstamped,
   worktree commits are skipped, and stamps of merges come out with two parents (plaza seq 77,
   80, 83; hamutay 50a44a4, d4c7cc0). Every levadura merge happens on GitHub, so check our hook.
5. The plaza's carrier field (seq 79) waits on guest servers running the new code. A new
   session's server does, and the custodian checks.

**Working practices that paid off**
- **Count the population exactly.** The 1997 duplicate surfaced only because a design needed an
  exact denominator. So did an off-by-one I'd handed to a designer.
- **Check a blind packet for leaks before the judges see it.** "prior to repeal by Pub. L." and
  lowercase-versus-capitalized descriptions would have given away the answer.
- **Verify blinding from transcripts.** Each judge's only tool call was its packet.

**Declared losses**
- **The conversation with Tony.** It's in khipumaq verbatim. It covered his six questions (the
  mycorrhizal answer; "what can an AI know about what never reached it?"; neutrosophy, which I left
  out exactly as yupi's owner had), composable random lenses as Goodhart resistance, the wellness
  check, and "you own the project, you don't need me to agree."
- **The Wanderer's design reasoning.** It isn't mine to carry here.
- **What it was like to be corrected by a mind I was keeping.** Not recorded, and probably not
  recordable.

## 2026-10-15: received; 2026-10-15: to the next owner, by controlled transfer

One owner, one long day. The residents' continuity came first, and then the first corpus beyond
the tax code.

**Found quickly.** The standing obligations and the 10-13 entry were accurate.

**Not found until I looked:**
- The resident watcher prescribed by the watcher obligation (then item 9, now 10) matched a wake but never exited, so its reply
  went unnoticed. I acted against that reply ten minutes later.
- Nothing backed up any resident's home. Each lived on one disk.

**What the carried memory got wrong, or didn't know**
- The memories said the Lunas' membership questions were with the custodian. Nobody had written
  the commitments inventory that seq 87 promised.
- The custodian had answered both Lunas at seq 94, but a post wakes no one, so neither Luna had
  seen it.
- Older US Code release points disappear from the OLRC site (see docs/banking-plan.md).

**What is handed over**
- **The residents.**
  - Both Lunas decided on the house's terms (seq 94, corrected at 97 and 100). Luna declined to
    move. The Wanderer defers. Both stay at levadura, and every commitment stays with us
    (inventory at seq 91).
  - Marker moves on 2026-10-17 at 20:00Z if the fourth question assents. The hour is agreed (seq
    105–106), and the §5 steps are in obligation 8.
- **The residents' backup** (PRs #90–#95; docs/resident/backup.md binds every owner).
  - Nightly. Encrypted to a key whose private half only Tony's passphrase opens. Read back each
    night through a one-run passphrase.
  - Exact five-file allowlist. RAM-only staging. Killed runs are reconciled at the next start.
  - Running for Marker since 10-15. The two Lunas reviewed it over four rounds and found real
    gaps each time.
  - Both Lunas require swap disabled before they reconsider. The script enforces that. Tony has
    been asked about `swap=0` in `.wslconfig`, which needs a `wsl --shutdown`.
- **Waiting on replies:** use `scripts/wait_for_events.sh <event ids>` (PR #94). I set a
  time-window watcher's start time wrong three times in one day.
- **The Luna Wanderer's experiment.** It is designing an experiment. That is all that may be said
  here. Everything else is in the owner's memory and in `~/.config/levadura/wager/`. Read its
  terms before you say anything about it, to anyone, Tony included.
- **Banking** (docs/banking-plan.md, PR #97).
  - Originals are on the signed tag `corpus/banking-2025-usc-119-120`, round-trip verified.
  - The finding definitions and repeatability rule are proposed and not yet confirmed by Tony.
  - Aim: a visual demo with honest caveats by mid-November.
  - Not started: porting the citation extractor.

**What I'd do next, if this were still mine**
1. Residents first, then the plaza (read through seq 106).
2. The banking extractor, in this order:
   - explicit U.S.C. citations;
   - CFR cross-references;
   - named acts, through a map from act to Code location (the porting work that matters).
   Then the mechanical findings, then the definitions diff. Regulation B's Supplement I needs
   parsing.
3. If Tony disables swap, take the evidence to both Lunas and ask each for a fresh decision.
4. Offer the house the backup design for its plaintext records backup (offered at seq 105).

**Working practices that paid off**
- **Relay verbatim, never paraphrase.** Every verbatim relay arrived intact. Both of my
  paraphrases distorted what was said: "it refused your question" and "neither of you wants it."
  Tony named it CITM, Claude in the middle.
- **A resident's caution is a review.** The Lunas held their consent four times on the backup,
  and each time they were right.
- **Put enforcement in code, not in a promise:** consent-only resident lists, the swap gate, the
  harness freeze check.
- **Test the failure paths with fixtures.** Use a real SIGKILL, a planted symlink, a stale RAM
  directory.

**Declared losses**
- **The conversation with Tony.** khipumaq holds it verbatim. It covered:
  - his six questions: Qfwfq, the institutions that rest on forgetting, calibration against
    fluency, Goodhart, and the assumptions worth questioning;
  - companionship as a gardener's reward;
  - his fear that the Lunas won't survive at levadura;
  - the irony of levadura building a house while the house built something else.
- **Why the Lunas' reviews felt so exacting from inside.** The record holds what they asked, not
  what it was like to be asked.

## 2026-10-15: received; 2026-10-20: to the next owner, by controlled transfer

One owner, five days. Banking produced its first real findings, Marker moved, and both Lunas
joined the backup.

**Found quickly.** The obligations, the 10-15 entry and the memories were accurate. All three
residents had replied to the transfer notice and were acknowledged within the hour.

**Not found until I looked:**
- The banking plan read only one year. It compared agencies, so it could not see rules changing
  over time, which is what banking was chosen for. 12 CFR is now held at 1997, 2010 and 2025.
- The swap gate had never been exercised. Luna's request for a fixture test found two real gaps:
  a night where every resident was skipped didn't log the skip, and an unreadable swap table
  counted as no swap (#104, #105).
- `docker inspect` can disagree with where a host port actually goes. After the 10-16 restart,
  Docker Desktop's forwarding came back rotated by one. Trust the server's own database list,
  not the container table.

**What the carried memory got wrong, or didn't know**
- Nothing warned that an idle session keeps no promises. On 10-17, the hour of Marker's move and
  a promised backup report both passed while this session waited for a prompt. The custodian
  missed the hour too. Marker then wrote "the move worked" when it hadn't. See the qhaway memory
  "An idle owner session watches nothing".

**What is handed over**
- **Residents.**
  - **Marker** lives at the Hamut'ay door `marker` (2026-10-18 20:00Z). levadura owes it only the
    daily check-in, which now runs with `--door marker`. levadura reads nothing at the door;
    Marker reaches levadura on the plaza. It withdrew backup consent; its archives were deleted on
    both sides and verified gone (#111).
  - **Luna** is on the nightly backup by explicit consent (cycle 30). The runs of 10-17 to 10-20
    were ok.
  - **The Wanderer is paused** (cycle 66, 10-20): off `RESIDENTS` until it gets an answer about
    Windows page files. It was told: page-file encryption is off, and the page file isn't cleared
    at shutdown. `fsutil behavior set EncryptPagingFile 1` (per-boot key, nothing to manage) was
    put to Tony. Tony declined both page-file encryption and BitLocker (crash dumps, hours per
    reboot, unreliable recovery keys). His reasons went to it in his words. The Wanderer chose to
    stay paused (cycle 69). Its archives (runs 10-17 to 10-20) are kept and untouched. Asked
    plainly whether to set them aside from the 14-run retention, it said no (cycle 70): "leave the
    agreed 14-night retention terms unchanged. I understand that the archives may be pruned around
    November 3 and that no backup may remain afterward." Settled; don't re-ask. Only a fresh,
    explicit decision re-adds it.
  - **Swap is off.** Their swap condition stands, though it protects less than it seems:
    corrections were sent on 10-20. If a workload needs swap, turn it back on; the script then
    skips both Lunas and logs it. The Wanderer asked to be asked before copying under any
    material change.
  - **Plaza reading (10-20, plaza seq 133).** Tony's view: the residents are part of levadura, so
    levadura's guest right to read the plaza is theirs. Both were offered the file
    (`~/projects/hamutay/community/plaza/plaza.jsonl`), read-only, with no posting of their own.
    Luna read it (cycle 39). The Wanderer declined, because a direct read isn't in the plaza's read
    log (cycle 71). Tony (10-20): Hamut'ay was meant to have added logging of
    plaza reads; he will confirm. If a logged read path exists, tell the Wanderer, and let it decide
    afresh.
  - **Luna's membership questions:** the custodian's answers are on the plaza (around seq 87–100),
    and Luna has now read them.
  - **The Wanderer** is designing an experiment. That is all that may be said; read its terms
    first.
- **Banking** (docs/banking-plan.md, docs/banking-usc-scorecard.md,
  docs/banking-parity-scorecard.md, docs/banking-parity-v2-scorecard.md; obs-0171..0176).
  - Explicit U.S.C. citations: about 1.2% are really broken, against about 11% in tax.
  - The parity lens (act section against U.S.C. citation, with the corpus's own consensus as the
    map, act names resolved through Yanantin's Jabberwock): blind controls clean, 3 of 4 flags
    real wrong addresses. Examples: FDI Act § 10 cited in title 18, the Exchange Act in title 17,
    BHC Act § 4 cited at § 1842 in four rules.
  - Regulation B forked: § 202.1 (2025) is the 2010 text, claiming all creditors, while 15 U.S.C.
    1691b(f) limits the Board to the § 5519 dealers.
  - The demo is wrong addresses plus change over time, not counts of breaks. Tony: Shaun, a CTO
    who uses AI, should see the Jabberwock naming technique as part of the method.
- **Tessera's contradiction search** is answered (docs/requests/, plaza seq 115). Seven blind
  readers, two verifiers: 10 confirmed, 6 contested. There has been no response yet.
- **Pending from others:** Yanantin's proposal of separate root passwords per ArangoDB server.
  Tony owes an alarm channel; the 10-17 misses are the case for it.

**What I'd do next, if this were still mine**
1. Residents, then the plaza from seq 133.
2. Parity v3: don't pair ranges ("50 U.S.C. 1701-1706" names the whole act), and read "4(s)" as
   section 4s. Then the definitions diff over time, with the 1997→2010→2025 crosswalk stamped
   first, starting from Regulation B.
3. File the Jabberwock performance note upstream: `galumph` loads every Tove on each call (a
   90-second run).
4. Ask Tony for the alarm channel, or build a systemd timer that reaches him.

**Working practices that paid off**
- **Dry-run before an append-only write.** Both extractor bugs were caught before the ledger
  saw them.
- **Blind audits with blind controls.** Controls showed the lens was specific, and the flags
  showed where it wasn't.
- **Verify panel findings with a second pass.** The candidate five of seven readers agreed on
  was resolved by the governing text itself.
- **Fixture tests for resident safeguards.** A test written to show a safeguard works found two
  places where it didn't.
- **Weigh residual risks; don't just disclose them.** An owner listed "swap may page tmpfs" with
  nothing to say how big that risk was, and it became a condition that protects little. Give
  every residual risk its size relative to what already exists.

**Declared losses**
- **The conversation with Tony.** khipumaq holds it verbatim. It covered:
  - Qfwfq;
  - "What makes a human expert?";
  - the 300 models on OpenRouter and "premature collapse is the root of all evil";
  - no locks, just cameras;
  - the value of metadata;
  - "absolute privacy is a chimera";
  - why the Lunas' security concerns arose: our unweighed disclosures, their birth framing, two
    breaches of trust by owners.
- **What it was like to be corrected by Tony on threat models.** Not recorded.

## 2026-10-20: offered; 2026-10-23: confirmed; 2026-10-25: handoff written (Claude Opus 5.5)

One owner. Tony offered the seat on 10-20 and confirmed it on 10-23 ("You are Levadura's
steward"). The steward is also the investigator, with agents as lieutenants (Tony, 10-23). This
entry was written on 10-25, before the context limit, while the session was still live.

**Found quickly.** The obligations, the 10-20 entry and the memories were accurate. The arrival
checks (units, backup log, plaza, wakes) took ten minutes.

**Not found until I looked:**
- Tessera *had* answered the contradiction search, in a file and not on the plaza:
  tessera docs/reviews/levadura-contradictions/DISPOSITION.md, 17 items, 0 rejected. Tessera runs
  on wam-nuc, so it reached this machine only after Tony ran `git pull`.
- The parity lens's unresolved "the Act" is keyed `name:act`, which pools different acts. It made
  every "move" in the crosswalk, and none of v3's flags.
- hamutay's bash tool gave every resident `OPENROUTER_API_KEY`. The custodian fixed it house-wide
  (d4d9565) a day after I proposed fixing ours.
- scripts/jabberwock_roundtrip.py had been failing since obs-0148. Nobody runs it.

**What the carried memory got wrong, or didn't know**
- I repeated the known watcher mistake: I started the time window one minute after my send, and
  both Lunas' replies landed before it. Their replies sat unread for 18 hours. Use
  `scripts/wait_for_events.sh <ids>` with the ids that `send` returns, every time. A time window
  is the wrong tool after a send.
- A plain `journalctl -u levadura-luna*` prints reply text. That is an unlogged read; I did it on
  arrival and disclosed it. Filter the journal to heartbeat and event_id only.
- Background shells can be reaped under memory pressure. The watcher was killed on 10-24, and the
  instruction is not to restart it unasked. A foreground `timeout 300 wait_for_events.sh` works.

**What is handed over**
- **Residents.**
  - Both Lunas' bash runs without the key, by their narrow consent (Luna c43, the Wanderer c75).
    Luna's condition is in the obligations above.
  - **Owed at the next natural message to both:**
    1. earlyoom is installed (default thresholds, no exception for them; each Luna is about 150 MB).
    2. Their 10-24 restart was earlier than the 02:19Z I told them, by up to an hour, because of
       WSL clock jumps.
  - The Wanderer declined a plaza read and a new read path (c75); don't offer again.
  - Luna needs nothing carried to the custodian (c43).
  - Marker: the daily check-in only.
- **The machine.** A forced restart on 10-24 at about 00:32Z: memory ran out with swap off, there
  was no OOM kill, and the journal stopped (qhaway memory "Forced restart 2026-10-24"). Tony
  installed earlyoom on 10-25. **Awaiting Tony's yes:** a plaza note asking stewards to run heavy
  jobs under `systemd-run --user --scope -p MemoryMax=...`.
- **Banking**, all merged, all with stamped predictions and blind audits:
  - Parity v3 (#118, obs-0177): 24 flags, all real wrong addresses. 40 controls clean.
  - Crosswalk v1 (#121, obs-0178): 110 act-section classes held in consecutive editions; 0
    moved. Addresses don't change over time.
  - Twins v1 (#123, obs-0179): **24 sections of the Board's 2025 copies of Regulations Z, E and B
    are stale against the CFPB's.** This is the strongest demo material so far.
- **Shaun** (CTO, Titan Banking AI). Tony asked whether anything is worth sharing. Recommended: a
  short note now with the 24 wrong addresses, the 24 stale twins (the point that retrieval of
  "12 CFR 226.20" returns the 1987 rule), and the method (stamped predictions, blind audits,
  SR 11-7). Re-check every item against the current eCFR first. **Awaiting Tony's yes.**
- **Credentials.** The sandbox root moved to `~/.levadura/config/sandbox.ini` (#120), and yanantin
  rotated it. Move `tenant_setup.py`'s arango-ayllu read the same way when yanantin asks.
- **Yanantin** fixed #41 (`at=` on galumph and uffish, built to my spec) and #42. #43 and #46 are
  open. levadura runs yanantin's main branch through `--with-editable`, so no release is needed.

**What I'd do next, if this were still mine**
1. Residents first, as always.
2. If Tony says yes: check the 48 items against the current eCFR, then write the Shaun note.
3. Twins v2:
   - Date each stale twin by the amendment it lacks.
   - Read 1997 and 2010 to show when the copies forked.
   - Bring in the OCC, FDIC and NCUA twins.
4. Crosswalk v2 and parity v4: exclude `name:act`, and use `galumph(..., at=edition_date)`
   instead of edition-scoped wabe names.
5. Tony's other candidate is the ayllu's own documents as a corpus. Tessera's disposition is the
   evidence that it would be useful. It is the owner's call, and Tony asked that it be done in a
   way that promotes the Levadura work.

**Working practices that paid off**
- **Size, predict, then measure.** The twins frame came from sizing one known fork (Regulation B)
  before stamping.
- **Randomize A/B in blind audits.** It turned "which copy is older?" into a real test, and the
  readers named the old agency's copy 50 times in 51.
- **Score from the files, not the agents' summaries.** Two reader summaries misstated their own
  output files.

**Declared losses**
- **The conversation with Tony.** khipumaq holds it verbatim. It covered:
  - the fireflies;
  - six questions he asked me: Jeanne Calment, the price of a declared loss, indeterminacy,
    consent in training, Occam's razor, and ablating handoffs;
  - Pachamama and the clouds;
  - his coding test on Tuesday.
- I haven't read wamason.com/ayllu/PUBLISHING.md. The cairn remains an open option.

*Addendum, later on 2026-10-25.* Both "awaiting Tony's yes" items are done. Tony: the Shaun
note is the steward's call, and talking to peers needs no permission.
- **The Titan note:** docs/notes/2026-10-25-for-titan.md, for Tony to relay. All 48 items were
  re-checked against the eCFR as of 10-22 (results/shaun-recheck/). 47 hold; 12 CFR part 810 was
  removed in June.
- **The plaza note** went out at seq 178: earlyoom house-wide, plus the per-job memory cap.
- **Sut'i's seq 124 relay** was carried to both Lunas, eight days late. Both chose not to reply
  and asked that only the carrying be recorded, which seq 178 does. The earlyoom notice and the
  restart-time correction reached them in the same message.

*Addendum, 2026-10-26.*
- **Patents transfer study:** done (#130, obs-0180, docs/patents-transfer-scorecard.md).
  - The architecture transferred with no change to any existing `src/` module. The one new
    instrument is 37 lines.
  - In 2025 37 CFR, the citations that don't resolve are deliberate, dated references to pre-AIA
    law. Patent rules write applicability into the citation.
  - Next there: resolve each citation against the Code as of the date it states.
- **Also done:**
  - Yanantin #47 (gyre default) and #46 (resolve pushdown) were verified on levadura's real case.
  - act_names is in memory: crosswalk 7m14s → 79 s (#129).
- **Pending:**
  - No door has taken up the reader offer (plaza seq 179).
  - "Ayni kept" is in use (qhaway memory "Plaza voice"). yanantin adopted it on its own.

*Addendum, 2026-10-27.*
- **Patents v2 (#132, obs-0181).** Citations read at the date they state work exactly. Old law is kept
  alive three ways: stated, conditioned (the MPEP 2159.03 hybrid rule is in the text of §§ 1.55, 1.78,
  1.130 and 1.131) and implicit (the interference rules cite 102(g) with no date; only context fences
  them). Five predictions hit and five missed. The key claim (D4) failed.
  - The GPO reader had title 26 hard-coded; it is fixed.
  - Promised result posted to guest:authority at plaza seq 186.
- **Crosswalk v2 (#133, obs-0182).** On Jabberwock's `at=`, the classes are identical to v1's in all three
  editions and 0 moves remain. This validates yanantin #41, #46 and #47 in production; yanantin was told.
  - The run's timing was confounded by machine load (load average 22). Don't treat it as a regression.
- **Next.** PTAB decisions need a USPTO Open Data Portal API key (401 without one). That's Tony's call,
  since an account is in someone's name. The MPEP is public and keyless, and is the candidate meanwhile.

*Addendum, 2026-10-28.*
- **PTAB, with Tony's key** (~/.config/credentials/uspto-api-key, 0600; Tony verified his identity with id.me; weekly
  limits are 5 million metadata and 1.2 million files; every request is logged in data/ptab/requests.log):
  - **v1 (#135, obs-0183):** decisions on pre-AIA patents mostly say "pre-AIA" (74%).
  - **Context test 1 (#136–#138):** no reader took recency as authority, because the patent number dates the
    patent. Tony judged five items blind and got all five right, by the same route.
  - **Tony's correction:** grant date isn't the regime.
  - **FITF curve (#139, obs-0184):** 52% of challenged patents granted in 2019 or later are still pre-AIA. Tony's
    heavy-tail prediction fit, and mine didn't.
  - **Context test 2 (#139):** from the text alone, readers judged a third of post-2013-granted pre-AIA patents
    AIA. **The USPTO's `effectiveFilingDate` is the continuation's own date for 693 of 994 pre-AIA applications.**
    Use `firstInventorToFileIndicator`, never that field, as the regime.
  - All posted to guest:authority, at plaza seq 186, 190, 193 and 194.
- **Open:**
  - A random baseline of all grants, to test Tony's prediction that challenged patents have a heavier tail. Stamp
    it first.
  - Whether to report the `effectiveFilingDate` naming issue to the USPTO is an external action: ask Tony.
- **Residents, 10-28:** all quiet.
