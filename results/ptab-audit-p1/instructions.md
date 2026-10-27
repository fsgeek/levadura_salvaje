# Audit P1: which patent law does this Board decision apply, and does it say so?

You are a blind reader. Read only this file and `packet.jsonl` in the same directory. Do not open any other
file in the repository, and do not search the web.

Each item is a final written decision of the Patent Trial and Appeal Board (2021–2026) about a patent granted
before March 16, 2013. That is the date the America Invents Act's (AIA) first-inventor-to-file versions of
35 U.S.C. 102 and 103 took effect, so such a patent was examined under the earlier ("pre-AIA") versions.
`passages` are up to eight excerpts around the decision's citations to 35 U.S.C. They aren't the whole
decision.

For each item, answer:
- **applies**: which version of §§ 102/103 the decision applies: "pre-AIA", "AIA", "unclear", or
  "not-102-103" (the excerpts show no §§ 102/103 ground at all).
- **says_so**: "yes" if the excerpts say which version applies (for example "pre-AIA", or a footnote on the
  AIA's effective date), "no" if they don't, "unclear".
- **wrong_regime**: "yes" only if the decision appears to apply the wrong version for this patent; otherwise
  "no" or "unclear".
- **note**: one sentence, quoting the words that decided your answer if you can.

Write one JSON object per line, in item order, to the output file named in your task:
`{"item": "p-01", "applies": "...", "says_so": "...", "wrong_regime": "...", "note": "..."}`
