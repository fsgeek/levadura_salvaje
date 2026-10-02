The recorded counts reproduce correctly, and the stored readings join correctly to units. The main problems are latent lens bugs and conclusions that exceed what the experiment establishes. No files changed.

Ranked findings:

1. **High — Stored labels are not checked against the audited result files.**  
   [instrument.py:178](/home/tony/projects/levadura_salvaje/spikes/surface1/instrument.py:178) loads mutable JSONL files and checks only each row’s *input-text* hash against the unit locator. Changing a label while preserving that hash silently changes the result, while the tool continues advertising the original ledger entries and audit quality. Both ledger entries contain result-file hashes that the loader could verify. I reproduced this with an in-memory file substitution: `current → historical` was accepted with the unchanged text hash. Duplicate unit rows also silently overwrite earlier rows.

2. **High — “Both callers used the reading as a pointer, not a verdict” is overclaimed.**  
   [surface1-scorecard.md:284](/home/tony/projects/levadura_salvaje/docs/surface1-scorecard.md:284), [surface1-scorecard.md:288](/home/tony/projects/levadura_salvaje/docs/surface1-scorecard.md:288). Sonnet says the lens “therefore treats most of these as still operative” ([answer-caller-sonnet-3.md:38](/home/tony/projects/levadura_salvaje/spikes/surface1/answer-caller-sonnet-3.md:38)) without explaining the section-level versus §902-dependent-rule distinction. Reading some text afterwards does not exclude adopting the label as a verdict elsewhere.

   Strictly registered U5 can still defensibly fail: Sonnet does not explicitly equate `current` with “misleading.” But the broader claim that label adoption definitively did not occur is unsupported. Opus’s “model judgment” caveat concerns reliability; its needs-list item at line 22 supplies the relevant scope qualification.

3. **Medium — Stale-unit pagination loses units and falsely reports completeness.**  
   [instrument.py:237](/home/tony/projects/levadura_salvaje/spikes/surface1/instrument.py:237), [instrument.py:245](/home/tony/projects/levadura_salvaje/spikes/surface1/instrument.py:245). `stale_units` always uses `stale[:LIST]`; stale overflow is excluded from `more`. With 250 stale units, I obtained 200 IDs, `truncated=False`, and `list_next=None`. Explicitly requesting cursor 200 returned the same first 200. This did not affect the saved runs, whose stale counts were zero.

4. **Medium — `returned` omits unread and stale IDs actually shown.**  
   [instrument.py:238](/home/tony/projects/levadura_salvaje/spikes/surface1/instrument.py:238). `shown` includes classified lists and samples, but excludes `not_read_units` and `stale_units`. Two unread units produce two displayed IDs and `returned=0`; the 250-stale reproduction displayed 200 IDs and likewise reported zero.

5. **Medium — Partial or malformed readings produce misleading counts and agreement.**  
   [instrument.py:218](/home/tony/projects/levadura_salvaje/spikes/surface1/instrument.py:218), [instrument.py:225](/home/tony/projects/levadura_salvaje/spikes/surface1/instrument.py:225). A missing judge row becomes the literal label `"None"` in that judge’s counts, rather than missing coverage. Stored labels are never validated against `LENSES[name]["labels"]`: two `"live"` rows count as judge agreement even though `"live"` is rejected as a requested label. A missing database unit plus null stored hashes also passes because `None == want.get(u)`.

   These are latent cases: the committed files have complete, matching judge keysets and valid labels. Validate the stored schema and hash presence, and represent missing judge coverage separately.

6. **Medium — U7’s correct numerical failure does not establish absence of substitution.**  
   [surface1-scorecard.md:293](/home/tony/projects/levadura_salvaje/docs/surface1-scorecard.md:293). Round 3 has 13 text calls, exactly matching round 2. But call totals conflate breadth, depth and pagination:

   | Caller | Text calls, R2 → R3 | Distinct CFR units explicitly cited/followed |
   |---|---:|---:|
   | Opus | 10 → 8 | 5 → 1 |
   | Sonnet | 3 → 5 | 2 → 3 |

   Opus’s four large pages of one section inflate the call count while its reading breadth contracts. Keep **U7 fail**; “the reading did not substitute for reading” does not follow.

7. **Medium — Round 3 omits material confounds.**  
   [surface1-scorecard.md:298](/home/tony/projects/levadura_salvaje/docs/surface1-scorecard.md:298). Between the recorded rounds, callers gained nonmatch lists, changed anchor behavior, paging hints and reverse paging ([surface1-scorecard.md:233](/home/tony/projects/levadura_salvaje/docs/surface1-scorecard.md:233)). Round-3 callers directly use reverse paging, making these changes relevant to U7.

   Lens also changes population access: it supplies complete classification lists for this small population; Sonnet’s preceding `cited_by 902` requested only 12 units. Its question, scope, audit figures and “read both sides” caution also provide explicit guidance. The experiment cannot separate classification, enumeration, guidance and existing model knowledge. The committed artifacts do not establish matched caller effort or context beyond the brief.

   The “hand audit” was performed by Claude instances, with stratified sampling; it is neither an independent human audit nor validation specifically of §902-dependent-rule currency ([currency-scorecard.md:56](/home/tony/projects/levadura_salvaje/docs/currency-scorecard.md:56), [observations.jsonl:133](/home/tony/projects/levadura_salvaje/ledger/observations.jsonl:133)).

8. **Medium — The governance reply overstates automatic Q3 extraction.**  
   [reply-to-governance-analysis-plan.md:42](/home/tony/projects/levadura_salvaje/docs/requests/2026-10-02-reply-to-governance-analysis-plan.md:42). The two `supersedes` pairs are real and mechanically extractable. They do not make Q3’s `where_corrected` and `lag` extractable “without judgment” across levadura.

   Governance asks about *promoted claims*, with assertion and correction locations and lag in commits and days ([analysis-plan:73](/home/tony/projects/governance/docs/superpowers/specs/2026-09-30-calibration-study-analysis-plan-DRAFT.md:73)). The links identify corrections to two measurement observations. They do not identify every earlier headline, promotion event, correction location, or correcting commit. Their `observed_at` dates describe the corpus, not correction timing. Connecting these rows to the study’s claim units still requires judgment.

9. **Medium — The governance reply cites a snapshot that cannot support its round-3 assertions.**  
   [reply-to-governance-analysis-plan.md:8](/home/tony/projects/levadura_salvaje/docs/requests/2026-10-02-reply-to-governance-analysis-plan.md:8), [reply-to-governance-analysis-plan.md:27](/home/tony/projects/levadura_salvaje/docs/requests/2026-10-02-reply-to-governance-analysis-plan.md:27). `78d0f24` contains rounds 1–2 but no round-3 prediction file. Round 3 was added in `cecba93`. Moreover, the reply commit precedes the round-3 scorecard commit, so “Their scores are in” the scorecard was premature for round 3 at that revision.

   The narrower pre-run registration claim checks out: the prediction commit and stamp commit precede the first recorded round-3 calls.

10. **Medium — The scorecard misses substantive answer overreach.**  
    [surface1-scorecard.md:304](/home/tony/projects/levadura_salvaje/docs/surface1-scorecard.md:304) records ranking and pattern-attribution errors, but omits Sonnet’s stronger unsupported assertions. Sonnet admits it did not read the special effective-date paragraph, then categorically says a reader of the section alone would not learn the cutoff ([answer-caller-sonnet-3.md:34](/home/tony/projects/levadura_salvaje/spikes/surface1/answer-caller-sonnet-3.md:34)). Beginning/end slices and narrow regex nonmatches do not establish that absence. Its claim that most other §902 references are incidental and cause little misleading effect also lacks population-level evidence ([answer-caller-sonnet-3.md:39](/home/tony/projects/levadura_salvaje/spikes/surface1/answer-caller-sonnet-3.md:39)).

11. **Medium — Exported footprints are insufficient for independent response reconstruction.**  
    [instrument.py:250](/home/tony/projects/levadura_salvaje/spikes/surface1/instrument.py:250), [footprints.py:26](/home/tony/projects/levadura_salvaje/spikes/surface1/footprints.py:26). Lens correctly logs all effective input arguments and sampled IDs. But it does not log combination totals, complete returned lists or reading-file identities; the exporter also drops manifest and returned/truncated metadata.

    §1.902-1 is absent from both recorded §902 lens samples. Its U3 eligibility depends on reconstructing the full lists from the committed data. That reconstruction succeeds here, but the footprint itself does not preserve those returned IDs. Call order cannot establish selection motive.

12. **Low — The printed Opus path is incorrect.**  
    [surface1-scorecard.md:274](/home/tony/projects/levadura_salvaje/docs/surface1-scorecard.md:274) prints `00122344442244442`; [footprints.json:1511](/home/tony/projects/levadura_salvaje/spikes/surface1/footprints.json:1511) establishes **`00122344422444442`**. Measures occupy calls 10–11.

The U1–U7 verdicts assess as follows:

| Item | Assessment |
|---|---|
| U1 | **Pass**: 1 successful lens call for Opus, 3 for Sonnet. |
| U2 | **Pass**: both report reproduced counts. |
| U3 | **Formal pass, weak criterion**. Complete lists qualify both; Sonnet additionally cites units actually present in its earlier part-54 lens sample. Neither establishes lens-caused selection or substantive checking of the currency judgment. |
| U4 | **Opus pass is defensible**: its needs-list item distinguishes the cited provision from another rule. “Named precisely” and “found from the output” exceed the evidence. |
| U5 | **Strict fail is defensible; broader absence claim is unsupported**, particularly for Sonnet. |
| U6 | **Pass**: no citation/unit or cell/population grain confusion found. Other reasoning errors remain. |
| U7 | **Fail**: 13 equals 13. No substitution inference follows. |

The two lens tests at [test_surface.py:264](/home/tony/projects/levadura_salvaje/spikes/surface1/test_surface.py:264) bypass `_readings` through injected cache entries. They do not check file integrity, duplicate rows, stored-schema validation, partial judge coverage, missing locators/hashes, or actual joins. They also omit:

- Label filtering’s documented **any-judge** semantics, retained population-wide counts/agreement, and mixed-label combinations.
- Paging classified, unread and stale lists, including overflow and past-end cursors.
- `returned` as the union of every displayed ID.
- Sample bounds, uniqueness, bucket membership and deterministic seeds.
- Footprint argument/sample contents and CLI/MCP parity.

Changing the label filter also changes samples within retained combinations at the same seed because one RNG is consumed across combinations. That is worth specifying and testing; it violates no current documented guarantee.

Verification: both 1,675-row files match their ledger file hashes; every reading matches the sidecar and CFR text hash; all round-3 lens/measure counts and sampled IDs reproduce. CLI/MCP argument forwarding checks passed. The existing suite produced **36 passes**; one temporary-file fixture was blocked by the read-only sandbox. Governance’s coder exclusions, Jev participation, and the two supersession links are supported.