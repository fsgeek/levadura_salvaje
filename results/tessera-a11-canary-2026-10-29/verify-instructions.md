# Verify candidate findings

You are a verifier. Read only what is in your working directory: this file, `candidates-blind.json` (candidate
findings from several independent readers; unverified, possibly wrong, often duplicates), and the texts under
`corpus/`. Every location is `FILE:LINE`, relative to `corpus/`. Do not open anything else. Do not use the web,
memory tools, or any other source. Do not write or change any file except the output file named in your task.

## The texts and their authority

- `docs/phase-0-prereg.md` is the signed original. Amendments 1–10 are signed and layered on it in order; a later
  amendment governs an earlier one. Each amendment must list, in its own change table, every earlier registered
  sentence it changes (A9.7, A10.7, A11.3, and the "What changed" sections of earlier amendments).
- A9, A10, `formal/p8/PROOF.md`, `docs/V1-PROFILE.md`, `formal/p8/ENCODING-V1.md` and `formal/p8/HYBRID-SUPPLEMENT.md`
  form the frozen V1 specification (`formal/freeze-v1/FREEZE-RECORD.md`). Frozen text is not edited; readings go
  elsewhere, and real changes need an amendment.
- `docs/phase-0-prereg-amendment-11.md` (A11) is an **unsigned draft**. It may still be corrected before signing.
- The other files are records and evidence or deployment files that A11 cites.

## For each candidate

1. Find both locations and read enough of the surrounding text to understand them. Check that the quotes are really
   there. Line numbers may be a little off, so find the real lines.
2. **verdict**:
   - `real`: the two places really cannot both hold, or one really changes the other without saying so, or a term
     really has two meanings that matter, or a citation really points to the wrong place.
   - `not_real`: the texts agree, the quote isn't there, or the conflict dissolves on reading. A conflict the texts
     already acknowledge and resolve is not real (for example "this supersedes X", a change-table row that covers
     it, or a reconciliation note).
   - `unclear`: you can't tell from the texts.
3. **same_as**: if it is the same finding as an earlier candidate you judged (same defect, even with different
   wording or line numbers), give that candidate's id. Otherwise give "".
4. **touches_a11**: `yes` if one location is in A11, or if it is a sentence that A11.3 or A11.5 should have listed
   because A11 changes what it refers to. Otherwise `no`.
5. **repair**: what fixing it would take, if real:
   - `a11_draft`: a correction to the unsigned A11 before it is signed (including adding a row to A11.3);
   - `new_amendment`: a change to signed or frozen text that A11 does not and should not cover;
   - `editable_only`: only a non-registered, non-frozen file needs to change;
   - `none`: not real.
6. **severity** (if real): `substantive` if it changes a verdict, an obligation, a security claim or who may do what;
   `wording` if it is a locator, count or phrasing defect that a careful reader would see through.

## Output

Write a JSON array, one object per candidate, in id order, to the output file named in your task:

```
{"id": "c000", "verdict": "real|not_real|unclear", "same_as": "", "touches_a11": "yes|no",
 "repair": "a11_draft|new_amendment|editable_only|none", "severity": "substantive|wording|",
 "loc_a": "FILE:LINE (corrected)", "loc_b": "FILE:LINE (corrected)",
 "why": "one or two sentences, quoting the decisive words"}
```

Judge every candidate. Be strict: a reader's confidence is not evidence.
