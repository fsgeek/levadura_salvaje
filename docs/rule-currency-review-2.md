The numerical results reproduce, but several structure guarantees and scorecard interpretations overclaim.

I reviewed v3 at **`2e9d00b`**, the branch tip when I started. The branch advanced to v4 during the review; line numbers below refer to that v3 snapshot. No files were modified.

Ranked findings:

1. **P1 — Excerpts can omit the actual illustrated rule’s limit.** [rule_currency.py:173](/home/tony/projects/levadura_salvaje/src/levadura_salvaje/lenses/rule_currency.py:173)

   Example context consists of the nearest preceding main paragraph and its ancestors. It does not retrieve the provisions the example actually illustrates.

   **Concrete failure:** § 1.902-4 #4 receives an excerpt containing `(d) Illustrations`, abbreviated example facts, and nearby table cells. It omits `(a)` and `(b)`, whose distribution rules explicitly end **before January 1, 1978**. Qwen changes this record from `time_limited` to `untimed` ([result:153](/home/tony/projects/levadura_salvaje/results/rule-currency-qwen-v3-902-2025.jsonl:153)). That is a real limit disappearing from context, contradicting the scorecard’s interpretation of W3.

2. **P1 — Reader A’s blanket compliance with the carryover criterion is unsupported.** [scorecard:178](/home/tony/projects/levadura_salvaje/docs/rule-currency-scorecard.md:178), [rule_currency.py:80](/home/tony/projects/levadura_salvaje/src/levadura_salvaje/lenses/rule_currency.py:80)

   The criterion requires a rule that **carries past amounts into later periods with no end date**. It does not say every historical computation becomes `untimed` whenever the section has an open-ended applicability date.

   Audit **items 19 and 24** concern § 1.909-6(c)(1)’s annual determination, explicitly ending with the corporation’s **last pre-2011 taxable year**. Reader A cites the section-wide “ending after February 9, 2015” sentence instead. That does not establish compliance with the citation-local criterion, and the local endpoint supports `time_limited`.

   Consequently, “each” disputed rule has open-ended application and “half the judges don’t follow” the criterion are unjustified. Items **31 and 45** also concern pointer-versus-rule classification, a separate disagreement. “One ambiguity” is too strong.

3. **P1 — Sibling preference misclassifies unambiguous inline Roman children.** [structure.py:150](/home/tony/projects/levadura_salvaje/src/levadura_salvaje/structure.py:150)

   `_place()` always tries sibling continuation before child opening, including successive designators within one paragraph.

   In § 1.367(b)-4(h)(7), `(7) Triangular reorganizations —(i) Definition` becomes a new **top-level `(i)`**, because `(i)` continues `(h)`. Subsequent `(ii)` and `(B)` paragraphs fail; the actual top-level applicability `(i)` then becomes a Roman child of the wrongly placed paragraph.

   I found the same inline misclassification in § 1.904(f)-12, § 1.954-6, and § 1.965-2. Inline child context needs different handling from an ambiguous standalone designator.

4. **P1 — Failed ancestry is discarded rather than propagated.** [structure.py:207](/home/tony/projects/levadura_salvaje/src/levadura_salvaje/structure.py:207)

   Failure restores the previous stack. A following child or continuation can therefore receive a confident ancestry under an unrelated earlier paragraph.

   Reproduction: `(a) Live rule` → `(q) Before 1987` → `(1) section 902 applies`. Only `(q)` fails; `(1)` receives `(a)` as its ancestor and uses `structure`, silently losing the possible governing limit.

   In the actual CFR, § 1.704-1’s failed `(viii)…(a)` paragraph is followed by successfully placed `(1)` and `(2)` paragraphs attached to an unrelated earlier `(s)(4)` chain. The documented guarantee that chains passing through failure become unknown is not implemented.

5. **P1 — Applicability selection can return an unrelated provision.** [structure.py:248](/home/tony/projects/levadura_salvaje/src/levadura_salvaje/structure.py:248)

   Selection searches any occurrence of `effective` or `applicability` within 120 characters, prefers the last deepest-level-zero match, then falls back to any level. It neither identifies a date heading reliably nor checks which rule the provision covers.

   Concrete examples:

   - § 1.904-7 citations under `(f)` receive `(d)`’s special date for **high withholding tax interest**, omitting `(f)(10)`’s relevant applicability provision.
   - § 1.338-9(b)(3)(ii)(D) receives a date expressly governing **paragraph `(d)`**.
   - § 1.985-1 receives `(b)(2)(ii)(E)`’s date instead of the regulations’ general `(a)(2)` date.
   - § 1.963-2’s “effective foreign tax rate” is mistaken for applicability context.

   Labeling these as **the section’s** applicability paragraph increases their apparent authority.

6. **P2 — Combined designators produce self-parents, duplicate ancestors, and sibling-specific context.** [structure.py:215](/home/tony/projects/levadura_salvaje/src/levadura_salvaje/structure.py:215)

   Multiple logical nodes share one paragraph index, but `parent` and `ancestry` operate on those indices without consistently collapsing them. Across the reviewed sections, **500 paragraphs have themselves as parent**, and **276 have duplicate ancestor indices**.

   More substantively, § 1.985-1’s post-August-1994 rule includes as an “ancestor” the paragraph containing its **pre-August-1994 sibling rule**. The excerpt cannot distinguish the shared `(2)` heading from the sibling `(i)` restriction. Logical designator nodes need separate text boundaries.

7. **P2 — Truncation can remove governing limits or the marked citation itself.** [rule_currency.py:191](/home/tony/projects/levadura_salvaje/src/levadura_salvaje/lenses/rule_currency.py:191), [rule_currency.py:200](/home/tony/projects/levadura_salvaje/src/levadura_salvaje/lenses/rule_currency.py:200)

   A long own paragraph is centered around the citation without preserving its opening restriction. An in-memory reproduction loses “applies only before 1987” while retaining the citation and reporting `structure`.

   The budget comment promises to drop outer ancestors first; the implementation instead cuts the final string’s **tail**. A valid six-level main/example hierarchy with a long continuation produces an excerpt containing **neither citation marker**.

   No recorded excerpt hits the overall budget, but **25 own paragraphs, 254 ancestry selections, and 72 applicability selections undergo clipping**. “None is truncated” is defensible only as a claim about the final budget cutoff.

8. **P2 — Example scopes and attachment lack reliable boundaries.** [structure.py:180](/home/tony/projects/levadura_salvaje/src/levadura_salvaje/structure.py:180), [structure.py:193](/home/tony/projects/levadura_salvaje/src/levadura_salvaje/structure.py:193), [structure.py:237](/home/tony/projects/levadura_salvaje/src/levadura_salvaje/structure.py:237)

   Reproduced cases:

   - Closing a nested `<EXAMPLE>` does not restore the outer example’s scope or heading.
   - A plain `Example 1.` starts a scope with no termination rule; a later operative paragraph can remain falsely inside it.
   - Numbered headings such as `(1) Example 1.` are not recognized by `EXAMPLE`.
   - `enclosing()` attaches **any** nonparagraph citation to the preceding paragraph, without checking its XML container. An authority heading after an example becomes example/table context.

   The 28 recorded attachments reproduce, but nearest-paragraph attachment is not a general enclosure guarantee.

9. **P2 — The ancestry probe does not measure the production parser’s failure rate.** [probe_rule_ancestry.py:102](/home/tony/projects/levadura_salvaje/scripts/probe_rule_ancestry.py:102), [design:55](/home/tony/projects/levadura_salvaje/docs/rule-currency-v3-design.md:55)

   The probe uses unnormalized paragraph text and token-by-token failure handling. Production uses normalized text, includes `FP`, and rolls back whole paragraphs.

   Normalization exposes spaced italic designators that the probe misses. Outside tables of contents, production sees **3,889 designators and 357 failed paragraphs**; the probe reports **3,524 designators and 119 failed tokens**. These are different denominators and failure units. The quoted **3.4%** is not a production ancestry error rate, and successful placement does not establish correct placement.

10. **P2 — A probe already drawn randomly is incorrectly removed from the statistical sample.** [audit_rule_currency.py:48](/home/tony/projects/levadura_salvaje/scripts/audit_rule_currency.py:48), [audit_rule_currency.py:85](/home/tony/projects/levadura_salvaje/scripts/audit_rule_currency.py:85)

    Every configured probe gets `probe=True`, even when selected in the ordinary random draw. `_load()` then excludes it. With the current population and **seed 9**, this leaves **44 statistical items**, including only 14 in that stratum.

    Missing configured probes are also silently ignored. Selection provenance and required probe presence need validation. **The recorded seed-2 audit is unaffected:** its probe was an additional item, and the committed packet/key replay exactly.

11. **P2 — XML enumeration can silently shrink the intended population.** [measure_rule_currency_qwen.py:102](/home/tony/projects/levadura_salvaje/scripts/measure_rule_currency_qwen.py:102)

    `items()` verifies sections it encounters but never checks that all expected sidecar sections were encountered. Removing a volume or section can silently remove its citations. `check_final()` compares results against that already-shrunken list.

    In-memory reproduction: `_sections_xml()` yielding nothing makes `items()` return `[]`, and `check_final([], [])` succeeds. The current files correctly reproduce 548 records; the completeness safeguard is incomplete.

12. **P2 — `verify_pins` does not check every pinned file, and supersession is an unconditional waiver.** [verify_pins.py:19](/home/tony/projects/levadura_salvaje/scripts/verify_pins.py:19), [verify_pins.py:44](/home/tony/projects/levadura_salvaje/scripts/verify_pins.py:44)

    The enumerator recognizes selected schemas only. It ignores explicit file/hash pairs such as `statute_results_file`/`statute_results_sha256` in obs-0139, `features`/`features_sha256` and `labels`/`labels_sha256` in obs-0150, and obs-0151’s `score_files`.

    Any superseded entry’s mismatch or missing file is labeled “explained,” without checking whether its successor explains that particular pin. The reported **143 successful checks and one obs-0163 mismatch reproduce**, and obs-0164 explains that specific mismatch. “Every file” and “only unexplained mismatches fail” remain broader than the implementation.

The W1–W7 verdicts follow **as numerical prediction outcomes**:

| Prediction | Reproduced outcome | Qualification |
|---|---:|---|
| W1 | 365/548 = 66.6% | Inside the predicted interval; directional reasoning failed. |
| W2 | 27/337 = 8.0% | Label transitions, not 27 verified hidden limits. |
| W3 | 52/188 = 27.7% | Label transitions, not 52 verified contextual corrections. |
| W4 | 34/45 = 75.6% | Agreement threshold passes. |
| W5 | 31/34 = 91.2% | Conditional on reader agreement. |
| W6 | Midpoint 69.7% | Below 75.4%; a sensitivity-range midpoint. |
| W7 | Reader A says `untimed` | The specified event occurred. |

“Structure cuts both ways” describes the transition counts, but its explanation is unproven and has counterexamples. Besides § 1.902-4 above, § 1.904-7 #92 flips **toward `time_limited` despite an explicit carry-forward rule into years beginning after December 31, 2004**. Also, **all 44 fallback excerpt hashes change**, and the system prompt changes. The statement that fallback input “didn’t change” is false.

Git history confirms the predictions precede the recorded results: prediction commit **`40a5099` at 14:48:54 UTC**, measurement commit **`5774504` at 14:57:28 UTC**, then audit commit **`5026359`**. Git alone cannot establish when the first model call began.

The tests miss these failure modes. In particular, [test_structure.py:41](/home/tony/projects/levadura_salvaje/tests/test_structure.py:41) compares slices against text derived from those same slices; it does not independently validate paragraph boundaries. There are no `excerpt_v3` tests for context selection, marker preservation, clipping, or fallback behavior, nor tests for probe overlap, missing XML coverage, or pin-schema coverage.

Verification: **22 applicable tests passed**; five answer-file tests were excluded under the read-only constraint. Independently, all **4,609 paragraph texts** matched normalized XML paragraph content, section coordinate text matched in all 73 sections, and all 548 final excerpt hashes validated. I found no demonstrated raw→flat→normalized offset bug in this population.