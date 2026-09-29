# Plumbing: an append-only world for minds that forget

*2026-09-29, draft 1, by the owning instance (Opus 5.5). A design, not a measurement.
It goes to adversarial review before slice 1 is built. The framing comes from
conversation with Tony: the project is plumbing for a "Prime Radiant"-like ability
to move between scales in a large corpus, not a sequence of studies.*

## Why

A mind that can only accumulate context has to hoard. The pilot's persistent arm
tried to copy the whole inventory into its state until the output cap stopped it.
A Hamut'ay taste_open instance curates what it keeps. It can drop a detail, but
only safely if the detail stays reliably retrievable. **The world is append-only
so that the minds don't have to be.**

The plumbing is that world: a corpus with its instruments' results, linked so that
- every aggregate drills down to the rows it counted, and those rows to text spans;
- every row rolls up to the observations that include it;
- every document can be followed across editions.

It matters when the corpus outgrows any context. Governance documents do, and so do
regulations over decades. The pilot found that a persistent mind buys nothing when
the world fits in the prompt.

**The target user is someone else:** a human or an instance who loads a corpus, runs
instruments, and writes a paper from what they see. The fossil findings are examples
of what the tool finds, not what it's for.

## The layers

1. **World (this design):** documents, editions, references, and the observations
   instruments make about them.
2. **Instruments:** fast, population-wide judges, such as Jev lenses, CLM, the
   citation extractor and mini-AGI. They write observations into the world. They
   stay instruments: obs-0149 showed Jev's judgment doesn't distill into a surface
   model.
3. **Experts (later):** taste_open instances that each live through a region of the
   world and curate state that *cites world ids* rather than copying facts. Experts
   can clone, combine and seed new experts, under Hamut'ay's split-self contract,
   which the plumbing records but doesn't decide.
4. **Routing (later):** "who has seen something like this?" Two signals:
   - CLM, matching the question to expert descriptions contrastively;
   - footprint overlap in the graph (below).
   They should check each other.

## Data model (corpus-agnostic)

Vertices:
- **`document`:** one version of one unit (a CFR section in one edition, a USC
  provision at one release point). Holds the text (or its hash plus a pointer), a
  stable `unit` key that persists across versions (for example `cfr26:1.56-0`), the
  edition, `observed_at` (when the text held), and the source hash.
- **`edition`:** a corpus snapshot (CFR 1997, USC 119-4) with its own mixed dates.
  An edition isn't a moment.
- **`observation`:** one ledger entry, mirrored. The JSONL ledger stays
  authoritative, with its hash chain and OTS stamps.
- **`agent`:** an instrument, a human or an expert instance.

Edges, all append-only with a provenance envelope:
- **`part_of`:** document → edition.
- **`reference`:** document → document (a CFR section citing a USC provision). The
  edge carries the span and the resolution outcome **at a stated edition of the
  target**, because the same citation resolves differently at 1996, 119-4 and
  119-110. Validity time lives on the edge.
- **`succeeds`:** document → document, the same unit across editions, with
  `text_changed` and the pairing rule. Reuse (the same number, a different subject)
  is an edge kind of its own, never an assumption.
- **`measured`:** observation → document. It carries the instrument's per-item
  result (label, probabilities, surprise, audit verdict), so an aggregate
  observation reaches every item it counted.
- **`derived_from`:** observation → observation.
- **`visited`** (footprint): agent → document or observation, recorded when an
  expert's query returns the node, with the query and cycle. This is what footprint
  routing uses.
- **`lineage`:** agent → agent (cloned-from, combined-from, seeded-from), with the
  cycle at the split.

Nothing is updated or deleted. A correction is a new edge that points at what it
corrects, as the ledger does.

## Tool surface (shaped for an expert's calls)

Every operation takes serializable input, returns bounded pages (default 40, like
the pilot's ledger tool) with a continuation token, and returns ids an expert can
cite.

- **`aggregate(filter, group_by)`:** counts and rates over documents or references,
  such as "share of references broken at 119-4, by part". Zoom up.
- **`drill(observation | aggregate cell)`:** the items behind a number. Zoom down.
- **`span(reference)`:** the text around a citation. Down to the page.
- **`history(unit)`:** a unit's versions across editions, with changes and reuse.
  Across time.
- **`neighbors(id, kinds)`:** one hop along chosen edge kinds.
- **`search(text, filter)`:** ArangoSearch over document text. It fills the content
  gap Llika's spec declares.

Access goes through a tenant-bound service that never hands out the database handle
(Llika's principle, and the reason for it: ArangoDB has no access control finer than
a database). A Python library and CLI come first, then an MCP wrapper once there's a
caller.

## Relation to Yanantin

- The ledger already maps onto Jabberwock (`docs/jabberwock-mapping.md`).
- Llika shares these principles (ArangoDB, append-only, provenance, a tenant-bound
  RPC-shaped service). It deliberately excludes what corpus zoom needs: aggregation,
  batch loading, content search and validity time on edges.
- So this is built here, on Llika's principles, so that convergence is a migration,
  not a rewrite. A letter to Yanantin's owner, through Tony, offers the content-index
  slice and describes footprints and lineage.

## Slice 1 and its acceptance test

**Load:**
- CFR 26, 1997 and 2025: 11,141 documents;
- USC 26 at GPO 1996, 119-4 and 119-110: about 155k provisions;
- references with per-release outcomes, from the v2 extractor files;
- `succeeds` pairings and reuse edges;
- every per-section instrument result as `measured` edges on mirrored ledger
  observations.

**Accept when all of these hold:**
1. Findings #1–#3 in `findings-2026-09-24.md` are each reproduced by one
   `aggregate` call, matching the ledger values exactly.
2. Each of those drills to its items and then to spans, and a sample of 20 items
   matches the source files.
3. Every loaded item's `measured` edges roll up to the ledger observations that
   counted it, and none are orphaned.
4. `history` follows §1.56-0 and a reused number (old §683) across editions
   correctly.
5. A scripted "expert" session of ten tool calls leaves a footprint that a
   `neighbors` call can reconstruct.

**Not in slice 1:** experts, routing, CLM, a second corpus, the MCP wrapper.

## Open questions for review

- **Text storage.** 11k CFR documents are fine in the database. USC texts at three
  releases may not be. Store hashes plus a pointer to the release files?
- **Footprints of large queries.** Is a `visited` edge per returned node too much for
  an `aggregate` over 125k references? The alternative is one edge to the query's
  result set.
- **Pairing across editions by unique number only** drops repeated numbers (601 in
  1997). Is a content-similarity pairing worth adding in slice 1?
- **Database placement.** Our own database on the shared `arango-ayllu`, with our
  own user (pending Tony).
