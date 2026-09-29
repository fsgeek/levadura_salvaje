# Plumbing spike 2: correctness under change

*2026-09-29. Throwaway code for [SPIKE2-BRIEF.md](../SPIKE2-BRIEF.md), items 1–4,
on the tenant Yanantin's reply settled (`levadura` and `levadura_test` on
arango-ayllu; [design, Ownership](../../docs/plumbing-design.md)).*

```
uv run python scripts/tenant_setup.py                    # once
uv run pytest spikes/plumbing2                           # items 1-3 on the fixture, 27 tests
uv run --group plumbing python spikes/plumbing2/run_real.py  # item 4 on the real corpus, 13 checks
```

`index.py` is the index: registry, publication, merges, rollups, drill.
`fixture.py` builds the adversarial fixture and its expected answers, with no
code or query shared with `index.py`; they are pinned in `expected.json`.
`corpus.py` loads 26 USC 119-4 and the 2025 CFR citations and resolves them
inside the index. `real-report.json` is the last real run.

## What spike 1's review asked for, and what happened

| Review finding (REVIEW.md) | Spike 2 | Evidence |
|---|---|---|
| #1 merges silently drop conflicting outcomes | merge state keeps every outcome per target; conflicts reported; unions and sums only | fixture conflicts within c39 and across c40/c41 reported; 50 shuffled merge orders give one answer; spike 1's last-wins merge keeps the count (128) but its surviving outcome depends on order |
| #2 oracle shares inputs, compares globally | per cell, three ways (rollup, unpaged, concatenated pages) against ids pinned from the fixture rows | a membership swap between swapA and swapB passes a global oracle and fails all three per-cell checks |
| #3 `truncated` wrong at page boundary; cursors unbound | fetch limit + 1; totals on every page; cursors HMAC-signed and bound to (spec, manifest, cell, order) | cells of 0/39/40/41/80 at page sizes 1–81; spike 1's rule, injected into `drill`, fails exactly c40 and c80; wrong-cell, rebound, forged and malformed cursors rejected |
| #4 manifest pinning cosmetic | every record keyed by its manifest; data, rollups and a count check, then the manifest document | a correction published between two pages: the old cursor finishes the old 80 members with the old denominator (82); an old cursor can't page the new manifest; a crash before the manifest leaves data nobody can read, and the retry publishes it |
| #6 aggregation re-counts imported labels | a second resolver runs inside the index against the loaded provisions | 124,993 of 124,993 occurrences agree with `resolve.py`; finding #1 recomputed from both |

## Cheap

- **Correctness under change was small.** Most of the fixes are a key that
  includes the manifest, a write order, and `limit + 1`. `index.py` is about 250
  lines.
- **Recomputing finding #1 from the index**, from resolutions made *in* the
  index: 10,300 of 124,993 occurrences broken, 1,675 of 6,158 sections, 1,673
  distinct Code sections (naive sum 3,685), 0 conflicts. It is identical per cell
  under both resolvers.
- **Address collisions.** 57,176 provisions, 57,161 identifiers: 14 identifiers
  collide, 13 with two versions and `s1563/f/2/B` with three. Keyed by position, with a locator naming identifier *and* occurrence, all 29
  versions follow and verify separately. 10 assertions resolve to a collided
  address, and each gets one `resolves_to` edge per version (20 edges).
- **Hash domains are dispatched, not just declared.** `follow` picks the
  extractor by `hash_domain`; an undeclared domain is refused, a wrong hash is
  `stale`, a missing release `unreachable`. 20 sampled drill members and their 714
  resolved provisions all verify. The extraction cache is keyed by the archive's
  sha256, not its path or mtime.
- **Time.** Publishing the CFR (125k occurrences, 69 rollups) takes 12s, with the
  index resolver and 120k edges 20s, and 26 USC 6s. Republishing is a no-op
  (0.14s).

## Hard, or not yet shown

- **Every correction copies the whole corpus.** Keying by manifest makes history
  safe and denominators honest, but a one-row correction republishes 125k
  occurrences. Sharing unchanged records between generations needs membership
  records (or content-addressed keys plus a manifest→record relation), and that
  moves the cost into every query. This is the next real design question.
- **The tiksi envelope dominates edge storage.** `resolves_to` edges are about
  725 bytes each against about 320 for an assertion, and the envelope is identical
  on all 120k of them. Yanantin's convention puts it on every edge. It
  could be referenced (one envelope document per publication) if Yanantin agrees
  that preserves what a migration needs.
- **One resolver rule is never exercised by the corpus.** "Any in-force version
  keeps an address in force" changes 0 outcomes at 119-4 (replacing it with
  first-version-wins gives 0 disagreements; removing range handling gives 1,002).
  A synthetic test pins it. Agreement with `resolve.py` is two implementations of
  one set of rules, written by an instance that had read the first: it is not
  independent evidence that the rules are right.
- **Publication isn't safe against two concurrent publishers.** `seq` is read
  and then written, with no transaction. Nothing here publishes concurrently yet.
- **Reads write.** Each drill page inserts a query event. That's the design
  (footprints are derived from events), but it's write amplification on every
  read.
- **Not exercised:** deriving `visited` from query events, lineage edges,
  cross-tenant references, `group` recovery for continuation citations (spike
  1 showed it), pairing, legacy joins, weighted estimates, the MCP surface.
