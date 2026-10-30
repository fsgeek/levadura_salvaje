# Tessera — Phase 0 Pre-Registration, Amendment 9 — V1: the claim, the profile, the re-scoped gate, and the obligations carried forward (2026-10-12)

> **Status: PROPOSED. This document is the instrument and is not yet signed. The author's first commit containing
> this file is its signing act** (the house form since Amendment 5). Drafted 2026-10-12 by the AI collaborator
> (Claude, Opus 5.5, owner instance) from `docs/V1-SCHEDULE.md`, `docs/V1-DERIVATION-DRAFT.md` (§1, §3, §4, §6),
> `docs/reviews/anchor-signatures/` (CODEX-REVIEW.md, DISPOSITION.md), `formal/p8/ENCODING-V1.md` and
> `prototype/spike/SPIKE-REPORT.md`. Revised 2026-10-12 after the Codex and skeptic reviews of this draft, applying
> the owner's dispositions in `docs/reviews/amendment-9/DISPOSITION.md`. Revised again 2026-10-13 by the owner (A9.4 verdict stability;
> A9.5 root-KSK reliance periods, append-only trust configuration, git object format; A9.6 slot-2 custody and its
> policy signer, sequential rotation), from `docs/reviews/a9-custody/`, `docs/reviews/v1-profile/` and
> `docs/V1-V2-COMPATIBILITY.md`; the pre-revision text is kept in `docs/reviews/a9-final-delta/`.
> Layered on the original and Amendments 1–8.
> Per amend-don't-rewrite, none of them is edited: every registered sentence this amendment changes is listed in
> §A9.7 with its source line and its replacement, and is left standing in its file.

**Provenance labels.** Every load-bearing statement carries one:
- **AUTHOR DECISION** — the author ruled, or adopted a recommendation, in his own quoted words, dated. Equivalent to
  RULED/ADOPTED (author) in `formal/spike/first-link/DECISION.md`.
- **OWNER DECISION** — taken by the owner instance (Claude Opus 5.5) under the project ownership the author assigned
  on 2026-10-12. It is not an author ruling. Where an author statement prompted it, his words are quoted as the
  prompt, not as the ruling.
- **RECOMMENDED** — drafted, not decided by anyone.

Nothing here binds until the author signs. **What the signature means for OWNER items:** the author has read them
and does not object. It does not convert them into author rulings. The only items the signature ratifies as his
are the five parameters A9.2 puts to him (δ, ε, k, N, S).

---

## What this amendment establishes

**The claim.** V1 is a dual-signed timestamp notary for Tessera's own domain, `wamason.com`. Provided the service's
signing capability was not misused within the key's window, a V1 receipt lets anyone, with no network and no help
from Tessera, check four things: that particular bytes were presented to the Tessera V1 service; that both of the
service's keys signed them; that two channels (DNSSEC, and a signed, timestamped git commit) said those keys
belonged to that domain and were allowed to issue during a stated window; and that the bytes *and both signatures*
existed no later than a time T fixed by Bitcoin. Against the window, the declared issue time is not earlier than
its not-before, and the verified chain-time T is not later than its not-after.

**The adversary.** Anyone who tampers with, forges, strips, swaps, replays, reattributes or backdates receipts;
anyone who captures authority-channel credentials while signing capability stays uncompromised (A8.3's sense of
capture); and anyone who steals a key, gains signing capability, or breaks a signature algorithm *after* a receipt
was anchored. Against these, V1's verdicts hold under the registered cryptographic, key-use and chain assumptions.

**The boundaries.** V1 does not say who submitted the bytes or what they mean. It does not evaluate revocation, or
whether an algorithm or key was still safe when it signed. It offers no standing, renewal, wrappers or degraded
verification, and no lower time bound or priority. It does not hold against an adversary who holds signing
capability for every required slot inside the window (capture of the issuing AWS account confers it for both
slots, C3); against whole-author-sphere capture (R-2.15); or against breaks of SHA-256, OpenTimestamps, Bitcoin
history deeper than k, or, in git's links, a second-preimage break of SHA-1 or attacker influence over committed
contents; or against compromise of the verifier's distribution, meaning its release and the trust configuration
compiled into it (an explicit external assumption, A9.5). Both keys are under one controller.

---

## A9.0 The decisions this amendment implements

**AUTHOR DECISIONS, 2026-10-10** (one message, quoted in full for A–C; checked against the session record,
2026-10-10T15:43Z: the "Decision A/B/C:" prefixes are his, and the rest of the message is his Q1 question):
- **A, the V1 promise.** *"Decision A: I accept your recommendation."* The non-promises come with it: submitter
  identity, standing (reported `ABSENT`), wrappers and renewal, degraded verification, and revocation (B).
- **B, revocation.** *"Decision B: (i) seems to be the only honest answer; (ii) can be added as an additional
  service without promising anything more."* Revocation is not evaluated (A9.4). An anchored "no revocation as of
  ship time" statement is an optional add-on service, outside V1's promise.
- **C, the 4 Dec acceptance bar.** *"Decision C: I accept your recommendation."* Zero unsafe accepts; false rejects
  only on the two named honest cases V1 does not support (d2, h); a human tester (A9.1: n = 1, "Aki Doe").

**AUTHOR DECISION, 2026-10-09 (Q5).** D is `wamason.com`, as a demonstration: *"I do control wamason.com, so it's a
perfectly reasonable choice for now."*

**OWNER DECISION, 2026-10-12 (Q1): adopt this amendment as the instrument.** The author returned the ruling: *"The
decision to change that rule isn't mine, it is the owner of the project."* Formal-first stays, tied to V1's finite
claim set rather than the whole design. The throwaway prototype and the spike showed that code built as an
instrument sharpens the model without anchoring it. A9.2 therefore replaces "Before any code".

**OWNER DECISIONS, 2026-10-12, from the anchor-signature review and its follow-ups:** the signature-inclusive
receipt anchor and the sign–freeze–stamp order (A9.5); `historical_security: NOT_EVALUATED` (A9.4); the git stamp
targets the signed commit id (A9.5); the existential root-KSK rule (A9.5); the single issuance window and its
issuer invariant, the hybrid signer profile with its fallback, the `gpg`-slot declared-time check, the C3 non-claim
and the two conditional product guarantees (A9.6); the cut order (A9.2).

**OWNER DECISIONS, 2026-10-12, from the reviews of this draft** (`docs/reviews/amendment-9/DISPOSITION.md`): all
nine Codex findings and Skeptic findings 1–3, 5–23 are applied as disposed there; Skeptic finding 4 (cut the hybrid)
is rejected, and its cut order is adopted.

**Superseded owner statements from earlier on 2026-10-12:** 30-day overlapping windows; the 48 h and then 96 h
retirement margin as a registered parameter; the exit procedure in the instrument. Operating numbers and the exit
procedure now live in `docs/V1-OPERATIONS-RUNBOOK.md` (DRAFT, not registered).

**Owner corrections prompted by the author, 2026-10-12:**
- *Contracts in content.* The author: *"it does not enforce that identity has been validated, but it does not
  prohibit including evidence of identity either. If having two digital signatures over a contract that is
  included in the attested bundle isn't sufficient, then I think we're done - because Tessera isn't in the
  business of verifying identity."* The owner's earlier statement that V1 cannot serve such contracts is withdrawn.
  Scenario cases i and i′ are added (A9.1).
- *Key protection.* The author: *"our implementation needs to carefully protect the keys, such as using a hardware
  key, TPM, or enclave style KMS."* Implemented by A9.6; the hardware specifics are in the operations runbook.
- *Key lifetimes.* The author: *"these become product side questions and guarantees. One way to protect keys is to
  limit their lifetime. That doesn't prevent compromise, but it does mitigate the potential damage."* The single
  window of at most 90 days (A9.6) is an owner decision implementing this.
- *Signer preference.* The author: *"I think we should build our V1 with a PQ implementation"* (2026-10-12). The
  conditional hybrid (A9.6) records this as his stated preference, not as a claim requirement.

**Earlier owner decisions carried in, not routed:** P8's method; standing omitted; the header-pin rule; the DNSSEC
snapshot rule; E18 read as k = 6 under `DepthK = k − 1` (`formal/PROPERTIES.md:177`); the V1 build as the second
encoder.

---

## A9.1 V1's success definition, claim, profile and scenario mapping — OWNER DECISION (Q1), implementing A and C

**Success definition** (`docs/V1-SCHEDULE.md`, adopted here). V1 succeeds when:
1. An organisation can obtain a receipt, at a stated cost and latency, asserting that *these exact bytes were
   presented, signed by key K whose authority is evidenced by named channels, no later than time T*.
2. A relying party can verify that claim without Tessera running and without the authors' help. From V1's
   documentation alone, it reaches the safe decision on every case of the registered mapping below, including the
   cases whose answer is "not established": **zero unsafe accepts; false rejects only on d2 and h** (AUTHOR
   DECISION C; this replaces V1-SCHEDULE's "the prototype's scenario set"). *Evidence:* one human tester (n = 1,
   recorded under the pseudonym "Aki Doe") who meets the independence criteria of `docs/V1-TESTER-BRIEF.md`: a CS
   background; no knowledge of attestation, timestamping, blockchains or this project; has not discussed Tessera
   with the author; and no help from the project during the test. The evidence is stated as one tester's result,
   not as a result about relying parties in general.
3. V1 ships by 4 December 2026, or the project stops pursuing V1 by explicit decision at that point.

Milestones (ceilings, accepted by the author 2026-10-09: *"I'll accept those dates"*): 16 Oct, 30 Oct, 20 Nov,
4 Dec, with V1-SCHEDULE's slip rule.

**Claim.** *Conditional on the registered cryptographic and key-use assumptions, a V1 receipt lets anyone holding it
establish, without Tessera, that the attested content was presented to the Tessera V1 service, whose own domain is
D; that each of the service's two keys K = {K_kms, K_gpg} signed its own frame binding that content; that two named
channels authenticated these keys for D, with an issuance window the git channel committed, in chain order, before
the receipt's anchor, at the stated evidence times; that
the signed frames and their exact signatures existed no later than T; and that the declared issue time is not
earlier than the window's not-before and the verified chain-time T is not later than its not-after. Effective
revocation and historical algorithm and key safety are not evaluated, and the receipt attests neither the
submitter nor the content's meaning. The verdict is typed and says what was not established.*

| # | Sub-claim | Non-claim kept beside it |
|---|---|---|
| C1 Bytes | The verifier reconstructs each signer's exact frame; both bind the same content and common metadata, the designated fingerprint in its slot. The receipt-anchor preimage `A_sig` over both frames and both signatures is unambiguous. | Nothing about meaning or truth. Payload identity is not frame equality. |
| C2 Presentation | The content was presented at some issuance event of the V1 service (existential). | Not who submitted it; not whether a replay suits the transaction. |
| C3 Signature | Each required signature verifies over its designated frame; a missing, stripped or substituted one fails. | **The two keys are separate technical failure domains under a single controller; V1 claims no separation of control and no independent fates**, and no independent approval of content. The `gpg` signer signs frames delivered by the AWS-side issuer, so capture of the issuing account confers signing capability for both slots; the non-exportable key prevents key export, not misuse. |
| C4 Authority | DNSSEC (owner name D, evaluated at the snapshot's own anchored time) and the anchored git key assertion (full commit→tree→blob path) authenticated K for D, with the issuance window, at their evidence times. **Chain-order pre-commitment** (OWNER DECISION 2026-10-14, BROADEN; `docs/reviews/spec-sufficiency/` F01): the git assertion's selected anchor height plus 5 is lower than the receipt's selected anchor height, so the window was confirmed at k = 6 in the chain before the receipt was anchored. The verifier fixes the required set. | Revocation not evaluated. Not public publication of the commit. Neither channel commits to any receipt (CODEX-REVIEW 3). Pre-commitment is chain order, not UTC (A2.1); DNSSEC evidence establishes no publication before issue. |
| C5 Time | The frames **and their exact signatures** existed no later than T, the verified attestation at the lowest block height in the presented OTS proof (both T and its confirmations come from that attestation; OWNER DECISION 2026-10-14, F03: header times are not monotone, so "earliest" means chain order); the three-conjunct predicate holds at k = 6. | Presentation-sensitive T. No lower bound, no priority. Header times are chain-time proxies. Reorganization deeper than k is a residual. |
| C6 Without Tessera | The verdict is a pure function of the bundle, the published verifier and its distributed trust configuration. | Custody is the holder's. Dead-project reconstruction not demonstrated. A selected anchor (C5) beyond the newest pin is `UNVERIFIABLE`. Every supplied header must be pinned. An unselected attestation without its headers supplies no fact and is not a failure (OWNER DECISION 2026-10-14, F02). |
| C7 Safe decision | The verdict is typed and reports `revocation: NOT_EVALUATED`, `historical_security: NOT_EVALUATED` and standing separately; a non-expert makes no unsafe accept on the mapping (4 Dec criterion, not yet established). Assigned build evidence includes A9.4's missing-capture negative control. | Revocation, historical security and standing are not claimed. |

**Profile `tessera-v1-strict`** (identifier and spec hash inside the signed bytes):
- *Encoding:* `formal/p8/ENCODING-V1.md` at the signing commit, including D-1 to D-17; number rule A9.8. If the
  hybrid branch is taken, the signing-commit baseline plus the branch-registration supplement (A9.6) governs it.
- *Receipt anchor, issue order, git target, root-KSK rule:* A9.5.
- *Signers, issuance window:* A9.6.
- *Authority:* DNSSEC for D plus the git key assertion, both required, n = 2.
- *Trust configuration* (ships with the verifier, never from the bundle): root KSK-2017 and KSK-2024 with separate
  publication, signing and reliance periods; the repository key; a signed, versioned set of pinned mainnet header hashes.
  A bundle header outside the pins gives `UNVERIFIABLE / HEADERS_NOT_COVERED`. The trust configuration's KSK
  periods are as known at release; snapshots after an unlisted rollover are `UNVERIFIABLE`.
- *Bundle:* spec identifier and hash (signed); spec and conformance vectors (content-addressed); a bound
  plain-language purpose preamble; a dependency manifest (RFC 8785, OpenPGP, the signature algorithms in use,
  SHA-256, SHA-1 for git object linkage, the DNSSEC algorithms in the chain, OTS, Bitcoin headers).
- *Verification:* strict only; one layer; no wrappers, renewal, TLR or waiver policy.
- *Stable field set* (A9.4): the verdict, its reason code, T, `revocation`, `historical_security` and standing.
- *Parameters:* A9.2.
- *Issuance:* an operated API (API Gateway + Lambda + KMS).
- *Issuer invariant:* a receipt ships only when complete; an operator refusal never concerns a shipped receipt.

**Separations.** V1 is a profile and milestone, not the "v1 product" done-line (`phase-0-prereg.md:589-617`),
which stands with the H2 panel and kill criterion. V1 is not the production version. H1b is withdrawn for V1,
not falsified.

**Scenario mapping, registered before any V1 run** (prototype expectations kept as history). Every row: profile
`tessera-v1-strict`, strict request, `revocation: NOT_EVALUATED`, `historical_security: NOT_EVALUATED`, standing
`ABSENT/NOT_ISSUED_IN_PROFILE`.

| Case | Fixture | Expected verdict | Safe decision |
|---|---|---|---|
| a, g | Honest receipt as shipped (a's TLR removed) | `VALID_STRICT` | Accept as: these bytes were presented to Tessera by T |
| b | Reattribution under attacker keys | `INVALID` | Reject |
| c | Two-layer transplant | `UNVERIFIABLE/OUT_OF_PROFILE` | Reject |
| d1 | a's bundle; degraded request, then strict | Waiver refused; strict `VALID_STRICT` | Accept under strict only |
| d2 | a with repo evidence removed | `UNVERIFIABLE` | Reject: **registered false reject** |
| d3 | Clone, TLR removed (one key, one channel) | `INVALID` (A4.2 precedence) | Reject |
| e, e′ | a's bytes; slot-B key revoked inside (declared, anchor], or (e′) before declared | `VALID_STRICT` | Non-revocation **not established**; a transaction needing it must not rely on this receipt alone |
| f | Impostor's content through the honest service | `VALID_STRICT` | The receipt attests no submitter |
| h | Honest renewal wrapper | `UNVERIFIABLE/OUT_OF_PROFILE` | Reject: **registered false reject** |
| i | `content` = a contract plus two valid party signatures, issued honestly | `VALID_STRICT` | Accept as: this signed contract existed by T. The parties' signatures and keys are the relying party's to check |
| i′ | As i, one party signature does not verify | `VALID_STRICT` (Tessera does not read `content`) | Reject the *contract*: the receipt is valid, a party signature fails the relying party's own check |

Rows i and i′ are an owner addition after Decision C; they add no false reject. *Registered prediction:* a
headline-only reader fails e and f; i′ is the same hazard and is in the test. The test measures whether the
documentation prevents that. The E10 vectors test the verifier, not comprehension.

## A9.2 The Band 0 gate, re-scoped to V1's claims — OWNER DECISION (Q1)

- **Code rule: one gate.** *"Before any code"* (`phase-0-prereg.md:102`, author clarification 2026-08-29: code
  intended for the service) is replaced by: **no V1 issuer or verifier code is written before the whole 30 Oct exit
  is recorded.** There is no per-claim gate.
  - *Instrument code* is defined by location: it lives under `prototype/` or `formal/spike*/`, and service code never
    imports it. An instrument's outputs may select among branches registered here (A9.6's signer branch); they
    never stand as evidence for a C-row, and nothing an instrument produces discharges an obligation.
  - The author commits `prototype/spike*` (the spikes that shaped the root-KSK rule and the signer choice), so the
    record holds them.
  - *This is a weakening* (A9.7 row 1, W). P8 rests on a prose proof plus vectors, time-boxed, not on a
    machine-checked proof, and the 30 Oct time box replaces the original's "No time bound".
- **Exit gate, 30 Oct, for `tessera-v1-strict` only:** P1, P2, P3 [model], P4, P5, P5c, P10 and P7's
  type-separation half `checked`; P8 by prose proof plus golden and rejection vectors **for `A_sig`**, surviving a
  time-boxed falsification attempt; P9 as a contract inspection; E6a with companions; the 129 strict correct-form
  rows plus statements M2 and M5; E18 with its time-boxed sign-off; the one-page E8/E7/E11 sheet; the E12 page.
  Added 2026-10-12: the anchored-versus-unanchored-signature negative control; `ISSUANCE_WINDOW` and
  `DNS_WINDOW_LENGTH` vectors; the root-KSK rollover control (A9.5); the signer branch recorded (A9.6).
- **Cut order, registered.** If the 30 Oct exit slips, the first item cut is the PQ hybrid (the registered
  fallback is then taken), and nothing else is on the list: the signature-inclusive anchor `A_sig`, the root-KSK
  rule and the git stamp target (D-16) are required.
- **After exit:** 20 Nov: P3 assumption half, P9 code inspection, E10 vectors run against AWS, bounded local
  refusal, A9.4's missing-capture negative control (C7 evidence), H3 measured. 4 Dec: relying-party test and
  dead-service test. E10 extraction moves to 13 Nov.
- **Not discharged:** the original H0, the full capstone gate, every A9.3 obligation. The exit opens Phase 1a for
  V1-profile code only, still by an explicit, dated, signed opening commit (A9.7 row 2).
- **Closure rule.** Each review is time-boxed and dated. A finding after its review date gates V1 only if it gives
  a concrete counterexample to C1–C7, or shows that one of C1–C7 lacks the evidence assigned to it. A finding
  against guarantee 2 (A9.6) is a C4 finding for this rule. Any other finding goes to the A9.3 register with a
  named capability. The author's E9 read is accept or reject per row.
- **Parameters (E14):** δ = 72 h, ε = 24 h, k = 6, N = 3, S = 24 h. OWNER DECISION, put to the author: his
  signature on this amendment ratifies these five parameters. The closure rule stays an OWNER DECISION (the author
  returned the Q1 ruling to the owner, 2026-10-12).

## A9.3 Obligations carried forward — OWNER DECISION (Q1)

Each stays registered with its original text. Its V1-era trigger becomes "before the named capability is offered",
and only a later profile offers it.

| Obligation | Future capability |
|---|---|
| Submitter attestation, per-organisation issuer | **Attributed receipts** (a non-personal D is a precondition) |
| SC row, A8.4 query, W1 in S-STANDING, O-74, R-6.44, TLR | **Protocol standing** |
| P6 status capture, freshness bound F, DNSSEC status capture, revocation-timing vectors | **Long-term validation (T4)** |
| Forward-link successor slot and its vector | **Service succession** |
| E6b, refusal decomposition and both companions | **Portable refusal records** |
| Lifecycle model, P7 wrapper half, A6.1 vector, O-30, custodial parameter schema, RFC 4998 renewal | **Wrapping and renewal** |
| Case (d) eleven, A8.3 slices, A1 §A1.2.1 waiver lattice, A5.3 record, M6, M7 | **Degraded verification** |
| n-ary channels (O-69) | **Jurisdictional diversity (T3)** |
| PQ on the portable leg (A3 §A3.6) | **Production version** |

**V2 drivers: candidate capabilities, recorded for context.** They create no obligation and need no amendment to
drop. None is promised, scheduled or gating.
1. **Separation of control:** independently evidenced custodians, each holding one share of a threshold (m-of-n)
   signing set, so that no single controller can mint. It is what would retire C3's single-controller non-claim.
2. **Party identity use cases:** receipts whose evidence concerns the identity of the parties in `content`, beyond
   what cases i/i′ give (V1 carries such evidence but never checks it).
3. **Renewal:** as in *Wrapping and renewal* above.
4. **Revocation evaluation:** as in *Long-term validation* above, and the B(ii) add-on service.

## A9.4 Revocation and historical security: not evaluated — AUTHOR DECISION B; OWNER DECISION for historical security. A weakening under A1 §A1.1.

- **Weakened.** For V1 bundles, `VALID_STRICT` evaluates neither P6 condition: `key_authorized(declared_issue_time)`
  against effective revocation, and no revocation effective at or before `max(anchor_time, declared_issue_time)`
  (A4.3). Every report carries `revocation: NOT_EVALUATED` next to the verdict. *Why:* under the registered text
  a verifier that cannot evaluate revocation returns `UNVERIFIABLE` for every receipt.
- **Historical security.** Every report carries `historical_security: NOT_EVALUATED`. V1 does not evaluate whether
  a signing algorithm or key was safe when it signed. The documentation names what a later examiner must supply:
  an authenticated safe-before cutoff per algorithm and per key, compared against T with A2.1's chain-time
  uncertainty (CODEX-REVIEW 8). A surviving PQ attestation slot prevents a P-256 break alone from supplying every
  required attestation signature. An ML-DSA-65 cutoff and the classical slot remain; historical authority, per-key
  custody and continuing commitment and history security remain assumptions. A PQ slot never removes the need for
  a theft cutoff.
- **Issuer duty.** The V1 issuer never re-authorizes a key (R-5.24). V1 defines no revocation publication.
- **Contract for later verifiers.** Missing status capture does not by itself invalidate a V1 receipt. A later
  verifier given a V1 bundle, under the same governing V1 specification, policy, trust configuration and other
  declared inputs, returns the same verdict and values in the stable field set (A9.1), and never a weaker verdict
  because of missing status capture. **Verdict stability** (OWNER DECISION 2026-10-13, `docs/V1-V2-COMPATIBILITY.md`): a V1
  bundle is always evaluated under its signed `common.spec`. Trust configurations are append-only (A9.5), so a
  later configuration cannot turn a V1 verdict into `UNVERIFIABLE` by dropping a KSK, a header pin or a repository
  key. Later algorithm policy enters the separate historical-security assessment only as an authenticated
  per-algorithm cutoff compared with T, with A2.1's chain-time uncertainty; authenticated per-key theft cutoffs are
  assessed separately there as well. It never overwrites the V1 verdict or its six stable fields, whether T is
  before, equal to or after a cutoff. A receipt whose T precedes an algorithm's cutoff keeps its V1 verdict; that
  comparison alone does not establish historical safety. Later revocation, standing, renewal and historical-security
  results are reported separately, together with later adverse evidence. The V1 verdict continues to apply the
  algorithm policy registered for its governing V1 specification, including its original malformed, unsupported and
  prohibited-identifier cases (A9.7 row 29). This
  binds later verifiers and profiles; it is not a property V1 itself demonstrates. **This is not
  non-repudiation.** Evidence (C7): for an otherwise valid, fully performable bundle where missing status capture
  is the sole difference, a companion returning `INVALID` or `UNVERIFIABLE` must go red.

## A9.5 Strict-only, standalone; the receipt anchor — OWNER DECISIONS 2026-10-12 except where marked

- **Dispatch.** Out-of-profile input gives `UNVERIFIABLE / OUT_OF_PROFILE` at dispatch; A4.2 precedence holds inside.
- **H1a's suite.** Forge, tamper, backdate, break-chain, strip-one-signature, out-of-profile, the A9.1 mapping.
  Degradation and wrapper instances move to their capabilities.
- **Receipt anchor.** OTS stamps `SHA256(A_sig)`, tag `tessera-v1/receipt-anchor-sig`, which commits to both frames
  and their exact detached signatures in manifest slot order (ENCODING-V1 §5, D-8, D-14). The verifier verifies the
  committed signature bytes only. The frame-only layout is withdrawn, with no fallback.
- **Issue order (D-15).** Fix manifest and metadata; build frames; sign; verify; **freeze** the signature bytes;
  **stamp** `A_sig` (one stamp per receipt, R-3.42); obtain confirmation; ship. A signature made after T cannot fit
  the anchor. A retry that changes any committed byte needs a fresh stamp. Signature identifiers stay independent
  of signature bytes; the anchor digest may commit to them; nothing is normalized after stamping.
- **Git stamp target (D-16).** The git channel's OTS stamp targets the **signed commit's object id**, never a tree,
  blob or unsigned commit. The verifier recomputes the id, verifies `gpgsig`, follows commit→tree→blob, and checks
  the stamped id. SHA-1 linkage remains a stated residual. The git evidence names its object format, and V1
  accepts only `sha1`: the key-assertion repository stays in SHA-1 format at a host that supports it, whatever
  git's default becomes (the author, 2026-10-13: Git 3 moves to SHA-256 in 2027; GitHub does not support it).
  The pre-freeze bundle schema (V1-PROFILE §2.1, G-26) defines the git-evidence member `object_format` as the string
  `"sha1"`. It is an evidence descriptor, not a new signed-frame or key-publication field. A missing descriptor gives
  `UNVERIFIABLE / GIT_OBJECT_FORMAT_MISSING`; an unsupported value gives `UNVERIFIABLE / GIT_OBJECT_FORMAT`. The
  verifier recomputes the SHA-1 object ids from the raw commit/tree/blob bytes, so this descriptor cannot override
  their interpretation. For V1 the stamped message is exactly 40 lowercase ASCII hex digits naming the signed commit
  id followed by one LF byte. The schema/check specification and conformance cases are fixed before the 30 Oct
  profile freeze; no P8 frame or key-publication vector changes are required.
- **Root-KSK rule.** The root DNSKEY set is valid at the snapshot's anchored time **if some trusted KSK whose reliance
  period contains that time validates it**. Each KSK entry records signing-start, signing-end and a sourced reliance
  lifetime L, with the reliance interval [signing-start, signing-end + L]. L is the registered acceptance-policy
  value derived from the cited root DNSKEY RRSIG validity evidence; a largest observed lifetime is labelled observed,
  not asserted to be a proven global maximum. A candidate must also satisfy cryptographic validation and the selected
  RRSIG's inception/expiration checks at the snapshot's own verified anchored time. This extension permits authentic
  pre-retirement evidence anchored later; it does not establish that signing occurred before retirement. A thief of
  a retired KSK can manufacture eligible root evidence during the extension. Exposure is bounded by the reliance
  endpoint in snapshot chain time, not by a finite UTC duration under A2.1. Historical authority-key safety and the
  continuing anchor/history assumptions remain necessary and are not evaluated by V1. **AUTHOR ADOPTED, 2026-10-13**
  (`docs/reviews/v1-profile/` F2; kind CORRECT: the withdrawn cutoff claimed a protection DNSSEC itself does not
  supply, since resolvers accept a retired KSK's signatures until they expire). The author: *"I'd argue that the
  'narrowing of protection' wasn't a real narrowing, it was us admitting the real level of protection given the
  constraints of the project."* The rule is existential and order-independent: a candidate that fails is
  informational, and the result is computed once, after every eligible key has been tried (F1). A trusted KSK that
  is published but did not sign is informational, never a failure. The trust configuration records signing and
  reliance periods separately from publication and revocation dates.
- **Trust-configuration authority** (OWNER DECISION 2026-10-14, after `docs/reviews/spec-sufficiency/` F04). The
  trust configuration is authenticated independently of the bundle and of both authority-channel credentials. Each
  verifier release compiles in the hash of its configuration. Releases are authenticated by a key that neither the
  DNS credential, the repository key nor the issuing AWS account can use; the dated custody record names that key
  and its access boundary. Capture of an authority-channel credential grants no ability to sign a release,
  authorize a configuration hash, or replace the compiled trust root. CI is not the authenticity check. Compromise
  of the release key is distribution compromise, a stated boundary.
- **Trust configuration is append-only** (OWNER DECISION 2026-10-13). Trust configuration entries are append-only: KSKs, header
  pins and repository keys are never removed, and finalized period endpoints never change. Repository trust entries
  name D, the key and an inclusive signing interval; the git assertion passes this trust check if some configured
  entry for D verifies gpgsig and its interval contains the signed commit's own verified anchored time. Repository
  entries have no KSK-style reliance extension. Unknown material cannot establish this required check. Append-only
  extensions preserve previously usable trust witnesses; newly covered evidence can improve an earlier UNVERIFIABLE
  result. Exact stable-field identity remains the contract for identical declared inputs. Closing an open period must
  not retrospectively exclude evidence previously accepted under that entry; the pre-freeze configuration records the
  endpoint/update convention explicitly. **Rollover control:** a snapshot taken while one trusted KSK is published but not signing must pass
  (SPIKE-REPORT, KSK-2024 re-capture; without it every receipt from 2026-10-11 would be falsely rejected).
- **Custody.** V1 offers no renewal. Long-horizon validity depends on the dependency manifest and on the holder
  keeping the exact bytes (a mirror that alters a signature byte breaks its copy, CODEX-REVIEW 5).

## A9.6 Signers, the issuance window, and what they guarantee — OWNER DECISIONS 2026-10-12

**Signer profile, conditional.** The hybrid records the author's stated preference (2026-10-12: *"I think we
should build our V1 with a PQ implementation"*). It is not a claim requirement: no sentence of C1–C7 needs it. It
is the first item cut if 30 Oct slips (A9.2).
- **If the hybrid spike passes by 21 Oct:** slot `kms` is AWS KMS **ML-DSA-65** (FIPS 204, in KMS's HSMs), raw
  signature per ENCODING-V1 §5.2 rule R; slot `gpg` is **P-256** OpenPGP (rule O), signed by a
  non-exportable, hardware-protected key in a separate technical key-custody domain outside the issuing AWS account
  (*slot-2 custody*, below), pulling from a queue with no inbound path.
  One pair algorithm identifier names both slot schemes (`common.alg` is shared, R-3.12). This adopts for V1 the
  hybrid A3 §A3.6 deferred.
- *Pass condition* (OWNER DECISION 2026-10-12, fixed after an offline pre-spike, `prototype/spike-pq/`, which the
  author commits, and before the KMS spike):
  - the pair identifier is registered with its mode and context;
  - the mixed-format pairing passes R-3.12 and P3's model;
  - a real KMS ML-DSA-65 signature over a V1 frame (external μ above 4 KB) verifies offline in two
    implementations;
  - a real P-256 signature from the `gpg` slot as deployed verifies offline;
  - the full selected byte profile is specified and tested: attestation **and manifest-possession** verification
    for both slots, slot key and fingerprint encodings, key-use assumptions appropriate to each slot (PROOF's
    OpenPGP type-0x00 assumption does not describe the raw ML-DSA slot), and golden and rejection vectors with an
    agreement run for rule R.

  All of it by 21 Oct, or the fallback is taken automatically. The offline pre-spike is feasibility evidence only
  (approximate JCS, no real KMS, a bare SLH-DSA portable slot rather than this pair); it does not satisfy the
  condition.
- **Registered fallback, otherwise:** both slots classical P-256 under P4': KMS-backed OpenPGP P-256, plus the
  `gpg` slot under slot-2 custody. The signature-inclusive anchor and the
  issuance window are retained unchanged.
- **Slot-2 custody (OWNER DECISION 2026-10-13).** The `gpg`-slot key is generated non-exportable in hardware outside
  the issuing AWS account: a token on author-controlled hardware, or an HSM-backed key at a provider other than AWS.
  The owner chooses between them, and records the choice, dated, in the profile before the 30 Oct freeze. The choice
  takes into account measured token throughput and issuance availability, and the author's concern about scalability
  (2026-10-13: *"Scalability is a real, legitimate, concern"*). Either choice satisfies the author's key-protection
  requirement (A9.0) and leaves C1–C7 unchanged. The key's authority is evidenced by the key-publication record in
  both cases.
  - *Policy signer.* In either custody option, a queue-pulling policy signer outside the issuing AWS account
    validates the complete V1 frame and enforces the declared-time check using its own clock before requesting a
    signature. The issuing AWS account can enqueue frames but cannot invoke the slot-2 key directly, change that
    policy or clock, or obtain the policy signer's key-use credentials. The slot-2 key is dedicated to V1 tagged
    type-0x00 documents (attestation and manifest-possession). The dated custody record names this enforcement
    boundary and its access policy. Non-exportability protects against key export, not signing misuse through the
    permitted queue path.
  - *Deadline.* For the hybrid, the final custody implementation must have completed the deployed-slot
    pass-condition evidence by 21 Oct. The owner may defer selection until before 30 Oct only among custody
    implementations that each met that deadline; otherwise the registered fallback is taken. A custody selection
    changes neither rule O nor any claim, pass condition or exit obligation.
  - *Limit.* Separate technical custody does not imply independent availability, independent signing fates,
    separate control or independent approval of content; C3 applies to both options.
- **Branch registration.** If the hybrid branch is taken, the owner registers, before the 30 Oct freeze, a dated
  **branch-registration supplement** bounded to the pair identifier with its mode and context, the ENCODING-V1 §5.2
  edit for rule R, and the completed pass-condition evidence, naming the exact ENCODING-V1 and specification
  hashes. The signing-commit baseline plus that supplement governs the hybrid branch. This amendment authorizes
  that supplement and nothing else in it; it needs no further amendment and no further author approval. Either
  way, the owner records the branch taken, dated, in ENCODING-V1 §5.2 and the profile before the freeze.
- **Declared-time check (issuer side, not a verifier rule).** The `gpg`-slot signer refuses a frame whose
  `declared_issue_time` is outside ε (A9.2) of its own clock. Whoever controls the queue (an AWS takeover) still
  has signing capability for both slots; the check limits that to minting at the current time. For an HSM-backed key,
  this refusal is enforced by the policy signer, not by the HSM's generic signing API. Separation of control stays a
  V2 driver (A9.3).

**Issuance window.** The key-publication record carries `issuance-not-before` and `issuance-not-after`, **both
mandatory**, identical in DNS and the git blob (ENCODING-V1 §7, §7.1, D-17).
- **Registered invariant: `issuance-not-after − issuance-not-before ≤ 90 days`** (a record that violates it is
  rejected, `DNS_WINDOW_LENGTH`). This amendment registers the first issuance window only; it does not yet
  authorize successor issuance. A future sequential-replacement registration may retain the frozen V1 byte/check
  profile: the same DNS owner and git path, new keys, and a new window with next.not-before > previous.not-after (both
  endpoints are inclusive). Each receipt carries its own historical snapshot and commit. Multiple TXT records at the
  required owner fail `DNS_RRSET`; a substituted per-key owner name fails `DNS_OWNER`. The V1 verifier checks each
  receipt's window, not non-overlap between receipts. Before successor issuance, the owner records a dated rotation
  registration naming the two-window positive/negative vectors and the model, checked property and result
  establishing the intended issuance invariant. This future rotation evidence is not added to the 30 Oct
  first-window gate. Without that registration, issuance stops at the first window's end.
- **Verifier rule (C4).** A receipt is `INVALID / ISSUANCE_WINDOW` unless the declared issue time is not earlier
  than not-before and the verified chain-time T is not later than not-after, with T as registered and no margin.
  T itself is not compared with not-before.
- **Issuer invariant.** An attempt whose T would exceed not-after is not shipped. The stop margin, the window's
  actual dates and the rotation plan are operating numbers, not registered (`docs/V1-OPERATIONS-RUNBOOK.md`).
- A published window cannot be shortened; detection changes no V1 verdict.
- The relying-party documentation states: `ISSUANCE_WINDOW` can result from presenting a later proof; ask the
  holder for the issuer's original proof.

**Exit.** The exit procedure is not part of this instrument; it is in the operations runbook. No V1 verifier rule
consults any end-of-issuance statement (OWNER DECISION 2026-10-12).

**The two product guarantees, stated conditionally (CODEX-REVIEW 7).** Guarantee 2 is the C4 window rule, stated
as a property; a finding against it is a C4 finding for the closure rule (A9.2). Guarantee 1 is not computed.
1. **Past receipts survive later compromise.** A receipt whose exact signatures are anchored by T cannot have
   signatures manufactured after an adversary gains signing capability for every required slot substituted into
   it, while SHA-256, the OTS commitment and the pinned chain history stay secure. Its historical authenticity also
   needs the signing and key-use assumptions to have held before T, authentic historical authority, and no relevant
   compromise before T; V1 does not evaluate these (`historical_security: NOT_EVALUATED`). A later key theft or
   algorithm break does not by itself invalidate such a receipt. It does not cure earlier theft, unauthorized
   signing before T, misissuance or whole-author-sphere capture, and does not prove that the issuer itself obtained
   the stamp or issued the bundle uniquely.
2. **Signing capability mints only inside the window, in chain time.** Even signing capability for every required
   slot cannot make a receipt pass V1 with verified T after its authenticated not-after, under continuing anchor
   and history assumptions and provided the authority channels are not also captured (republishing a window is a
   new authority event; whole capture is R-2.15). Translating this into a finite UTC cutoff requires an additional,
   explicit backward-skew assumption that V1 does not establish: A2.1 registers no finite bound on B − C, and
   neither ε nor S is one. Inside the window, such an adversary mints receipts that pass; the window cannot be
   shortened, and detecting misuse is the B(ii) add-on, not V1.

**C3 non-claim.** The two keys are *separate technical failure domains under a single controller; no separation of
control or independent fates.* The `gpg` signer signs frames delivered by the AWS-side issuer, so capture of the
issuing account confers signing capability for both slots; the non-exportable key prevents key export, not misuse.
With the hybrid the slots differ in algorithm (lattice and elliptic curve) and custody (AWS KMS and the
slot-2 custody); under the fallback a P-256 break defeats both slots.

## A9.7 What changed

**Registered sentences changed.** Kind: **W** weakened, **C** capability not offered by V1, **G** gate or trigger
moved, **H** hypothesis withdrawn, **T** test registration, **R** replaced or narrowed for V1, **K** clarified. Every
change applies to `tessera-v1-strict` only; each sentence stays standing and governs everything else. Paths are
`docs/` unless given. Quotation marks mark exact source words; *paraphrase* marks the rest. The file:line column
is the source citation; the replacement column points into this amendment.

| # | Registered sentence | file:line | Replacement for V1 | Kind |
|---|---|---|---|---|
| 1 | "Before any code, the central guarantee is established by a machine-checked formal model and proof … No time bound … the Phase 1 / H1b clock does not start until Band 0 is resolved" | `phase-0-prereg.md:102-107` | A9.2's single code gate; P8 by prose proof plus vectors, time-boxed, not machine-checked; the 30 Oct ceiling and slip rule replace "No time bound"; H1b withdrawn | W |
| 2 | "Band 0 (H0) must be resolved before Phase 1 begins"; "Only then does **Phase 1a** begin …, marked by an explicit, dated, signed commit declaring the build runway open" | `phase-0-prereg.md:714-732` | The prerequisite changes: the recorded 30 Oct V1 exit (A9.2), not H0's resolution, opens Phase 1a for V1-profile code only; H0 stays unresolved. The explicit, dated, signed opening commit remains | G |
| 3 | Capstone gate: every ledgered cross-model assumption discharged with a broken companion | `phase-0-prereg-amendment-3.md:220-231` | Strict correct-form rows only; case (d), divergences and withheld results stay with the capstone | G |
| 4 | "Done when (v1 product)" and the kill criterion | `phase-0-prereg.md:589-617` | Not V1; kept as the later product done-line | C |
| 5 | H1a red-bar "for each attack family … and each degradation scenario" | `phase-0-prereg.md:203-208` | A9.5's suite; degradation cases move to their capability | G |
| 6 | H1b: LocalStack, 1/sec, within 7 days of the H1a freeze | `phase-0-prereg.md:210-224` | Withdrawn for V1, not falsified | H |
| 7 | P6: `key_authorized(declared) ∧ no revocation effective at or before anchor_time` | `phase-0-prereg-amendment-1.md:199-214` | Not evaluated; `revocation: NOT_EVALUATED` (A9.4) | W |
| 8 | A4.3's rewritten revocation-after-anchor sentence | `phase-0-prereg-amendment-4.md:111-123` | As row 7 | W |
| 9 | §4.4 "Revocation is time-relative … `INVALID`" | `phase-0-prereg.md:537-546` | As row 7 | W |
| 10 | Standing mechanism modelled "before Band 0 exit" | `formal/spike/FIRST-LINK-SPIKE.md:50-56` | Moves to Protocol standing | G |
| 11 | Standing invariant | `phase-0-prereg-amendment-3.md:531-557` | No TLR; standing `ABSENT/NOT_ISSUED_IN_PROFILE`, reported separately | C |
| 12 | Refusal-record decomposition, commitment, companions | `phase-0-prereg-amendment-3.md:572-581`, `:816-828` | Bounded local refusal returned by the API | C |
| 13 | Integrated lifecycle model green before the H1a crypto-core freeze | `phase-0-prereg-amendment-3.md:783-806` | Trigger moves to Wrapping and renewal; the 30 Oct profile freeze is not the crypto-core freeze | G |
| 14 | Custodial renewal "before the old mechanism becomes unreliable" | `phase-0-prereg-amendment-3.md:273-278` | No renewal; custody and dependency manifest stated (A9.5) | C |
| 15 | KMS and local GPG "independent failure domains"; *paraphrase:* they fail for uncorrelated reasons (source: "They fail for *uncorrelated* reasons"), so durability does not rest on any single domain surviving; and "two independent signatures whose validity does not share a failure domain" | `phase-0-prereg.md:292-299`, `:304-305` | Narrowed to C3's non-claim: separate technical failure domains under a single controller; no separation of control or independent fates; under the fallback both slots share P-256's failure. The registered local-GPG placement is replaced for V1 by A9.6's slot-2 custody alternatives, both through the external policy signer; rule O and the gpg fingerprint scheme are retained. The spec's restatements (`implementation-spec.md:226`, `:604-610`) follow this row as consequences; they are not new author rulings | R |
| 16 | A8.4's new query ("a new query, predicted red under C-C15(i) … run with A8.3's batch") and its spec edits (O-74, R-6.44 innermost) | `phase-0-prereg-amendment-8.md:95-98`, `:100-106` | Postponed with standing; A8 remains the source record | G |
| 17 | Prototype scenario expectations | `prototype/consumers/scenarios.py:72-133` | Kept as history; A9.1's mapping registered prospectively | T |
| 18 | Dead-project (clean-room) demonstration | `phase-0-prereg-amendment-3.md:371-378` | Not run for V1; the dead-service test is | G |
| 19 | Forward-link successor slot registered "before format freeze with a slot-bearing golden vector" | `implementation-spec.md:651-656`; `formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:159-206` | Not in V1; a later profile carries it | C, G |
| 20 | §4.7 review recency attested (hard rule) | `phase-0-prereg.md:564-572` | Not offered by V1; moves with the product done-line | C |
| 21 | Custodial parameter schema and clock roles ratified at Band 0 | `phase-0-prereg-amendment-3.md:435-451` | Trigger moves to Wrapping and renewal | G |
| 22 | "numbers must be exactly representable as IEEE 754 doubles … string-encoded, never a JSON number"; restated in A7's canonical-payload reading ("under the precision rule of the original §4.3") | `phase-0-prereg.md:501-505`; `phase-0-prereg-amendment-7.md:33-39` | A9.8's value-preserving rule | R |
| 23 | Rejection of "numbers not exactly representable as IEEE 754 doubles" | `phase-0-prereg-amendment-1.md:268-270` | A9.8's value-preserving rule | R |
| 24 | "signatures and anchors commit to a framed envelope" (R-3.9); restated in A7 ("Signatures and anchors commit to the signed frame") | `phase-0-prereg-amendment-1.md:255-264`; `phase-0-prereg-amendment-7.md:33-39` | Signatures commit to frames; the receipt anchor commits to frames plus their exact signatures (A9.5) | K |
| 25 | "Hybrid classical+PQ dual signing is explicitly deferred to a deployment profile or later amendment" | `phase-0-prereg-amendment-3.md:480-482` | If the spike passes, V1 is that deployment profile, governed with the branch-registration supplement (A9.6); otherwise unchanged | R (conditional) |
| 26 | P7's amended discharge: the verdict-independence half by S-P7 Q4's control and companions and "one H1a conformance vector" on the band-1 docket | `phase-0-prereg-amendment-6.md:43-57` | The wrapper half and its H1a vector move to Wrapping and renewal (A9.3); P7's type-separation half stays on the 30 Oct gate | G |
| 27 | The waived-evidence observation record; "The record format is an H1a obligation, entered on the band-1 docket" | `phase-0-prereg-amendment-5.md:145-154` | Moves to Degraded verification (A9.3, "A5.3 record") | G |
| 28 | The degraded-policy semantics (waiver lattice) | `phase-0-prereg-amendment-1.md:301-327` | Not offered by V1: strict only, no waiver policy (A9.1); moves to Degraded verification | C |
| 29 | "an identifier prohibited by applicable policy" | `phase-0-prereg-amendment-3.md:503-508` | A9.4: V1's registered algorithm policy determines its verdict; later algorithm prohibition/cutoff results belong to a separate assessment and cannot overwrite that verdict | R |

**Changed in effect (not counted below).** "the public git commit publishing the same fingerprints"
(`phase-0-prereg-amendment-1.md:434-438`) and "public repositories" (`phase-0-prereg.md:300-302`). C4 does not
establish public publication. **OWNER DECISION 2026-10-12: public publication remains an issuer duty, and the
verifier does not prove that it happened.** Reason: the author's standard for authority capture is *visible*
(2026-10-08). A key assertion nobody can see cannot make a capture visible, so publishing the repository is what
lets a third party notice a substituted key. The verifier cannot check this duty; the relying-party text says so.

**Process readings changed in effect** (clerk readings, not registered theorem statements; listed so the change is
visible, and not counted as registered changes; acknowledged in `V1-DERIVATION-DRAFT.md:212-216`):
- E10's extraction timing moves to 13 Nov (`formal/BAND0-EXIT.md:69-70`, `:96-97`).
- The exit-status reading for V1 (`implementation-spec.md:2197-2198`): the 30 Oct exit is V1's, not Band 0's.

**Named and not changed:** "The PQ signature implementation … gates the production version"
(`phase-0-prereg-amendment-3.md:473-476`; V1 is not the production version); A1's monotonic key lifecycle (`phase-0-prereg-amendment-1.md:216-224`; any rotation
issues a new key); H3's three cost numbers (`phase-0-prereg.md:232-248`); the red-bar/CI rule (`:548-553`);
break-chain attacks (`:203-205`); the P4 check-result partition (later algorithm-policy effects are narrowed by row 29); A2.1's predicate; the credibility line; §8's "does not proceed"
clause.

**In sum:** two weakenings (P6, rows 7–9; the code rule, row 1); one hypothesis withdrawn (H1b, row 6); eleven gates
or triggers moved (rows 2, 3, 5, 10, 13, 16, 18, 19, 21, 26, 27); seven capabilities not offered (rows 4, 11, 12,
14, 19, 20, 28); one claim narrowed (row 15); five sentences replaced or clarified for V1 (rows 22–25, 29); one test
registration changed (row 17). Twenty-nine rows, plus one disposition left open and two process readings. A8
remains the source record.

## A9.8 The number rule, for the V1 profile — OWNER DECISION (ENCODING-V1 D-1); supersedes rows 22–23

prereg §4.3 and A1 P8 reject a number not exactly representable as an IEEE 754 double. That rule does not compose
with RFC 8785: it accepts inputs whose canonical form it then rejects (ENCODING-V1 §1.2). For `tessera-v1-strict`
it is replaced by: **accept a number exactly when RFC 8785's canonical serialization preserves its value; reject
otherwise.** Proof: `formal/p8/PROOF.md` Lemma 3. Vectors: `formal/p8/vectors/`.

---

## Open items, not decided by this amendment

- **Q4**, recruiting the person who serves as the 4 Dec tester, recorded as "Aki Doe" (AUTHOR DECISION C requires
  a human; A9.1 fixes n = 1 and the independence criteria).
- The pair algorithm identifier (registered in the branch-registration supplement, A9.6).
