# Predictions: how often is an eCFR "substantive" version only editorial, and does a cheap classifier notice what the instrument can't? (Claude)

*Written 2026-11-03 by the steward (Claude Opus 5.5), and stamped before any measurement. The
fetch of raw texts (scripts/fetch_title12_versions.py) began before this file. Fetching measures
nothing, and no fetched text has been read.*

## Why

The replay's smoke-1 found that the eCFR versioner records an amendment-announcement notice as a
substantive version on the publication date. A research instance (Haiku) noticed it before the
steward's instrument did (results/replay/smoke-1/NOTES.md, note 3). Tony asked (2026-11-03)
whether cheap classifiers might still be useful. This study tests one role for them: a
*second instrument*, built differently from the deterministic one, run over the whole population.
The informative output is where the two disagree.

## What I knew

- In smoke-2's twin parts, 14 of 33 changed sections on 6 dates were announcement-only
  (results/replay/smoke-2/flags.jsonl). Those dates were chosen as twin-part change dates, not
  at random.
- The announcements preceded their effective changes by 60 to 90 days (91 FR 21668: 04-22 to
  07-21; 91 FR 23604–23606: 05-01 to 06-30).
- **Population:** 504 title 12 section versions (not removed) issued 2025-06-16 to 2026-10-23, 475
  marked `substantive` by the versioner (versions API, fetched 2026-11-02).

## Population and instruments

- **Population:** every title 12 section version, type `section`, not removed, issued on or after
  2025-06-01. Each pairs its text on its amendment date with its text on the day before.
- **Deterministic label** (src/levadura_salvaje/ecfr.py):
  - `announcement_only`: the regulation text, with announcement notices masked, is unchanged and
    a new notice was added;
  - `unchanged_other`: the masked text is unchanged and no new notice was added;
  - `text_changed`: the masked text differs.
- **Classifier:** Haiku 4.5 via OpenRouter. It sees the section number and a word-level diff
  (difflib opcodes, capped at 6,000 characters) and answers `editorial` or `substantive`, with one
  sentence of reason. It has no access to the deterministic label. It runs on every version.
- **Blind audit:** every disagreement on a `text_changed` version (deterministic says the text
  changed; the classifier says `editorial`), plus 20 random agreements as controls. Two readers
  (Opus, Sonnet) are each shown the diff and asked "does this change what the rule requires,
  permits or covers?" They are not told either instrument's label. A and B order is random.

## Predictions

| | Prediction | Point | Interval |
|---|---|---|---|
| E1 | Share of `substantive`-marked versions that are `announcement_only` | 30% | 15–50% |
| E2 | Share of `substantive`-marked versions that are `unchanged_other` (editorial changes the mask doesn't name) | 5% | 1–15% |
| E3 | The classifier says `editorial` on `announcement_only` versions | ≥ 90% | pass/fail |
| E4 | Share of `text_changed` versions the classifier calls `editorial` | 15% | 5–30% |
| E5 | **The plumber test.** Among E4's disagreements, both blind readers side with the classifier (no change to what the rule requires, permits or covers) | ≥ 50% | pass/fail |
| E6 | Among the 20 agreement controls, both readers judge the change substantive | ≥ 17 of 20 | pass/fail |

**What each outcome teaches.**
- **E1 high:** the eCFR's own label is a poor change signal, and a watcher must filter it.
- **E5 pass:** a cheap classifier catches real instrument errors, which is a role worth keeping.
- **E5 fail with E4 high:** it is noise, and its disagreements cost more audit than they return.
- **E3 fail:** the classifier can't see even the known editorial class, and no other role for it
  should be tried until that's understood.

Cost is measured from the run and reconciled with OpenRouter, not estimated here.
