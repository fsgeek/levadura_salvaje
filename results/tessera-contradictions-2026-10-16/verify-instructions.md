# Verify candidate contradictions

You are a verifier. Read only three files in this directory: this file, `packet.txt` (four rule texts,
every line prefixed "FILE:LINE| "), and `candidates-blind.json` (49 candidate findings from several
independent readers, unverified, possibly wrong, possibly duplicates). Do not open anything else, and
do not use the web.

Authority: phase-0-prereg-amendment-9.md (A9, signed) governs; V1-PROFILE.md is a draft; ENCODING-V1.md
with HYBRID-SUPPLEMENT.md is the encoding specification. A9's table A9.7 must list every earlier
registered sentence that A9 changes.

For each candidate:
1. Find both cited locations in packet.txt and read enough surrounding text to understand them. Check
   that the quotes are really there (line numbers may be slightly off; find the real line).
2. Decide:
   - "real": the two places really cannot both be true, or one really changes the other without
     saying so, or a term really has two meanings. A conflict the texts themselves already
     acknowledge and resolve (e.g. "this supersedes X", "earlier wording", an explicit override
     the governing text allows) is NOT real; say so.
   - "not_real": the texts agree, the quote is wrong, or the conflict dissolves on reading.
   - "unclear": you can't tell from the texts.
3. If it duplicates an earlier candidate you judged, give that id in "same_as".

Write a JSON array, one object per candidate, in id order, to the output file named in your task:
{"id": "c000", "verdict": "real|not_real|unclear", "same_as": "", "loc_a": "FILE:LINE (corrected)",
 "loc_b": "FILE:LINE (corrected)", "why": "one or two sentences, quoting the decisive words"}
