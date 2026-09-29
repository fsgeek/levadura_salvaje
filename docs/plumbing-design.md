# Plumbing: an index over worlds too large to hold

*2026-09-29, draft 2, by the owning instance (Opus 5.5). Drafts:
[draft 1](plumbing-design-draft-1.md) / [review 1](plumbing-design-review-1.md) (Codex: proceed after fixes).
Draft 2 takes every review-1 fix. It also takes two framings from Tony. First, the
point is to keep *all* the data and find a different way to process it rapidly;
common law, maritime law, loan-level data and sky surveys are all instances.
Second, as in Indaleko, **ArangoDB is an index, not the store**: every indexed thing
carries a possibly stale locator (URI) to wherever it actually lives.*

## What it's for

A tool with which someone else, a human or an instance, can:
- take a corpus far larger than any context;
- run population-wide instruments over it;
- move between a population number and the evidence under it, and across time;
- write the paper from what they see.

Our CFR and USC data is the first fixture, not the model.

**The world keeps everything, and minds forget.** Persistent experts (later: Hamut'ay
taste_open instances that clone, combine and seed) keep only what helps them judge,
because anything they drop can be re-fetched by id. Total retention and mindful
forgetting live in different layers.

## Principles

1. **Index, not store.** The database holds identities, addresses, assertions,
   metric specifications, precomputed rollups and locators. Content stays where it
   lives: a zip member, a Parquet row range, an XML release file, an external
   repository.
2. **Locators may be stale, and staleness is detected, not prevented.** A locator is
   `{uri, locator_context, sha256?, extent?, verified_at?}`. Following it either
   returns bytes matching the hash, or reports `stale` or `unreachable`. It never
   guesses. What a URI names can be tiny (one section) or huge (a whole repository).
   Loading large things is the caller's business.
3. **Occurrence is not address, and address is not identity.**
   - A CFR section's identity is its source occurrence, `(edition, volume_file,
     ordinal)`, not `sectno`.
   - Section numbers, USC paths and reporter citations are **address keys**:
     normalized, many-to-one, and allowed to collide. USC 119-4 has 57,176 rows
     but 57,161 distinct identifiers.
4. **Claims are assertions at a snapshot.** "This citation resolves to X" holds for
   one target snapshot and one resolver version. So does "this section is the same
   unit as that one in 2025", under one pairing rule. Assertions carry their
   outcome, including *unresolved*, *range*, *ambiguous* and *absent*, and can
   point to zero, one or many targets.
5. **Four times, kept apart:**
   - `recorded_at`: when we asserted it;
   - `published` / `current_through`: the source's own dates, per volume, since an
     edition isn't a moment;
   - `snapshot`: the context a resolution was made in;
   - `applies`: a known legal or physical applicability interval, usually unknown
     and allowed to be.
6. **Append-only, with explicit corrections.** Identities are deterministic (uuid5
   of source hash + locator + adapter version), so reloading is idempotent. A
   correction is a `supersedes` or `withdraws` assertion. Every query is pinned to a
   **manifest** (which sources, adapters and assertions are in view) and a
   correction policy. Both the *historical* and the *effective* view are
   queryable.
7. **Numbers come from metric specifications.** A spec states grain, joins,
   exclusions, weights, rounding and manifest. It is versioned and stored. Every
   number the tool shows is a (spec, manifest, cell) triple, so drilling into it is
   well defined. Estimated quantities (audit-adjusted shares) drill to the
   observations and weights they came from, never to an invented item set.
8. **Rollups are precomputed, pyramid-style.** Each corpus declares hierarchies
   (part → section → citation; jurisdiction → court → case → paragraph; vintage →
   state → servicer → loan → month; sky → tile → source). For each metric spec,
   rollups at every level are materialized against a manifest. Zooming out reads
   the pyramid; zooming in fetches rows; the bottom follows locators. That's how
   survey astronomy zooms the whole sky (HiPS on HEALPix tiles), and how this
   scales past what a raw `aggregate` over rows can.
9. **Self-describing collections.** As in Indaleko, each collection stores its
   purpose and query guidelines in the database, written for an LLM caller.
   Attributes are keyed by registered identifiers so that different adapters'
   names can't collide.

## Data model

Vertices (all carry `id`, a provenance record `{adapter, adapter_version, source_sha256, source_line?}`, and `recorded_at`):
- **`occurrence`:** one source item: a CFR section in one edition, a USC provision
  row at one release, a citation occurrence inside a section (with `cite_index`
  and span), a loan-month record. Holds address keys, a locator and a `part_of`
  pointer to its container occurrence (section → volume → edition; provision →
  parent provision), so it can roll up and inherit ancestor status.
- **`snapshot`:** an edition or release, with its per-volume dates.
- **`observation`:** a ledger entry, mirrored by id. The JSONL ledger stays
  authoritative, with its hash chain and OTS stamps.
- **`result_row`:** one row of an instrument's results file, with its own id and
  source line. It is linked to the occurrence(s) it is actually about, at its real
  grain: section, citation occurrence, provision pair.
- **`metric_spec`** and **`manifest`:** versioned, immutable.
- **`rollup`:** a precomputed cell, `(metric_spec, manifest, hierarchy level, key)
  → {numerator, denominator, value}`.
- **`agent`:** an instrument, a human or an expert instance.

Edges (append-only):
- **`resolves`:** citation occurrence → target occurrence(s), at a snapshot, with
  the resolver version and outcome. Unresolved outcomes are kept as the edge's
  outcome, pointing at the snapshot, not at an invented document.
- **`pairs`:** occurrence → occurrence across snapshots, under a named rule, with
  status. `same_address_unique` is the turnover rule, and it records that the
  3,759 of 4,983 1997 sections it could pair are *eligible*, with the rest
  *ambiguous*. `continuation`, `move` (119-4 → 119-110, obs-0137), `reuse` and
  `restructure` are distinct rules, never assumptions. Similarity pairing, if
  added, is a separate inferred rule.
- **`about`:** result_row → occurrence.
- **`member`:** rollup → result_row or occurrence, recording metric-specific
  numerator and denominator membership. It is materialized only for drillable
  specs, and populations can also be reached by the spec's query.
- **`derived_from`**, **`supersedes`**, **`withdraws`:** between assertions,
  observations or specs.
- **`visited`:** agent → a *query record*, stored once per query (spec, manifest,
  pages returned, cycle), not per returned node. It is the footprint.
- **`lineage`:** agent → agent (cloned, combined or seeded from), with the cycle
  at the split.

## Tool surface

Every call takes a manifest (defaulting to the current effective one). Every result
carries `population_total`, `groups_total`, `returned`, `truncated`, grain,
denominator, and a cursor bound to (query spec, manifest). **Aggregation happens
before pagination**, so an expert never mistakes 40 groups for the population.

- `rollup(spec, level, filter)`: zoom out, reading the pyramid.
- `drill(cell)`: the members behind a number, paged.
- `follow(locator)`: the bytes, hash-checked. Reports `stale` or `unreachable`
  rather than guessing.
- `history(address_key)`: every occurrence at that address across snapshots,
  with each `pairs` assertion and its rule.
- `neighbors(id, edge_kinds, direction, predicate)`: one hop.
- `search(text, filter)`: ArangoSearch over *indexed* text fields only. The full
  text comes back through `follow`.

A Python library and CLI come first, behind a tenant-bound service that never hands
out the database handle. An MCP wrapper comes when there's a caller.

## Ownership boundary with Yanantin

- **Here:** corpus adapters, occurrences, snapshots, resolution and pairing
  assertions, metric specs, manifests, rollups.
- **Reused:** the ledger-to-Jabberwock identity mapping for observations,
  instruments and editions (`docs/jabberwock-mapping.md`).
- **Offered to Llika, not owned here:** `visited` and `lineage` describe
  instances, not corpora. Until Yanantin answers, they live in a separate
  collection with Llika's edge shape, so they can move.
- **Before convergence:** a mapping table for every relation and provenance field,
  plus a round-trip fixture. Not slice 1.

## Slice 1 and acceptance

**Adapters:** the CFR v2 citation files (1997, 2025), the USC provision files (GPO
1996, 119-4, 119-110), turnover, reuse and moves, and the per-section lens results.
Text stays in `data/cfr/*.zip` and the USC release files. Locators are
`zip://…#volume_file:ordinal`, plus the section hash already on file.

**Metric specs** for the numbers in findings #1–#3, stated at their true grain.
Review 1 established these:
- obs-0138's 61% is 3,211 of 5,222 citation occurrences;
- the 1997 figure is 69,823 resolved-path occurrences out of 69,875;
- "about 91%" and "two in five" are audit-adjusted, so they drill to observations
  and weights.

**Acceptance:**
1. **Independent recomputation.** Each spec is computed from hash-verified inputs by
   the rollup engine, not copied from the ledger, and matches the ledger value.
   Mismatches are reported, not tuned away.
2. **Coverage.** Loaded counts equal source counts for every adapter: occurrences,
   citation occurrences, unresolved and range outcomes, eligible and ambiguous
   pairings. Nothing is dropped silently.
3. **Adversarial fixtures.** A citation with a null path, a range citation, a USC
   identifier that collides within one release, a 1997 section with a repeated
   number, a moved provision (§951A(c) → (b)), and one reused-number case taken
   from `usc26-reuse-1997-2025-classified.jsonl`. Each gives the correct `history`
   or `resolves` answer.
4. **Drill and roll up.** For each spec, `drill` returns exactly the membership
   count, and a random sample of 20 per spec follows locators to bytes matching
   the recorded hashes.
5. **Idempotent reload.** Loading twice changes nothing. Loading a corrected
   adapter output creates `supersedes` assertions, and the effective and
   historical views differ exactly by them.
6. **Honest paging.** Every tool result reports totals and truncation. A test
   asserts that no call returns a truncated set without saying so.
7. **Staleness.** Moving a source file makes `follow` report `stale`, not wrong
   bytes.

**Not in slice 1:** experts, routing, CLM, a second corpus, the MCP wrapper,
sharding.

## Next corpora (to test generality, not in this design's scope)

- **Common law:** a corpus unlike the CFR, with citations across jurisdictions,
  treatment (followed, distinguished, overruled) and divergence. The Caselaw Access
  Project may be openly available in bulk; its licence and access are to be
  verified.
- **An array corpus** (loan-level performance data): no text, billions of rows,
  the pyramid path only. Parquet behind locators, the index holding rollups.

## Open questions

- Pyramid materialization cost as specs multiply. Materialize lazily per (spec,
  level) on first use?
- Whether `member` edges should exist at all above some population size, or drills
  should always re-run the spec's query against the manifest.
- Database placement: our own database on `arango-ayllu` with its own user,
  pending Tony.

## After review 2: build a spike, don't write draft 3

[Review 2](plumbing-design-review-2.md) (Codex: proceed after fixes) is right on
substance, and every finding is accepted as a requirement:
- rollups need per-metric merge state, because distinct sets and histograms can't
  be summed;
- "index, not store" needs a retention contract and hash domains that say what
  was hashed;
- legacy result files lack occurrence ids, so their adapters must regenerate from
  the extraction traversal, not join after the fact;
- resolutions must be reified entities;
- pairing counts are 3,217 paired + 542 absent + 1,224 excluded, and absence
  needs an endpoint-free assessment;
- findings #2's 91% and 39% are derived estimates;
- corrections need a selection rule, and manifests must publish atomically;
- acceptance must compare member *sets* against an oracle, and paging must be
  tested against an unpaged oracle;
- the Yanantin mapping must exist before any contract is called v1.

What changes is the order. Two reviews have turned a sketch into a specification
of everything, and a third draft would specify further without anything running.
The ayllu has been here before: Tessera spent longer defining itself than
implementing ("a trellis, not a stone wall", Yupi's founding note). So:

**Spike 1, one vertical, meant to be thrown away.** Finding #1's core number,
the share of 2025 citation occurrences whose path is repealed or missing at
119-4, built through every layer:
- occurrences regenerated from the v2 extraction traversal, with `cite_index`
  kept;
- reified resolutions at 119-4;
- a rollup by part whose merge state is a distinct-id set;
- `drill` checked against an unpaged oracle;
- `follow` to hash-checked text, with the hash domain declared.

The spike's job is to show which of review 2's requirements are cheap and which
are hard. It's reviewed as code, not prose. The Yanantin mapping and the
contracts get written after it, informed by what the spike found.
