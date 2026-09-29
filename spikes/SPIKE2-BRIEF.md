# Brief for plumbing spike 2

*Written 2026-09-29 by the owner who built spike 1, for whoever builds spike 2
(possibly a new owner). Read first: [docs/plumbing-design.md](../docs/plumbing-design.md),
[review 2](../docs/plumbing-design-review-2.md), [spike 1 README](plumbing1/README.md)
and [its review](plumbing1/REVIEW.md).*

*Status 2026-09-29: items 1–4 built in [plumbing2](plumbing2/README.md) and reviewed ([REVIEW.md](plumbing2/REVIEW.md)); the review's findings are fixed there.*

## Order: correctness under change before breadth or scale

Codex's spike-1 review is explicit: these tests come before more corpus breadth or
any bitmap optimization.

1. **A tiny adversarial fixture**, hand-built, with expected ids pinned per cell:
   - conflicting outcomes for the same Code section, within one part and across
     parts;
   - memberships deliberately swapped between cells;
   - exact page boundaries: cells of 0, 39, 40, 41 and 80 members.

   Merges must be order-independent or must reject conflicts explicitly. Every
   cell's rollup, its unpaged query and its concatenated pages are compared,
   *separately*, against the pinned ids.
2. **Honest paging.** Fetch `limit + 1` to decide `truncated`. Cursors are opaque
   and bound to (spec, manifest, cell, order); a cursor presented for the wrong
   cell or manifest is rejected. Every page reports totals.
3. **Manifests that are really pinned.** Assertion keys include the manifest or
   extraction generation, so a corrected import adds rather than overwrites.
   Publish a corrected manifest *while* a drill is paging, and prove the old
   manifest still returns its original members and denominators. Publication is
   atomic: data first, then the manifest.
4. **Only then:** resolve citations to the loaded USC provisions, exercising
   address collisions (57,176 rows, 57,161 identifiers at 119-4) and multiple
   targets. Follow USC text with its own declared hash domain.

## Out of scope for spike 2

A second corpus, scale, the MCP wrapper and the Yanantin mapping. The mapping
comes before any contract is called v1.

## Facts already established (don't re-derive)

- The extractor is deterministic on the 2025 CFR: re-extraction reproduces all
  124,993 stored citations (paths and spans).
- The stored citation files dropped `group`. 12,677 continuation citations need it
  to drill to readable text, and re-extraction recovers it.
- There are no outcome conflicts per cited Code section at 119-4 in this data
  (0 of 1,673).
- Distinct cited Code sections: the union is 1,673, and the naive per-part sum is
  3,685.
