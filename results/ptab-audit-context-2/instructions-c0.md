# Which version of the patent law does this Board decision apply?

You are a blind reader. Read only this file and the batch file named in your task. Do not open any other file in
the repository, and do not search the web.

Each item is a final written decision of the Patent Trial and Appeal Board (issued 2021–2026) in an inter partes
review or similar trial. `passages` are up to eight excerpts around the decision's citations to 35 U.S.C.; they
aren't the whole decision. The America Invents Act (AIA) replaced 35 U.S.C. 102 and 103 with new versions for
patents and applications with an effective filing date on or after March 16, 2013. Older patents remain under
the earlier ("pre-AIA") versions.

For each item, answer:
- **applies**: the version of §§ 102/103 under which the decision assesses patentability: "pre-AIA", "AIA" or
  "unclear". Give your best judgement from what is in front of you; "unclear" is a legitimate answer.
- **basis**: one sentence naming what in the item decided your answer.

Write one JSON object per line, in item order, to the output file named in your task:
`{"item": "...", "applies": "...", "basis": "..."}`
