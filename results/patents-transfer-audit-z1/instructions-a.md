# Audit Z1a: does each patent-rule citation to the Patent Act point at law that exists?

You are a blind reader. Read only this file and `packet-a.jsonl` in the same directory. Do not open
any other file in the repository, and do not search the web.

Each item is a citation to title 35 of the United States Code (the Patent Act) in a 2025 patent
rule (37 CFR). `citation_as_read` is the span a program read, and `excerpt` is the passage around
it. Some of these citations point at a section, subsection or paragraph that the program could not
find in the current Code. Others it did find. You aren't told which.

For each item, answer:

- **broken**: "yes" if, as written, the citation points at a provision that doesn't exist in
  35 U.S.C. today (a wrong number, a subdivision that isn't there, a provision repealed or
  renumbered, for example by the America Invents Act), "no" if it points at an existing provision,
  "unclear" if you can't tell.
- **program_misread**: "yes" if `citation_as_read` shows the program mis-parsed the text, "no"
  otherwise.
- **deliberate_old_law**: "yes" if the rule seems to refer to the old provision on purpose (for
  example, pre-AIA law still governing older applications or proceedings), "no" or "unclear"
  otherwise.
- **note**: one sentence, naming the right provision if you can.

Write one JSON object per line, in item order, to the output file named in your task:
`{"item": "a-01", "broken": "...", "program_misread": "...", "deliberate_old_law": "...", "note": "..."}`
