# Predictions: rule-currency lens v3, excerpts from paragraph structure

*Written 2026-10-03 by the owning instance (Claude Opus 5.5), before any v3 call. v3 keeps v2's
question and labels. It changes what the judge sees: the section heading, the opening of each
ancestor paragraph, the worked example and what introduces it, the citation's own paragraph,
and the section's applicability paragraph (`src/levadura_salvaje/structure.py`,
`rule_currency.excerpt_v3`; design in docs/rule-currency-v3-design.md).*

*Known before the run, from building the excerpts (not predictions):*
- *476 of 548 excerpts come from structure;*
- *28 attach a table or extract citation to the paragraph before it;*
- *44 fall back to v2's window, 43 because a designator chain failed and 1 in a table-of-contents heading;*
- *excerpts average 2,077 characters (largest 4,135), and none is truncated.*

*Same 548 records, the same Qwen3.8-27B settings and lease. A fresh blind audit: two new readers
(fresh subagents, one Opus and one Sonnet), 15 per v3 label (seed 2). Plus one fixed probe:
1.902-3 #49 (v2 audit item 21), the ownership exception both v2 readers labelled `time_limited`
where the text supports `untimed`. Its access log is extracted from the transcripts afterwards,
as in v2.*

| | Prediction |
|---|---|
| W1 | Qwen v3 `untimed`: 58% (45–70). v2 was 61.5%. Seeing the governing limits should move some citations to `time_limited`. |
| W2 | **What the window hid.** Of v2's 337 `untimed`, the share that v3 labels `time_limited`: 10% (3–20) |
| W3 | Of v2's 188 `time_limited`, the share v3 labels `untimed`: 15% (5–30). Qwen's past-period-amount error mostly persists. |
| W4 | the two new readers agree: 85% (75–95) |
| W5 | their consensus agrees with Qwen v3: 80% (65–92) |
| W6 | the audit-adjusted `untimed` range (computed by `audit_rule_currency.py adjust`) has a midpoint below v2's (75.4%). p = 0.6 |
| W7 | the probe, 1.902-3 #49: at least one v3 reader labels it `untimed`. p = 0.6 |

W2 is the number v3 exists for. If it is near zero, v2's window wasn't hiding much, and the
review's concern (#3), though correct in principle, didn't move the measurement.
