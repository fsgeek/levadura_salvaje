# Tessera — Phase 0 Pre-Registration, Amendment 4 — precision repairs and discharge-path rulings (2026-09-06)

> **Status correction, 2026-09-06 (collaborator, recording the record; the author's explicit confirmation is requested in the next batched read).** The author committed this document unchanged at `5188e7a` ("Address outstanding issues, clarify unclear text, commission a (non-blocking) TLA+ probe"), OTS-stamped at `5dfd82b`. The suite library's D-6 entry, the tracker's P9/P10 rows, and the S-STANDING models read that commit as the signing act (S-STANDING RESULTS.md, routed item 1). The stale DRAFT line is retained below per amend-don't-rewrite.
>
> **Confirmed by the author 2026-09-12 (ROUTED C1, "C1-C4 as recommended"): `5188e7a` is this amendment's signing commit; in force since. Recorded in Amendment 5 §A5.0.**
>
> **Status: DRAFT — adopted in session, not yet signed.** Every ruling
> below was made by the author on 2026-09-06 in dialogue, answering the
> eight items batched in `formal/suite/ROUTED-2026-09-06.md`; this text
> was drafted by the AI collaborator (Claude, Fable 5.1) the same day
> from those answers, quoting the author where he gave reasons. It
> becomes in force on the author's signing commit and OpenTimestamps
> stamp. Per amend-don't-rewrite, the original and Amendments 1–3 are
> not edited; this document states what changes and why.
>
> **What this document is.** The fourth amendment, layered on
> `phase-0-prereg.md` (`75207ba`), Amendment 1 (`03cd3db`), Amendment 2
> (`62f0c5f`), and Amendment 3 (`8ae4720`). It contains no new
> mechanism and weakens no property. Six of its seven sections repair
> registered prose to what the checked models already implement, or
> assign a discharge path to an obligation that had none; the seventh
> registers a principle the author has applied three times as one
> sentence so it need not be re-derived per property.
>
> **Provenance.** Sources: the cross-family falsification reviews of
> the P4, P5/P6, and P5c TLA+ models
> (`docs/reviews/2026-09-06-codex-tla-falsification-p4-p5p6-p5c.md`,
> items 1, 2, 10); the S-P3 results (`formal/suite/s-p3/RESULTS.md`
> F8 and its 2026-09-05 ruling); the S-STANDING and S-P7 predictions
> drafts (`formal/suite/s-standing/`, `s-p7/`); the suite enumeration's
> amendment note 5; the author's 2026-09-06 ruling on the scope of
> "defend it cold" (`formal/spike/first-link/DECISION.md`, under the
> residual entry).

---

## A4.1 P9 and P10: tool assignment and discharge path

**What Amendment 1 says.** §A1.4 assigns P9 and P10 to TLA+ among the
state-machine properties. §A1.2 marks both **[model]**. No TLA+ model
of either exists, and none was scheduled.

**P10 — amended tool assignment: ProVerif.** P10's registered property
sentence — *an adversary controlling any proper subset of the external
authority channels cannot cause a manifest asserting a non-authorized
key to satisfy the `VALID_STRICT` evidence requirement* — is exactly
what the first-link spike's Q1 and Q3 proved in both leaked-channel
variants (`formal/spike/first-link/`, decision `459aff0`) and what
S-P3's strict-mode Q1 proved again under the shared library
(`formal/suite/s-p3/`). The A1.4 assignment predates the tool
decision; the symbolic verifier is the right tool for an adversary
claim. P10's **[model]** half is discharged by those runs, at the
`checked` level, on this amendment's signature; its degraded half
("names which authority evidence was waived and why") is P4's
explicit-policy logic and is carried there. The possession half
(manifest self-signature, A1.5 item 3) is S-P3 ledger entry 2,
already labelled as P10-carried-in-S-P3.

**P9 — amended discharge: inspection plus conformance vector.** A TLA+
model of "the verdict is a pure function of bundle and policy" would
be stateless because its author wrote it stateless — the
companion-that-cannot-fail pattern this record already names as
theater. P9 is discharged by (i) an enumeration of the reference
verifier's inputs, which the standing probe's Q6 produced
(`formal/spike/standing-probe/RESULTS-PROBE.md`), carried into the
coverage map and re-checked against the reference verifier at H1a; and
(ii) one H1a red-bar vector: the same bundle and declared policy,
verified on two isolated machines with no network, must yield the same
verdict, and a verifier that consults any optional service must fail
the vector. P9's discharge label changes from **[model]** to
**[inspection + vector]**.

**Optional TLA+ probes, non-discharging — RULED (author).** The author
asked what is lost by not building the TLA+ models and ruled that they
be built anyway as *probes* in the design-probe tier (ruling of
2026-08-29): *"If they don't find anything, we don't use it as
evidence. If they do find something, we can act upon that between now
and exit."* So: the collaborator builds TLA+ models of P9 and P10 on
its own schedule; a green result is **not evidence** and is not cited
by any tracker row; a red result or an unrepresentable-attack finding
is a finding to be dispositioned before exit. What a P10 TLA+ leg
could still show that the symbolic leg cannot: the state logic of two
archived, time-anchored evidences under the explicit-policy waiver
lattice — which P4's model covers generically and a P10-specific
model would cover concretely. That is the gap the probe exists to
look into.

## A4.2 P4: precedence ratified; one qualifier

**Precedence — RULED (author).** When one required check fails and
another cannot be performed, the verdict is `INVALID`. This is what
`formal/tla/P4_VerifierStates.tla` implements (its comment, lines
49–52, said "for author ratification"); §A1.2.1 orders the two cases
separately and never the combination. Reason: a definite failure is
stronger evidence than an open question, both outcomes are
fail-closed, and the alternative would make the verdict depend on
evaluation order. The author: *"I consider this to be ratified and
consistent with prior discussion."*

**Qualifier.** P4's sentence "A check that cannot be performed yields
`UNVERIFIABLE` — never any `VALID` state, under any trace" is read,
and is hereby written, as "A **required** check that cannot be
performed…". §A1.2.1 already limits the unperformable-to-
`UNVERIFIABLE` rule to non-waivable checks and permits explicit
policies to waive declared redundancy whether or not the waived check
could be performed; the model's `ExactDegraded` invariant implements
that; the P4 sentence was looser than both. This is a
claim-correspondence repair in the A3 §2 style, not a weakening: the
operative claim is unchanged.

## A4.3 P5/P6: revocation after the anchor

Amendment 1 (line 212) says: "Revocation effective *after*
`anchor_time` does not retroactively change the verdict." The
registered two-conjunct rule two lines earlier requires authorization
at `declared_issue_time` **and** no revocation at or before
`anchor_time`; when the anchor precedes the declared time (possible
within ε), a revocation between them invalidates, and
`AuthorizedAtDeclared` in `P5P6_TemporalRevocation.tla` correctly
says so. The sentence is hereby written: "Revocation effective after
both `anchor_time` and `declared_issue_time` does not retroactively
change the verdict." The author: *"fix the prose to conform with the
intent."*

## A4.4 The gate's third clause: what the written proof is

`phase-0-prereg.md` §8 requires, before Phase 1a, "the informal
written proof (the author's defend-it-cold account) is in the
repository." Under the author's 2026-09-06 ruling on the scope of
"defend it cold" (the project, its core decisions, and what it can
and cannot do — never per-proof tool fluency) and the suite's
amendment note 5, that account **is the collection of each checked
model's plain-language statement of claim, adversary, and boundary**,
carried with the model as a reading aid. The artifact must exist for
exit. Its sufficiency for non-expert readers is *reviewed* (by the
lower-ceiling reader probe and by the blind reverse-translation) and
is **not** a gate; the correctness gate for each model is cross-family
falsification review. The author: *"I'm trying to not block this
project as much as possible."* The second clause of §8 (author and AI
each judge the model faithful to the claim) is satisfied from that
statement and the cross-family comparator, which this amendment states
so that no reader infers the author read the tool text cold.

## A4.5 P7: two signed-object types added

P7's enumerated set — base attestation, wrapper, issuer-key manifest,
authority evidence, conformance vector, review-recency attestation —
gains two members: the **terminal lineage record** (the standing-
evidence construction adopted 2026-08-31, entered 2026-09-04) and the
**portable refusal record** (A3 §A3.7.2). Each carries its own
domain-separation tag inside its signed bytes, and no trace may accept
an object of either type as another. Until this amendment is signed
the S-STANDING plan declares the TLR tag model-local; on signature the
tags enter the shared theory library as a recorded divergence.

## A4.6 Degraded mode: the general principle — RULED (author)

Applied first to P3 (2026-09-05, S-P3 F8), then to standing
(S-STANDING plan, 2026-09-06), and now registered once so it is not
re-derived per property:

> In degraded mode — any verdict other than `VALID_STRICT`, including
> the sole-channel-compromised case — the verifier's job is to hand
> the adjudicator the evidence of what could and could not be
> excluded, marked as degraded per §A1.2.1's explicit-policy logic.
> Tessera does not decide whether the adjudicator should trust the
> attestation and must not try to. A correspondence that holds in
> strict mode and fails in degraded mode is therefore a registered
> **cost** of degradation, to be stated in the relying-party story,
> never a defect of the construction — provided the verdict says it is
> degraded.

The author's reason, in his words: *"In 2106, Tessera won't exist in
its current form and the only honest story is the adjudicator will
have to make the decisions based upon the information available to
them; anything else would imply some long-term service guarantees of
Tessera, which I view as dishonest."* Vocabulary registered with it:
the **verifier** is P9's pure function (bundle and declared policy
in, verdict out); the **adjudicator** is the relying party who decides
trust using the verdict and anything else available, including any
third-party log (band-1 docket item 27). An enumeration or
observability API may feed a log and may never feed a verdict.

## A4.7 What did not change

No property is weakened; no mechanism is selected or altered; no
tracker row moves except P10 (→ `checked`, [model] half, on signature)
and P9's discharge label. Band 0's exit list (§8) is unchanged in
substance; A4.4 states how its third clause is met. The suite ruling
that S-STANDING carries the wrapper-shaped transplant (A7 of the
routed file) is a plan-level decision entered in the two predictions
files, not registered text.
