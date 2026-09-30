# Review of plumbing spike 3 (Codex, verbatim)

Read-only review: **11 tests collected**, pinned fixture expectations match their generator. I reproduced three issues with in-memory stubs. I did not execute the database suites: they truncate/write data.

1. **HIGH — Paging mixes incompatible string orders.**  
   [lineage.py:275](/home/tony/projects/levadura_salvaje/spikes/plumbing3/lineage.py:275) sorts members in AQL; [lineage.py:297](/home/tony/projects/levadura_salvaje/spikes/plumbing3/lineage.py:297) applies the continuation predicate in Python. AQL uses [server-language collation](https://docs.arango.ai/arangodb/stable/aql/fundamentals/type-and-value-order/), whereas Python compares Unicode code points. Given English-collated `["a", "å", "b"]`, limit 2 returns `["a", "å"]`, then **an empty page**, missing `"b"`. The fixture’s IDs conceal this. Use the same comparator for sorting and continuation, with a deterministic tie-breaker.

2. **HIGH — The no-change shortcut ignores snapshot identity.**  
   [lineage.py:163](/home/tony/projects/levadura_salvaje/spikes/plumbing3/lineage.py:163) compares only `h(rows)`. Publishing identical rows at a new snapshot returns the old manifest, with old assertion slots and old snapshot metadata—even though snapshot participates in both slot and manifest identity. Confirmed with a stub. Compare the complete semantic identity, including snapshot and writer version; production must also pin upstream dependencies.

3. **MEDIUM — Crash retry assumes an unchanged checkpoint plan, but that plan is absent from identity.**  
   [lineage.py:160](/home/tony/projects/levadura_salvaje/spikes/plumbing3/lineage.py:160), [lineage.py:207](/home/tony/projects/levadura_salvaje/spikes/plumbing3/lineage.py:207): crash after writing retractions with checkpoints disabled, then retry with the threshold restored. The same `m` now describes a fresh root, but insert-only staging retains its old retractions. I reproduced the resulting count-check failure. This fails safely, but is not universally retryable. Freeze/version the staging plan. The inherited `ix.ADAPTER` also provides no separate lineage implementation version.  
   [lineage.py:234](/home/tony/projects/levadura_salvaje/spikes/plumbing3/lineage.py:234) verifies counts only; it does not verify persisted content or rollup equality.

4. **The core ancestry visibility construction stands under its invariants.**  
   [lineage.py:99](/home/tony/projects/levadura_salvaje/spikes/plumbing3/lineage.py:99), [lineage.py:203](/home/tony/projects/levadura_salvaje/spikes/plumbing3/lineage.py:203): retractions carry the **old record’s cell**, so moves retract correctly in both scoped and whole-view reads. Deletions touch the old cell; [lineage.py:137](/home/tony/projects/levadura_salvaje/spikes/plumbing3/lineage.py:137) writes zero-unit rollups, preventing resurrection through an older rollup. Reappearance writes a newer rollup. Re-added slots receive new birth keys; abandoned generations are excluded from later ancestry. Checkpoints use only `[m]`. All public readers gate on a manifest.  
   This depends on unique, valid input slots and immutable staging plans. [lineage.py:78](/home/tony/projects/levadura_salvaje/spikes/plumbing3/lineage.py:78) silently overwrites duplicate units; [lineage.py:121](/home/tony/projects/levadura_salvaje/spikes/plumbing3/lineage.py:121) silently collapses duplicate visible slots.

5. **CAS is coherent; “rebase” means whole-snapshot replacement.**  
   [lineage.py:237](/home/tony/projects/levadura_salvaje/spikes/plumbing3/lineage.py:237): with append-only manifests and the unique `(stream, seq)` index installed, a stale parent’s successor sequence is occupied, forcing recomputation against current. That is a valid CAS construction.  
   However, if A changes slot X and B changes Y from the same base, B’s successful rebase restores X from B’s supplied rows. This matches the declared whole-state contract and the oracle; it **does not preserve concurrent independent corrections**. Production must explicitly choose replacement semantics or patch merging/conflict detection.

6. **The oracle and mutants are substantive; coverage claims are broader than the assertions.**  
   [test_lineage.py:118](/home/tony/projects/levadura_salvaje/spikes/plumbing3/test_lineage.py:118): reproducing the random chain found 9 additions, 14 deletions and 7 moves, but **zero emptied cells, reappearing cells or re-added deleted units**. The mutation generator also never restores a dropped citation.  
   [test_lineage.py:46](/home/tony/projects/levadura_salvaje/spikes/plumbing3/test_lineage.py:46) checks rollups/drills only for expected surviving cells: a stale rollup for a vanished cell escapes. `cell_states` is checked per cell only for members; its counts and cited sets are not compared exactly, and merged totals are ignored.  
   [test_lineage.py:173](/home/tony/projects/levadura_salvaje/spikes/plumbing3/test_lineage.py:173) has no barrier or assertion that `_Rebase` occurred; serialized execution satisfies the race test. Crash hooks run after completed stages, including all record batches ([lineage.py:219](/home/tony/projects/levadura_salvaje/spikes/plumbing3/lineage.py:219)). The post-checkpoint delta is checked only for ancestry, not answers ([test_lineage.py:233](/home/tony/projects/levadura_salvaje/spikes/plumbing3/test_lineage.py:233)).  
   Both mutants genuinely modify the acceptance path and detect their specified faults.

7. **The report supports member agreement and record-count savings, not complete answer equivalence.**  
   [measure.py:48](/home/tony/projects/levadura_salvaje/spikes/plumbing3/measure.py:48) verifies members only—even for sampled rollups/pages. Wrong denominators, broken counts, occurrence counts or cited outcomes can pass. [README.md:66](/home/tony/projects/levadura_salvaje/spikes/plumbing3/README.md:66) overstates this as every generation matching the oracle.  
   The **315,355 versus 5,247,774 assertions** arithmetic does stand. Storage statistics are collection-wide, however ([measure.py:146](/home/tony/projects/levadura_salvaje/spikes/plumbing3/measure.py:146)); reruns accumulate unrelated streams, and assertion counts alone are not total byte savings.

8. **Measured comparisons stand at their sampled points; causal diagnoses do not follow from these artifacts.**  
   [measure.py:103](/home/tony/projects/levadura_salvaje/spikes/plumbing3/measure.py:103) creates matching-row baselines at depths 4, 40 and 41. There are none at 5/10/20, and the checkpoint changes another ten occurrences before measurement ([measure.py:132](/home/tony/projects/levadura_salvaje/spikes/plumbing3/measure.py:132)); its baseline is therefore approximate, not identical.  
   [measure-report.json:568](/home/tony/projects/levadura_salvaje/spikes/plumbing3/measure-report.json:568) gives mass-change ratios of **3.92× drill, 2.21× unpaged, 4.02× all states**. “Reads about 4×” needs that qualification.  
   The reviewed artifacts contain no profiler output supporting the “17×”, “365→218 ms” or “50,100 entries” history ([README.md:94](/home/tony/projects/levadura_salvaje/spikes/plumbing3/README.md:94)). Nor does `measure.py` isolate `_view` time: full-row hashing and five count queries also contribute. A zero-retraction checkpoint rules out retractions as its residual cost; it does not identify the remaining bottleneck. Separate stream collections still contain that stream’s historical versions. Archiving old records must preserve access for old manifests/cursors.

Before production: fix snapshot identity and ordering; freeze/version retry plans; validate unique slots and exact persisted state; force stale-parent races and partial-batch failures; test disappearance/reappearance/resurrection and checkpoint retries; define concurrent-edit semantics, durability and historical retention; capture query plans and phase timings before selecting indexes or checkpoint thresholds.

**Verdict:** delta-sized writes, substantial record-count savings, the ancestry/retraction/tombstone construction, and the reported sampled timings stand. General paging correctness, snapshot-aware idempotence, unconditional crash retry, exhaustive change coverage, concurrent edit preservation, and the claimed performance causes do not.
---

## Prompt

You are an adversarial code reviewer from another model family. Review the throwaway spike in spikes/plumbing3/ (lineage.py, test_lineage.py, measure.py, README.md, measure-report.json). It builds on spikes/plumbing2/ (index.py, fixture.py), which you reviewed before (spikes/plumbing2/REVIEW.md). Read code and run read-only commands; you probably can't reach the database, so review statically where needed.

The design: records keyed by (born generation, slot); a correction writes changed slots plus append-only retractions; a reader for manifest m sees records born in m's ancestry not retracted within it; rollups rewritten only for touched cells, read from the most recent ancestor; CAS commit requiring the parent to still be current, with rebase; checkpoints (fresh roots) past a retraction threshold.

Focus:
1. Correctness of visibility: can any reader (cell_states, rollup, unpaged, drill, _view used for deltas) see a record it shouldn't, or miss one it should? Consider units moving between cells (cell-scoped retractions), deletions, re-adding a slot previously deleted, rebases after a lost race, crashed generations whose keys a later generation might need, checkpoints, and the rollup "most recent ancestor" rule when a cell becomes empty or reappears.
2. The test oracle (fixture.expected) and whether the tests, including the random chain and the mutants, prove what they claim. Anything vacuous?
3. Concurrency and crash safety of publish/_publish_on/_Rebase.
4. Whether README's measurements and conclusions follow from measure.py and measure-report.json, including the "two wrong diagnoses" section and the same-rows baseline.
5. What must be true before this becomes non-spike code.

Be concrete (file:line). Terse markdown. End with a verdict: which conclusions stand.
