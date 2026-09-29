# Plumbing spike 1: what was cheap and what was hard

*2026-09-29. Throwaway code for [docs/plumbing-design.md](../../docs/plumbing-design.md)
("After review 2"). Run `uv run --group plumbing python spikes/plumbing1/check.py`:
17 checks, all pass. It uses a throwaway database (`levadura_spike1`) on the
ArangoDB sandbox container.*

> **Read with [REVIEW.md](REVIEW.md) (Codex).** "17/17" supports a narrow, static,
> single-load import. It does not support stable identity across extractor
> changes, manifest-pinned history, honest paging at page boundaries, or evidence
> validated per cell:
> - the paging oracle shares its inputs with `drill`, and compares members only
>   globally, not per cell;
> - `truncated` is wrong when exactly `limit` members remain;
> - resolution keys omit the manifest, so a corrected import would overwrite
>   history;
> - the per-part `MERGE` of outcomes would hide conflicting outcomes for one Code
>   section.
>
> In this data there are none: 0 of 1,673 cited Code sections have more than one
> outcome at 119-4, checked directly from the source file. So the histogram match
> is real here, but the code would mask a conflict elsewhere. The conclusions below
> hold at that narrower scope.

One vertical, for finding #1 at USC 119-4, through every layer:
- occurrences with stable identity;
- reified resolutions;
- rollups by part with per-metric merge state;
- drill with keyset paging;
- a locator followed to hash-checked text.

The CFR text stays in its zip; the database is the index.

## Cheap (it worked the first time)

- **Occurrence identity.** Re-running the extractor over every 2025 section
  reproduces the stored citation list exactly: paths and spans, 0 of 6,158
  sections differ. So `(section, cite_index)` is a trustworthy identity, and review
  2's "regenerate from the traversal" rule costs only extraction time.
- **Recomputing from the index gives the ledger's numbers exactly.** All of these
  match obs-0129:
  - 10,300 of 124,993 occurrences broken;
  - 1,675 of 6,158 fossil-candidate sections;
  - 1,673 distinct cited Code sections, with the same breakdown by outcome.
  
  The numbers are computed from reified resolutions, not copied from the ledger.
- **Merge state is not a nicety.** Summing each part's distinct cited Code sections
  gives **3,685**; the union is **1,673**. Additive rollups would be wrong by a
  factor of 2.2 on a finding already published. Carrying sets as the merge state
  fixes it. Materializing 69 parts took 0.7s.
- **Keyset paging is exact.** Across all 69 parts, drilling into the 1,675 fossil
  sections page by page reassembles the unpaged oracle exactly, with no
  duplicates, and every `population_total` is honest.
- **Idempotency.** uuid5 keys plus replace-on-duplicate: reloading changes nothing.
- **Locators.**
  - A relocated copy verifies.
  - A changed hash reports `stale`.
  - A missing file reports `unreachable`.
  - With an extraction cache keyed by the file's identity on disk, following 20
    spans takes 2.7s.

## Hard, or found on the way

- **The stored results had quietly lost evidence.** 12,677 citations (10%) are
  *continuations*, like "section 509(a) (2) **or (3)**". Their span covers only
  "(3)". The extractor's `group` field, which ties "(3)" back to "section 509(a)",
  was dropped when `cfr-usc-citations-v2-*.jsonl` was written. Without
  re-extraction, one citation in ten can't be drilled to readable evidence. This is
  review 2's HIGH #3 in concrete form, and it's why adapters must regenerate from
  the traversal rather than join legacy files. The spike's first run failed this
  check. Recovering `group` through re-extraction fixed it.
- **The cost of that rule is load time:** 198s, almost all of it re-extraction. It's
  fine here and would matter at the scale of case law.
- **`follow` initially re-parsed the whole zip on each call.** A cache was needed,
  as review 2 predicted. Text at scale needs addressable storage: one member per
  section, or byte offsets, not "parse the volume and count".
- **Sets as merge state won't scale as they stand.** Arrays of ids are fine at
  1,675 and not at billions of rows. Compressed bitmaps (exact) or sketches
  (approximate, declared as such) come next.

## Not attempted

- Linking resolutions to target provisions. The 57,176 provisions at 119-4 are
  loaded, but no `targets` links exist, so address collisions aren't yet
  exercised.
- Corrections and `supersedes`, and atomic manifest publication.
- Following USC text; a second snapshot; the Yanantin mapping.
