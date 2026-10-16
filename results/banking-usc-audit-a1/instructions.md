# Audit A1: do these regulation citations point at statute that isn't there?

You are a blind reader. Read only this file and `packet.jsonl` in the same directory. Do not open
any other file in the repository, and do not search the web.

Each of the 40 items is a citation of the United States Code found in a 2025 federal banking
regulation. `excerpt` is the surrounding regulation text; `citation_as_read` is the exact span a
program read as a citation; `cited` is how the program parsed it (title, section, then
subdivisions separated by "/"). `statute_record` is what the official US Code XML (release point
119-120) holds for that path. Take it as true.

For each item, answer two questions:

1. **extraction_correct**: does the regulation text, read as a lawyer would, cite exactly the
   provision in `cited`? Answer "yes", "no" (the program misread it, e.g. a range read as one
   section, a missed letter, the wrong title) or "unclear".
2. **provision_gone**: given `statute_record`, is the provision the regulation cites (as the
   regulation wrote it) absent, repealed, transferred or otherwise not in force at 119-120?
   Answer "yes", "no" or "unclear".

Also give `likely_intended`: if you can tell what the drafter meant to cite, say so briefly;
otherwise "". And a one-sentence `note`.

Write one JSON object per line, in item order, to the output file named in your task:
`{"item": "item-01", "extraction_correct": "...", "provision_gone": "...", "likely_intended": "...", "note": "..."}`
