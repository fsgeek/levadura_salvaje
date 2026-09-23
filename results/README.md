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
