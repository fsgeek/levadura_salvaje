# Scorecard: how often is an eCFR "substantive" version only editorial, and do cheap classifiers notice? (obs-0187, obs-0188)

*2026-11-03.*
- **Predictions:** `predictions/2026-11-03-ecfr-editorial-claude.md` (stamped at 8574b1c) and amendment 1,
  Jev (stamped at 89c11f7), both before any measurement.
- **Records:** `results/ecfr-editorial/`.
- **Question:** Tony's (2026-11-03): might cheap classifiers still be useful?

## The answer

- **The eCFR's own "substantive" flag is wrong more often than right** in title 12 since June 2025. Of 408
  flagged version pairs:
  - 140 (34.3%) change nothing but an amendment-announcement notice;
  - at least 75 more are text changes that two blind readers both judged editorial.
- **The deterministic instrument overcounts too.** "The text changed" includes "must" → "shall", office
  renamings and cross-reference updates. At least 75 of its 288 text changes are editorial.
- **Cheap classifiers notice this.** Of the text changes Haiku called editorial, both readers agreed on 67.6%
  (75/111). For Jev the figure was 55.1% (65/118).
- **They must not be used as filters.** Both readers judged 23 of Haiku's editorial calls substantive, and 43
  of Jev's. A filter built on either would hide real rule changes. Used as a second opinion that ranks
  probable noise, leaving the decision to a reader, they earn their cost: Haiku cost $0.25 for 429 diffs.
  This is the first wander's warning made concrete: "when a cheap judgment selects what gets examined, its
  errors hide in whatever wasn't selected."

## Predictions

| | Prediction | Result | |
|---|---|---|---|
| E1 | 30% (15–50%) of substantive-flagged versions are announcement-only | 34.3% (140/408); 29.5% with the 66 flagged new sections | **hit** |
| E2 | 5% (1–15%) unchanged but not an announcement | 0% | miss, low |
| E3 | Haiku calls ≥ 90% of announcement-only versions editorial | 140/140 | **vacuous** (see deviations) |
| E4 | Haiku calls 15% (5–30%) of text changes editorial | 38.5% (111/288) | miss, high |
| E5 | ≥ 50% of E4's calls confirmed editorial by both readers | 67.6% (75/111) | **pass** |
| E6 | ≥ 17 of 20 agreement controls judged substantive by both | 18/20 | **pass** |
| J1 | Jev calls ≥ 90% of announcement-only versions editorial | 140/140 | **vacuous** |
| J2 | Jev calls 15% (5–30%) of text changes editorial | 41.0% (118/288) | miss, high |
| J3 | Jev and Haiku agree on 85% (75–95%) of text changes | 77.4% (223/288) | **hit** |
| J4 | ≥ 50% of Jev's editorial calls confirmed by both readers | 55.1% (65/118) | **pass** |
| J5 | Jev's precision ≥ Haiku's | 55.1% vs 67.6% | **fail** |

E4 and J2 missed high because the steward underestimated the eCFR's editorial churn, not because the classifiers
were noisy: most of the extra calls were confirmed.

## Deviations, declared

1. **New sections (found in the dry run, before measurement).** 74 of the 504 versions are sections new on their
   date, such as part 1077 on 2026-10-01, with no text the day before. The predictions didn't anticipate them.
   They are reported as their own class (`new_section`, 66 of them flagged substantive), and E1 is given both
   with and without them. One version had a genuine fetch error.
2. **E3 and J1 are vacuous.** The classifiers saw the diff of the *masked* texts. For announcement-only versions
   that diff is empty, so both saw "(no difference)". The predictions said only "a word-level diff". The steward
   didn't notice until after the run. To test this properly, the classifiers would have to see the unmasked
   diff that contains the notice.
3. **Reader B was replaced.** The first Sonnet reader read the diffs cut to about 1,000 characters, wrote a hand
   list of 71 `substantive` ids, and gave every other item `editorial` by default. That is the label the test
   asks readers to confirm, so the shortcut could not fail in the classifiers' disfavor. Its output is kept
   (`audit/reader-b-invalid-default-editorial.jsonl`) and not scored. A second pass ran under
   `audit-instructions-v2-addendum.md`: no default, read every diff whole, decisive text verbatim. It quoted
   verbatim on 167 of 167, checked mechanically. Reader A (Opus) read every batch whole and labeled each item
   individually. It paraphrased its decisive text on 72 items, which its instructions allowed.

## Limits

- The eCFR is editorial, not the official CFR.
- "Editorial" is judged from a diff capped at 6,000 characters, without the full section.
- Both readers are Claude models. They agreed on 154 of 167 items.
- Jev's cost wasn't measured.
- The new-section class isn't audited.
- One prompt, one model version each. A classifier that is less precise here, like Jev, may do better on
  another question, as it did on the currency lens (56 of 60 agreement, obs-0133).
