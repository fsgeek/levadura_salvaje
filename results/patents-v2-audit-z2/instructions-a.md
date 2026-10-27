# Audit Z2a: does this patent rule refer to pre-AIA law here?

You are a blind reader. Read only this file and `packet-a.jsonl` in the same directory. Do not open any other
file in the repository, and do not search the web.

Each item is a citation to title 35 of the U.S. Code (the Patent Act) in a 2025 patent rule (37 CFR).
`citation_as_read` is the span a program read; `excerpt` is the passage around it. The America Invents Act
(AIA) changed parts of title 35, mostly effective March 16, 2013, but older law still governs some
applications and proceedings.

For each item, answer:
- **pre_aia**: "yes" if, at this citation, the rule refers to the law as it stood before the AIA's changes (by a
  stated date, by saying "pre-AIA", or unmistakably by context); "no" if it refers to current law; "unclear".
- **how**: "stated" (a date or "pre-AIA" appears with the citation), "context" (only the surrounding procedure
  shows it), or "" (if pre_aia is not "yes").
- **note**: one sentence.

Write one JSON object per line, in item order, to the output file named in your task:
`{"item": "a-01", "pre_aia": "...", "how": "...", "note": "..."}`
