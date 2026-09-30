# Plumbing spike 3: corrections that don't copy the corpus

*2026-09-30. Throwaway code answering spike 2's first "Hard" item: every correction
republished the whole corpus ([spike 2 README](../plumbing2/README.md)). It builds on
spike 2's `index.py` (cursors, merges, insert-only writes) and its fixture. Reviewed
by Codex ([REVIEW.md](REVIEW.md)). This README describes the code **after** that
review's fixes; the table at the end maps each finding to what changed.*

```
uv run pytest spikes/plumbing3                                 # 16 tests on the fixture
uv run --group plumbing python spikes/plumbing3/measure.py     # the real corpus -> measure-report.json
uv run --group plumbing python spikes/plumbing3/diagnose.py    # query-plan evidence -> diagnose-report.json
```

## The design (`lineage.py`)

- **Records live in slots, keyed by generation.** A slot is a unit, an occurrence
  (`unit#i`) or an assertion (`unit#i@snapshot`). A record's key is (born, slot),
  where `born` is the generation that wrote it.
  - A child generation writes only the slots whose content changed, plus a
    *retraction* (born in the child) for every record it replaces or removes.
    Nothing is updated.
  - Content alone can't be the key. A crashed, unpublished generation would then
    own records that a later generation needs.
  - Duplicate slots in the input are refused.
- **Readers see an ancestry.** A manifest records its parent and its ancestry. A
  reader for manifest m sees records born in m's ancestry that no generation in
  it has retracted: Jabberwock's bitemporal pattern, with generations for time.
  - A retraction carries the cell of the record it retracts, so a single-cell
    read builds only that cell's retraction set.
- **Rollups.** Only cells a correction touched get new rollups. A reader takes the
  rollup from the most recent ancestor that has one. A cell that empties gets a
  zero-unit rollup, so an older rollup can't resurrect it.
- **Identity.** A generation's identity covers:
  - its content: rows, snapshot and writer `VERSION`;
  - its parent;
  - its plan: the checkpoint threshold.
  
  "Nothing changed" means identical content, so the same rows at a new snapshot
  make a new generation. A retry under a different plan is a different generation,
  and never reuses the staged writes of another plan.
- **Verification before commit.** The persisted records, compared by slot and
  content hash, and the persisted rollups are checked against what was written,
  not just counted.
- **The commit.** It is spike 2's compare-and-swap, and the parent must still be
  current. A publisher that loses the race rebases on the new current, and its
  orphaned writes stay invisible.
- **Semantics are whole-state replacement.** If two corrections race from one
  parent, the loser rebases and its rows replace the winner's, including slots only
  the winner changed. Concurrent independent patches are *not* preserved. That
  choice has to be made deliberately before this is real code.
- **Checkpoints.** Once retractions accumulated since the last root exceed 25% of
  the corpus, the next generation is a fresh root with no ancestry.
- **Paging** sorts and continues with one comparator: the unit id's UTF-8 bytes
  (`TO_HEX`), which is code-point order. Server collation and Python can no longer
  disagree.

## Correctness (16 tests)

The oracle is `fixture.expected(rows)`, plain Python over the rows each
generation intends to hold, sharing nothing with `lineage.py`. Every check
compares each cell's complete state three ways: persisted rollup, `cell_states`
(units, occurrences, broken, members, cited) and unpaged plus paged members. It
also compares the merged totals. Cells expected to have vanished must have no
state and no rollup. The tests:
- **A 20-generation random chain** (outcome flips, additions, deletions, moves,
  dropped citations), with every generation checked.
- **Cases the chain never reached:** a whole cell vanishes and returns with the
  same units; a dropped citation is restored.
- **A correction published during paging.**
- **Crashes** after the first record batch, retractions, rollups and
  verification. The parent still reads exactly, and the retry publishes.
- **Six corrections held at a barrier after computing their deltas against the
  same parent**, then committed together. At least five rebases are recorded, the
  chain has seqs 1–7, and each generation reads exactly as its rows.
- **Checkpoints.** A large correction becomes a checkpoint, and the delta after it
  is checked in full.
- **The review's findings:**
  - ids that collation and code points order differently (case, accents, a
    decomposed accent, digits, punctuation) page without loss at limits 1–5;
  - the same rows at a new snapshot make a new generation;
  - a retry under a changed plan works, and a disabled threshold is stored.
- **Mutants.** Ignoring retractions is caught, and so is reading the oldest rollup
  instead of the newest.

## The real corpus (`measure-report.json`, one run)

- **Writes are delta-sized.**
  - The first publish takes 12s.
  - Corrections of 1, 100 and 5,000 changed citations each write exactly n
    assertions, n retractions, and rollups for the touched cells.
  - Each takes 3–5s. The time goes to reading the parent's whole view in order to
    compute the delta. `measure.py` doesn't break that time down further.
  - A 60k-citation delta takes 12s. The checkpoint after it takes 17s.
- **Every generation matches the oracle's complete per-cell state and merged
  totals** (all 42). The persisted rollups and pages were also checked for 6 cells
  at the first, middle and last generation.
- **Records.** 42 generations hold 315,355 assertions, where full copies would hold
  5,247,774. Storage statistics are per collection, and the spike 2 collections
  also hold earlier runs' baselines, so compare record counts, not bytes.
- **Reads, for the largest cell (part 1) and `cell_states` over all 69 cells.**
  Timings from one run. The full copy's own drill varied 36–47 ms across runs, so
  read ratios as roughly ±25%.

| state | full copy of the same rows: drill / unpaged / all states | lineage: drill / unpaged / all states | ratio |
|---|---|---|---|
| depth 4 | 47 ms / 53 ms / 0.44 s | 91 ms / 73 ms / 1.01 s | 1.9× / 1.4× / 2.3× |
| depth 40 | 46 ms / 52 ms / 0.37 s | 101 ms / 83 ms / 1.11 s | 2.2× / 1.6× / 3.0× |
| after a 60k delta | 101 ms / 117 ms / 0.46 s | 468 ms / 378 ms / 1.98 s | 4.6× / 3.2× / 4.3× |
| the checkpoint after it | *baseline ≈ the row above; the checkpoint changed 10 more citations* | 171 ms / 182 ms / 1.38 s | ≈1.7× / 1.6× / 3.0× |

## What this says

- **Small corrections are cheap to write, reads are 1.4–3.0× slower, and depth
  matters little.** From depth 4 to depth 40, 36 more generations add 10–13%.
- **A mass change costs reads 3–4.6×** against the same data. A checkpoint brings
  drill and unpaged back to 1.6–1.7×. The policy "delta if small, checkpoint if
  large" holds up. The 25% threshold is a guess this data didn't test.
- **`cell_states` over all cells stays about 3× slower, even at a checkpoint.**
  There are no retractions there, which rules them out. `measure.py` and
  `diagnose.py` don't identify the remaining cost. The stream's collections do
  hold every generation's records (103k + 103k + 50k + … for part 1 alone,
  `diagnose-report.json`), but that is a suspect, not a finding.

## Two wrong diagnoses, recorded

The profiler caught both, and no review did. `diagnose.py` reproduces the evidence.
1. **"The retraction set grows."** After the 60k delta I blamed the per-query set
   of every retraction in the ancestry, and tried an indexed per-record probe. The
   probe is 18× *slower* (6.94 s against 0.39 s for `unpaged`), because the cell
   holds every version of its records, and a subquery per version costs more than
   one set. Scoping the set to the cell helped little. A checkpoint with *zero*
   retractions was still slow, so the set wasn't the main cost.
2. **"Dead versions are scanned."** Indexes that include `born` helped (kept), but
   the checkpoint stayed slow. The query plan settled it:

| part 1, member query | members | index entries scanned |
|---|---|---|
| before the mass correction | 2,200 | 17,277 |
| after the 60k delta | 3,267 | 110,551 |
| at the checkpoint | 3,267 | 50,100 |

My random correction had flipped enough in-force outcomes to repealed that part 1's
broken assertions roughly tripled. **The answer had grown**, and I had been comparing
against a full copy of the *original* rows. With a baseline of the same rows, both
effects show:
- the data effect: 17k → 50k entries, and the full copy slows too;
- the layout effect: 50k → 110k entries after the delta, removed by the checkpoint.

## Not done, and needed before this is real code

- **Edges (`resolves_to`).** They would follow the same rule, retracted with their
  assertion.
- **Deltas supplied by the caller**, instead of being computed from a full read of
  the parent.
- **A deliberate choice between whole-state replacement and patch merging.**
- **Archiving generations older than the last checkpoint**, while keeping them
  readable for old manifests and cursors.
- **Tests of crashes *inside* a batch, and of durability.**
- **Phase timings and query plans for every reader**, before choosing indexes or
  the checkpoint threshold.

## Review findings → changes

| # | Finding | Change | Evidence |
|---|---|---|---|
| 1 HIGH | paging sorted in AQL, continued in Python | one comparator (UTF-8 bytes via `TO_HEX`) for both | `test_paging_order_is_one_comparator` |
| 2 HIGH | "no change" ignored the snapshot | identity = rows + snapshot + writer `VERSION` | `test_same_rows_new_snapshot_is_a_new_generation` |
| 3 | a retry under another checkpoint plan reuses staged writes; counts-only verification | plan (threshold) in identity; persisted slots, hashes and rollups verified before commit | `test_retry_under_a_changed_plan…` |
| 4 | duplicate slots collapse silently | refused | `test_duplicate_units_are_refused` |
| 5 | "rebase" silently replaces concurrent independent edits | documented as whole-state replacement; a choice required before real code | docstring, above |
| 6 | chain never empties/restores; checks compare members only; race may run serially; checkpoint follow-up unchecked | complete state and vanished cells checked; vanish/return test; barrier forces the race (≥5 rebases asserted); crash after the first batch; follow-up checked | tests above |
| 7 | the real-corpus verify compared members only | complete per-cell state and merged totals, for every generation | `measure-report.json` checks |
| 8 | ratios and causes overstated; profile evidence not in artifacts | ratios per reader; approximate checkpoint baseline marked; residual cause called a suspect; `diagnose.py` reproduces the plans | `diagnose-report.json` |

Two bugs came from my own fixes and were caught by the new tests:
- A loop variable shadowed the new `content` identity, so "no change" was never
  recognized. The re-publish assertion caught it at once.
- An infinite threshold (checkpoints disabled) wasn't valid JSON in the manifest.
  `measure.py` failed on it, and a test now covers it.
