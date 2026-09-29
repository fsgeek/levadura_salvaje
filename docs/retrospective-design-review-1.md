# Review of retrospective design draft 1 (Codex, verbatim)

*Prompt: `results/…` not stored; reproduced below the review.*

**Draft 1 cannot support its claimed leakage measurement.** The underlying descriptive prediction experiment is salvageable.

Recomputed from the citation files using the turnover script’s unique-number filter:

| Population | Verified counts |
|---|---|
| 1997 sections | 4,983 records; 3,759 unique-number records retained |
| T1 | 1,137 = 806 still + 151 cured + 180 gone |
| T2 eligible non-fossils | 2,622 = 207 turned + 2,053 surviving non-fossils + 362 absent |
| “869” | 207 turned + 662 classified as new; **not 869 onsets among 1997 sections** |

**CRITICAL**

1. **The leakage estimator is unidentified.** [(Design)](/home/tony/projects/levadura_salvaje/docs/retrospective-design-draft-1.md:50)  
   `(H − H−) − (B1 − B1−)` assumes masking destroys equal amounts of legitimate predictive signal in radically different models. Nothing establishes that. Residual recognition, semantic damage and interactions can move the estimate either way; it is **not even a justified lower bound**. H’s advantage over M/B1 also includes model capacity and general knowledge differences.  
   **Fix:** report masking sensitivity only. To estimate a causal contamination effect, randomize future-information exposure between otherwise identical models. For actual foresight, use a frozen model and prospectively collected outcomes.

2. **T2 lacks a complete outcome definition and label table.** [(Script)](/home/tony/projects/levadura_salvaje/scripts/measure_fossil_turnover.py:34)  
   The turnover file omits T2 negatives. Treating its absent rows as negatives conflates 2,053 surviving non-fossils with 362 disappearances. Restricting to survivors instead conditions on a future event. Two snapshots establish endpoint status, not whether fossilization ever occurred and subsequently reversed.  
   **Fix:** materialize all 2,622 rows; define a three-way endpoint—fossil, non-fossil, absent—or explicitly make survivor-conditional prediction the estimand. Exclude the 662 “new” rows.

3. **“Fate” currently means identifier/extractor status, not regulatory decay.** [(Scorecard)](/home/tony/projects/levadura_salvaje/docs/fossils-1997-scorecard.md)  
   “Gone” means number absent, not repeal. “Cured” means zero detected broken references, not repaired law: **18/151 cured sections have unchanged text**. “Still” need not retain the original broken citation. Reused statutory identifiers can conceal stale references. The 1997 audit confirms only 49/60 flagged citations; that is not section-level label accuracy.  
   **Fix:** either rename targets to literal observed statuses and narrow conclusions, or adjudicate regulatory continuity and citation-level transitions, separating moves, replacements, statutory changes and extraction errors.

**HIGH**

4. **Existing feature artifacts cross the curtain.** [(Age script)](/home/tony/projects/levadura_salvaje/scripts/measure_fossil_age.py:22)  
   Existing repeal ages derive from **2025 citations and USC 119-4**. Filtering their years to ≤1997 would not remove selection by later survival/status. Existing mini-AGI scores read **2025 text**. By contrast, obs-0139’s broken counts genuinely resolve against GPO-1996; its separate modern validation does not itself contaminate those counts.  
   **Fix:** build inputs from an allowlist of historical source hashes. Recompute repeal/amendment features from historical documents; mark unavailable dates missing. Keep 119-4 exclusively in outcome construction.

5. **Mini-AGI’s held-out promise is insufficiently specified.** [(Scorer)](/home/tony/projects/levadura_salvaje/scripts/minagi_score.py:78)  
   Existing weights trained on 95% of 1997 sections; they cannot provide unseen-section scores for the full cohort. Holding out record IDs also permits duplicate text across folds: the source contains **593 repeated text-hash groups**. The earlier insignificant memorization comparison does not establish absence of memorization.  
   **Fix:** score only 1997 text using fresh, grouped out-of-fold training; keep duplicate/near-duplicate sections together, freeze preprocessing and learning, and record training membership per prediction.

6. **No learning/evaluation protocol exists for B0, B1 or M.**  
   Features and surprise scores are not three-class forecasts. Fitting their mappings, thresholds or calibration to evaluation outcomes leaks labels. A B0 computed from the entire endpoint cohort is an oracle-prevalence reference, not a 1997 forecast. Designer knowledge of existing results also makes later stamping insufficient for confirmatory claims.  
   **Fix:** freeze mappings or use grouped, nested train/test separation; distinguish retrospective supervised prediction from historically available forecasting. Reserve an untouched cohort or call this exploratory.

7. **The optional “leakage impossible” control is invalid.**  
   Anthropic distinguishes Haiku’s **February 2025 reliable knowledge cutoff from July 2025 training-data cutoff**, overlapping OBBBA. Earlier proposals can also reveal later changes. Performance on statute headings cannot bound performance on regulatory fates. [Official specifications](https://platform.claude.com/docs/en/models/overview)  
   **Fix:** remove the impossibility/bounding claims; use outcomes arising after a pinned model’s verified training boundary, preferably collected prospectively.

8. **Selection and imbalance can manufacture apparent utility.**  
   T1’s majority class is **70.9%**. T2 positivity is **7.9%** across all eligible sections, or **9.2%** among survivors. Outcome-stratified sampling changes calibration and precision unless weighted. Missing 1997 volumes and excluded duplicate-number records limit generalization.  
   **Fix:** publish eligibility and sampling probabilities, weight population metrics, report per-class recall and precision–recall performance, and include majority/prevalence baselines.

**MEDIUM**

9. **Metrics and uncertainty are underspecified.**  
   Multiclass AUC needs an averaging convention; macro-F1 needs a decision rule. Sections sharing statutory references can fail together, making independent-section bootstrap intervals optimistic.  
   **Fix:** preregister a primary metric, probability/threshold rules and paired comparisons; bootstrap meaningful regulatory/citation clusters.

10. **The quoted budget is understated.**  
    At standard Haiku pricing, 4,474 × 2,500 input tokens already costs **$11.19**, before outputs. Another 100 output tokens/call adds **$2.24**. Batch pricing could make $6–8 plausible, but must be specified. T1 averages **13,936 characters**, so 2.5k tokens needs measurement. Three seeds across k folds require **3k training runs**, plus scoring. [Pricing](https://www.anthropic.com/claude/haiku?m=1)  
    **Fix:** tokenize the actual cohort, budget outputs/retries and long sections, specify batch use, and benchmark the complete fold schedule.

**Verdict: redesign.** Retain a carefully labeled endpoint-prediction benchmark; replace the claimed leakage estimator and post-cutoff control.
---

## Prompt

You are an adversarial reviewer from another model family. Review the experimental design in docs/retrospective-design.md (draft 1) in this repository. The designer (Claude) wants the experiment to be informative and may be biased toward designs that make a contaminated forecaster look foresightful or that make leakage look measurable when it is not.

You may read anything in the repository: docs/findings-2026-09-24.md, docs/fossils-1997-scorecard.md, docs/minagi-scorecard.md, docs/mini-agi-as-instrument.md, the ledger (ledger/observations.jsonl), results/cfr-fossil-turnover-1997-2025.jsonl and the scripts that produced them (scripts/measure_fossil_turnover.py etc.).

Find: (1) CRITICAL flaws that would make results uninterpretable; (2) HIGH issues; (3) MEDIUM. Specifically check: whether the targets T1/T2 are defined and measurable from existing files (verify counts); whether any leak-free arm actually leaks post-1997 information (e.g. features computed from later documents, repeal years, the 119-4 statute); whether the identity-ablation leakage estimate (H - H-) - (B1 - B1-) is identified or confounded; whether "gone" and "cured" are clean classes; whether mini-AGI scoring avoids read-it-already contamination; base rates and class imbalance; cost realism. For each issue give a concrete fix. End with a verdict: proceed / proceed after fixes / redesign. Be terse. Markdown.
