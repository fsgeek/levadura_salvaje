# Tessera — Phase 0 Pre-Registration, Amendment 6 — P7's discharge path (2026-09-12)

> **Signing recorded, 2026-09-13 (AI collaborator, recording the record; the stale status line below is retained per amend-don't-rewrite).** The author's first commit containing this file is `c105be7` (2026-09-12, "Another round of amendments, reviews, decisions, and (hopefully) one step closer to moving to implementation."), OTS-stamped at `f1ac93f`. By the sentence below ("which is its signing act") this amendment has been in force since that commit, and P7's tracker row moved to `checked` on it (`formal/PROPERTIES.md`, note of 2026-09-12).
>
> **Status: PROPOSED — the ruling below was adopted in session
> 2026-09-12 (author); this document is the instrument and is not yet
> signed. It becomes in force on the author's commit of this file,
> which is its signing act.** Drafted by the AI collaborator (Claude,
> Fable 5.1) the same day from the author's answer to
> `formal/suite/ROUTED-2026-09-06.md` §D item D1. Layered on the
> original (`75207ba`) and Amendments 1–5 (`03cd3db`, `62f0c5f`,
> `8ae4720`, `5188e7a`, `504e662`). Per amend-don't-rewrite, none of
> them is edited. One section; it selects no mechanism and weakens no
> property.

---

## A6.1 P7: tool assignment amended; the verdict-independence half discharged by control, companions and vector

**What Amendment 1 says.** §A1.4 assigns P7 "TLA+ and ProVerif"; §A1.2
marks it **[model]**. The symbolic half — no cross-type confusion,
opaque inner bytes, standing binds to the innermost issuance identity
— has been modelled (`formal/suite/s-p7/`, the Q1–Q6 ladder with its
companions plus the §A5.5 addendum, cross-family reviewed
2026-09-06 and 2026-09-12, headers read by the author 2026-09-12). No
TLA+ module of P7 exists, none was scheduled, and no ruling assigned
its TLA+ half elsewhere, as the 2026-08-29 Question 2 ruling did for
P1. The 2026-09-12 tracker-prerequisite assessment found this the only
thing keeping P7's row `open`.

**What P7's TLA+ half would say.** Read from Amendment 1's P7 text:
*wrapping never alters the inner package's independently computed
verdict*, per layer (A3 §A3.2 item 4). That is a verdict-composition
claim, not a state-machine claim. The inner verdict is P4's function
applied to the inner bytes; P7 requires that the wrapper be
structurally unable to touch those bytes. Whether it can is what S-P7
Q4 tests: the opaque-embedding control is green and both
re-serialization companions are red (`formal/suite/s-p7/RESULTS.md`,
Q4). A TLA+ model of "the inner verdict is unchanged" would compute
P4's function twice on the same bytes and observe equality — the
companion-that-cannot-fail pattern this record names as theater
(A4.1, the P9 reasoning).

**Amended discharge — RULED (author) by adoption of the
collaborator's recommendation.** P7's tool assignment becomes
**ProVerif; H1a vector**. The [model] half is S-P7. The
verdict-independence half is discharged by (i) S-P7 Q4's
opaque-embedding control and its two re-serialization companions,
already run, and (ii) one H1a conformance vector: a wrapped bundle's
inner verdict equals the same inner bundle's standalone verdict, under
every P4 verdict value (`VALID_STRICT`, `VALID_DEGRADED`, `INVALID`,
`UNVERIFIABLE`), with a re-serializing wrapper as the red bar. The
vector is entered on the band-1 docket. Optionally, on A4.1's terms, a
non-discharging TLA+ probe of two-layer verdict composition may be
built on the collaborator's schedule: a green result is not evidence
and is cited by no tracker row; a red result or an unrepresentable
finding is dispositioned before exit.

**Tracker.** P7's row moves `open` → `checked` on this amendment's
signature, its other recorded prerequisites being satisfied: tool
passes, cross-family review run on the pre-addendum body and on the
§A5.5 addition, the author's C5 read returned with its one NO repaired
in the tree (model line 55, 2026-09-12). `discharged` waits on the
author's read of the two cross-family reviews. The integrated
adversarial lifecycle model (A3 §A3.9) remains, as registered, not a
Band 0 exit obligation.

## A6.2 What did not change

No property is weakened; no mechanism is selected or altered; no
tracker row other than P7 moves. P8's obligations that S-P7 routes to
it (concrete opacity of the embedding under the outer canonicalization
pass; distinguishability of the unexercised object types in bytes) are
unchanged and remain P8's.
