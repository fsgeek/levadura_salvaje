# The ledger as a Jabberwock client

*2026-09-22. Levadura is Yanantin's third demonstration, after Qhaway and
llm-memory. The ledger's model was reinvented here before anyone noticed
that Yanantin's Jabberwock already had it. This note maps one onto the other,
and records what the first real client found.*

## Mapping

| Ledger | Jabberwock |
|---|---|
| entry | **Vorpal**: `tulgey` = quantity, `id` = uuid5 of the ledger id |
| `recorded_at` | `Vorpal.brillig` (event time) |
| `observed_at` | `gyre_from` (world time), carried as an *extra field* (see gap 1) |
| `instrument` | **Bandersnatch**, a Jabberwock with a Tove in `levadura.instrument` |
| population (a volume, a log) | **Jabberwock** with Toves in `levadura.source` and `sha256` |
| CFR edition | **Borogove**; each volume joins it by a **Rath** whose `gyre_from` is that volume's own date |
| `coverage_gap`, `open_question` | kept inside the Vorpal for now; candidates for **mome** Vorpals |
| edition totals | a **Frabjous**, a fold that is never stored |

Because instruments are entities, calibration becomes ordinary data: an
audited miss rate is a Vorpal *about the instrument*. That is the main reason
to adopt this before the first Jev lens.

## Result

`scripts/jabberwock_roundtrip.py` writes all ledger entries into a
DuckDB-backed store, reads each one back through the Frabjous fold, and
requires identical canonical JSON. **45/45 identical, 0 records skipped.**
Both editions come back as Borogoves with their mixed volume dates
(1997: 1990 and 1997; 2025: 2020, 2024 and 2025).

The JSONL ledger stays authoritative for now. Its hash chain and the OTS
stamps are the tamper evidence that the activity stream doesn't have yet.

## Gaps found by a real client

181 Jabberwock unit tests pass, and none of them exercises the following:

1. **A Vorpal has no world time.** The spec insists that `brillig` (event
   time) and `gyre` (world time) must never be confused, but the
   observation record only has `brillig`. "Elder's state was 55,389 tokens
   on May 8" has no first-class place for May 8. It works as an extra field;
   it should be part of the model.
2. **There is no public backfill path.** `outgrabe` always sets
   `brillig = now`, so historical observations can't be imported with their
   true event time. The spike writes through `store.store_fact` using
   Jabberwock's public models and provider constants, but reaches through
   `Brillig._store` to do it.
3. **The default normalizer lowercases.** That is right for handles
   (`FsGeek` → `fsgeek`) and lossy for URLs and file names
   (`CFR-2025-title-26.zip`). `register_normalizer` solves it, but it is a
   process-wide registry, so one client's choice changes another's.
4. **The activity stream has no tamper evidence.** There is no hash chain on
   stored facts. Levadura keeps its JSONL chain and OTS stamps until that
   exists.

Also found, but not a code problem: Yanantin's local `.venv` has lost its
packages (`No module named 'pydantic'`); in a clean isolated environment,
all tests pass.
