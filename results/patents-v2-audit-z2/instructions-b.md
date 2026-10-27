# Audit Z2b: does this passage state an applicability condition beyond a date?

You are a blind reader. Read only this file and `packet-b.jsonl` in the same directory. Do not open any other
file in the repository, and do not search the web.

Each item is a passage from a 2025 patent rule (37 CFR) that mentions March 15 or 16, 2013, the dates around
which the America Invents Act's first-inventor-to-file provisions took effect. Look at the sentence that
contains the date.

For each item, answer:
- **condition**: "yes" if that sentence makes the rule's application depend on something about the application
  or claim beyond a single date (for example its effective filing date, what claims it contains or ever
  contained, or its relationship to an earlier application); "no" if the date alone is stated (for example "as
  in effect on March 15, 2013"); "unclear".
- **note**: one sentence.

Write one JSON object per line, in item order, to the output file named in your task:
`{"item": "b-01", "condition": "...", "note": "..."}`
