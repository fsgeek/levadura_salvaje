# Audit instructions: does this change alter the rule?

You are a blind reader. Each item in `audit-packet.jsonl` is one change to one section of 12 CFR
(U.S. banking regulations). It is shown as a word-level diff between the section's text the day
before an amendment date and on that date. Each diff line is: `op | before | after`.

For each item, answer one question:

**Does this change alter what the rule requires, permits, prohibits, or whom or what it covers?**

- `substantive`: yes. For example, a new duty, a changed threshold, an added or removed exception,
  a changed scope or definition that matters to coverage, or a changed effective date of an
  obligation.
- `editorial`: no. For example, renumbering, a cross-reference update with no change of meaning,
  a typo fix, a source or authority note, formatting, or a notice about another document.
- `unclear`: the diff doesn't show enough to decide. Say what's missing.

Judge only from the diff. Don't look anything up. You aren't told how anyone else labeled these
items, and nothing in an item's position or number says anything.

Write one JSON line per item to your output file:
`{"item": "item-001", "label": "substantive" | "editorial" | "unclear", "decisive_text": "<the words in the diff your judgment rests on>", "note": "<one sentence>"}`
