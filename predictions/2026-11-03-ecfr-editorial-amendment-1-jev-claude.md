# Amendment 1 to the eCFR editorial predictions: Jev as a second classifier (Claude)

*Written 2026-11-03 and stamped before any measurement, like the original
(predictions/2026-11-03-ecfr-editorial-claude.md, stamped at 8574b1c). Nothing in the original changes.*

## Why

Tony (2026-11-03): Jev was meant as "a mechanism by which you can chew through large blobs of text and
see if it is worth making it a candidate for study." The record supports that role better than the
steward first said. In the currency lens, a blind hand audit agreed with Jev on 56 of 60 (obs-0133,
docs/currency-scorecard.md). What failed was distilling Jev into a fastText student
(docs/distill-scorecard.md) and the investigator pilot. Jev joins this study as a second cheap
instrument beside Haiku: a System One classifier against a small LLM.

## What I knew

- One Jev call, to confirm access: a made-up diff ("at least 100" to "at least 1,000 covered
  originations"), labeled `substantive` at 0.99 by `jev-1.13.0`. It used no corpus text.
- Jev's window is 32k tokens per call. The diff cap (6,000 characters) fits well inside it.

## Added instrument

- **Model:** `jev-1.13.0`, pinned.
- **Input:** the same diff Haiku sees, in a state field `diff`, with the section number in a header line.
- **Question:** one Choice. The instructions and criteria restate the original prompt's two
  definitions, `editorial` and `substantive`, word for word.
- **Recorded:** label, probabilities, confidence and request id. It never sees the deterministic
  label or Haiku's.
- **The audit packet** adds every `text_changed` version where Jev says `editorial` and Haiku doesn't,
  so each classifier's disagreements with the instrument are judged the same way.

## Predictions

| | Prediction | Point | Interval |
|---|---|---|---|
| J1 | Jev says `editorial` on `announcement_only` versions | ≥ 90% | pass/fail |
| J2 | Share of `text_changed` versions Jev calls `editorial` | 15% | 5–30% |
| J3 | Jev and Haiku agree on `text_changed` versions | 85% | 75–95% |
| J4 | Among `text_changed` versions Jev calls `editorial`, both blind readers side with Jev | ≥ 50% | pass/fail |
| J5 | Jev's precision on its `editorial` calls (J4's share) is at least Haiku's (E5's share) | yes | pass/fail |

J5 is the plumber test between the two cheap instruments: whether the cheaper, less general one
notices as well.
