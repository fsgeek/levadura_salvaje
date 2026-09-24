# Results

Per-section outputs of instruments, one JSONL line per section, keyed by
`volume_file` + `ordinal` (section numbers repeat in 1997). The ledger holds
one entry per volume that cites the file by sha256; the file is the detail,
the ledger is the claim.

## Known quirks

- **amt-baseline v1**: the phrase "minimum taxable income" is shadowed by
  "alternative minimum tax", which matches first at the same position in
  "alternative minimum taxable income". Positivity is unaffected; the
  `by_phrase` counts undercount it. Left as registered; a v2 would use
  overlapping matches.

## Files

- `amt-baseline-v1-<edition>.jsonl` — keyword + citation baseline, per section.
- `amt-jev-v1-<edition>.jsonl` — the AMT lens, per section: label from the
  strongest chunk, that chunk's probabilities, all chunk labels, request ids.
- `amt-jev-v1-<edition>.partial.jsonl` — the raw per-call record the run
  resumes from: one line per Jev call (or refusal), in completion order.
  Keys written before budgets were added (`vol#ord#sha#k`) are read as
  budget 40000. 35 chunks were refused as `max_tokens_exceeded` (21 in
  1997, 14 in 2025) and their sections re-split at a smaller budget.
- **amt-jev v1 note**: `confidence` is TypeSafe's (n·p_max − 1)/(n − 1),
  not a top-two margin, and probabilities are rounded to 2 decimals.
- `jev-repeat-v1.jsonl` — every wire state (header + chunk text, by sha256)
  the AMT lens sent to Jev more than once, with each call's label and
  probabilities and the widest per-label spread. Ledger: obs-0122.
- `usc26-provisions-<release point>.jsonl` — every identified provision of
  26 USC (section down to subitem): identifier, level, status, heading,
  character count, and sha256 of its text without notes. Ledger:
  obs-0123 (119-4), obs-0124 (119-110), obs-0125 (the diff).
  Repealed runs of sections share one element with a range identifier,
  e.g. `/us/usc/t26/s4471...4474`; readers must expand these.
- `cfr-usc-citations-v1-2025.jsonl` — every Code citation the v1 extractor
  found in each 2025 CFR section, with its outcome against 26 USC at 119-4
  and 119-110. Ledger: obs-0126 (119-4), obs-0127 (119-110).
  **Known v1 resolver bugs** (found after the run, fixed in v2): USLM writes
  section numbers like 1400Z–2 with an en dash, so hyphenated CFR citations
  of them read as absent-section; range identifiers whose endpoint has a
  dash suffix (`s1400L...1400U–3`) were skipped, so those sections read as
  absent-section, not repealed.
- `cfr-usc-citations-v2-2025.jsonl` — the same with extractor v2 and
  resolver v2 (en-dash and range fixes). Ledger: obs-0129, obs-0130.
- `fossil-audit-v1-2025.jsonl` — the blind audit of v1: 100 broken and 30
  control occurrences, both passes, adjudications, and final judgments.
  Ledger: obs-0128. Scorecard: docs/fossil-scorecard.md.
- `usc26-reuse-119-4-119-110.jsonl` — identifiers whose heading changed, or
  that are in force at 119-110 but absent or repealed at 119-4, with both
  headings. Ledger: obs-0131. Scorecard: docs/reuse-scorecard.md.
- `currency-jev-v1-2025.jsonl` (+ `.partial.jsonl`) — the currency lens
  over the 1,675 fossil-candidate sections: section label (current >
  historical > no_rules), the deciding chunk's probabilities, each section's
  citation and broken counts. Ledger: obs-0132.
