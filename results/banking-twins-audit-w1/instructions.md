# Audit W1: two copies of one regulation — how do they differ?

You are a blind reader. Read only this file and the batch file named in your task. Do not open any
other file in the repository, and do not search the web.

After the Dodd-Frank Act (2010), several federal consumer-finance regulations exist in two copies
in the 2025 Code of Federal Regulations (12 CFR), each kept by a different agency for the
institutions it still covers. Each item shows the same section of one regulation from both
copies, as `text_A` and `text_B` (which copy is which is not given, and is random). Part numbers
are masked as N and agency names as AGENCY. `diff` lists the word-level differences (it may be
cut short), and `truncated` says whether the texts were cut at 9,000 characters. In some items
the two copies differ a lot; in some, hardly at all.

For each item, answer:

- **difference**: one of
  - "editorial": wording, numbering, cross-references or agency names only; the same rule;
  - "scope": an intended difference in whom the section covers or which agency acts, with the
    rule otherwise the same;
  - "stale": one copy lacks a substantive amendment that the other has taken (say which, A or B,
    seems older, in the note);
  - "both": the copies differ in substance in ways that aren't one copy lagging the other;
  - "unclear": you can't tell.
- **older**: "A", "B" or "" (only for "stale").
- **note**: one sentence on the substance of the difference.

Write one JSON object per line, in item order, to the output file named in your task:
`{"item": "item-01", "difference": "...", "older": "...", "note": "..."}`
