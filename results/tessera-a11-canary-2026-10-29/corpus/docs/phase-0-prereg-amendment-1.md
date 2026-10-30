# Tessera — Phase 0 Pre-Registration, Amendment 1

> **What this document is.** The first amendment to the Phase 0
> pre-registration (`phase-0-prereg.md`, commit `75207ba`, GPG-signed,
> OTS-anchored). The original is never edited; amendments are separate,
> layered, dated documents — the same wrap-don't-replace discipline §3.1
> applies to attestations, applied to the pre-registration itself. A
> pre-registration that mutates silently is worthless; one that amends
> visibly, with the reasons on record, is the method working as intended.
>
> **Provenance.** This amendment is the outcome of four adversarial review
> rounds, all *before* Band 0 work began, on the author's initiative:
>
> 1. **2026-07-03, Claude** (AI collaborator per §0/§6 of the original —
>    mechanics, drafting, pushback): the review that produced this
>    amendment's first draft, including its pre-registered predictions of
>    what an external reviewer would find.
> 2. **2026-07-03, GPT-5.5, round 1** (non-author AI reviewer, external to
>    the authoring session — explicitly *not* an independent human review;
>    highest reasoning setting; prompted flat — "would you be willing to
>    review a pre-registration amendment" plus both documents attached, no
>    steering): a falsification-style review of the first draft. Four
>    blocking findings were confirmed and incorporated; the first draft's
>    P10 and P5, in particular, contained the kind of subtle overclaim this
>    project exists to catch. Artifact:
>    `docs/reviews/2026-07-03-gpt5.5-amendment-1-review.md`, committed
>    alongside this amendment per A1.7's own rule.
> 3. **2026-07-03, GPT-5.5, round 2** (same reviewer, reviewing the revised
>    draft with round 1 in context): one material finding — P6, as revised,
>    evaluated key authorization only at `declared_issue_time`, admitting a
>    revocation/backdating interaction inside the δ window — plus five
>    precision fixes. All confirmed and incorporated. Artifact:
>    `docs/reviews/2026-07-03-gpt5.5-amendment-1-review-round2.md`, committed
>    alongside this amendment per A1.7's own rule.
> 4. **2026-07-03, Gemini 3.5 Flash ("Antigravity")** (non-author AI
>    reviewer, external to the authoring session; default configuration;
>    prior review rounds in context): three blocking findings — wrapper
>    re-serialization (P7), undefined anchor confirmation depth (P5), and
>    key-lifecycle monotonicity (P6) — plus three precision fixes. All
>    confirmed and incorporated, with placement and wording corrections
>    recorded in the disposition. Artifact:
>    `docs/reviews/2026-07-03-antigravity-amendment-1-review.md`.
>
> All decisions herein are the author's (Tony Mason); the division of labor
> is unchanged.

---

## A1.0 Why amend before starting

The review found that the pre-registration, as signed, could be *passed by a
proof that does not protect the project*. H0 pre-registered that a
machine-checked proof would exist, but not **what it must prove**. That gap
is precisely the drift-vector formal-methods theater needs: months into the
modeling, the provable-in-practice properties drift toward whatever the
model makes easy, and "the proof holds" quietly becomes "the proof of
whatever we managed to prove holds." The agreement gate, as written, would
judge fidelity only *after* any such drift, by the same parties who drifted.

This amendment closes that gap by pre-registering the property list
(A1.2), the degraded-policy semantics (A1.2.1), the adversary model (A1.3),
and the tooling rationale and choice discipline (A1.4). It also resolves
one design hole the review surfaced (manifest authority, A1.5), states the
temporal-anchor semantics precisely (A1.6), and hardens the agreement gate
from a confirmation task into a falsification task (A1.7). The original
objectives, bands, and invariants are not weakened; this amendment *adds*
resolution and evidence obligations (A1.8).

---

## A1.1 Clarification of the H0 falsifier

The original's phrasing — "if the guarantee cannot be proven, there is
nothing worth building" — could be misread as one-shot: first failed proof
attempt, project over. That is not the claim and never was. The method is
iterative, as all modeling is: model, attempt proof, find the flaw, revise,
re-prove — with each revision recorded in the journal.

Iteration within scope is ordinary work. **Falsification is scope
reduction.** Precisely: H0 (as amended) is falsified if any A1.2 property
cannot be discharged without one of the following:

- **weakening the property** as pre-registered;
- **demoting** a property from `[model]`/`[proof]` to `[assumption]`;
- **excluding** a declared A1.3 adversary capability;
- **changing the construction so materially** that it no longer implements
  the dual-signature + temporal-anchor design of §3.1.

Any such weakening requires a further signed, dated amendment stating what
was weakened and why; absent that amendment, Phase 1 does not begin. This
gives a future reader a concrete way to see whether Band 0 succeeded,
failed, or changed scope — rather than an unfalsifiable "no model could be
built." Building the service on a foundation that required concealed
weakening would be theater; that, and only that, is what the original
sentence forbids.

---

## A1.2 The pre-registered properties (the theorem statements)

These are the properties the Band 0 work must establish, stated in prose
*before* any modeling begins, so that "the proof holds" has a fixed
referent. Each names how it is discharged: **[model]** — proven in the
machine-checked model under idealized primitives (Layer 1); **[proof]** —
proven directly (not a state-machine claim); **[assumption]** — cited as an
explicit Layer 2 assumption, not proven. Restating a property here in
sharper form does not weaken the original's hard invariants; where an
invariant (§4.3, §4.6) and a property overlap, the property is the
checkable form of the invariant.

Temporal vocabulary used throughout (defined precisely in A1.6):
`declared_issue_time` is what the issuer claims; `anchor_time` is the
Bitcoin block time of the OTS anchor, which establishes only that the
anchored bytes existed *not after* that block.

- **P1 — Integrity (the headline claim).** There is no reachable state in
  which the verifier returns `VALID_STRICT` or `VALID_DEGRADED` for a
  package whose canonical bytes differ from bytes signed at issue time.
  **[model]**

- **P2 — Signature-set completeness (anti-stripping).** The canonical
  signed bytes commit to the required-signer manifest. A package presenting
  fewer signatures than its manifest requires yields `INVALID` — never
  `VALID_STRICT`, and `VALID_DEGRADED` only under an explicit, recorded
  policy within the waivable set of A1.2.1. Consequence: "issued with one
  signature" and "issued with two, one stripped" are distinguishable by
  construction, because the expected set is inside what every signature
  signs. **[model]**

- **P3 — Key binding (anti-substitution).** Acceptance binds each
  signature to the issuer identity committed in the signed bytes. The
  adversary model (A1.3) explicitly includes key-substitution attacks
  (DSKS / exclusive-ownership failures: constructing a different keypair
  under which an existing message–signature pair verifies, then
  re-presenting the package under a substituted manifest). Idealized
  signatures assume this binding by fiat; Ed25519 signature verification
  alone does not provide protocol-level issuer binding or exclusive
  ownership — the verification equation is not, by itself, the
  issuer-binding protocol. Discharge is split:
  - the binding of identity into signed bytes — the signed bytes include,
    at minimum: domain-separation tag, object type (per P7's enumeration),
    algorithm identifier, issuer identity, key fingerprint, manifest hash,
    and canonicalization version — is **[model]**;
  - the implementation's **verification profile** is **[assumption]**,
    named in Layer 2 and discharged as H1a evidence: exact library and
    version, accepted signature encodings, public-key validation behavior,
    low-order-point handling, cofactor equation variant, and negative test
    vectors for each, all recorded in the repository.

  This property may not fall between the layers.

- **P4 — Fail-closed state logic.** The verifier's four states partition
  all outcomes. A required check that fails yields `INVALID`. A check that
  cannot be performed yields `UNVERIFIABLE` — never any `VALID` state,
  under any trace. `VALID_DEGRADED` arises only from an explicit, recorded
  policy within A1.2.1's waivable set, never as a default or a fallback.
  (The checkable form of §4.6.) **[model]**

- **P5 — Temporal soundness (two-sided).** The anchor is an upper bound on
  creation time, and only that (A1.6). Strict verification requires the
  anchor to be consistent with the declared issue time **in both
  directions**:

      declared_issue_time − ε  ≤  anchor_time  ≤  declared_issue_time + δ

  The δ side **bounds** *backdating*: a forger signing new bytes cannot
  obtain a conforming anchor for a claimed time more than δ in the past —
  backdating within the tolerance window is not eliminated, only bounded.
  The ε side **bounds** *post-dating*: an issuer cannot declare an issue
  time more than ε after the anchor and later present the receipt as
  fresh.

  **δ and ε belong to the verifier, not the receipt.** A receipt records
  its issue-time policy version and the observed anchor delay; it may not
  choose its own temporal tolerances — a receipt-controlled tolerance
  would let a malicious issuer write an enormous window into the signed
  bytes. The reference verifier's strict policy fixes the maxima: **δ =
  72 hours** (OTS aggregation-to-confirmation lag plus Bitcoin timestamp
  skew), **ε = 24 hours** (Bitcoin block timestamps may lag real time by
  hours under the median-time-past rule). A verifier may choose stricter
  bounds; no degraded policy may enlarge δ or ε beyond the strict maxima.
  Both maxima are ratified (or revised, on the record) at Band 0 exit.
  Temporal-anchor consistency is **non-waivable** (A1.2.1). **[model]**,
  resting on the Bitcoin/OTS assumptions of A1.6 **[assumption]**.

  *Issuance-protocol corollary (so honest receipts cannot rot):* issuance
  is not complete until the anchor is **confirmed** — buried at a minimum
  confirmation depth **k** on the Bitcoin chain (strict default **k = 6**,
  ratified with δ and ε at Band 0 exit) — within δ of
  `declared_issue_time`. Depth is what "confirmed" *means*: a
  one-confirmation anchor orphaned by a transient reorganization would
  leave an already-shipped receipt permanently unverifiable, so a receipt
  never ships on a shallow anchor. If confirmation is delayed past δ for
  benign reasons (calendar outage, fee spikes, reorg), the receipt is
  **re-issued** with a fresh declared time and re-anchored — the failed
  attempt is discarded, not shipped. Without this rule, honest-but-late
  anchoring would be permanently indistinguishable from backdating.

- **P6 — Revocation time-relativity (evaluated over the uncertainty
  window).** The anchor proves only that the signed bytes existed *not
  after* `anchor_time`; it cannot locate the signing moment inside
  [`declared_issue_time`, `anchor_time`]. Evaluating authorization only
  at `declared_issue_time` would therefore admit a revocation/backdating
  interaction: a key revoked inside the δ window could sign *after*
  revocation while declaring a time just before it, and pass both P5 and
  a point-evaluated P6. Accordingly, `VALID_STRICT` requires
  authorization **throughout the uncertainty window**:

      key_authorized(declared_issue_time)
      ∧ no revocation effective at or before anchor_time

  Revocation effective *after* `anchor_time` does not retroactively
  change the verdict. Revocation effective at or before `anchor_time`
  yields `INVALID`.

  **Key lifecycle is monotonic, by design commitment.** Revocation is
  terminal: a revoked key is never re-authorized; re-keying issues a *new*
  key with a new fingerprint and a new manifest entry. Without
  monotonicity, "no revocation effective at or before `anchor_time`"
  would be ambiguous across revoke–re-authorize cycles; with it, the
  interval check is well-defined. This is an issuer key-management rule
  that the model *assumes* and operational policy *enforces* — a design
  commitment, not a cryptographic assumption, and deliberately not filed
  under Layer 2.

  This interval evaluation is deliberately stricter than checking
  `declared_issue_time` alone, and it can fail honest receipts whose key
  was revoked between declaration and anchor confirmation — the correct
  fail-closed outcome: the system cannot honestly prove such a receipt
  was signed before the revocation, and the issuance protocol (P5
  corollary) already treats unconfirmed issuance as incomplete. (The
  checkable form of §4.4's revocation paragraph, in A1.6's vocabulary.)
  **[model]**

- **P7 — Wrapper and object-type soundness.** Every signed object carries
  a domain-separation type tag *inside the signed bytes*, drawn from the
  enumerated set: base attestation, wrapper, issuer-key manifest,
  authority evidence, conformance vector, review-recency attestation
  (§4.7). No trace exists in which an object of one type is accepted as
  another (no cross-type confusion). A wrapper commits to the inner
  package's **exact bytes, embedded as an opaque byte string** (e.g.,
  base64 of the inner package's framed bytes) — never as parsed JSON.
  Outer canonicalization must be structurally unable to re-serialize,
  re-escape, or otherwise touch the inner byte stream: a nested-JSON
  embedding would let a different outer canonicalization version silently
  alter the inner bytes and break the inner signatures and OTS proof.
  (Hash-only commitment is rejected: the inner bytes must travel *inside*
  the bundle, or P9's self-containment fails.) The wrapper records both
  inner and outer canonicalization versions. Wrapping never alters the
  inner package's
  independently-computed verdict — the wrapper attests the inner *bytes*,
  never the inner *verification result* (preserving §3.1's distinction
  exactly). **[model]**

- **P8 — Canonicalization injectivity, framing, and rejection.**
  `canonical()` is injective on its **accepted payload domain**, and the
  encoding is boundary-unambiguous. JCS (RFC 8785) itself carries no
  length header, so the frame supplies it: signatures and anchors commit
  to a **framed envelope** —
  `type_tag || canonicalization_version || payload_length || payload` —
  where `payload` is the JCS bytes. The *issuer* constructs the frame; the
  *verifier* reconstructs it independently and rejects any mismatch; the
  exact binary layout is fixed, with golden vectors, before the Band 1
  freeze. A parser cannot disagree about where the payload ends. The
  accepted domain is
  closed by explicit *rejection*: anything outside it is refused, never
  "helpfully" normalized. Rejection is required, at minimum, for:
  duplicate object names; `NaN`/`Infinity`; numbers not exactly
  representable as IEEE 754 doubles (per §4.3, such values must be
  string-encoded); `-0` and numeric edge cases; non-I-JSON strings;
  inputs relying on Unicode normalization assumptions; unknown
  canonicalization versions; trailing bytes; type-tag mismatch;
  length-prefix mismatch. Golden vectors (§4.3) evidence the positive
  domain; the rejection suite evidences the negative domain — both are
  H1a obligations. Injectivity over the accepted domain is discharged by
  direct proof. **[proof]**

- **P9 — Verification statelessness.** The verdict is a pure function of
  the bundle and the verifier's declared policy — no service-side state,
  no live network dependency, appears in the decision. (The checkable form
  of §4.4's hard rule.) **[model]**

- **P10 — Manifest authority (external evidence plus possession).** The
  issuer-key manifest carries **two independent, archived, time-anchored
  authority-publication evidences** — the DNSSEC snapshot and the anchored
  repository publication (A1.5) — **plus** a manifest self-signature by the
  issuer keys. The self-signature proves *possession* and binds the
  manifest bytes to the asserted keys; it is **not authority evidence and
  is never counted as an authority channel** — an adversary substituting
  their own key self-signs trivially. `VALID_STRICT` requires **all**
  external authority evidences to validate, plus proof-of-possession.
  Property: an adversary controlling any proper subset of the external
  authority channels cannot cause a manifest asserting a non-authorized
  key to satisfy the `VALID_STRICT` evidence requirement. Missing or
  partially-validating evidence degrades by A1.2.1's explicit-policy
  logic, naming which authority evidence was waived and why — never
  silently. **[model]**

**Change discipline.** This list may be amended before Band 0 exit only by
a further signed, dated amendment stating what changed and why — the same
rule as everything else in the pre-registration. Silent narrowing of the
property list is the failure mode this section exists to prevent.

### A1.2.1 Degraded-policy semantics (the waiver lattice)

`VALID_DEGRADED` exists so long-horizon verification does not collapse to
a boolean — not as a universal escape hatch. Its scope is fixed here:

**Non-waivable checks.** No verifier policy may waive: canonical-byte
integrity (P1, P8); type/domain separation (P7); boundary framing (P8);
key-to-issuer binding for every accepted signature (P3); temporal-anchor
consistency (P5). A package failing any non-waivable check is `INVALID`
under **every** policy — no degraded policy may promote it
(*monotonicity*). A non-waivable check that *cannot be performed* yields
`UNVERIFIABLE`, never any `VALID` state — the P4 partition applies inside
the lattice: performed-and-failed → `INVALID`; unperformable →
`UNVERIFIABLE`; neither is promotable.

**Waivable checks (declared redundancy only).** Degraded policies may
weaken only declared redundancy requirements: accepting a subset of the
issue-time signature set (P2); accepting fewer than all external
manifest-authority evidences (P10); accepting a signature whose trust root
is no longer independently recoverable, where the remaining checks pass.

**Recording.** Every `VALID_DEGRADED` verdict records the precise waived
check set and the policy that authorized the waiver — the informed-consent
act of §3.1, made auditable.

---

## A1.3 The adversary model (explicit capabilities)

The Band 0 adversary can, at minimum:

1. **Alter** any bytes of a package, receipt, manifest, or wrapper after
   issue.
2. **Strip, reorder, or duplicate** signatures within the signature set.
3. **Substitute keys** — including choosing keypairs *after* seeing valid
   signatures (the DSKS capability of P3) — and always self-sign with keys
   it holds (possession is free to the adversary; see P10).
4. **Replay** valid packages, receipts, or manifests in other contexts, and
   re-frame objects across the P7 type boundaries.
5. **Craft manifests** freely, and anchor anything: anchoring proves
   existence at a time, not authority (A1.5, A1.6).
6. **Control any proper subset of the external manifest-authority
   channels** (P10).
7. **Drive the legitimate issuance path** with authorized credentials —
   named to re-affirm the original's misissuance boundary: this adversary
   is *out of scope for the cryptographic construction* and is met by
   operational controls (§3.1, threat classes). The model documents the
   boundary; it does not pretend to cover it.

The adversary cannot break the idealized primitives — signature
unforgeability, hash collision/preimage resistance, or the temporal-anchor
assumptions — which are the cited Layer 2 assumptions (original H0; A1.6).

---

## A1.4 Tooling: the right tool per target, not the familiar tool

The original said "TLA+ and/or Lean4." That was reached for on familiarity,
and the review contested it — recorded here in the §6
disagreements-on-the-record spirit:

- **The verifier state machine and temporal logic (P1, P2, P4, P5, P6, P7,
  P9, P10)** — TLA+. This *is* state-machine work, TLA+'s home turf, and
  the author can read and defend TLA+ cold, which the agreement gate
  requires.
- **The composition under an active adversary (P1–P3, P7 under A1.3)** —
  a symbolic protocol verifier, **Tamarin or ProVerif**, whose built-in
  Dolev-Yao adversary derives, replays, and substitutes messages natively.
  Hand-rolling an adversary inside TLA+ would make the proof's value rest
  on the fidelity of that hand-rolled adversary — reintroducing the
  wrong-model risk at the exact spot it is hardest to review.
- **Canonicalization injectivity (P8)** — direct proof over the encoding
  rules (Lean4 if warranted, rigorous prose proof plus the golden-vector
  and rejection suites if that is honest sufficiency), separate from the
  state-machine work.

**Tool-choice discipline (anti-tool-shopping).** "Tamarin or ProVerif"
must not become "whichever tool proves the desired result." The choice is
fixed *before* theorem-proving begins: a bounded spike may compare the two
only on **expressiveness and author-readability** for P1–P3/P7 under A1.3
— not on which yields the proof. The choice, the rejected alternative, and
the reason are committed before substantive proof work starts. Switching
tools later requires a signed amendment naming the blocker.

**The readability trade-off, named.** The author reads TLA+ but not (yet)
Tamarin's lemma language or ProVerif's applied pi calculus. A tool the
author cannot audit weakens the human half of the agreement gate exactly
where it matters most. Mitigation, committed to here: every
symbolic-verifier lemma carries a **prose mapping** back to the A1.2
property it discharges, and the informal written proof (H0 requirement 3)
covers the composition argument in the author's own words regardless of
tool.

**Cross-model correspondence (the two-formalisms risk, named).** The
construction is formalized twice — a TLA+ state machine and a symbolic
protocol model — and two formalisms of "the same" system can quietly
describe two subtly different systems, each verified, neither wrong,
jointly meaningless. The informal written proof must therefore include an
explicit **correspondence mapping** between the TLA+ transitions and the
symbolic tool's rules/facts, arguing that both describe the same
construction; the model-derived conformance vectors (A1.7) test both
against the same implementation, which bounds — but does not eliminate —
the divergence risk.

Learning to read the symbolic tool's output well enough to contest
it is part of the capability H0 demonstrates — the deskilling defense
(§6), applied at the new edge.

---

## A1.5 Manifest authority: resolving the circularity

The review surfaced a hole in §4.4 as written: the bundle's issuer-key
manifest was to carry "timestamped evidence that those keys were authorized
issuer keys at issue time, the manifest itself anchored." But **anchoring
proves existence, not authority** — anyone can anchor a manifest claiming
anything. A manifest signed by the keys it authorizes is circular; a
manifest signed by a separate root key reintroduces the single trust
domain §3.1 rejects.

**Resolution (not deferral): apply §3.1's own argument recursively.**
Authority at issue time cannot be conjured from nothing — every PKI bottoms
out in trust anchors; the honest move is to make the anchors plural,
independent, archived, and time-anchored. The manifest carries **two
external authority-publication evidences plus proof-of-possession**:

1. **DNSSEC chain snapshot** — the `wamason.com` records publishing the
   issuer-key fingerprints, with the signature chain to the root as it
   existed at issue time, *archived in the bundle* (discovery channels stay
   discovery; the archived snapshot is what verification uses).
2. **Anchored repository publication** — the public git commit publishing
   the same fingerprints, with the commit object, its signature, the
   relevant proof material, and the OTS proof **archived in the bundle**
   (like the DNSSEC snapshot: verification uses the archive, never live
   repository availability — P9).
3. **Manifest self-signature** by the issuer keys — *proof of possession
   only*. It binds the manifest bytes to the asserted keys and is never
   counted as authority evidence (P10): an attacker's invented key
   self-signs for free.

`VALID_STRICT` requires both external evidences plus possession. A future
verifier sees that at issue time, two channels with independent operational
failure modes asserted the same key authority, and the asserted keys were
demonstrably held. Subverting the process requires tampering with both
external channels, at or before issue time, consistently.

**Declared residual risks (difficulty, not impossibility):**

- **Correlated control.** Both external channels are ultimately operated by
  the same author — same registrar sphere, same person. Their independence
  is real against *channel failure* (registrar lapse vs. repository-host
  lapse) and against an attacker who compromises one channel; it is weaker
  against an adversary who owns the author's entire operational sphere at
  issue time. That adversary sits at the misissuance boundary (A1.3, item
  7) and is met operationally, not cryptographically.
- **Trust-anchor recursion.** The archived DNSSEC chain validates against
  the root trust anchors *as they existed at issue time*. A verifier
  decades later needs trustworthy knowledge of those historical anchors —
  which is itself a historical-authority question. Concretely, the
  reference verifier maintains an **archived historical trust-anchor
  store** (DNS root keys and repository signing keys, by validity period),
  distributed *with the verifier* as trust configuration — not
  service-side state, so P9 is not violated. The plural-evidence
  structure and the §3.1 wrapping model (re-anchoring under fresh trust
  *before* old roots decay) mitigate the remaining recursion; they do not
  eliminate it.

Not *perfect* — plural evidence is a difficulty argument, not an
impossibility proof, and it is declared as such — but *difficult*, and P10
makes the difficulty claim checkable.

---

## A1.6 Temporal anchor semantics, stated precisely

The original's forgery argument ("producing a valid OTS anchor at the
original time") compressed what the anchor actually establishes. Precisely:

- **Vocabulary.** `declared_issue_time` — the issue time the issuer claims,
  committed inside the signed canonical bytes. `anchor_time` — the Bitcoin
  block time of the OTS anchor over those bytes.
- **The anchor is an upper bound on creation time.** The anchor proves the
  bytes existed *not after* `anchor_time` — nothing more. It provides **no
  lower bound**: old bytes can be stamped today, and a forger with
  compromised keys can sign new bytes today. What the anchor prevents is
  *backdating* — obtaining a conforming anchor in the past for bytes
  created now. New forgeries dated honestly-now are the key-compromise /
  misissuance classes (§3.1), met operationally, not by the anchor.
- **The verifier enforces a two-sided consistency check (P5).**
  `declared_issue_time − ε ≤ anchor_time ≤ declared_issue_time + δ`, with
  strict defaults δ = 72 hours and ε = 24 hours, both declared per receipt
  and ratified (or revised, on the record) at Band 0 exit. Temporal
  consistency is non-waivable (A1.2.1). The issuance protocol treats
  anchor confirmation — at minimum depth k, strict default k = 6 (P5
  corollary) — within δ as part of successful issuance; late or reorged
  anchors force re-issue.
- **Layer 2 assumptions, extended.** To the original's cited assumptions
  (signature unforgeability, SHA-256 resistance, OTS/Bitcoin timestamp
  assumptions) add, explicitly: Bitcoin block timestamps are inexact —
  consensus rules (median-time-past, the two-hour future bound) bound but
  do not eliminate skew — absorbed into δ and ε; anchors at depth ≥ k are
  treated as permanent (a reorganization deeper than k is out of model,
  subsumed by the history assumption that follows); and **the
  proof-of-work history remains intact and available over the
  adjudication horizon**. A
  fifty-year adjudication story rests on Bitcoin's fifty-year survival;
  stating that plainly is the declare-what-you-cannot-see ethos, applied
  to the anchor itself.

---

## A1.7 The agreement gate, hardened

The original gate asked author and AI to independently *agree* the model is
faithful. Confirmation tasks produce weak evidence: a reviewer re-reads the
author's framing and nods, because the framing is persuasive — that is why
the author chose it. And the AI collaborator that helped author the model
agreeing with it is close to self-review. Two changes, both consistent with
§4.5's different-model discipline, applied one level up:

1. **The fidelity review is a falsification task performed by non-author
   models.** Models that had no hand in authoring the formal model receive
   the A1.2 property list (prose) and the model itself, and are tasked
   adversarially: *construct a concrete trace the model accepts that the
   properties say must be rejected, or a property the prose implies that
   the model fails to state.* A reviewer who hunted for a counterexample
   and failed is evidence; a reviewer who agreed is a nod. The hunt's
   artifacts are committed either way — found or not found — and each
   review records, for reproducibility: model, vendor, and date; the
   prompts used; configuration where available; the hash of the exact
   input bundle; and whether the reviewer saw prior review transcripts.

2. **Model-derived conformance vectors.** The model checker's explored
   traces are mechanically extracted into concrete fixtures for the real
   verifier — each trace names inputs and the verdict the model requires
   (e.g., "manifest requires {KMS, GPG}, bundle carries only KMS →
   `INVALID`"). This narrows the declared model-to-code gap (the code is
   tested against the model's exact predictions, not hand-written
   approximations of them) and doubles as a fidelity check: an unfaithful
   model, concretized into fixtures, produces *visibly absurd test cases*
   — far easier to catch than a subtle misstatement in temporal logic.
   These vectors become part of the H1a suite, with a clean division of
   labor: model-derived vectors *evidence* conformance to the model on the
   extracted traces — testing, not proof of implementation/model
   equivalence, preserving the original's attested-not-proven discipline
   for the model-to-code gap; the adversarially-authored red-bar attacks
   (§4.5) hunt for what is *outside* the model. **Declared limitation:** the trace-to-fixture translation
   is itself a step with fidelity risk — abstract states must be
   concretized into real byte-level bundles. The concretizer is therefore
   reviewed under the same non-author discipline, and its output is
   spot-audited by eye; the risk is named, not waved off.

**Declared residual risk — self-adjudication.** Whether a reviewer's
counterexample stands or is refuted is judged by the author. Independent
adjudication costs money the pre-registered no-spend constraint (H3)
forbids; the softness is therefore declared rather than concealed, and
every adjudication (counterexample accepted or refuted, with reasoning) is
committed alongside the review artifacts, so a future reader can re-judge.

H0's resolution criteria are amended accordingly: requirement (2) now
reads — the falsification-task review by non-author models has run, its
artifacts are committed, and no unrefuted counterexample stands; and the
conformance-vector extraction is added to the H1a evidence obligations.

---

## A1.8 What did change, and what did not

The ranked objectives (§1), the bands and the H1–H3 hypotheses as
originally registered, the hard invariants (§4), the success and kill
criteria (§5), and the division of labor (§6) are **not weakened** by this
amendment. This amendment **adds** obligations: pre-registered theorem
statements and a waiver lattice (A1.2, A1.2.1), an explicit adversary
model (A1.3), a tool-choice discipline (A1.4), a manifest-authority
mechanism with declared residual risks and a historical trust-anchor
store (A1.5), precise temporal semantics with new Layer 2 assumptions and
a confirmation-depth rule (A1.6, P5), a key-lifecycle monotonicity
commitment (P6), an opaque-embedding rule for wrappers (P7), a
framed-envelope specification (P8), a falsification-style agreement
gate with reproducibility requirements, new H1a evidence obligations
(conformance vectors, the P3 verification profile, the P8 rejection
suite), and an auditable H0 falsifier (A1.1). The gate (§8) is unchanged
in intent: Band 0 resolves before Phase 1 begins, and "the foundation did
not hold" remains a valid, honest outcome. What this amendment changes is
that the gate can no longer be *passed by accident* — the theorems are
named, the adversary is named, the tools fit the targets, and the fidelity
check tries to break the model instead of blessing it.
