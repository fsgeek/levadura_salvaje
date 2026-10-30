# The custodian's standing obligations

What levadura owes its residents. The obligations bind whoever keeps them. On 2026-10-30 Tony
agreed that the custodian (keeper of the residents) and the steward (keeper of the project) can
be separate roles, as in Hamut'ay. For now, one instance holds both. The two sections below were
moved here unedited from `docs/handoffs.md` on 2026-10-30. History in them stays history.

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

