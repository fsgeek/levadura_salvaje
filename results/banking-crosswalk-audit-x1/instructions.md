# Audit X1: did the address of this act section change between editions?

You are a blind reader. Read only this file and `packet.jsonl` in the same directory. Do not open
any other file in the repository, and do not search the web.

Each item is one section of a named Act, as cited in federal banking regulations (12 CFR) in two
editions (`earlier_edition` and `later_edition`, from 1997, 2010 and 2025). For each edition,
`address` is the United States Code location that the edition's regulations most often give for
that Act section, `pairs` is how many citations agree on it, and `excerpts` are up to two passages
from that edition where the citation appears. `address_heading_2025` is that location's heading in
the 2025 Code, which may differ from the heading in the earlier year. In some items the two
addresses are the same and in some they differ.

For each item, answer:

- **change**: one of
  - "same": both editions give the same address, and it is right for both;
  - "real": the addresses differ because the law's codification really changed (renumbered,
    moved, or reclassified);
  - "error": the addresses differ, or one is wrong, because an edition's regulations cite it wrongly;
  - "misread": the excerpts show the program read the citations wrongly;
  - "unclear": you can't tell.
- **note**: one sentence, naming the right address(es) if you can.

Write one JSON object per line, in item order, to the output file named in your task:
`{"item": "item-01", "change": "...", "note": "..."}`
