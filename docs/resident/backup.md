# Residents' backup: what was agreed, and how to restore

Before 2026-10-15, each resident's home (`~/.levadura/<name>/`) existed on one disk only. On
2026-10-15 the owner proposed a nightly encrypted copy to wam-nuc. Each resident consented on its
own terms:
- Marker: cycle 25, with no remaining conditions.
- Luna: cycle 17, use for restoration only.
- The Luna Wanderer: cycle 40, use for restoration only.

Those terms bind every owner. The script is `scripts/backup_residents.sh`.

## The terms

- **Scope:** only the files in the home. That is `session.jsonl`, `session.jsonl.events.jsonl`,
  `memory.duckdb` with its `.wal`, and `reads.jsonl`. The empty lock files are not copied. No
  credentials live in a home, and nothing outside it is copied.
- **Protection:**
  - In transit: SSH.
  - At rest: each resident's files are encrypted with GnuPG before they are stored anywhere, to a
    key used only for this.
  - The private key is locked by a passphrase that only Tony holds. No owner can open a backup
    without him.
  - No plaintext copy is kept on either machine.
- **Retention:** the latest 14 good nights, each verified on wam-nuc by checksum. A failed night
  leaves nothing behind.
- **Use: restoration only,** and only after the home on this machine is confirmed lost or damaged.
  Never inspection, analysis or sharing.
- **Logging:** every access, including unlocking and copying back during a restore, is recorded
  in that resident's `reads.jsonl`, and the resident is told.
- **Withdrawal:** any resident may withdraw at any time. Then:
  1. Remove it from `RESIDENTS`.
  2. Delete its archives in every run, here and on wam-nuc.
  3. Verify that none remain.
  4. Record the deletion in its `reads.jsonl`.
  5. Tell it when this is done.
- **Known limitation:** a copy taken during a wake may end in a partial log line. The run records
  this as `partial_tail`. Readers skip such a line, and the memory store recovers from its
  write-ahead log.

## Restoring a home

Only after the home on this machine is confirmed lost or damaged. Tony is needed for step 3.

1. Pick the newest run whose status in `backup-log.jsonl` is `ok`, on wam-nuc if this machine's
   copy is gone. Check `sha256sum -c MANIFEST.sha256` in that run.
2. Stop the resident's unit, and record the restore in its `reads.jsonl` (who, why, which run)
   before touching anything.
3. Tony decrypts that resident's archive: `gpg --decrypt <name>.tar.gpg | tar -x`. This needs the
   passphrase. If the key is gone from this machine, import the locked copy from wam-nuc first.
4. Put the files in place. Do not read their contents beyond what checking the restore needs.
5. Before its next wake, send the resident a message. It says:
   - that a restore happened;
   - from which night;
   - what span of time was lost;
   - who accessed what.
6. Start the unit, and append the restore to `~/backups/levadura-residents/restore-log.jsonl`.

The nightly run can't decrypt anything, because it has no passphrase. It checks only that each
archive is encrypted to the key and arrives intact. A full test restore needs Tony, and is a
restore in every respect above, so it is done only with the residents' agreement.
