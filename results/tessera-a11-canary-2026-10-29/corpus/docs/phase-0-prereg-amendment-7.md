# Tessera — Phase 0 Pre-Registration, Amendment 7 — the specification's routed contradictions: nine rulings, two record dispositions (2026-09-14)

> **Signed 2026-09-14 at `9863513`** ("Further revisions, clarifications, and a move towards completion of the design."), the author's first commit containing this file, OTS-stamped at `d871c90` and anchored at `7a995eb`; pushed the same day. Recorded by the AI collaborator; the status line below is retained per amend-don't-rewrite.
>
> **Status: PROPOSED — the rulings below were made by the author on
> 2026-09-14 in session; this document is the instrument and is not yet
> signed. The author's first commit containing this file is its signing
> act** (the house form since Amendment 5). Drafted the same day by the
> AI collaborator (Claude, Fable 5.1, owner instance) from the author's
> one message answering the eleven open items of
> `docs/implementation-spec.md` §12 (C-03 to C-08, C-10 to C-13, C-15),
> quoting the author verbatim in every section and marking, in two
> places, where the collaborator read a word differently from how it
> was typed so that the author can correct it. Layered on the original
> (`75207ba`) and Amendments 1–6 (`03cd3db`, `62f0c5f`, `8ae4720`,
> `5188e7a`, `504e662`, `c105be7`). Per amend-don't-rewrite, none of
> them is edited; sentences this amendment supersedes are named and
> left standing in their files. No property is weakened (A1 §A1.1);
> §A7.11 says what changed and what did not.

Labels are the `formal/spike/first-link/DECISION.md` ones. Every
section's ruling is **ADOPTED (author)** unless it says otherwise; the
author's words are in italics inside quotation marks; everything not in
quotation marks is the collaborator's instrumentation of them.

---

## A7.1 Canonical payload bytes and the signed frame are two byte strings (C-03) — ADOPTED (author)

*"I think it would be useful to clearly separate canonical payload
bytes from the signed frame."*

**Instrument.** Two terms, fixed: the **canonical payload bytes** are
`canonical(payload)`, the JCS (RFC 8785) serialization under the
precision rule of the original §4.3; the **signed frame** is the
framed envelope of Amendment 1 §A1.2 P8, `type_tag ||
canonicalization_version || payload_length || payload`, whose fourth
field *is* the canonical payload bytes. Signatures and anchors commit
to the signed frame. The length is a frame field. The original §4.3's
sentence "Length is bound into the canonical bytes (not a side field)"
(`docs/phase-0-prereg.md:492-494`) is superseded by A1 P8 as A1 §A1.8
already implies, and is read from this amendment on as "the length is
bound into the signed bytes"; it is not edited. Golden vectors exist
for both strings separately (P8: the canonical payload bytes; the
frame layout: the signed frame).

## A7.2 The issuer-key manifest may carry references, resolvable only from the bundle or from declared trusted inputs (C-04) — ADOPTED (author), reading B

*"B. You should allow references to be resolved entirely from the
bundle or from explicitly declared trusted inputs. Note that a
reference shouldn't require a network lookup (e.g., offline, albeit
limitations are permissible.)"*

**Instrument.** The original §4.4's "(or references)" stands. A
reference in the manifest is permitted when its target is resolvable
either (i) from material inside the bundle or (ii) from an input the
verifier's declared policy explicitly names as trusted (the trust
configuration of the implementation specification §2.3), and never by
a live lookup. Under (ii) the reference stays inside P9's pure
function, since the declared policy is one of its two arguments;
"explicitly declared" was the collaborator's reading of how P9 is
preserved, **confirmed by the author 2026-09-14:** *"Agreed. Make them
explicitly declared."* A trusted input not named in the declared policy
is not a trusted input. A reference the
verifier cannot resolve from (i) or (ii) makes the check that needs
it unperformable (`UNVERIFIABLE` for that required check, per the P4
partition); "limitations are permissible" is read as this and nothing
broader. A1 §A1.5's "archived in the bundle" for the two authority
evidences is unchanged: (ii) does not license archiving an authority
evidence outside the bundle.

## A7.3 The scope of the `anchor-late` observation (C-05) — ADOPTED (author); reading confirmed by the author

*"I'd suggest making the object scope explicit: the receipt's required
temporal checks are still not non-waivable. This still permits a
waived redundant authority to carry a late-anchor observation. I
wouldn't permit any waiver to eliminate the final complete chain."*

**Reading, confirmed by the author.** The second sentence as typed,
"still not non-waivable", would make the receipt's own temporal checks
waivable, which the third sentence, A2 §A2.2 ("Temporal-anchor
consistency is already non-waivable") and A3 §A3.2's linked floor all
forbid. The collaborator read it as *"still non-waivable"* and
instrumented that. **Confirmed by the author, 2026-09-14, in session:**
*"(1) was not intended to make them waivable."* The section stands.

**Instrument.** Object scope, made explicit: A2 §A2.2's three
temporal conjuncts apply to **the receipt's own shipped anchor** and
are non-waivable; a late receipt anchor is performed-and-failed,
`INVALID`, never an observation. A5 §A5.3's `anchor-late` is an
observation recorded against **a waived redundant authority
evidence's own anchor** and never determines the verdict. No waiver
may remove the final complete evidence chain (A3 §A3.2, unchanged).
A2 §A2.2 and A5 §A5.3 are both correct on their own objects; neither
is edited.

## A7.4 Declared time is never presented as priority; adjudicators reason for themselves (C-06) — ADOPTED (author); restates the scope of A2 §A2.4

*"Tesser should not present declared time as proof of first-to-file
priority. Rather, this is a decision that an adjudicator could use in
their own reasoning - not because Tessera provides any claims. This
limitation is not a service-refusal requirement."*

**Instrument.** A2 §A2.4's commitment is read as a commitment about
**Tessera's own surfaces, policies and claims**: no Tessera verifier
policy, report, rendering or marketplace rule presents
`declared_issue_time` as evidence of first-to-file priority, and
Tessera makes no priority claim. What an adjudicator does with a
declared time in their own reasoning is theirs (A4 §A4.6). Tessera
does not refuse service, verification or reporting on the ground that
a relying party might so reason. **Collaborator's note, for the
author's eye:** A2 §A2.4 as written says "no downstream marketplace
rule may order competing receipts by declared time"; this section
narrows the *bearer* of that rule from every downstream party to
Tessera and its own surfaces. It is instrumented as an amendment
section rather than a reading so that the narrowing is on the record
as a change. The prohibition's ground, that re-issue gives the issuer
discretion over declared times, is unchanged and is the reason Tessera
itself must never present declared time as priority. **The author, on
being shown the narrowing, 2026-09-14:** *"the point truly is
adjudicators can do whatever they want, we're merely providing them
with evidence with clearly delineated limitations."* The narrowing is
adopted knowingly.

## A7.5 A3 §A3.6.2's "exactly one case" is scoped to algorithm-identifier handling (C-07) — ADOPTED (author)

*"You should scope 'exactly one case' to handling of the
algorithm-identifier. This allows other required checks to be
unperformable independently. The standing is still a separate
assessment."*

**Instrument.** A3 §A3.6.2 item 2's sentence "`UNVERIFIABLE` for
exactly one case — a well-formed, correctly bound, but unsupported
algorithm identifier" is read as bounding **the algorithm-identifier
check's** outcomes only: within that check, one and only one input
shape yields `UNVERIFIABLE`. Every other required check yields
`UNVERIFIABLE` when it cannot be performed, independently, under P4
and A4 §A4.2 (A3 §A3.2.2 `:146-149` and §A3.4 `:353-356` are
instances, not conflicts). The standing dimension's `UNVERIFIABLE` is
a value of the orthogonal assessment (A3 §A3.7.1), not a P4 verdict.
The non-author reviewer's observation of 2026-09-14 that the
specification's C-07 "Implementer" paragraph was logically mistaken
on this point is accepted; that paragraph is corrected in the
specification.

## A7.6 The ship guard: the §A3.7.3 repair governs; the §A3.9 summary line is superseded (C-08) — ADOPTED (author), reading A; reading confirmed by the author

*"A. The summary appears to be stale. Can you ensure explicit repair
governs, so that three temporal conjuncts plus burial death are what
matters."*

**Reading confirmed.** "burial death" was read as *"burial depth"* (the
`DepthK` conjunct of the bridge's `Ship` guard). The author, 2026-09-14:
*"C8 was a misspelling on my part … Depth is right."*

**Instrument.** A3 §A3.7.3's panel-driven repair governs: the issuer
ships on the three temporal conjuncts of A2 §A2.2 plus burial depth
`DepthK = k − 1`, and does not re-run envelope verification (P1–P3)
at ship. The §A3.9 summary line "A2.1 prose repair (issuer ships on
full `VALID_STRICT`)" (`docs/phase-0-prereg-amendment-3.md:832`) is
the unrepaired wording and is superseded; it is not edited.

## A7.7 One standing vocabulary, with the S-series mapped onto it (C-10) — ADOPTED (author), reading B

*"B. It needs an explicit mapping of S1 to ESTABLISHED and S[2-4] to
ABSENT. We need to retain the specific reasons. A malformed or
temporally inconsistent standing evidence means it is UNVERIFIABLE
(the existing rules)."*

**Instrument.** The standing report's value set is A3 §A3.7.1's:
`ESTABLISHED`, `ABSENT`, `UNVERIFIABLE`, each with a reason code. The
first-link S-series (`formal/spike/first-link/DECISION.md:797-801` and
the SC-3 S4 row) maps onto it as follows, reason codes retained and
pairwise distinct as registered:

| Row | S-series verdict | Standing value | Reason code |
|-----|------------------|----------------|-------------|
| S1 | standing | `ESTABLISHED` | `TERMINAL_DISPOSITION_SHOWN` |
| S2 | no standing | `ABSENT` | `SUPERSEDED` |
| S3 | no standing | `ABSENT` | `NO_TERMINAL_DISPOSITION_EVIDENCE` |
| S4 | no standing | `ABSENT` | `ISSUANCE_REFUSED` |
| — | — | `UNVERIFIABLE` | `STANDING_EVIDENCE_MALFORMED` (SC-3, internally inconsistent evidence) |
| — | — | `UNVERIFIABLE` | `STANDING_EVIDENCE_TEMPORAL_MISMATCH` (SC-3, the TLR's anchor failing A2.1) |

"standing" / "no standing" remain readable as the S-series' names for
`ESTABLISHED` / `ABSENT` and are not a third value. The two
probe-observed codes `STANDING_EVIDENCE_MISMATCH` and
`STANDING_EVIDENCE_SIGNATURE_INVALID` are not registered by this
section (specification §11 O-75 stands). The H1a standing vectors
carry the mapped values.

## A7.8 Confirmation depth: the registered default k = 6 is preserved; the checked evidence is owed at that parameter or by a parameter-general argument (C-13) — ADOPTED (author)

*"We should preserve the intended production parameter by using
commission evidence at said parameter, or at a parameter-general
argument. We should not change the default to match a small checked
configuration."*

**Instrument.** The strict default k = 6 (`DepthK = 5`) of A1 §A1.2
P5 and A2 §A2.1 stands, subject to ratification at Band 0 exit as
registered. The P5c and bridge configurations checked at `DepthK = 2`
remain evidence for the checked abstraction and are not evidence at
the registered parameter (`formal/tla/READING-AID-P5c.md:226-231`
already says so). One obligation is added to the Band 0 exit list
(`formal/BAND0-EXIT.md` E18): either (a) the P5c, P5P6 and bridge
modules re-run at `DepthK = 5` with `MaxTime` and the other bounds
sized so that every registered witness still fires (the non-author
reviewer's caution of 2026-09-14: replacing the one constant can make
witnesses unreachable), or (b) a written argument, reviewed by a
non-author model, that every checked invariant is independent of the
value of `DepthK` above the minimum the witnesses need. Green at (a)
is evidence at the parameter; (b) is evidence for the family of
parameters. The tracker's parameter box is unchanged.

## A7.9 The frame: the four-field envelope and the signer-specific bindings both stand, joined by an explicit encoding map settled before format freeze (C-15) — ADOPTED (author)

*"We should preserve the concrete four-field envelope and the signer
specific semantic bindings _if_ an explicit encoding map demonstrates
both requirements. We should settle the map before format freeze
because neither field count alone gives us an answer."*

**Instrument.** A1 §A1.2 P8's four-field signed frame and A5 §A5.4's
seven signer-specific bindings (object type, algorithm, identity,
manifest hash, canonicalization version, payload, key fingerprint) are
both registered and are not in conflict *provided* an **encoding map**
shows where each symbolic binding lives in bytes: as an envelope field
(type tag, canonicalization version, payload), or inside the canonical
payload under P3's obligations (the A3 §A3.6.1 precedent for the
algorithm identifier; docket item 25's precedent for the forward
link), or in the manifest tuple the frame commits to by hash. The map
must also separate the requester's content from the signer-specific
metadata around it, so that "payload equal across signer slots" (A5
§A5.4) is a statement about bytes. The map is a **pre-freeze
obligation**, entered on the band-1 docket as item 33 and on the
specification's §10.2 list; until it is settled, the frame layout
remains open (specification §11 O-01) and no golden vector for the
signed frame is final. The symbolic library's seven-argument `framed`
constructor is an abstraction of both, not a byte layout.

## A7.10 Two record dispositions that change no registered text (C-11, C-12) — ADOPTED (author)

**C-11, key binding as a ledger dependency.** *"B for S-P1.
Authorship and key binding compose as complementary claims. We should
not create a dependency if said dependency cannot falsify the claim of
the consumer. Different consumers will need their own dependency
analysis."* Disposition: S-P1's ledger entry 1 stands as written
(complementary, not consumed, no cross-model entry claimed;
`formal/suite/s-p1/RESULTS.md:330-345`); S-P3's ledger entry 1 is
read as naming S-P1 a *related* family, not a consumer. The rule the
author states — a cross-model ledger entry exists only where severing
the producer would falsify the consumer's query — is the reading of
A3 §A3.3's gate text that the capstone discharge matrix applies, and
S-P2 and S-P7 make their own determination against S-P3's entry when
their entries are entered (`formal/BAND0-EXIT.md` E5a). Recorded by an
appended note in `formal/COVERAGE-MAP.md`.

**C-12, the S-P3 reading aid.** *"Code description needs to be
accurate: the fields are bound, they are not checks done by S-P3 and
the obligation to validate is not here, it is somewhere else."*
Disposition: the model headers are accurate as they stand
(`sp3_q2_degraded_compromised.pv:53-55`, "included in the signed bytes
but unexercised"); the two reading-aid rows that list `ot` and `cv`
inside a column of check statuses (`formal/suite/s-p3/READING-AIDS.md`
lines 177 and 302) are corrected in place with a dated marker to say
the fields are bound and not checked here, their validation obligations
being P7's (object type) and P8/H1a's (canonicalization version). No
model is edited; the deferred recut in `s-p3/RESULTS.md:346-367` is
thereby adopted as a reading-aid correction only.

## A7.11 What changed, and what did not

**Readings that bind from this amendment's signature:** §A7.1 (two
byte strings), §A7.2 (references, offline-resolvable), §A7.3 (object
scope of `anchor-late`), §A7.5 (scope of "exactly one case"), §A7.6
(the ship guard), §A7.7 (one standing vocabulary, mapped). **One
narrowing, stated as such:** §A7.4 narrows the bearer of A2 §A2.4's
ordering prohibition to Tessera's own surfaces and claims. **Two
obligations added:** §A7.8 (evidence at k = 6 or a parameter-general
argument, Band 0 exit E18) and §A7.9 (the encoding map, pre-freeze,
docket 33). **Two record dispositions:** §A7.10.

**Not changed:** every property statement of A1 §A1.2; the P4
partition; A2 §A2.1's confirmation predicate and §A2.2's conjuncts;
A3 §A3.2's linked floor; the standing invariant A3 §A3.7.1; the
registered defaults δ, ε, k, N and their ratification at exit; every
tracker row. **The A1 §A1.1 falsifier is not triggered:** no property
is weakened; §A7.4's narrowing concerns a design commitment about
Tessera's own conduct, not a verifier guarantee, and the guarantee it
protects (declared times never order receipts on Tessera's surfaces)
is kept.

**Two words were read against their typing and both readings were
confirmed by the author on 2026-09-14** (§A7.3 "still non-waivable";
§A7.6 "burial depth"); the confirmations are quoted in place. Nothing
in this amendment rests on a collaborator's reading of the author's
words that the author has not confirmed.
