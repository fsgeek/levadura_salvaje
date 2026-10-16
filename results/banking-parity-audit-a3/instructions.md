# Audit A3: does each citation pair point at the same law?

You are a blind reader. Read only this file and `packet.jsonl` in the same directory. Do not open
any other file in the repository, and do not search the web.

Each item comes from a 2025 federal banking regulation that cites a statute two ways at
once: a section of a named Act, and a United States Code location. `pair_as_read` is the span a
program read. `cited_usc` is the U.S.C. location the regulation gives, and `cited_usc_heading` is
that section's heading in the official Code (release point 119-120). `reference_usc` is a U.S.C.
location that other regulations most often give for the same Act section, and
`reference_usc_heading` is its heading. The reference is a hint, not an answer key. It can be
the same as the cited location, and it can be wrong.

For each item, answer:

- **misaddressed**: "yes" if the U.S.C. location the regulation gives is not where the named Act
  section is codified (wrong title, wrong section, a typo, an outdated location). "no" if it is
  the right address. "unclear" if you can't tell.
- **program_misread**: "yes" if `pair_as_read` shows the program mis-parsed the text (for example
  it cut a citation short), "no" otherwise.
- **correct_address**: if misaddressed, the right U.S.C. location if you can tell, else "".
- **note**: one sentence.

Write one JSON object per line, in item order, to the output file named in your task:
`{"item": "item-01", "misaddressed": "...", "program_misread": "...", "correct_address": "...", "note": "..."}`
