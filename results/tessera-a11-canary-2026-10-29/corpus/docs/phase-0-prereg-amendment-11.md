# Tessera — Phase 0 Pre-Registration, Amendment 11 — P3's verification profile as a floor and a duty; dependency sweeps; the slot-2 boundary and the spike keys (DRAFT, 2026-10-28)

> **Status: DRAFT by the owner instance (Claude Opus 5.5), revised after the Codex non-author review
> (`docs/reviews/amendment-11/CODEX-REVIEW.md`, A11-01 to A11-07; `DISPOSITION.md`). Not signed.** The author's
> first commit containing the final text is its signing act. Layered on the original and Amendments 1–10, none of
> which is edited. Every registered sentence this amendment changes is listed in §A11.3.
>
> **Outcomes informed this amendment** (the original's amendment rule). Each change is disclosed separately.
> - **§A11.2, P3.** The P3 evidence (`formal/p3-verification-profile/`) was built and reviewed before this text.
>   Building it exposed the stale checklist. No P3 result failed and is relabelled here. The floor's shape is the
>   author's proposal of 2026-10-28.
> - **§A11.5 item 2, the slot-2 boundary.** This is a **retrospective relaxation** of a deadline-qualified
>   restriction. It is proposed after the 21 Oct deadline, and after the candidate code (`service/signer-gcp/`) was
>   written and reviewed.
> - **§A11.5 item 5, K-R's enforcement.** The owner's placement decision (2026-10-27) moved KMS signing from the
>   issuer role to a dedicated policy signer and said it changed no registered sentence. It changed the
>   supplement's description of who computes μ and who may sign. The confirmation review found this.
> - **§A11.5 item 3, the spike keys.** The owner's deployment draft had contradicted a registered commitment. That
>   draft is withdrawn, and this amendment changes nothing in the commitment.

## A11.1 What went wrong

P3's assumption half (A1 §P3, `phase-0-prereg-amendment-1.md:144-148`) requires the verification profile to record
the *exact library and version, accepted signature encodings, public-key validation behavior, low-order-point
handling, cofactor equation variant, and negative test vectors for each*. Two of those fields name concepts of
Ed25519-style curves, which A1 used as its example (`:136`). V1 later registered OpenPGP P-256 and then, on
2026-10-16, the hybrid ML-DSA-65 + P-256 (`formal/p8/HYBRID-REGISTRATION-RECORD.md`). Neither registration re-read the
checklist.

For ML-DSA, the two curve fields have no referent. The other four fields still apply in full. So the checklist
names nothing specific to ML-DSA's own verification pitfalls: it **demands too little**. Nothing had been accepted
on it. The assumption half was open (`formal/PROPERTIES.md:37`) and due after the freeze
(`formal/freeze-v1/FREEZE-RECORD.md:81`).

The method's defect: **a registered decision can change what an earlier registered sentence refers to, and nothing
requires anyone to re-read that sentence.** §A11.4 adds that duty.

## A11.2 P3's verification profile: floor and duty

**The proofs are unchanged.** P3's model half assumes a verifier with stated behaviour. The assumption half is
bounded implementation evidence that the shipped verifier has that behaviour. It does not show that every model
assumption is preserved in general.

1. **Fields kept.** All six of A1's fields stay. For each algorithm in the governing specification they are read as
   follows:

   | A1 field | ECDSA P-256 (rule O) | ML-DSA-65 (rule R) |
   |---|---|---|
   | exact library and version | `cryptography` and its bundled OpenSSL, identified by wheel tag and native-library SHA-256 | same |
   | accepted signature encodings | OpenPGP v4 packet; MPI rules; r, s ∈ [1, n−1]; rule-O policy | exact 3309 bytes; strict hint and z encoding |
   | public-key validation | exact uncompressed point; coordinates < p; on the curve; checked before the library | exact SPKI; no algebraic validation exists |
   | low-order-point handling | cofactor 1: infinity rejected as a key and as the equation's result; invalid-curve points rejected | no referent. Replaced by: degenerate-key behaviour recorded |
   | cofactor equation variant | cofactor 1: a single variant; x(R) reduced mod n | no referent. Replaced by: the FIPS 204 interface (pure, empty context), with every other interface rejected |
   | negative vectors for each | owner vectors plus Wycheproof | owner vectors plus Wycheproof |

2. **Floor (registered).** The evidence is the files listed in
   `formal/p3-verification-profile/FLOOR-MANIFEST.sha256`, whose SHA-256 is fixed at signing. At this draft it is
   `a69204e9f69a2af3a0bcac96991b55109b0ff0f3efdd6e2182424dd347a24a88`, covering 15 files. They hold:
   - the owner vectors: 223 tests, mutation-sensitive (PROFILE.md §6);
   - Wycheproof commit `d17cc89fa5c8f4f4d378b5385ebf75da5d0926c9`, three files pinned by SHA-256: 968 tests.
     - **ML-DSA-65** runs end to end through the verifier. Two disagreements, tcId 3 and 4, are V1 policy (empty
       context only).
     - **ECDSA P-256** runs through the verifier's key validation, MPI rules, range policy and verification, with
       the digest substituted. 219 non-strict DER cases are tested at library level only. 21 P1363 strings of the
       wrong length reach neither interface. There are no disagreements.
3. **Discharge.** Adopting this floor is not discharging P3. P3's assumption half is discharged only when:
   - (a) the manifest verifies;
   - (b) every test in it passes;
   - (c) the deployed verifier package's identity has been checked against F1 (`test_deployed_zip_identity`, run
     with the deployed zip);
   - (d) no disagreement or finding affecting a required behaviour is unresolved. A recorded defect blocks
     discharge until it is fixed and re-tested.
4. **Operational duty (not a registered result).** The floor's checks, and the latest published vectors for each
   algorithm in use, are re-run on every verifier release, on every change to the signature library's version or
   build, on every new upstream vector commit, and at least quarterly. Each run is recorded with its date, inputs and
   outcome, and attested by the operator.
5. **What a later finding changes.**
   - **A security-policy finding** (an algorithm, parameter or key later judged weak) never rewrites a V1 verdict.
     It reaches relying parties as a historical-security result, beside the verdict and its stable fields
     (A9.4, `phase-0-prereg-amendment-9.md:267-283`).
   - **An implementation-conformance defect** (the verifier disagrees with the governing specification, for example
     by accepting a malformed or prohibited case the specification rejects, A9:278) is not preserved as V1
     behaviour. It is fixed in a signed release, which names the affected releases and says what changed. A silent
     change to the verifier is never permitted.

## A11.3 Registered sentences changed

| Source | Was | Now |
|---|---|---|
| `phase-0-prereg-amendment-1.md:144-148` | the six fields, the two curve fields named in Ed25519's terms | the six fields as read in §A11.2 item 1; the floor and discharge conditions of items 2–3 |
| `phase-0-prereg-amendment-10.md:675` | "as amended by rows 15 and 25" | "as amended by row 15" (row 25 cut, E9 row 2) |
| `phase-0-prereg-amendment-9.md:386-392`; `270ca49:docs/V1-PROFILE.md:1023-1037` | the boundary as the selected, deadline-qualified implementation, described through `prototype/policy-signer/` | *only if the author adopts §A11.5 item 2:* a named replacement under conditions (i)–(iv) |
| `formal/p8/HYBRID-SUPPLEMENT.md:151-152, :173-174, :533` (K-R) | `μ` "computed by the issuer"; "`kms:Sign` only for the issuer role" | `μ` computed by the KMS-slot policy signer (`service/signer-kms/`) from an `F` it has validated; `kms:Sign` only for that signer's role, with the issuer roles holding no KMS permission |
| `270ca49:docs/V1-PROFILE.md` custody record, "HYBRID-SUPPLEMENT §9 item 6" | a stale locator | `formal/p8/HYBRID-SUPPLEMENT.md` §11 item 6, lines 524-526. The frozen bytes are unchanged; this corrects the locator only |

## A11.4 Dependency duty for registered decisions

When a registered decision changes a parameter (an algorithm, a custody form, a channel, a horizon, a scope, a key),
the owner sweeps the registered texts for sentences whose referent the change alters. Each one is recorded as
amended, superseded, still fitting or open, before the decision's change is treated as complete. An owner decision
that touches a registered parameter is checked against those texts before it is recorded.

## A11.5 Results of the first sweep (2026-10-28)

The sweep covered the original, Amendments 1–10, the freeze, the tracker and the author-rulings files
(`docs/reviews/stale-dependencies/SWEEP-2026-10-28.md`). The owner checked each finding against its source. The
review added item 3.

1. **H3 (`phase-0-prereg.md:232-248`): not amended.** H3 is a hypothesis with a stated falsifier. Its examples are
   AWS-based, but they do not restrict it to AWS. It is measured over the whole deployed system, every provider
   included. A measurement protocol is recorded before measurement. It covers retained resources (including the
   compliance-locked trail bucket), defines the demonstration and idle periods, and reports the three numbers
   separately. A slot-2 signer and an issuer poller that run through the operating window conflict with "idle
   compute exactly $0". If that or another number fails, H3 is reported as falsified. The operating window is not
   redefined as a demonstration to avoid this.
2. **The slot-2 enforcement boundary: for the author's ruling.** A9.6 requires the final custody implementation to
   be deadline-qualified (`phase-0-prereg-amendment-9.md:389-392`). The frozen record keeps "the selected,
   deadline-qualified custody implementation" (`270ca49:docs/V1-PROFILE.md:1023-1026`) and describes it through
   `prototype/policy-signer/`, which met the deadline on 2026-10-14. That qualification stands as historical
   evidence. It does not qualify a replacement. The E9 ruling R5b (`docs/reviews/e9-packet/AUTHOR-RULINGS.md:54`,
   packet row 5b) allows porting instrument code with evidence earned on the resulting bytes. But it does not
   address A9.6's deadline-qualified custody, so it does not settle this question. Keeping the hybrid **with the
   replacement signer** depends on this ruling. Keeping it with the prototype does not.
   **Proposed:** `service/signer-gcp/` may replace the prototype, provided that before the first shipped receipt:
   - (i) it preserves **every A9.6 custody and policy requirement**: complete-frame validation; the declared-time
     check on its own clock before signing; the issuing account able to enqueue but not to invoke the key, change
     the policy or clock, or obtain key-use credentials; and the key dedicated to V1 type-0x00 documents. It also
     preserves every property in the frozen record;
   - (ii) the external custody record names the deployed implementation, its image digest and its configuration;
   - (iii) deployed evidence is earned on the new bytes. That means: a deployed positive signature that verifies
     offline; deployed refusals for a malformed frame, a wrong tag, a wrong alg, a wrong fingerprint and a declared
     time outside ε; a review of every principal that can cause a signature or administer the signer
     (`service/issuer/DEPLOY.md` step 8); and verified retirement of every other signing path (step 7);
   - (iv) all of it identifies the tested image and configuration.

   **Without this ruling**, production uses the deadline-qualified prototype signer. Slot 2 then has no signer-side
   signing stop or `sign_by` (`prototype/policy-signer/signer/main.py`), and frames travel inline in SQS messages,
   which cannot carry the 1 MiB client limit (IS-09, `docs/reviews/issuer/CODEX-REVIEW.md:35`). That limit is an
   owner operational resolution, stamped but not registered (`docs/V1-SERVICE-RESOLUTIONS.md:20`). It would be
   narrowed.
3. **The spike keys (`formal/p8/HYBRID-SUPPLEMENT.md` §11 item 6, lines 524-526): unchanged.** "Both spike keys
   are deleted after the re-capture verifies, once the review clears." The owner's deployment draft
   (2026-10-27) reused them as production keys. That contradicted this commitment, and the draft is withdrawn.
   Production uses new keys (`service/issuer/DEPLOY.md`), recorded in the external custody record before use.
4. **A dangling cross-reference (`phase-0-prereg-amendment-10.md:675`).** Row 25 was cut (E9 row 2,
   2026-10-23; profile §5). This is a CLARIFY: the fallback cites row 15 only.
5. **K-R's enforcement (`formal/p8/HYBRID-SUPPLEMENT.md:148-172, :533`): amended in wording, the assumption
   unchanged.** (K-R) itself stands: the ML-DSA-65 key signs only V1 tagged strings, in pure mode with the empty
   context, under EXTERNAL_MU, for no other protocol. What changes is who enforces it. The supplement names the
   issuer as the computer of `μ` and the issuer role as the only `kms:Sign` principal. In V1 as designed (deployment pending), a
   dedicated policy signer validates the complete frame (tag, alg, key fingerprint, ε, `sign_by`, the signing stop)
   *before* computing `μ`, and its role is the only `kms:Sign` principal (`service/signer-kms/`; key policy in
   `service/signer-kms/infra/main.tf`). This narrows what a captured issuer role alone can get signed. It does not
   change the supplement's stated limit: "whoever may call `kms:Sign` on the key can sign any message by computing
   `μ`". An administrator of the account can still grant that (`PutKeyPolicy`), which is C3.
