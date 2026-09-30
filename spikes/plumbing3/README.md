# Plumbing spike 3: corrections that don't copy the corpus

*2026-09-30. Throwaway code answering spike 2's first "Hard" item: every correction
republished the whole corpus ([spike 2 README](../plumbing2/README.md)). This one
builds on spike 2's `index.py` (cursors, merges, insert-only writes) and its fixture.*

```
uv run pytest spikes/plumbing3                                 # 11 tests on the fixture
uv run --group plumbing python spikes/plumbing3/measure.py     # the real corpus; writes measure-report.json
```

## The design (`lineage.py`)

- **Records live in slots, keyed by generation.** A slot is a unit, an occurrence
  (`unit#i`) or an assertion (`unit#i@snapshot`). A record's key is (born, slot),
  where `born` is the generation that wrote it.
  - A child generation writes only the slots whose content changed.
  - For every record a child replaces or removes, it writes a *retraction*, also
    born in the child. Nothing is ever updated.
- **Why content alone can't be the key.** A crashed, never-published generation
  would then own records that a later generation needs. With insert-only writes,
  the later generation would silently inherit an invisible record.
- **Readers see an ancestry.** A manifest records its parent and its whole
  ancestry. A reader for manifest m sees records born in m's ancestry that no
  generation in the ancestry has retracted. This is the bitemporal pattern of
  Yanantin's Jabberwock aliases, with generations standing in for time.
  - A retraction carries the cell of the record it retracts, so a read of one
    cell builds only that cell's retraction set.
- **Rollups are rewritten only for cells a correction touched.** A reader takes
  the rollup from the most recent ancestor that has one.
- **The commit is spike 2's compare-and-swap, plus one rule: the parent must still
  be current.** A publisher that loses the race rebases on the new current. Its
  orphaned writes stay invisible, because no committed ancestry contains them.
- **Checkpoints.** Once the retractions accumulated since the last root exceed 25%
  of the corpus, the next generation is a checkpoint: a fresh root with no
  ancestry that rewrites every slot.

## Correctness (11 tests)

The oracle is `fixture.expected(rows)`, plain Python over the rows each
generation *intends* to hold. It shares nothing with `lineage.py`. The tests:
- **20 generations of random corrections**, each generation checked in every
  cell three ways, plus the merged top. The corrections flip outcomes, add
  units, delete units, move units between cells and drop citations.
- **A correction published while a reader is paging.**
- **A crash after each of four stages.** The parent still reads exactly, and a
  retry publishes.
- **Six corrections racing from one parent.** All six commit with rebases, the
  chain has seqs 1–7, and each generation reads exactly as the rows it intended.
- **A large correction becomes a checkpoint.** The older generations are
  unchanged, and later deltas resume on the new root.
- **Mutants.** Ignoring retractions is caught, and so is reading the oldest
  rollup instead of the newest.

## The real corpus (`measure-report.json`)

- **Correction cost.**
  - The first publish takes 11s.
  - Corrections of 1, 100 and 5,000 changed citations each write exactly their
    delta: n assertions, n retractions, and rollups for the touched cells only.
  - Each correction takes 3–5s regardless of size. The time goes to reading the
    parent's whole view to compute the delta. A caller that supplied the delta
    itself would avoid that.
  - A 60k-citation correction takes 11s. A checkpoint takes 15s.
- **Storage.** 42 generations hold 315k assertions. Full copies would hold 5.2M.
- **Every generation matches the oracle**, in all cells and the merged top. Rollups
  and pages were also checked for 6 cells at the first, middle and last generation.
- **Reads, against a full copy of *the same rows***, for the largest cell (part 1)
  and for `cell_states` over all 69 cells:

| state | full copy: drill / unpaged / all states | lineage: drill / unpaged / all states |
|---|---|---|
| small corrections, depth 4 | 36 ms / 43 ms / 0.33 s | 78 ms / 50 ms / 0.84 s |
| small corrections, depth 40 | 36 ms / 41 ms / 0.33 s | 88 ms / 61 ms / 0.95 s |
| after a 60k-citation delta | 108 ms / 136 ms / 0.44 s | 424 ms / 302 ms / 1.77 s |
| the checkpoint after it | (same rows) | 142 ms / 126 ms / 1.11 s |

## What this says

- **Small corrections: cheap to write, nearly flat with depth, and 1.2–2.9× slower
  to read** (unpaged 1.2×, drill 2.2×, all states 2.5× at depth 4). Depth matters
  little: 36 more generations of small corrections add 13–22%.
- **A mass change costs reads about 4×** against the same data, until a checkpoint
  brings drill and unpaged back near parity. The policy "delta if small, checkpoint
  if large" holds up. A 25% threshold is a guess that this data didn't test.
- **`cell_states` over all cells stays 2.5× slower even after a checkpoint.** A
  checkpoint has no retractions, so the overhead is scanning a stream that holds
  every generation's records. Keeping each stream's records in their own
  collection, or archiving generations older than the last checkpoint, would
  address it. Not tried.

## Two wrong diagnoses, recorded

The first two explanations of the slow reads were wrong. The profiler caught the
error, and no review did.
1. **"The retraction set grows."** After the 60k delta, I blamed building a set of
   every retraction in the ancestry, and tried an indexed per-record probe instead.
   The probe was 17× *worse*: the cell holds every version of its records, and a
   subquery for each one costs more than one set. I then scoped retractions to
   the cell. That helped little, and a checkpoint with *zero* retractions was
   still slow. So the set wasn't the main cost.
2. **"Dead versions are scanned."** Indexes that include `born` cut the
   checkpoint's drill from 365 to 218 ms (kept), but didn't restore it. Profiling
   the query showed 50,100 index entries scanned: part 1 holds 103k assertions,
   and my random correction had flipped enough in-force outcomes to repealed that
   its broken share rose from about 10k to about 50k. **The answer had grown, and
   I was comparing against a full copy of the *original* rows.** The fix was a
   baseline of the same rows at every read point, which produced the table
   above. Both effects turned out to be real, and the first run's comparison
   couldn't separate them.

## Not done

- **Edges (`resolves_to`).** They would follow the same rule, retracted with their
  assertion, but aren't implemented here.
- **Deltas supplied by the caller**, instead of being computed from a full read of
  the parent.
- **Archiving generations older than the last checkpoint.**
- **Paging.** `drill` computes the cell's member list, then slices it. It is
  correct but not keyset-efficient.
