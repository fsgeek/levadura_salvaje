# Review of plumbing spike 2 (Codex, verbatim)

**Useful progress, but “correctness under change” remains narrower than claimed.** Static review plus read-only fixture checks; I did not run the database suites because they write/truncate data. Both pinned fixture generations match their generator.

1. **HIGH — Manifest identity omits the resolved USC generation and edge targets.**  
   [index.py:98](/home/tony/projects/levadura_salvaje/spikes/plumbing2/index.py:98), [corpus.py:181](/home/tony/projects/levadura_salvaje/spikes/plumbing2/corpus.py:181), [run_real.py:64](/home/tony/projects/levadura_salvaje/spikes/plumbing2/run_real.py:64): the CFR manifest hashes rows containing outcomes, but targets travel separately through `extra`. Reloading corrected USC provisions can change provision keys while preserving every outcome. Republishing then returns the old CFR manifest immediately, preserving old edges. The manifest also records no USC-manifest dependency. **Pin dependencies and edge-producing inputs in manifest identity.**

2. **HIGH — Unpublished data is readable.**  
   [index.py:121](/home/tony/projects/levadura_salvaje/spikes/plumbing2/index.py:121): `cell_states` never calls `published`; it returns partially imported generations. I confirmed the missing gate with a database stub. `drill`, `rollup`, `unpaged`, and `IndexResolver` do gate publication. The crash test checks only drill and rollup ([test_spike2.py:167](/home/tony/projects/levadura_salvaje/spikes/plumbing2/test_spike2.py:167)). Thus README’s “data nobody can read” is false. Separate a private staging aggregator from the published reader.

3. **HIGH — Publication is a single-writer convention, not a complete atomic/retry protocol.**  
   [index.py:163](/home/tony/projects/levadura_salvaje/spikes/plumbing2/index.py:163), [index.py:189](/home/tony/projects/levadura_salvaje/spikes/plumbing2/index.py:189): two publishers can select the same predecessor and write equal `seq`; `current` has no tie-breaker. Same-manifest publishers can both pass the initial check, continue replacing records after another publishes, and collide inserting the manifest. Edge retries also replace timestamps/provenance ([corpus.py:193](/home/tony/projects/levadura_salvaje/spikes/plumbing2/corpus.py:193)), contrary to the append-only convention. README acknowledges concurrent sequencing, but the consequences include ambiguous selection and post-publication writes. The test crashes only after all data is complete; republish checks only counts. Require serialized/CAS publication, immutable completed generations, and fault injection between batches, rollups, edges, verification, and commit.

4. **The fixture oracle is meaningfully independent; some mutation claims overreach.**  
   [fixture.py:71](/home/tony/projects/levadura_salvaje/spikes/plumbing2/fixture.py:71) shares no implementation with `index.py`; checked-in expectations prevent silent changes unless regenerated. It is still a generated oracle over the same synthetic inputs, not separately hand-authored expected IDs. Literal boundary/conflict assertions strengthen it.  
   The swap and truncation mutations genuinely exercise `check_cell` and prove those faults are detected. But [test_spike2.py:237](/home/tony/projects/levadura_salvaje/spikes/plumbing2/test_spike2.py:237) merely demonstrates a local last-wins algorithm’s order dependence; it never injects that mutant into the acceptance path, and does not reproduce within-cell last-wins aggregation. Also, all tests—including pure fixture/resolver tests—skip when configuration is absent ([test_spike2.py:15](/home/tony/projects/levadura_salvaje/spikes/plumbing2/test_spike2.py:15)).

5. **MEDIUM — Real checks promise stronger coverage than they assert.**  
   [run_real.py:92](/home/tony/projects/levadura_salvaje/spikes/plumbing2/run_real.py:92) compares pages with freshly computed `cell_states`, **not persisted rollups**.  
   [run_real.py:105](/home/tony/projects/levadura_salvaje/spikes/plumbing2/run_real.py:105) checks aggregate fanout arithmetic; moving an edge to the wrong assertion/provision preserves the check. It proves neither endpoint validity nor one edge per expected version. Compare exact endpoint sets per assertion.  
   [run_real.py:124](/home/tony/projects/levadura_salvaje/spikes/plumbing2/run_real.py:124) permits zero USC follows. The report’s 714 successes are useful observed coverage, but the acceptance condition does not require any.

6. **Paging substantially stands for frozen generations and positive limits.**  
   [index.py:241](/home/tony/projects/levadura_salvaje/spikes/plumbing2/index.py:241): distinct members, strict keyset ordering, `limit + 1`, page totals, and HMAC binding to spec/manifest/cell/order are coherent. Boundary and wrong-cell/manifest tests are substantive; I found no normal cross-cell/manifest cursor bypass. However, `limit=0` on a nonempty cell reaches `page[-1]` and crashes. Validate positive integer limits. Stability also depends on the publication immutability missing above.

7. **Resolver agreement supports implementation consistency, not independent semantic validation.**  
   [corpus.py:128](/home/tony/projects/levadura_salvaje/spikes/plumbing2/corpus.py:128) closely restates [resolve.py:51](/home/tony/projects/levadura_salvaje/src/levadura_salvaje/resolve.py:51): same normalization, status precedence, range rule, ancestor walk. It shares the USC extractor and citation inputs; README appropriately admits prior implementation exposure.  
   “124,993/124,993” includes **46 null-path occurrences** that neither implementation resolves. Nested `zip` comparisons also fail to assert lengths or identities ([run_real.py:70](/home/tony/projects/levadura_salvaje/spikes/plumbing2/run_real.py:70)). Collision rows are preserved, but first-position wins among differing non-null statuses; overlapping ranges use unsorted database order. Synthetic expectations must establish those policies. Edges to all versions represent candidates, including repealed versions, rather than a uniquely selected effective provision.

8. **Hash dispatch works; cache invalidation is incompletely demonstrated.**  
   [corpus.py:211](/home/tony/projects/levadura_salvaje/spikes/plumbing2/corpus.py:211): domains select distinct extractors and text hashes are verified. Cache keys include archive hash **and path**. Hashing and extraction reopen the file separately, allowing replacement between them to cache different bytes under the earlier digest. No test changes archive contents; changing the expected hash tests mismatch reporting only. Sampled whole-section follows also do not establish citation-span/group correctness.

9. **Tenant defaults follow the convention; setup has security/recovery gaps.**  
   [tenant_setup.py:44](/home/tony/projects/levadura_salvaje/scripts/tenant_setup.py:44) creates separate app/test databases and users; runtime uses configured tenant credentials, with no root lookup. No credential printing appears. But setup grants the intended database and denies `_system` without clearing existing grants elsewhere.  
   [tenant_setup.py:59](/home/tony/projects/levadura_salvaje/scripts/tenant_setup.py:59): `0600` applies on creation; an existing permissive file remains readable while credentials are rewritten, until the later chmod. Truncation is non-atomic, and passwords change before durable configuration storage. Use a private temporary file plus atomic replacement and verify effective grants.

**First next step:** close publication/dependency identity and visibility gaps, then test crash/retry/concurrent publication and exact edge sets. Do this before storage sharing or bitmap work.

**Verdict:** per-cell fixture validation, conflict-preserving merges, positive-limit paging, sequential correction pinning, collision preservation, and sampled hash verification stand. Universal publication invisibility, robust concurrent/idempotent publication, independent resolver correctness, and per-assertion edge completeness do not. Full-generation copying is a demonstrated cost; “correctness was cheap” is premature. The committed [report timings](/home/tony/projects/levadura_salvaje/spikes/plumbing2/real-report.json:166) support warm no-op timings, not README’s cold-publication timings or storage-size measurements.
---

## Prompt

You are an adversarial code reviewer from another model family. Review the throwaway spike in spikes/plumbing2/ (index.py, corpus.py, fixture.py, test_spike2.py, run_real.py, README.md, real-report.json) against spikes/SPIKE2-BRIEF.md and your own review of spike 1 (spikes/plumbing1/REVIEW.md). Also review src/levadura_salvaje/tenant.py and scripts/tenant_setup.py. You may read code and run read-only commands; you probably cannot reach the database, so review statically where needed.

The spike claims 27 fixture tests and 13 real-corpus checks pass. Focus:
1. Tests or checks that could pass vacuously, or that don't test what their names claim. Is the fixture's expected.json genuinely independent of index.py? Do the mutation tests prove what they say?
2. Correctness of publication and manifest pinning: atomicity (data, rollups, count check, then manifest), idempotent retry, the selection rule (`current`), and anything a crash or a second publisher could break. Is a partially written generation truly invisible to every reader (drill, rollup, unpaged, cell_states, IndexResolver)?
3. Paging and cursors: limit+1, totals per page, HMAC binding. Any way to get a wrong page, skip or duplicate a member, or reuse a cursor across manifests/cells?
4. The index resolver in corpus.py versus src/levadura_salvaje/resolve.py: is it really an independent implementation, and does "124,993/124,993 agree" support what the README says? The edges (resolves_to) and the collision handling. follow() and its hash-domain dispatch and cache.
5. The tenant: does it meet the convention (one db + user per tenant, a _test db, no root at runtime, credentials 0600)? Any leak?
6. Whether the README's cheap/hard conclusions are supported, and what spike 3 (or the first non-spike code) must do first.

Be concrete (file:line). Terse markdown. End with a verdict: which conclusions stand.
