# Review of retrospective design draft 2 (Codex, verbatim)

Draft 2 resolves several review-1 findings substantively, but **“identified by construction” remains too strong**.

Recomputed from the citation files using the turnover filter:

| 1997 stratum | Absent | Present-broken | Present-clean | Total |
|---|---:|---:|---:|---:|
| Fossil | 180 | 806 | 151 | 1,137 |
| Non-fossil | 362 | 207 | 2,053 | 2,622 |
| Total | 542 | 1,013 | 2,204 | 3,759 |

The 4,983 original records yield 3,759 unique-number records. None of the 542 absences is caused by excluding a duplicated 2025 number.

**CRITICAL**

1. **The exposure intervention is contradictory.** [Lines 60–74](docs/retrospective-design.md:60) require training only on other folds, yet invoke familiarity with held-out sections’ surviving 2025 text as the mechanism. Excluding those counterparts removes direct contamination; including them violates the unqualified fold rule.  
   **Fix:** explicitly restrict **1997** training by fold; separately specify whether held-out sections’ 2025 counterparts enter contaminated training. Randomize and record actual exposure.

2. **Corpus replacement is not an isolated measurement of leakage.** At fixed bytes, more 2025 text means less 1997 training. Differences combine historical-training displacement, general distribution changes, and target-specific future knowledge. The contrast can identify a specified corpus-mixture intervention, but cannot separately identify memorized-survival inflation. “25%” also leaves corpus coverage versus sampling proportion undefined.  
   **Fix:** name the estimand as corpus-mixture effect, or add an equal-budget control with the same historical exposure and future-text dose but withheld evaluation counterparts. Freeze sampling, order, and dose definitions.

**HIGH**

3. **The logistic mapping can learn from in-sample surprise.** An “inner split” of labels does not ensure its calibration sections were excluded from reader training. Training the mapping on familiar sections and evaluating on unfamiliar sections can manufacture arm differences. [Protocol](docs/retrospective-design.md:62)  
   **Fix:** use disjoint reader-training, mapping-training, and evaluation groups, or nested cross-fitting that produces genuinely unseen historical-text scores for mapping training too. Explicitly require fresh random initialization and historical-only duplicate grouping.

4. **“No future” still excludes an important dependency: future labels.** B0, B1 and M0 mappings learn other sections’ 2025 outcomes. That supports retrospective supervised prediction, not a forecast available in 1997. Review 1’s distinction remains unresolved.  
   **Fix:** call them “no future-text exposure” arms and scope conclusions accordingly; historical forecasting requires earlier completed training horizons.

5. **Seed uncertainty is unsupported.** The old 0.042 figure is median per-section seed spread in surprise, not uncertainty in paired multiclass log-loss differences. Comparing them mixes different quantities. Adding seeds conditionally on the observed result compounds the problem. [Budget](docs/retrospective-design.md:91)  
   **Fix:** precommit multiple paired seeds and independently randomized exposure samples; estimate uncertainty in the actual primary contrast.

6. **Part bootstrap does not establish citation-cluster independence.** References cross parts, and part 1 contains **2,245/3,759 sections (59.7%)**. Resampling parts can omit or multiply most of the population; it also misses training randomness.  
   **Fix:** define the inference population, inspect citation-sharing clusters, and report sensitivity to clustering plus repeated training. Keep finite-cohort descriptive contrasts explicit.

**MEDIUM**

7. **Imbalance handling is improved but incomplete.** Majority shares are **70.9%** in fossils, **78.3%** in non-fossils, and **58.6%** pooled. Present-clean is also a minority within fossils (13.3%), omitted from the named minority metrics.  
   **Fix:** include historical-stratum-conditioned B0, all-class PR metrics, and explicit recall decision rules and calibration conventions.

8. **The cost estimate covers training only.** Fifteen runs imply about **147M training bytes**; one evaluation pass per dose already requires about **100M bytes** over the cohort, before mapping scores, inner retraining, benchmarks or additional seeds.  
   **Fix:** benchmark the complete split/scoring schedule and quote total GPU hours. API $0 is credible.

**Review-1 resolution:** T2 is now fully definable from existing files, although the complete label artifact remains to be built. The identity-ablation estimator and invalid cutoff control are genuinely removed. Historical broken counts genuinely resolve against GPO-1996; the modern validation does not contaminate those counts. The allowlist excludes the leaking repeal-age artifacts and existing 2025 mini-AGI scores. Renaming “gone/cured” resolves the interpretation problem **only for literal identifier/extractor outcomes**—these remain unsuitable as adjudicated regulatory decay classes. Also, the 662 excluded rows are “classified new,” not all genuinely new.

**Verdict: proceed after fixes.**
---

## Prompt

You are an adversarial reviewer from another model family. Review the experimental design in docs/retrospective-design.md (draft 2; draft 1 and your review 1 are in docs/retrospective-design-draft-1.md and docs/retrospective-design-review-1.md — check that review 1 findings are actually resolved, not just reworded) in this repository. The designer (Claude) wants the experiment to be informative and may be biased toward designs that make a contaminated forecaster look foresightful or that make leakage look measurable when it is not.

You may read anything in the repository: docs/findings-2026-09-24.md, docs/fossils-1997-scorecard.md, docs/minagi-scorecard.md, docs/mini-agi-as-instrument.md, the ledger (ledger/observations.jsonl), results/cfr-fossil-turnover-1997-2025.jsonl and the scripts that produced them (scripts/measure_fossil_turnover.py etc.).

Find: (1) CRITICAL flaws that would make results uninterpretable; (2) HIGH issues; (3) MEDIUM. Specifically check: whether the targets T1/T2 are defined and measurable from existing files (verify counts); whether any leak-free arm actually leaks post-1997 information (e.g. features computed from later documents, repeal years, the 119-4 statute); whether the identity-ablation leakage estimate (H - H-) - (B1 - B1-) is identified or confounded; whether "gone" and "cured" are clean classes; whether mini-AGI scoring avoids read-it-already contamination; base rates and class imbalance; cost realism. For each issue give a concrete fix. End with a verdict: proceed / proceed after fixes / redesign. Be terse. Markdown.
