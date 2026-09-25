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
- `currency-audit-v1-2025.jsonl` — blind hand labels for 60 stratified
  sections plus the 14 AMT fossils, both passes and the adjudication.
  Ledger: obs-0133. Scorecard: docs/currency-scorecard.md.
- `fossil-audit-v2-2025.jsonl` — blind audit of the v2 extractor and
  resolver, same protocol as v1. Ledger: obs-0134.
- `dated-jev-v1-2025.jsonl` (+ `.partial.jsonl`) — the dated-period lens
  over the 1,675 fossil candidates (names_ended_period > silent >
  no_rules). Ledger: obs-0135.
- `dated-audit-v1-2025.jsonl` — blind hand labels for 60 sections, 20 per
  dated-lens label. Ledger: obs-0136. Scorecard: docs/dated-scorecard.md.
- `usc26-moves-119-4-119-110.jsonl` — each heading-changed identifier
  classified as move, ambiguous or replaced, with its new position.
  `cfr-moved-citations-v2-2025.jsonl` — every 2025 CFR citation through a
  moved provision, with the path it cites and where that rule is now.
  Ledger: obs-0137.
- `cfr-fossil-age-v2-2025.jsonl` — every citation of a repealed section
  with the year it was repealed. Ledger: obs-0138.
- `usc26-provisions-gpo-1996.jsonl` — 26 USC as published by GPO, current
  through 1997-01-06 (tag corpus/uscode-gpo-1996-1997), read by
  `gpo_usc.py`, with subdivisions inferred from HTML classes. It matches
  USLM on 98.2% of paths (recall) and 99.3% (precision) when the reader is
  run on the GPO 2023 edition. `cfr-usc-citations-v2-1997.jsonl` — the 1997
  CFR's Code citations resolved against it. Ledger: obs-0139.
- `fossil-audit-v2-1997.jsonl` — blind audit of 1997 citations against the
  GPO statute. Ledger: obs-0140. Scorecard: docs/fossils-1997-scorecard.md.
- `cfr-fossil-turnover-1997-2025.jsonl` — fate of each 1997 fossil
  candidate and origin of each 2025 one, by uniquely numbered sections.
  Ledger: obs-0141.
- `bounded-reader-v1-2025.jsonl` and `bounded-reader-v1/*.evidence.txt` —
  60 sections: panel ground truth, Haiku 4.5 readers without (A) and with
  (B) the ledger's evidence packet. Ledger: obs-0142. Scorecard:
  docs/bounded-reader-scorecard.md.
- `usc26-reuse-1997-2025.jsonl` — section headings 1997 vs 2025 with Jaccard
  (pairs below 0.5; reused = below 0.2); `cfr-cites-reused-1997-2025.jsonl`
  — 2025 CFR sections citing a reused section; ledger obs-0143.
  `usc26-reuse-1997-2025-classified.jsonl` — blind reuse/restructure/rename
  labels; ledger obs-0144.
- `bounded-reader-v2-2025.jsonl` and `bounded-reader-v2/*.evidence.txt` —
  v2: 120 fresh sections, panel blind to the packet, reuse flags in the
  packet. Ledger: obs-0145.
