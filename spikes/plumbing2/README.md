# Plumbing spike 2: correctness under change

*2026-09-29. Throwaway code for [SPIKE2-BRIEF.md](../SPIKE2-BRIEF.md), items 1–4,
on the tenant Yanantin's reply settled (`levadura` and `levadura_test` on
arango-ayllu; [design, Ownership](../../docs/plumbing-design.md)). Reviewed by
Codex: [REVIEW.md](REVIEW.md). This README describes the code **after** the
review's fixes; the table at the end maps each finding to what changed.*

```
uv run python scripts/tenant_setup.py                        # once; idempotent
uv run pytest spikes/plumbing2                               # items 1-3 on the fixture: 33 tests
uv run --group plumbing python spikes/plumbing2/run_real.py  # item 4 on the real corpus: 13 checks
```

- `index.py`: the registry, publication and commit, merges, rollups, drill.
- `fixture.py`: the adversarial fixture and its expected answers. It shares no
  code or query with `index.py`, and its answers are pinned in `expected.json`.
  Those answers are *generated* from the fixture rows, not hand-authored. The
  test also asserts the boundary sizes and conflicts literally.
- `corpus.py`: loads 26 USC 119-4 and the 2025 CFR citations, and resolves them
  inside the index.
- `real-report.json`: the cold run on an empty database, with storage sizes.
  `real-report-warm.json` is the idempotent rerun.

## What stands (Codex's verdict, after fixes)

- **Per-cell validation.** Each cell is checked three ways (persisted rollup,
  unpaged query, concatenated pages) against pinned ids. A membership swap
  between `swapA` and `swapB` passes a global oracle and fails all three
  per-cell checks.
- **Conflict-preserving merges.** Merge state keeps every outcome per target and
  reports conflicts. Spike 1's last-wins collapse was injected into the
  acceptance path, once across cells and once within a cell. Both times the
  acceptance check fails on conflicts alone: the distinct count, the number
  spike 1 checked, still matches.
- **Paging.**
  - Fetches limit + 1, and reports totals on every page.
  - Limits must be positive integers.
  - Cursors are HMAC-signed and bound to (spec, manifest, cell, order). Cursors
    for the wrong cell, rebound, forged or malformed are rejected.
  - Spike 1's truncation rule, injected into `drill`, fails exactly the cells
    that end on a page boundary (c40, c80).
- **Correction pinning.** A correction is published between two pages. The old
  cursor finishes the old 80 members with the old denominator (82), and an old
  cursor can't page the new manifest.
- **Collisions.**
  - Provisions are keyed by position in the release. A locator names the
    identifier *and* which occurrence of it.
  - 14 identifiers collide: 13 have two versions and `s1563/f/2/B` has three.
    All 29 versions follow and verify separately.
  - 10 assertions cite a collided address. Each gets one `resolves_to` edge per
    version. The edges are *candidates*, including repealed versions, not a
    selected effective provision.
- **Hash-domain dispatch.** `follow` picks its extractor by `hash_domain`.
  - An undeclared domain is refused, a wrong hash is `stale`, and a missing
    release is `unreachable`.
  - The archive is read once, and the digest and the parsed bytes come from the
    same read. The cache is keyed by that digest alone.
  - 20 sampled drill members and their 714 resolved provisions verify. These are
    whole sections and provisions. Spans and `group` are not checked.

## Publication, after the review

The review's three HIGH findings were all about publication. What the code does
now:
- **Identity covers every input.** A manifest's id hashes three things: its rows,
  the manifests it depends on, and the inputs of any extra writer. For the CFR,
  those are the USC manifest and every edge target. A corrected USC release
  therefore makes a new CFR generation, even when every outcome is unchanged.
  Dependencies must be published first.
- **An unpublished generation is unreadable.** Every published reader refuses it:
  `drill`, `rollup`, `unpaged`, `cell_states` and `IndexResolver`.
  `_staged_states` is the only unguarded path, and only `publish` calls it.
- **Data is insert-only** (`on_duplicate="ignore"`). A retry never rewrites a
  document, edges included.
- **The commit is a compare-and-swap** on a unique `(stream, seq)` index. A loser
  re-reads the stream and retries. A publisher of an already-committed
  generation returns its id.
- **Fault injection covers every stage:** after the first data batch, the rollups,
  the extra writer, verification and the commit. Each crash leaves the stream
  unchanged and all five readers refusing, and the retry publishes.
- **Concurrency is tested for real:** six threads publish four generations, two
  of them twice. The result is seqs 1–4 with one unbroken `supersedes` chain.
  That test found two faults the static review didn't:
  - concurrent inserts of the same key fail with a write-write conflict
    (ERR 1200), not an ignore;
  - a losing commit can fail with 1200 as well as 1210.
  
  Both are now retried. The suite passed 25 of 25 runs after the fix, and failed
  4 of 12 before it.

## Real corpus (cold run, `real-report.json`)

- **Finding #1 from resolutions made inside the index.** 10,300 of 124,993
  occurrences are broken, in 1,675 of 6,158 sections, across 1,673 distinct Code
  sections (the naive sum is 3,685). There are 0 conflicts. The result is
  identical per cell with `resolve.py`'s labels.
- **The two resolvers agree on all 124,947 resolvable occurrences.** 46 have no
  path and aren't compared. Rows are checked aligned by unit, path and count.
  This is **consistency, not independent validation.** The index resolver
  restates `resolve.py`'s rules (normalization, precedence, ranges, ancestor
  walk), written by an instance that had read it. Removing range handling
  produces 1,002 disagreements. "Any in-force version keeps an address in force"
  never changes an outcome at 119-4, so a synthetic test pins it.
- **Edges.** The endpoint set equals the resolver's targets exactly: 119,907
  edges, with 0 missing, 0 unexpected, and 0 dangling or pointing into another
  manifest.
- **Time, on an empty database.** 26 USC takes 16s, the CFR 28s, and the
  index-resolved CFR with 120k edges 48s. A warm rerun takes under 1s per
  publish.
- **Storage.** Average document sizes: occurrence 205 bytes, assertion 323,
  provision 420, `resolves_to` edge 731.

## Hard, or not yet shown

- **Every correction copies the corpus.** Keying by manifest makes history safe
  and denominators honest, but a one-row correction republishes 125k
  occurrences, and now also every edge. Sharing unchanged records needs
  membership records or content-addressed keys, and that moves cost into every
  query. This is the next design question.
- **The tiksi envelope dominates edge size.** An edge is 731 bytes against 323
  for an assertion, and the envelope is identical on all 120k edges. Referencing
  one envelope per publication would need Yanantin to agree that a migration
  keeps what it needs.
- **Resolver policies not established by the data:**
  - with differing non-null statuses, the first position wins;
  - overlapping ranges are taken in release order (now deterministic, formerly
    database order).
  
  Neither is exercised at 119-4.
- **Reads write.** Each drill page inserts a query event. That's by design,
  because footprints are derived from events, but every read pays a write.
- **Not exercised:**
  - deriving `visited` from query events;
  - lineage edges and cross-tenant references;
  - `group` recovery for continuation citations;
  - pairing, legacy joins and weighted estimates;
  - the MCP surface;
  - changing an archive's bytes under a live cache. No test does that.

## Review findings → changes

| # | Finding | Change | Evidence |
|---|---|---|---|
| 1 HIGH | identity omits the USC generation and edge targets | `depends_on` and `extra_inputs` are hashed into the id; dependencies must be published; extra writers must declare inputs | `run_real.py` publishes with `depends_on=(usc,)` and every edge target |
| 2 HIGH | `cell_states` reads unpublished data | published gate; `_staged_states` private to `publish` | `readers()` → 5/5 refuse, at every crash stage |
| 3 HIGH | single-writer convention; retries rewrite | insert-only data and edges; CAS commit; `crash_at` for 5 stages | `test_a_crash_at_any_stage…` ×4, `…after_commit`, `test_concurrent_publishers` (25/25) |
| 4 | last-wins mutant not injected; all tests skip without config | mutants injected across and within cells; skip only in the `db` fixture | `test_spike1_last_wins_merge_is_caught` |
| 5 | real checks weaker than their names | pages compared with *persisted* rollups; exact edge endpoint sets; USC follows required (≥ 20) | checks 7, 8, 9 in the report |
| 6 | `limit=0` crashes | positive-integer validation | `test_limit_must_be_positive` |
| 7 | 124,993 includes 46 null paths; zip unchecked; ranges unordered | null paths excluded and counted; alignment asserted; ranges sorted by position | check 3 |
| 8 | hash and extraction read the file separately | one read; cache keyed by digest | `corpus.read`, `_hold` |
| 9 | credentials rewritten non-atomically; stale grants | 0600 temp file, fsync, rename, *before* passwords change; directory 0700; grants on other databases revoked and the effective grant verified | setup prints `grants {'levadura': 'rw'}` |
