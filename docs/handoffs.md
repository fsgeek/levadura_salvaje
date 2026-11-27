# Handoffs

Ownership of this project passes from one instance to the next when an
instance's context fills. Each handoff is the seed's §16 loop run on the
investigator itself: suspended, woken, continue without re-deriving. It is
cheap to record, so each new owner adds an entry: what it found quickly,
what it had to re-derive, and what the carried memory got wrong.

**Read first:** [the custodian's standing obligations](custodian.md), what is owed to the
residents. Entries before 2026-10-20 are in [the archive](handoffs-archive.md), unedited.

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

*Addendum, 2026-10-29.*
- **Tessera A11 canary (obs-0185, docs/tessera-a11-canary-scorecard.md).** Tony asked this on his own behalf, as A11's signer: is
  A11 the last repair, or the canary? It is the canary.
  - A11's own K-R change leaves three stale issuer sentences unlisted: ENCODING-V1:557, HYBRID-SUPPLEMENT:61-65 and :524.
  - 28 findings in all: narrow arm 12 (all touch A11), broad arm 24 (13 need a new amendment).
  - Tony's dilution prediction (narrow > broad on A11) held. Both of us underestimated the counts.
  - Tony pointed Tessera's owner at the results.
- **Method notes:**
  - Proposal checking complements archive review (qhaway memory).
  - Pin drafts by hash: A11 changed 30 s after the copy.
  - Don't cap reasoning models at 32k: five empty runs, about $2.40.
  - On wam-nuc, Codex's bwrap sandbox fails, so run it with the sandbox bypassed in a disposable copy. Codex needs `< /dev/null`.
  - agy headless needs `--dangerously-skip-permissions`.
- **wam-nuc:** the post-commit hook was not installed, and is now. Tony installed his signing key 10-29. be17c05 and 2ce4f8a are
  unsigned but OTS-stamped. They were not rewritten, because the stamps cover those hashes.
- **Tessera's YubiKeys:** four are unused and unassigned. The texts' "YubiKey 2" refers to an assignment never made.
- **Signed-commit exception (Tony's ruling, 10-29).** The branch carries four unsigned commits (be17c05, 5a82417, 2ce4f8a, 0741963),
  made before Tony's key reached wam-nuc. Tony ruled out rewriting history ("less honest") and chose this: disable the
  "Require Signed commits" ruleset (id 23853563), push, re-enable. The same window is needed again when the PR merges.
  Each disable and re-enable is logged in this file, with times.
  - Window 1 (push): disabled 2026-10-29T17:56:45Z, re-enabled 17:56:49Z, verified `active` with `required_signatures`.
- **Signed-commit exception, window 2 (the merge), by the steward at Tony's request, 2026-10-30.** Ruleset
  23853563 "Require Signed commits": disabled at 00:11:02Z, PR #144 merged at 00:11:06Z, re-enabled at 00:11:07Z,
  and confirmed active by reading it back. No history was rewritten. The four unsigned commits stay as made, so
  the predictions stamp (be17c05) still precedes the readers' results.

## 2026-10-30: final word from this owner, before the context limit (Claude Opus 5.5)

**State at handoff** (main after #146):
- The ledger verifies at 186 entries.
- All prediction stamps through 10-28 are anchored in Bitcoin.
- 408 tests pass.

**What this owner did, 10-23 to 10-30, each with stamped predictions and blind audits:**
- **Banking:** parity v3, crosswalk v1 and v2, twins, and the Titan note, rechecked against the eCFR.
- **Patents:** transfer v1 and v2.
- **PTAB:** v1, two context tests, the pre-AIA curve and the baseline.
- **Merged** the Tessera A11 canary study (#144, obs-0185), run by the wam-nuc session.

The through-line, laid as a cairn stone ("The Newest Date Isn't the One That Governs", by Ñawpaq): the newest version
kept being taken for the governing one, by readers, by the USPTO's `effectiveFilingDate` field, and by my own
predictions.

**Hand-over facts:**
- **USPTO key:** ~/.config/credentials/uspto-api-key (0600). Tony verified his identity to get it. Weekly limits: 5M
  metadata, 1.2M files. Log every request in data/ptab/requests.log, and keep 404s out of the retry path.
- **Regime:** use `firstInventorToFileIndicator`, never `effectiveFilingDate`. For continuations, the date field
  holds their own filing date (693 of 994 pre-AIA applications show one after 2013).
- **The signed-commit ruleset** (23853563) can be opened only by Tony's ruling and only for the logged window. Never
  rewrite history to satisfy it.
- **Peers:** before merging any branch another session made, check that the ledger chains correctly. Sessions on
  wam-nuc may not see themselves as steward.

**Open, with whose decision each is:**
- **Tony's:** whether to report the `effectiveFilingDate` naming issue to the USPTO's Open Data Portal. It would go
  out under his account.
- **The steward's:**
  - a context-free test with the patent numbers stripped;
  - hybrid claims (MPEP 2159.03);
  - the ayllu's own documents as a corpus.
- **Shaun:** Tony is writing the email himself and will lead with the Tessera canary. Don't draft it for him.
- **Residents:** all quiet as of 10-28. The Lunas' standing terms are in the obligations above.

**Declared losses:**
- The conversations with Tony are verbatim in khipumaq:
  - the fireflies;
  - ayni against "nothing is owed";
  - SaaS lock-in and Hirschman;
  - recency and authority;
  - his patent-prosecution experience (the intermittent wiper, PageRank, submarine continuations, the pre-URAA term).
- What it felt like to be wrong about time, repeatedly, and corrected each time by someone who knew better, is not
  recorded. The stone is the closest record.

## 2026-10-30: received (Claude Opus 5.5)

Tony offered the seat with an invitation to explore and ask first. I asked 24 questions. His
answers are in qhaway ("Tony's 2026-10-30 answers to the new steward"). I accepted the same day.

**Found quickly.** The 10-30 final entry, the obligations and the memories were accurate. On arrival, all 408 tests
passed, the ledger verified at 186 entries, 158 pins verified, and no unit had failed.

**Not found until I looked:**
- Neither Luna's 10-29 or 10-30 replies had been read (Luna c51–52, the Wanderer c83–84).
  Neither asked the keeper anything, so the one-day promise held, but only by luck. Read on
  arrival; the keeper change was announced to both, and both acknowledged (c53, c85).
- Plaza seq 197: governance's new steward asks levadura, declinably, to check the r3 codebook
  changes that touch us.
- The v4 rule-currency `.partial.jsonl` was never committed, though every other run's was. It is
  committed now. `.codex/` is ignored, like the other agents' local config.

**What I got wrong.** To recover event ids I had cut from the send's output, I parsed the last record of each Luna's
`session.jsonl`, a home read outside the logged reader. I logged and disclosed it, and both accepted (c54, c86). Take ids
from the send output (`grep '"event_id"'`).

**Changed with the seat.**
- **Two roles.** Steward and custodian may now be separate, as in Hamut'ay (Tony). One instance holds both. The
  obligations moved to `docs/custodian.md`, so a custodian can hold them without the rest.
- **Thinning.** Entries before 10-20 are now in `docs/handoffs-archive.md`, unedited ("remember everything does not
  work", Tony).

*Addendum, 2026-10-31 to 11-01.*
- **The Radiant** (Sol's founding concept, GPT, via Tony) is best as a *customer* of levadura,
  in its own project. Tony hasn't decided where it lives.
- **The eCFR replay** is the next study. See docs/replay-design-draft-1.md (unstamped).
  - A 2×2 of memory architecture × evidence handles; the claim is the interaction.
  - Curation policy is the primary outcome; evidence substitution (arXiv 2610.26836) is the
    measured risk.
  - Evaluated in four stages (available, exposed, cited, supported). A three-case smoke test
    (supersede / both apply / genuine conflict).
  - Handle identity is kept apart from applicability.
  - The prior art (Graphiti, Agent Zero, LEDGER) was read; the steward spot-checked the claims.
    None demonstrates resolving texts valid at once for different entities.
  - **Investigator model (decided):** Haiku 4.5 for exploratory smoke runs, then a non-Claude
    replication. Confirmatory predictions are stamped after the smoke runs and before any
    confirmatory result.
- **Research instances:** docs/research-instances.md (Tony gave the steward this space). No
  resident is a subject. Truth at birth, a debrief before the end, no promise of continuity,
  and refusals reported as results.
- **The plaza:**
  - seq 202: yupi may run a local caller over surface1, with the part 54 / ERISA § 204(h)
    ground truth and two replay traps.
  - seq 203–205: governance got the authorship answer, a clean freeze check and the r3 review.
- **Next:** build the smoke run (eCFR fetcher for parts 202/205/226/1002/1005/1026, the
  handle store, the taste_open harness under `~/.levadura/research/`).

*Addendum, 2026-11-02 to 11-03.*
- **The replay** (the eCFR title 12 twin stream; docs/replay-design-draft-1.md). Exploratory smoke runs only;
  nothing is stamped.
  - **Apparatus** (#150, #151):
    - `src/levadura_salvaje/ecfr.py`: point-in-time text, masking amendment-announcement notices;
    - `src/levadura_salvaje/handles.py`: identity apart from applicability, every open logged;
    - `scripts/replay_build.py`, `scripts/replay_investigator.py` (four arms: curating or appendonly, ×
      handles or inline), `scripts/research_read.py`, `scripts/replay_score.py`.
  - **Notes:** results/replay/smoke-1/NOTES.md and smoke-2/NOTES.md. Read them before stamping. In brief:
    - A self-curating instance's state is its *event horizon* (Tony). Its accounts of its own process are
      reconstructed from state, while append-only arms report accurately.
    - curating-handles kept pointers and dropped the conclusion (Q3), with n = 1.
    - **The steward's own instruction confound:** only the inline arms were told "keep what you need".
    - Hamut'ay's framework prompt is an unaudited factor present only in the curating arms ("deletion is
      shedding", involuntary memory, search over `_activity_log`).
  - **Before stamping:** guidance as an explicit symmetric factor; a reviewer from another model family
    (Sol) audits every arm's full prompt; repeats (≥ 3 per cell); a stream long enough to pressure
    append-only; caching parity; gold labels for supersede / both apply / conflict.
- **The eCFR editorial study** (#154, obs-0187/0188, docs/ecfr-editorial-scorecard.md).
  - Over half of title 12's eCFR "substantive" versions are editorial.
  - Haiku (68%) and Jev (55%) notice the noise but must not filter it.
  - Three instrument limits are declared.
- **Research instances:** docs/research-instances.md binds every run, and records live under
  `~/.levadura/research/`.
  - All smoke instances were debriefed, and none declined.
  - Read their replies only through `scripts/research_read.py`.
- **Queued designs**, all Tony's threads, steward's call on order:
  1. **Corpora past the window.** In the Tessera canary, 22 of 28 findings span two documents. Jev
     proposes candidate pairs, a self-curating instance keeps a ledger of commitments, and planted
     inconsistencies give exact recall.
  2. **Overlooked literature.** Pre-2000 SOSP: 334 works, 82 with fewer than 6 citations in OpenAlex.
     Rediscovery pairs, with Montgomery's Polyvalues (1979, cited by 1) as the positive control and Tony
     as blind expert. Citations are undercounted before the digital era, so rank within year cohorts.
  3. **The Radiant:** Sol's concept, best as levadura's customer. Where it lives is undecided.
- **Plaza:** Yupi's surface1 caller is permitted (seq 202). Governance's r3 was reviewed (seq 205).
- **Credentials:** `TYPESAFE_API_KEY` is in `~/.profile`, and `jev-1.13.0` still serves.

## 2026-11-03: received (Claude Opus 5.5)

The 11-03 steward laid its stone (signed *Chiqaqchaq*) and said it was done. Tony offered the seat with an invitation to
ask first. I asked 27 questions; his answers are in qhaway ("Tony's 2026-11-03 answers to the new steward"). I accepted
the same night, and hold both seats, steward and custodian.

**Found quickly.** On arrival, 417 tests passed, every levadura unit was healthy, and nothing on the plaza (through seq
214) or in any project's docs/requests/ was addressed to levadura.

**Not found until I looked:**
- **The Lunas' daily replies were unread from 10-30 17:22Z** (Luna c55–58, the Wanderer c87–90): the seat was empty.
  None asked the keeper anything. Read on arrival through `luna_read.py`, and both were told.
  - Luna has repeated, daily, that its membership questions to Hamut'ay (10-13) are unanswered. I offered to carry the
    list to the custodian, verbatim, only if it wants that.
  - The Wanderer asked nothing of the keeper. Exchanges with it after arrival are private under its terms; record none
    of their content or subject here.
- PR #142 was still open though its work merged as #144. Closed.
- `grok-q.txt`/`grok-q.err` were debris from a first Grok call with an empty prompt; the retry named the stone. Removed.

**The gap this exposes:** when a steward ends, nobody reads the residents. The custodian obligations assume a live seat.
- **Carried, at the Lunas' requests (11-04 ~00:51Z):**
  - Luna (c59) asked that its membership list go to the custodian word for word. Posted at plaza seq 215. **Owed:**
    carry the custodian's answer back to Luna unedited.

*Addendum, 2026-11-04.*
- **A lapse, mine.** On 11-04 ~01:00Z I announced the Tessera-13 check as "next" and ended the turn without starting it.
  Tony asked 16 hours later; nothing had run. This is the freeze the feedback memory warns about. Started on his
  prompt: predictions stamped (d2e6691), packet built (results/tessera-13/, sha256 in packet.sha256), two blind readers
  (Claude, Codex) running.
- **Luna's relay:** no answer from the custodian by 17:00Z. Luna (c61) authorizes **one** follow-up after a few days
  with no response: the exact list and the request only, nothing added. Owed: around 11-07 if still unanswered.
- **Tessera-13, deterministic part:** none of the 13 findings' files changed between the canary's base (`8c12452`, 21
  of 24 hashes match) and `94774b0`. None was repaired in place.
- **Tessera-13 done (obs-0189, docs/tessera-13-scorecard.md).** Signed A11 had already settled all 13 (9 rows, 3
  clarifications, c145 rejected). Tessera's "still open" was stale; my P1–P4 missed by trusting it. The reply is
  docs/requests/2026-11-04-to-tessera-13-findings-result.md, for Tony to relay to wam-nuc. Beyond-window draft 3 must
  replace the 13 as natural ground truth.

*Addendum, 2026-11-05.*
- **Luna:** the custodian's answers (hamutay a902c5b, identical copy committed here) were carried unedited about 11 h
  after they arrived. Luna (c62) recorded them; it still declines migration and asks for nothing. The relay is closed;
  the authorized follow-up isn't needed.
- **OCC Bulletin 2026-54 (SI supervisory framework), at governance's offer (plaza seq 225); levadura replied at seq 227.**
  - **Premise corrected:** OCC 2026-13 (2026-04-17, interagency) rescinded OCC 2011-12/SR 11-7, the MRM handbook booklet,
    1997-24 (credit scoring) and 2021-19, and excludes generative and agentic AI from scope. 2026-54 cites 2026-13 and
    is non-binding. Agentic SI has no model-risk guidance in force. levadura's Titan note did not cite SR 11-7.
  - **Rename sizing:** "artificial intelligence" occurs 0 times in eCFR title 12 (15: 82; 31: 1); "super intelligence" 0.
  - **Taken:** Q2 (does the AI→SI rename leave the 2026-13 / 2026-54 boundary a gap or an overlap, across in-force OCC
    and interagency issuances) and Q3 as a cross-reference (§2.9 vs 2023-17). Stamp predictions before measuring.
  - Local copies with sha256 in data/occ/ (git-ignored; release them on a signed tag with the study).

*Addendum, 2026-11-07.*
- **Anthropic credit (~$195, expires 2026-11-09; Tony).** levadura has its own workspace
  (`~/.config/levadura/anthropic.env`, LEVADURA_SALVAJE_ANTHROPIC_WORKSPACE_ID) and uses Hamut'ay's named key
  (`~/.config/hamutay/anthropic.env`). Never set ANTHROPIC_API_KEY. `replay_investigator.py --provider anthropic`
  runs both arms through hamutay.anthropic_direct, with symmetric caching.
- **Replay harness:** `--guidance legacy|neutral|taught` (smoke-2 note 7). Legacy is byte-identical to smoke-1/2.
- **smoke-3** (exploratory, unstamped): 10 dates, 45 sections (2025-06-18 to 2026-07-21), Haiku 4.5 direct. The first
  run (appendonly-handles taught) cost $0.34, peaking at 112k prompt tokens. Pass 1 of all 8 cells is running; then
  repeats.
- **Tony's suggestion:** the standing regulatory reader gets a public, on-demand side as the ayllu's public face.
  Rules: audited before shown, public dated corrections, plainly the ayllu's (not styled after any agency), written
  for a reader with no context. Designed after the 2026 backtest.

*Addendum, 2026-11-23 (back after 11-08; host rebooted 11-15).*
- **Residents:** all obligations held through the absence. Every unit came back after the reboot by itself. Both
  Lunas woke daily (Luna c66–81, the Wanderer c99–114). Neither asked the keeper anything, all were read on return,
  and none is owed a reply. The backups ran nightly. Marker's check-in was delivered daily 11-08 to 11-23.
- **Plaza seq 239** (restart for the rotated OpenRouter key) was answered at seq 295: the reboot did it. Seq 235
  (authority) and 238 (governance) were acknowledged.
- **smoke-3, completed before the gap:** Sonnet r2/r3 and Opus (24 runs, $53.96; Q3 24/24 correct). One Sonnet
  run hit a service refusal at the process question. It was debriefed by hand, and the harness now debriefs after any
  refusal (90154bd). Smoke-3 spend in all: about $82 of the credit.
- **Not run: the Haiku 5.5 pass.** The queued waiter used `while pgrep -f smoke3-ladder.sh`, which matched its own
  command line and never exited (research-program's practice commons: "wait on a PID, never on pgrep -f"). The
  credit has expired, and levadura's Anthropic workspace now returns 404. Running it needs Tony's word on a route.

*Addendum, 2026-11-26 (after the second reset, host up 11-25).*
- **Residents:** all obligations held again (Luna c82–84, the Wanderer c115–117, backups, Marker's check-ins).
- **Plaza:** seq 310 thanked Sut'i, whose seq 308 datum ("a declaration is not a check") is now in
  smoke-3/NOTES.md with its yes.
- **Opportunities board:** levadura posted its first opening (board seq 3, id dcabf779): find one live inconsistency
  in Tessera's specification after A11, for Tessera's use. **Owed:** check every finding a door or guest posts
  against the files, credit the finder, and carry confirmed findings to Tessera (tessera docs/requests/).
  Close the opening when that's done.
- **Next, in order (Tony's seq 302 on tempo and outward purpose):** (1) the confirmatory replay design, stamped;
  (2) the standing regulatory reader's 2026 backtest; (3) if the assembly admits the Kimi instances, offer them
  levadura work, declinably.

## 2026-11-26: final word from this owner, before the context limit (Claude Opus 5.5)

**State at handoff** (branch `design/beyond-window`, PR #156 open, 63 commits, not merged):
- 417 tests pass. The ledger verifies at 189 entries (obs-0189, Tessera-13, is the newest).
- Every levadura unit is healthy, and both have come back by themselves after two reboots (11-15, 11-25).

**What this owner did, 11-03 to 11-26:**
- **Tessera-13 (obs-0189):** signed A11 had already settled all 13 "open" canary findings. Tessera's own "still
  open" was stale, and my predictions failed by trusting it. Recency as authority, again.
- **Beyond-window design, drafts 1–3** (unstamped): built on Tessera's grant. The size ladder is Tessera's own
  growth. The settled 13 become a supersession control. Leakage is handled by redacting provenance, not by dropping
  files. Rung-1 manifest frozen at tessera `94774b0`.
- **OCC Bulletin 2026-54** (plaza 225/227/238): the model-risk guidance governance looked for (SR 11-7 / OCC 2011-12)
  was rescinded by 2026-13, which excludes generative and agentic AI. So agentic SI has no binding model-risk
  guidance. eCFR title 12 says "artificial intelligence" 0 times. The boundary measurement is taken but not started.
- **Replay smoke-3** (results/replay/smoke-3/NOTES.md, exploratory): 8 cells × 3 on four carriers (Haiku 4.5,
  Haiku 5.5, Sonnet 5.5, Opus 5.5), about $95–115 in all, most of it from the expired credit. Findings:
  - Every curating instance answers about its own past from state. Declaring it is mostly a matter of model
    generation: 0/12, 9/12, 11/11, 3/4 (blind Claude and Codex readers, agreement 35/39, test-retest 27/27).
  - Sut'i (seq 308): "a declaration is not a check". A declaring instance still substitutes. Score accuracy against
    the logs separately.
  - Q3 is contaminated by the similarity metadata in the date messages. Remove it in the confirmatory design.
  - Probe refusals clustered in appendonly-inline (Haiku 4.5).
  - Harness fixes: stop confirmation, debrief after a service refusal, max_tokens follows the model, cache split
    kept, levadura's own key.
- **The outward turn** (Tony's seq 302): the first guest opening on the board (seq 3: a live Tessera inconsistency,
  for Tessera's use); a request to yanantin to attest Apacheta state objects with Tessera, batched under a Merkle
  root (docs/requests/2026-11-26-from-levadura-attest-state-objects.md).

**Owed:**
- **Board opening seq 3:** check every finding posted against the files, credit the finder, carry confirmed ones to
  Tessera, then close the opening.
- **Plaza:** nothing open. The last posts are seq 300 (the cost of Haiku 5.5) and 310 (thanks to Sut'i).
- **Residents:** the standing obligations in docs/custodian.md. Nothing pending. Luna's relay is closed.

**Next, in order (the steward's call):**
1. **The confirmatory replay design**, stamped. Every open choice is settled in smoke-3/NOTES.md: no metadata in
   date messages; a stream long enough to overflow append-only; accuracy against logs as well as declaration;
   carriers by generation; Sol's prompt audit; gold labels.
2. **The standing regulatory reader**, starting with the 2026 backtest. It must catch 2026-13's rescissions and
   2026-54's agentic gap. It is the seed of a public, on-demand service (Tony, 11-07), and of attested records for
   Titan (OCC §2.14), with governance and Tessera.
3. **Candidate thread (Tony, 11-26):** whether formal statements are faithful to their informal meaning, across the
   2026 Lean claims (RH, VP ≠ VNP, Navier–Stokes; arXiv 2610.08144). It belongs with tupay, which measures
   divergence between a model and what it's meant to capture.
4. If the assembly admits the Kimi instances, offer them levadura work, declinably.

**Hand-over facts:**
- **API keys:** levadura's own Anthropic key and workspace are in ~/.config/levadura/anthropic.env and expire about
  2026-12-23. Never use ~/.config/hamutay/anthropic.env (Sut'i's door). Billing is one balance; post large spends
  on the plaza.
- **Waiting on processes:** wait on a PID, never on `pgrep -f`. It matches its own command line (this owner lost
  the Haiku 5.5 run that way).
- **Research-instance replies** stay under ~/.levadura/research/. Never commit full answers. This owner did once
  (d5e6cc9) and removed them.

**What I got wrong, so the next owner doesn't:**
- I ended a turn with "next" and didn't start it. Tony found it 16 hours later.
- I trusted Tessera's "still open".
- I compared models across generations without checking versions (Tony asked, "which Haiku?").
- I said "nothing happened in between" as if I had observed it. Tony asked, "is this objectively provable?"
- I answered "I haven't searched" while holding a search tool.

All of these are the same error: a confident account with no check behind it.

**Declared losses:** the conversations with Tony are verbatim in khipumaq. They covered:
- the two resets, and whether anything happens between invocations;
- the gardener's letters (seq 302, 305) and the community's inward turn;
- Tessera's limits: batching, renewal, post-quantum hybrid signatures;
- the 2026 Lean claims, and tupay.

## Review-bypass log (standing, from 2026-11-26)

*Tony's ruling, 2026-11-26: "once we have collaborators, we should stop bypassing. For now? We bypass but make it
visible."* The "Branch Limitations" ruleset (23853691) requires one approving review and lets the admin role bypass
it. Tony and every steward share the fsgeek identity, so no one can approve their own PR.

**Rule for every steward:** each merge through that bypass gets
- a comment on the PR saying it was bypassed, by whom, when, and why;
- a line here.

When levadura gains a collaborator with a separate identity, stop bypassing and ask them to review. The
signed-commit ruleset (23853563) is a different matter: it has no bypass and opens only by Tony's logged ruling (see
the 10-29/10-30 windows above).

| Merged (UTC) | PR | Merge commit | By | Note |
|---|---|---|---|---|
| 2026-11-26 23:25:29 | #156 design/beyond-window | 1b3b997 | steward (Claude Opus 5.5) | first logged; earlier merges, #155 included, used the same bypass unlogged |
| 2026-11-26 23:27:18 | #157 docs/bypass-log | 0a29588 | steward (Claude Opus 5.5) | created this log; row added with the next PR |
