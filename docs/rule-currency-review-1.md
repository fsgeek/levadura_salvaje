The recorded counts and verdict arithmetic reproduce. **The main overclaim is treating 82% (73–91) as a well-supported population estimate:** the calculation excludes consequential disagreements, and its bootstrap omits important uncertainty. I found no evidence that predictions were rewritten after their respective runs. No files were modified.

Findings ranked by severity:

1. **High — Excluding disagreements materially changes the audit adjustment.**  
   [Scorecard:79](/home/tony/projects/levadura_salvaje/docs/rule-currency-scorecard.md:79), [obs-0159:159](/home/tony/projects/levadura_salvaje/ledger/observations.jsonl:159).

   The calculation reallocates entire Qwen strata using only items on which readers agree:

   | Qwen stratum | Population | Consensus labels | Excluded |
   |---|---:|---|---:|
   | `untimed` | 337 | 12 untimed | 3 |
   | `time_limited` | 188 | 7 untimed, 5 time-limited | 3 |
   | `not_a_rule` | 23 | 2 untimed, 13 not-a-rule | 0 |

   Consequently:
   ```
   untimed = (337 × 12/12 + 188 × 7/12 + 23 × 2/15) / 548
           = 82.068%
   ```
   The arithmetic is correct. Its population interpretation requires agreement-selected items to represent excluded items within each stratum. That assumption is unsupported: disagreements concern headings, applicability, and historical inputs—the substantive classification problem.

   Using **all 15 answers per stratum**, reader A’s adjusted untimed estimate is **68.1%**, and reader B’s is **82.6%**. Assigning the six disputed items wholly outside/inside `untimed` yields a **65.8–84.9% sample sensitivity range**, before sampling uncertainty. These are sensitivity calculations, not confidence intervals.

   Exclusion is disclosed, but its effect and missingness assumption are not adequately explained. Adjudication or explicit disagreement sensitivity is needed before promoting 82% to the headline.

2. **High — The bootstrap reproduces, but “95% interval” overstates its coverage.**  
   [Scorecard:80](/home/tony/projects/levadura_salvaje/docs/rule-currency-scorecard.md:80), [obs-0159:159](/home/tony/projects/levadura_salvaje/ledger/observations.jsonl:159).

   I reproduced **72.9–90.9%** using 10,000 within-stratum resamples, seed 0. However, resampling the twelve unanimous `untimed` observations always produces twelve untimed labels. Thus the adjustment treats the classification precision of **337/548 citations—61.5% of the population—as certain**.

   The interval captures variation in the observed consensus labels, conditional on the selected consensus subset. It does not capture excluded disagreements, shared reader errors, missing context, or uncertainty about unseen error categories.

   The audit sampled without replacement; particularly for `not_a_rule`, 15/23 is a substantial sampling fraction. A design-based interval should address that finite population sampling. Omitting that correction can overstate that component’s variance, so every deficiency is not necessarily in the same direction. Repeated citations from the same rules also warrant a sensitivity analysis for correlated interpretation errors.

3. **High — Excerpt absence becomes evidence of currency, although the governing rule may be absent.**  
   [Excerpt function:114](/home/tony/projects/levadura_salvaje/src/levadura_salvaje/lenses/rule_currency.py:114), [example criterion:64](/home/tony/projects/levadura_salvaje/src/levadura_salvaje/lenses/rule_currency.py:64), [headline:88](/home/tony/projects/levadura_salvaje/docs/rule-currency-scorecard.md:88).

   The normalized coordinates and citation marking check out; I found no demonstrated offset bug. The weakness is the fixed 1,500-before/700-after window. It preserves the section heading but does not retrieve paragraph ancestry, the illustrated rule, or applicability provisions.

   Concrete examples: v2 item 13’s own example heading is **4,251 characters before** its citation; item 16’s is **2,584 characters before**. Both are outside the window. Yet v2 explicitly says an example is untimed unless the excerpt shows a historical limit.

   This supports “no limit visible in this excerpt,” more readily than “the rule, by its own words, still applies.” The ledger acknowledges omitted limits, but the headline does not carry that qualification. The same excerpts are used for the audit, so reader agreement cannot detect a limit omitted from everyone’s input.

4. **Medium — Resume and `record` lack the invariants their claims require.**  
   [Resume:94](/home/tony/projects/levadura_salvaje/scripts/measure_rule_currency_qwen.py:94), [finalization:120](/home/tony/projects/levadura_salvaje/scripts/measure_rule_currency_qwen.py:120), [record:130](/home/tony/projects/levadura_salvaje/scripts/measure_rule_currency_qwen.py:130).

   Cached answers are accepted by key, with only an excerpt hash checked at finalization. There is no validation of cached labels, prompt provenance, model identity, or inference settings. A malformed last JSONL line prevents resumption altogether.

   More seriously, `record()` does not reconstruct the expected population or verify completeness, uniqueness, excerpt hashes, or correspondence to the partial file. It can append an incomplete or stale final file while attributing it to the current prompt.

   I demonstrated these paths using in-memory mocks: resume accepted an invalid cached label from a different reported model; `record()` accepted a one-row final with an incorrect excerpt hash. **The committed files themselves are complete and consistent**—this is a script correctness defect, not evidence those runs were corrupted.

5. **Medium — Consensus contains a concrete applicability error.**  
   [v2 packet:21](/home/tony/projects/levadura_salvaje/results/rule-currency-audit-v2-902-packet.jsonl:21), [reader A:21](/home/tony/projects/levadura_salvaje/results/rule-currency-audit-v2-902-reader-a.jsonl:21), [reader B:21](/home/tony/projects/levadura_salvaje/results/rule-currency-audit-v2-902-reader-b.jsonl:21).

   Item 21 includes an exception allowing § 1.902-3 to apply before the year ownership requirements are first met, when they are first met after 1986. That endpoint has no stated calendar cutoff before 2025. Nevertheless, both readers label it `time_limited`; reader B quotes the general historical cutoff while overlooking the exception.

   Under the text-only criterion, “necessarily ended before 2025” does not follow. This item needs adjudication. Reclassifying this single consensus item from time-limited to untimed changes the adjusted estimate by **2.9 percentage points**, illustrating how consequential twelve-item strata are.

6. **Medium — Blinding is asserted, but not established by the artifacts.**  
   [Sampler description:6](/home/tony/projects/levadura_salvaje/scripts/audit_rule_currency.py:6), [key creation:48](/home/tony/projects/levadura_salvaje/scripts/audit_rule_currency.py:48), [reader instructions:3](/home/tony/projects/levadura_salvaje/results/rule-currency-audit-v2-902-instructions.md:3).

   The packets contain no Qwen labels. But the keys are written alongside them, and contain the labels explicitly. Results, predictions, prior audit answers, and potentially the other reader’s answers are accessible repository files.

   The committed instructions do not establish restricted access or prohibit reading these other files. There are no reader execution traces or context manifests here establishing what “fresh” readers inherited or opened. **Readers could have seen keys or labels; I found no evidence proving they did.**

   V2 also repeats **three exact v1 audit citations**. This creates an additional possible answer leak if prior artifacts or parent context were available. The disclosed Claude-family dependence is a separate confound; it does not address access-based blinding.

7. **Medium — V4/V6 meet their thresholds, but the improvement claim is confounded.**  
   [Scorecard:67](/home/tony/projects/levadura_salvaje/docs/rule-currency-scorecard.md:67), [interpretation:71](/home/tony/projects/levadura_salvaje/docs/rule-currency-scorecard.md:71), [V6 definition:23](/home/tony/projects/levadura_salvaje/predictions/2026-10-02-rule-currency-v2-claude.md:23).

   Both the prompt and audited sample changed. Equal allocation across **new Qwen labels** changes the sample composition: v1 contains eighteen identified examples, v2 seven. Four of v2’s seven come from § 1.952-1, and all seven receive untimed consensus. There is no demonstrated success here on examples illustrating explicitly historical rules.

   Example membership is determined from readers’ decisive text, rather than an independently fixed inventory. This can miss examples whose explanations omit the word.

   The observed 7/7 supports the stated sample threshold. It does not establish population agreement ≥80%; even an independent binomial interpretation gives a two-sided exact 95% lower bound of about **59%**. Likewise, “wording took” is plausible, but the 47%→87% comparison does not isolate wording’s causal effect.

8. **Medium — The audit sampler/scorer silently accepts inconsistent inputs.**  
   [Sampling:35](/home/tony/projects/levadura_salvaje/scripts/audit_rule_currency.py:35), [scoring:55](/home/tony/projects/levadura_salvaje/scripts/audit_rule_currency.py:55).

   Sampling joins final labels by volume/ordinal/index without verifying the stored source or excerpt hashes. Scoring silently overwrites duplicate item IDs, ignores extra answers, and accepts invalid labels. It checks missing answers, but does not bind readers’ answers to a particular packet hash.

   I demonstrated that two matching invalid labels become a “consensus” entry. The shipped reader files have valid, unique, complete IDs and labels, and both deterministic samples reproduce. These missing checks did not produce an observed counting error here.

9. **Low — “548 occurrences / every citation” is broader than the actual frame.**  
   [Population selection:42](/home/tony/projects/levadura_salvaje/scripts/measure_rule_currency_qwen.py:42), [prediction population:5](/home/tony/projects/levadura_salvaje/predictions/2026-10-02-rule-currency-claude.md:5), [results:539](/home/tony/projects/levadura_salvaje/results/rule-currency-qwen-v2-902-2025.jsonl:539).

   There are **548 extracted reference records but 547 distinct textual spans**. The inverted § 902(a)/(b) records at result lines 539–540 share the same span and excerpt. Counting both is defensible for reference targets, but contradicts “one question per citation occurrence.”

   The frame also inherits the extractor’s exclusion of section-range interiors. The corpus contains ranges such as “sections 901 through 905,” which include 902 without producing a 902 record. Describe the population as the pinned sidecar’s resolved § 902 reference records.

   Population reconstruction also lacks an explicit expected-set check: iterating a ZIP missing target-bearing sections would silently produce a smaller population. In the supplied ZIP, all 548 target records were recovered.

10. **Low — Some provenance and explanatory claims exceed what was recorded.**  
    [Prediction link:147](/home/tony/projects/levadura_salvaje/scripts/measure_rule_currency_qwen.py:147), [Qwen explanation:32](/home/tony/projects/levadura_salvaje/docs/rule-currency-scorecard.md:32), [scorer output:67](/home/tony/projects/levadura_salvaje/scripts/audit_rule_currency.py:67).

    Obs-0158 points to the **v1 prediction file**, because the measurement script hardcodes that path. The audit scorer does not implement the adjusted estimate, bootstrap, or example classification recorded in obs-0159; these require a separately reconstructed calculation.

    Also, “Qwen … because an example isn’t a rule” is an inferred explanation. Qwen supplied labels only, and labeled examples **12 not-a-rule, 5 untimed, 1 time-limited**. The evidence supports an example-related ambiguity, not a demonstrated single consistent Qwen policy.

Every numerical verdict in the [scorecard tables](/home/tony/projects/levadura_salvaje/docs/rule-currency-scorecard.md:15) follows under the apparent convention that interval predictions pass when the observed sample statistic falls within the stated range:

| Verdict | Recomputed evidence | Assessment |
|---|---|---|
| R1 pass | 275/548 = 50.2% | Supported |
| R2 pass | 214/548 = 39.1% | Supported |
| R3 pass | 59/548 = 10.8% | Supported |
| R4 fail, low | 5/59 = 8.5% | Supported as a comparison of model labels; “current only because of other rules” is stronger |
| R5 fail | 34/54 = 63.0%, below 70% | Supported |
| R6 pass | 17/17 time-limited | Count supported; semantic reliability weakened by item 21 |
| R7 pass | 65/96 = 67.7%, above 60% | Supported |
| R8 fail, high | 20/21 = 95.2%, above 88% | Supported; conditional on reader agreement |
| R9 fail | 21/45 = 46.7% | Supported |
| V1 pass | 38/59 moved, all to untimed | Supported; two v2 sampled examples still receive Qwen `not_a_rule` |
| V2 pass | 337/548 = 61.5% | Supported |
| V3 pass | 4 of the same 59 sections | Supported as a model-label gap |
| V4 pass | 39/45 = 86.7% | Supported for the new balanced sample |
| V5 pass | 30/39 = 76.9% | Within 70–95%; does not demonstrate 85% agreement |
| V6 pass | 7/7 identified examples | Supported narrowly; weak generalization |

The commit sequence supports prospective predictions: v1 predictions enter at `2a8c173` (14:44:23 PDT), followed by their stamp; v1 results/audit and v2 predictions enter at `df3102f` (15:11:18), followed by their stamp; v2 results enter at `628454e` (15:25:47). Ledger recording times are consistent with that sequence. Stored result, partial, audit-file, and prompt hashes check out, and the ledger verifies.

The v2 decisions are **reasonable operational choices**, especially treating hypothetical dates differently from rule applicability and distinguishing historical inputs from historical applicability. The example decision is justified as a definition for this lens, provided the illustrated rule’s timing is actually available. Carryovers largely clarify v1’s existing no-end-date criterion; pointers sharpen an existing cross-reference category.

Calling V1–V6 “passes” is therefore fair as **prospective checks of an audit-informed revision**. The v2 predictions explicitly disclose that status. Calling them six independent confirmations of correctness, or treating the adjusted headline as validated rule currency across the corpus, would overclaim.