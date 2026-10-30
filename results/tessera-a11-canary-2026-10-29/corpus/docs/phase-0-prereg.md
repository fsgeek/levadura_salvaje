# Tessera — Phase 0 Pre-Registration

> **What this document is.** A dated, GPG-signed, OpenTimestamps-anchored
> declaration of intent, made *before* the system it describes is built. Its
> credibility comes from the fact that it cannot be backdated: the Bitcoin
> anchor on the commit that introduces it fixes its existence in time. The
> build journal that follows will be measured *against* this document —
> including, honestly, where reality diverged from it.
>
> **Why pre-register at all.** Anyone can write a flattering after-the-fact
> story. Pre-registration converts the build log from a highlight reel into
> evidence: the hypotheses, success criteria, and design commitments are on
> record before the outcomes are known, so the reader can check the work
> instead of trusting the narrator.

---

## 0. Provenance of this document

- **Author:** Tony Mason (architecture, judgment, all decisions herein).
- **AI collaborator:** Tyst (`tessera@wamason.com`) — mechanics, drafting,
  pushback. Division of labor is explicit and recorded; see §6.
- **Integrity:** this commit is signed by the Tyst key (ed25519,
  `2B9C F308 ...42C7 3835`) and anchored via OpenTimestamps. The signing key
  is the WHO layer; the OTS anchor is the WHEN layer.

An AWS native attestation service modeled on our work in Willay: a robust
demonstration of building, validating, observing, and deploying a
beta-quality attestation service.

---

## 1. Objective and the honest ranking

The function of an attestation service is to provide a neutral, third
party's cryptographic binding to a package of information delivered to
it.  Attestation in this usage is similar to SSL certificates that say
"this attestation says that the party in control of a website has
demonstrated this control and the following certificate validates it."

The distinction here is that a Tessera attestation is an attestation of
information at a fixed point in time, while an SSL certificate is an
attestation of website ownership with a fixed expiration.

Why would you use an attestation:

1. to demonstrate a tamper-resistant pre-registration, such as a hypothesis,
   an experimental design, and a predicted outcome.
2. to record the findings of one or more third parties, such as an
   audit, regulatory policy, ontology, or citation.  Note: this is a
   suggested but not exhaustive list.
3. to record agreements between parties, such as a contract, and
   signatures of parties to that contract, similar to the way a notary validates
   documents.

The distinction here is that this attestation is over a _digital artifact_.  Thus,
for example, the SHA256 hash value of a document, or a blockchain address, or
some other unique identifier, might be part of the digital artifact.

This service provides a cryptographic signature and timestamp over the digital artifact
and that attestation receipt permits future parties to verify the attestation.
The design is done in such a way that the receipt is verifiable independent
of the attestor, which ensures the ability of parties in the future to validate
the signed artifact.

**The honest ranking.** Two objectives, strictly ranked, and the ranking is
the discipline:

1. **Primary — the demonstration.** Close the operational-envelope gap (§7):
   show that I can build, validate, observe, secure, and deploy an attestation
   service to a beta-quality bar, with the engineering rigor visible in the
   repository itself. This is the objective. It succeeds or fails on its own,
   independent of whether anyone ever pays for the service.

2. **Secondary — possible commercial service (upside, not premise).** Tessera
   may become a viable attestation-as-a-service. If it does, good — but the
   revenue-bearing pieces (billing/payment integration, PCI *certification*,
   customer acquisition, scaling for real traffic) are **deferred until
   validated paying demand exists**, and built no sooner. The product dream
   does not expand the demonstration's scope. Note the distinction the primary
   objective *does* honor: Tessera is architected **to the PCI standard**
   (minimal cardholder-data environment, segmentation, key custody) as a matter
   of engineering discipline — designing to the bar is demonstration; obtaining
   the certificate is product, and waits.

**Credibility line (non-negotiable):** every architecture decision here is
the human author (Tony) in collaboration with AI agents. The purpose of
the AI agents is to accelerate the typing, push back on my decisions, clarify
them, but not to _make_ those decisions without consultation.

---

## 2. Hypotheses (falsifiable, dated)

A key aspect of designing this project is to identify the anticipated
criteria for evaluating the project itself.

The work is decomposed into dependency-ordered bands. The bands matter because
they have different risk profiles, and the hypotheses are stated per band rather
than lumped into one figure. **Band 0 precedes all of them:**

0. **Band 0 — the formal foundation (H0).** Before any code, the central
   guarantee is established by a machine-checked formal model and proof (see
   H0). This is formal-methods work, not software engineering, and it gates
   everything: if the guarantee cannot be proven, there is nothing worth
   building. No time bound — a rushed proof is worse than none — and the
   Phase 1 / H1b clock does not start until Band 0 is resolved.
1. **Band 1 — cloud-independent core.** The cryptographic guarantees, proven
   on a laptop with no AWS and no LocalStack. This is the invariant the later
   bands must not break. It has no irreducible wall-clock latency in its test
   path (OTS *confirmation* latency is deferred to band 3; band 1 tests use
   stamped-not-yet-confirmed proofs). Throughput-bound, fast.
2. **Band 2 — local vertical slice.** The same guarantees delivered through
   the LocalStack-emulated pipeline (S3/DynamoDB/SQS/Lambda/KMS), sustaining
   a steady issue rate. Cloud-*shaped* but free and local.
3. **Band 3 — real cloud.** The operated service on actual AWS: the attack
   surface, real KMS, observability, adversarial attack, cost/capacity claims.
   Wall-clock-bound (terraform apply, GuardDuty population, OTS confirmation),
   slow and externally gated.

- **H0 — the foundational claim (gates the entire project).** Tessera's central
  guarantee — that altering any part of a signed attestation package requires
  solving a computationally hard problem — is established by *formal proof of a
  machine-checked model*, with one honestly-declared gap between model and code.
  This is not software engineering; it is the precondition for Tessera being a
  *commercial* offering rather than a demonstration of confidence. A party
  relying on an attestation in adjudication must be able to *depend* on the
  guarantee, not trust an assertion of it.

  *Two layers, kept distinct (so the claim cannot be accused of formal-methods
  theater):*
  - **Layer 1 — symbolic composition invariant (what the checker proves).**
    Assuming *idealized* signatures, hashes, canonicalization, and temporal
    anchors, a machine-checked model (TLA+ and/or Lean4) establishes that the
    verifier accepts only packages satisfying the intended integrity and
    ordering properties — e.g. "no transition leads to an accepted receipt over
    altered bytes," "ordering/replay conditions hold." This is exactly what
    state-machine and proof tooling is good at.
  - **Layer 2 — computational assumptions (what is depended on, not proven).**
    The idealized primitives are justified by *external* assumptions we cite,
    not discharge: signature unforgeability, SHA-256 collision/preimage
    resistance (only as actually needed), and Bitcoin/OpenTimestamps timestamp
    assumptions. The cryptographic claim "altering any part requires solving a
    computationally hard problem" holds *under these stated assumptions and an
    explicit adversary model* — it is not proven from nothing.

  *The verification chain, by trust source:*
  1. **A machine-checked formal model** of the construction (Layer 1 above).
     The checker establishes that *the model* has the claimed properties — but
     **not** that the model is the *right* model. Model fidelity to intent is a
     human judgment, not a checkable one. What is proven is **our own
     composition** (Layer 1) under the cited primitive assumptions (Layer 2);
     the document states crisply which is which.
  2. **An agreement gate:** author and AI must each independently agree the
     model faithfully captures the claim before it is handed onward — a
     cross-model convergence, not a single nod, to catch "the checker proved the
     wrong model."
  3. **An informal written proof** (not required for the proof obligation —
     the checked model carries that — but required as the H2 evidence for the
     formal core). A passing checker is identical whether the human owns the
     formalism or prompted an AI into it; the written, defend-it-cold prose is
     the artifact that demonstrates the *author's understanding* of the core,
     which is the primary objective (§1) and the deskilling defense (§6) at the
     spot it is hardest and most tempting to skip.

  *Human external review is NOT a resolution requirement — deliberately.* The
  gate is **machine-checked** (free, deterministic, repeatable, in CI, in our
  control). Requiring an *independent human* formal-methods reviewer would set
  the bar where it cannot be met under the pre-registered no-spend constraint
  (H3): a competent reviewer costs money, so a human-review gate would either
  stall the project indefinitely in Band 0 or force spend we committed against.
  Therefore human external review is an **optional enhancement, gated on a
  revenue stream (the secondary objective, §1)**. Its *absence is a declared
  residual risk:* a machine-checked proof and multi-model agreement reduce the
  probability of an undetected flaw but do not eliminate it — no review,
  machine or human, guarantees a future party will not find a hole. That
  residual risk is accepted and disclosed, not concealed. (Earlier drafts made
  human external review a hard gate; that was an over-tightening, removed.)

  *The declared gap (what is attested, not proven):* the chain proves *the
  model* sound. It does **not** prove that *the code implements the model* —
  that link is *attested, not proven*. When the code deviates from the model,
  that is a *bug*, hunted by the H1a adversarial suite — the ordinary
  spec-to-implementation relationship, stated plainly rather than concealed.
  Declaring this gap is the Tessera ethos applied to Tessera: declare what you
  cannot see.

  *Resolved when:* the machine-checked model (1) holds under its stated
  assumptions, the agreement gate (2) has passed, and the informal written
  proof (3) is in the repository, with the model-to-code gap documented. Human
  external review is not required for resolution (see above); if later obtained
  under a revenue stream, its outcome is recorded. *Falsified if:* no such proof
  can be produced, or
  it shows the guarantee fails under realistic assumptions — **the project does
  not proceed to Phase 1 as designed.** The H1b clock does not start until H0
  is resolved.

- **H1a (band 1 — crypto core):** The cloud-independent cryptographic core is
  frozen *before* any LocalStack work begins, with adversarial evidence that
  the implementation conforms to the H0 model. (Tests do not *prove*
  correctness — H0 is the proof gate; H1a is *implementation evidence* that the
  code rejects the enumerated attacks and conforms to the model's expected
  verifier behavior.) *Falsified if:* there is not a public, adversarially-
  authored red-bar suite that, for each attack family — forge, tamper,
  backdate, break-chain, strip-one-signature — and each degradation scenario,
  shows the verifier emits the **correct explicit verification state** (see
  §4.6): `VALID_STRICT`, `VALID_DEGRADED(policy)`, `INVALID`, or `UNVERIFIABLE`.
  Emitting the *right* state for every case is the criterion — including the
  fail-open trap of returning `VALID` where the honest answer is `UNVERIFIABLE`.
- **H1b (band 2 — vertical slice speed):** A local vertical slice (issue →
  verify → chain a receipt, all on LocalStack) sustaining **1 attestation/second**
  lands within **7 calendar days** of the Band 1 freeze. The 1/sec figure is a
  *functional throughput* check (the pipeline sustains a steady rate without
  deadlock or chain corruption), explicitly **not** a real-infrastructure
  performance claim — LocalStack's performance characteristics are not AWS's.
  *Clock (as a state machine, no ambiguity):*
  H0 resolved → Phase 1a implements the cloud-independent crypto core →
  **H1a freeze commit** (dated, signed; this both closes H1a and opens the H1b
  window) → Phase 1b builds the LocalStack slice → **H1b evidence commit** must
  land within 7 calendar days of the H1a freeze commit. Both endpoints live in
  the anchored git history; elapsed time is auditable from the timestamps, not
  asserted from memory.
  *Falsified if:* no H1b evidence commit demonstrating 1/sec sustained on
  LocalStack lands within 7 calendar days of the H1a freeze commit.
- **H2 (division of labor):** The architecture decisions are demonstrably
  mine; AI handled mechanics. *Falsified if:* the multi-model review panel (the
  same ≥3 unrelated LLM models that adversarially review security in §5, here
  tasked to interrogate architecture ownership) finds a load-bearing decision I
  cannot justify without reconstructing it from the AI's reasoning. The panel is a
  proxy for the only reviewer who matters: someone reading the repository to
  see what was actually done.
- **H3 (cost discipline):** Three separate numbers, so none can be trivially
  contradicted by the pricing page:
  - **demo-cycle variable cost under $25** — a complete cycle (`terraform apply`
    → run the full red-bar + load suite → `terraform destroy`) at standard
    on-demand pricing;
  - **persistent monthly footprint under $5/month** — the intentional always-on
    pieces (each customer-managed KMS key ~$1/mo, a Route 53 hosted zone
    ~$0.50/mo, the ledger's S3 bucket) are low single-digit dollars, *not*
    "cents";
  - **idle compute exactly $0** — nothing *runs* between demonstrations (no
    Fargate task, idle EC2, or provisioned capacity).

  Cost is measured against *standard* pricing, not free-tier: free-tier credits
  may cover actual spend, but H3 evidences cost *governance*, not subsidy.
  *Falsified if:* a measured demo cycle exceeds $25 at standard rates, the
  persistent footprint exceeds $5/month, or any idle compute persists between
  demonstrations.

---

## 3. Architecture decisions (the part that is genuinely yours)

### 3.1 The signing-architecture decision — KMS vs. GPG vs. dual

The decision space, stated neutrally before the decision and its reasoning:

- **Willay's model (A):** local GPG signs; verification needs only the
  pinned fingerprint and the bundle. Maximally portable, zero infrastructure.
  Rejected for Tessera because it exercises no cloud-native services — it's
  "Willay with extra overhead."
- **KMS-native (B):** KMS signs the cloud receipt. This exercises real
  cloud-native key custody, and current KMS supports offline-verifiable
  asymmetric signatures — including `ECC_NIST_EDWARDS25519` (Ed25519) and
  post-quantum `ML-DSA` (FIPS 204) key specs; the private key remains in KMS
  while the public key downloads via `GetPublicKey` for verification outside
  AWS. B is therefore **technically viable** — the earlier belief that KMS
  could not sign Ed25519 was wrong (corrected against current AWS docs). It is
  rejected as the *sole* trust mechanism not because KMS is incapable, but
  because it concentrates issuer custody, AWS account lifecycle, key-deletion
  risk, IAM/policy risk, and public-key-provenance risk in **one operational
  domain**.
- **Dual-attestation (C), the chosen path:** KMS signs the cloud receipt to
  demonstrate cloud-native custody, **and** local GPG counter-signs to preserve
  a portable, independent WHO layer (Willay's). Public keys are published via
  DNS (`wamason.com`, DNSSEC), repositories, and the bundle. The justification
  is **not** that KMS is incapable; it is that a long-lived attestation should
  not rest on a single operational trust domain.

**Decision: C.**

**Why C, defended cold.** The threat model for an attestation is not "is this
signature valid today" — it is "will this signature adjudicate in fifty years,
when the issuer may be gone." B is technically capable (it can even produce
offline-verifiable Ed25519 or post-quantum signatures), but it places the
entire trust story in **one operational domain**: AWS account lifecycle, KMS
key-deletion policy, IAM, and the provenance of the published public key all
sit together. If that domain lapses — the account closes, the key is deleted,
the policy changes, the published key's provenance becomes unclear — the
attestation's verifiability is at risk, all at once, for correlated reasons.

C signs the same canonical bytes with two keys from *independent failure
domains* — KMS (cloud-native custody) and local GPG (Willay's portable WHO
layer). They fail for *uncorrelated* reasons (AWS account/policy lapse vs. local
key disclosure), so the attestation's durability does not rest on any single
domain surviving. **Not replicating is what concentrates the risk**; the cost of
C over B is essentially nil, and the benefit is that attestations stand up to
adjudication even if one trust domain disappears entirely.

**Key distribution is a separate axis from dual-signing.** Public keys are not
secret; they are published redundantly — via DNS (`wamason.com`, DNSSEC), in
public repositories, and in the attestation bundle itself. This defends against
any single distribution channel expiring. Note this redundancy could be applied
to B as well; it is *not* what justifies C. What only C provides is two
independent signatures whose validity does not share a failure domain.

**Verification policy lives with the verifier, not frozen into the receipt.**
The attestation carries a *set* of signatures (a JSON map of key-type →
signature), not an AND/OR rule. The default reference verifier requires **all
issue-time signatures to verify** — the strong guarantee a naive holder gets
without having to understand the policy.

This fail-closed default is not a fragility to apologize for; it is the system
refusing to lie. If one signature can no longer be verified, we will **not**
let a naive holder assume the attestation is still fully valid. A verifier
*may* override and accept a lower bar — but the act of overriding is itself an
informed-consent step: by relaxing the requirement, the verifier has
demonstrated they understand the tradeoff and have knowingly accepted a weaker
guarantee, thereby changing their own self-label from "naive" to "not naive."
The objection "but naive users will be misled by a relaxed check" therefore
cannot land: the category it worries about cannot exist, because relaxing the
check is precisely the act that exits naivety. (Long-term, the wrapping model
below lets fresh assurance be re-anchored *before* old algorithms fail, so a
fully-strict verification can remain available across decades — but that is
additional assurance, not a rescue this default requires.)

That argument is the *justification*; the *mechanism* that implements and tests
it is an explicit set of verifier states (this is what makes the policy
auditable rather than rhetorical, and it is the H1a acceptance criterion —
§4.6):
- `VALID_STRICT` — all issue-time signatures verify (the fail-closed default);
- `VALID_DEGRADED(policy=...)` — accepted under an explicit, recorded weaker
  policy the verifier chose (the informed-consent override);
- `INVALID` — a required check failed;
- `UNVERIFIABLE` — a check could not be performed (missing key, unsupported
  algorithm, expired trust root). Critically, this is **never** silently
  promoted to `VALID`.

**Temporal upgrade by wrapping, not replacement.** Cryptographic strength
decays; post-quantum standards are still in flux, and the right time to choose
a PQ algorithm is when a customer needs that guarantee — it will be a
*different* key algorithm, a real architectural choice encoded per-receipt.
Rather than re-sign old payloads (which would require the original
canonicalization to remain byte-identical forever), a **superseding
attestation wraps the original package** and signs *that* with the new-algorithm
key. The inner attestation's bytes, signatures, and OTS proof are immutable;
the wrapper is a new layer with its own time-anchor. This (a) makes the
upsigning *visible and ordered* rather than a silent mutation, (b) lets a
customer add PQ assurance *while the original keys are still trusted* — the
window in which bootstrapping new trust is actually sound — and (c) dissolves
the canonicalization-freeze problem into per-layer versioning: each layer
records which canonical form it used. Wrapping is a *paid* operation; nesting
depth is therefore bounded by willingness to pay (as PKI key sprawl is bounded
by storage budget), not by a protocol cap. It is for rare, high-value
supersession, not routine.

**What the wrapper attests.** The base service wrapper attests *integrity of
the inner object* — "this 2026 package existed and is bit-for-bit unaltered,
re-anchored under a 2030 algorithm." It commits to the inner package's **bytes**,
**not** to the inner receipt's *verification result* at wrap time: the wrapper
does not assert "the inner receipt was VALID_STRICT when wrapped," because that
would be a form of re-evaluation. The inner receipt's validity stands on its own
signatures, verified independently whenever a relying party checks it. It does
**not** re-evaluate the original claim. Semantic re-attestation (a genuinely new inspection over the old
package, with its own losses and open questions) is a separate, priced business
offering, and — honestly declared — *may not be available years later*, because
the evaluator, context, and resolvable evidence degrade over time. (An expert
report written in 2021 can be updated in 2031, but not for free, and perhaps
not at all.)

**The temporal anchor is an independent trust dimension that crypto advances
do not touch.** The *intended* argument: even total signature compromise should
not let a forger rewrite the *past*, because forging a Tessera attestation would
require breaking the signature algorithm(s) **and** producing a valid
OTS/Bitcoin anchor at the original time — i.e., forging Bitcoin's proof-of-work
history. Length is bound into the canonical bytes every signature commits to, so
length-extension / boundary-ambiguity attacks must also defeat both keys *and*
the anchor.

**This argument is not yet proven, and that gap gates the project (H0).** The
paragraph above states the guarantee we *believe* holds; it is an assertion, not
a formal result. Establishing it — a threat model, a machine-checked formal
model of the composition, and a proof that the model has the claimed invariants
— is **Band 0**, the precondition for building anything. Asserting it here
without proof would be exactly the theater this project exists to refute. See
H0.

**Four distinct threat classes (do not conflate them).** The cryptographic
story above defends two of these; the other two need *operational* controls,
and saying so plainly is part of declaring what we cannot see:
- **Cryptographic forgery** — an attacker produces an accepted receipt without
  authorized signing authority. *Mitigation:* the dual-signature + anchor
  construction (H0).
- **Tampering** — an attacker alters an issued package after the fact.
  *Mitigation:* same construction; the signatures and anchor break.
- **Misissuance** — an *authorized or compromised issuer path* signs content it
  should not. Dual signatures do **not** prevent this if the attacker can drive
  both signers through the legitimate issuance path. *Mitigation:* authorization
  controls and audit logs, **not** cryptography. Named here so it is not
  mistaken for something the signing construction solves.
- **Key compromise** — an attacker obtains signing capability outside normal
  policy. *Mitigation:* KMS/GPG domain separation (§3.1) reduces correlated
  compromise; OpenTimestamps constrains backdating; the §4.2 threat model and
  TTL bound the local-key blast radius.

**Open question (declared, deferred):** a *quantitative* forgery-cost analysis
of the combined construction (signature-set + length-bound canonicalization +
OTS anchor) is not yet done. The argument above is qualitative
(independent-failure-domains); the quantitative bound is unproven. Deferring it
is honest — and the scenario that would make it worth doing (a customer with
many supersessions) is itself the revenue signal that funds the analysis.

**Hard invariants this decision incurs (see §4):** the `canonical(payload) →
bytes` function is the true root of trust and must be frozen and explicitly
versioned; the verification path must depend on *zero* service-side state.

### 3.2 The shared-core / forked-edge boundary

The prior spec proposed reusing Willay's `canonical.py`, signing, models,
evaluators, and ledger logic unchanged, forking only the cloud edges (compute,
key custody, storage, queue), with clean extractability as a goal.

**Decision: the shared-core / forked-edge boundary is not a design priority
for Tessera.** Tessera is a demonstration of *building and operating the
service*, not a reusable, detachable, re-deployable library — that
extractability goal belongs to Willay, not here. Code is reused from Willay
where convenient, but clean separation is not an architectural commitment, and
no effort is spent making the core independently redeployable. This is a
deliberate *narrowing* of scope: optimizing for extractability we do not need
would be wasted work.

(The one piece of Willay's core that *is* load-bearing — and therefore is a
hard invariant, see §4 — is the canonicalization function, because the
wrap/upgrade model in §3.1 depends on it being frozen and versioned. That is a
property of the bytes, not of code extractability.)

---

## 4. Hard invariants

The five standard NFRs (security, reliability, observability, scalability,
usability) are addressed operationally in §5 and the design spec. The items
below are *hard invariants* — not aspirations but rules with mechanical
enforcement, committed to before any implementation. They are the lines that,
if crossed, mean the system has failed regardless of what else works.

### 4.1 Secure observability (hard rule)
Key material is **unloggable by construction** — never logged, not private
keys, not passphrases, not "redacted-but-present," not in a debug branch, not
as a joke. Enforced *mechanically*: structured logging that cannot serialize
key types, plus a CI secret-scan gate that fails the build if signing material
reaches a log sink. Discipline is not the control; the type system and CI are.

### 4.2 Signing-key threat model (explicit, accepted)
The commit-signing key (Tyst, ed25519, `...42C73835`) is **passphraseless**
with a **6-month TTL** (expires 2026-12-07), residing on a firewalled
workstation. **Threat accepted:** host compromise lets an attacker sign as
the tessera committer. **Mitigation:** short TTL + revocation certificate
(already generated). **Deferred (deliberately, not by oversight):**
higher-assurance signing (enclave/secure sandbox so the key never touches an
internet-facing system) until there is real demand for it. This is a defensible
demonstration-project tradeoff; it would NOT be acceptable for a production
root-of-trust, and the journal should say so.

**TTL note.** 6 months is acceptable *for the demonstration* — a passphraseless
key on a firewalled box facing a low-probability, bounded-blast-radius threat.
**Trigger to revisit:** if anyone relies on issued attestations, shorten the
TTL toward monthly *and* move to the deferred enclave/HSM model so
passphraseless-ness stops being acceptable at all.

**Hardware token (e.g. YubiKey) — considered, deferred.** A hardware token for
the local GPG layer would close the passphraseless vulnerability and read well
on a CV. It is declined *for now*, for two reasons that are on-thesis rather
than convenience: (1) it reintroduces interactive touch-to-sign, defeating the
headless, non-interactive signing the project deliberately chose; (2) it
concentrates local-layer custody in a single hardware token — a step *toward*
the single-domain concentration §3.1 rejects, not away from it. It sits in the
same deferred enclave/HSM tier, gated on real reliance, not adopted as security
theater.

**Security review (flagged).** This section is the one most worth an
independent adversarial pass. Per the project's method (§6), that review is a
*different model's* job, not the model that authored this — it is a tracked
item, not a claim of completeness here.

### 4.3 Canonicalization is frozen and versioned (hard rule)
`canonical(payload) → bytes` is the true root of trust — more than any key.
The wrap/upgrade model (§3.1) requires that a signature added years later
commit to bytes reconstructible exactly as they were at issue time. Therefore
the canonical form is **frozen and explicitly versioned**: it never changes
silently; any change is a *new, versioned* canonical form, and every receipt
records which version it used. Length is bound into the canonical bytes (not a
side field), so the encoding is **boundary-unambiguous** by construction (a
parser cannot disagree about where the payload ends).

**Bind to an existing deterministic standard, not a hand-rolled function.**
Canonicalization is the graveyard of cryptographic implementations: differing
language runtimes disagree on whitespace, key ordering, number precision, and
Unicode escaping, which silently breaks cross-platform verification. The
canonical form binds to **RFC 8785 (JSON Canonicalization Scheme, JCS)** rather
than a bespoke `canonical()`. JCS's one sharp edge — numbers must be exactly
representable as IEEE 754 doubles — is handled by an explicit invariant: **any
value not exactly a double (hashes, large/256-bit integers, blockchain
addresses, opaque identifiers) is string-encoded, never a JSON number.** (JCS is
an Informational RFC, not IETF standards-track — cited as the deterministic
serialization we adopt, with the precision rule above closing its gap.)

Operational commitments that make this checkable, not merely asserted:
1. canonicalization **test vectors** are part of the public verifier
   conformance suite;
2. every canonicalization **version has byte-for-byte golden examples**;
3. **wrappers record both inner and outer** canonicalization versions.

(We claim boundary-unambiguity, which is what the length-binding buys. We do
*not* make a blanket "length-extension-resistant" claim — that is
construction-specific and would invite cryptographic nitpicking we have not
earned; the relevant property here is unambiguous framing, proven in Band 0.)

### 4.4 Verification path depends on zero service-side state (hard rule)
An attestation must verify with the service **dead**. The verification path
touches no database, no live service, no cloud reachability. The operational
database exists to *run* the service (who may request an attestation, rate
limits, keys, later billing) and is **never** on the path that *verifies* one.
If verifying ever requires service-side state, the verification-independence
guarantee is broken.

**DNS and repositories are *discovery* mechanisms, not *verification*
dependencies.** A public key sitting in the bundle proves little by itself — the
future verifier needs to know that key was an *authorized issuer key at the
relevant time*. Therefore the bundle carries an **issuer-key manifest**: the
issuer public keys (or references) plus *timestamped evidence* that those keys
were authorized issuer keys at issue time, the manifest itself anchored. The
future verifier then has an archived trust path inside the bundle, rather than
needing live DNS or a reachable repository. DNS/repo remain useful for *finding*
keys; they are not *required* to *verify*.

**Revocation is time-relative.** A key revoked *after* issue does not retroactively
invalidate attestations made *while it was authorized* — the manifest's
timestamped authorization evidence, anchored, establishes the key was valid *at
issue time*, and an attestation signed then remains `VALID_STRICT`. The naive
reading ("the key is revoked now, therefore the receipt is invalid") is wrong and
is exactly the kind of error the verifier-state logic must get right: revocation
*after* the anchored issue time is irrelevant to that receipt; revocation
*effective before or at* issue time means the signature was never authorized
(`INVALID`). This is precisely why the temporal anchor (WHEN) is load-bearing
alongside the signature (WHO).

### 4.5 Adversarial tests are authored by a different model (hard rule)
The red-bar suite's attacks are authored by a *different* model (Codex) than
the one that wrote the implementation, so the implementer cannot unconsciously
shape attacks to what the code survives. This is not perfect (shared
training-distribution blind spots remain) but is a real, defensible separation,
and stronger than self-authored tests. Test/code separation is CI-enforced.

### 4.6 The verifier returns an explicit typed state, never a bare boolean (hard rule)
Verification yields one of `VALID_STRICT`, `VALID_DEGRADED(policy=...)`,
`INVALID`, or `UNVERIFIABLE` (§3.1) — a typed result, never a bare `true`/`false`.
A boolean collapses the load-bearing distinction between "this failed a check"
(`INVALID`) and "this check could not be performed" (`UNVERIFIABLE`), which is
exactly where fail-open bugs hide. The typed state is what makes the fail-closed
policy *auditable and testable* rather than rhetorical, and it is the form H1a's
acceptance criteria assert against.

### 4.7 Review recency is itself attested (hard rule)
This pre-registration's exit gate (§5) uses **multi-model adversarial review** —
not a professional human audit, and not claimed as one. A substantive human
audit requires a paid expert; anything less labelled "audit" would be theater. A
real system has a *recurring* review cycle, not a one-time blessing. So review
recency is made a verifiable property: the service attests *when it was last
adversarially reviewed* (signed, timestamped), and review staleness beyond a
declared threshold fails the invariant. The system that attests artifacts
attests its own audit recency — dogfooding, not decoration.

---

## 5. Success criteria & kill criterion

Three gates, in order, not to be conflated:

- **The gate (§8 / H0)** comes first — the formal foundation. Nothing below
  begins until it is resolved.
- **The initial-slice gate (H1 §2)** — Band 1 frozen, then the LocalStack
  vertical slice at 1/sec within 7 days of the declared Phase 1 start.
- **The whole-project gate (§5 below)** — when Tessera is a credible **v1
  product**, not merely an impressive demonstration. This is a deliberately
  binary, checklist-able bar rather than a subjective "impressive enough"
  judgment, because a credibility artifact wants a done-line a reader can check.

**Done when (v1 product):**
- Sustains **10,000 attestations in a 24-hour period** (~0.116/sec sustained).
- Survives **multi-model adversarial review by at least three unrelated LLM
  models**, including the web-facing surface. (This is the demonstration-project
  adversarial-review mechanism — explicitly *not* a substitute for a professional
  human security audit, and not labelled "audit.")
- **Review recency is attested** (§4.7): the service publishes a signed,
  timestamped record of when it was last adversarially reviewed, and treats
  staleness past a declared threshold as a failing invariant — encoding that
  review is a recurring cycle, not a one-time gate.
- **Account lifecycle complete through sign-up and API-key management**
  (creation, invalidation, usage-log access) — the security-relevant authn/authz
  surface, red-bar tested (forge a key? use a revoked one? escalate via the
  usage log?), not merely features. **Billing/payment is deferred** (a known
  Stripe-shaped, SAQ-A-minimizing integration when paying demand is validated —
  not built for v1).
- **Architected to the PCI standard, not certified to it.** The cardholder-data
  environment is minimized *by design* (tokenize via a compliant processor so
  PCI scope is SAQ-A-shaped, not SAQ-D), evidencing segmentation, key-management,
  and access-control judgment. Designing to the bar is the demonstration;
  obtaining the certificate is deferred product work.
- The scaling question — *if promoted for AI-agent use (e.g. openclaw,
  hermes-agent), could it scale to handle success?* — is answered by
  **architecture + load evidence** (a design-and-load-test claim, not a
  production-traffic claim).

**Kill criterion (further work is vanity):** the v1 done-line above is green and
the scale-to-success path is demonstrated *on paper*. Past that point — tuning
for traffic that does not yet exist, polishing UI, chasing scale that has not
been sold — is vanity. Stop and ship the demonstration.

---

## 6. Method & division of labor (the meta-claim)

The stance is contest-then-adopt: the prior design spec (a previous AI's work,
in `docs/tessera-cloud-demo-spec.md`) is coherent and useful, but it is *not*
ratified. Architecture decisions are re-derived or contested in the human
author's voice; the disagreements are part of the credibility evidence, because
a design merely executed from an AI's spec would demonstrate the deskilling
failure mode, not the healthy one. AI accelerates mechanics; the judgment is
the author's.

**Disagreements with the prior spec, on the record:**

1. **The prior spec's KMS-only signing fork (B) concentrates the trust story in
   one operational domain.** KMS is technically capable (it signs Ed25519 and
   even post-quantum ML-DSA, with offline-verifiable public keys) — so the
   disagreement is *not* that KMS is incapable, as an earlier draft wrongly
   implied. It is that resting a long-lived attestation solely on KMS ties its
   verifiability to a single domain's account lifecycle, key-deletion policy,
   IAM, and public-key provenance (§3.1). Rejected in favor of dual-signing (C)
   across independent failure domains, with DNS/repo/bundle key publication and
   a bundled issuer-key manifest. This was the load-bearing architectural
   disagreement.

2. **The prior spec under-specified supersession.** It had no model for adding
   assurance (e.g. post-quantum) to existing attestations. The wrap-don't-
   replace model (§3.1) — which also dissolves the canonicalization-freeze into
   per-layer versioning — is a Tessera addition, not the spec's.

3. **The prior spec treated the cloud-independent core and the LocalStack slice
   as one phase.** They are separated here into bands (§2): the cryptographic
   guarantees are frozen on a laptop *before* any LocalStack work, so the
   cloud-shaped layers cannot silently regress the invariant.

4. **The prior spec assumed the central guarantee, never demanded it be
   proven.** It described an attestation service as if "tamper-evident,
   cryptographically secure" were established by construction. It is not. The
   guarantee that altering a signed package requires solving a hard problem is
   an *unproven claim* until a machine-checked formal model and proof exist
   (H0 / Band 0). Treating that as a gating precondition — building nothing
   until the foundation is proven — is the largest divergence from the prior
   spec, and the one most central to the difference between a commercial
   offering and theater. Formal verification is itself a capability the project
   demonstrates (§7).

(Further disagreements are expected as the build proceeds; the journal records
them as they arise.)

*Right-sizing note (carried from the prior spec, and true): the documentation
layer is a dated markdown journal, not an attestation system. The cleverness
goes in the service, not the log.*

---

## 7. Capability-map rows targeted (the CV mechanics)

The gap profile is coherent, not a random scatter, and it *is* the CV thesis
made concrete: **I have the infrastructure primitives but not the operational,
security-posture, and observability envelope around them.** I have built the
components services are made of; the market wants people who can *operate*
services. Tessera closes exactly that envelope. Stated honestly in three bands:

**Direct gaps being closed (the point of the project — the "operate it" layer,
mostly the SRE / security-engineering cluster, hard to fake and hard to learn
from docs alone):**
- ECS / Fargate
- KMS (key custody)
- CloudTrail (audit)
- GuardDuty / Security Hub (threat detection / posture)
- S3 Object Lock (WORM / immutability)
- OpenTelemetry / Prometheus / Grafana (observability)
- SLOs / error budgets / load testing / graceful degradation
- CDK / Terraform IaC
- FinOps / cost governance

**Reinforced (already have hands-on; this project evidences depth, not novelty):**
Lambda, SQS, DynamoDB, EC2, EBS, S3 (basic — *not* Object Lock), and security
architecture generally.

**Acknowledged stretch (a real edge of competence, named rather than hidden):**
web-facing systems. I do not typically build public-facing web surfaces; the
API gateway and (v1) web surface are a deliberate stretch, not a strength I am
claiming. Declaring this edge is itself the point — the same "declare what you
cannot see" ethos the attestation service embodies, applied to my own CV. A
reviewer should trust the strong claims *more* because the weak edge is stated.

---

## 8. The gate — this project does not begin until these are true

A pre-registration is only honest if it can name the condition under which the
project *does not proceed*. Tessera has one, and it is non-negotiable:

**Band 0 (H0) must be resolved before Phase 1 begins.** Concretely:
- a machine-checked formal model (TLA+ and/or Lean4) of the attestation
  construction and its claimed invariants exists, and the proof — resting on
  cited external hardness assumptions, proving *our own composition* — holds;
- the agreement gate has passed (author and AI each independently judge the
  model faithful to the claim);
- the informal written proof (the author's defend-it-cold account) is in the
  repository.

The gate is **machine-checked**, by design. Independent *human* formal-methods
review is *not* a resolution requirement under the no-spend constraint (H3) — it
is an optional enhancement gated on a revenue stream, and its absence is a
declared residual risk (no review, machine or human, guarantees a future party
won't find a hole). This keeps the bar rigorous *and* achievable in our control,
rather than set where it can never be met.

Only then does **Phase 1a** begin (implementing the cloud-independent crypto
core), marked by an explicit, dated, signed commit declaring the build runway
open. The 7-day H1b window opens later, at the H1a freeze commit (§2).

**If H0 cannot be met, the project does not proceed as designed — and that is a
valid, honest outcome of this pre-registration, not a failure to conceal.** A
highlight reel cannot say "we stopped because the foundation did not hold." A
real pre-registration can, and that is precisely where its credibility comes
from. The central guarantee of an attestation service is not something to
assert and build around; it is something to prove, or to honestly report we
could not. Building on an unproven foundation would be theater — the one
outcome this project exists to refute.
