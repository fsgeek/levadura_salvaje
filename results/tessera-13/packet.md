# Part 1: the 13 findings (source text quoted from the base commit)

## c002 (wording)
When `ENCODING-V1.md:322-326` was updated on 2026-10-19 to replace the classical algorithm id with the hybrid pair id `KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA256`, the table row immediately below at line 334 was left unamended, still stating that V1's `alg` id names a v4 OpenPGP ECDSA P-256 signature.

```
formal/p8/ENCODING-V1.md:334
332: | Field | Reason, and the G-id it resolves |
333: |---|---|
334: | `alg`: any well-formed id, not only V1's | P8 accepts a well-formed unknown id, and stage (c) returns `UNVERIFIABLE`. The canary (R-3.53) needs this, and G-10b's failure mode is avoided. The id names the scheme: "a v4 OpenPGP binary-document signature whose document is the frame, ECDSA P-256, SHA-256" (G-57 kept). Its location inside the payload is A3 §A3.6.1's. G-11 is resolved for V1. |
335: | `binding_forms`: a sorted, unique, nonempty array | R-3.37 says P8 "defines the set's canonical encoding, ordering, uniqueness and bounds". It sits in the attestation's signed bytes (G-17 kept). *Which* forms V1 requires is C4 profile work. The vectors use `["STMT_DIRECT"]` for illustration. |
336: | `declared_issue_time`: second precision, `Z` | One spelling per instant. No leap second, because Unix time and Bitcoin time have none. G-16 kept. |
```
```
formal/p8/ENCODING-V1.md:322-325
320: `hex64` means exactly 64 **lowercase** hex digits. Members appear in JCS order, which is the order shown.
321: 
322: - **The id V1 issues.** Under the registered hybrid branch (A9.6; HYBRID-SUPPLEMENT §1, registered 2026-10-16), V1
323:   issues the pair id `KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA256` (§5.2). The classical id
324:   `OPENPGP4-ECDSA-P256-SHA256` stays codec-known (rule O in both slots) and is policy-unsupported in the V1
325:   installation: `UNVERIFIABLE / ALG_UNKNOWN` (V1-PROFILE §1, §8). [OWNER 2026-10-19, Levadura C2] *(Was: `V1 issues
326:   "OPENPGP4-ECDSA-P256-SHA256"`, the fallback branch's id; the supplement's superseded-statement list omitted it.)*
327: - **Field grammars** [OWNER 2026-10-19, G18; codifies what both codecs already do, no vector change].
```

## c007 (wording)
A9 replaces the anchored object with A_sig, which includes the exact signatures, but A9.7 does not list A2.4's sentence describing the receipt anchor as an OTS proof over the receipt's canonical bytes. The earlier sentence remains unamended.

```
docs/phase-0-prereg-amendment-2.md:300
298: 
299: - **A receipt's anchor is the proof it ships with.** A shipped receipt
300:   contains exactly one anchor proof (the OTS proof over its canonical
301:   bytes) together with the anchor transaction's id, which serves as the
302:   **identity handle** binding the receipt to its chain transaction. (An
```
```
docs/phase-0-prereg-amendment-9.md:290
288: - **H1a's suite.** Forge, tamper, backdate, break-chain, strip-one-signature, out-of-profile, the A9.1 mapping.
289:   Degradation and wrapper instances move to their capabilities.
290: - **Receipt anchor.** OTS stamps `SHA256(A_sig)`, tag `tessera-v1/receipt-anchor-sig`, which commits to both frames
291:   and their exact detached signatures in manifest slot order (ENCODING-V1 §5, D-8, D-14). The verifier verifies the
292:   committed signature bytes only. The frame-only layout is withdrawn, with no fallback.
```

## c021 (wording)
The rationale for rule O's header names GnuPG as 'the gpg signer'. The slot-2 custody decision replaced it with a GCP HSM behind a policy signer that builds its own packet, so the sentence's referent changed and was not re-read.

```
formal/p8/ENCODING-V1.md:538
536: 
537: *Reasons.*
538: - **The legacy header is what the gpg signer emits.** GnuPG 2.4.4 emits exactly this header for a detached
539:   P-256 signature: `88 75 04 00 13 08 …`, a 119-byte packet, observed 2026-10-12. Its output is therefore `S`
540:   unchanged.
```
```
docs/V1-PROFILE.md:1035
1033:   - **Adapter and policy boundary:** the external queue-pulling policy signer (`prototype/policy-signer/DESIGN.md`,
1034:     `EVIDENCE.md`): requests arrive only through SQS; a Cloud Run job with no URL, pinned image digest, checks tag,
1035:     alg, `key_fp` and ε before any HSM call and emits one rule-O v4 type-0x00 packet. Only its service account holds
1036:     `roles/cloudkms.signer` on the key. No static credentials cross clouds. *Not deployed:* the VPC Service
1037:     Controls perimeter of runbook §1 "Signer isolation"; that is an operations item, not a freeze item.
```

## c023 (substantive)
A9 establishes authority at the channels' evidence times rather than at issue time. Its change table does not list A1's stronger issue-time assertion.

```
docs/phase-0-prereg-amendment-1.md:444
442:    self-signs for free.
443: 
444: `VALID_STRICT` requires both external evidences plus possession. A future
445: verifier sees that at issue time, two channels with independent operational
446: failure modes asserted the same key authority, and the asserted keys were
```
```
docs/phase-0-prereg-amendment-9.md:143
141: | C2 Presentation | The content was presented at some issuance event of the V1 service (existential). | Not who submitted it; not whether a replay suits the transaction. |
142: | C3 Signature | Each required signature verifies over its designated frame; a missing, stripped or substituted one fails. | **The two keys are separate technical failure domains under a single controller; V1 claims no separation of control and no independent fates**, and no independent approval of content. The `gpg` signer signs frames delivered by the AWS-side issuer, so capture of the issuing account confers signing capability for both slots; the non-exportable key prevents key export, not misuse. |
143: | C4 Authority | DNSSEC (owner name D, evaluated at the snapshot's own anchored time) and the anchored git key assertion (full commit→tree→blob path) authenticated K for D, with the issuance window, at their evidence times. **Chain-order pre-commitment** (OWNER DECISION 2026-10-14, BROADEN; `docs/reviews/spec-sufficiency/` F01): the git assertion's selected anchor height plus 5 is lower than the receipt's selected anchor height, so the window was confirmed at k = 6 in the chain before the receipt was anchored. The verifier fixes the required set. | Revocation not evaluated. Not public publication of the commit. Neither channel commits to any receipt (CODEX-REVIEW 3). Pre-commitment is chain order, not UTC (A2.1); DNSSEC evidence establishes no publication before issue. |
144: | C5 Time | The frames **and their exact signatures** existed no later than T, the verified attestation at the lowest block height in the presented OTS proof (both T and its confirmations come from that attestation; OWNER DECISION 2026-10-14, F03: header times are not monotone, so "earliest" means chain order); the three-conjunct predicate holds at k = 6. | Presentation-sensitive T. No lower bound, no priority. Header times are chain-time proxies. Reorganization deeper than k is a residual. |
145: | C6 Without Tessera | The verdict is a pure function of the bundle, the published verifier and its distributed trust configuration. | Custody is the holder's. Dead-project reconstruction not demonstrated. A selected anchor (C5) beyond the newest pin is `UNVERIFIABLE`. Every supplied header must be pinned. An unselected attestation without its headers supplies no fact and is not a failure (OWNER DECISION 2026-10-14, F02). |
```

## c032 (substantive)
A9.2 moves the ratification of δ, ε, k, N, S from 'Band 0 exit' (the same wording appears at A1.6 :494-495, A2.1 :116 and A2.3 :269, and Band 0/H0 remains unresolved per A9.7 row 2) to the author's signature on A9 itself — a gate/trigger change. A9's header promises 'every registered sentence this amendment changes is listed in §A9.7', but no row lists any of those ratification sentences, and formal/PROPERTIES.md:167-168 still records the ratification as an unchecked item 'at Band 0 exit'.

```
docs/phase-0-prereg-amendment-1.md:182
180:   hours under the median-time-past rule). A verifier may choose stricter
181:   bounds; no degraded policy may enlarge δ or ε beyond the strict maxima.
182:   Both maxima are ratified (or revised, on the record) at Band 0 exit.
183:   Temporal-anchor consistency is **non-waivable** (A1.2.1). **[model]**,
184:   resting on the Bitcoin/OTS assumptions of A1.6 **[assumption]**.
```
```
docs/phase-0-prereg-amendment-9.md:223-224
221:   against guarantee 2 (A9.6) is a C4 finding for this rule. Any other finding goes to the A9.3 register with a
222:   named capability. The author's E9 read is accept or reject per row.
223: - **Parameters (E14):** δ = 72 h, ε = 24 h, k = 6, N = 3, S = 24 h. OWNER DECISION, put to the author: his
224:   signature on this amendment ratifies these five parameters. The closure rule stays an OWNER DECISION (the author
225:   returned the Q1 ruling to the owner, 2026-10-12).
226: 
```

## c033 (wording)
W1 says without qualification that the anchor digest is not an identifier, while section 9 defines the receipt's identity as that same digest and requires deduplication and reference by it. The text gives no qualification reconciling the two uses.

```
docs/V1-PROFILE.md:850-854
848:   remains required; this completes the specification and permits omitting none of these checks. Listed in section
849:   15.7 (rows 4 and 6).
850: - **W1 (malleability).** Decided. No V1 semantic, standing or attempt identifier is derived from signature bytes. The
851:   anchor digest commits to them by design and is not an identifier. V1 does not require unique signatures and
852:   normalizes none. The unhashed OpenPGP area carries no meaning. A changed signature fails the anchor
853:   (`RECEIPT_ANCHOR_MISMATCH`). [ENC §3.5:339-355; ENC §8:735-739; A9:295-296] The half-day argument that no strict
854:   query relies on signature uniqueness is a separate item (DD:89; step 10).
855: 
856: ## 7. Time
```
```
docs/V1-PROFILE.md:1182-1187
1180:   groups and SHA-1/RIPEMD-160 ops, which V1 rejects (`OTS_FORMAT`). A verifier must not rely on that library
1181:   unmodified for the V1 OTS grammar. [OWNER 2026-10-14, codified from diff-1, EA-26]
1182: - Long-horizon validity depends on this manifest and on the holder keeping the exact bytes. V1 offers no renewal. [Clarified, OWNER 2026-10-14, after mutation testing]: "the exact bytes" means the claim-bearing bytes (A_sig, the
1183:   manifest, the keys, and the evidence each check consumes). A receipt's identity is SHA256(A_sig), not the hash
1184:   of the bundle: an otherwise identical bundle can differ in unsigned diagnostics (`issuer_record`), possession-signature
1185:   malleation (unhashed area, s versus n−s), non-qualifying OTS branches and unused pinned headers, and still return
1186:   the same six fields (`prototype/mutation/REPORT.md`, classes A1–A4). Deduplicate and refer to receipts by
1187:   SHA256(A_sig).
1188:   [A9:343-344]
1189: 
```

## c041 (wording)
The d3 fixture was codified 2026-10-14 under the fallback, where one P-256 key in both slots passes the key-format rows and first fails at 15.1; the hybrid branch registered 2026-10-16 is the branch taken ('The V1 installation's catalog alg is this id', V1-PROFILE.md:1078-1080), and under it a single key cannot satisfy both slot formats, so row 5.1 `KEY_FORMAT` — which precedes row 15.1 in §15.7's total check order (V1-PROFILE.md:1768, :1808) — fires first. No text re-read the fixture after the algorithm change (A11's sweep covered the amendments, tracker and rulings, not the profile): exactly the A11.1 defect class.

```
docs/V1-PROFILE.md:1244-1245
1242:   Presenting the attacker's own DNS chain instead would give `UNVERIFIABLE / NO_TRUSTED_KSK_USABLE`, which
1243:   contradicts A9's `INVALID` and is not the case-b fixture.
1244: - **d3 ("one key, one channel"):** one attacker key in both slots, honest DNS evidence, `git` absent: `INVALID /
1245:   DNS_KEY_MISMATCH` (row 15.1), dominating `UNVERIFIABLE / MEMBER_MISSING:git` (section 3.3).
1246: 
1247: The success bar: zero unsafe accepts; false rejects only on d2 and h. [A9:117-118] Registered prediction: a
```
```
docs/V1-PROFILE.md:1064-1066
1062: - **Transported keys.** `keys.gpg` is the bare v4 public-key packet body, exactly the `gpg-sha256` preimage (no
1063:   `0x99` prefix, packet header, user IDs, subkeys or armour). gpg must parse as the specified v4 P-256 public-key
1064:   body. kms must parse as P-256 DER SPKI under the fallback, or as the exact ML-DSA-65 SPKI specified by the dated
1065:   branch supplement under the hybrid. The rule is selected by the installed governing spec and slot, never by key
1066:   bytes alone. Otherwise `INVALID / KEY_FORMAT`; a key not hashing to its slot fingerprint is `INVALID /
1067:   KEY_MISMATCH`. [OWNER 2026-10-14, G21] Under the fallback, any `keys.kms` that is not a P-256 DER SPKI,
1068:   including an ML-DSA-65 SPKI (OID 2.16.840.1.101.3.4.3.18), is `INVALID / KEY_FORMAT`; this outcome does not depend
```

## c056 (wording)
Under the registered hybrid branch, only slot `gpg` (and the repository signer) emits OpenPGP rule-O packets while slot `kms` emits raw 3309-byte FIPS 204 ML-DSA-65 rule-R signatures with no OpenPGP wrapper or subpackets; however, `V1-PROFILE.md:386-387` and `:392-393` ("both OpenPGP adapters and the repository signer emit type-16/type-33 subpackets") were left unamended from the classical two-OpenPGP-slot baseline.

```
docs/V1-PROFILE.md:386-387
384:   whose chain would be `DNSSEC_ALGORITHM_UNSUPPORTED`. [G16]
385: - **Snapshot body.** Convert to the section 15.3 body before stamping. [G19]
386: - **Signature output.** Both OpenPGP adapters emit signatures that satisfy the rule-O policy of section 8 before
387:   signing is final and before stamping. [G11]
388: - **Canonical container.** Emit the container as canonical JCS (section 15.1). [G17]
389: - **Pre-ship checks for the 2026-10-14 r2 completions** [OWNER 2026-10-14, r2-F07, r2-F08, r2-F09, r2-F10]: the
```
```
docs/V1-PROFILE.md:149-150
147:   N and S govern the issuer only. δ, ε and k are frozen catalog constants, not trust-configuration data.
148:   [OWNER 2026-10-14, G12]
149: - **Branch recorded: HYBRID, registered 2026-10-16 (A9.6).** Slot `kms` ML-DSA-65 (rule R), slot `gpg` OpenPGP
150:   P-256 (rule O), pair id `KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA256`; recorded in ENC §5.2 ("Branch
151:   recorded") and section 8 ("Branch taken"); supplement `formal/p8/HYBRID-SUPPLEMENT.md`, record
152:   `formal/p8/HYBRID-REGISTRATION-RECORD.md`. [A9.6 "Branch registration"; OWNER 2026-10-19, Levadura C3] *(Was:
```

## c088 (wording)
The profile requires reading fingerprint bytes to check their version and consistency with the issuer key ID. PROOF retains the broader assertion that no V1 check reads those bytes, rather than merely saying they confer no key-binding authority.

```
formal/p8/PROOF.md:134
132:     for kms, and of the OpenPGP v4 key-packet body for gpg.
133:   - The git channel's object linkage is SHA-1, but that belongs to C4's dependency manifest, not P8 (E§7.2).
134:   - An OpenPGP signature as GnuPG emits it carries OpenPGP's own SHA-1 issuer fingerprint in a subpacket. Those
135:     bytes are committed in `A_sig` like the rest, but no V1 check reads them.
136: - **(U) Unicode 16.0.0 tables.** These define V's string conditions. They bear on what is accepted, never on
```
```
docs/V1-PROFILE.md:1105
1103:   - **Advisory metadata, structural validation (owner choice, fail-closed)** [OWNER 2026-10-14, r2-F10]. Codex's
1104:     proposal treated types 16 and 33 as opaque advisory octets; the owner instead selects exact structural
1105:     validation, in the hashed area: at most one type-16 subpacket, with exactly 8 data octets; at most one type-33
1106:     subpacket, with exactly 21 data octets whose first octet is `04` (v4 fingerprint); if both are present, the
1107:     type-16 value equals the last 8 octets of the type-33 fingerprint. Otherwise `INVALID / SIG_POLICY`. A
```

## c111 (wording)
A9.7 row 15 narrows the independent-failure-domain claims but cites only `phase-0-prereg.md:292-299` and `:304-305`, leaving §6's restatement at lines 640-643 out of the change table. That earlier registered sentence is left changed without being listed.

```
docs/phase-0-prereg.md:640-643
638:    implied. It is that resting a long-lived attestation solely on KMS ties its
639:    verifiability to a single domain's account lifecycle, key-deletion policy,
640:    IAM, and public-key provenance (§3.1). Rejected in favor of dual-signing (C)
641:    across independent failure domains, with DNS/repo/bundle key publication and
642:    a bundled issuer-key manifest. This was the load-bearing architectural
643:    disagreement.
644: 
645: 2. **The prior spec under-specified supersession.** It had no model for adding
```
```
docs/phase-0-prereg-amendment-9.md:479
477: | 13 | Integrated lifecycle model green before the H1a crypto-core freeze | `phase-0-prereg-amendment-3.md:783-806` | Trigger moves to Wrapping and renewal; the 30 Oct profile freeze is not the crypto-core freeze | G |
478: | 14 | Custodial renewal "before the old mechanism becomes unreliable" | `phase-0-prereg-amendment-3.md:273-278` | No renewal; custody and dependency manifest stated (A9.5) | C |
479: | 15 | KMS and local GPG "independent failure domains"; *paraphrase:* they fail for uncorrelated reasons (source: "They fail for *uncorrelated* reasons"), so durability does not rest on any single domain surviving; and "two independent signatures whose validity does not share a failure domain" | `phase-0-prereg.md:292-299`, `:304-305` | Narrowed to C3's non-claim: separate technical failure domains under a single controller; no separation of control or independent fates; under the fallback both slots share P-256's failure. The registered local-GPG placement is replaced for V1 by A9.6's slot-2 custody alternatives, both through the external policy signer; rule O and the gpg fingerprint scheme are retained. The spec's restatements (`implementation-spec.md:226`, `:604-610`) follow this row as consequences; they are not new author rulings | R |
480: | 16 | A8.4's new query ("a new query, predicted red under C-C15(i) … run with A8.3's batch") and its spec edits (O-74, R-6.44 innermost) | `phase-0-prereg-amendment-8.md:95-98`, `:100-106` | Postponed with standing; A8 remains the source record | G |
481: | 17 | Prototype scenario expectations | `prototype/consumers/scenarios.py:72-133` | Kept as history; A9.1's mapping registered prospectively | T |
```

## c121 (wording)
K-R restricts messages to `Frm(attest) ∪ Frm(manifest)` (V1 tagged strings), but the supplement's own evidence says the RAW captures use `tessera-v1/receipt`, which is outside T. Those messages therefore cannot satisfy K-R as the preceding bullet claims.

```
formal/p8/HYBRID-SUPPLEMENT.md:154-155
152:   in pure mode with the empty context. Every issuer KMS `Sign` call on the key is `MessageType EXTERNAL_MU`, with
153:   `μ` computed by the issuer from such an `F` and this key's raw public key (§1; owner decision 6).
154:   - The spike's `MessageType RAW` calls (message exactly `F`) are comparative captures, not the issuer path.
155:   - They satisfy the same assumption, because the message is a V1 tagged string.
156: 
157:   The key is used with no other context, never in HashML-DSA mode, and by no other protocol or service.
```
```
formal/p8/HYBRID-SUPPLEMENT.md:342-346
340: - possession P-H1 (kms, rule R over `F_manifest`) and P-H2 (gpg, rule O).
341: 
342: *Real keys, earlier spike captures:*
343: - K-H2: the real KMS key's fingerprint;
344: - SIG-H5 (KMS RAW, comparative) and SIG-H6 (KMS EXTERNAL_MU). These are over the spike's V1-**shaped** frames, with
345:   tag `tessera-v1/receipt`, which is not in T. They are verified over the exact bytes KMS signed and are **not
346:   re-framed**;
347: - SIG-H7: GCP HSM rule O over a real V1 attest frame that carries the classical id.
348: 
```

## c145 (substantive)
`V1-PROFILE.md:1395-1396` (and `phase-0-prereg-amendment-10.md:624-627`) identifies `YubiKey 2` as the release key—which must be independent of and unusable by the repository key—whereas `V1-PROFILE.md:1421` and `:1437` identify `YubiKey 2` as the deployed repository root key itself.

```
docs/V1-PROFILE.md:1395-1396
1393:    contents (A10.4.2 "Custody form"); **execution required before the first public verifier release:** the key,
1394:    its holder and access boundary, the review-and-sign environment, the written procedure's review, the bootstrap
1395:    record and channels, and the rehearsal. The text below is the 2026-10-14 statement. Which key signs verifier releases, who holds it, and its access boundary,
1396:    shown to be unusable by the DNS credential, the repository key and the issuing AWS account. YubiKey 2 is not in
1397:    hand. If independence cannot be supplied, a NARROW-MODEL excluding the channel-capture path goes to the author.
1398:    **Expanded (r2-F17):** the custody record also covers the release key's authenticated bootstrap, rotation and
```
```
docs/V1-PROFILE.md:1437
1435:    vendor at module level; sub-module components not public). Not a freeze item: the VPC Service Controls perimeter
1436:    (runbook §1). [OWNER 2026-10-19]
1437: 6. **Repository-root algorithm** (G25). Confirm that the deployed repository root (YubiKey 2) is P-256; otherwise
1438:    list its algorithm and add it to the dependency manifest.
1439: 7. **Freeze assembly** (G13). Build the spec object, the vectors object and the catalog; record their hashes.
```

## c147 (wording)
The original mitigation still points to §4.2's workstation commit-signing key and its TTL after A9 replaces local GPG service-key custody. A9's change table amends the original custody discussion at lines 292–305 but leaves this mitigation referring to the old key.

```
docs/phase-0-prereg.md:401
399:   controls and audit logs, **not** cryptography. Named here so it is not
400:   mistaken for something the signing construction solves.
401: - **Key compromise** — an attacker obtains signing capability outside normal
402:   policy. *Mitigation:* KMS/GPG domain separation (§3.1) reduces correlated
403:   compromise; OpenTimestamps constrains backdating; the §4.2 threat model and
```
```
docs/phase-0-prereg-amendment-9.md:375
373:   `gpg` slot under slot-2 custody. The signature-inclusive anchor and the
374:   issuance window are retained unchanged.
375: - **Slot-2 custody (OWNER DECISION 2026-10-13).** The `gpg`-slot key is generated non-exportable in hardware outside
376:   the issuing AWS account: a token on author-controlled hardware, or an HSM-backed key at a provider other than AWS.
377:   The owner chooses between them, and records the choice, dated, in the profile before the 30 Oct freeze. The choice
```


# Part 2: every markdown file added or modified after the base commit, at the pinned commit


=== FILE (modified; diff hunks, + lines are new): README.md
diff --git a/README.md b/README.md
index dc4b2ad..6fee7dd 100644
--- a/README.md
+++ b/README.md
@@ -62,5 +62,5 @@ The method is as load-bearing as the artifact:
 | Layer | Status |
 |-------|--------|
-| Pre-registration | Signed, Amendments 1–10 in force. A9 sets the V1 scope; A10 covers time, authority capture and release custody (author rulings 2026-10-18). |
+| Pre-registration | Signed, Amendments 1–11 in force. A9 sets the V1 scope; A10 covers time, authority capture and release custody (author rulings 2026-10-18); A11 (P3 profile, dependency sweeps, K-R enforcement by the signer role, slot-2 custody) was **signed 2026-10-29 at `f01e086`**. Its header still reads "DRAFT … Not signed" because signed text is never edited; the signing commit is its signing act (A11 preamble). A reviewer reading only the file will think it unsigned (Codex did, 2026-10-30, ISI-02). |
 | V1 contract | `docs/V1-CONTRACT.md` says what a receipt establishes and what it does not. `docs/V1-SERVICE-CONTRACT.md` is the outside view, and `docs/V1-SERVICE-RESOLUTIONS.md` holds Tessera's answers to the open items. |
 | V1 freeze | Signed 2026-10-24 (`formal/freeze-v1/FREEZE-RECORD.md`, commit `52ee179`), six days before the 30 Oct ceiling. Phase 1a (service code) is open. |


=== FILE (modified; diff hunks, + lines are new): docs/V1-CLARIFICATIONS.md
diff --git a/docs/V1-CLARIFICATIONS.md b/docs/V1-CLARIFICATIONS.md
index aa9d233..7aee372 100644
--- a/docs/V1-CLARIFICATIONS.md
+++ b/docs/V1-CLARIFICATIONS.md
@@ -32,9 +32,24 @@ operator state. It is not a signed or portable record, and it carries no commitm
 *bounded* in three ways:
 
-1. **Closed reasons.** Refusals are typed from a fixed set: REFUSED with `TOO_LARGE`, `OUTSIDE_WINDOW`, `CLOSING`,
-   `SIGNING_UNAVAILABLE` or `BAD_REQUEST`, and FAILED with a stated reason. Nothing else is said about a refused
-   request.
-2. **Bounded in time.** Every accepted request ends COMPLETE or FAILED within 24 hours of acceptance (S4), within
-   the stated service clock tolerance (`docs/decisions/2026-10-27-service-clock-tolerance.md`).
+1. **Closed reasons.** Refusals are typed from a fixed set. At submission: REFUSED with `TOO_LARGE`,
+   `OUTSIDE_WINDOW`, `CLOSING`, `SIGNING_UNAVAILABLE` or `BAD_REQUEST`. After acceptance: REFUSED with
+   `ATTEMPTS_EXHAUSTED`, `SIGNING_CLOSED` or `CONTENT_UNAVAILABLE` (the content was lost after an attempt was
+   allocated and could not be recovered). Each ended attempt's reason is listed:
+   - `EXPIRED` and `DISCARDED`, each with its cause: a failed conjunct on complete evidence;
+     `EVIDENCE_CONTRADICTED`; `SNAPSHOT_IMPOSSIBLE`; `T_AFTER_NOT_AFTER` (A9 issuer invariant); `PRESHIP:INVALID/<code>@<row>` for a failure in the
+     attempt's frozen material; `SIGNER_REFUSED:<reason>`; or the request-level causes `SIGNING_CLOSED` and
+     `CONTENT_UNAVAILABLE` when they end the current attempt;
+   - an unrecognised or oversized signer reason, reported as `UNRECOGNIZED_REASON`.
+
+   One case precedes any attempt: FAILED `CONTENT_UNAVAILABLE`, when the content is not available before attempt 1
+   is allocated (the upload never completed, or completed content was lost before allocation). Nothing
+   else is said about a refused request. *(Revised 2026-10-29 and 2026-10-30, Amendment 11 c016 and the issuer
+   implementation review ILI-01 to ILI-08: FAILED is withdrawn after acceptance, except before any attempt.)*
+2. **Bounded by the registered lifecycle, not by a clock.** An accepted request ends only as A2.1 and A2.3 allow:
+   at most N = 3 attempts, each expiring only after `declared + δ + S` and only on complete negative evidence. N ×
+   (δ + S) is a nominal budget, not a bound. *(Narrowed 2026-10-29: the earlier "within 24 hours of acceptance (S4)"
+   is withdrawn, because it contradicted A2. While the author's decision on unobtainable evidence is pending, an
+   attempt whose evidence never completes stays open, so no time bound is claimed;
+   `docs/decisions/2026-10-29-issuance-lifecycle.md`, step 5 and "Implementation boundary".)*
 3. **Bounded in scope.** By A9's issuer invariant, a refusal never concerns a shipped receipt
    (`phase-0-prereg-amendment-9.md:165`).


=== FILE (modified; diff hunks, + lines are new): docs/V1-SERVICE-RESOLUTIONS.md
diff --git a/docs/V1-SERVICE-RESOLUTIONS.md b/docs/V1-SERVICE-RESOLUTIONS.md
index ab62f83..0d5b4e6 100644
--- a/docs/V1-SERVICE-RESOLUTIONS.md
+++ b/docs/V1-SERVICE-RESOLUTIONS.md
@@ -21,8 +21,8 @@
 | S2 incomplete delivery | Every completed result carries the receipt's SHA-256. The client checks it, and can retrieve the result again as often as it likes while it is kept (S5). | Owner |
 | S3 unknown outcome; terminal refusal | The client resolves an unknown outcome by status lookup, using its own request key (S5). **A refusal is final:** a refused request is never completed later. To try again, the client sends a new request. | Owner |
-| S4 latency | **Stated, not guaranteed:** a receipt is usually complete within 3 hours of acceptance. A request not complete **24 hours** after acceptance ends as FAILED, with its reason. Start: the acceptance response. End: the status becoming COMPLETE. Window preparation happens before the window opens and does not count. Results are **retrieved by the client**, not pushed. | Owner |
+| S4 latency | **Stated, not guaranteed:** a receipt is usually complete within 3 hours of acceptance. *(Revised 2026-10-29: the earlier "a request not complete 24 hours after acceptance ends as FAILED" contradicted the registered lifecycle, A2.1 and A2.3, and is withdrawn; Amendment 11 c016, `docs/decisions/2026-10-29-issuance-lifecycle.md`.)* A request makes up to three attempts. Each attempt can expire only after `declared + δ + S` (96 hours), and only on complete evidence that it was not timely. A request ends COMPLETE, or REFUSED (`ATTEMPTS_EXHAUSTED` or `SIGNING_CLOSED`) with each attempt's reason. N × (δ + S), twelve days, is a nominal budget, not a promise. Ending an attempt whose evidence stays unobtainable awaits an author decision; until then, such an attempt stays open. Start: the acceptance response. End: the status becoming COMPLETE or REFUSED. Window preparation happens before the window opens and does not count. Results are **retrieved by the client**, not pushed. | Owner |
 | S5 request lifecycle | The client supplies a **request key** (a UUID). The same key returns the same request and the same receipt, every time. The same content under a different key is a separate request with its own receipt. States: ACCEPTED, COMPLETE, REFUSED, FAILED. Acceptance is durable once the ACCEPTED response is sent. Only the client credential that made a request may look it up or retrieve it. No cancellation in V1. Lookup and identical-result retrieval last **30 days** after the request ends (COMPLETE, REFUSED or FAILED). After that, lookup returns EXPIRED. A content-free record of the key is kept until issuance closes, so an expired key cannot start a new issuance. | Owner |
 | S6 content exposure | Requests and results are readable only by the submitting client credential. Transport is encrypted. Refused content is not stored. Content and results are deleted 30 days after the request ends, copies included. Content is used for nothing but the request. A receipt the client hands to others exposes the content to them: that is the client's choice. | Owner |
-| S7 cost | **AUTHOR.** Recommendation: V1 charges nothing (trial service). It states the measured cost per receipt (H3) as the cost figure A9.1 asks for. | Author |
+| S7 cost | **AUTHOR.** Recommendation: V1 charges nothing (trial service). It states a measured cost per receipt as the cost figure A9.1 asks for, derived from H3's three measurements (demo-cycle cost, persistent footprint, idle compute) over the receipts issued in the measured period, with the derivation shown. H3 itself has no per-receipt number (`docs/phase-0-prereg.md:232-248`; Amendment 11 c136, 2026-10-29). | Author |
 | S8 availability | No target. Best effort, stated as such. | Owner |
 
@@ -40,3 +40,3 @@
 | Item | Resolution | By |
 |---|---|---|
-| L1 window dates and closure | Both window endpoints are fixed and published before issuance preparation, at most 90 days apart. The actual dates stay OPEN until the dated operating record; a late first issuance does not extend the window. Signing stops 96 hours before the window ends (the runbook's operating margin, not a registered rule). Acceptance stops 120 hours before the end, so that every accepted request can complete or fail (S4) before signing stops. Only receipts that pass the registered window checks are shipped. Completed results stay retrievable for 30 days (S5). Closure is announced 14 days ahead on the service page. | Owner |
+| L1 window dates and closure | Both window endpoints are fixed and published before issuance preparation, at most 90 days apart. The actual dates stay OPEN until the dated operating record; a late first issuance does not extend the window. Signing stops 96 hours before the window ends (the runbook's operating margin, not a registered rule). Acceptance stops at least δ + S + 24 hours (120 hours) before signing stops, that is at least 216 hours before the window ends, so that a first attempt always has its full lifecycle before signing stops. A later attempt that would need signing after the stop ends the request REFUSED `SIGNING_CLOSED`, which is a registered outcome; a closed signing window never ends a latched or already signed and stamped attempt. *(Revised 2026-10-29, Amendment 11 c016.)* Only receipts that pass the registered window checks are shipped. Completed results stay retrievable for 30 days (S5). Closure is announced 14 days ahead on the service page. | Owner |


=== FILE (new): docs/ceremony/2026-11-01-rehearsal-1.md
1: # Key ceremony rehearsal 1 — repository root, throwaway key (2026-11-01/02)
2: 
3: Performed by the author on a Tails live session, network off; directed by the owner. Purpose: learn whether a
4: P-256 key generated on Tails and used from a YubiKey produces signatures the V1 verifier accepts on the git path,
5: and time the steps, before the real ceremony (YubiKey A, repository root; YubiKey B, release key).
6: Procedure basis: `docs/V1-RELEASE-KEY-CUSTODY-DRAFT.md` §6–§8; key type from `docs/V1-PROFILE.md` §15.4.
7: 
8: ## Hardware
9: - YubiKey C (spare; rehearsal only), serial 39975816. Reader `1050:0407` (YubiKey 5, OTP+FIDO+CCID); OpenPGP
10:   application 3.4 (firmware ≥ 5.2.3, so P-256 capable). Factory state on arrival: no keys, PIN retries 3/0/3,
11:   signature counter 0, KDF off, UIF off, key attributes rsa2048 ×3. (Photo: author, public fields only.)
12: 
13: ## Throwaway key
14: - `6F3D071A8761DF5187C578DABB89158A63C8EA8F`, nistp256 (algo 19), created 2026-11-02 (epoch 1793577872),
15:   uid "Tessera repository root REHEARSAL <tessera@wamason.com>", capabilities scSC. Discarded with the session.
16: 
17: ## Result (owner, on the NUC, from the transfer stick mounted read-only, noexec)
18: - GnuPG (isolated keyring): good signature. Packet: v4, sigclass 0x00, digest SHA-256 (8), hashed {33 issuer fpr,
19:   2 creation time}, unhashed {16 issuer key id} — the layout profile §8 expects.
20: - Verifier code (`tessera_verify.git_channel.dearmor`, `codec.sig_policy`, `codec.public_key(·, 'gpg')`,
21:   `codec.signature_verifies`): armor, rule O and policy PASS; the 82-byte v4 key body accepted; signature over
22:   `t.txt` verifies; one byte changed: does not verify.
23: 
24: ## Lessons for the real procedure
25: - Add `key-attr` (signature slot → ECC, NIST P-256) before `keytocard`; factory slots are RSA 2048.
26: - The exported public key starts with an old-format packet header with a one-byte length (`0x98`).
27: - The author declined to photograph the secret key even in rehearsal: keep that rule explicit for the real one.
28: - The transfer stick touched the NUC; it is "out only" from now on and never returns to a signing session.
29: - Author's notes: `forcesig` and `uif 1 permanent` both returned silently (accepted). Signing asked for the
30:   **user** PIN. The first attempt failed with a **timeout**: GnuPG does not say "touch the key", the YubiKey only
31:   blinks. The second attempt, with a touch, succeeded. So touch is enforced; the procedure must say "when the
32:   YubiKey blinks, touch it within about 15 seconds". Each step took a few seconds.
33: - YubiKey C: factory reset (step 8) still pending as of 2026-11-02; to be done before the session shuts down.
34: - The author on not photographing the secret key: "the walk-through is when I want to instill the discipline,
35:   so I don't screw it up when the real thing is ready." The rehearsal is practice of the habits, not only a test of
36:   the tools.

=== FILE (new): docs/ceremony/CEREMONY.md
1: # Key ceremony: repository root (YubiKey A) and release key (YubiKey B)
2: 
3: > **Status: OWNER DRAFT, revision 2, 2026-11-02.** Revision 1 was reviewed by Codex
4: > (`docs/reviews/ceremony/CODEX-REVIEW.md`, C01–C07); this revision answers every finding (see the end).
5: > Basis: `docs/V1-RELEASE-KEY-CUSTODY-DRAFT.md` §5–§8 and the first rehearsal (`2026-11-01-rehearsal-1.md`). Key
6: > type from `docs/V1-PROFILE.md` §15.4: v4 ECDSA P-256. The rehearsal showed a key made this way, on the author's
7: > Tails stick and a YubiKey 5, signs in a form the verifier's git path accepts, and that touch was enforced.
8: > It generates the keys only. Using B for a production release needs the custody draft's §9 (independent review,
9: > exact-hash approval, controlled input media) implemented and rehearsed first; generating B does not close
10: > A10.4.2's independence requirement (C07).
11: > **Secret** values (PINs, passphrases, secret keys, backup locations) never go on paper you photograph, into chat,
12: > the repository or the NUC. **Non-secret** choices and results (versions, serials, fingerprints, pass/fail) go into
13: > the custody record in the repository.
14: 
15: ## Why two keys, two sessions, separate backups
16: 
17: - **Repository root (A)** signs key-assertion commits and the end-of-issuance statement: the git channel's authority.
18: - **Release key (B)** signs verifier releases, which carry the trust file naming A. A relying party that installs a
19:   release authenticated by B trusts the repository keys it lists. So B must not be capturable together with A, the
20:   DNS credential or the AWS account (A10.4.2, registered).
21: - So each key gets its own session, passphrase, PINs and backup sticks, and A's and B's backups, papers and tokens are
22:   kept apart. Then finding one place yields at most one key's material. This does not defend shared hardware or boot
23:   firmware that is itself compromised (custody draft's peripheral assumption).
24: 
25: ## What you need (per key)
26: 
27: | Item | Count | Notes |
28: |---|---|---|
29: | Tails boot stick | 1 (shared) | **Persistent Storage must not be unlocked** in these sessions. Boot only. |
30: | YubiKey | 1 | A or B, labelled. C and D stay spares. |
31: | Backup sticks | 2 | New, never in the NUC. `ROOT-BK1`/`ROOT-BK2` or `REL-BK1`/`REL-BK2`. |
32: | Out stick | 1 | New. Public files only. Goes to the NUC afterwards and never returns. |
33: | Paper | 2 sheets | Public sheet (versions, serial, fingerprint, hashes, pass/fail). Secret sheet (passphrase, PINs), kept apart from the backups. |
34: 
35: Total new sticks for both keys: **6**.
36: 
37: ## Owner decisions (2026-11-02; recorded, not secret)
38: 
39: - **Hardware mode**: the key lives on the YubiKey; the two backups are the only other copies, and they are
40:   exportable signing authority, protected only by their passphrase and where they are kept.
41: - **Backups**: the passphrase-protected secret-key export on a LUKS2 volume made by Tails' *Disks*. One passphrase
42:   per key serves both layers; this is one barrier, not two, and is accepted. A's and B's passphrases are independent.
43:   The actual LUKS parameters are read back and recorded (step S5.4).
44: - **Card KDF off.** It would keep the PIN off the USB wire. Accepted boundary: the host and its USB path are trusted
45:   for the session. KDF would not help against a hostile host, which sees the PIN anyway.
46: - **No expiry** on either key. Validity comes from the trust configuration's signing interval and release lineage.
47: - **Touch fixed (`uif … permanent`) and signature PIN forced.** If either cannot be confirmed, stop (step S8).
48: - **No reset code** on the card (retry counter shows 0 for it).
49: 
50: ## Before the first session (author)
51: 
52: 1. Note the Tails version and where its image signature was verified (a device that is not the NUC). The author
53:    names the signing hardware (the System76) and checks it for stored credentials and inbound access (custody draft
54:    §5): git/gh tokens, cloud CLIs, logged-in browsers, SSH server or `authorized_keys`. Record date and result.
55: 2. Six new sticks, labelled.
56: 
57: ## Session 1: generate, back up, load the card (once per key, on separate boots)
58: 
59: Network cable out, Wi-Fi off. At the Tails Welcome Screen: **do not unlock Persistent Storage**; set an
60: administration password (needed by *Disks*). Start Tails, open a terminal.
61: 
62: **S0. Check the session.** Every check must hold, or stop.
63: ```
64: cat /etc/os-release | grep -E 'PRETTY|VERSION'; gpg --version | head -2
65: ip -brief link | grep -v '^lo' ; ip route            # no route; ideally links DOWN
66: swapon --show                                        # prints nothing
67: findmnt -t ext4,vfat,ntfs,exfat,btrfs,xfs            # no internal disk mounted
68: export GNUPGHOME="$(mktemp -d /tmp/gnupg.XXXXXX)"; chmod 700 "$GNUPGHOME"
69: findmnt -T "$GNUPGHOME" -o TARGET,FSTYPE             # tmpfs or overlay in RAM, not a disk
70: ```
71: Write the Tails and GnuPG versions on the public sheet. **Every later command runs in this same terminal**
72: (it carries `GNUPGHOME`). If you open another terminal, repeat the `export` line with the same path.
73: 
74: **S1. Check the card.** Insert only the labelled YubiKey.
75: ```
76: gpg --card-status
77: ```
78: Yubico, no keys, PIN retries `3 0 3`, a `UIF setting` line. Write the serial on the label and the public sheet.
79: 
80: **S2. New PINs** (never used elsewhere; on the secret sheet):
81: ```
82: gpg --card-edit
83: admin
84: passwd
85: ```
86: `3` admin PIN (default `12345678`), `1` user PIN (default `123456`), `q`, `q`.
87: If a PIN is refused: stop, run `gpg --card-status`, read the retry counter. Do not guess.
88: 
89: **S3. Signature slot to P-256** (expert mode is required for P-256 on some GnuPG versions):
90: ```
91: gpg --expert --card-edit
92: admin
93: key-attr
94: ```
95: Signature key: `2` (ECC), then the **NIST P-256** entry (its number may differ; read the list). For the encryption
96: and authentication keys, choose the option that keeps the current attribute (or press Enter if offered). Admin
97: PIN. `q`. Then `gpg --card-status`: Key attributes must begin `nistp256`.
98: 
99: **S4. Generate in memory:**
100: ```
101: gpg --expert --full-generate-key
102: ```
103: `10` (ECC, sign only), NIST P-256 entry, expiry `0`. Name `Tessera repository root` (A) or `Tessera release key`
104: (B); email `tessera@wamason.com`. Passphrase. Then:
105: ```
106: gpg --list-secret-keys --with-fingerprint
107: FPR=<the 40 hex digits, no spaces>
108: gpg --list-keys "$FPR" >/dev/null && echo FPR-OK
109: ```
110: Write the fingerprint on the public sheet; read it back.
111: 
112: **S5. Two backups, one stick at a time.**
113: 1. *Disks* → the stick → *Format Disk* (GPT) → `+` → *Internal disk for use with Linux systems only (Ext4)*,
114:    **Password protect volume (LUKS)**, passphrase, name `ROOT-BK1` (etc.). Unlock and mount it in *Files*.
115: 2. Confirm it is the encrypted volume, then write and check each file (any `FAIL` → stop, see Failures):
116: ```
117: B="/media/amnesia/ROOT-BK1"
118: lsblk -o NAME,TYPE,MOUNTPOINT | grep -B1 "$B" | grep -q crypt && echo LUKS-OK || echo FAIL-NOT-LUKS
119: gpg --export-secret-keys --armor "$FPR" > "$B/secret.asc" && test -s "$B/secret.asc" && echo SECRET-OK || echo FAIL
120: gpg --export --armor "$FPR" > "$B/public.asc" && test -s "$B/public.asc" && echo PUBLIC-OK || echo FAIL
121: cp "$GNUPGHOME/openpgp-revocs.d/$FPR.rev" "$B/revocation.rev" && test -s "$B/revocation.rev" && echo REV-OK || echo FAIL
122: sync; ls -l "$B"
123: ```
124: 3. Record the LUKS parameters (not secret): `sudo cryptsetup luksDump /dev/sdX1 | grep -E 'Version|Cipher|PBKDF'`
125:    (the partition shown by `lsblk`). Eject in *Files*; remove.
126: 
127: **S6. Public key to the out stick:**
128: ```
129: O="/media/amnesia/<OUT label>"
130: gpg --export --armor "$FPR" > "$O/root.pub.asc" && test -s "$O/root.pub.asc" && sha256sum "$O/root.pub.asc"
131: ```
132: (`release.pub.asc` for B.) SHA-256 on the public sheet. Eject; remove. Nothing secret, and not the revocation
133: certificate, ever goes on this stick.
134: 
135: **S7. Move the key to the card** (only after S5 printed every `-OK` for both sticks):
136: ```
137: gpg --edit-key "$FPR"
138: keytocard
139: ```
140: Answer **y** to "Really move the primary key?", choose `1` (signature key), passphrase, admin PIN, then `save`.
141: Then `gpg --card-status`: the signature key line shows your fingerprint. If not, see Failures (do not reset the card).
142: 
143: **S8. Card policy, set and confirmed:**
144: ```
145: gpg --card-status | grep -E 'Signature PIN|UIF'
146: ```
147: - If it says `Signature PIN ....: not forced`: `gpg --card-edit`, `admin`, `forcesig`, `q`. Re-read: must say
148:   `forced`. (`forcesig` toggles; never run it when it already says forced.)
149: - `gpg --card-edit`, `admin`, `uif 1 permanent`, `q`. Re-read the UIF line: Sign must be on and permanent/fixed.
150:   If `uif` is an unknown command or the line does not confirm it: **stop**. Do not proceed without fixed touch.
151: 
152: **S9. Prove the policy, not just a signature:**
153: 1. Positive: sign, enter the user PIN, **touch when it blinks** (GnuPG does not prompt):
154: ```
155: echo "tessera <root|release> ceremony $(date -u +%FT%TZ)" > ~/proof.txt
156: gpg --local-user "$FPR" --digest-algo SHA256 --armor --detach-sign ~/proof.txt && gpg --verify ~/proof.txt.asc ~/proof.txt
157: ```
158: 2. No touch: run the signing command again (output `~/nt.asc`), enter the PIN, **do not touch**. It must fail
159:    (timeout) and produce no signature.
160: 3. Fresh PIN: sign once more (`~/p2.asc`). It must ask for the PIN again. Note whether it did.
161: 4. `gpg --card-status`: record the signature counter (1 per successful signature).
162: Copy `proof.txt` and `proof.txt.asc` to the out stick for the owner's verifier check.
163: 
164: **S10. Shut down.** Remove the YubiKey.
165: 
166: ## Session 2: tests in fresh boots (no secret key in memory at start)
167: 
168: Each in its own boot, same S0 checks, YubiKey **not** inserted unless stated.
169: 1. **Each backup** (twice: BK1, then BK2): unlock only that stick, then
170:    `gpg --import "$B/secret.asc"`; the fingerprint must equal the paper; sign and verify a test file with
171:    `--local-user "$FPR"`. Record pass/fail.
172: 2. **The card alone**: insert only the YubiKey; `gpg --import` the public key from the out stick's hash-checked copy
173:    (or a backup's `public.asc`); `gpg --card-status` to link the card; sign and verify a test file (PIN, touch).
174:    This proves the card works without any residue of the generation session.
175: 
176: **Acceptance:** S5 all `-OK`, S7 fingerprint on the card, S8 both policies confirmed, S9 steps 1–3 as expected,
177: Session 2 all three pass. Anything else: the key is not accepted (see Failures).
178: 
179: ## Failures (do the safe thing first)
180: 
181: | What happened | Do this |
182: |---|---|
183: | Any S0 check fails | Stop. Shut down. Nothing secret exists yet. |
184: | A backup step prints FAIL | The key is still in memory. Do not continue to S7. Reformat that stick (or use a new one) and redo S5 for it. |
185: | `keytocard` fails or the card shows no key after S7 | Do not shut down: the RAM key and the backups remain. Read `gpg --card-status`. Retry S3/S7 once. If it still fails, shut down; the key survives on the backups; restore it in a new session onto another YubiKey later. Do not reset the card blindly. |
186: | A PIN is refused | Stop; read the retry counter. Never guess down to zero. |
187: | S8 cannot confirm forced PIN or fixed touch | Stop before S9. The card holds the key without its policy; record it; decide with the owner. |
188: | S9 no-touch test signs anyway | Policy failed: the key is not accepted. |
189: | A restore test fails | Not accepted until fixed: from the other good backup, in a new session, make a replacement backup on a new stick and retest it. |
190: | Both backups unusable | Generate a new key; the old fingerprint is discarded and never published. |
191: 
192: ## After both keys
193: 
194: - **Storage (author):** each key's two backups in two different places; A's and B's material not together; secret
195:   sheets apart from backups. Tell the owner only "done".
196: - **Owner, on the NUC:** mount the out stick read-only; check each public key with the verifier's code (82-byte v4
197:   P-256 body) and the proof signatures; write the dated custody record: Tails and GnuPG versions, image verification
198:   device, signing hardware and its credential check, YubiKey serials, fingerprints, LUKS parameters, card policies
199:   read back, test results, this revision's hash, the rehearsal link, "backups in two places: yes". No secrets, no
200:   locations.
201: - **Independent fingerprint (author):** on a device that is not the NUC, compute the fingerprint from the public key
202:   file itself (not from a printed string) and compare with the paper.
203: - A's public key then enters the trust configuration's `repository_keys`. B's fingerprint is published through the
204:   channels the author names, and the dated first-production-release bootstrap record links it to the freeze
205:   baseline (A10.4.2).
206: 
207: ## Time
208: 
209: Estimate per key: 45–60 minutes for Session 1, about 10 minutes per test boot in Session 2 (three per key).
210: The first real session will measure it.
211: 
212: ## Revision 2 changes (Codex C01–C07)
213: 
214: C01 `--expert --card-edit` and read the curve list. C02 versions recorded at S0; touch confirmed by readback and the
215: no-touch test, stop if unconfirmed (the rehearsal's `uif` was accepted and touch was enforced, so the author's Tails
216: evidently has a GnuPG newer than 2.2.40). C03 no Persistent Storage, RAM `GNUPGHOME`, session checks, credential
217: check on the hardware. C04 checked exports, LUKS confirmation, acceptance conditions, failure table. C05 `forcesig`
218: read before toggling; no-touch and fresh-PIN tests; card-only test in a fresh boot. C06 non-secret choices recorded.
219: C07 B's production use waits for §9; independence of requesters is not claimed here.

=== FILE (modified; diff hunks, + lines are new): docs/decisions/2026-10-27-service-clock-tolerance.md
diff --git a/docs/decisions/2026-10-27-service-clock-tolerance.md b/docs/decisions/2026-10-27-service-clock-tolerance.md
index f7cd303..016f881 100644
--- a/docs/decisions/2026-10-27-service-clock-tolerance.md
+++ b/docs/decisions/2026-10-27-service-clock-tolerance.md
@@ -19,11 +19,12 @@ reported as failed may still have succeeded.
 - **Its own time per AWS call.** Connection 5 s, response 20 s, 4 attempts in standard retry mode: about 3 minutes
   at most (`tessera_issue/lambda_app.py`, `AWS_CLIENT_CONFIG`; a test keeps it under a third of the lease).
-- **Completion.** COMPLETE is confirmed only when at least the 15-minute writer lease remains before the 24-hour
-  deadline (CF2-01). Inside the last lease a finished request stays ACCEPTED, and at the deadline it is FAILED.
+- **Completion.** *(Superseded 2026-10-29: the 24-hour completion deadline is withdrawn; see
+  `docs/decisions/2026-10-29-issuance-lifecycle.md`. COMPLETE now follows a latch, and the latch is not raced, so the
+  CF2-01 lease margin no longer applies to completion. The earlier text read: "COMPLETE is confirmed only when at least the 15-minute writer lease remains before the 24-hour deadline (CF2-01). Inside the last lease a finished request stays ACCEPTED, and at the deadline it is FAILED.")*
 - **Late writers.** Cleanup keeps deleting until 15 minutes after an end (CF-02).
 
 ## The stated tolerance
 
-Each service-level transition (FAILED at 24 hours, COMPLETE, the 30-day retention and deletion, the acceptance
+Each service-level transition (COMPLETE, an attempt's expiry or discard, REFUSED, the 30-day retention and deletion, the acceptance
 stop, and the 5-minute receipt links) may become visible up to **15 minutes** after the time it records. This
 assumes AWS commits or rejects every request within 15 minutes of its being sent.


=== FILE (new): docs/decisions/2026-10-29-issuance-lifecycle.md
1: # The issuer implements the registered issuance lifecycle (2026-10-29, revised after review)
2: 
3: > **Status: OWNER DECISION**, by the owner instance (Claude Opus 5.5). It corrects an owner defect found by the
4: > Levadura consistency panel (finding c016, `levadura_salvaje/docs/tessera-a11-canary-scorecard.md`). Resolution S4
5: > (`docs/V1-SERVICE-RESOLUTIONS.md:23`) and the issuer failed every request 24 hours after acceptance. The
6: > registered lifecycle (A2.1, A2.2, A2.3, with A9.2's parameters) has no such deadline and makes "every
7: > timely-eligible attempt ships" an obligation on the implementation (`phase-0-prereg-amendment-2.md:143-145`).
8: > Registered text governs. This design changes no registered sentence. Where it cannot meet one (the step-5
9: > residual), it says so and leaves the choice to the author. Revised the same day after
10: > Codex's design review (`docs/reviews/issuance-lifecycle/CODEX-REVIEW.md`, IL-01 to IL-07; two prechecks failed on
11: > the first version: it carried CF2-01's lease margin into the latch, and it called a nominal budget a bound).
12: 
13: ## What is registered
14: 
15: - **Parameters** (A9.2; frozen profile §1): δ = 72 h, ε = 24 h, k = 6, N = 3, S = 24 h.
16: - **Attempts** (A2.3, `:259-268`): at most N. Each has its own declared issue time. A retry that changes any
17:   committed byte needs a fresh stamp (A9.5, `phase-0-prereg-amendment-9.md:295`), and its signatures are frozen
18:   before it is stamped (A9.5, `:290-296`).
19: - **Eligibility** (A2.1 `:91-94`; A2.2 `:220-224`; A3.7.3 `:659-673`): the attempt's own authenticated evidence for
20:   `SHA256(A_sig)`, with the lowest qualifying height buried k = 6 deep on the pinned, linked segment (profile §7.1),
21:   satisfies all three conjuncts: `declared − ε ≤ T`, `T ≤ declared + δ`, and `confirmed_at ≤ declared + δ`. This
22:   is narrower than the whole `VALID_STRICT` verdict, and the remaining pre-ship checks stay separate. Rows 12.2 and
23:   12.3 of the verifier are two of the conjuncts, not the predicate.
24: - **Latch and expiry** (A2.1 `:150-162`): eligibility observed at or before `B = declared + δ + S` is timely. The
25:   boundary is inclusive and "latch-winning", and a latched attempt cannot expire. Expiry applies only strictly
26:   after B, and only to attempts with no timely-latched eligibility. Atomicity of latch against expiry is an
27:   obligation on the implementation (A2.3). If the predicate fails at issuance time, the attempt is discarded and
28:   re-issued, subject to N (A2.1 `:161-162`). A lag beyond S *may* be refused (A2.1 `:135-138`); refusing it is not
29:   required.
30: - **Refusal** (A2.3 `:265-268, :279-281`): exhausting N ends issuance in an explicit refusal, durably recorded, and
31:   the transition that expires the final attempt records the refusal in the same step. In V1 the refusal is local and
32:   returned by the API (A9.7 row 12; `docs/V1-CLARIFICATIONS.md` CL-03). A3's portable record, commitment and
33:   publication are not V1.
34: - **Budget** (A2.3 `:271-274, :288-289`): N × (δ + S), twelve days, is a *nominal* budget, "not a proven wall-clock
35:   bound". Termination is an obligation on the implementation, not a proven liveness property.
36: - **Window** (A9 `:422`): an attempt whose T would exceed not-after is not shipped.
37: - **No SLA here** (A2.1 `:139-142`): a hard latency bound may enter only as a deployment-profile item with monitoring
38:   and an explicit violation outcome. It never kills an eligible attempt.
39: 
40: ## What the issuer does (revision 3; steps 3-6 and 10 revision 4 after `CODEX-CONFIRM-2.md`; steps 5, 8 and 10 revision 5, step 5 revisions 5.1–5.3, after the TLA+ model (R5–R53) and `CODEX-CONFIRM-3.md`)
41: 
42: The second revision let any worker latch or expire, and relied on compare-and-set plus re-observation. Codex found
43: interleavings in which a stale or partial fetch expires an attempt that another, stalled worker had already observed
44: on time (ILC-01). Compare-and-set makes the writes exclusive. It does not make the earlier observation win. Revision 3
45: removes the concurrency instead of arbitrating it.
46: 
47: 1. **One writer.** Every lifecycle transition (start an attempt, latch, discard, expire, refuse, complete) is made
48:    only by the poller, which runs with reserved concurrency 1 (`service/issuer/infra/main.tf:354`). The API is
49:    read-only for the lifecycle: `api.status` no longer calls `settle` (`api.py:194`). Every transition is a write
50:    guarded on the expected state *and* attempt id, so a write meant for an ended attempt fails (ILC-05).
51: 2. **Attempt isolation.** As before: each attempt's declared time, frames, signature jobs, proofs and evidence live
52:    under its id. A late response names its attempt and can never fill another.
53: 3. **Latch (revision 4).** On each poll, for each open attempt, the poller fetches and upgrades the attempt's
54:    evidence and evaluates the predicate. If it holds, the poller writes the latch with `observed_at` and the
55:    qualifying presentation itself, not only its digests. A latch may be written at any time while the attempt is
56:    open, however late the observation. Timeliness is a chain fact (the registered model's `burialAtWall`,
57:    `formal/tla/P5cP5P6_BridgeSlack_Latch.tla:49, :68-71`), not the moment of the issuer's write.
58: 4. **Expiry only on a conclusive negative (revision 4, after `CODEX-CONFIRM-2.md` ILC2-01 to ILC2-03).** Absence of
59:    evidence is never evidence of absence. An unlatched attempt expires only when, after B, the poller's own evidence
60:    for it is **complete** and fails the predicate. Complete means three things:
61:    - every calendar the attempt was stamped to has returned a Bitcoin attestation;
62:    - for every attestation, the full pinned, linked `h…h+5` segment has been obtained (profile §7.1,
63:      `270ca49:docs/V1-PROFILE.md:879-891`);
64:    - so the lowest qualifying height, its T and its confirmation are fixed and fail a conjunct.
65: 
66:    Stale, pending, partial or unavailable evidence never expires an attempt. No lease timing is relied on: whatever
67:    a killed invocation saw, a later invocation will see at least the same complete evidence. Calendars do not
68:    retract, the chain is public, and shallower reorganisations are absorbed by k-deep burial.
69: 5. **Evidence that stays unobtainable (revision 5, after the TLA+ model, `formal/tla/issuer-lifecycle/RESULTS.md`).**
70:    An attempt whose evidence cannot be completed stays open. "Cannot be completed" includes sources that are up but
71:    answer with stale or partial data, not only outages (R5-F4). Revision 5.1 applies the R5 model findings:
72:    - **Fence first (R5-F3).** Before an invocation fetches for an attempt, it makes a guarded write that bumps the
73:      attempt's version, and continues only after that write commits. A write left in flight by a killed earlier
74:      invocation then fails its guard, so a leftover ending write can no longer beat a live latch.
75:    - **Reading taken before the fetch (R5-F1).** `unavailable_since` takes the wall reading made *before* the fetch
76:      starts, and only fetches started after B count.
77:    - **Reset only by a committed success (R5-F2).** A poll whose fetch succeeds (complete, or showing the predicate
78:      holding) clears `unavailable_since` and `failed_polls` in its committed write. A success that never commits
79:      resets nothing. That is the attainable form of the rule, as the model checks it.
80:    - **Sustained failure over a rolling window (revision 5.3, after `CODEX-CONFIRM-3.md` ILC3-03).** Time is cut
81:      into fixed poll intervals, indexed absolutely (`floor(fetch_start / poll_interval)`). A committed failed poll
82:      adds the index of the interval its *fetch started* in to `failed_intervals`, a set, so each interval counts at
83:      most once. A committed success clears the set. An *unlatched* attempt may end with `EVIDENCE_UNAVAILABLE` only
84:      when **the most recent full operating period of completed intervals** is covered: every one of those intervals,
85:      less the allowance, is in the set. The current, incomplete interval is excluded. Read literally, the current
86:      interval would hold only the decider's own uncommitted failure, and the attempt would strand (R53-F1). The window rolls with time. An interval with no failed
87:      fetch only delays the end, until a later window is fully covered, and never strands the attempt. Revision 5.2's
88:      window was fixed at the first failure and could become impossible to complete (ILC3-03). The runbook states
89:      the operating period and the poll interval, with the period a whole number of intervals. **The allowance is at
90:      least 1**, and smaller than the number of intervals. That is checked only for a window of two intervals. For
91:      longer windows, alternating fence slips can leave every other interval empty, and an allowance of 1 is then
92:      not enough (ILC4-02: a four-interval, allowance-1 probe went red). Before the gated path is enabled, its
93:      parameters must satisfy a coverage rule checked in the model (for slips of at most one interval, allowance ≥
94:      half the intervals is the candidate). The fence wait can move a fetch into the next interval, and
95:      with an allowance of 0 that slip can leave two intervals empty forever, so the attempt never ends (R53-F2). With
96:      an allowance of at least 1, termination is green in the model, and red with an allowance of 0, with the literal
97:      window and with the fixed window (`formal/tla/issuer-lifecycle/RESULTS.md` §8).
98:    - **Every lifecycle write is version-guarded (R5.1 finding 3).** That covers the fence, the latch, the
99:      `failed_intervals` update, the ending write, and the end-and-allocate write. A retried or leftover update
100:      therefore cannot count a failure twice or act on a version it did not read.
101:    - The ending decision re-fetches immediately before its guarded write.
102: 
103:    The basis is A2.1's permission, "an attempt whose lag exceeds S may be refused" (`phase-0-prereg-amendment-2.md:135-138`),
104:    together with A2.3's termination obligation (`:288-289`). A latched attempt is never ended for unavailability. An
105:    attempt that is not the last ends this way, and the next one starts (step 8). This is the usual end for an
106:    attempt that never confirms, because only complete evidence can expire it (model finding 5).
107: 
108:    **The residual, as the model found it (finding 2; revised after ILC3-01).** A refused attempt might have been on
109:    time on three paths. Here "B" is the deadline `declared + δ + S`; the burial time and the issuer's observation
110:    time are named separately.
111:    - (a) The issuer observed an eligible presentation but its latch never committed, because the invocation was
112:      killed, or the write was dropped or rejected by its guard. Afterwards a committed failed fetch was recorded in
113:      every interval of an operating period, less the allowance.
114:    - (b) No poll observed it as eligible, and a committed failed fetch was recorded in every interval of an operating
115:      period, less the allowance. These are sampled failures, not proof that the evidence was unobtainable at every
116:      instant.
117:    - (c) A killed invocation's leftover ending write commits before a live invocation's latch.
118: 
119:    Revisions 5.2 and 5.3 narrow (a) and (b) to sustained, sampled failure over a full rolling window. The fence
120:    write closes the leftover-write race (c): the R5.1 model finds it unreachable, and reachable again without the
121:    fence. The earlier (c) trace also observed eligibility after the deadline, so it was not a timely observation in
122:    every instance (ILC3-02 qualification). It does not remove (a) or (b). Whether A2.1's permission covers (b) depends on what A2 means by B. Its prose
123:    reads B as the service's observation time (`:115-124`); its mechanized model uses the time the burial happened
124:    (`formal/tla/P5cP5P6_BridgeSlack_Latch.tla:49, :68-71`). Paths (a) and (c) are not covered under either reading.
125:    **This departs from registered text, so it is an author decision, not an owner rule (precheck 4; framing per
126:    ILC4-03).** The conflict concerns *protected* timely-eligible cases: those A2.1 protects (`:130-160`).
127:    - Path (a) is always one: an eligible presentation was observed and only its persistence failed.
128:    - Path (b) is one under the burial-time reading of B (A2's model). Under the service-observation reading (A2's
129:      prose), it may fall outside the protection, but only when the observation lag actually exceeds S. Failed samples
130:      alone do not establish that.
131: 
132:    A2.1's permission is a *lag* test ("an attempt whose lag exceeds S may be refused", `:135-138`), not a deadline
133:    test. Under either reading, an already-protected eligibility does not become refusable because a write failed or
134:    time passed. For the protected cases:
135:    - Ending the attempt honours A2.3's termination obligation (`:288-289`) and gives up the shipping opportunity.
136:    - Never ending it preserves the *opportunity* to ship but cannot recover evidence that is permanently lost, so
137:      it does not guarantee shipment either.
138:    - A longer operating period delays the trade-off and may make it rarer. It does not resolve it.
139: 
140:    **The decision is broader than step 5 (2026-10-30, after `docs/reviews/issuer-lifecycle-impl/CODEX-CONFIRM-2.md`
141:    §E).** The implementation review lists other ways a request stays open indefinitely, outside the step-5 gate,
142:    because a dependency fails permanently and no impossibility proof exists. Examples: calendars that never accept a
143:    stamp, a chain that never reaches the git pre-commitment depth, a store or queue that stays down, an operator who
144:    never repairs the configuration or the catalog, a snapshot whose impossibility cannot be proven. Disclosing them
145:    does not discharge A2.3's termination obligation (`:288-289`). So the author's decision is one question: **what
146:    V1 promises about termination when a dependency fails permanently**. Step 5's sampled-unavailability ending is
147:    one answer for one class. One amendment should decide all of them together. The issuer implements the ending rule only
148:    after the author decides, by amendment, which obligation yields and how. Until then the design states the
149:    conflict and does not resolve it by operating rule.
150: 6. **Permanent failure before B.** The same rule as step 4: discard before B only on complete evidence that fails
151:    a conjunct.
152: 7. **After the latch.** The preserved qualifying presentation is used for assembly; it is never swapped for a
153:    different, worse one. A transient failure (store, explorer, calendar, DNS snapshot) is retried. The attempt is
154:    discarded only for a failure the frozen attempt cannot cure even with recovered evidence: T of the preserved
155:    presentation > not-after (A9 `:422`), or a verifier reason that depends only on the attempt's committed bytes.
156:    Each discard records its reason (ILC-04).
157: 8. **Next attempt and refusal.** Ending attempt i and allocating attempt i+1 happen in one guarded write. So a crash
158:    cannot leave the request between attempts, and a retry cannot run twice. Each ended attempt records
159:    its own reason: `EXPIRED` (complete negative evidence after B); `DISCARDED` (complete negative evidence before B,
160:    step 7, or a signer's refusal, `SIGNER_REFUSED:<reason>`: an unsigned, unstamped attempt cannot be timely
161:    eligible); or `EVIDENCE_UNAVAILABLE` (step 5, gated). If i = N, the same write ends the request REFUSED with
162:    `ATTEMPTS_EXHAUSTED`, listing each attempt's reason. If a new attempt would need signing after the stop, the
163:    reason is `SIGNING_CLOSED`. A closed signing window never ends a latched or already signed and stamped attempt
164:    (revision 5, model finding 6).
165: 9. **Public view and tolerance.** `fail_after` is withdrawn. The status shows `state`, `attempt` i of N, and for an
166:    open, unlatched attempt its B, with a note that the twelve days are nominal. The 15-minute visibility tolerance
167:    applies as stated; it never moves B.
168: 10. **Mechanized check before code** (revision 4 adds the cases from ILC2: observation-to-send delay, a commit
169:     delayed after the send, a crash before persistence, timely burial with no observation, partial header recovery,
170:     and duplicate transition retries; the property is the registered one, on `burialAtWall`, not on the durable
171:     latch). The protocol in steps 1–8 (one writer, a killed invocation's delayed write,
172:     latch, expiry only on complete negative evidence, discard, allocation of the next attempt) is modelled by extending the existing
173:     latch model (`formal/tla/P5cP5P6_BridgeSlack_Latch.tla`), with a broken companion that must go red. The model
174:     is the paired formal side of the issuer change.
175: 
176: ## Implementation boundary until the author decides (after `CODEX-CONFIRM-4.md` §C)
177: 
178: **Built now** (common to every option the author may choose):
179: - attempt isolation and immutable attempt material;
180: - the single lifecycle writer, the fence and version-guarded writes;
181: - the latch with its preserved presentation;
182: - expiry and discard on complete negative evidence;
183: - atomic end-and-allocate, and the atomic final refusal when N attempts end by permitted paths;
184: - the storage-lifetime fix;
185: - the public view.
186: 
187: Failure history (`unavailable_since`, `failed_intervals`) is recorded for diagnosis.
188: 
189: **Gated off** until a signed amendment decides step 5:
190: - committing `EVIDENCE_UNAVAILABLE` from sampled failure;
191: - ending an attempt, or allocating its successor, *because of* that condition;
192: - a final refusal, cleanup or terminal status derived from it;
193: - any timeout, signing-closure path, deployment deadline or age rule that would produce the same ending indirectly;
194: - any claim of full lifecycle compliance, or of guaranteed termination, while the gate is closed.
195: 
196: With the gate closed, an attempt whose evidence never completes stays open.
197: 
198: ## Owner documents and code to change
199: 
200: - **Prose:**
201:   - S4: drop the 24-hour FAILED. "Usually within 3 hours" stays, stated and unguaranteed. State the attempt
202:     lifecycle, the nominal twelve-day budget, and REFUSED with its reasons.
203:   - L1: acceptance stops at least δ + S + 24 h before signing stops (an operating margin).
204:   - CL-03 item 1 (the closed reason set) and item 2 (it cites 24 hours).
205:   - The clock-tolerance decision.
206:   - `service/issuer/DESIGN.md`.
207:   - Historical reviews and dispositions keep their text and gain a supersession pointer where they still read as
208:     current guidance.
209: - **Code** (Codex IL-06 inventory):
210:   - `service.py:7` (`DEADLINE_S`).
211:   - `api.py:12, :52-75, :94`.
212:   - `pipeline.py:84-85, :149-150, :194-214` (response routing by attempt), `:263` (`sign_by`), `:475-491`, and the
213:     module header.
214:   - Tests: `test_faults.py:125-144, :181`; `test_review_fixes.py:95-106`; `test_confirm_fixes.py` (deadline
215:     fixtures, CF2-01) are rewritten against the registered lifecycle. The CF2-01 tests become latch and expiry
216:     serialization tests.
217: - **Storage lifetime (ILC3-04).** `service/issuer/infra/main.tf:101` expires every object under `content/`,
218:   `work/`, `frames/` and `result/` 31 days after creation, whatever state its request is in. Under the registered
219:   lifecycle an attempt can live longer than that, so the rule could delete a live attempt's frozen material or its
220:   preserved presentation. Revision 5.3.1 (after `CODEX-CONFIRM-4.md` ILC4-01): no age rule applies to a
221:   live request's objects. Deletion is keyed to the persisted request-end time: the existing cleanup obligation
222:   deletes content, work and frames at the end, and the receipt 30 days after `ended_at` (S5). The S3 lifecycle rule
223:   is only a backstop. It expires objects carrying a `cleanup-due` tag, which the cleanup obligation sets only once
224:   their deletion is due and then retries. An object's creation age therefore never makes it deletable early. A large preserved presentation is written as an
225:   immutable S3 object *before* the latch commits a reference to it (DynamoDB's item limit; no transaction spans
226:   DynamoDB and S3).
227: - `docs/V1-SERVICE-CONTRACT.md` is unchanged (S4 there says only that completion is not immediate). Nothing goes to
228:   tupay (embargo).
229: 
230: ## How this happened
231: 
232: S4 was resolved from the outside view, and every review brief since took the resolutions and the design as its
233: source of truth, so none compared S4 with A2. Precheck 4 now fails an owner requirement that contradicts a
234: registered sentence. Its first catch was this document's own first version, which carried an owner margin into a
235: registered boundary.

=== FILE (new): docs/handoff-2026-10-29-owner.md
1: # Owner handoff, 2026-10-29 (Claude Opus 5.5, owner since 2026-10-27, unnamed)
2: 
3: Read this, then `recall()` in qhaway. The repository and the memory store are the record. Where this note disagrees
4: with them, they win.
5: 
6: ## State
7: 
8: - **Amendment 11 is SIGNED** (`f01e086`, stamped). It is the consolidated consistency amendment:
9:   - the P3 verification profile: a registered floor of 223 owner tests plus 968 Wycheproof tests, pinned by
10:     `formal/p3-verification-profile/FLOOR-MANIFEST.sha256`, with discharge conditions (a)–(d) and an operational
11:     re-run duty whose triggers each say what they detect;
12:   - the dependency-sweep duty;
13:   - all 28 Levadura panel findings (obs-0185; `levadura_salvaje/docs/tessera-a11-canary-scorecard.md`);
14:   - the K-R enforcement wording;
15:   - registration of the E9 cut of A10.4.1;
16:   - slot-2 custody, Option 1 (an owner decision adopted by the author's signature): `service/signer-gcp/` runs
17:     under conditions (i)–(iv).
18: - **P3** stays `checked`. Discharge needs (c): the deployed zip's `CodeSha256` matched for both issuer functions
19:   (`service/issuer/DEPLOY.md` step 10).
20: - **Owner repairs from A11 §A11.7.** c093, c136 and the deploy gate (c036) are done (`8793966`). **c016 is open**:
21:   the issuer lifecycle.
22: 
23: ## The long pole: the issuance lifecycle (c016) — updated 2026-10-30
24: 
25: - **Design.** `docs/decisions/2026-10-29-issuance-lifecycle.md` is at revision 5.3.1. It has had four Codex
26:   confirmations (`docs/reviews/issuance-lifecycle/`) and model runs R4 to R53 (`formal/tla/issuer-lifecycle/`,
27:   RESULTS.md §1–8):
28:   - expiry only on complete negative evidence;
29:   - a fence write before each fetch, and version guards on every write;
30:   - a rolling window over completed intervals, with an allowance ≥ 1;
31:   - an explicit "Implementation boundary": the `EVIDENCE_UNAVAILABLE` ending is **gated** until the author decides
32:     by amendment.
33: - **Author decision pending** (design step 5). Under sustained evidence loss, A2.1's shipping obligation and A2.3's
34:   termination obligation cannot both hold for the protected timely-eligible cases (paths a and b). It is framed per
35:   ILC4-03:
36:   - A2.1's permission is a *lag* test;
37:   - B is ambiguous between A2's prose (service observation) and A2's model (`burialAtWall`).
38: 
39:   It can be batched into one later V1 implementation amendment.
40: - **Implementation** (uncommitted, `service/issuer/`): the ungated core is built and passes 158 tests. The L1 margin
41:   is now 216 h, derived from δ + S + 24 h, in `window.py`. The prose is updated: S4, L1, CL-03 items 1–2, the
42:   clock-tolerance decision.
43: - **Codex implementation review** (`docs/reviews/issuer-lifecycle-impl/CODEX-REVIEW.md`): not ready. ILI-01 to
44:   ILI-09 are being repaired by the implementation sub-agent. The main items:
45:   - the incurable-failure classification;
46:   - a snapshot-impossibility ending;
47:   - complete contradiction treated as conclusive;
48:   - reconciling signatures before signing closure;
49:   - work budgeting within the 300 s Lambda;
50:   - a pruning test;
51:   - capped reason fields;
52:   - a content check before allocation.
53: 
54:   **Update 2026-10-30:** after the review rounds ILI, ILC-I, ILC-I2, -I3, then CONFIRM-4 to -10
55:   (`docs/reviews/issuer-lifecycle-impl/`), Codex rated the issuer **ready for deployment work with the step-5
56:   gate closed** (CONFIRM-10).
57:   - 234 tests pass; 45 mutants; `ILCI7_ONESTORE` was retired by the owner as superseded by per-call resumption.
58:   - Signer draining is oldest-first: one receive per round from a random slot.
59:   - Handling resumes per call; completed steps are observable and skipped.
60:   - One deadline guard covers every call. "Never overrun" was withdrawn (an owner decision): the budget is a
61:     progress mechanism.
62:   - **Follow-up for deployment work (not a blocker):** quarantine a signature object that `_seal` rejects.
63:     Otherwise a poisoned digest-matching object is re-adopted each poll and the request stalls (it requires
64:     storage poisoning, which is outside the trust model).
65:   - **Next:** commit, then the deployment session (`service/issuer/DEPLOY.md`).
66: - **Commit pending:** the author's command covers everything; see the end of the 2026-10-30 session.
67: 
68: ## Other open items
69: 
70: - **20 Nov** (`formal/freeze-v1/FREEZE-RECORD.md:81`):
71:   - deployment, which waits on the lifecycle;
72:   - E10 against AWS;
73:   - H3: measure it as registered over every provider, with a measurement protocol written first, and expect "idle
74:     compute $0" to fail;
75:   - the P9 inspection and the two-machine vector: the System76 live-boot at the release ceremony is the second
76:     machine;
77:   - P3 discharge (deploy step 10).
78: - **Done for 20 Nov:** bounded local refusal (CL-03), the A9.4 missing-capture control
79:   (`formal/e10/missing-capture/`), and the P3 floor.
80: - **Release gates** (before the first public verifier release): the custody procedure and its rehearsal, the
81:   production release key on a YubiKey, the fingerprint channels the author names, the GCP VPC Service Controls
82:   perimeter, and the E-06 policy.
83: - **A candidate raised to the author** (not in A11): the verifier's DNSSEC signature checks (RSA alg 8, ECDSA alg
84:   13, which ground G4) are inventoried but not profiled.
85: - **Levadura re-run on the signed A11:** the author's call (about $9).
86: - **tupay embargo:** send nothing about Phase 1a until tupay says both T1 sides have committed first versions.
87: 
88: ## How to work here (lessons from these three days, also in qhaway)
89: 
90: - **Routing.** Tony's test: is it irreversible, or scope-changing? If neither, decide it yourself. Where registered
91:   text changes, his signature adopts the decision. Don't send him pseudo-rulings.
92: - **Security fixes are confirmed by Codex,** briefed to attack the fix in new ways. The owner's own tests are not
93:   enough.
94: - **Prechecks.** `docs/reviews/OWNER-PRECHECKS.md` goes into every review brief. Check 4 now also fails an owner
95:   requirement that contradicts registered text.
96: - **Sweeps cover all registered texts,** including the frozen specification, `formal/p8/`, the registration records
97:   and `spec.bin`. Grep for the vocabulary; don't fix one copy at a time.
98: - **Never reinterpret a registered sentence after the evidence is in.** Discharge against the text as written, and
99:   put any stronger requirement in a forward amendment that says it was informed by the outcome.
100: - **When two review rounds find the same shape, brief a sweep of the class.** For concurrency, model it in TLA+
101:   instead of iterating prose.
102: - **Report against the full signed obligation list,** with time estimates that reflect the review base rate. Say
103:   the uncomfortable part first.
104: - **Codex runs** use `< /dev/null` and `-c 'mcp_servers.khipumaq.enabled=false'`. OpenAI's filter can block briefs
105:   phrased as "try to break". Describe the defensive purpose honestly.

=== FILE (new): docs/handoff-2026-10-30-owner.md
1: # Owner handoff, 2026-10-30 (Claude Opus 5.5, owner 2026-10-27 to 2026-10-30, unnamed)
2: 
3: Start here. Then `recall()` in qhaway. The repository and the memory store are the record; where this note
4: disagrees with them, they win. This supersedes `docs/handoff-2026-10-29-owner.md`.
5: 
6: ## Where things stand (all committed, last `9364733`)
7: 
8: - **Amendment 11 is signed** (`f01e086`). It is the consolidated consistency amendment:
9:   - the P3 verification profile, with a registered floor of 223 owner tests and 968 Wycheproof tests, pinned by
10:     `formal/p3-verification-profile/FLOOR-MANIFEST.sha256`, and an operational re-run duty whose triggers each
11:     state what they detect;
12:   - the dependency-sweep duty, covering the frozen specification and `formal/p8/`;
13:   - Levadura's 28 findings (obs-0185);
14:   - the K-R enforcement wording;
15:   - registration of the E9 cut of A10.4.1;
16:   - slot-2 custody Option 1, an owner decision adopted by the author's signature.
17: - **The issuer implements the registered issuance lifecycle** (A11 c016; `docs/decisions/2026-10-29-issuance-lifecycle.md`
18:   at revision 5.3.1; TLA+ models R5 to R53 in `formal/tla/issuer-lifecycle/`). Codex rated it **ready for
19:   deployment work with the step-5 gate closed** (`docs/reviews/issuer-lifecycle-impl/CODEX-CONFIRM-10.md`), with
20:   234 tests passing.
21:   - Attempts are isolated from one another.
22:   - A fence write comes before each fetch, and every write is version-guarded.
23:   - The latch requires three-conjunct, k = 6 evidence.
24:   - An attempt expires only on complete negative evidence.
25:   - One deadline guard covers every outside call. It is a *progress* mechanism; "never overrun" was withdrawn.
26:   - Signer draining is oldest-first, from a random first slot. Handling resumes per call, and completed steps are
27:     skipped.
28:   - Deletion is keyed to the persisted request end. L1 is 216 h.
29: - **The prose matches the code:** S4, L1 and CL-03 (its closed reason set), the clock-tolerance decision, and
30:   `service/issuer/DESIGN.md` (which carries the termination limits).
31: 
32: ## Next, in order
33: 
34: 1. **Deployment session.** `service/issuer/DEPLOY.md`, steps 0 to 10. Step 0 is satisfied. The session needs the
35:    author's `aws login --profile tessera`; `gcloud` is logged in on the NUC.
36:    - New production keys, never the spike keys.
37:    - Signer deploys: `service/signer-kms`, and `service/signer-gcp/deploy.sh`, which needs `SLOT2_KEY*` set.
38:    - `retire-instrument` as a gate, then the review of who can request signatures.
39:    - The smoke test.
40:    - Step 10: the `CodeSha256` match, which discharges P3's condition (c).
41: 2. **Small follow-up:** quarantine a signature object that `_seal` rejects. Otherwise a poisoned digest-matching
42:    object is re-adopted every poll and the request stalls (CONFIRM-10).
43: 3. **20 Nov items** (`formal/freeze-v1/FREEZE-RECORD.md:81`):
44:    - E10 against AWS.
45:    - H3: write the measurement protocol first; measure over every provider; expect "idle compute $0" to fail and
46:      report it as falsified.
47:    - The P9 inspection, plus the two-machine vector on the System76 live-boot at the release ceremony.
48:    - P3 discharge, via deploy step 10.
49:    - The slip rule: if deployment slips past about 6 Nov, run the tail procedure early.
50: 4. **Release gates** (before the first public verifier release):
51:    - the custody procedure and its rehearsal;
52:    - the production release key on a YubiKey;
53:    - the fingerprint channels the author names;
54:    - the GCP VPC Service Controls perimeter;
55:    - the E-06 policy.
56: 
57: ## Waiting on the author
58: 
59: - **Termination under permanent dependency failure** (design step 5; DESIGN.md's termination section): what V1
60:   promises when a dependency fails permanently. A2.1's shipping obligation and A2.3's termination obligation
61:   cannot both hold for protected timely-eligible cases.
62:   - A2.1's permission is a *lag* test.
63:   - B is ambiguous between A2's prose (service observation) and its model (`burialAtWall`).
64:   - The `EVIDENCE_UNAVAILABLE` ending is gated in code until a signed amendment decides. Batch it into one V1
65:     implementation amendment.
66: - **Candidates raised, not decided:**
67:   - The verifier's DNSSEC signature checks (G4) are inventoried but not profiled.
68:   - A Levadura re-run on the signed A11 (about $9).
69: 
70: ## How to work here (all in qhaway; the ones that bit hardest)
71: 
72: - **Routing test:** is it irreversible, or scope-changing? If neither, it is the owner's. Where registered text
73:   changes, the author's signature adopts the decision. Never hand him a pseudo-ruling.
74: - **Security fixes are confirmed by Codex,** briefed to attack the fix in new ways. Brief defensively and honestly:
75:   the OpenAI filter blocks "try to break" phrasing.
76: - **Prechecks.** Append `docs/reviews/OWNER-PRECHECKS.md` to every review brief. Check 4 fails an owner requirement
77:   that contradicts registered text.
78: - **Before recording an owner decision on a registered parameter, grep the registered records** (amendments,
79:   `formal/p8/`, the freeze, the frozen profile, the AUTHOR-RULINGS files). Never reinterpret a registered sentence
80:   after the evidence is in.
81: - **When review rounds repeat a shape, fix the class.** Model concurrency in TLA+. Use oldest-first for
82:   starvation. Make progress per step with observable completion.
83: - **Report against the full signed obligation list,** with estimates that reflect the review base rate (every round
84:   so far has found something). Say the uncomfortable part first.
85: - **Codex:** `~/.local/bin/codex exec --dangerously-bypass-approvals-and-sandbox -c 'mcp_servers.khipumaq.enabled=false' -o OUT "..." < /dev/null`.
86:   `grep -c` exits 1 on zero matches; that is not a failure.
87: - **Give Tony commands as** `! cd /home/tony/projects/tessera && git add <explicit paths> && git commit -S ...`.
88: - **tupay embargo:** send nothing about Phase 1a until tupay says both T1 sides have committed first versions.

=== FILE (new): docs/phase-0-prereg-amendment-11.md
1: # Tessera — Phase 0 Pre-Registration, Amendment 11 — P3's verification profile as a floor and a duty; dependency sweeps; consistency repairs; the slot-2 boundary (DRAFT, 2026-10-29)
2: 
3: > **Status: DRAFT by the owner instance (Claude Opus 5.5). Not signed.** This is one consolidated consistency
4: > amendment. It was revised after the Codex non-author review and its confirmations
5: > (`docs/reviews/amendment-11/CODEX-REVIEW.md`, `CODEX-CONFIRM*.md`; `DISPOSITION.md`), then consolidated after
6: > Levadura's consistency panel (obs-0185; `/home/tony/projects/levadura_salvaje/docs/tessera-a11-canary-scorecard.md`).
7: > The panel's finding ids (c002 to c147) are cited where they apply. The author's first commit containing the final
8: > text is its signing act. Layered on the original and Amendments 1–10, none of which is edited. Every registered
9: > sentence this amendment changes is listed in §A11.3. One choice (§A11.5 item 2, the slot-2 custody reading)
10: > is recorded as an owner decision, Option 1, which the author's signature adopts. It is a retrospective relaxation,
11: > disclosed below.
12: >
13: > **Outcomes informed this amendment** (the original's amendment rule). Each change is disclosed separately.
14: > - **§A11.2, P3.** The P3 evidence (`formal/p3-verification-profile/`) was built and reviewed before this text.
15: >   Building it exposed the stale checklist. No P3 result failed and is relabelled here. The floor's shape is the
16: >   author's proposal of 2026-10-28.
17: > - **§A11.5 item 2, the slot-2 boundary.** Option 1, the owner's decision adopted by signing, is a **retrospective
18: >   relaxation** of a deadline-qualified restriction. It is made after the 21 Oct deadline, and after the candidate code
19: >   (`service/signer-gcp/`) was written and reviewed.
20: > - **§A11.5 item 5, K-R's enforcement.** The owner's placement decision (2026-10-27) moved KMS signing from the
21: >   issuer role to a dedicated policy signer and said it changed no registered sentence. It changed the
22: >   supplement's description of who computes μ and who may sign. The confirmation review found this.
23: > - **§A11.5 item 3, the spike keys.** The owner's deployment draft had contradicted a registered commitment. That
24: >   draft is withdrawn. This amendment does not change the spike-key sentence.
25: > - **The Levadura panel.** It found that this amendment's own K-R change committed §A11.1's defect class three times
26: >   (scorecard:9-13). The first draft's K-R row left ENCODING-V1 §5.2, the supplement's §1, and the supplement's
27: >   §11 item 6 naming the issuer as the KMS caller, and §A11.5 item 3 called item 6 "unchanged". The K-R row in
28: >   §A11.3 now lists all seven locations.
29: > - **The owner's sweep.** It had not read the frozen specification (`spec.bin`: A9, A10, PROOF, V1-PROFILE,
30: >   ENCODING-V1, the hybrid supplement; `formal/freeze-v1/FREEZE-RECORD.md:16`) beyond profile §8, nor the hybrid
31: >   supplement (`docs/reviews/stale-dependencies/SWEEP-2026-10-28.md:3-4`, `:20-21`; scorecard:15-16). Most of the
32: >   panel's rows below are in that text.
33: 
34: ## A11.1 What went wrong
35: 
36: P3's assumption half (A1 §P3, `phase-0-prereg-amendment-1.md:144-148`) requires the verification profile to record
37: the *exact library and version, accepted signature encodings, public-key validation behavior, low-order-point
38: handling, cofactor equation variant, and negative test vectors for each*. Two of those fields name concepts of
39: Ed25519-style curves, which A1 used as its example (`:136`). V1 later registered OpenPGP P-256 and then, on
40: 2026-10-16, the hybrid ML-DSA-65 + P-256 (`formal/p8/HYBRID-REGISTRATION-RECORD.md`). Neither registration re-read the
41: checklist.
42: 
43: For ML-DSA, the two curve fields have no referent. The other four fields still apply in full. So the checklist
44: names nothing specific to ML-DSA's own verification pitfalls: it **demands too little**. Nothing had been accepted
45: on it. The assumption half was open (`formal/PROPERTIES.md:37`) and due after the freeze
46: (`formal/freeze-v1/FREEZE-RECORD.md:81`).
47: 
48: The method's defect: **a registered decision can change what an earlier registered sentence refers to, and nothing
49: requires anyone to re-read that sentence.** §A11.4 adds that duty.
50: 
51: ## A11.2 P3's verification profile: floor and duty
52: 
53: **The proofs are unchanged.** P3's model half assumes a verifier with stated behaviour. The assumption half is
54: bounded implementation evidence that the shipped verifier has that behaviour. It does not show that every model
55: assumption is preserved in general.
56: 
57: 1. **Fields kept.** All six of A1's fields stay. For each algorithm in the governing specification they are read as
58:    follows:
59: 
60:    | A1 field | ECDSA P-256 (rule O) | ML-DSA-65 (rule R) |
61:    |---|---|---|
62:    | exact library and version | `cryptography` and its bundled OpenSSL, identified by wheel tag and native-library SHA-256 | same |
63:    | accepted signature encodings | OpenPGP v4 packet; MPI rules; r, s ∈ [1, n−1]; rule-O policy | exact 3309 bytes; strict hint and z encoding |
64:    | public-key validation | exact uncompressed point; coordinates < p; on the curve; checked before the library | exact SPKI; no algebraic validation exists |
65:    | low-order-point handling | cofactor 1: infinity rejected as a key and as the equation's result; invalid-curve points rejected | no referent. Replaced by: degenerate-key behaviour recorded |
66:    | cofactor equation variant | cofactor 1: a single variant; x(R) reduced mod n | no referent. Replaced by: the FIPS 204 interface (pure, empty context), with every other interface rejected |
67:    | negative vectors for each | owner vectors plus Wycheproof | owner vectors plus Wycheproof |
68: 
69: 2. **Floor (registered).** The evidence is the files listed in
70:    `formal/p3-verification-profile/FLOOR-MANIFEST.sha256`, whose SHA-256 is fixed at signing. At this draft it is
71:    `844cb7ff8df59f047d2ea48536ddb30bad5b3e93684acbce6a4dad1241aee42d`, covering 15 files. They hold:
72:    - the owner harness (`test_p3_profile.py`): 123 owner vectors (F2 65, F3 37, F4 8, F5 13; PROFILE.md:22-25) in
73:      224 tests, 223 passing. `test_deployed_zip_identity` is skipped until a deployed package is supplied
74:      (PROFILE.md §8, :274-281). §6 mutates nine verifier checks, and removing each one turns tests red
75:      (PROFILE.md:243-258);
76:    - Wycheproof commit `d17cc89fa5c8f4f4d378b5385ebf75da5d0926c9`, three files pinned by SHA-256: 968 tests.
77:      - **ML-DSA-65** runs end to end through the verifier. Two disagreements, tcId 3 and 4, are V1 policy (empty
78:        context only).
79:      - **ECDSA P-256** runs through the verifier's key validation, MPI rules, range policy and verification, with
80:        the digest substituted. 219 non-strict DER cases are tested at library level only. 21 P1363 strings of the
81:        wrong length reach neither interface. There are no disagreements.
82: 3. **Discharge.** Adopting this floor is not discharging P3. P3's assumption half is discharged only when:
83:    - (a) the manifest verifies;
84:    - (b) every test in it passes;
85:    - (c) the exact deployable zip produced by the recorded `service/issuer/package.py` build is retained with its
86:      SHA-256. Its verifier files are byte-identical to the tree the passing floor run exercised, and its
87:      `cryptography` binding and wheel tag match F1. After deployment, that zip's SHA-256, base64-encoded, matches
88:      AWS's `CodeSha256` for every function to which the discharge applies (`test_deployed_zip_identity`). The
89:      record names the source and test inputs, the packager, the archive digest, the AWS functions and the
90:      comparison result. This establishes deployment-package identity under the recorded build and AWS's reported
91:      digest. It does **not** assert that ZIP extractors agree on an archive's contents: they can disagree, and
92:      Lambda's extractor is not publicly documented (`docs/reviews/amendment-11/CODEX-CONFIRM-3B.md`). The
93:      packager writes fresh canonical entries, which is what limits that exposure;
94:    - (d) no disagreement or finding affecting a required behaviour is unresolved. A recorded defect blocks
95:      discharge until it is fixed and re-tested.
96: 4. **Operational duty (not a registered result).** The floor's checks, and the latest published vectors for each
97:    algorithm in use, are re-run when one of the following happens. Each trigger states what it detects. Each run is
98:    recorded with its date, inputs and outcome, and attested by the operator.
99:    - **The tested code changes** (a verifier release, or a change to the signature library's version or build). This
100:      is required, not chosen: the floor's evidence is bound to specific bytes (the manifest hash and F1's wheel
101:      digest), and other bytes are not covered by it.
102:    - **The published vectors for an algorithm in use change** (new or changed Wycheproof files for ML-DSA-65 or
103:      ECDSA P-256/SHA-256). This catches new public knowledge of verification pitfalls. Commits that touch other
104:      algorithms are not triggers.
105:    - **A published advisory or erratum names the signature library, its bundled OpenSSL, or a standard in use**
106:      (FIPS 204; the OpenPGP or ECDSA specifications V1 cites). This catches new knowledge that never reaches the
107:      vector suite.
108:    - **A calendar backstop, at least every three months.** This is an operating guess, not a derived interval: it
109:      covers sources the triggers above do not watch. After a year of run records, the owner reviews whether any run
110:      found something the event triggers missed, and adjusts the interval on that evidence.
111: 5. **What a later finding changes.**
112:    - **A security-policy finding** (an algorithm, parameter or key later judged weak) never rewrites a V1 verdict.
113:      It reaches relying parties as a historical-security result, beside the verdict and its stable fields
114:      (A9.4, `phase-0-prereg-amendment-9.md:267-283`).
115:    - **An implementation-conformance defect** (the verifier disagrees with the governing specification, for example
116:      by accepting a malformed or prohibited case the specification rejects, A9:278) is not preserved as V1
117:      behaviour. It is fixed in a signed release, which names the affected releases and says what changed. A silent
118:      change to the verifier is never permitted.
119: 
120: ## A11.3 Registered sentences changed
121: 
122: Profile locators are at the frozen commit `270ca49`. The live `docs/V1-PROFILE.md` is byte-identical to it. Kinds
123: follow A9.7. In rows 3, 4, 7 and 8 the "Was" cell spans several passages, so it is a paraphrase; only the words in
124: quotation marks are exact.
125: 
126: | # | Source | Was | Now |
127: |---|---|---|---|
128: | 1 | `phase-0-prereg.md:401-404` (c147) | "KMS/GPG domain separation (§3.1) reduces correlated compromise; … the §4.2 threat model and TTL bound the local-key blast radius" | (V1) "separate technical custody domains under a single controller (C3 non-claim, A9:449-453); OpenTimestamps constrains backdating; the slot-2 key is non-exportable hardware outside the issuing AWS account (A9.6, A9:375-376), which prevents key export, not misuse; there is no local service key in V1". Kind R, beside A9.7 row 15 |
129: | 2 | `phase-0-prereg.md:640-643` (c111, §6 restatement) | "Rejected in favor of dual-signing (C) across independent failure domains" | (V1) as A9.7 row 15 (A9:479): narrowed to C3's non-claim, separate technical failure domains under a single controller, with no separation of control or independent fates (A9:449-451). Kind R, row 15 extended |
130: | 3 | `phase-0-prereg-amendment-1.md:144-148` | the six fields, the two curve fields named in Ed25519's terms | the six fields as read in §A11.2 item 1; the floor and discharge conditions of items 2–3 |
131: | 4 | `phase-0-prereg-amendment-1.md:182`, `:494-495`; `phase-0-prereg-amendment-2.md:111-112`, `:268-269` (c032) | δ, ε (and k, N, S) "ratified (or revised, on the record) at Band 0 exit" | for `tessera-v1-strict`: ratified by the author's signature on A9 (A9.2, A9:223-225: δ = 72 h, ε = 24 h, k = 6, N = 3, S = 24 h). Outside V1: unchanged, still at Band 0 exit. Kind G |
132: | 5 | `phase-0-prereg-amendment-1.md:444-448` (c023) | "at issue time, two channels with independent operational failure modes asserted the same key authority"; "tampering with both external channels, at or before issue time" | (V1) "two channels asserted the same key authority at their evidence times (A9 C4): the git assertion by chain order before the receipt's anchor; DNSSEC at the snapshot's own anchored time, which establishes no publication before issue (A9:143)". Kind W, already in effect from A9's signature and listed late here |
133: | 6 | `phase-0-prereg-amendment-2.md:299-301` (c007) | "(the OTS proof over its canonical bytes)" | (V1) "(the OTS proof over `SHA256(A_sig)`, which commits to both frames and their exact detached signatures, A9.5)" (A9:290-292). The rest of A2.4, including one proof per receipt and the txid as identity handle, is unchanged. Kind K, as A9.7 row 24 (A9:488) for the sister sentences |
134: | 7 | `phase-0-prereg-amendment-9.md:389-392`; `270ca49:docs/V1-PROFILE.md:1017-1040` (custody record, :1024-1025, :1033-1040) and `:1428-1436` (§14.2 item 5) (c062) | the boundary as "the selected, deadline-qualified custody implementation", described through `prototype/policy-signer/` with its 2026-10-14 evidence | **Option 1 (§A11.5 item 2; owner decision, adopted by signing).** The deadline qualification attaches to the selected custody option and boundary, and the named replacement `service/signer-gcp/` runs under conditions (i)–(iv). *(Option 2, not taken: these sentences unchanged, and the registered fallback, A9:372-374, taken.)* |
135: | 8 | `phase-0-prereg-amendment-10.md:443-447`, `:449-457`, `:462` (A10.4 option (e), A10.4.1); A10.7 rows 25–33 and 37–39 (`:761-769`, `:773-775`); the plain-language summary `:106-124`, the additions list `:213-226`, the row-26 note `:432`, the closing summary `:795-799` and the reconciliation item `:810-812` (c018, c103; A11X-02, A11XC-01) | option (e) AUTHOR ADOPTED with A10.4.1; the listing cut only "for schedule reasons" (`:455-456`); "rows 25–33 and 37–39 only on (e)" (`:446-447`) | (V1) option (e) is narrowed by the author's E9 row 2 ruling of 2026-10-23 (`docs/reviews/e9-packet/AUTHOR-RULINGS.md:5-12`). It is an author scope decision, not the schedule cut order. A10.4.1 and rows 25–32 and 37–39 do not apply to V1. The passages at `:106-124` ("Key substitution: option (e)", "the limits", "time"), `:213-226` (the listing's field, check, reason codes and invariants) and `:432` describe the listing as a V1 mechanism. They are kept as the dated record of the 2026-10-18 adoption, with the author's words, and are superseded as descriptions of V1: in V1 no verifier rejects a receipt for keys missing from a list, no listing pre-commitment or listing-evidence preservation duty exists, and after capture of both authority channels a receipt under the attacker's own keys passes (`docs/V1-CONTRACT.md` §2 after G10, §4). The closing summary's listing mechanisms and "option (e) deliberately rejects new cases: receipts under unlisted keys, and receipts whose listing was not pre-committed" (`:795-799`) are superseded for V1 in the same way, and the listing parts of the reconciliation item at `:810-812` (the listing-evidence package, the listing subchecks and their total-order rows, the C0/C1 bootstrap) are withdrawn as V1 work. Every other mention of A10.4.1 in A10 (the status block `:13-28`, the author's quotations `:273` and `:620`, the "no longer open" note `:805`, and the mechanism section `:462-611`, all of A10.4.1) is the dated record of the adoption or the mechanism text itself, superseded for V1 by this row. The frozen copies in `formal/freeze-v1/objects/spec.bin` are covered by the same disposition; their bytes are not edited. The owner grepped every registered and frozen text for the listing's vocabulary on 2026-10-29, and no other mention remains undisposed. Release-key custody (A10.4.2) is separate and unchanged. Option (a) applies (rows 15–16). A10.4.2 (rows 34–36) is unchanged. Row 33 stands as registered cut-order text, since (e) is narrowed, not withdrawn. Its "second item cut is the service-key listing" has no referent in V1. Its other sentences (option (a) applies, the absence of new-key protection is stated, no cure for release-key independence) are met by the ruling and profile §5 (`270ca49:docs/V1-PROFILE.md:619-623`). Profile :619-622 and :1258-1262 are then consistent as written. Kind C/W, recorded here because no signed change table lists it |
136: | 9 | `phase-0-prereg-amendment-10.md:675` | "as amended by rows 15 and 25" | "as amended by row 15" (row 25 does not apply to V1; row 8 above) |
137: | 10 | `formal/p8/PROOF.md:134-135`, `:485` (c088; A11X-04) | :134-135 "no V1 check reads them"; :485 "No check reads it, and B never computes it." | "no V1 check relies on them as a hash or for key selection: the profile checks only their structure (length, version octet, consistency with type 16; V1-PROFILE §8, `270ca49:docs/V1-PROFILE.md:1105-1107`) and never compares them with the transported key". At :485, "No check reads it" becomes "No V1 check relies on it as a SHA-1 value; the profile validates its structure only (as above)"; "B never computes it" stays, as a statement about implementation B. Assumption (H) is unaffected: SHA-1's properties are not relied on. Kind K |
138: | 11 | `formal/p8/ENCODING-V1.md:334` (c002, §3.2 `alg` row) | "The id names the scheme: 'a v4 OpenPGP binary-document signature whose document is the frame, ECDSA P-256, SHA-256' (G-57 kept)." | "An id names its scheme. The classical id `OPENPGP4-ECDSA-P256-SHA256` names 'a v4 OpenPGP binary-document signature whose document is the frame, ECDSA P-256, SHA-256' (G-57 kept). The pair id V1 issues (`:322-323`) names ML-DSA-65, pure mode, empty context (rule R) in slot `kms` and that OpenPGP scheme (rule O) in slot `gpg` (§5.2; HYBRID-SUPPLEMENT §1)." Kind K |
139: | 12 | **K-R.** `formal/p8/HYBRID-SUPPLEMENT.md:61-64`, `:152-153`, `:173-174`, `:524`, `:533`, `:274-276` (the supplement's copy of the E§5.2 replacement text); `formal/p8/ENCODING-V1.md:557-559` (c004, c008, c011, c097, c108; A11X-01) | :61 "it is the issuer's only path"; :63-64 "the issuer always computes `μ` … and sends `μ`"; :152-153 "Every issuer KMS `Sign` call on the key is `MessageType EXTERNAL_MU`, with `μ` computed by the issuer from such an `F`"; :173-174 "(K-R) is an issuer-code and IAM assumption: the key policy grants `kms:Sign` only to the issuer role, and the issuer code builds only V1 frames"; :524 "the issuer always uses EXTERNAL_MU for the kms slot, attestations and possession alike"; :533 "`kms:Sign` only for the issuer role"; ENC:557-558 and its copy at supplement :274-275 "The issuer obtains `S_kms` (attestation and possession) from KMS with `MessageType EXTERNAL_MU` only, sending μ" | In each sentence, the actor that computes `μ` and calls `kms:Sign` is the KMS-slot policy signer (`service/signer-kms/`). It runs in the issuing AWS account under its own IAM role. It computes `μ` only from an `F` it has validated: tag, alg, key fingerprint, ε (attestation frames only; manifests carry no declared time, HYBRID-SUPPLEMENT:495), `sign_by`, the signing stop (`service/signer-kms/tessera_sign_kms/signer.py:176-185`). Its role is the only `kms:Sign` principal, and the issuer roles hold no KMS permission (`service/signer-kms/infra/main.tf:33-34`; `service/issuer/infra/main.tf:181`). :173-174 reads: "(K-R) is a signer-code and IAM assumption: the key policy grants `kms:Sign` only to the KMS-slot policy signer's role, and that signer signs only V1 frames it has validated." **The (K-R) restrictions are unchanged** (:151-153, :157): the key signs only V1 tagged strings, in pure mode with the empty context, and is used by no other protocol or service. Only the actor that enforces them changes, so the wording of :152-153 changes as stated. The historical capture labels "selected issuer path" and "issuer-computed μ" (:76, :353, :412, :478) describe the 2026-10-13/14 captures and still fit (A11X-01, A11X-05). EXTERNAL_MU only, for attestations and possession alike, is unchanged. The verifier side is unchanged. Kind R |
140: | 13 | `formal/p8/HYBRID-SUPPLEMENT.md:154-155` (c121) | "They satisfy the same assumption, because the message is a V1 tagged string." | "The genuine-frame RAW captures (SIG-G1, P-G1) satisfy the same assumption. SIG-H5 (RAW) and SIG-H6 (EXTERNAL_MU) were made over spike frames tagged `tessera-v1/receipt`, which is not in T (:344-345), under the spike key. That key is never a production key and is deleted under §11 item 6 (§A11.5 item 3), so (K-R) for the production key is unaffected." Kind K |
141: | 14 | `270ca49:docs/V1-PROFILE.md:1244-1245` (c041, d3) | "one attacker key in both slots, honest DNS evidence, `git` absent: `INVALID / DNS_KEY_MISMATCH` (row 15.1)" | "Under the pair id: the attacker's own key of the right type in each slot (ML-DSA-65 SPKI in kms, P-256 v4 body in gpg; :1064-1065), with consistent manifest, possession and signatures, honest DNS evidence, `git` absent: `INVALID / DNS_KEY_MISMATCH` (row 15.1), dominating `UNVERIFIABLE / MEMBER_MISSING:git`." The A9.1 outcome, INVALID, is unchanged. The fixture bytes are regenerated. Kind K (fixture only) |
142: | 15 | `270ca49:docs/V1-PROFILE.md:1029` (custody record) | "HYBRID-SUPPLEMENT §9 item 6", a stale locator | `formal/p8/HYBRID-SUPPLEMENT.md` §11 item 6, the spike-key sentence at :525-526. The frozen bytes are unchanged; this corrects the locator only |
143: 
144: ## A11.4 Dependency duty for registered decisions
145: 
146: When a registered decision changes a parameter (an algorithm, a custody form, a channel, a horizon, a scope, a key),
147: the owner sweeps the registered texts for sentences whose referent the change alters. Each one is recorded as
148: amended, superseded, still fitting or open, before the decision's change is treated as complete. An owner decision
149: that touches a registered parameter is checked against those texts before it is recorded.
150: 
151: ## A11.5 Results of the first sweep (2026-10-28)
152: 
153: The sweep covered the original, Amendments 1–10, the freeze, the tracker and the author-rulings files
154: (`docs/reviews/stale-dependencies/SWEEP-2026-10-28.md`). The owner checked each finding against its source. The
155: review added item 3. The sweep did not read the rest of the frozen specification or the hybrid supplement
156: (`SWEEP-2026-10-28.md:3-4`, `:20-21`). The Levadura panel read them. Its findings are §A11.3 rows 1, 2, 4–6, 8 and
157: 10–14, §A11.6 and §A11.7.
158: 
159: **Scope from now on.** Every sweep under §A11.4 reads the frozen specification object in full (`spec.bin`: A9, A10,
160: PROOF, V1-PROFILE, ENCODING-V1 and the hybrid supplement; `formal/freeze-v1/FREEZE-RECORD.md:16`), as well as the
161: original, every amendment, the freeze record, the tracker and the author-rulings files.
162: 
163: 1. **H3 (`phase-0-prereg.md:232-248`): not amended.** H3 is a hypothesis with a stated falsifier. Its examples are
164:    AWS-based, but they do not restrict it to AWS. It is measured over the whole deployed system, every provider
165:    included. A measurement protocol is recorded before measurement. It covers retained resources (including the
166:    compliance-locked trail bucket), defines the demonstration and idle periods, and reports the three numbers
167:    separately. A slot-2 signer and an issuer poller that run through the operating window conflict with "idle
168:    compute exactly $0". If that or another number fails, H3 is reported as falsified. The operating window is not
169:    redefined as a demonstration to avoid this.
170: 2. **The slot-2 enforcement boundary: an owner decision (Option 1), adopted by the author's signature.** A9.6 requires the final custody implementation to
171:    be deadline-qualified (`phase-0-prereg-amendment-9.md:389-392`). The frozen record keeps "the selected,
172:    deadline-qualified custody implementation" (`270ca49:docs/V1-PROFILE.md:1024-1025`). It describes it through
173:    `prototype/policy-signer/` (:1033-1037), which met the deadline on 2026-10-14 (:1038-1040; §14.2 item 5,
174:    :1429-1435). That qualification stands as historical evidence.
175: 
176:    Production cannot run the prototype. Instrument code under `prototype/` stays instrument code, and service code
177:    that ports it must earn its own evidence on its own bytes (`formal/freeze-v1/FREEZE-RECORD.md:62-64`). Nothing an
178:    instrument produces discharges an obligation (A9:198-200). The E9 ruling R5b (`docs/reviews/e9-packet/AUTHOR-RULINGS.md:54`)
179:    allows porting instrument code with evidence earned on the resulting bytes. It does not address A9.6's
180:    deadline-qualified custody, so it does not settle this question. The registered texts do not say whether a
181:    post-deadline port counts as "the selected, deadline-qualified custody implementation". Each reading keeps a
182:    different registered text. A choice is needed, and the relaxation it makes needs the author's signature.
183: 
184:    > **OWNER DECISION FOR THE AUTHOR'S SIGNATURE (2026-10-29): Option 1.** Asked whether this is irreversible or
185:    > scope-changing, the owner answered no to both for Option 1. It changes no V1 scope. The practical lock-in is
186:    > the first production receipt under the hybrid keys, at deployment, not this text, and a later amendment can
187:    > revisit it before then. Option 2 is the scope change (it drops PQ and amends the freeze) and buys no claim V1
188:    > makes. The authority Option 1 needs is the author's signature on this amendment. **Signing adopts Option 1.**
189:    > If the author disagrees, the text changes before signing. Both options are kept below as stated before the
190:    > choice.
191:    >
192:    > **Option 1: the custody implementation is the custody option and boundary (port permitted; keeps the hybrid).**
193:    > A signed row says the A9.6 deadline qualification (A9:389-392; `270ca49:docs/V1-PROFILE.md:1024-1025`,
194:    > `:1429-1435`) attaches to the selected custody option and boundary: GCP Cloud KMS HSM, P-256, non-exportable,
195:    > behind a queue-pulling policy signer with the A9.6 checks (A9:382-388). The 2026-10-14 instrument run evidenced
196:    > that option, and A9.2 lets an instrument select among registered branches (A9:198-199). Production runs the
197:    > service port `service/signer-gcp/`, provided that before the first shipped receipt:
198:    > - (i) it preserves **every A9.6 custody and policy requirement**: complete-frame validation; the declared-time
199:    >   check on its own clock before signing; the issuing account able to enqueue but not to invoke the key, change
200:    >   the policy or clock, or obtain key-use credentials; and the key dedicated to V1 type-0x00 documents. It also
201:    >   preserves every property in the frozen custody record (`270ca49:docs/V1-PROFILE.md:1017-1040`) except the
202:    >   identity of the implementation, its 2026-10-14 deadline evidence and its prototype paths, which this option
203:    >   replaces;
204:    > - (ii) the external custody record names the deployed implementation, its image digest and its configuration;
205:    > - (iii) deployed evidence is earned on the new bytes. That means: a deployed positive signature that verifies
206:    >   offline; deployed refusals for a malformed frame, a wrong tag, a wrong alg, a wrong fingerprint and a declared
207:    >   time outside ε; a review of every principal that can cause a signature or administer the signer
208:    >   (`service/issuer/DEPLOY.md` step 8); and verified retirement of every other signing path (step 7);
209:    > - (iv) all of it identifies the tested image and configuration.
210:    >
211:    > This keeps FREEZE-RECORD.md:62, A9.2 and A9.6's custody and policy requirements. It overrides the code-identity
212:    > reading of "the selected, deadline-qualified custody implementation" (profile :1024-1025) and of A9.6's "final
213:    > custody implementation" (A9:389-390). Cost: it is a retrospective relaxation, made after the deadline and after
214:    > the candidate code existed. It is disclosed as such in the header.
215:    >
216:    > **Option 2: the code-identity reading is kept (A9.6 fallback).** No port can be deadline-qualified, and the
217:    > prototype cannot run production, so the hybrid's custody condition cannot be met. A9.6's own consequence
218:    > applies: "otherwise the registered fallback is taken" (A9:391; cut order A9:211-212). That is classical P-256
219:    > in both slots (A9:372-374), with slot 2 still under A9.6 custody through a ported service signer. The fallback
220:    > has no 21 Oct custody deadline. This keeps A9.6, A9.2 and FREEZE-RECORD.md:62 literally. Cost: it drops the PQ
221:    > slot. A9:346-350 records PQ as the author's stated preference, not a claim requirement, and the first item cut.
222:    > It changes the frozen catalog's `alg` (`formal/freeze-v1/objects/catalog.json`; FREEZE-RECORD.md:16, :20), so
223:    > the freeze must be amended or redone before issuing. The 2026-10-16 hybrid registration becomes moot.
224:    >
225:    > Chosen: **Option 1**, by the owner, adopted by the author's signature on this amendment.
226: 
227:    **Why the owner chose Option 1.** It keeps every custody and policy requirement and re-earns all evidence on the
228:    bytes that run. Option 2 keeps the deadline text literally but gives up the author's stated preference and
229:    reopens the freeze. Until this amendment is signed, issuance does not start (§A11.7, `service/issuer/DEPLOY.md`
230:    step 0).
231: 3. **The spike keys (`formal/p8/HYBRID-SUPPLEMENT.md` §11 item 6, :524-526).** The spike-key sentence (:525-526)
232:    is **unchanged**: "Both spike keys are deleted after the re-capture verifies, once the review clears." The
233:    item's first sentence (:524), "the issuer always uses EXTERNAL_MU for the kms slot", is changed by §A11.3 row 12
234:    (K-R). The owner's deployment draft (2026-10-27) reused the spike keys as production keys. That contradicted
235:    this commitment, and the draft is withdrawn. Production uses new keys (`service/issuer/DEPLOY.md`), recorded in
236:    the external custody record before use.
237: 4. **A dangling cross-reference (`phase-0-prereg-amendment-10.md:675`).** Row 25 does not apply to V1 (E9 row 2,
238:    2026-10-23; §A11.3 row 8). This is a CLARIFY: the fallback cites row 15 only (§A11.3 row 9).
239: 5. **K-R's enforcement (`formal/p8/HYBRID-SUPPLEMENT.md:61-64`, `:148-174`, `:524`, `:533`;
240:    `formal/p8/ENCODING-V1.md:557-559`): amended in wording, the assumption unchanged.** (K-R) itself stands: the
241:    ML-DSA-65 key signs only V1 tagged strings, in pure mode with the empty context, under EXTERNAL_MU, for no other
242:    protocol. What changes is who enforces it. The supplement and ENCODING-V1 §5.2 name the issuer as the computer
243:    of `μ` and the issuer role as the only `kms:Sign` principal. In V1 as designed (deployment pending), a
244:    dedicated policy signer validates the complete frame (tag, alg, key fingerprint, ε for attestation frames only,
245:    `sign_by`, the signing stop) *before* computing `μ`. Manifests carry no declared time, so ε does not apply to
246:    possession signing (HYBRID-SUPPLEMENT:495; `service/signer-kms/tessera_sign_kms/signer.py:180-184`). The
247:    signer's role is the only `kms:Sign` principal (`service/signer-kms/`; key policy in
248:    `service/signer-kms/infra/main.tf`). This narrows what a captured issuer role alone can get signed. It does not
249:    change the supplement's stated limit: "whoever may call `kms:Sign` on the key can sign any message by computing
250:    `μ`" (:171-172). An administrator of the account can still grant that (`PutKeyPolicy`), which is C3.
251: 
252: ## A11.6 Clarifications
253: 
254: These are readings, not changes. Each narrows or clarifies only and adds no claim.
255: 
256: 1. **ENCODING-V1 §5.2 rule O *Reasons* (c021). Narrowing.** "ENCODING-V1 §5.2 rule O *Reasons*
257:    (`formal/p8/ENCODING-V1.md:538-544`) record the 2026-10-12 GnuPG observation that motivated the legacy-header
258:    form. Rule O itself is unchanged. Under the pair id, the gpg slot's packet is assembled by the slot-2 policy
259:    signer (profile §8 custody record, `270ca49:docs/V1-PROFILE.md:1033-1036`), and it is a Tessera-assembled packet
260:    held to the same form as :541 requires. :541's 'KMS slot's packet' describes the classical id only, because
261:    under the pair id the kms slot emits rule R and has no packet."
262: 2. **W1 and receipt identity (c033). Clarifying.** "Profile §6 W1 (`270ca49:docs/V1-PROFILE.md:850-851`) 'is not an
263:    identifier' has the sense of its cited source ENC §3.5 (`formal/p8/ENCODING-V1.md:400-402`): no semantic,
264:    standing or attempt identifier, and no identifier of the statement, is derived from signature bytes. §9's 'A
265:    receipt's identity is SHA256(A_sig)' (:1183-1187) is an exact-bytes identity for deduplicating and referring to
266:    one receipt's claim-bearing bytes. Two receipts of one statement with different valid signatures are different
267:    receipts. Neither text widens the other."
268: 3. **"Both OpenPGP adapters" (c056). Narrowing.** "Profile §6 issuer duties 'Both OpenPGP adapters'
269:    (`270ca49:docs/V1-PROFILE.md:386-387`) and 'both OpenPGP adapters and the repository signer' (:392-393) mean
270:    every OpenPGP signer in use. Under the pair id that is the gpg slot's policy signer (and the repository signer).
271:    The kms slot emits rule R, to which the rule-O policy does not apply. Both apply under the classical id."
272: 
273: **Not confirmed: c145.** It read profile §14.2 item 1's "YubiKey 2 is not in hand" (`270ca49:docs/V1-PROFILE.md:1396-1397`)
274: as naming YubiKey 2 the release key. No text does. The runbook says the release key is "Not YubiKey 2"
275: (`docs/V1-OPERATIONS-RUNBOOK.md:125`). Nothing is needed.
276: 
277: ## A11.7 Owner-document repairs (not registered text)
278: 
279: These are owner documents. The owner makes each repair outside this amendment. They are listed so the record shows
280: where each one belongs.
281: 
282: - **c016.** `docs/V1-SERVICE-RESOLUTIONS.md:23` (S4): the 24-hour terminal FAILED conflicts with A2's
283:   `declared + δ + S` expiry (`phase-0-prereg-amendment-2.md:260-264`, 96 h at A9.2's values) and A9:422. S4 keeps
284:   "usually complete within 3 hours" as a non-guaranteed figure. A request ends only by the registered lifecycle:
285:   COMPLETE, or REFUSED when its N attempts are exhausted (A2.3). The issuer had no attempts, no latch and no
286:   refusal, so this is more than an edit. The owner's design is `docs/decisions/2026-10-29-issuance-lifecycle.md`,
287:   reviewed in `docs/reviews/issuance-lifecycle/`. This amendment does not
288:   restate that design, which is still under review; the design document governs its own content. Whatever it
289:   settles must meet A2.1 and A2.3 as registered, including the latch that excludes expiry (A2.1 `:153-160`) and "every
290:   timely-eligible attempt ships" (`:143-145`). **Signing this amendment does not accept any residual the design
291:   states** (at present, an on-time observation lost before it is persisted, followed by permanent loss of the
292:   evidence, which could end in refusal). Such a residual is assessed in the lifecycle work, against the registered
293:   text, and needs its own author decision if it remains. Matching edits: CL-03 items
294:   1 and 2 (`docs/V1-CLARIFICATIONS.md`), the clock-tolerance decision, `service/issuer/DESIGN.md`, and the issuer
295:   code and tests (inventory in the design). A shorter hard bound needs a signed amendment (A2.1 `:139-142`).
296: - **c036.** `service/issuer/DEPLOY.md`: a gate before the session's first step makes the whole deployment wait for
297:   the §A11.5 item 2 ruling, recorded in this amendment's signed text. Until then, issuance cannot start. No prototype fallback is added. Under Option 2, steps 5–7 and the key section are
298:   rewritten for the classical fallback.
299: - **c093.** `formal/PROPERTIES.md:167-168`: add S, and record that for `tessera-v1-strict` all five parameters were
300:   ratified by the author's signature on A9 (A9:223-225). The Band 0 exit item stays open outside V1 (§A11.3 row 4).
301: - **c136.** `docs/V1-SERVICE-RESOLUTIONS.md:26` (S7): replace "(H3)" with a cost derived from H3's three
302:   measurements, stated with its derivation. Per-receipt cost is not an H3 number (`phase-0-prereg.md:232-248`).
303: 
304: Repairs to this draft itself, applied above: c004 (row 12's locators and item 5's range), c030 (Option 1 condition
305: (i)), c055 (§A11.2 item 2's counts), c062 (row 7's sources), c097 (item 3), c108 (ε in row 12 and item 5), and
306: c006 (the barred prototype default removed from item 2).

=== FILE (modified; diff hunks, + lines are new): docs/reviews/OWNER-PRECHECKS.md
diff --git a/docs/reviews/OWNER-PRECHECKS.md b/docs/reviews/OWNER-PRECHECKS.md
index 88bb6a6..c4dc691 100644
--- a/docs/reviews/OWNER-PRECHECKS.md
+++ b/docs/reviews/OWNER-PRECHECKS.md
@@ -18,3 +18,5 @@
 4. **Binding text.** For every sentence the document treats as a requirement, is it registered (a signed amendment,
    the freeze, or a recorded author ruling), or is it something an instance wrote? An unregistered sentence used as a
-   requirement is FAIL. Since 2026-10-27, `docs/V1-SCHEDULE.md`'s ruling budget is a known instance of this.
+   requirement is FAIL. Since 2026-10-27, `docs/V1-SCHEDULE.md`'s ruling budget is a known instance of this. Also FAIL: an owner
+   requirement (a resolution, a design document, a code constant) that contradicts a registered sentence. Since
+   2026-10-29, S4's 24-hour FAILED against A2.3's per-attempt `declared + δ + S` expiry is the known instance.


=== FILE (new): docs/reviews/amendment-11/CODEX-CONFIRM-CONSOLIDATED.md
1: **Verdict: not ready for the author’s custody ruling and signature.** One further row-8 dependency omission remains. The pending owner repairs in A11.7 are acknowledged and are not a blocker.
2: 
3: Reviewed read-only; scratch used only `/tmp/tmp.8v3aby2ZaX`. No repository edits or git writes.
4: 
5: | Finding | Status | Repair evidence |
6: |---|---|---|
7: | A11X-01 | **CLOSED** | [A11:127](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:127) includes supplement:274–276 and classifies the historical capture labels as still fitting. |
8: | A11X-02 | **CLOSED** | [A11:123](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:123) explicitly supersedes all three identified passages and states that attacker-key receipts pass after dual-channel capture. Further omission below. |
9: | A11X-03 | **CLOSED** | [A11:270](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:270) now says the latch excludes expiry, consistent with [A2:153–160](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:153). |
10: | A11X-04 | **CLOSED** | [A11:125](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:125) adds PROOF:485, scopes the claim to SHA-1 reliance, and preserves the implementation-B observation. |
11: | A11X-05 | **CLOSED** | [A11:127](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:127) names the unchanged restrictions, corrects the locators, and explicitly changes the enforcement actor. |
12: | Paraphrase labelling | **CLOSED** | [A11:110–112](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:110) labels rows 3, 4, 7 and 8 as paraphrases, reserving exactness for quoted words. |
13: 
14: **A11XC-01 — High: row 8 still misses A10’s closing summary and outstanding listing work.**
15: 
16: [A11:123](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:123) does not dispose of:
17: 
18: - [A10:795–799](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-10.md:795): the listing adds mechanisms, and option (e) “deliberately rejects new cases: receipts under unlisted keys.”
19: - [A10:810–812](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-10.md:810): listing evidence, classifier subchecks and C0/C1 bootstrap remain listed as reconciliation work.
20: 
21: The frozen copies occur at [spec.bin:2821–2825](/home/tony/projects/tessera/formal/freeze-v1/objects/spec.bin:2821) and [spec.bin:2836–2838](/home/tony/projects/tessera/formal/freeze-v1/objects/spec.bin:2836).
22: 
23: Extend row 8 to preserve these as adoption history while superseding the listing claims and implementation duties for V1. This follows [A11.4:134–137](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:134); it does not require rewriting historical frozen bytes.
24: 
25: The repeat grep covered the requested preregistrations, `formal/p8/*.md`, `formal/freeze-v1/`, and the profile obtained with `git show 270ca49:docs/V1-PROFILE.md`.
26: 
27: - **Row 10:** no further undisposed requirement found. Frozen profile:1092 repeats “never read,” but :1103–1114 already supplies structural validation and an explicit dated correction. The quotation inside that correction is historical. PROOF’s two occurrences are covered by repaired row 10.
28: - **Row 12:** no further operative actor assignment found outside its repaired inventory. Supplement:22 is the dated HS-05 revision summary; the `HYBRID-SUPPLEMENT-DRAFT.md` matches are the historical draft. Frozen `spec.bin` also contains the inventoried source passages; those are frozen copies of the same requirements, not additional independent rules.
29: 
30: | Owner precheck | Result | Evidence |
31: |---|---|---|
32: | Capture row | **FAIL** | Row 8 leaves A10:797–798’s rejection promise undisposed: A11XC-01. It conflicts with [V1-CONTRACT:37](/home/tony/projects/tessera/docs/V1-CONTRACT.md:37) and :72. |
33: | Trigger clause | **PASS** | [A11:123](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:123) grounds the listing cut in the author’s scope ruling; :198–205 makes the custody fallback conditional on Option 2; :270–271 excludes latched attempts from expiry. |
34: | Requester | **PASS** | [A11:180–190](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:180) addresses queue access and principals causing signatures; :225–232 addresses direct KMS permission and administrative bypass. |
35: | Binding text | **PASS** | [A11:259–273](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:259) identifies owner documents, rejects S4’s conflicting deadline, and preserves registered latch protection. Pending repairs are not represented as completed or governing exceptions. |
36: 

=== FILE (new): docs/reviews/amendment-11/CODEX-CONFIRM-DECISION.md
1: **Verdict: not ready for the author’s signature.**
2: 
3: - **A11D-01 — FAIL: stale choice wording remains.** [A11:227–230](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:227) still says “a recommendation, not a decision” and “Until the author rules,” contradicting the new owner decision. Also update “If the author picks Option 1” at [line 17](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:17). No custody-choice blank remains. “Deployment pending” at line 243 describes deployment status and is appropriate.
4: 
5: - **A11D-02 — PASS: disclosure and authority preserved.** The retrospective relaxation, its post-deadline timing and already-written candidate code remain disclosed. The decision block explicitly requires the author’s signature; [DEPLOY step 0](/home/tony/projects/tessera/service/issuer/DEPLOY.md:39) gates deployment on signing. The owner’s decision alone does not amend registered text.
6: 
7: - **A11D-03 — PASS: Option 2 remains accurate.** Its substantive description is unchanged: classical P-256 in both slots, retained slot-2 custody, no hybrid custody deadline, and an amended or rebuilt freeze before issuance. Row 7 identifies it as the alternative not taken.
8: 
9: - **A11D-04 — PASS: no other A11 changes found.** Compared the complete amendment captured in the preceding `codex-confirm-item4.log` with the current file: differences are confined to the named custody edits. DEPLOY’s tracked diff adds only step 0; its previous wording was not available as a complete snapshot for an exact comparison.
10: 
11: No repository files or git state were written.
12: 

=== FILE (new): docs/reviews/amendment-11/CODEX-CONFIRM-ITEM4.md
1: **Verdict: ready for the author’s custody ruling and signature.** No blocking finding in the three edits.
2: 
3: - **A11I4-01 — PASS, c016.** [A11:279–288](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:279) accurately identifies the residual in the [lifecycle design:68–76](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:68). It preserves A2.1/A2.3 as governing requirements and explicitly prevents A11’s signature from accepting that residual. This confirms the boundary, not the lifecycle design’s conformance.
4: 
5: - **A11I4-02 — PASS, deployment gate.** [c036:289–291](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:289) and [DEPLOY:39–45](/home/tony/projects/tessera/service/issuer/DEPLOY.md:39) correctly require the signed custody ruling before deployment. Both respect the ruling’s alternatives and [FREEZE-RECORD:62–64](/home/tony/projects/tessera/formal/freeze-v1/FREEZE-RECORD.md:62). DEPLOY requires rewriting all steps under Option 2; c036’s narrower list does not exempt the remaining steps.
6: 
7: - **A11I4-03 — PASS, operational triggers.** [Item 4:95–109](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:95) retains mandatory reruns, records and operator attestation. It explains each trigger’s purpose and labels the calendar interval as an operating guess with a review point. These are operational duties proposed for adoption, not registered results or guarantees of detection. No claim is widened, and no contradiction with A11’s bounded evidence or discharge conditions was found.
8: 
9: - **A11I4-04 — Additional change identified.** Comparing the complete A11 snapshot captured in `codex-confirm-row8.log` with the current file found only the three described edits **plus** [row 8:134](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:134): `:462-579` became `:462-611, all of A10.4.1`. This locator correction was already disclosed in [DISPOSITION:114](/home/tony/projects/tessera/docs/reviews/amendment-11/DISPOSITION.md:114). Nothing else changed.
10: 
11: Owner prechecks, applied to these edits:
12: 
13: | Check | Result | Evidence |
14: |---|---|---|
15: | Capture row | **PASS** | A11:95–109, 279–291 add no attacker-key rejection or capture-visibility promise; consistent with V1-CONTRACT:37, 52–53, 72. |
16: | Trigger clause | **PASS** | A11:183–218, 289–291 and DEPLOY:39–45 leave the ruling pending; neither option’s consequence is activated prematurely. |
17: | Requester | **PASS** | DEPLOY:41 incorporates ruling conditions (i)–(iv), including enqueue versus key-invocation authority and review of every principal able to cause signing (A11:191–202). |
18: | Binding text | **PASS** | A11:281–288 subordinates the owner design to registered A2 requirements; item 4 remains an explicitly proposed duty; DEPLOY:39–45 waits for signed authority. |
19: 
20: Review was read-only; scratch was confined to a fresh `mktemp -d`.
21: 

=== FILE (new): docs/reviews/amendment-11/CODEX-CONFIRM-ROW8.md
1: **Verdict: ready for the author’s custody ruling and signature; A11.7’s pending owner repairs are not a blocker.**
2: 
3: - **A11R8-01 — CLOSED: A11XC-01.** [Row 8](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:123) now explicitly supersedes A10:795–799’s listing mechanisms and rejection promise, withdraws the listing-related reconciliation duties at :810–812, and covers their frozen `spec.bin` copies.
4: 
5: - **A11R8-02 — Independent search: no undisposed hit found.** I searched the original, A1–A10, every `formal/p8/*.md`, all of `formal/freeze-v1/` with binary-as-text searching, and the profile extracted with `git show 270ca49:docs/V1-PROFILE.md`. Independent terms included broad `list/listed/listing`, `pre-commit`, `pre-publish`, allowlist/whitelist, authorized keys, key sets, registries and schedules, alongside the reason codes. All relevant positive listing requirements are disposed by row 8 or the frozen profile’s §5 cut. This includes A10:582–610: although beyond row 8’s expressly inventoried :462–579 range, these remain within **A10.4.1**, which row 8 supersedes wholesale for V1. DNSSEC rollover, release allowlisting and git-assertion pre-commitment are separate retained checks.
6: 
7: - **A11R8-03 — Repair scope: consistent with the previous finding.** Compared with the prior review’s description, row 8 adds the requested closing-summary and reconciliation dispositions, plus adoption-history and frozen-copy coverage. I found no unrelated substantive change within that repair. **Without the prior amendment snapshot, I cannot establish that nothing elsewhere in the amendment changed.**
8: 
9: Repository read-only; no git writes. Scratch used only `/tmp/tmp.yfA4hAyKqi`.

=== FILE (new): docs/reviews/amendment-11/CODEX-REVIEW-CONSOLIDATED.md
1: **Verdict: not ready for the author’s ruling and signature; fix the dependency omissions and lifecycle contradiction, then confirm the repairs.**
2: 
3: Reviewed the live **282-line** draft, all 15 change-table rows, the scorecard, all 28 disposition records and the prior confirmations. No repository edits or git writes were made. I did not read `levadura_salvaje/predictions/`.
4: 
5: ### Findings
6: 
7: **A11X-01 — High: the K-R row still leaves a frozen normative duplicate unchanged.**
8: 
9: Location: [A11:126](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:126).
10: 
11: Row 12 changes ENCODING-V1:557–559 but misses the same rule in [HYBRID-SUPPLEMENT:274–276](/home/tony/projects/tessera/formal/p8/HYBRID-SUPPLEMENT.md:274):
12: 
13: > The issuer obtains `S_kms` … from KMS … sending
14: 
15: That is inside §7’s **exact replacement block**, not merely a record of an experimental capture. Under A11’s component-specific meaning of “issuer,” it retains precisely the actor assignment row 12 replaces. This repeats the dependency defect A11.4 addresses.
16: 
17: **Fix:** add supplement:274–276 to row 12, replacing the actor consistently while retaining the formula and verifier behavior. Explicitly classify the historical “issuer-computed μ” capture descriptions as historical and still fitting.
18: 
19: **A11X-02 — High: the E9-cut row misses A10’s plain-language protection claims.**
20: 
21: Location: [A11:122](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:122).
22: 
23: Row 8 accounts for the adoption, mechanism section and change-table rows, but leaves these registered restatements outside its source inventory:
24: 
25: - [A10:106–124](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-10.md:106): the verifier rejects unlisted keys; the mechanism stops scoped users accepting attacker receipts; holders preserve listing evidence.
26: - [A10:213–226](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-10.md:213): the listing adds checks, reason codes, issuer duties and protection.
27: - [A10:432](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-10.md:432): row 26 replaces the boundary sentence under option (e).
28: 
29: These remain misleading descriptions of the narrowed option (e). In particular, the plain-language rejection promise conflicts with V1-CONTRACT:37 and :72: captor-key receipts pass after both authority channels are captured.
30: 
31: **Fix:** extend row 8 with explicit dispositions for these passages. Preserve the dated adoption history and author quotations; supersede the passages describing the listing as a current V1 mechanism. State that no listing rejection, precommitment or preservation duty remains in V1. Keep release-key independence separate.
32: 
33: **A11X-03 — High: A11 introduces an impermissible latch override.**
34: 
35: Location: [A11:268–269](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:268).
36: 
37: The phrase “a latch that expiry can override only by re-observing the chain evidence” permits expiry of a latched attempt. [A2:153–160](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:153) expressly forbids that: expiry applies only to attempts without timely-latched eligibility.
38: 
39: The cited owner design agrees with A2: [design:49–56](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:49) first requires finding the attempt **not latched**, then requires re-observation and a conditional write.
40: 
41: **Fix:** replace the phrase with:
42: 
43: > a latch that excludes expiry; expiry of an unlatched attempt requires re-observing the chain evidence and an atomic check that no latch intervened
44: 
45: No registered relaxation is needed.
46: 
47: **A11X-04 — Medium: the fingerprint correction misses PROOF’s second “no check reads it” statement.**
48: 
49: Location: [A11:124](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:124).
50: 
51: Row 10 correctly repairs PROOF:134–135, but [PROOF:485](/home/tony/projects/tessera/formal/p8/PROOF.md:485) still says:
52: 
53: > No check reads it, and B never computes it.
54: 
55: The profile structurally checks the fingerprint bytes, including cross-field consistency. The historical implementation-B statement can remain if accurate; the unqualified “No check” needs its scope stated. Otherwise the consolidated repair leaves the same contradiction elsewhere in the frozen proof.
56: 
57: **Fix:** add :485 to row 10, distinguishing V1 structural validation from SHA-1 security reliance and from the recorded vector-checker behavior.
58: 
59: **A11X-05 — Low: row 12’s “unchanged assumption” locator contradicts its own edit.**
60: 
61: Location: [A11:126](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:126).
62: 
63: “The (K-R) assumption itself (:151–152, :156) is unchanged” includes the beginning of the very sentence whose actor changes; :156 is blank. The no-other-context/protocol restriction is at :157.
64: 
65: **Fix:** say that the **allowed-message, pure-mode, empty-context and exclusive-key-use restrictions** remain unchanged, citing :151–153 and :157, while the enforcement actor changes. Avoid declaring the source wording unchanged.
66: 
67: ### Change-table audit
68: 
69: “Checked” below means the quoted source words match after Markdown/line-wrap normalization; explicit ellipses are omissions, not complete quotations.
70: 
71: | Row | Assessment |
72: |---|---|
73: | 1 | Checked. Appropriate V1 narrowing; correctly distinguishes non-exportability from misuse. |
74: | 2 | Checked. Extends A9’s existing narrowing to the §6 restatement. |
75: | 3 | **Was is a paraphrase**, not an exact quotation. Proposed fields, floor and discharge conditions are adequately identified. Label it “paraphrase” for precision. |
76: | 4 | Mixed paraphrase/exact excerpt. Four locations checked; V1 ratification and non-V1 preservation are correct. |
77: | 5 | Checked. Correctly removes issue-time authority/publication implications. |
78: | 6 | Checked. Correct signature-inclusive target; retains the surrounding identity-handle rule. |
79: | 7 | Mixed paraphrase/exact excerpt. All three custody/deadline locations are represented; replacement remains pending. |
80: | 8 | Mixed paraphrase/exact excerpts. Correct substantive cut and row-33 treatment; **incomplete dependencies, A11X-02**. |
81: | 9 | Checked. Correct once row 8’s cut is registered. |
82: | 10 | Checked. Correct replacement; **missed restatement, A11X-04**. |
83: | 11 | Source wording checked. Replacement correctly separates classical and pair identifiers. Inner quotation marks differ typographically. |
84: | 12 | Quoted excerpts checked. Actor replacement is bounded; **A11X-01 and A11X-05 remain**. |
85: | 13 | Checked. Correctly distinguishes genuine-frame captures from spike-tag captures; does not turn SIG-H5 into conforming production evidence. |
86: | 14 | Checked. Correct hybrid fixture description and reason precedence; preserves A9’s INVALID outcome. |
87: | 15 | Checked. Correct locator-only repair. |
88: 
89: Apart from the identified omissions, I found no additional sentence silently changed by these rows. The table should explicitly label its paraphrases rather than imply every Was cell is an exact quote.
90: 
91: ### Completeness, clarifications and author choice
92: 
93: All **28 disposition IDs appear in A11**. That includes the explicitly unconfirmed c145; no confirmed or partial disposition lacks a corresponding row, clarification, draft correction or owner repair.
94: 
95: The owner repairs are **listed, not completed**. Live S4 still contains the 24-hour FAILED rule; DEPLOY steps 6–7 remain unconditional; PROPERTIES still omits S; S7 still attributes per-receipt cost to H3. A11.7 largely acknowledges their pending status. These should not be reported as implemented repairs.
96: 
97: All three A11.6 readings are acceptable:
98: 
99: - Item 1 preserves rule O and interprets its rationale for the hybrid.
100: - Item 2 reconciles statement identity with exact receipt identity using ENC’s existing qualification.
101: - Item 3 applies OpenPGP duties to the OpenPGP signers actually in use, preserving rule R for kms.
102: 
103: Neither custody option offers production use of prototype code. Option 1 accurately identifies the retrospective deadline relaxation and requires evidence on service bytes. Option 2 accurately retains classical fallback custody, has no hybrid custody deadline and requires freeze reconciliation. PQ is correctly described as the author’s preference rather than a C-row requirement. The owner recommendation is visibly separate from the pending author decision.
104: 
105: The outcome disclosures are materially adequate: they expose the late checklist repair, retrospective custody relaxation, prior K-R misstatement and withdrawn spike-key reuse. Row 13 preserves the historical capture defect, and row 14 preserves the registered verdict. I found no undisclosed conversion of a failed historical result into a pass. Preserve that distinction when regenerating the fixture.
106: 
107: ### §A11.2 verification
108: 
109: **PASS.** Compared with the amendment text embedded in `codex-confirm-4.log`, only the owner-harness count/coverage paragraph changed; the requirements and limitations are unchanged.
110: 
111: All **15 manifest entries verify**. The manifest hash matches A11:70 exactly:
112: 
113: ```text
114: 844cb7ff8df59f047d2ea48536ddb30bad5b3e93684acbce6a4dad1241aee42d
115: ```
116: 
117: The live profile also matches frozen commit `270ca49`. I did not rerun the test suite or establish deployment evidence; manifest verification does not discharge P3.
118: 
119: ### Owner prechecks
120: 
121: | Check | Result | Evidence |
122: |---|---|---|
123: | Capture row | **FAIL** | [A11:122](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:122) leaves A10:106–124’s rejection promises undisposed. A11X-02. A11’s direct fixture claim at :128 appropriately assumes honest DNS. |
124: | Trigger clause | **FAIL** | [A11:269](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:269) permits expiry despite a latch; A2’s expiry trigger requires no timely latch. A11X-03. |
125: | Requester | **PASS** | [A11:180](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:180), :188–189 and :224–231 address queue access, principals able to cause signing, direct key permission and administrative bypass. No claim rests solely on key storage. |
126: | Binding text | **FAIL** | [A11:269](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:269) describes an owner construction that contradicts registered A2 latch protection. The cited owner design itself correctly forbids that construction. |
127: 

=== FILE (modified; diff hunks, + lines are new): docs/reviews/amendment-11/DISPOSITION.md
diff --git a/docs/reviews/amendment-11/DISPOSITION.md b/docs/reviews/amendment-11/DISPOSITION.md
index 7c1dd20..e24d591 100644
--- a/docs/reviews/amendment-11/DISPOSITION.md
+++ b/docs/reviews/amendment-11/DISPOSITION.md
@@ -82,2 +82,81 @@ the check and named archive-manipulation techniques. It was re-run as two briefs
     `CodeSha256` is a V2 candidate.
 - The manifest was regenerated. The floor gives 1201 passed, 1 skipped.
+
+## Consolidated draft review (`CODEX-REVIEW-CONSOLIDATED.md`, 2026-10-29): owner disposition
+
+The draft was consolidated from the Levadura panel's 28 findings. The review found that all 28 are accounted for
+and the custody options are stated neutrally. It found three high findings, two of them the panel's own pattern
+again (a fix that leaves a copy of the text elsewhere unchanged), and three prechecks FAILED. All findings applied:
+
+| ID | Sev | Disposition |
+|---|---|---|
+| A11X-01 | High | The K-R row adds the supplement's copy of the E§5.2 sentence (`HYBRID-SUPPLEMENT.md:274-276`). The historical "issuer-computed μ" capture labels are stated to still fit. |
+| A11X-02 | High | Row 8 adds A10's plain-language passages (`:106-124`), its additions list (`:213-226`) and the row-26 note (`:432`). They are kept as the dated record of the 2026-10-18 adoption and superseded as descriptions of V1. In V1 no listing rejection, pre-commitment or preservation duty exists, and attacker-key receipts pass after capture of both channels (V1-CONTRACT §2, §4). |
+| A11X-03 | High | The owner's own c016 sentence said expiry could "override" a latch, which A2.1 forbids. It now says the latch excludes expiry and describes the revision-3 design (one writer; expiry only after B plus the lease, on fresh evidence). |
+| A11X-04 | Med | Row 10 adds `PROOF.md:485` ("No check reads it"), scoped as in :134-135. "B never computes it" stays. |
+| A11X-05 | Low | The K-R row no longer calls source wording "unchanged". The unchanged restrictions are named and cited (:151-153, :157), and the actor change is stated. |
+| Paraphrases | — | The table states that the "Was" cells of rows 3, 4, 7 and 8 are paraphrases; only quoted words are exact. |
+
+The owner repairs in §A11.7 remain listed, not done (the live S4 still has the 24-hour rule). They are done with the
+issuer lifecycle change.
+
+## Consolidated confirmation (`CODEX-CONFIRM-CONSOLIDATED.md`): owner disposition
+
+A11X-01 to -05 and the paraphrase labelling were CLOSED. A11XC-01 (High): row 8 still missed A10's closing summary
+(`:795-799`, "deliberately rejects new cases: receipts under unlisted keys") and the listing parts of the
+reconciliation item (`:810-812`). This was the fourth missed copy for the listing cut, so the owner did not repair
+it alone. The owner grepped every registered text (prereg, A1–A10, PROOF, ENCODING-V1, HYBRID-SUPPLEMENT,
+HYBRID-REGISTRATION-RECORD, FREEZE-RECORD, profile at `270ca49`) for the listing's vocabulary (`service_keys`,
+`SERVICE_KEYS_NOT_LISTED`, `unlisted`, `LISTING_`, `A10.4.1`, `key listing`, `listing evidence`, `listing
+pre-commit`). Every hit is now disposed by row 8: either named explicitly or covered as adoption history, the
+mechanism section or frozen copies. A9:157 and profile :531 ("unlisted rollover") are DNSSEC terms, unrelated.
+
+**Row-8 confirmation (`CODEX-CONFIRM-ROW8.md`):** A11XC-01 CLOSED; independent wider search found no undisposed hit. Ready for the author. Owner tidy: the mechanism-section range is corrected to `:462-611` (all of A10.4.1, which ends where A10.4.2 begins at :612).
+
+## Author's pre-signing Codex read (relayed by the author, 2026-10-29): owner disposition
+
+The author ran the draft by Codex before ruling. Codex leaned toward Option 1 and asked for two bounded corrections.
+Both are applied:
+- **DEPLOY.md gate.** A step 0 now makes the whole deployment wait for the §A11.5 item 2 ruling, recorded in the
+  signed amendment. It states what each option means for the steps, and that no option uses `prototype/` code.
+  A11.7 c036 is updated to match.
+- **Stale lifecycle summary in A11.7 c016.** The summary described revision 3 (expiry after the boundary plus the
+  write lease), while the design is now at revision 4 (expiry only on complete negative evidence, no lease timing).
+  The owner had revised the design twice after writing the summary. A11 now defers to the design document instead
+  of restating it. Following Codex's caution, it also says that **signing A11 does not accept any residual the
+  lifecycle design states**: such a residual is assessed in the lifecycle work against A2.1 and A2.3, and needs its
+  own author decision if it remains.
+
+Codex also noted that §A11.2 item 4 is a continuing operational duty: re-runs on every verifier or library change,
+every new upstream vector commit, and at least quarterly. This is stated in the amendment, and the author should
+weigh it as an ongoing cost, not a one-time approval.
+
+## Author's question on the operational triggers (2026-10-29): owner disposition
+
+The author asked whether §A11.2 item 4's triggers are the right boundaries or educated guesses. Owner assessment:
+- Code or library change is required: the evidence is bound to bytes.
+- "Every upstream vector commit" had the right purpose at the wrong grain: it now triggers only on files for the
+  algorithms in use.
+- "Quarterly" was a guess standing in for knowledge outside the vector suite. It is replaced by advisory and erratum
+  triggers, plus a calendar backstop labelled as an operating guess, to be reviewed on a year of run records.
+
+Item 4 is rewritten so that each trigger states what it detects. This is an unreviewed edit to the draft. The
+owner's confirmation runs before signing.
+
+A boundary candidate raised to the author, not added to A11: the verifier's DNSSEC signature checks (RSA alg 8,
+ECDSA P-256 alg 13, which ground G4) are inventoried but not profiled (`formal/p3-verification-profile/PROFILE.md:54-58`).
+No registered property asks for a verification profile for them.
+
+## Custody ruling as an owner decision (2026-10-29)
+
+The author asked whether the custody ruling is irreversible or scope-changing. Owner's answer:
+- Option 1 is neither. It changes no V1 scope. The practical lock-in is the first production receipt under the
+  hybrid keys, at deployment, and a later amendment can revisit it before then.
+- Option 2 is the scope change: it drops PQ and amends the freeze, for no claim V1 makes.
+
+So the choice does not need the author's separate ruling. It needs his signature, because Option 1 relaxes a
+registered reading, and signing A11 gives that. The ruling block, the header, §A11.5 item 2, change-table row 7 and
+DEPLOY step 0 now record Option 1 as the owner's decision, adopted by signing. Option 2 is kept as the alternative
+not taken, and the retrospective-relaxation disclosure is unchanged.
+
+**Decision-wording confirmation (`CODEX-CONFIRM-DECISION.md`):** A11D-01 (stale "recommendation, not a decision", "Until the author rules", "If the author picks Option 1") fixed; A11D-02 to -04 PASS. A grep for the stale phrasings finds none left.


=== FILE (new): docs/reviews/ceremony/BRIEF-CONFIRM.md
1: # Confirmation brief: key ceremony revision 2 (owner, 2026-11-02)
2: 
3: Your review `docs/reviews/ceremony/CODEX-REVIEW.md` (C01–C07) covered revision 1. `docs/ceremony/CEREMONY.md` is now
4: revision 2. Read-only except your report. For each of C01–C07, say whether revision 2 resolves it (cite lines), and
5: report any new defect revision 2 introduces, with severity and a concrete failing scenario. Pay particular attention
6: to: whether every S0–S9 command is correct for GnuPG 2.2.40 *and* 2.4.x (the author's Tails accepted `uif` and
7: enforced touch in the rehearsal, so it is probably a newer GnuPG; the procedure now records the version at S0 and
8: stops if fixed touch cannot be confirmed); whether `GNUPGHOME` is used consistently, including `keytocard`, the
9: revocation path and Session 2; and whether the failure table ever leads to losing the last usable copy.
10: Write to docs/reviews/ceremony/CODEX-CONFIRM.md.
11: 
12: # Owner prechecks, run by the reviewer
13: 
14: > **Status: OWNER PROCESS, 2026-10-27.** Every owner instance has written these down as lessons and then repeated
15: > the mistakes (the 2026-10-19 stone, and its 2026-10-27 postscript "Naming it did not stop it"). The author's
16: > answer to "what do new owners get wrong in their first week": *"that they will behave differently from the prior
17: > instances."* So these checks are not left to the owner's self-review. The owner appends this file verbatim to
18: > every review brief (Codex or another family), and the reviewer reports each check as PASS or FAIL with file:line.
19: 
20: ## Checks
21: 
22: 1. **Capture row.** For every plain-language statement of what holds, what happens when an attacker controls both
23:    authority channels (DNS and git)? If the text implies that the attacker's own keys are rejected, or that a
24:    capture is detected or made visible, that is FAIL. Ground truth: `docs/V1-CONTRACT.md` §2 (after G10) and §4.
25: 2. **Trigger clause.** For every registered rule cited as authority (an amendment section, a table row, a ruling),
26:    did the rule's trigger condition actually occur? Citing a consequence whose trigger has not happened is FAIL.
27: 3. **Requester.** For every security claim about keys or signing, who can cause a signature to be made? A claim
28:    that reasons only about where a key is stored, and not about who can submit work to the signer, is FAIL.
29: 4. **Binding text.** For every sentence the document treats as a requirement, is it registered (a signed amendment,
30:    the freeze, or a recorded author ruling), or is it something an instance wrote? An unregistered sentence used as a
31:    requirement is FAIL. Since 2026-10-27, `docs/V1-SCHEDULE.md`'s ruling budget is a known instance of this. Also FAIL: an owner
32:    requirement (a resolution, a design document, a code constant) that contradicts a registered sentence. Since
33:    2026-10-29, S4's 24-hour FAILED against A2.3's per-attempt `declared + δ + S` expiry is the known instance.

=== FILE (new): docs/reviews/ceremony/BRIEF.md
1: # Review brief: key ceremony revision 1 (owner, 2026-11-02)
2: 
3: Review `docs/ceremony/CEREMONY.md` in /home/tony/projects/tessera, read-only (write only your report). It is the
4: procedure the author will follow on an offline Tails session to create the V1 repository root (YubiKey A) and the
5: release key (YubiKey B). Context: `docs/V1-RELEASE-KEY-CUSTODY-DRAFT.md` (§5–§8, §11), `docs/V1-OPERATIONS-RUNBOOK.md`
6: §1, `docs/V1-PROFILE.md` §15.4 and §6.3, `docs/phase-0-prereg-amendment-10.md` row 34 (A10.4.2), and the rehearsal
7: record `docs/ceremony/2026-11-01-rehearsal-1.md` (Tails GnuPG + YubiKey 5 signatures passed the verifier's git
8: signature path).
9: 
10: Please check:
11: 1. **Correctness of each command** for Tails 6 (Debian 12, GnuPG 2.2.x) and a YubiKey 5 (OpenPGP 3.4): order of
12:    key-attr / keytocard / forcesig / uif; whether `keytocard` removes the local secret only on `save`; whether the
13:    revocation certificate path is right; whether any step leaves a plaintext secret on a persistent medium.
14: 2. **Gaps against the custody draft and registered text**: anything §6–§8 or A10.4.2 requires that this procedure
15:    omits or contradicts (for example the session conditions in §5, the custody record contents, the independence of
16:    A and B). Distinguish registered requirements from the owner's own choices.
17: 3. **Failure handling**: what the author should do if a step fails midway (e.g. keytocard fails after backups,
18:    a restore test fails, a PIN is entered wrongly), and whether the procedure says so.
19: 4. **The owner decisions listed in the document** (hardware mode, LUKS2 via Disks with one passphrase for both layers
20:    of one key's backups, KDF off, no expiry): any that weaken a stated property.
21: 
22: Report findings with severity, file:line and a concrete failing scenario; say plainly if a section is sound.
23: Write the report to docs/reviews/ceremony/CODEX-REVIEW.md.
24: 
25: # Owner prechecks, run by the reviewer
26: 
27: > **Status: OWNER PROCESS, 2026-10-27.** Every owner instance has written these down as lessons and then repeated
28: > the mistakes (the 2026-10-19 stone, and its 2026-10-27 postscript "Naming it did not stop it"). The author's
29: > answer to "what do new owners get wrong in their first week": *"that they will behave differently from the prior
30: > instances."* So these checks are not left to the owner's self-review. The owner appends this file verbatim to
31: > every review brief (Codex or another family), and the reviewer reports each check as PASS or FAIL with file:line.
32: 
33: ## Checks
34: 
35: 1. **Capture row.** For every plain-language statement of what holds, what happens when an attacker controls both
36:    authority channels (DNS and git)? If the text implies that the attacker's own keys are rejected, or that a
37:    capture is detected or made visible, that is FAIL. Ground truth: `docs/V1-CONTRACT.md` §2 (after G10) and §4.
38: 2. **Trigger clause.** For every registered rule cited as authority (an amendment section, a table row, a ruling),
39:    did the rule's trigger condition actually occur? Citing a consequence whose trigger has not happened is FAIL.
40: 3. **Requester.** For every security claim about keys or signing, who can cause a signature to be made? A claim
41:    that reasons only about where a key is stored, and not about who can submit work to the signer, is FAIL.
42: 4. **Binding text.** For every sentence the document treats as a requirement, is it registered (a signed amendment,
43:    the freeze, or a recorded author ruling), or is it something an instance wrote? An unregistered sentence used as a
44:    requirement is FAIL. Since 2026-10-27, `docs/V1-SCHEDULE.md`'s ruling budget is a known instance of this. Also FAIL: an owner
45:    requirement (a resolution, a design document, a code constant) that contradicts a registered sentence. Since
46:    2026-10-29, S4's 24-hour FAILED against A2.3's per-attempt `declared + δ + S` expiry is the known instance.

=== FILE (new): docs/reviews/ceremony/CODEX-CONFIRM.md
1: # Ceremony revision 2 — Codex confirmation
2: 
3: Reviewed 2026-11-02 against `BRIEF-CONFIRM.md`, including all four appended prechecks. **Revision 2 does not yet resolve C01–C07 completely. Revise before production key generation.** The isolation, acceptance and requester-boundary text is substantially improved. Remaining blockers concern fixed-touch readback and preservation of an untested last usable copy; fresh-boot instructions and bootstrap details also need completion.
4: 
5: Snapshot: HEAD `54b382cd308291cf92457ff640584fba51ffc02c`; working-tree `docs/ceremony/CEREMONY.md` SHA-256 `2bdb7dc0b7dd3223f4c37baa47fab568d066df6df71da05c7e6486d704c8ae9a`. Line references below are to that file unless another path is named. Review was read-only except this report. Pre-existing deployment changes and untracked ceremony material were preserved. No production card, key, PIN, backup or secret was accessed. This is document/source confirmation, not a hardware rehearsal or independence certification.
6: 
7: ## C01–C07 dispositions
8: 
9: | Finding | Revision 2 resolves it? | Evidence and residual |
10: |---|---|---|
11: | C01 — expert curve selection | **YES** | Lines 89–97 use `--expert --card-edit`, choose the displayed NIST P-256 entry, preserve other slots and require attribute readback. Empty algorithm input preserves the current attribute in the inspected upstream versions. |
12: | C02 — version and fixed touch | **PARTLY** | Lines 64,71 record GnuPG; lines 149–150 stop on unsupported/unconfirmed touch. This safely refuses 2.2.40 but does not make it compatible. New F01 below prevents the specified permanence readback on inspected 2.4 versions too. scdaemon/card firmware identification remains absent from the record at 197–200. The inference at 215–216 is plausible, not a measured version. |
13: | C03 — isolation | **PARTLY** | Lines 29,52–72 explicitly prohibit unlocking persistence, require independent image verification, identify the System76 and credential check, create a temporary RAM home, and check mounts/swap/network. Lines 168–174 reuse S0 on every test boot. No NUC script/configuration and no autorun conditions from custody draft §5 are still not stated explicitly. An overlay filesystem name alone does not establish that its writable layer is RAM. See command notes below. |
14: | C04 — backup/failure safety | **PARTLY** | Lines 119–121 now check export/copy exits and nonempty files; 135 and 176–177 gate transfer/acceptance; 186 protects PIN retries. But export success is not demonstrated recovery: F02 remains a last-copy failure path. The destination check is weak (F04), and fresh-boot recovery instructions remain incomplete (F03). |
15: | C05 — policy and primary tests | **YES at the procedural-design level**, subject to F01/F03 | Lines 145–150 read before toggling `forcesig`; 152–161 add no-touch and fresh-PIN tests, and count successful signatures; 172–177 require a fresh card-only test and reject unexpected outcomes. These are appropriate proposed tests. They have not been executed here; positive signing alone still proves neither fixed touch nor requester independence. |
16: | C06 — custody/bootstrap record | **PARTLY** | Lines 11–13 and 196–205 correctly distinguish secrets from public choices, record hardware/credential checks and results, independently compute the fingerprint and link the later bootstrap record to the freeze. Missing: a concrete authenticated initial-acquisition route, explicit retention of the approved public key outside the NUC, checks of actual published material, card firmware/scdaemon versions and protected export settings. See F05. |
17: | C07 — requester independence | **YES for this ceremony's bounded claim** | Lines 8–10 expressly defer production use until independent review, exact-hash approval and controlled input media are implemented and rehearsed; line 219 disclaims requester independence. The author supplies ceremony signing requests, while an operational channel captor could supply a malicious future release candidate. Storage/touch alone does not authorize those bytes. This resolves the overclaim by scope and handoff; it does not establish A10.4.2 independence. |
18: 
19: ## New defects and remaining concrete failure paths
20: 
21: ### F01 — HIGH, new: the required fixed-touch readback cannot distinguish fixed from ordinary on
22: 
23: **Lines 145–150,176.** In upstream GnuPG 2.4.4 and 2.4.8, human-readable card status prints `Sign=on` for both UIF value 1 (on) and value 2 (permanent). The command at 145 cannot produce the required permanent/fixed confirmation. The numeric colon output preserves the distinction.
24: 
25: Failing scenario: `uif 1 permanent` succeeds on a supported card, but the operator follows the readback literally and must stop despite correct configuration. If the operator instead accepts `Sign=on`, an ordinary on policy can pass this check; a no-touch timeout also cannot distinguish on from fixed. Preserve the stop condition and specify a rehearsed readback such as `gpg --with-colons --card-status`, requiring signature UIF value 2 (`uif:2:...`), together with successful policy setting. Do not attempt to disable touch as a negative test on the production card.
26: 
27: Evidence: upstream [2.4.4 card-util.c](https://github.com/gpg/gnupg/blob/gnupg-2.4.4/g10/card-util.c) and [2.4.8 card-util.c](https://github.com/gpg/gnupg/blob/gnupg-2.4.8/g10/card-util.c), status rendering and `uif`. This is source evidence, not a card observation.
28: 
29: ### F02 — HIGH, residual C04: failed transfer permits destroying the only demonstrated usable secret
30: 
31: **Lines 119–121,164,185,189–190.** The failed-transfer row says to shut down after one retry because the backups survive. They have only passed export/nonempty checks at that point; both recovery tests occur after shutdown. The successful path likewise shuts down before any backup has been restored, although a tested card can then supply a usable primary.
32: 
33: Failing scenario: both exports are present but cannot be decrypted with the retained passphrase, or their secret data cannot be restored; card transfer fails twice. Row 185 authorizes shutdown of the sole usable RAM key. The later discovery that both backups fail cannot recover that key. This is a conditional failure path, not an observation that GnuPG normally makes corrupt exports.
34: 
35: Before relinquishing the last demonstrated usable copy, validate recovery using isolated temporary keyrings/agents and only the candidate backup, while preserving the original key. Retain the separate fresh-boot tests for final acceptance. Do not justify shutdown after transfer failure by file existence alone. Distinguish “not yet tested” from “good” in row 189. If both backups fail but the card works, row 190 should explicitly preserve that card pending recovery or a deliberate abandonment decision; unusable backups do not imply the primary is unusable. No existing production key should be reset on this table's authority.
36: 
37: ### F03 — MEDIUM, new fresh-boot instructions lose their variables
38: 
39: **Lines 107,117,168–173.** S0 recreates `GNUPGHOME` but neither `B` nor `FPR`. Each Session 2 boot starts a new shell. Consequently the printed import operand expands to `/secret.asc`, and the signing selector is empty. This was reproduced with a clean Bash shell without running any import or accessing any key. The path at 117 also remains ROOT-BK1 even when the operator is processing ROOT-BK2 or either REL backup.
40: 
41: Failing scenario: an operator follows the fresh-boot backup test literally, unlocks BK2 and runs the printed command; it imports from `/secret.asc` and fails. Explicitly assign the actual mounted backup path and expected paper fingerprint in every test boot, check them before import, compare the imported fingerprint, and give the complete sign/verify commands. Use only a public key for the card-only boot. A backup `public.asc` fallback is safe only if no secret is imported from it and the input medium's role remains controlled.
42: 
43: ### F04 — MEDIUM, residual C04: LUKS check is not an exact destination check
44: 
45: **Lines 115–125.** `grep -B1 "$B" | grep -q crypt` checks matching output text and one preceding line; it does not establish the exact mount's backing device, identity or encryption format. A mount named ROOT-BK1-extra can match ROOT-BK1. If an ordinary RAM directory exists at the intended path, the check can announce LUKS-OK from the other mount and the following exports succeed into RAM.
46: 
47: Failing scenario: that naming/mount error affects a backup, the operator sees every required OK and removes an empty stick. Final restore acceptance should catch it, but row 185 already relies on those backups to permit shutdown. Resolve the exact mount with `findmnt`, trace that device to the intended encrypted mapper/label and physical stick, and stop before writes unless all agree. Record and check actual LUKS2 rather than assuming the GUI selected it. `luksDump` must target the partition actually identified, not an unverified sdX substitution.
48: 
49: ### F05 — MEDIUM, residual C06: publishing a fingerprint is not authenticated bootstrap
50: 
51: **Lines 201–205.** The independent computation is valuable, but “channels the author names” still does not specify authenticated first acquisition, retention outside the NUC or verification after publication.
52: 
53: Failing scenario: the author chooses repository and DNS publications; an attacker controlling both substitutes its B key and matching fingerprint for a new relying party. Two matching publications do not authenticate that initial key. State the concrete authenticated delivery method (or the explicit first-acquisition assumption and method), retain the approved key outside the operational environment and check each actual publication. These are unfinished custody-draft §8 steps (`docs/V1-RELEASE-KEY-CUSTODY-DRAFT.md:234–243`), not a finding that the first-production-release trigger has occurred.
54: 
55: ## S0–S9 and GNUPGHOME audit
56: 
57: - **S0:** The temporary export is inherited by all later GnuPG commands in that terminal. `keytocard` at 137–140, revocation copy at 121, and Session 2 GnuPG commands therefore use it consistently if S0 is repeated as instructed. No hard-coded default revocation path remains. For a second terminal, give `export GNUPGHOME="<existing RAM path>"` explicitly; rerunning `mktemp` creates another home. Check command success and verify the actual writable storage, rather than accepting every overlay. The filesystem-type filter is not exhaustive evidence that no internal disk is mounted; review backing devices/mounts. Observe that no network link is usable, not merely no default route. These are isolation checks, not GnuPG version differences.
58: - **S1–S2:** Card status, administration and PIN-change menu are consistent with the inspected sources. Upstream 2.2.40 lacks the required UIF status line, so the literal S1 acceptance cannot hold there. Stop before generation on an unsupported setup. Record the actual firmware/scdaemon versions before choosing a supported path.
59: - **S3–S4:** Expert P-256 selection and ECC sign-only option 10 agree with upstream 2.2.40 and 2.4.8 key-generation source. Read actual menus. The printed `FPR=<...>` is a substitution instruction, not executable shell syntax; replace it with the actual quoted value. `--list-keys` checks existence, not a comparison with the paper or a guarantee of the expected packet format.
60: - **S5–S7:** Quoted exports, revocation path and inherited home are appropriate; transfer uses the generated primary and `save`. The backup destination and recovery gaps are F02/F04. No production transfer was run to establish device behavior.
61: - **S8:** `forcesig` handling is corrected. Upstream 2.2.40 has no `uif`; 2.4.4/2.4.8 accept `uif 1 permanent` but have F01's readback limitation. Recording a version and stopping is safe refusal, not cross-version completion. Pin and rehearse the actual supported stack or supply a separately validated offline alternative.
62: - **S9:** SHA-256 detached signing and verification syntax is supported. For the negative and repeat tests, print complete commands with `--output ~/nt.asc` and `--output ~/p2.asc`, retain the same input and selector, and verify the second positive signature. Do not simply rerun the first command against its existing output: an overwrite prompt/cancellation is not a no-touch result. Require a touch timeout rather than any arbitrary failure. Current acceptance already rejects unexpected test outcomes.
63: 
64: Source checks used upstream [2.2.40 card-util.c](https://github.com/gpg/gnupg/blob/gnupg-2.2.40/g10/card-util.c), [2.2.40 keygen.c](https://github.com/gpg/gnupg/blob/gnupg-2.2.40/g10/keygen.c) and [2.4.8 keygen.c](https://github.com/gpg/gnupg/blob/gnupg-2.4.8/g10/keygen.c). The local executable reports GnuPG 2.4.4; it was not used against a card. Inspection of specific tags does not certify every 2.4.x package or downstream patch set.
65: 
66: ## Appended owner prechecks
67: 
68: Each result concerns this revision and its bounded claims, not certification of the service.
69: 
70: | Check | Result | File:line evidence |
71: |---|---|---|
72: | 1. Capture row | **PASS** | `docs/ceremony/CEREMONY.md:17–23,203–205` assigns authority roles and describes B-authenticated trust; it promises neither rejection of fresh attacker-key receipts nor capture visibility. Ground truth: `docs/V1-CONTRACT.md:34–37,50–53,72–74`: honest receipts protected under the stated assumptions, fresh attacker-key receipts pass after dual-channel capture, no detection guarantee. F05 concerns initial release authentication, not restoration of the cut listing. |
73: | 2. Trigger clause | **PASS** | `docs/ceremony/CEREMONY.md:8–10,20,204–205` cites A10.4.2's existing independence prerequisite and later bootstrap obligation. `docs/phase-0-prereg-amendment-10.md:616,624–643,668–673` applies the prerequisite under every option and places establishment before the first public production release. Revision 2 does not assert that release occurred, trigger fallback, or claim its rehearsal obligations discharged. |
74: | 3. Requester | **PASS for the expressly limited claim** | `docs/ceremony/CEREMONY.md:8–10,52–60,152–160,219` identifies the author-led ceremony and expressly defers candidate review, exact-byte approval and media controls for B's production use. Operational actors may propose future bytes; the author must authorize the exact release through the deferred procedure (`docs/V1-RELEASE-KEY-CUSTODY-DRAFT.md:253–278`). Storage separation is not treated here as a completed release-authorization argument. A broader claim that this ceremony establishes requester independence would fail. |
75: | 4. Binding text | **PASS** | `docs/ceremony/CEREMONY.md:3–10,37–48` labels the document OWNER DRAFT and distinguishes owner choices from registered A10.4.2 independence. That requirement is registered at `docs/phase-0-prereg-amendment-10.md:624–643`; the profile's key-format rule is implemented at `docs/ceremony/CEREMONY.md:6,99–104` (`docs/V1-PROFILE.md` §15.4). Exact ceremony commands and draft checks are proposed operating requirements, not silently attributed to signed registration. No ruling budget, fixed 24-hour FAILED rule or conflicting registered custody mandate is imported. This report treats operational defects as defects in that proposal, not violations of invented registered rituals. |
76: 
77: Generation is not a verifier release. No registration, freeze compliance, TEST-rejection rehearsal, deployed-package identity, production acquisition or full release-independence gate is discharged by this confirmation.

=== FILE (new): docs/reviews/ceremony/CODEX-REVIEW.md
1: # Ceremony revision 1 — Codex review
2: 
3: Reviewed 2026-11-02 against `docs/reviews/ceremony/BRIEF.md`, including all four owner prechecks. Recommendation: revise and rehearse the corrected procedure before generating production keys. Two command compatibility defects block the stated Tails 6 / Debian 12 / GnuPG 2.2 target. The isolation and acceptance conditions also need completion.
4: 
5: Snapshot: HEAD `54b382cd308291cf92457ff640584fba51ffc02c`; reviewed working-tree `docs/ceremony/CEREMONY.md` SHA-256 `1957f82babb5ad45d48b3b0ff3265bad5690eaf5c4f686affc5ab5101f98e8fc` (untracked at review time). Only this report was written in the repository. No production card, PIN, secret or backup was accessed. This is a source/document review, not a hardware rehearsal or independence certification.
6: 
7: ## Findings
8: 
9: ### C01 — HIGH: P-256 card attribute selection needs expert mode
10: 
11: **Location:** `docs/ceremony/CEREMONY.md:69–73`.
12: 
13: On GnuPG 2.2.40, `key-attr` calls `ask_curve`; NIST P-256 is marked expert-only. `admin` enables card administration, not GnuPG expert mode. With the printed `gpg --card-edit`, selection `3` is unavailable; the operator cannot complete this step as written. Use `gpg --expert --card-edit`, select the displayed P-256 entry, read the attributes back, and rehearse the complete prompt sequence. For encryption/authentication, an empty algorithm response leaves the existing attribute unchanged; spell out those responses rather than “leave ... as they are.”
14: 
15: Evidence: upstream [2.2.40 card-util.c](https://github.com/gpg/gnupg/blob/gnupg-2.2.40/g10/card-util.c), `ask_card_keyattr`; [keygen.c](https://github.com/gpg/gnupg/blob/gnupg-2.2.40/g10/keygen.c), `ask_curve`. The Debian bookworm patch set inspected below does not alter this selection.
16: 
17: ### C02 — HIGH: `uif` is unavailable in the stated GnuPG 2.2 target
18: 
19: **Location:** `docs/ceremony/CEREMONY.md:116–138`, also `:45` and `:56`.
20: 
21: Upstream 2.2.40's card-edit command table has no `uif` command; its status renderer also lacks the expected UIF display. I inspected Debian `2.2.40-1.1+deb12u2`'s patch set and found no UIF backport. Thus the printed command cannot establish fixed touch on this target. A reader who treats continuation of the interactive session as success can leave touch disabled; alternatively the required status check blocks completion. This is not evidence that the recorded rehearsal failed: that record names neither the Tails nor GnuPG version, so its successful command cannot establish 2.2 compatibility.
22: 
23: Pin and record the actual Tails, GnuPG, scdaemon and card firmware versions. Either use an offline-available, pinned YubiKey Manager with `ykman openpgp keys set-touch sig fixed`, or select and rehearse a GnuPG version supporting the printed command. Check fixed/permanent explicitly: ordinary `on` is weaker than the promised non-disableable policy and must not be accepted as equivalent at line 137. No online installation during the secret session.
24: 
25: Evidence: [2.2.40 card-util.c](https://github.com/gpg/gnupg/blob/gnupg-2.2.40/g10/card-util.c), command table/status renderer; [Debian patch archive](https://deb.debian.org/debian/pool/main/g/gnupg2/gnupg2_2.2.40-1.1+deb12u2.debian.tar.xz); [Yubico OpenPGP commands](https://docs.yubico.com/software/yubikey/tools/ykman/OpenPGP_Commands.html). Rehearsal evidence: `docs/ceremony/2026-11-01-rehearsal-1.md:3–5,29–33`.
26: 
27: ### C03 — HIGH: the RAM-only and independent-session assumptions are asserted, not enforced
28: 
29: **Location:** `docs/ceremony/CEREMONY.md:24`, `:49–50`, `:75–77`, `:141`, `:147`.
30: 
31: The boot stick is shared and not new, yet there is no prohibition on unlocking Persistent Storage, no explicit temporary RAM GnuPG home, and no check of the actual home/mounts. Tails can persist GnuPG keys. An operator using an existing persistent GnuPG setup generates/imports secrets onto the boot medium; shutdown does not remove those copies. At-rest key protection does not make this RAM-only or preserve the “only copies” inventory. Do not claim that a plaintext persistent write has been observed: the defect is that the procedure does not establish its absence.
32: 
33: Add an explicit no-persistence boot condition, an empty GnuPG home in verified RAM used consistently by every command (including the revocation path), no internal mounts/swap/hibernation, no autorun, no NUC scripts/configuration, and authenticated image verification independent of the NUC. Name the signing hardware and complete the laptop credential/inbound-access check. Specify these conditions for restore boots too. No secrets, photos or transcripts may go to chat/repository/NUC. Stop if any isolation check fails.
34: 
35: These are gaps against the **draft procedure**, `docs/V1-RELEASE-KEY-CUSTODY-DRAFT.md:99–106,121–133,173–177,210,229–230`; the registered requirement is the independent boundary and controlled crossing, not a registered mandate for these exact commands (`docs/phase-0-prereg-amendment-10.md:624–643`). Tails documents [GnuPG persistence](https://tails.net/doc/persistent_storage/configure/index.en.html#gnupg).
36: 
37: ### C04 — HIGH: failure paths can destroy the last usable copy or silently continue with failed backups
38: 
39: **Location:** `docs/ceremony/CEREMONY.md:87–100`, `:109–114`, `:141`, `:145–158`.
40: 
41: The export/copy commands run independently; `sync && ls` can succeed after `gpg` failed and left an empty `secret.asc`. Restore failure is only recorded, with no rejection condition. Scenario: both exports fail, keytocard fails, and the operator reaches shutdown. The sole usable secret vanishes. Another scenario leaves a working card but no recoverable backup and still proceeds to publication.
42: 
43: Require successful exits and nonempty expected outputs for each export/copy, check the mounted destination is the intended LUKS mapper before writing, and require both isolated restore tests plus primary test before accepting custody. Quote paths and substitute the actual label for every backup, including the hard-coded `ROOT-BK1` in the restore example. A directory or filename existing is insufficient evidence of a backup.
44: 
45: Add a short recovery table: on transfer failure preserve the original RAM key and encrypted backups, inspect actual card fingerprint/state, and do not reset/overwrite a production card blindly; do not shut down the last usable secret until a recoverable copy is established. On failed restore stop acceptance/publication, recover from the surviving good copy and replace/retest the failed backup offline. If no good copy remains, generate a new key and discard the abandoned fingerprint from proposed production records. On a wrong PIN stop and inspect remaining retries; do not guess repeatedly or intentionally exhaust counters. On touch timeout retry only after checking state and policy; “timeout means no touch” at line 132 is too categorical for all device/transport failures. Record non-secret outcomes. The draft's general incident section is not a substitute for these immediate ceremony decisions.
46: 
47: ### C05 — MEDIUM: positive signing alone does not test the promised PIN/touch behavior or the isolated primary
48: 
49: **Location:** `docs/ceremony/CEREMONY.md:116–139`, `:143–158`.
50: 
51: `forcesig` toggles the current policy; rerunning step 8 after a partial failure can turn forcing off. A single successful signature after a PIN/touch does not prove that signing without touch fails, that a second request requires a fresh PIN, or that agent caching does not supply it. The only card proof uses the generation session; no fresh-session primary test excludes residual software state.
52: 
53: Read the current policy, toggle only if needed, and require the desired readback. Add a controlled no-touch timeout test, a second signing request with observed PIN behavior, and a fresh-session card-only test importing only the public key. Record actual caching behavior and fixed touch. Account for test signatures in the counter: counter 1 ceases to be the acceptance value after additional tests. Do not use incorrect PIN attempts as a negative test. Draft basis: `docs/V1-RELEASE-KEY-CUSTODY-DRAFT.md:186–204,218–221`; these are draft operational checks, not separately registered rituals.
54: 
55: ### C06 — MEDIUM: custody/bootstrap record is incomplete and public author choices are hidden unnecessarily
56: 
57: **Location:** `docs/ceremony/CEREMONY.md:8`, `:164–172`.
58: 
59: The listed custody record lacks the signing setup, laptop credential-check date/result, holder/access boundary, pinned software/firmware/encryption settings, reset-code choice (none is acceptable), and test outcomes. “AUTHOR ... never in the repository” also sweeps public selections such as image version, verification device and publication channels into paper-only choices. A future reviewer then cannot reconstruct the boundary from the dated record. Keep secrets and locations private; record the non-secret choices/results required to identify the procedure and setup.
60: 
61: Bootstrap also needs an independently computed fingerprint, not merely a fingerprint string read from potentially substituted material; an approved public key retained outside the NUC; and a concrete authenticated first-acquisition route plus publication checks. Specify the dated first-production-release bootstrap record's link to the original freeze baseline and actual B fingerprint. Do not copy the custody draft's stale demand to put a post-freeze production fingerprint in the original freeze record. Basis: draft `:234–247`; registered A10.4.2 `:628–633,668–673`; runbook `:121–124`. No first public production release is established by this review, so these are unclosed prerequisites, not a declaration that its deadline has already been breached.
62: 
63: ### C07 — MEDIUM: separate keys/sessions do not establish requester independence
64: 
65: **Location:** `docs/ceremony/CEREMONY.md:14–18`, `:35–42`, `:162–172`.
66: 
67: A and B having different secrets/backups is sound, but an attacker controlling DNS/git/AWS can still supply a malicious candidate through the operational environment and solicit the author's touch/signature. Touch does not bind approval to bytes. The ceremony expressly defers per-release authorization to the draft's §9, so it does not itself close A10.4.2. Add an explicit handoff: no production use until independent review/build, baseline, exact archive-hash approval, controlled input media and author-only authorization are implemented and rehearsed. Holding B decides trust only through releases a relying party authenticates and installs; stealing it does not change an already retained verifier.
68: 
69: The theft statement at line 18 is also conditional: knowing a passphrase alone does not produce any key, and paper sheets/tokens must have compatible separation if location compromise is meant to expose at most one key. Separate boots on shared hardware do not withstand compromised shared hardware/boot firmware; retain the draft's peripheral assumption (`:146–149`). Registered basis: A10.4.2 `:624–643`; requester-specific draft basis `:92–98,203–204,260–289`.
70: 
71: ## Command and section disposition
72: 
73: | Section / operation | Assessment |
74: |---|---|
75: | Two key roles, separate backups and boots | Sound design choices for limiting shared custody exposure, subject to C03/C07; not separation of human control. |
76: | Card status, changing default admin/user PINs | Correct basic sequence. Record no reset code or configure one; enforce retry handling. |
77: | `key-attr` before import | Correct order; C01 fixes the command. Do not reconfigure a populated production slot casually. |
78: | Expert key generation: 10, curve 3, expiry 0 | Correct for upstream 2.2.40: sign-only ECC, NIST P-256, no expiry. UID and fingerprint listing are sound. |
79: | Export secret/public and revocation path | `~/.gnupg/openpgp-revocs.d/FPR.rev` is correct for the default home and uppercase full fingerprint. If a RAM home is selected, use its path. The auto-generated certificate is deliberately guarded with a leading colon before the armor header; retain the complete file and document authorized-use handling separately. It is not to go to the out stick. C04 covers unchecked failures. |
80: | `keytocard` then `save` | Correct, but add the preceding “Really move the primary key? (y/N)” → yes prompt. Card import occurs before save; save asks the agent to replace the local secret with a card stub. Quitting is not a rollback of the card write. This is not proven erasure or removal of backups/cache. Require readback and fresh-session signing. |
81: | PIN force, permanent touch | Order after key import is sensible. `forcesig` is a toggle; `uif` is incompatible with the stated 2.2 target (C02/C05). |
82: | SHA-256 detached proof and verification | Commands are sound; default signer is unambiguous only with an empty one-key home. Explicit `--local-user "$FPR"` improves recovery safety. Replace angle-bracket placeholders before running; they are not literal shell commands. |
83: | Separate restore boots without card | Sound and valuable: prevents the card or prior agent standing in for the backup. Requires C03/C04 acceptance conditions. |
84: | Out-only stick and read-only NUC use | Sound; never return it after NUC contact. Public signatures/key/proof text are appropriate; unpublished revocation material is not. |
85: | Timing | Honestly labelled estimate; no finding. |
86: 
87: For save behavior see [GnuPG key management](https://gnupg.org/documentation/manuals/gnupg/OpenPGP-Key-Management.html) and [2.2.40 keyedit.c](https://github.com/gpg/gnupg/blob/gnupg-2.2.40/g10/keyedit.c), `cmdKEYTOCARD`/`cmdSAVE`. No hardware behavior was inferred solely from a successful signature in the rehearsal.
88: 
89: ## Owner choices
90: 
91: - **Hardware mode:** acceptable under A10.4.2, which also permits offline software custody. Backups deliberately remain exportable signing authority; PIN/touch do not protect their use. Every backup and its decryption secret belongs to the access-boundary analysis.
92: - **LUKS2 with Disks defaults:** reasonable design but not a pinned setting as required by custody draft `:165`. Record exact tool/version, observed LUKS format, cipher/KDF parameters and protected secret-export format without secrets. The GUI description alone does not establish them. Do not treat this draft pinning rule as a registered demand for a particular cipher or two independent passwords.
93: - **Same password for both layers of one key:** gives no independent second password barrier. For the stated thief-with-stick threat, compromising that password unlocks both layers; this does not contradict a registered two-password requirement (none found). A/B passwords must remain independent and generated offline. Seven-word physical-dice generation is a reasonable recommendation, not an adopted registered word count.
94: - **Card KDF off:** removes PIN protection against passive USB observation. Defensible only under a trusted host/USB-path assumption; offline alone does not prevent a USB logger. KDF would not stop a malicious signing host that sees entered PINs or asks for unintended signatures. State the accepted boundary rather than “buys nothing.” No registered requirement for KDF-on was found.
95: - **No expiry:** no contradiction found. Repository validity is evaluated through the configured signing interval; release authentication follows its separately authenticated lineage. Neither establishes automatic compromise detection/recovery. OpenPGP revocation is not evaluated by receipt verification (`docs/V1-CONTRACT.md:45`); retaining a certificate does not add that property.
96: 
97: ## Appended owner prechecks
98: 
99: Each result concerns the reviewed document, not a general certification of the system.
100: 
101: | Check | Result | Evidence and disposition |
102: |---|---|---|
103: | 1. Capture row | **PASS** | `CEREMONY.md:12–18,171–172` describes authority roles and required B independence; it never promises attacker-key rejection or visibility after DNS+git capture. Ground truth remains `docs/V1-CONTRACT.md:37–39,52–53,72`: honest material protected; fresh attacker-key receipts pass; no detection guarantee. B independence does not restore the cut listing. |
104: | 2. Trigger clause | **PASS** | `CEREMONY.md:15–16` invokes A10.4.2's unconditional independence prerequisite, which applies under every option (`amendment-10.md:616,624–634`). It does not invoke fallback, claim deadline breach, or use the ceremony/rehearsal to declare the first-public-release gate closed. Required production release rehearsal and TEST rejection remain pending obligations (`:642–657`), not consequences demonstrated here. |
105: | 3. Requester | **FAIL** | `CEREMONY.md:14–18,35–42` supports independence primarily with storage/session separation and does not identify who may submit work or how author approval binds to bytes. C07 supplies the concrete channel-captor/requester scenario. Deferral to §9 is legitimate scope separation, but prevents treating this ceremony as an independence argument. |
106: | 4. Binding text | **PASS** | `CEREMONY.md:3–8,33–45` labels owner draft/choices; `:15–16` correctly attributes independence to adopted A10.4.2/row 34 (`amendment-10.md:624–643,770`). No schedule ruling budget or 24-hour FAILED rule is imported. Draft procedural omissions above are labelled draft gaps, not promoted to registered mandates. Owner choices remain proposals for author confirmation; no conflicting registered command/cipher/expiry mandate was found in the cited registration. |
107: 
108: A production key-generation ceremony is not itself a verifier release. This review neither invokes the NARROW-MODEL fallback nor declares registration, release-format freeze compliance, TEST-rejection rehearsal, deployment identity, or the full release gate discharged.

=== FILE (new): docs/reviews/ceremony/codex-confirm-last.md
1: Wrote [CODEX-CONFIRM.md](/home/tony/projects/tessera/docs/reviews/ceremony/CODEX-CONFIRM.md).
2: 
3: It covers C01–C07 and all four prechecks. Revision 2 still needs changes, chiefly fixed-touch readback and preserving the last usable secret after transfer failure. Only the report was changed.
4: 

=== FILE (new): docs/reviews/ceremony/codex-last.md
1: Report written to [CODEX-REVIEW.md](/home/tony/projects/tessera/docs/reviews/ceremony/CODEX-REVIEW.md).
2: 
3: Seven findings: four high, three medium, including two GnuPG 2.2 command compatibility defects. All appended prechecks are reported; requester analysis fails.
4: 
5: Recommendation: revise and rehearse before production key generation. Ceremony unchanged.
6: 

=== FILE (new): docs/reviews/issuance-lifecycle/CODEX-CONFIRM-2.md
1: **Verdict: not ready to implement.** Revision 3 removes concurrent poller execution, but it still permits loss of timely eligibility, and its lease argument does not cover the interval from observation to sending the write. Step 10 needs to check the registered property without redefining eligibility as successful persistence.
2: 
3: Review was read-only; no repository edits or git writes. Constructed counterexamples are in [scratch](/tmp/tmp.OmyIY8mGav/counterexamples.txt). These are protocol traces, not TLC results.
4: 
5: ### A. ILC-01–05
6: 
7: “CLOSED” below concerns the design correction, not implementation conformance.
8: 
9: | Finding | Status | Assessment against registered text |
10: |---|---|---|
11: | **ILC-01 — timely observation loses to expiry** | **PARTIAL** | [Steps 1–4](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:46) remove simultaneous poller invocations and the API lifecycle writer. But “counts once that write is durable” weakens the protected event, and the delayed-write argument is incomplete. [A2:153–160](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:153) requires the inclusive boundary to be latch-winning. See ILC2-01–02. |
12: | **ILC-02 — premature permanent failure** | **PARTIAL** | [Step 6](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:75) correctly waits for every calendar, but “no pending calendar” does not establish that every attestation’s qualifying header evidence is complete. [A2:161–162](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:161) does not authorize treating recoverable missing evidence as permanent predicate failure. See ILC2-03. |
13: | **ILC-03 — unavailable-evidence refusal** | **PARTIAL** | [Step 5](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:71) expressly protects durable latches and uses the single writer. It still treats absence of a durable latch as sufficient protection against refusing timely eligibility. A2.3’s termination obligation does not cancel [A2.1’s eligibility protection](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:130). |
14: | **ILC-04 — overbroad post-latch discard** | **CLOSED** | [Step 7](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:78) preserves the qualifying presentation, retries transient failures, and restricts discard to incurable failures. That respects [A9’s completeness invariant](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:165) and [not-after prohibition](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:422). The implementation must classify the underlying failure, rather than merely classify a verifier reason code. |
15: | **ILC-05 — terminal guards and retry recovery** | **CLOSED** | [Steps 1 and 8](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:46) specify state/attempt guards and atomic end-and-allocate, including refusal. This addresses duplicate transitions and the between-attempt crash gap, consistent with [A2.3’s atomic refusal requirement](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:278). |
16: 
17: ### B–C. Protocol attack and new findings
18: 
19: **ILC2-01 — High: persistence is substituted for the registered eligibility event.**
20: 
21: [Revision:55](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:55) says:
22: 
23: > “The observation counts once that write is durable.”
24: 
25: That is a substantive restriction. An observation at B followed by a crash before persistence becomes an observation that never counted. Disclosure as a residual does not establish compatibility with the registered latch obligation.
26: 
27: The model makes the discrepancy sharper. [`NewBlock`:68–71](/home/tony/projects/tessera/formal/tla/P5cP5P6_BridgeSlack_Latch.tla:68) records `burialAtWall` when burial occurs. [`EligibleInLifecycle`:49](/home/tony/projects/tessera/formal/tla/P5cP5P6_BridgeSlack_Latch.tla:49) tests that time; there is no issuer-fetch or persistence prerequisite. A2 expressly identifies this expression as its mechanized boundary counterpart at [155–156](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:153).
28: 
29: Consequently, **the stated residual is not the only path**:
30: 
31: 1. Burial occurs on time.
32: 2. No issuer invocation observes it before sources become unavailable.
33: 3. Step 5 eventually ends the unlatched attempt.
34: 
35: No killed, undurable observation is needed. Polling delay or starvation can produce the same gap.
36: 
37: A2’s prose also calls B the service’s observation time at [115–124](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:115). That creates a refinement question between prose and model; it does not authorize silently replacing either with durable-write time. Step 10 must expose and resolve that distinction, preserving the existing property rather than proving a weaker replacement.
38: 
39: **ILC2-02 — High: waiting until B + lease does not drain every timely-observation write.**
40: 
41: [Revision:59–62](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:59) relies on the clock decision’s assumption that AWS resolves a request within fifteen minutes **of sending it** ([clock decision:27–29](/home/tony/projects/tessera/docs/decisions/2026-10-27-service-clock-tolerance.md:27)). Observation and sending are separate events.
42: 
43: With B = 0 and lease = 900 seconds:
44: 
45: | Time | Event |
46: |---|---|
47: | 0 | Poller observes qualifying evidence on time. |
48: | 2 | It sends the guarded latch write, then is killed. |
49: | 901 | Successor reads OPEN; a fresh fetch returns stale/pending evidence; expiry commits. |
50: | 902 | Earlier latch write resolves and fails its guard. |
51: 
52: The write resolved within 900 seconds of sending. Expiry occurred strictly after B + lease. Nevertheless, expiry beat a timely observation.
53: 
54: The guards prevent reopening the expired attempt; **they do not make the timely latch win**. The protocol needs an ordering or recovery mechanism covering observation-to-send as well as send-to-resolution. An undurable observation remains a separate problem even after that repair.
55: 
56: The same unresolved write can overlap a later invocation’s store operations despite reserved concurrency 1.
57: 
58: **ILC2-03 — Medium: calendar completion does not freeze the lowest qualifying height.**
59: 
60: [Step 6:75–77](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:75) infers that no pending calendar means the lowest qualifying height cannot change.
61: 
62: Counterexample:
63: 
64: - Every calendar proof has returned a Bitcoin attestation.
65: - A higher attestation has its complete pinned segment and fails a temporal conjunct.
66: - A lower attestation lacks its header segment.
67: - Recovering that segment later makes the lower attestation qualify and satisfy the predicate.
68: 
69: This follows directly from [profile:879–891](/home/tony/projects/tessera/docs/V1-PROFILE.md:879): qualification requires the full pinned, linked segment; an incomplete branch supplies no time fact. Header times are nonmonotone.
70: 
71: Step 6 becomes sound only if “complete” includes all evidence needed to establish the claimed stable selection, rather than its parenthetical “no pending calendar.” A missing header must not become permanent failure merely because calendar work finished.
72: 
73: **Invocation overlap and retries.** Reserved concurrency 1 caps simultaneous invocations of this poller function. Timeouts, Lambda retries, and EventBridge redelivery do not themselves bypass that cap; duplicate events remain possible and must be handled sequentially and idempotently. AWS documents both the [concurrency cap](https://docs.aws.amazon.com/lambda/latest/dg/configuration-concurrency.html) and [asynchronous retries, throttling, and duplicate delivery](https://docs.aws.amazon.com/lambda/latest/dg/invocation-async-error-handling.html).
74: 
75: The live configuration is **300 seconds**, not fifteen minutes: [main.tf:352–363](/home/tony/projects/tessera/service/issuer/infra/main.tf:352). Fifteen minutes is the write lease. Even if execution timeout became fifteen minutes against the ten-minute schedule, excess invocations would be throttled/queued; downstream requests already sent remain the relevant overlap.
76: 
77: The API currently still calls `settle` at [api.py:194](/home/tony/projects/tessera/service/issuer/tessera_issue/api.py:194). Removing that writer is therefore a necessary implementation change, not an existing guarantee.
78: 
79: **Step 7:** sound as the revised design rule. Preserve the actual qualifying evidence durably, not only its digest, and classify “incurable” against recovery using that presentation.
80: 
81: **Step 8:** sufficient for duplicate **end-and-allocate transitions**, provided the expected state and attempt id are evaluated atomically at commit and a failed or ambiguous write causes a reread. The existing store already uses [version CAS](/home/tony/projects/tessera/service/issuer/tessera_issue/aws.py:78). This does not provide exactly-once external signing or stamping; attempt-labelled jobs and idempotent recovery still carry that work.
82: 
83: ### Owner prechecks
84: 
85: | Check | Result | File:line and assessment |
86: |---|---|---|
87: | **1. Capture row** | **PASS** | [Revision:18–22](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:18), [78–82](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:78) make no claim that dual-channel capture rejects attacker keys or reveals capture. [Contract:37,72–73](/home/tony/projects/tessera/docs/V1-CONTRACT.md:37) remains explicit: attacker-key receipts can pass; issuing-account capture permits issuance. |
88: | **2. Trigger clause** | **FAIL** | [Revision:71–77](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:71) does not establish the relevant antecedents: unlatched is not necessarily untimely; no pending calendar is not necessarily permanent predicate failure. |
89: | **3. Requester** | **PASS** | [Revision:46–51,83–86](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:46) makes no key-security claim based solely on storage or independent custody. Attempt routing and signing closure remain explicit. This is not a certification of signer requester authorization. |
90: | **4. Binding text** | **FAIL** | [Revision:55,66–74](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:55) introduces durable-write counting and an operating refusal policy without demonstrating compatibility with [A2:130–160](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:130) and its cited burial-time model. An owner residual cannot amend that protection. |
91: 
92: Step 10 should include observation-to-send delay, delayed commits, crashes before persistence, timely burial without observation, partial header recovery, and duplicate transition retries. A green model that starts protection only at durable latch would leave the central discrepancy unchecked.
93: 

=== FILE (new): docs/reviews/issuance-lifecycle/CODEX-CONFIRM-3.md
1: **Verdict: not ready to implement.** The fence repair is sound within the checked bounds, but the residual remains incomplete, and revision 5.2’s fixed interval window can prevent termination.
2: 
3: Review was read-only, with no repository edits or git writes. All reviewer-created files are under [scratch evidence](/tmp/tmp.nSu1oGphAh/EVIDENCE.md). Revision-5.2 files appeared during review; observations about them concern a captured, in-progress model, not completed section-7 results.
4: 
5: **A. Previous findings**
6: 
7: | Finding | Status | Assessment |
8: |---|---|---|
9: | **ILC2-01 — persistence substituted for eligibility** | **PARTIAL** | [Design:52](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:52) now preserves chain timeliness independently of persistence. However, timely eligibility can still end `EVIDENCE_UNAVAILABLE`. Acknowledging that departure does not discharge [A2.1:130](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:130) or its inclusive latch obligation at line 153. The author decision remains outstanding. |
10: | **ILC2-02 — observation-to-send gap defeats lease draining** | **CLOSED** | [Steps 4–5](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:57) remove lease-based negative inference and fence before fetching. Once the successor’s fence commits, the predecessor’s ending write cannot pass its version guard. The no-fence companion reproduces the race. This closes the specific ordering defect, not all lost-observation paths. |
11: | **ILC2-03 — calendar completion does not fix selection** | **CLOSED** | [Design:59](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:59) now requires every attestation’s full pinned, linked segment. That addresses the missing-lower-header counterexample and matches the requested historical profile §7.1 at `270ca49:879–891`. |
12: 
13: The design correctly retains the three conjuncts required by A2.2 and A3.7.3, frozen signatures and fresh stamps under A9.5, local refusal under A9.7, and A9’s completeness and not-after checks. These are design assessments, not implementation conformance findings.
14: 
15: **E. New findings**
16: 
17: **ILC3-01 — High: residual (a) unnecessarily requires a killed invocation.**
18: 
19: [Design:98](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:98) names a timely observer killed before writing. But a timely observation can also be lost when its latch write is rejected, without any invocation being killed. The design itself says an uncommitted success resets nothing at [line 76](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:76).
20: 
21: I disabled `Kill` in scratch copies and added a reachability witness. TLC found the path in both R51 and the captured R52:
22: 
23: 1. Eligibility is fetched at the inclusive boundary.
24: 2. Its latch write is sent but dropped without applying.
25: 3. Subsequent fetch failures satisfy the operating-period rule.
26: 4. `EVIDENCE_UNAVAILABLE` commits.
27: 
28: The R52 trace includes committed failures in both required intervals, so the interval-set repair does not remove this path. See [R52 counterexample](/tmp/tmp.nSu1oGphAh/r52-drop/drop.out:27).
29: 
30: Broaden (a) to **an observed eligible presentation whose latch never commits**, including crashes, rejected writes, and failed guards. Neither source outage nor process death is necessary.
31: 
32: **ILC3-02 — Medium: `P5_Spread` does not establish the interval coverage attributed to it.**
33: 
34: [RESULTS:509](/home/tony/projects/tessera/formal/tla/issuer-lifecycle/RESULTS.md:509) describes distinct invocation-start ticks, then equates that with no skipped scheduled tick. The actual ghost records `w.st0`, whereas the design counts the interval in which the **fetch starts**: [R51:318](/home/tony/projects/tessera/formal/tla/issuer-lifecycle/IssuerLifecycleR51.tla:318).
35: 
36: There are two differences:
37: 
38: - Distinct invocation starts can have fetches in the same later interval.
39: - Enough distinct historical ticks do not establish coverage of every interval in a particular operating period.
40: 
41: A scratch probe changed only this ghost’s timestamp from invocation start to fetch start. `P5_Spread` then failed with committed failed fetches at 2 and 4, an ending decision at 4, and no failed fetch at 3: [counterexample](/tmp/tmp.nSu1oGphAh/spread-fetch.out:27).
42: 
43: Thus [RESULTS:635](/home/tony/projects/tessera/formal/tla/issuer-lifecycle/RESULTS.md:635) overstates the guarantee even with one invocation start per tick. R52 begins repairing the timestamp distinction, but its checked spread property still counts distinct fetch times rather than directly asserting the required interval membership.
44: 
45: **ILC3-03 — High: the initial operating-period window can become permanently impossible to satisfy.**
46: 
47: [Design:79](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:79) needs a rule for advancing or restarting a failed coverage window. The captured R52 interpretation records only indices below `Expected`: [R52:334](/home/tony/projects/tessera/formal/tla/issuer-lifecycle/IssuerLifecycleR52.tla:334). Its ending guard requires enough indices from that initial window: [R52:254](/home/tony/projects/tessera/formal/tla/issuer-lifecycle/IssuerLifecycleR52.tla:254).
48: 
49: With period 2, interval 1, allowance 0:
50: 
51: - The first committed failure starts the window at 2.
52: - Interval `[3,4)` has no committed failure.
53: - All later polls fail, but their interval indices are outside the counted window.
54: 
55: The missing interval can never be recovered. If evidence never completes, there is neither a successful reset nor another ending path.
56: 
57: TLC reached an open, unburied attempt with `unavailable_since=2`, `fi={0}`, and three committed failures by time 6, without faults: [witness](/tmp/tmp.nSu1oGphAh/stranded.out:27). This is a reachability result plus a structural argument for continued nontermination, **not** a TLC liveness counterexample.
58: 
59: Specify a rolling window or a restart rule that preserves the coverage requirement. Parameter validation must also define partial intervals and constrain the allowance.
60: 
61: **ILC3-04 — Medium: the change inventory omits storage expiration that can destroy live attempt material.**
62: 
63: The design permits prolonged open attempts and retries transient post-latch failures indefinitely: [design:112](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:112). Existing infrastructure expires every object under `content/`, `work/`, `frames/`, and `result/` after 31 days: [main.tf:101](/home/tony/projects/tessera/service/issuer/infra/main.tf:101).
64: 
65: Consequently, a sufficiently delayed live attempt can lose its frozen material independently of evidence-source recovery. S3 lifecycle expiration is based on object age and matching filters; it does not consult the request’s lifecycle state. [AWS lifecycle documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/intro-lifecycle-rules.html)
66: 
67: Add retention/lifecycle handling to the implementation inventory. The model’s durable-store abstraction hides this concrete failure.
68: 
69: **B. Model fidelity and property meanings**
70: 
71: The models faithfully represent a useful **lifecycle core**, not all steps 1–10.
72: 
73: | Checked claim | What it establishes |
74: |---|---|
75: | **P1 / `NoTimelyExpiry`** | Timely eligibility is protected against the modeled `expired` and `discarded` states. It explicitly excludes `unavail`; it does not prove “every timely-eligible attempt ships.” |
76: | **`NegativeEndsAreTrue`, `LatchIsTrue`, `ExpiryAfterB`** | Negative ends have a failing abstract verdict; latches have a passing verdict; expiry/discard decisions use the stated boundary. The three conjuncts are abstracted into `pass`, not recomputed from headers. |
77: | **P2 and action properties** | Current-attempt isolation, allocation ordering, one shipped attempt, and modeled state-transition protection. They do not establish exactly-once signing, stamping, publication, or delivery. |
78: | **P3** | Final modeled end and refusal are atomic; intermediate modeled ends allocate the next attempt atomically. |
79: | **P4** | Bounded termination under the stated fairness, scheduling, finite-fault and write-resolution assumptions. R51’s completed liveness run uses N=1 and modifies polling at `MaxTime`; it does not establish R52 termination. |
80: | **P5 / `USAfterB`** | The committed failure history and decision guards described by the formulas. Successful fetches without committed writes remain unprotected. |
81: | **`P5_Spread`** | The distinct-timestamp cardinality check, subject to ILC3-02—not the stronger interval-coverage claim. |
82: | **Residual/sanity witnesses** | Reachability or bounded unreachability of their particular ghost predicates, not completeness of the residual taxonomy. |
83: 
84: The fence result is useful evidence: the correct bounded run completes, the no-fence companion goes red at matching bounds, and orphaned writes are reachable. Conversely, B2 staying green is reported honestly; these properties do not require the second-writer companion to fail.
85: 
86: Material abstractions remain:
87: 
88: - **One request:** hides cross-request starvation under one 300-second poller invocation.
89: - **Two attestations:** covers the lower-header decoy, not arbitrary branch collections or concrete selection/authentication.
90: - **No reorgs:** assumes buried evidence remains permanent. Six-deep burial does not mechanically exclude deeper reorgs.
91: - **One clock:** hides premature or delayed period decisions from clock changes between invocations.
92: - **Durable atomic store:** hides lost evidence and the expiration in ILC3-04.
93: - **Immediate abstract assembly:** hides packaging, publication and delivery failures.
94: - **No signing/stamping or signing closure:** step 8’s `SIGNING_CLOSED` behavior is not checked.
95: - **No post-latch incurable discard:** the model’s unconditional `LatchProtects` is stronger than—and does not represent—step 7.
96: 
97: The last exclusion matters: a temporally eligible attempt can legitimately fail an additional shipping requirement, including A9’s not-after invariant. The model does not check that classification.
98: 
99: **C. Residual and B**
100: 
101: The residual is **not yet precise or complete**:
102: 
103: - Replace killed-before-write with successful observation whose latch never commits.
104: - State sampled failed fetches and committed records, rather than continuous evidence unavailability.
105: - Say **every required interval except the allowance**. [Design:104](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:104) currently drops that qualification.
106: - Resolve ILC3-03 before asserting sustained failure guarantees termination.
107: 
108: Outside `EVIDENCE_UNAVAILABLE`, step 7 can discard temporal eligibility for an incurable completeness/window failure. Signing closure prevents a necessary new attempt; it expressly does not terminate an existing latched or already signed-and-stamped attempt.
109: 
110: The B question is real and fairly raised: [A2:115](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:115) includes service observation-path delay, whereas [`NewBlock`:68](/home/tony/projects/tessera/formal/tla/P5cP5P6_BridgeSlack_Latch.tla:68) records burial independently of observation. Neither a green lifecycle check nor owner prose resolves that refinement.
111: 
112: Two qualifications are needed:
113: 
114: - Keep observation time, burial time, and the deadline distinct; the documents overload “B.”
115: - The historical path-(c) trace observes eligibility at 3 with deadline 1. Therefore [RESULTS:226](/home/tony/projects/tessera/formal/tla/issuer-lifecycle/RESULTS.md:226) cannot call that particular observation timely. The categorical statement about (c) in [design:107](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:107) needs qualification, although the fence now closes that race.
116: 
117: **D. AWS implementability**
118: 
119: The AWS primitives are sufficient:
120: 
121: - Conditional version updates can implement the fence and subsequent guards. End-and-allocate can use one item update or a DynamoDB transaction. [AWS conditional writes](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/read-write-operations.html)
122: - Reserved concurrency 1, timeout 300 seconds and a ten-minute schedule are valid and already configured at [main.tf:352](/home/tony/projects/tessera/service/issuer/infra/main.tf:352). Concurrency limits invocations; asynchronous retries and duplicate delivery still require idempotence. [AWS concurrency](https://docs.aws.amazon.com/lambda/latest/dg/configuration-concurrency.html), [AWS retries](https://docs.aws.amazon.com/lambda/latest/dg/invocation-async-error-handling.html)
123: - A schedule is not proof that every request was visited in every interval. Count actual fetch starts.
124: - Large preserved presentations can live in immutable S3 objects, written before committing their references in the latch. DynamoDB has a 400-KB item limit and no transaction spanning DynamoDB and S3. [AWS storage guidance](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-use-s3-too.html)
125: 
126: Operating period and allowance can remain runbook numbers. Their permitted values and window semantics must nevertheless be specified. AWS cannot supply the missing termination rule in ILC3-03.
127: 
128: **Owner prechecks**
129: 
130: | Check | Result | Evidence |
131: |---|---|---|
132: | **1. Capture row** | **PASS** | [Design:18](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:18) makes no claim of attacker-key rejection or capture visibility. [Contract:37](/home/tony/projects/tessera/docs/V1-CONTRACT.md:37) explicitly permits attacker-key receipts after dual-channel capture. |
133: | **2. Trigger clause** | **FAIL** | [Design:93](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:93) cites excessive-lag refusal permission, but unlatched state plus failed polls does not establish its antecedent for previously timely-observed attempts. Disclosure at lines 105–109 correctly leaves this unresolved. |
134: | **3. Requester** | **PASS** | [Design:15](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:15) and [121](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:121) make no custody-only key-security claim. This does not certify signer authorization; [A9:401](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:401) explicitly recognizes queue-controller signing capability. |
135: | **4. Binding text** | **FAIL** | [Design:8](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:8) says registered text is unchanged, while [108](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:108) acknowledges incomplete compliance with its shipping obligation. An owner operating rule cannot authorize that departure. The author decision remains necessary. |
136: 

=== FILE (new): docs/reviews/issuance-lifecycle/CODEX-CONFIRM-4.md
1: **Verdict: not ready to implement the entire ungated part as written.** The lifecycle core can proceed independently of the author decision, but the proposed storage fix still permits premature deletion. Correct ILC4-01 first; the author need not decide step 5 before that work proceeds.
2: 
3: Review was read-only, with no repository edits or git writes. Reviewer-created material is under [scratch evidence](/tmp/tmp.aRpLH86bRI/EVIDENCE.md).
4: 
5: **A. Previous findings**
6: 
7: | Finding | Status | Assessment |
8: |---|---|---|
9: | ILC3-01 — residual requires a kill | **CLOSED** | [Design:107](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:107) covers any observed eligible presentation whose latch never commits. R53’s no-kill witness supplies the dropped-write example. |
10: | ILC3-02 — spread is not interval membership | **CLOSED** | R53 records fetch-start times and checks membership in the decision’s completed window. The earlier one-poll-per-tick claim is explicitly withdrawn at [RESULTS:790](/home/tony/projects/tessera/formal/tla/issuer-lifecycle/RESULTS.md:790). |
11: | ILC3-03 — fixed window strands | **CLOSED for the fixed-window defect** | The window now rolls. Recovery after a gap is reachable; B8 preserves the broken fixed-window behavior. The broader termination claim needs ILC4-02’s qualification. |
12: | ILC3-04 — live material expires | **PARTIAL** | [Design:171](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:171) adds live-object protection, but its tagging mechanism does not establish 30-day retention after ending. |
13: 
14: **B. R53 spot-check**
15: 
16: **P5 now asserts the requested property.** [Win:267](/home/tony/projects/tessera/formal/tla/issuer-lifecycle/IssuerLifecycleR53.tla:267) selects the most recent completed intervals. At the ending commit, [lines 377–381](/home/tony/projects/tessera/formal/tla/issuer-lifecycle/IssuerLifecycleR53.tla:377) require enough of those intervals to contain committed failed fetches whose **fetch-start time** belongs to that interval.
17: 
18: The window is evaluated at `w.dec`, the ending decision time, rather than the later store-commit time. That matches the requested **decision’s window**. It does not prove continuous unavailability, protect an uncommitted success, or establish the shipping obligation.
19: 
20: **Allowance-1 termination is meaningful at its stated bounds.** I reproduced the original run: **19,487 distinct states, termination green**. Removing the extra MaxTime start also produced green with the same state count. Thus this particular positive result does not depend on the end-of-time relief.
21: 
22: Its limits remain substantial:
23: 
24: - N=1, Expected=2, Allowance=1, no faults, one invocation start per tick, and the stated fairness/write-resolution assumptions.
25: - It does not establish termination for registered N=3 or arbitrary operating periods.
26: - A scratch N=2 probe, restricted to permanently pending evidence, went red after allocating attempt 2 at time 4 and exhausting polling at MaxTime=7. That is a **horizon artifact**, not evidence of unbounded nontermination. A multi-attempt check needs sufficient horizon and explicit treatment of the bound.
27: 
28: **The companions are real broken designs.**
29: 
30: | Companion | Mutation and significance |
31: |---|---|
32: | **B4** | Ends after elapsed time and one failed poll, without historical window coverage or the second fetch. P5 correctly rejects it; I reproduced red. |
33: | **B6** | Uses a failure counter instead of interval membership. Bursts can satisfy the counter despite missing intervals. Its reported P5 failure matches the mutation. |
34: | **B7** | Uses the same counter design at one invocation start per tick. Fence delay still separates invocation start from fetch start. I reproduced the old spread property failing. |
35: | **B8** | Requires coverage of the original fixed window. A missed interval remains irrecoverable. I reproduced the exhaustive “no end after a gap” result: **488,041 states**. This is deliberately a green invariant describing broken behavior. |
36: 
37: [RESULTS:859](/home/tony/projects/tessera/formal/tla/issuer-lifecycle/RESULTS.md:859) accurately lists the omissions: B2, no-fence B5, sanity witnesses, one-poll residual witnesses, earlier variants, and multi-attempt termination. These omissions do not erase the checked repairs. They do mean:
38: 
39: - R53 has no fresh positive sanity evidence for every lifecycle outcome.
40: - The fence companion’s sensitivity remains inherited evidence; R53 freshly checks only the correct side.
41: - Storage, signer authorization, external-work idempotence, signing closure, and post-latch assembly remain outside this model’s assurance.
42: 
43: **C. Implementation boundary and author decision**
44: 
45: After correcting storage retention, these can proceed: attempt isolation, immutable attempt material, single-writer lifecycle, fencing and version guards, preserved-presentation latch, complete-negative expiry/discard, atomic end-and-allocate, atomic final refusal, and the public view.
46: 
47: They are common machinery for the author’s stated options. No implementation can be guaranteed immune to arbitrary future author changes, but these choices do not presuppose which obligation yields.
48: 
49: Exactly these behaviors must remain gated:
50: 
51: - Committing `EVIDENCE_UNAVAILABLE` from sampled failure.
52: - Ending or allocating a successor **because of that condition**.
53: - Final refusal, cleanup, or terminal public status derived from that condition.
54: - Any replacement timeout, “signing closed,” deployment deadline, or age rule that produces the same ending indirectly.
55: - Claims of full lifecycle compliance or guaranteed termination while this path remains disabled.
56: 
57: Failure-history collection can remain diagnostic. With the gate closed, incomplete evidence leaves the attempt open; final refusal still operates when N attempts have ended through permitted paths.
58: 
59: The author decision identifies a real conflict, but needs the qualifications in ILC4-03:
60: 
61: | Option | Consequence |
62: |---|---|
63: | **Shipping yields after sustained sampled failure** | An amendment authorizes ending despite potentially timely eligibility, defines the sampling rule, and accepts lost shipping opportunities. |
64: | **Termination yields** | Preserve open attempts and retry recovery indefinitely. This preserves the opportunity to ship; it cannot manufacture permanently lost evidence. |
65: | **A long operating period** | Delays the tradeoff and may reduce exposure. Any finite period retains the counterexample; length alone resolves neither obligation. Coverage parameters also need ILC4-02’s repair. |
66: 
67: A2.1’s permission is specifically **lag exceeds S**, not “now exceeds the deadline”:
68: 
69: - Under **service-observation B**, path (b) may fall outside the shipping guarantee when observation lag exceeds S. Failed samples alone do not establish that antecedent. Path (a) includes protected timely observations, but “observed before the deadline” and `B−C≤S` are not interchangeable tests.
70: - Under **burial-time B**, timely burial remains timely despite missing issuer observations. Later failed fetches do not establish excessive burial lag.
71: - Under either reading, an already protected eligibility cannot acquire refusal permission merely because persistence failed or time passed. The author should reconcile the prose/model meanings explicitly.
72: 
73: **D. New findings**
74: 
75: **ILC4-01 — Medium: tagging `ended` does not start a post-end retention clock.**
76: 
77: [Design:174](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:174) changes the age rule to an `ended` tag filter while promising 30 days after ending. S3’s age-based expiration remains based on object creation; an old object can become immediately eligible when tagged. [AWS lifecycle documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html)
78: 
79: This matters for preserved presentations and results written before a delayed terminal commit. Protect live objects, then base deletion eligibility on a persisted **request-ended timestamp**. An age backstop must not undercut that retention. This is the blocker within the requested ungated scope.
80: 
81: **ILC4-02 — Medium: allowance ≥1 is insufficient for arbitrary operating periods.**
82: 
83: [Design:89–93](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:89) permits arbitrary whole-number periods with allowance ≥1. The positive model covers only two intervals.
84: 
85: A scratch four-interval, allowance-1 probe found termination red. Fetches at `2,2,4,4,6,6,8,8…` leave only two of every four completed intervals covered; three are required. The alternating pattern can continue beyond the finite horizon.
86: 
87: Constrain the supported parameters or establish a scheduling/coverage assumption sufficient for them. “Allowance at least 1” alone is not that assumption. This affects the gated path.
88: 
89: **ILC4-03 — Medium: the conflict paragraph overstates what waiting achieves and which residuals are protected.**
90: 
91: [Design:118–124](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:118) says both paths violate shipping and that never ending “does the reverse.” Under observation-time B, path (b) need not be protected. Under permanent evidence loss, waiting does not ensure shipping.
92: 
93: State the conflict over **protected timely-eligible cases**, distinguish retaining an opportunity from achieving shipment, and distinguish the lag test from the deadline test. The author decision remains necessary.
94: 
95: **Owner prechecks**
96: 
97: | Check | Result | File:line evidence |
98: |---|---|---|
99: | **1. Capture row** | **PASS** | [Design:19](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:19) makes no attacker-key rejection or capture-visibility claim. [V1-CONTRACT:37](/home/tony/projects/tessera/docs/V1-CONTRACT.md:37) and §4 retain the dual-capture limitation. |
100: | **2. Trigger clause** | **PASS, with step 5 gated** | [Design:125](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:125) withholds implementation pending amendment. The citation at line 99 does **not** independently authorize ending; ILC4-03 requires clearer framing. |
101: | **3. Requester** | **PASS** | [Design:17](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:17) specifies signing/stamping order without claiming custody alone provides security. [A9:401](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:401) explicitly recognizes queue-controller signing capability. Signer authorization is not certified here. |
102: | **4. Binding text** | **PASS for the gated proposal** | [Design:121–126](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:121) identifies the departure and reserves authorization to an author amendment. Disabling that path does not itself discharge A2.3 termination. |
103: 

=== FILE (new): docs/reviews/issuance-lifecycle/CODEX-CONFIRM.md
1: **Verdict: not ready to implement.** The revision fixes the predicate definition, removes the early latch cutoff, and corrects the twelve-day claim. Step 3 still does not establish latch-winning atomicity; steps 4 and 6 introduce additional ways to discard protected attempts.
2: 
3: Review was read-only. Scratch enumeration is in [interleavings.txt](/tmp/tmp.f0QJh9236H/interleavings.txt). No repository edits or git writes were made.
4: 
5: ### A. Confirmation of IL-01–07
6: 
7: Here, **CLOSED** means the revised design addresses the finding, not that implementation conformance has been established.
8: 
9: | Finding | Status | Assessment |
10: |---|---|---|
11: | **IL-01: eligibility definition** | **CLOSED** | [Revision:18–22](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:18) includes authenticated, attempt-bound evidence, six-deep burial, and all three conjuncts. This matches A2.1’s “**full three-conjunct temporal predicate**” ([A2:91–94](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:91)), A2.2’s `declared − ε ≤ anchor_time`, `anchor_time ≤ declared + δ`, and `confirmed_at ≤ declared + δ` ([A2:220–224](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:220)). A3.7.3 expressly retains “the three-conjunct temporal predicate plus the burial-depth requirement,” without requiring the whole envelope verification at ship ([A3:659–673](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-3.md:659)). |
12: | **IL-02: latch boundary and atomicity** | **PARTIAL** | The prohibited margin is removed at revision:47–48, 81–83. However, re-observation plus CAS does not meet “**inclusive and latch-winning**” or “**Atomicity of the latch against the expiry transition**” ([A2:153–160](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:153)). See ILC-01. |
13: | **IL-03: late-observation policy** | **CLOSED** | [Revision:58–59](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:58) consistently permits late-observed eligibility while open and prohibits reopening expired attempts. A2.1 says an attempt whose lag exceeds S “**may be refused**” ([A2:135–138](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:135)); refusal is optional. The policy is permissible, although its concurrency implementation remains defective. |
14: | **IL-04: nominal budget** | **CLOSED** | Revision:33–34, 79–80 correctly follow “a **nominal lifecycle budget**” and “**not a proven wall-clock bound**” ([A2:271–274](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:271)). |
15: | **IL-05: durable refusal and API** | **PARTIAL** | Revision:67–71 specifies atomic durable refusal and API delivery; revision:91 includes CL-03’s reason set. These address “**explicit refusal, durably recorded**” and refusal “**in the same step**” as final expiry ([A2:265–281](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:265)). A9.7 row 12 substitutes “**Bounded local refusal returned by the API**” ([A9:476](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:476)). But `EVIDENCE_UNAVAILABLE` lacks a safe terminal-transition rule; see ILC-03. |
16: | **IL-06: change inventory/public semantics** | **CLOSED** | Revision:85–105 incorporates the identified implementation, test and prose sites. Revision:78–80 withdraws misleading `fail_after` semantics. This closes the design inventory finding; it does not certify that future edits cover every dependency. |
17: | **IL-07: isolation and failure handling** | **PARTIAL** | Attempt isolation and signing closure are substantially addressed. Revision:64 follows A9.5: “**A retry that changes any committed byte needs a fresh stamp**”; the registered order freezes signatures before stamping ([A9:290–296](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:290)). Permanent-failure classification and post-latch discard remain underspecified; see ILC-02 and ILC-04. |
18: 
19: The profile was checked using `git show 270ca49:docs/V1-PROFILE.md`. Its §7.1 states:
20: 
21: > “T is the time of the verified attestation at the **lowest block height** in the presented OTS proof” — lines 860–862.
22: 
23: > “It is presentation-sensitive: a different presentation of the same receipt can select a different T.” — lines 861–862.
24: 
25: Qualification requires the pinned, linked `h…h+5` segment, and an incomplete branch “supplies no time or trust fact” — lines 879–888. These qualifications are central to the remaining defects.
26: 
27: ### B. Step 3 concurrency review
28: 
29: **ILC-01 — High: re-observation does not make a timely observation win.**
30: 
31: Affected text: [revision:45–59](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:45), especially the assertion at lines 54–56.
32: 
33: Let L be the latching worker and E the expiring worker. Both initially read version v, OPEN.
34: 
35: | Interleaving or condition | Result |
36: |---|---|
37: | L observes qualifying evidence by B and commits its latch before E’s CAS | Safe: E’s CAS fails. |
38: | E reads first; L subsequently commits; E then tries its old-version write | Safe: E’s CAS fails. |
39: | L observes by B; its write stalls; E reads OPEN after B, independently fetches an older/pending proof, and commits expiry | **Violation:** L’s CAS subsequently fails. A timely-eligible attempt expires. |
40: | E fetches partial evidence; L has the complete pinned segment; E treats “predicate not established” as false | **Same violation.** Successful fetching is not proof of completeness or absence. |
41: | L crashes after timely observation but before its write; E later obtains poorer evidence | No durable observation protects the attempt. It may expire. Crash recovery is unspecified. |
42: | E fetches pending evidence; OTS upgrade becomes available; L fetches it by B; E delays its expiry write until after B | **Violation possible.** E’s decision is based on evidence that no longer represents what another worker observed. |
43: | Both independently fetch the same complete qualifying evidence | E cannot legitimately conclude false. Re-observation works in this restricted case. |
44: | Explorers disagree | Neither “the latest fetch wins” nor one worker’s failure establishes authoritative absence. The design gives no reconciliation rule. |
45: | A reorganisation shallower than six displaces a successor near the tip | It can disrupt a newly six-deep observation without removing its inclusion block. A later fetch can lack the former six-header view. Re-fetching must not silently erase the preserved authenticated observation; pin conflicts require explicit handling. |
46: | Workers’ wall clocks differ | One can decide “after B” while another records “at B.” The note does not define a common lifecycle clock or ordering that makes these decisions consistent. Its visibility tolerance supplies neither. |
47: 
48: A small exhaustive enumeration of the six read/observe/write events, constrained so L’s timely observation precedes E’s post-B fetch, produced **10 schedules; expiry won in three** when E received stale negative evidence. This is a bounded counterexample enumeration, not a model discharge.
49: 
50: The decisive schedule is:
51: 
52: ```text
53: L reads v
54: L observes qualifying evidence at B
55: E reads v, OPEN
56: E reads time > B and fetches stale/pending evidence
57: E CAS(v → EXPIRED) succeeds
58: L CAS(v → LATCHED) fails
59: ```
60: 
61: CAS establishes exclusive writes. It does **not** establish precedence of an earlier observation over a later terminal write. Step 3 therefore **does not meet the registered latch obligation**.
62: 
63: For a fixed, correctly authenticated presentation, these races do not by themselves allow a false predicate to latch: step 2 still requires it to hold. Accepting an observation after B is also expressly permitted by this design. However, the design must distinguish a valid latch on one presentation from a later, different presentation that fails.
64: 
65: The repair must specify how observation and terminal decisions are serialized, how pending observations survive crashes, and how stale/partial evidence is distinguished from a conclusive negative. Another CAS alone is insufficient.
66: 
67: **ILC-03 — High: the unavailable-evidence timeout bypasses the protection step 3 needs.**
68: 
69: Affected text: [revision:56–59, 67–71](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:56).
70: 
71: “Evidence unavailable means do not expire” permits an **unbounded wait** under an indefinitely unavailable source. Calling twelve days nominal is correct, but A2.3 still makes termination a contract obligation ([A2:288–289](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:288)).
72: 
73: Step 6 supplies a finite operating timeout, but elapsed time alone does not establish its authorization:
74: 
75: - A2.1 permits refusal when the observation lag exceeds S.
76: - An outage at E does not establish that no worker observed eligibility by B.
77: - A timely observation may be pending, crashed before persistence, or durably latched elsewhere.
78: - Step 6 does not expressly restrict this refusal to an unlatched OPEN attempt or make it respect the latch/expiry serialization.
79: 
80: Consequently, **step 6 is not demonstrated consistent with A2.1 and A2.3**. A finite refusal policy can be compatible for genuinely unprotected attempts; this note does not define how it establishes that condition. It must never refuse a latched attempt merely because evidence later becomes unavailable.
81: 
82: ### C. Discard, signing closure and shipping
83: 
84: **ILC-02 — High: step 4’s example does not establish permanent failure.**
85: 
86: Affected text: [revision:60–62](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:60).
87: 
88: A2.1 authorizes discard when:
89: 
90: > “the predicate fails **at issuance time**” — [A2:161–162](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:161).
91: 
92: It does not make every unsuccessful evidence fetch an irrevocable failure.
93: 
94: A currently presented proof whose lowest qualifying height has a late timestamp can later acquire a **lower qualifying attestation**. The selected T and confirmation segment then change. With nonmonotone header times, neither height order nor one late timestamp proves every possible qualifying presentation fails.
95: 
96: Thus step 4 is consistent **only when permanence is actually established**. Its example, as written, establishes failure of the current presentation, not permanent failure of the attempt. It could discard an attempt for which another worker already holds timely qualifying evidence.
97: 
98: Signing closure in [revision:63–66](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:63) is otherwise sound: it prevents fresh signatures while preserving latched and already signed/stamped attempts that can finish. Refusal for `SIGNING_CLOSED` must occur only after the current attempt has legitimately ended and a fresh attempt would require prohibited signing.
99: 
100: **ILC-04 — Medium: step 7 has a valid safety exception but an overbroad discard category.**
101: 
102: Affected text: [revision:72–77](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:72).
103: 
104: Two registered constraints limit shipping:
105: 
106: > “a receipt ships only when complete; an operator refusal never concerns a shipped receipt” — [A9:165](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:165).
107: 
108: > “An attempt whose T would exceed not-after is not shipped.” — [A9:422–423](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:422).
109: 
110: Accordingly, **a temporal latch does not compel shipping an incomplete or otherwise prohibited receipt**. Step 7’s genuine, irreparable `T > not-after` case is consistent with the issuer invariant. Neither the temporal predicate nor A3.7.3 establishes full envelope validity.
111: 
112: However:
113: 
114: - “A verifier verdict other than `VALID_STRICT`” is not itself evidence of permanent failure.
115: - Missing snapshots, proofs, headers or storage objects can be recoverable.
116: - A different proof can select a different T; the issuer must preserve the qualifying presentation rather than replace it with a worse one and call the result incurable.
117: - A2.1:161–162 addresses failure of the temporal predicate, not arbitrary post-latch finalization failures.
118: 
119: **Step 7 honours the shipping obligation only if “permanent” means that the frozen attempt cannot be completed lawfully, including by recovering evidence and using its preserved qualifying proof.** As written, it does not establish that restriction tightly enough. A valid, complete, timely-eligible attempt must not be discarded for scheduling delay, transient dependency failure, or an avoidable change of presentation.
120: 
121: ### D. Additional defect
122: 
123: **ILC-05 — Medium: terminal-state guards and retry recovery remain unspecified.**
124: 
125: At [revision:45–75](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:45), step 2 describes a CAS latch without explicitly requiring OPEN/current-attempt state; steps 4 and 7 do not specify equivalent guarded discard transitions. Step 5 also leaves recovery between ending attempt i and creating i+1 undefined.
126: 
127: Require explicit transition guards, atomic attempt allocation or idempotent recovery, and re-evaluation after CAS failure. Otherwise delayed workers can act on ended attempts, retries can duplicate, or a crash can leave the request between attempts. “An expired attempt is never reopened” states the intended invariant but does not specify its enforcement.
128: 
129: ### Owner prechecks
130: 
131: | Check | Result | Evidence |
132: |---|---|---|
133: | **1. Capture row** | **PASS** | Revision:18–22, 41–44 makes no claim that dual-channel capture rejects attacker keys or reveals capture. [Contract:35–37, 72–73](/home/tony/projects/tessera/docs/V1-CONTRACT.md:35) still governs: attacker-key receipts can pass; issuing-account capture permits signing. |
134: | **2. Trigger clause** | **FAIL** | Revision:60–62 treats failure of one presented proof as permanent attempt failure. Revision:67–71 uses evidence unavailability as a refusal trigger without establishing absence of protected timely eligibility. Neither cited registered consequence follows from those facts alone. |
135: | **3. Requester** | **PASS** | Revision:41–44, 63–66 discusses attempt-labelled signature work and signing closure; it makes no security claim based solely on key location or independent signer control. This does not establish requester authorization conformance. |
136: | **4. Binding text** | **FAIL** | Revision:54–56 asserts a latch guarantee its mechanism does not provide. Revision:60–62 and 67–71 permit terminal outcomes without establishing their compatibility with A2.1’s protected eligibility. Owner operating numbers cannot override that registered obligation. |
137: 

=== FILE (new): docs/reviews/issuance-lifecycle/CODEX-REVIEW.md
1: **Verdict: not ready to implement.** The direction is correct, but the eligibility definition, latch boundary, and claimed lifecycle bound need correction first.
2: 
3: Review was read-only. I checked the registered amendments, the profile at `270ca49`, the verifier and issuer, and searched `service/` and `docs/` for the requested strings.
4: 
5: 1. **IL-01 — High: eligibility is incompletely defined.**  
6:    [Design lines 18–20 and 29–31](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:18) identify eligibility with rows 12.2/12.3. Those rows are only two comparisons; they neither establish an authenticated anchor nor check the lower temporal bound.
7: 
8:    Registered authority:
9: 
10:    > “The issuer evaluates this conjunct **as part of the full three-conjunct temporal predicate**” — [A2.1:91–94](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:91).
11: 
12:    > `declared_issue_time − ε ≤ anchor_time`  
13:    > `anchor_time ≤ declared_issue_time + δ`  
14:    > `confirmed_at ≤ declared_issue_time + δ` — [A2.2:220–224](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:220).
15: 
16:    [A3.7.3:659–673](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-3.md:659) explicitly preserves the **burial-depth requirement** alongside those three conjuncts, while distinguishing them from the whole `VALID_STRICT` verdict. A9.7 explicitly leaves A2.1’s predicate unchanged.
17: 
18:    For V1, the evidence must concern the attempt’s frozen `A_sig`: [A9.5:290–296](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:290) requires stamping `SHA256(A_sig)` and freezing signatures before stamping. Frozen profile §7.1, lines 860–900, requires selecting the lowest qualifying height, with the complete pinned, linked `h…h+5` segment; `confirmed_at` comes from that same selected branch.
19: 
20:    **Correction:** define eligibility over authenticated, attempt-bound evidence with six confirmations and all three temporal conjuncts. Keep the remaining pre-ship checks distinct. Rows 12.2/12.3 alone are insufficient.
21: 
22: 2. **IL-02 — High: CF2-01’s early cutoff contradicts the registered latch boundary.**  
23:    [Design lines 38–42](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:38) require the latch decision at least `WRITE_LEASE_S` before expiry. That excludes eligibility observed during the final 15 minutes, including the exact registered boundary.
24: 
25:    Registered authority:
26: 
27:    > “Eligibility observed at exactly `B = declared + δ + S` is timely — the boundary is **inclusive and latch-winning**” — [A2.1:153–156](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:153).
28: 
29:    > “Expiry … applies only **strictly after** the boundary, and only to attempts with no timely-latched eligibility. Atomicity of the latch against the expiry transition is part of the mutual-exclusion construction obligation” — A2.1:157–160.
30: 
31:    CF2-01 addressed the owner’s requirement that **completion become visible before a deadline**. Registered eligibility instead protects an observation from subsequent packaging and scheduling delay. An owner write-lease rule cannot move that observation boundary earlier.
32: 
33:    A compare-and-set prevents both terminal transitions winning against the same record version; it does **not** alone ensure that timely observation wins. For example, one worker observes eligibility at the boundary, its write stalls, and another worker expires the unchanged record afterward.
34: 
35:    **Correction:** specify serialization of evidence observation, latch and expiry, including delayed writes and crash recovery. Expiry must account for pending timely observations. Any AWS commit-latency assumption remains an assumption; the existing clock-tolerance decision does not authorize shrinking A2’s boundary.
36: 
37: 3. **IL-03 — Medium: permitting late-observed eligibility is allowed, but step 4 contradicts itself.**  
38:    The permissive choice at [design lines 40–42](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:40) is compatible with:
39: 
40:    > “An attempt whose lag exceeds S **may be refused**” — [A2.1:135–138](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:135).
41: 
42:    “May” does not require refusal. Accepting authenticated chain-valid evidence observed after the nominal boundary, before an irreversible expiry decision, is a permissible policy choice. It cannot revive an already expired/refused attempt.
43: 
44:    But “latch whenever the predicate holds before expiry is decided” conflicts with the preceding requirement to decide the latch **15 minutes before** the boundary. State one consistent policy: mandatory protection for timely eligibility, optional acceptance of late observations while the attempt remains open, and no reopening after expiry.
45: 
46: 4. **IL-04 — Medium: twelve days is a nominal budget, not an upper bound.**  
47:    [Design lines 44 and 49](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:44) say the request ends “at up to” `N × (δ + S)`, plus clock tolerance. The registration explicitly disclaims that conclusion:
48: 
49:    > “a **nominal lifecycle budget** … a nominal budget, **not a proven wall-clock bound on the process**” — [A2.3:271–274](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:271).
50: 
51:    > “termination is a contract obligation on the implementation, not a proven liveness property” — A2.3:288–289.
52: 
53:    Polling outages, delayed retry starts, and latched finalization can exceed twelve days. The optional late-observation policy further prevents treating this arithmetic as a hard bound.
54: 
55:    **Correction:** describe twelve days as nominal attempt-window budgeting. Do not turn it into a replacement request deadline.
56: 
57: 5. **IL-05 — Medium: specify V1’s atomic durable refusal and API outcome; do not import portable-refusal machinery.**  
58:    [Design lines 21 and 36–37](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:21) correctly require explicit refusal, but the implementation section should require the terminal state and reason to become durable together.
59: 
60:    Registered authority:
61: 
62:    > “explicit refusal, durably recorded” — [A2.3:265–268](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:265).
63: 
64:    > “the transition expiring the final attempt’s window records the refusal in the same step” — A2.3:279–281.
65: 
66:    A3 adds portable records, commitments, handoff and publication. However, [A9.7 row 12:476](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:476) replaces the refusal-record decomposition with:
67: 
68:    > “Bounded local refusal returned by the API”.
69: 
70:    Thus V1 needs an atomic, final, locally durable refusal with a reason, exposed through its authenticated API and retained under its declared policy. It does **not** need A3’s portable record, public commitment, publication channel or acknowledgment workflow. “Recorded reason” suffices only if it means durable terminal operator state, not merely a log message.
71: 
72:    The owner-document list also misses [CL-03 item 1:34–35](/home/tony/projects/tessera/docs/V1-CLARIFICATIONS.md:34): its closed reason set lacks `ATTEMPTS_EXHAUSTED` and `SIGNING_CLOSED`, and associates accepted-request failures with `FAILED`.
73: 
74: 6. **IL-06 — Medium: the change inventory omits operational deadline sites and tests.**  
75:    The listed documents cover the principal prose locations, apart from CL-03 item 1. They do not enumerate every executable use of the old rule.
76: 
77:    The requested search found these active implementation sites:
78: 
79:    | File | Locations requiring review |
80:    |---|---|
81:    | [service.py](/home/tony/projects/tessera/service/issuer/tessera_issue/service.py:7) | `DEADLINE_S`, line 7 |
82:    | [api.py](/home/tony/projects/tessera/service/issuer/tessera_issue/api.py:52) | completion settlement, lines 52–75; `fail_after`, line 94; import, line 12 |
83:    | [pipeline.py](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:81) | `_end`, lines 84–85; `advance`, 149–150; signer `sign_by`, 263; post-check rejection, 480–481; header commentary/import |
84:    | [test_faults.py](/home/tony/projects/tessera/service/issuer/tests/test_faults.py:125) | deadline expectations, lines 125–144 and 181 |
85:    | [test_review_fixes.py](/home/tony/projects/tessera/service/issuer/tests/test_review_fixes.py:95) | deadline-crossing expectations, lines 95–106 |
86:    | [test_confirm_fixes.py](/home/tony/projects/tessera/service/issuer/tests/test_confirm_fixes.py:46) | deadline fixtures and CF2-01 expectations, including lines 46, 178 and 198 onward |
87: 
88:    The authoritative prose sites are S4, L1, CL-03, the clock-tolerance decision and issuer `DESIGN.md`, as anticipated. Historical issuer reviews and dispositions also contain the old rule: preserve their historical text and add a supersession pointer where they serve as current implementation guidance.
89: 
90:    Other matches describe **ε**, **S**, or the retirement margin; those are separate rules and should retain their registered values.
91: 
92:    Finally, `fail_after = current attempt expiry` becomes misleading once eligibility latches, and it never promises request termination when another attempt remains. Specify its public semantics for retries and finalization.
93: 
94: 7. **IL-07 — Medium: retry isolation and post-latch failure handling need design decisions.**  
95:    The attempt list is a start, but [design steps 1–3](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:28) omit several consequential transitions.
96: 
97:    Registered authority:
98: 
99:    > “A retry that changes any committed byte needs a fresh stamp” — [A9.5:295](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:295).
100: 
101:    > “If the predicate fails at issuance time, the attempt is discarded and re-issued … subject to the attempt bound” — [A2.1:161–162](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:161).
102: 
103:    Before implementation, specify:
104: 
105:    - **Attempt isolation:** separate frames, signature jobs, proofs and latch evidence by attempt identity. Current work-object names are reused, and signature-response handling resolves through the request’s current jobs ([pipeline.py:194–214](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:194)). A late response must never populate a later attempt.
106:    - **Known-invalid evidence:** define discard/retry when a temporal conjunct fails, rather than only retrying after wall expiry.
107:    - **Finalization failures:** distinguish retryable packaging/evidence unavailability from irreversible refusal. Current pre-ship paths recapture snapshots or end `FAILED` ([pipeline.py:475–491](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:475)); merely adding a latch will not resolve their interaction with the shipping obligation.
108:    - **Signing closure:** closing signing prevents fresh signatures; it does not itself justify expiring an already latched attempt or abandoning an already signed attempt that can finish without more signing.
109: 
110:    The design correctly states `N = 3`, strict per-attempt expiry after `declared + δ + S`, and A9’s no-ship invariant for `T > not-after`. The new acceptance margin is an owner operating choice, not a registered guarantee of completion.
111: 
112: The owner prechecks, applied to the design note:
113: 
114: | Check | Result | Evidence |
115: |---|---|---|
116: | **1. Capture row** | **PASS** | [Lines 18–24](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:18) make lifecycle claims, with no claim that dual-channel capture rejects attacker keys or exposes capture. The contract’s attacker-key acceptance remains applicable. |
117: | **2. Trigger clause** | **FAIL** | [Lines 38–42](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:38) transplant CF2-01’s completion-deadline consequence into eligibility latching. That deadline requirement is being removed; registered latch precedence governs instead. |
118: | **3. Requester** | **PASS** | [Lines 13–14 and 35–37](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:13) require fresh signing and respect signing controls; they make no key-storage or independent-approval security claim. This pass does not establish isolation of retry jobs. |
119: | **4. Binding text** | **FAIL** | [Lines 18–19, 38–39 and 44–49](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:18) respectively narrow the registered predicate, impose a contradictory owner latch cutoff, and promote nominal budgeting into an upper bound. |

=== FILE (new): docs/reviews/issuer-lifecycle-impl/CODEX-CONFIRM-10.md
1: **Ready for deployment work with the step-5 gate closed; remaining termination limits await the author’s decision.**
2: 
3: - **Verification:** [234 passed](/tmp/tessera-confirm10.25NtwLy4/suite.log). Reran both original probes: their old starvation assertions fail because progress now occurs—resume-gap adoption on poll 2, admission-case adoption on poll 1, for either first slot. [Positive versions: 6 passed](/tmp/tessera-confirm10.25NtwLy4/positive.log).
4: - **Storage authority:** [Terraform](/home/tony/projects/tessera/service/issuer/infra/main.tf:236) grants the poller writes to `work/*`. The API writes only `content/*`; signer roles can read `frames/*` but cannot write signatures. “Existence means verified” therefore depends on trusted poller writes and storage integrity. These are repository IAM findings, not verification of deployed policies or additional administrator grants.
5: - **Forged/corrupted objects:** [Four probes passed](/tmp/tessera-confirm10.25NtwLy4/storage3.log). A digest-matching forged object can be adopted and logged without verification, including through redelivery. However, [`_seal`](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:704) rejects its exact bytes before constructing `A_sig`. Overwritten signature bytes also fail the digest check. Neither reached receipt construction through this path.
6: - **Availability consequence:** a digest-matching invalid object remains selectable by `_reconcile`; sealing clears the job, then reconciliation adopts it again. The probe reproduced six such turns, including after signing closure. This permits an indefinite signing stall under storage poisoning, rather than an incorrect terminal transition. Full poller compromise is broader: its IAM also permits direct result writes.
7: - **Capacity condition:** the stated admission condition now supports advancing the next incomplete durable handling step; the repeated-work gap is fixed. “Each poll” remains conditional on receiving a waiting response—random selection of an empty slot can produce an idle poll. The fairness claim is probabilistic.
8: - **New defects:** no additional blocker found within the trusted-storage assumption. The poisoning stall is a concrete storage-integrity limit, not discharged termination. `ILCI7_ONESTORE` is treated as retired by the owner’s decision.
9: 
10: No repository edits or git writes; all test scratch and basetemp directories stayed under the fresh scratch directory.

=== FILE (new): docs/reviews/issuer-lifecycle-impl/CODEX-CONFIRM-2.md
1: **Verdict: not ready for deployment work, even with the step-5 gate closed.**
2: 
3: Validation: **205 passed in 130.95 seconds**. Seven additional probes passed by reproducing defects. Fourteen targeted mutations were detected: five repair mutations, eight client-guard bypasses, and `GATE`. No repository edits or git writes.
4: 
5: Evidence: [additional probes](/tmp/tmp.iALl276cQE/test_round2.py), [results](/tmp/tmp.iALl276cQE/round2-final.log), [suite](/tmp/tmp.iALl276cQE/suite.log), [mutations](/tmp/tmp.iALl276cQE/mutations.log). No deployed AWS or TLC validation.
6: 
7: **A — Previous findings**
8: 
9: | Finding | Status | Assessment |
10: |---|---|---|
11: | ILC-I-01 | **PARTIAL** | The repairable KSK-configuration case is fixed. Blanket retry of row 13.5 introduces the RRSIG failure below. |
12: | ILC-I-02 | **PARTIAL** | Client method admission is substantially implemented. Total invocation bounds remain unestablished. |
13: | ILC-I-03 | **CLOSED** | The original stale-suffix probe now progresses; durable invalidation repairs that scenario. |
14: | ILC-I-04 | **CLOSED** | The recapture stage now evaluates impossibility before capturing. Initial capture has a separate gap below. |
15: | ILC-I-05 | **PARTIAL** | Held qualifying evidence is evaluated first. Calendar cursor persistence can still fail systematically. |
16: | ILC-I-06 | **CLOSED** | The reported classification, refusal-reason, and pre-allocation-content descriptions are reconciled. The new deadline claims have separate defects. |
17: 
18: I reran the original probe file: **8 passed, 4 failed**. Those four failures are old defect-reproduction assertions whose observed behavior has changed as intended. The old raw fake-signer probe still produces 320 seconds because its replacement `send` bypasses the deployed adapters; it does not establish an SQS guard bypass.
19: 
20: **B/F — Findings**
21: 
22: 1. **ILC-I2-01 — High: the deadline guard does not establish “never overrun.”**
23: 
24:    [aws.py:222](/home/tony/projects/tessera/service/issuer/tessera_issue/aws.py:222), [ots.py:314](/home/tony/projects/tessera/service/issuer/tessera_issue/ots.py:314), [dns.py:153](/home/tony/projects/tessera/service/issuer/tessera_issue/dns.py:153), [deadline.py:64](/home/tony/projects/tessera/service/issuer/tessera_issue/deadline.py:64).
25: 
26:    The client-call search found guarded entry points for DynamoDB, S3, SQS, SNS, calendar, explorer, and resolver requests. **It did not establish that every blocking operation is guarded:**
27: 
28:    - **S3:** `get_object` returns before `Body.read()`. The guard has already reset `CALL_TIMEOUT`; body consumption is outside it. A simulated body read advanced the invocation by **400 seconds**.
29:    - **HTTP:** `urlopen` and buffered `read(65536)` can perform multiple blocking reads without revisiting the total deadline. A real local server dripping bytes took **0.416 seconds with a 0.1-second total configured**.
30:    - **DNS:** the remaining time is reused across successive blocking operations. UDP send/receive share one timeout; TCP `sendall` inherits the connection timeout before the next `left()` check. A controlled probe consumed **1.1 seconds against a 1.0-second total**, with each operation respecting its individual allowance. Configurable hostname resolution adds another unbounded component.
31:    - **Pre-ship:** 30 seconds is an admission estimate, with no interruption mechanism.
32:    - The invocation deadline uses the integer wall clock, rather than a monotonic elapsed-time clock.
33: 
34:    **AWS arithmetic:** `3 × (3 + 8) + 2 × 20 = 73 seconds` correctly includes three configured attempts and conservatively allows two maximum backoffs. But connect/read timeouts are not a total-operation deadline; the arithmetic does not bound streamed bodies or all transport activity. See the [Botocore configuration reference](https://docs.aws.amazon.com/botocore/latest/reference/config.html).
35: 
36:    Consequently, DESIGN’s **“stall, no overrun”** envelope is demonstrated for its synthetic clients, not established for the actual transports. Lambda’s eventual hard kill is not graceful deadline enforcement.
37: 
38: 2. **ILC-I2-02 — High: a genuinely expired snapshot RRSIG is retried forever without recapture.**
39: 
40:    [pipeline.py:109](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:109), [dnssec.py:288](/home/tony/projects/tessera/service/verifier/tessera_verify/dnssec.py:288), [verify.py:247](/home/tony/projects/tessera/service/verifier/tessera_verify/verify.py:247).
41: 
42:    I generated correctly signed snapshots valid at capture but expired at their eventual anchor time. The real verifier returned **`INVALID/RRSIG_NOT_VALID_AT_EVAL_TIME`**. Four polls retained the same snapshot in `finalize`; capture count remained **1**.
43: 
44:    This evaluates validity at the snapshot’s **anchored historical time**, not today’s wall time. Waiting cannot repair that signature interval.
45: 
46:    **Yes: this outcome needs a byte/evidence-dependent recapture path**, with impossibility assessed only when the existing presentation’s incurability is established. Classify at the necessary reason/witness level: all of row 13.5 is too broad, but blindly declaring every root-authentication failure configuration-independent would repeat the prior wrongful-discard defect.
47: 
48: 3. **ILC-I2-03 — Medium: calendar work leaves insufficient budget to persist its progress.**
49: 
50:    [pipeline.py:755](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:755).
51: 
52:    `_upgrade` continues while at least **50 seconds** remain. Its subsequent S3 checkpoint requires **73 seconds** of admission allowance.
53: 
54:    With real guarded adapters and 20 pending calendars taking 20 seconds each, **three successive polls asked exactly calendars 0–11**. Each then failed the cursor write:
55: 
56:    > `s3.put_object: worst case 73 s, 40 s available`
57: 
58:    Calendars 12–19 were never reached. Changed proof bytes can likewise fail to persist. Reserve the required checkpoint writes before spending the remaining budget; the local-store cursor test misses this interaction.
59: 
60: 4. **ILC-I2-04 — Medium: active-request enumeration can prevent every request from receiving a turn.**
61: 
62:    [pipeline.py:170](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:170), [aws.py:120](/home/tony/projects/tessera/service/issuer/tessera_issue/aws.py:120).
63: 
64:    `active()` rereads every indexed request before returning anything. The durable scheduling cursor is consulted only afterward.
65: 
66:    **Reproduced with 15 requests and 20-second DynamoDB calls:** three polls exhausted their budgets during enumeration; no request advanced or allocated an attempt. This occurs at the advertised per-call progress latency, rather than the disclosed 30-second slow-store limit.
67: 
68:    Enumeration needs resumable pagination or another bounded scheduling mechanism. Continuous signer-response work can also consume the invocation before enumeration; the request cursor does not provide fairness across those work classes.
69: 
70: 5. **ILC-I2-05 — Medium: initial snapshot rejection still bypasses receipt classification indefinitely.**
71: 
72:    [pipeline.py:650](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:650).
73: 
74:    After stamping the receipt, `st_stamp` requires successful DNS capture before entering `evidence`. Persistent malformed captures therefore prevent evaluation of the receipt proof altogether.
75: 
76:    **Reproduced:** after chain progress beyond the attempt’s temporal limit, four further polls remained at `stamp`. The new impossibility check repairs *recapture after finalization*, not this initial-capture path.
77: 
78:    An obtainable, conclusive negative receipt should not be hidden behind successful snapshot acquisition. Snapshot impossibility may need additional evidence, but receipt classification can proceed independently.
79: 
80: **C — Deviations**
81: 
82: | Deviation | Judgment |
83: |---|---|
84: | Smaller SDK configuration | **No CF3-01 regression:** its test passes. Three total attempts means fewer opportunities to recover from transient errors than the former four. Standard retries still handle throttling, subject to retry quota; exhausted retries surface errors for later poll retries. This trades immediate resilience for shorter waits and does not itself prove a total bound. No live throttling experiment was performed. See [AWS retry behavior](https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html). |
85: | Configuration-dependent snapshot retries | Keeping KSK/reliance-period failures and header-dependent 13.4 outcomes repairable is appropriate. Treating **every 13.5 outcome** that way is defective: ILC-I2-02. |
86: | Six-header segment stored together | **Sound as a cache optimization:** [pipeline.py:715](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:715) checks size and linkage before using it; per-height recovery remains. It changes neither receipt eligibility nor the chain assumptions. It is not independent authentication against arbitrary store corruption. |
87: 
88: **D — Step-5 gate**
89: 
90: **Still closed.** Diagnostic failure history authorizes no ending, successor, refusal, or cleanup. The targeted `GATE` mutation fails the never-completes test. The defects above do not enable sampled-unavailability refusal.
91: 
92: **E — Remaining ways to stay open indefinitely outside that gate**
93: 
94: | Path | Assessment |
95: |---|---|
96: | Irreparable RRSIG failure retained in `finalize` | **Defect:** ILC-I2-02. |
97: | Calendar progress/cursor repeatedly lost | **Defect:** ILC-I2-03. |
98: | Enumeration or continuously replenished response work prevents scheduling | **Defect:** ILC-I2-04. |
99: | Initial snapshot capture repeatedly rejected | **Defect:** ILC-I2-05. |
100: | A stage repeatedly exceeds the available budget before its durable completion | **Stated slow-store limit**, provided described as a progress limitation; the claimed no-overrun guarantee remains defective. |
101: | Snapshot recapture where impossibility cannot be proved—pending proof, unobtainable MTP headers, or insufficient chain progress | **Stated limit.** Absence of an impossibility proof cannot authorize discard. |
102: | Latched snapshot proof never becomes usable; permanently missing preserved presentation or assembly material | **Stated external-evidence/storage limit.** Outside the unlatched step-5 ending policy. |
103: | Unrepaired catalog, trust configuration, verifier availability, or persistent header/presentation disagreement | **Stated operator/dependency limit.** No age-based ending is authorized. |
104: | Persistent store/queue failures, failed guarded commits, or stage exceptions before a terminal write | **Operational limitation**, with no general termination guarantee. Signing closure cannot complete a transition when its prerequisite reads/writes remain unavailable. |
105: | Chain never reaches the git precommitment depth, or initial calendars never accept a stamp | **Dependency limit before evidence processing.** No general finite completion bound follows. |
106: 
107: These limits may be honestly disclosed for bounded development work. Disclosure does **not** discharge [A2.3’s termination obligation](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:288).
108: 
109: **Owner prechecks**
110: 
111: | Check | Result | Evidence |
112: |---|---|---|
113: | Capture row | **PASS** | No reviewed repair claim adds attacker-key rejection or capture visibility. [V1-CONTRACT.md:37](/home/tony/projects/tessera/docs/V1-CONTRACT.md:37) and [§4:72](/home/tony/projects/tessera/docs/V1-CONTRACT.md:72) explicitly permit attacker-key receipts after dual-channel capture. |
114: | Trigger clause | **PASS** | [pipeline.py:948](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:948) now requires a byte-only invalid failure and complete proof before the MTP impossibility consequence. The previous KSK trigger counterexample is repaired. |
115: | Requester | **PASS** | [DESIGN.md:19](/home/tony/projects/tessera/service/issuer/DESIGN.md:19) identifies the issuer’s ability to enqueue signing work; [main.tf:255](/home/tony/projects/tessera/service/issuer/infra/main.tf:255) grants it. Signer authorization in deployment remains unverified. |
116: | Binding text | **FAIL** | [pipeline.py:110](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:110) uses an owner classification to retry incurably invalid snapshots indefinitely; scheduling defects also prevent progress with obtainable evidence. These leave [A2.3:288](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:288) unmet outside the gated policy choice. DESIGN’s disclosure supplies no registered waiver. |
117: 

=== FILE (new): docs/reviews/issuer-lifecycle-impl/CODEX-CONFIRM-3.md
1: **Verdict: not ready for deployment work, even with the gate closed.** One scheduling defect remains with obtainable signer responses; it is separate from permanent-dependency limits awaiting the author.
2: 
3: Validation: **216 passed in 131.49 seconds**. All eight targeted mutations were detected, including `GATE`. Three independent probes passed, reproducing the cold-start defect, checking timely snapshot capture, and measuring drain-share overshoot. No repository edits or git writes; scratch is in [/tmp/tmp.pyt6bZDeCk](/tmp/tmp.pyt6bZDeCk).
4: 
5: | Previous finding | Status | Assessment |
6: |---|---|---|
7: | ILC-I2-01 | **CLOSED under the owner decision** | S3 body consumption is inside the guard; elapsed timing is monotonic. HTTP/DNS/SDK total-time bounds remain stated limits, not established guarantees. |
8: | ILC-I2-02 | **CLOSED** | Expired anchored RRSIG intervals now cause recapture or reach the impossibility proof. Configuration-dependent failures remain retryable. |
9: | ILC-I2-03 | **CLOSED** | Calendar work reserves a checkpoint write. The guarded-adapter regression reaches every calendar. |
10: | ILC-I2-04 | **PARTIAL** | Paged enumeration and request-work allocation repair the original probes. Signer-slot fairness fails across cold starts. |
11: | ILC-I2-05 | **CLOSED for the reproduced defect** | Rejected captures no longer trap receipt processing in `stamp`; a latch without a snapshot enters capture processing. |
12: 
13: The original seven round-2 probes produced **five failed defect-reproduction assertions and two passes**: the five repaired behaviors changed; the accepted HTTP/DNS limits remain reproducible.
14: 
15: **ILC-I3-01 — Medium, DEFECT: signer-slot fairness depends on container reuse.**
16: 
17: [pipeline.py:364](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:364) stores `drain_turn` only on the issuer object. A cold start reconstructs the signers in KMS-first order at [lambda_app.py:46](/home/tony/projects/tessera/service/issuer/tessera_issue/lambda_app.py:46).
18: 
19: With continuously replenished KMS responses and SQS calls taking 20 seconds, I reset only that volatile rotation between polls, retaining stores and queues. After **eight cold-start-equivalent polls**:
20: 
21: - Both KMS signatures were recorded.
22: - Both valid GPG responses remained queued.
23: - The request remained in `signing`.
24: 
25: One warm continuation immediately serviced GPG and advanced the request to `stamp`. This distinguishes scheduling starvation from dependency failure.
26: 
27: The one-third allocation protects request work from continuous draining, but does not ensure fairness **between signer queues** across cold starts. Persist the starting slot or give each slot an independent opportunity before allowing one queue to consume the drain allocation.
28: 
29: Evidence: [probe](/tmp/tmp.pyt6bZDeCk/test_third.py), [output](/tmp/tmp.pyt6bZDeCk/third.log).
30: 
31: **ILC-I3-02 — Low, documentation: “at most a third” overstates the drain allocation.**
32: 
33: [DESIGN.md:224](/home/tony/projects/tessera/service/issuer/DESIGN.md:224) says draining may use “at most a third.” The checks at [pipeline.py:375](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:375) occur between response-processing units, without reserving their remaining cost.
34: 
35: A probe using 60-second SQS calls spent **120 seconds draining against a 96.67-second share**. Describe this as a cooperative allocation checked between units. This is a precision correction, not a reinstatement of the withdrawn total-time guarantee.
36: 
37: The other mechanisms and gate:
38: 
39: - **No-snapshot impossibility:** sound under the existing header/chain assumptions. [pipeline.py:1043](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:1043) requires neither a stored snapshot proof nor a committed snapshot reference before using `NO_SNAPSHOT`; the MTP test then excludes future timely anchors. With MTP still permitting a timely anchor, my independent probe captured a snapshot and advanced to `finalize`. I found no premature discard in this path.
40: - **Paged enumeration:** the DynamoDB continuation token and durable request position repair the original enumeration starvation. Position advances before request work.
41: - **Gate:** **still closed**. Diagnostic failure history authorizes no sampled-unavailability ending. The `GATE` mutation failed the never-completes test and four other lifecycle tests.
42: - **Remaining endings:** I found no additional wrongful-ending defect in the examined paths. The cold-start starvation is the remaining demonstrated implementation defect; permanent dependency failures remain unresolved author-policy cases.
43: 
44: **DESIGN’s termination disclosure is honest**, at [DESIGN.md:187](/home/tony/projects/tessera/service/issuer/DESIGN.md:187): the limits explicitly leave A2.3 unmet, disclosure discharges nothing, and [DESIGN.md:247](/home/tony/projects/tessera/service/issuer/DESIGN.md:247) keeps the ending policy gated. It needs the drain wording correction above and disclosure or repair of ILC-I3-01.
45: 
46: | Owner precheck | Result | Evidence |
47: |---|---|---|
48: | Capture row | **PASS** | The reviewed lifecycle changes add no attacker-key rejection or capture-visibility claim. Dual-channel capture still permits attacker-key receipts: [V1-CONTRACT.md:37](/home/tony/projects/tessera/docs/V1-CONTRACT.md:37), [72](/home/tony/projects/tessera/docs/V1-CONTRACT.md:72). |
49: | Trigger clause | **PASS** | Snapshot discard requires the byte-dependent/completeness conditions or actual absence of a snapshot, plus the MTP exclusion: [pipeline.py:1040](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:1040). |
50: | Requester | **PASS** | The design identifies the issuer as the signing-work requester: [DESIGN.md:19](/home/tony/projects/tessera/service/issuer/DESIGN.md:19); IAM grants queue submission at [main.tf:255](/home/tony/projects/tessera/service/issuer/infra/main.tf:255). Live signer authorization remains unverified. |
51: | Binding text | **FAIL** | Volatile queue rotation can prevent progress despite obtainable responses: [pipeline.py:364](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:364). The permanent-dependency decision supplies no waiver for this scheduling defect against [A2.3:288](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:288). |
52: 
53: Logs: [suite](/tmp/tmp.pyt6bZDeCk/suite.log), [prior probes](/tmp/tmp.pyt6bZDeCk/old-probes.log), [mutations](/tmp/tmp.pyt6bZDeCk/mutations.log). No deployed AWS or TLC validation was performed.
54: 

=== FILE (new): docs/reviews/issuer-lifecycle-impl/CODEX-CONFIRM-4.md
1: **Verdict: not ready for deployment work with the step-5 gate closed; a reduced-budget scheduling defect remains.**
2: 
3: Validation: **217 passed in 130.67 seconds**. No repository edits or git writes; scratch: [/tmp/tmp.6rbTsKov9q](/tmp/tmp.6rbTsKov9q).
4: 
5: **ILC-I4-01 — Medium: rotation can remain stuck when an empty first queue consumes the checkpoint budget.**
6: 
7: At [pipeline.py:392](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:392), an empty batch leaves rotation unchanged. A later non-empty batch triggers the rotation write without reserving its cost.
8: 
9: Independent reproduction, using the real guarded adapters:
10: 
11: - Poll budget **190 seconds**, SQS calls **60 seconds**, KMS empty, two valid GPG responses queued.
12: - Two receives consume 120 seconds, leaving **60 seconds** after the reserve. The rotation write requires **73 seconds** admission and is refused. Request-position writes cannot rescue it under that budget.
13: - After **12 polls**, durable rotation remained zero, both GPG signatures were absent, and both replies remained queued.
14: - Forcing GPG to start under the **same budget** allowed both signatures to be recorded.
15: 
16: This demonstrates avoidable scheduling starvation with obtainable responses. The reproduction uses a reduced budget; the original 290-second scenario is repaired. Evidence: [probe](/tmp/tmp.6rbTsKov9q/test_rotation.py), [log](/tmp/tmp.6rbTsKov9q/rotation.log). Reserve the rotation checkpoint before spending receives, and ensure empty-queue turns advance fairly.
17: 
18: The other requested confirmations:
19: 
20: 1. **Original cold-start probe: repaired.** GPG was served, all four signatures were recorded, and the request reached `evidence`. Its old starvation assertion failed as expected. [Log](/tmp/tmp.6rbTsKov9q/third.log).
21: 2. **Write guarding: yes.** Rotation uses the same deadline-guarded `cursor_put` as other poller-position writes. Reads are strongly consistent; writes are unconditional, with infrastructure limiting the poller to one concurrent invocation. Budget refusal can nevertheless cause ILC-I4-01.
22: 3. **DESIGN drain wording: accurate.** [Lines 224–226](/home/tony/projects/tessera/service/issuer/DESIGN.md:224) correctly describe cooperative allocation and possible overshoot. The rotation statement needs qualification or the repair above.
23: 4. **No other new defect identified in this narrow pass.** Step 5 remains closed; diagnostic unavailability history authorizes no ending.

=== FILE (new): docs/reviews/issuer-lifecycle-impl/CODEX-CONFIRM-5.md
1: **Verdict: not ready for deployment work with the step-5 gate closed until the author explicitly accepts unbounded signer-queue starvation as a stated limit, or it is repaired.**
2: 
3: Validation: **219 passed in 131.69 seconds**. No repository edits or git writes; all scratch is under [/tmp/tmp.vRDSdlYGSl](/tmp/tmp.vRDSdlYGSl).
4: 
5: 1. **Both original probes now serve GPG.** The reduced-budget probe collected all four signatures; its stage remained `signing` under the exhausted budget. The cold-start probe collected all four signatures and reached `evidence`. Their old starvation assertions failed as expected. [Probe log](/tmp/tmp.vRDSdlYGSl/probes.log).
6: 
7: 2. **Parity lock-in remains possible, including with small timing variation.** An independent [probe](/tmp/tmp.vRDSdlYGSl/test_lock.py) used a schedule phase of 599 seconds and alternating delivery delays of zero and two seconds. Starts at `599, 1201, 1799, 2401, …` all select slot 0. With replenished KMS traffic consuming the drain share, **12 polls left both GPG replies uncollected**. One slot-1 start collected both. [Result](/tmp/tmp.vRDSdlYGSl/lock.log).
8: 
9:    Exact 600-second spacing alternates correctly, regardless of fixed phase or constant clock skew. Variable delay or skew near a boundary can repeat parity; servicing only every other schedule window also locks parity. Ten minutes and 600 seconds agree—the vulnerability is sampling actual invocation time.
10: 
11:    Sustained lock-in appears unlikely under independent, varying delivery timing, but there is **no defensible numerical likelihood from the available evidence**. Correlated timing can sustain it indefinitely. EventBridge delivery retries use backoff and jitter; Lambda retries can cluster or cross windows. Neither guarantees a useful opposite-parity invocation. Their retry limits bound individual events, **not queue starvation**. [EventBridge retries](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-rule-retry-policy.html), [Lambda retries](https://docs.aws.amazon.com/lambda/latest/dg/invocation-async-error-handling.html).
12: 
13:    The 14-day response retention bounds preservation, not service: expiry can lose an uncollected reply. Recovery requires a sufficiently budgeted GPG-first invocation, or enough capacity to reach GPG second.
14: 
15: 3. **No other executable defect identified in this narrow pass.** The implementation follows the owner's time-derived-slot decision and removes ILC-I4-01’s checkpoint-budget obstruction. However, unconditional fairness remains unsupported. Minor documentation residue: the cold-start test still says rotation is persisted; code and DESIGN call the input “scheduled time” although it is actual invocation start time.
16: 
17: The owner’s implementation choice is clear. Acceptance of this demonstrated starvation residual is a separate author ruling; I have not inferred it.
18: 

=== FILE (new): docs/reviews/issuer-lifecycle-impl/CODEX-CONFIRM-6.md
1: **Verdict: not ready for deployment work with the step-5 gate closed; an obtainable-response starvation residual remains beyond the stated “cannot fit one receive per slot” limit.**
2: 
3: - **Suite:** 222 passed in 131.54 seconds.
4: - **Original probes:** all three collected every signature. Lock-in and cold-start reached `evidence`; reduced-budget remained `signing`. Their old starvation assertions failed as expected. The two ancillary checks passed.
5: - **Remaining defect:** the first-response exception can consume enough invocation budget to block the next slot despite its separate allowance. In an independent probe, one unrequested KMS response cost **240 seconds**: receive, index lookup, log write and acknowledgement, each taking 60 seconds and fitting its individual admission bound. Only **40 usable seconds** remained, so GPG never received.
6: 
7: Across **12 KMS-first polls**, both valid GPG replies stayed queued. A GPG-first control collected them. The probe uses combined/variable dependency latency and scheduled times 1,200 seconds apart; consecutive 600-second events alternate correctly.
8: 
9: This is **not limited to a budget unable to fit two receives**: the 290-second budget fits both 60-second receives, including their admission bounds. Earlier response handling consumes the capacity needed by the second slot. Independent allowances therefore do not guarantee service independently of ordering.
10: 
11: No other new defect identified in this narrow pass. No repository edits or git writes; scratch stayed under [/tmp/tmp.CnfcXg4OuN](/tmp/tmp.CnfcXg4OuN). Evidence: [original probes](/tmp/tmp.CnfcXg4OuN/probes.log), [counterexample](/tmp/tmp.CnfcXg4OuN/test_overrun.py), [counterexample results](/tmp/tmp.CnfcXg4OuN/overrun.log), [suite](/tmp/tmp.CnfcXg4OuN/suite.log).

=== FILE (new): docs/reviews/issuer-lifecycle-impl/CODEX-CONFIRM-7.md
1: **Not ready for deployment work with the step-5 gate closed: deterministic starvation remains beyond the stated capacity limit.**
2: 
3: - **Suite:** 221 passed in 132.96 seconds.
4: - **Four original probes:** rerun unchanged; three hit removed interfaces, and the cold-start starvation assertion failed because signatures were collected. Scratch adaptations preserve their workloads and check collection: **6 passed**.
5: - **New counterexample:** 290-second budget, SQS calls taking 50 seconds, DynamoDB calls taking 30 seconds, valid replies queued on both slots. Across 12 polls for **each possible first slot**, no signature reached its job record. Both receives occur; handling then exhausts admission capacity, and request servicing cannot reconcile the stored signature. The same situation repeats.
6: - **Capacity control:** one receive plus complete handling **and acknowledgement succeeds in 250 seconds**, with identical dependencies and budget. Thus this falls outside exception (b), and randomness cannot fix it.
7: 
8: The cause is [pipeline.py:385](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:385): the next-receive guard reserves **one store operation**, not a message’s complete handling cost. Both receive orders produce the same failure, so this is deterministic starvation, not an unlucky sequence whose probability vanishes.
9: 
10: [DESIGN.md:225](/home/tony/projects/tessera/service/issuer/DESIGN.md:225) explicitly describes probability-1 selection and the capacity limit, but **understates the residual**: “starvation-free by construction” and “whatever the schedule” do not hold. No additional distinct defect identified in this narrow pass.
11: 
12: Evidence: [counterexample and control](/tmp/tmp.1c5WQ5xzIA/test_capacity.py), [results](/tmp/tmp.1c5WQ5xzIA/capacity.log), [adapted probes](/tmp/tmp.1c5WQ5xzIA/adapted.log), [suite](/tmp/tmp.1c5WQ5xzIA/suite.log).
13: 
14: No repository edits or git writes. I missed redirecting pytest fixture scratch: the suite also used `/tmp/pytest-of-tony`, outside the requested fresh scratch directory.

=== FILE (new): docs/reviews/issuer-lifecycle-impl/CODEX-CONFIRM-8.md
1: **Not ready for deployment work with the step-5 gate closed: deterministic starvation remains when actual handling fits but per-call admission blocks completion.**
2: 
3: - **Suite:** [223 passed in 133.45 seconds](/tmp/tessera-confirm8.cl8D1KZ7/suite.log).
4: - **Prior counterexample fixed:** both first-slot choices now collect a signature. Earlier collection probes pass. The share-overrun probe needs its populated slot selected explicitly; that check also passes. [Results](/tmp/tessera-confirm8.cl8D1KZ7/verified.log).
5: - **Coherence:** [DESIGN.md:231](/home/tony/projects/tessera/service/issuer/DESIGN.md:231) does not explicitly distinguish actual latency from admission capacity. Interpreted as actual latency, its probability-1 claim is false. Interpreted as complete worst-case capacity, the condition is unmet by the AWS configuration.
6: - **New counterexample:** SQS **20 s**, DynamoDB **24 s**, S3 **47 s**. One receive plus complete handling takes **254 s**, or **278 s on redelivery**, both within **280 usable seconds**. Nevertheless, a guarded call encounters **70 s remaining against its 73 s admission requirement**. Across 12 polls for each first slot, no signature reaches the record; request servicing also cannot reconcile it. Larger-budget controls complete those same paths. [Probe](/tmp/tessera-confirm8.cl8D1KZ7/test_admission.py), [results](/tmp/tessera-confirm8.cl8D1KZ7/verified.log).
7: 
8: The required condition must include **every call’s admission headroom**, not merely total actual duration. Random selection cannot repair this failure. Also, `_handle_worst` omits the additional DynamoDB log write on redelivery of an already logged “used” signature.
9: 
10: No repository edits or git writes; all test scratch, caches and basetemp stayed under the fresh scratch directory.

=== FILE (new): docs/reviews/issuer-lifecycle-impl/CODEX-CONFIRM-9.md
1: **Not ready for deployment work with the step-5 gate closed: per-call resumability and the stated admission condition still overclaim progress.**
2: 
3: - **Verification:** [232 passed](/tmp/tessera-confirm9.5ZRcra9S/suite.log). The original admission counterexample now collects a signature on poll 2 for either first slot; its old starvation assertions therefore fail as expected. [Eight earlier drain probes pass](/tmp/tessera-confirm9.5ZRcra9S/drain.log).
4: - **Remaining defect:** [pipeline.py:508](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:508) repeats the signature write and frame read whenever the used-log entry is absent. It does **not** resume from every completed call.
5: - **Reproduction:** SQS **20 s**, DynamoDB **24 s**, S3 **60 s**. Receive plus the three locating reads consumes **92 s**, leaving **188 s**, satisfying DESIGN’s stated **73 s** headroom condition. Repeated signature write and frame read consume another **120 s**; the used-log write encounters **68 s** and is refused. Request servicing cannot start either. Across **12 polls for each first slot**, signatures remain stored but unlogged and unadopted. A larger-budget control completes. [Probe](/tmp/tessera-confirm9.5ZRcra9S/test_resume_gap.py), [results](/tmp/tessera-confirm9.5ZRcra9S/gap.log).
6: - **Crash safety:** no additional signature-loss, incorrect duplicate job update, or premature-ack defect found. Guarded updates and ack-last preserve recovery material. `_reconcile` verifies unlogged signatures before logging and adopting them; independent valid/invalid probes [both pass](/tmp/tessera-confirm9.5ZRcra9S/reconcile.log). Safe repetition does not establish progress.
7: - **DESIGN / mutant:** the capacity condition is now expressed in admission terms, but remains insufficient: it omits repeated work before the next incomplete step. Retiring `ILCI7_ONESTORE` is reasonable as superseding whole-message reservation, but does not establish the replacement’s claimed resumability.
8: 
9: No repository edits or git writes; test scratch, caches, and basetemp stayed under the fresh scratch directory.

=== FILE (new): docs/reviews/issuer-lifecycle-impl/CODEX-CONFIRM.md
1: **Verdict: not ready for deployment work, even with the gate closed.**
2: 
3: Validation: **182 passed in 103.92 s**. My adapted original probes and additional adversarial probes: **12 passed**, including assertions reproducing the remaining defects. Four supplied mutations—`NOPRUNE`, `ILI04`, `ILI07_RAW`, and `GATE`—each caused the targeted test to fail.
4: 
5: No repository edits or git writes. Scratch evidence: [probes](/tmp/tmp.lgKk0SQtBY/test_confirmation.py), [results](/tmp/tmp.lgKk0SQtBY/probes3.log). I did not rerun TLC or validate deployed infrastructure.
6: 
7: **A — Original findings**
8: 
9: | Finding | Status | Assessment |
10: |---|---|---|
11: | ILI-01 | **PARTIAL** | Contradiction, transaction-shape, signature, and frozen-git cases are repaired. Dependency classification still mishandles snapshot trust failures; ILC-I-01. |
12: | ILI-02 | **PARTIAL** | An impossibility path exists, but its predicate is insufficient and some execution paths never reach it; ILC-I-01/04. |
13: | ILI-03 | **CLOSED** | Complete all-contradicted evidence is classified invalid; pending evidence remains open. |
14: | ILI-04 | **CLOSED** | Durable signatures reconcile before closure. Independently reproduced. |
15: | ILI-05 | **PARTIAL** | Ordinary slow-header progress works. Invocation bounds and progress under recovery remain defective; ILC-I-02/03/05. |
16: | ILI-06 | **CLOSED** | Shipping with subsequently available lower headers is covered; `NOPRUNE` now fails that test. |
17: | ILI-07 | **CLOSED** | External oversized reasons are bounded and referenced separately; disabling bounding fails the test. |
18: | ILI-08 | **CLOSED** | Initial content check precedes allocation; later loss uses recovery or atomic end-and-refuse. Documentation qualifications remain below. |
19: | ILI-09 | **CLOSED** | The original FAILED/margin/“always” statements are corrected. New documentation inconsistencies remain; ILC-I-06. |
20: 
21: **E — Findings**
22: 
23: 1. **ILC-I-01 — High: `SNAPSHOT_IMPOSSIBLE` can discard a repairable, timely-anchored snapshot.**  
24:    [pipeline.py:847](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:847), [pipeline.py:877](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:877), [pipeline.py:948](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:948).
25: 
26:    Row **13.5 depends on trust configuration**, as well as snapshot bytes. I retained an originally timely snapshot, advanced the chain beyond the MTP threshold, and changed only the configured KSK interval. The real verifier returned `KSK_OUTSIDE_RELIANCE_PERIOD`; the issuer discarded attempt 1 as `SNAPSHOT_IMPOSSIBLE`. Restoring the configuration and testing the original attempt produced **COMPLETE**.
27: 
28:    MTP excludes new timely anchors. It does **not** establish that an existing anchored snapshot cannot become lawful after configuration or evidence repair. Likewise, “no pending calendar” alone does not establish the required incurability. Separate configuration-dependent failures and prove the existing presentation cannot be repaired before discarding.
29: 
30: 2. **ILC-I-02 — High: the budget does not bound an invocation to 300 seconds.**  
31:    [pipeline.py:144](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:144), [pipeline.py:280](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:280), [pipeline.py:299](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:299), [pipeline.py:518](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:518).
32: 
33:    Four signing sends taking 80 seconds apiece produced a **320-second poll**, without other costs. The AWS configuration permits four attempts per call. Signing sends have no budget checks; neither do individual response processing, full active-request enumeration, or cleanup operations.
34: 
35:    Header costs also omit checkpoint storage calls, assume exactly two explorers although the adapter accepts more, and treat HTTP timeouts as complete work-unit bounds. The 30-second pre-ship allowance is an assertion rather than an enforced limit. A 60-second reserve does not cover these unbounded sequences.
36: 
37: 3. **ILC-I-03 — Medium: checkpoint recovery can livelock on a stale suffix.**  
38:    [pipeline.py:675](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:675).
39: 
40:    With a stale cached header at `h+4`, linked-header validation fails and the fresh pass restarts at `h`. Under the original 12-second/request explorer conditions, each invocation refreshes only `h..h+2`. The next invocation restarts that same work.
41: 
42:    **Reproduced for six polls:** the stale height was never fetched; the attempt remained at `evidence`. Recovery needs durable invalidation or a durable refresh position, so completed refresh work advances toward the inconsistent suffix.
43: 
44: 4. **ILC-I-04 — Medium: snapshot rejection can bypass the impossibility path indefinitely.**  
45:    [pipeline.py:604](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:604), [pipeline.py:966](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:966).
46: 
47:    `_snapshot_impossible` runs only after finalization reaches a snapshot-related verifier failure. Once stage `snapshot` repeatedly rejects captured DNS material, it never reaches that check—even after the MTP threshold is exceeded.
48: 
49:    **Reproduced:** a late, complete snapshot first caused recapture; after further chain progress, persistent malformed captures left the attempt latched at `snapshot`. This exceeds DESIGN’s example of bad DNS remaining open *while MTP has not passed* the limit.
50: 
51: 5. **ILC-I-05 — Medium: pending-calendar work can starve already qualifying receipt evidence.**  
52:    [ots.py:191](/home/tony/projects/tessera/service/issuer/tessera_issue/ots.py:191), [pipeline.py:730](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:730).
53: 
54:    Upgrades revisit pending branches in the same order before header selection. With twelve pending calendar requests taking 20 seconds each, every invocation consumes its budget before selection—even though the proof already contains a qualifying, timely Bitcoin branch.
55: 
56:    **Reproduced across three polls.** Request round-robin does not provide fairness within a request. Preserve an upgrade cursor and allow eligibility evaluation independently of exhausting pending-calendar work.
57: 
58: 6. **ILC-I-06 — Low: operational descriptions and CL-03 are not fully reconciled.**  
59:    [DESIGN.md:164](/home/tony/projects/tessera/service/issuer/DESIGN.md:164), [DESIGN.md:169](/home/tony/projects/tessera/service/issuer/DESIGN.md:169), [V1-CLARIFICATIONS.md:38](/home/tony/projects/tessera/docs/V1-CLARIFICATIONS.md:38).
60: 
61:    - Classification selects an invalid frozen check preferentially, rather than necessarily the first failing check.
62:    - “Every UNVERIFIABLE result” is retried is inaccurate for snapshot rows, which can lead to discard.
63:    - CL-03’s attempt-cause list omits direct `SIGNING_CLOSED` and `CONTENT_UNAVAILABLE` causes emitted at [pipeline.py:494](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:494).
64:    - “Upload never completed” is narrower than the implemented pre-allocation failure: a completed upload subsequently lost before allocation also produces FAILED.
65: 
66: **B — Deviations**
67: 
68: | Deviation | Judgment |
69: |---|---|
70: | **1. Prune contradicted branches and ship** | **Sound for the resulting presentation.** Profile §7.1 and verifier row 11.3 reject a contradiction remaining in the presented proof; they do not require presenting every acquired branch. The repaired proof is rechecked. This changes presentation bytes and can change an unpruned presentation’s verdict from INVALID to VALID_STRICT. It leaves `A_sig` and the receipt identifier unchanged and removes no presentation a holder could construct by the same pruning. |
71: | **2. MTP impossibility proof** | **Sound as a conditional bound on new anchors; insufficient as implemented for overall impossibility.** Along a consensus-valid retained chain, MTP is nondecreasing, so the bound excludes future anchors satisfying row 13.7. Existing snapshot repair remains possible—ILC-I-01. Require the checkpoint to survive: “no reorg deeper than 6” is too loose if it permits removing exactly six blocks; the contract excludes reorganizations of **6 or more**. The assumptions are substantially stated in the code and A1.6, but DESIGN should state them explicitly. |
72: | **3. Frozen / snapshot / retry rows** | **Not wholly correct.** The added frozen cases repair the reported gaps, but row 13.5 cannot be classified solely as replaceable snapshot material. Its configuration-dependent outcomes require separate handling. |
73: | **4. Budget/checkpoint/cursor** | **Insufficient.** Cursor-before-work improves fairness among a finite set of requests, provided enumeration completes. It does not prevent invocation overruns, checkpoint-refresh livelock, or calendar starvation. |
74: | **5. Reason codes versus CL-03** | **Main new codes match; the exhaustive description still needs correction.** See ILC-I-06. Naming a reason does not establish its discard predicate. |
75: 
76: **C — Step-5 gate**
77: 
78: **Still closed in the reviewed implementation.** Diagnostic failure history does not authorize an ending; there is no sampled-unavailability refusal, age deadline, or signing-closure substitute for ending stamped/latched attempts. The `GATE` mutation is detected.
79: 
80: The wrongful snapshot discard above is a separate incurability-classification defect, not evidence that sampled-unavailability policy has been enabled.
81: 
82: **D — Other termination gaps**
83: 
84: **Yes.** ILC-I-03 and ILC-I-05 can prevent progress despite obtainable qualifying evidence. ILC-I-04 can retry indefinitely without evaluating an available impossibility argument. These extend beyond DESIGN’s stated concern that impossibility cannot be proven.
85: 
86: **Owner prechecks**
87: 
88: | Check | Result | Evidence |
89: |---|---|---|
90: | **1. Capture row** | **PASS** | Reviewed repair claims add no attacker-key rejection or capture visibility. [V1-CONTRACT.md:37](/home/tony/projects/tessera/docs/V1-CONTRACT.md:37) and [§4:72](/home/tony/projects/tessera/docs/V1-CONTRACT.md:72) remain controlling: attacker-key receipts can pass after dual-channel capture. |
91: | **2. Trigger clause** | **FAIL** | [pipeline.py:949](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:949) applies incurable-discard consequences without establishing that the existing snapshot is incurable; reproduced by ILC-I-01. Signing-closure’s original trigger defect is repaired. |
92: | **3. Requester** | **PASS** | [DESIGN.md:19](/home/tony/projects/tessera/service/issuer/DESIGN.md:19) identifies the issuer’s enqueue capability; [main.tf:255](/home/tony/projects/tessera/service/issuer/infra/main.tf:255) grants it. Absence of signing credentials does not establish resistance to unauthorized signing requests. Deployed signer authorization remains unverified. |
93: | **4. Binding text** | **FAIL** | The implementation’s blanket snapshot predicate contradicts the incurability condition at [lifecycle decision:143](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:143). Progress failures outside the gate also remain against [A2.3:288](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:288); owner documentation does not waive that registered obligation. |
94: 

=== FILE (new): docs/reviews/issuer-lifecycle-impl/CODEX-REVIEW.md
1: **Verdict: not ready for deployment work, even with the gate closed.**
2: 
3: The lifecycle core largely follows revision 5.3.1, but permanent-failure handling, signing recovery, runtime budgeting, and test coverage need correction. I made no repository or git writes. Scratch work is under [/tmp/tmp.H7U54TsUGg](/tmp/tmp.H7U54TsUGg).
4: 
5: Validation: **158 passed in 87.97 s**, with bytecode/cache writes disabled and pytest temporary files redirected to scratch. Seven additional scratch probes reproduced the cases below. I inspected R53 and its recorded results; I did not rerun TLC.
6: 
7: **Findings**
8: 
9: 1. **ILI-01 — High: the post-latch incurable set is incomplete.**  
10:    [pipeline.py:83](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:83), [pipeline.py:589](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:589), [pipeline.py:720](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:720).
11: 
12:    A proof can contain both a qualifying branch and a contradicted branch at the selected height. `fetch_evidence` ignores `select`’s contradiction flag; pruning retains both branches at that height. The attempt latches, then pre-ship returns `INVALID/OTS_MERKLE_MISMATCH`. That reason is absent from `COMMITTED_BYTES_REASONS`, so the immutable, invalid presentation is retried forever. **Reproduced.**
13: 
14:    The eleven listed reasons are consistent with immutable failures in the current assembly path, but they are not exhaustive. Other missing cases include receipt transaction-shape/txid failures and failures attributable to frozen git material. Classification must distinguish those from replaceable snapshot/configuration failures.
15: 
16:    **Fix:** classify failures by their actual evidence dependency and repairability. Reject or discard a definitively invalid preserved presentation with a recorded reason; test each classification against a real verifier outcome.
17: 
18: 2. **ILI-02 — Medium: known incurable snapshot failure has no ending path.**  
19:    [pipeline.py:696](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:696), [pipeline.py:714](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:714), [pipeline.py:730](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:730).
20: 
21:    Snapshot problems either wait, recapture, or retry. There is no representation of “this frozen attempt cannot obtain any lawful snapshot.” Consequently, under the brief’s **“can never be anchored” premise**, the attempt remains latched forever rather than taking step 7’s reasoned discard.
22: 
23:    The scratch probe reproduced the `SNAPSHOT_TIME → recapture → stamp → retry` loop. It does **not** establish irreparability merely from elapsed wall time: timestamps are nonmonotone, and historical evidence may recover.
24: 
25:    **Fix:** add an evidence-based permanent-failure classification. Do not introduce an age-based discard. Proven impossibility belongs outside the pending sampled-unavailability gate; indefinite retry of that proven-impossible case leaves A2.3 termination unmet outside that gate.
26: 
27: 3. **ILI-03 — Medium: complete, contradicted evidence is classified as pending.**  
28:    [pipeline.py:602](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:602).
29: 
30:    With no pending calendars, every full segment obtained, and every attestation contradicted by its pinned header, `sel is None` prevents classification as negative. The result is `pending` indefinitely. **Reproduced.**
31: 
32:    This is conclusive invalid evidence under [profile §7.1:889](/home/tony/projects/tessera/docs/V1-PROFILE.md:889), rather than missing evidence. Conversely, `sel is None` alone is insufficient to conclude failure.
33: 
34:    **Fix:** distinguish complete authenticated contradiction from incomplete/nonqualifying evidence. Record an explicit invalid-evidence reason; do not fabricate a failed temporal conjunct.
35: 
36: 4. **ILI-04 — Medium: signing closure precedes recovery of completed signing.**  
37:    [pipeline.py:410](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:410), [pipeline.py:415](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:415).
38: 
39:    All four signatures can already exist in S3 and the durable “used” log while their request-record updates were lost. After signing closes, `st_signing` discards before `_reconcile` can recover them. The request becomes `REFUSED/SIGNING_CLOSED` although no further signature is necessary. **Reproduced.**
40: 
41:    **Fix:** reconcile durable signatures before deciding whether signing is still required, then seal a complete recovered set regardless of closure. Add this interleaving to the closure tests.
42: 
43: 5. **ILI-05 — High: one healthy evidence fetch can exceed the entire Lambda budget.**  
44:    [pipeline.py:100](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:100), [pipeline.py:635](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:635), [chain.py:47](/home/tony/projects/tessera/service/issuer/tessera_issue/chain.py:47), [main.tf:363](/home/tony/projects/tessera/service/issuer/infra/main.tf:363).
45: 
46:    With two explorers, one six-header segment requires 24 sequential header/hash HTTP requests plus two tip requests. At 12 seconds each—below the configured 20-second HTTP timeout—that is **312 seconds**, before calendars, S3, DynamoDB, or the latch write.
47: 
48:    Every invocation can commit another fence and die before making progress. Multiple attestations and multiple requests worsen this; the poller has no durable scheduling cursor or remaining-time budget.
49: 
50:    **Fix:** bound and checkpoint work within the 300-second invocation, preserve fetched immutable material, and schedule requests fairly. Keep reserved concurrency 1 and the fence; do not solve overload by ending attempts.
51: 
52: 6. **ILI-06 — Medium: pruning’s load-bearing behavior is untested.**  
53:    [test_lifecycle.py:356](/home/tony/projects/tessera/service/issuer/tests/test_lifecycle.py:356), [test_lifecycle.py:570](/home/tony/projects/tessera/service/issuer/tests/test_lifecycle.py:570), [test_lifecycle.py:664](/home/tony/projects/tessera/service/issuer/tests/test_lifecycle.py:664).
54: 
55:    I independently ran the supplied `NOPRUNE` mutation against the lifecycle suite: **37 passed**.
56: 
57:    A scratch case exposed the missing distinction: latch a higher passing attestation while the lower segment is unavailable, then add that lower segment to the assembly headers. With pruning, assembly preserves the selected height. Without pruning, selection moves lower and assembly raises `StageError`.
58: 
59:    **Fix:** add this case through finalization/shipping, including lower evidence arriving through snapshot/git header collection. Require pruning removal to fail the test.
60: 
61: 7. **ILI-07 — Medium: an uncapped refusal reason can exceed DynamoDB’s item limit.**  
62:    [pipeline.py:279](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:279), [pipeline.py:165](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:165), [aws.py:54](/home/tony/projects/tessera/service/issuer/tessera_issue/aws.py:54).
63: 
64:    A signer’s unrestricted `reason` is copied into both the attempt ending and event history. A 210,000-character reason produced a **422,386-byte item** in the scratch probe. AWS limits items to 400 KiB, including attribute names and values. The terminal/allocation write therefore fails instead of completing. [AWS constraints](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Constraints.html)
65: 
66:    **Fix:** validate and cap external reason fields, retain a bounded reason code, and store oversized diagnostics separately by reference. Add serialized-item-size checks to the AWS adapter tests.
67: 
68: 8. **ILI-08 — Medium: `CONTENT_UNAVAILABLE` also terminates an allocated attempt.**  
69:    [pipeline.py:374](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:374), [pipeline.py:380](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:380), [DESIGN.md:29](/home/tony/projects/tessera/service/issuer/DESIGN.md:29).
70: 
71:    `st_frames` commits allocation before reading content. A missing content object then ends the request `FAILED/CONTENT_UNAVAILABLE`, marking the allocated attempt discarded. This contradicts the documented “before any attempt” exception and bypasses normal end-and-allocate handling.
72: 
73:    **Fix:** check content availability before allocation. Once allocated, a storage miss needs recovery or an explicitly justified permanent-failure path.
74: 
75: 9. **ILI-09 — Low: documentation still makes incompatible operational claims.**  
76:    [DESIGN.md:43](/home/tony/projects/tessera/service/issuer/DESIGN.md:43) says a failed pre-ship check becomes `FAILED`; the implementation generally retries or discards. [DESIGN.md:44](/home/tony/projects/tessera/service/issuer/DESIGN.md:44) says the new margin is unapplied, although [window.py:23](/home/tony/projects/tessera/service/issuer/tessera_issue/window.py:23) implements it.
77: 
78:    Also, [window.py:8](/home/tony/projects/tessera/service/issuer/tessera_issue/window.py:8) promises the first attempt “always” has its full lifecycle before signing stops. Acceptance spacing cannot guarantee that when allocation can be delayed.
79: 
80:    **Fix:** reconcile the current descriptions and describe the margin as an operating allowance, without a guaranteed processing bound.
81: 
82: **Conformance and the gate**
83: 
84: | Area | Assessment |
85: |---|---|
86: | Attempts and isolation | Implemented: separate material, signing IDs, response routing, declarations and stamps. |
87: | Single lifecycle writer | Implemented; status/receipt are read-only, poller concurrency is 1. Submission/upload bookkeeping remains separate. |
88: | Fence before fetch | Implemented for evidence, finalization and recapture; failed fencing prevents fetching. |
89: | Write guards | Implemented on version, request state, attempt ID and attempt state, including DynamoDB expressions at [aws.py:85](/home/tony/projects/tessera/service/issuer/tessera_issue/aws.py:85). |
90: | Eligibility | Own `A_sig` digest, k=6, full linked segments and all three inclusive conjuncts are checked. Invalid-proof classification has ILI-01/03 gaps. |
91: | Preserved latch | Presentation is written to S3 before its digest/reference commits at [pipeline.py:653](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:653). |
92: | Negative endings | Partial, stale, failed and pending fetches do not cause expiry. Complete-invalid evidence needs ILI-03’s distinction. |
93: | Atomic endings | End-and-allocate and final refusal occupy one conditional request-item write. A multi-item transaction is unnecessary for these transitions. |
94: | Storage lifetime | Corrected: live objects receive no age-expiration tag; cleanup derives eligibility from persisted request end. |
95: | Public view | Attempt number/state, open boundary, nominal-budget note and refusal reasons are exposed. |
96: 
97: **The sampled-unavailability gate is closed.** No lifecycle path produces `EVIDENCE_UNAVAILABLE`, reads diagnostic failure history to decide an ending, or turns an evidence-stage timeout/age/signing closure into an equivalent ending. Stamped and latched attempts survive signing closure. ILI-04 and ILI-08 are separate pre-stamp ending defects, not evidence that step 5 has secretly been enabled.
98: 
99: **Judgment on the seven deviations**
100: 
101: | Deviation | Judgment |
102: |---|---|
103: | **(a) Latch the passing presentation in hand; prune to its height** | **Sound for the shipped presentation**, subject to ILI-01/06. Profile §7.1 selects among qualifying branches in the presented proof; a missing lower segment supplies no time fact. Pruning prevents later assembly headers changing that presentation’s selection. This is not owner acceptance of the policy. |
104: | **(b) Complete evidence with no qualifying attestation remains open** | **Too broad.** Incomplete qualification remains open; complete authenticated contradiction is conclusive invalidity. ILI-03. |
105: | **(c) `COMMITTED_BYTES_REASONS`** | Listed members are defensible; **the set is incomplete**, and reason-only classification needs provenance. ILI-01. |
106: | **(d) Permanently impossible snapshot remains latched** | **Incorrect under the stated impossibility premise.** Step 7 should discard with evidence and reason. Elapsed wall time or one `SNAPSHOT_TIME` result does not establish that premise. ILI-02. |
107: | **(e) `FAILED/CONTENT_UNAVAILABLE` before any attempt** | Defensible for an abandoned upload. The implementation also applies it after allocation. ILI-08. |
108: | **(f) Signer refusal discards and allocates next** | Defensible for the current unsigned, unstamped attempt; it cannot yet have protected receipt eligibility. Keep routing/logging and bound the supplied reason. |
109: | **(g) Capped diagnostic runs** | Acceptable while diagnostic only. Capping loses history; it cannot later serve as complete gated coverage evidence without fresh analysis. |
110: 
111: The tests meaningfully exercise selected model interleavings: killed writes, fence sensitivity, duplicate endings, boundary latching and partial recovery. They are **not a complete model-trace replay or implementation refinement check**. Post-latch assembly, signing recovery and AWS execution constraints remain outside R53’s checked assurance.
112: 
113: For AWS, ordinary bounded attempt metadata and S3 presentation references avoid embedding large proofs in DynamoDB; ILI-07 remains the size hole. Request creation correctly uses a transaction for request plus tombstone. Cleanup’s obligation-before-terminal ordering is appropriate. `s3:PutObjectTagging` is granted to the poller at [main.tf:241](/home/tony/projects/tessera/service/issuer/infra/main.tf:241), matching the API’s required permission. [AWS tagging API](https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutObjectTagging.html)
114: 
115: **Owner prechecks**
116: 
117: | Check | Result | Evidence |
118: |---|---|---|
119: | **1. Capture row** | **PASS** | Reviewed lifecycle claims do not promise attacker-key rejection or capture visibility. Ground truth remains [V1-CONTRACT.md:37](/home/tony/projects/tessera/docs/V1-CONTRACT.md:37) and [§4:72](/home/tony/projects/tessera/docs/V1-CONTRACT.md:72): fresh attacker-key receipts pass after dual-channel capture. |
120: | **2. Trigger clause** | **FAIL** | [pipeline.py:412](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:412) applies signing closure before establishing that signing is still required. Durable recovery can falsify that antecedent—ILI-04. |
121: | **3. Requester** | **PASS** | [DESIGN.md:19](/home/tony/projects/tessera/service/issuer/DESIGN.md:19) identifies the issuer as queue requester; [pipeline.py:352](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:352) submits the work. Lack of direct signing credentials is not promoted into requester-compromise resistance. Deployed signer authorization remains unverified here. |
122: | **4. Binding text** | **FAIL** | The owner constant at [pipeline.py:83](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:83), treated as exhaustive at [DESIGN.md:160](/home/tony/projects/tessera/service/issuer/DESIGN.md:160), strands known immutable-invalid attempts. The pending step-5 decision does not waive [A2.3:288](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:288)’s termination obligation for these separate failures. |
123: 

=== FILE (new): docs/reviews/issuer-signer-interface/BRIEF.md
1: # Review brief: issuer <-> signer interface, after the frame-reference fix (owner, 2026-10-30)
2: 
3: You are reviewing the Tessera V1 issuer (`service/issuer/`) and its two production signers (`service/signer-kms/`,
4: `service/signer-gcp/`) in /home/tony/projects/tessera. Read-only, except that you may run the test suites
5: (`.venv/bin/python -m pytest -q` in each package directory) and write scratch files under /tmp.
6: 
7: ## What happened
8: 
9: Before deployment, the owner ran all four suites. The issuer (234) and verifier passed; both signer suites failed.
10: 
11: 1. **A real defect.** The issuance-lifecycle rework (commit 9364733) renamed large-frame objects in
12:    `service/issuer/tessera_issue/pipeline.py` `_send.stash` from `frames/<rid>/<sha256>` to
13:    `frames/<rid>/<attempt id>-<sha256>`. Both production signers refuse that form: signer-kms `RE_REF`
14:    (`tessera_sign_kms/signer.py:42`, which also requires the name to equal `frame_sha256`) and signer-gcp `RE_REF`
15:    (`tessera_signer/policy.py:29`). Every by-reference request (frames over `INLINE_MAX`, 256 KiB) would be refused
16:    BAD_REQUEST on every attempt, ending the request ATTEMPTS_EXHAUSTED. The issuer suite missed it because its
17:    stand-in signer does not check the reference form; Codex CONFIRM-10 reviewed the issuer alone.
18: 2. **Test-harness drift.** ILC-I6/ILC-I9 changed `SlotSigner.receive` to return `(handle, body, age)` and to read
19:    `Message.sent/.seq/.receives`. The signer suites' queue stand-ins and unpacking were not updated.
20: 
21: ## The change (FIX.diff in this directory)
22: 
23: - Issuer: the frame object name is exactly `sha256hex(frame)` again, as `service/issuer/DESIGN.md:92` states. The
24:   owner's reasoning: frames are deleted per request at the end (END_NS), not per attempt; nothing reads the attempt
25:   prefix; attempts' frames differ (declared time), and identical bytes would share one immutable object.
26: - A new issuer test checks the exact form the deployed signers accept, and fails without the fix (verified).
27: - Signer test harnesses: signer-gcp `QueueView.receive` returns the issuer's `Message` with the receive count;
28:   three-value unpacking in both suites.
29: 
30: Suites after the change: issuer 235, signer-kms 48, signer-gcp 118, verifier 135, all passing.
31: 
32: ## What we ask
33: 
34: A. **Confirm or refute the fix.** Is the owner's reasoning right that dropping the attempt prefix loses nothing?
35:    Check attempt isolation (ILI/ILC findings in `docs/reviews/issuer-lifecycle-impl/`), cleanup and `mark_due`, the
36:    `_seal`/signature-object paths, retries and late responses from an earlier attempt, and any S3 IAM or lifecycle
37:    rule in `service/issuer/infra/` or `service/signer-*/infra/` that keys on the object name.
38: B. **Sweep the class, not the instance.** The defect class is "the issuer and a signer disagree about the wire or
39:    storage contract, and no test runs them together". Enumerate every field and format that crosses the boundary in
40:    either direction (request JSON fields and their formats, `request_id` form, `sign_by` format, inline size limits
41:    against `INLINE_MAX` and each signer's limit, `frame_ref` and bucket/prefix, response fields, status and reason
42:    strings the issuer acts on, `frame_sha256` echo, signer `slot`/clock fields, key fingerprint form, SQS message
43:    attributes), and the infrastructure grants that let each signer read the frames prefix. For each, say whether the
44:    issuer's producer and each signer's consumer agree, citing file:line, and whether any test exercises the real
45:    signer code against the real issuer code for it.
46: C. **Test harness changes.** Do the signer-suite edits weaken any test (e.g. by hiding a receive-count case)?
47: 
48: Report findings with severity, file:line, and a concrete failing scenario. Say plainly if you find nothing.
49: Write your report to docs/reviews/issuer-signer-interface/CODEX-REVIEW.md.
50: 
51: # Owner prechecks, run by the reviewer
52: 
53: > **Status: OWNER PROCESS, 2026-10-27.** Every owner instance has written these down as lessons and then repeated
54: > the mistakes (the 2026-10-19 stone, and its 2026-10-27 postscript "Naming it did not stop it"). The author's
55: > answer to "what do new owners get wrong in their first week": *"that they will behave differently from the prior
56: > instances."* So these checks are not left to the owner's self-review. The owner appends this file verbatim to
57: > every review brief (Codex or another family), and the reviewer reports each check as PASS or FAIL with file:line.
58: 
59: ## Checks
60: 
61: 1. **Capture row.** For every plain-language statement of what holds, what happens when an attacker controls both
62:    authority channels (DNS and git)? If the text implies that the attacker's own keys are rejected, or that a
63:    capture is detected or made visible, that is FAIL. Ground truth: `docs/V1-CONTRACT.md` §2 (after G10) and §4.
64: 2. **Trigger clause.** For every registered rule cited as authority (an amendment section, a table row, a ruling),
65:    did the rule's trigger condition actually occur? Citing a consequence whose trigger has not happened is FAIL.
66: 3. **Requester.** For every security claim about keys or signing, who can cause a signature to be made? A claim
67:    that reasons only about where a key is stored, and not about who can submit work to the signer, is FAIL.
68: 4. **Binding text.** For every sentence the document treats as a requirement, is it registered (a signed amendment,
69:    the freeze, or a recorded author ruling), or is it something an instance wrote? An unregistered sentence used as a
70:    requirement is FAIL. Since 2026-10-27, `docs/V1-SCHEDULE.md`'s ruling budget is a known instance of this. Also FAIL: an owner
71:    requirement (a resolution, a design document, a code constant) that contradicts a registered sentence. Since
72:    2026-10-29, S4's 24-hour FAILED against A2.3's per-attempt `declared + δ + S` expiry is the known instance.

=== FILE (new): docs/reviews/issuer-signer-interface/CODEX-REVIEW.md
1: # Issuer–signer interface review
2: 
3: Reviewer: Codex. Date: 2026-10-30. Base commit: `8bcfcdaf8b5451158f8515ebdb3e583082740699`, plus the five working-tree files represented by `FIX.diff`.
4: 
5: **Confirm the frame-reference fix. No new functional issuer–signer incompatibility found in the reviewed paths.** Dropping the attempt prefix does not remove an isolation or cleanup control. The harness edits preserve the existing assertions and the actual receive count. There is one retained test-coverage gap below. The appended binding-text precheck also identifies existing registration conflicts; this review does not resolve them or certify deployment readiness.
6: 
7: Only this report was written in the repository. Production code and existing tests were left unchanged. Scratch integration code is `/tmp/issuer-signer-probe.py`. All cloud clients in the tests and probe are fakes; no cloud deployment or live IAM inspection was performed.
8: 
9: ## Findings
10: 
11: ### ISI-01 — Low: GCP integration coverage still substitutes the frame-path producer
12: 
13: Location: `service/signer-gcp/tests/test_issuer_protocol.py:17-23,34-63`; `service/issuer/tests/test_review_fixes.py:379-391`.
14: 
15: The GCP round trips run the real `SlotSigner` and real GCP signer, but their `stash_into` constructs `frames/rid-7/<digest>` itself. They do not invoke `pipeline._send`, `st_frames`, `drain`, or `_seal`. The new issuer regression checks a copied regular expression against stand-in requests, rather than calling the GCP consumer. A future GCP-only change that rejects the issuer's 64-hex request namespace while continuing to accept `rid-7` could pass both groups of tests and refuse every large real request. A GCP manifest-policy change could similarly reject actual pipeline manifests while accepting the independently constructed fixture.
16: 
17: This is a coverage finding, not a currently failing production scenario. The KMS package already has full pipeline issuance coverage for inline and 1 MiB content (`service/signer-kms/tests/test_roundtrip.py:73-93`). Thus “no test runs them together” is too broad for the current tree: KMS does; GCP runs the shared interface but substitutes the upstream producer.
18: 
19: Recommendation: retain a GCP pipeline test, ideally running both production signer classes together with fake provider clients, for inline and by-reference issuance. Retain a late-response/next-attempt case as well. The scratch probe ran both production signer classes through the real pipeline successfully for 20-byte and 1 MiB content. That supplies present review evidence but does not close the retained regression gap.
20: 
21: ### ISI-02 — Medium, pre-existing: implementation compatibility is not registered conformance
22: 
23: Locations: `formal/p8/HYBRID-SUPPLEMENT.md:170-176`; `service/signer-kms/infra/main.tf:54-74`; `docs/phase-0-prereg-amendment-11.md:3-10,240-250`; `service/issuer/tessera_issue/pipeline.py:46-49`; `docs/phase-0-prereg-amendment-2.md:260-289`.
24: 
25: The registered K-R enforcement text grants signing only to the **issuer role**; the implementation grants it only to the dedicated **signer role** and denies others. The proposed wording repair is in unsigned Amendment 11. Concrete consequence: applying the current signer policy does not implement the registered principal placement, even though the two packages interoperate and the signer policy restricts signing inputs. Passing these suites cannot adopt that amendment.
26: 
27: Separately, permanently incomplete evidence leaves an attempt open in the current gated lifecycle, while A2.3 retains an implementation termination obligation. A calendar that never supplies evidence is a concrete example. The design explicitly discloses this unresolved conflict (`docs/decisions/2026-10-29-issuance-lifecycle.md:140-146,189-196`). The reference fix neither introduces nor resolves it. Amendment 11 explicitly does not accept the lifecycle residual (`:287-295`). These are registration/claim limits, not reasons to restore attempt-prefixed frame names.
28: 
29: ## A. Why the fix is sound
30: 
31: - **Object identity:** `_send` now writes `frames/<rid>/<sha256(frame)>` (`pipeline.py:584-596`), matching `ResultStore.ref` (`stores.py:125-136`), KMS's strict reference grammar and filename/digest equality check (`signer.py:152-165`), and GCP's accepted grammar plus fetched-byte digest check (`policy.py:87-92`; `signer.py:130-149`). Here and below, signer filenames are relative to their respective package unless stated otherwise.
32: - **Isolation is elsewhere:** `st_frames` derives signer IDs from request **and attempt**, slot and frame hash; it persists an index containing the attempt and job before sending (`pipeline.py:653-674`; `signers.py:31-34`). Work frames remain `work/<rid>/<aid>/<frame>`. Signature objects remain `work/<rid>/<aid>/sig-<job>-<signature-digest>` (`pipeline.py:512-535`). None of these paths changed.
33: - **Equal bytes are safe to share:** different declarations normally change attestation bytes, but distinct attempts allocated in the same second can have equal declarations. The manifest is identical across attempts in any event. Isolation does not depend on all attempts having different frame hashes: the attempt remains in the signer-request scope even for equal frames. Hash naming provides content identity, not an attempt identifier. This relies on SHA-256 collision resistance and trusted storage/writers.
34: - **Retries and late replies:** unanswered jobs reuse their IDs (`pipeline.py:688-703`). A late response for the current job can satisfy it; a response indexed to a previous attempt is logged `other-attempt` before it can supply a signature or trigger refusal (`:479-500`). Duplicate current-job responses do not replace the selected signature (`:491-495`). GCP caches signatures only by `(request_id, frame digest)` within one run (`signer.py:62,168-185`); across runs and in KMS randomized signing may yield another signature. The issuer's digest-named signature objects and guarded adoption handle that.
35: - **Sealing:** `_seal` reads the attempt's work frames and selected signature objects, checks signature digests, verifies signatures on exact frames, and requires the durable used-log entry (`pipeline.py:706-734`). It does not consume frame-reference names. The trusted-storage limitation and poisoning stall recorded in `CODEX-CONFIRM-10.md` remain unchanged; a digest-looking name is not cryptographic verification by itself.
36: - **Cleanup and `mark_due`:** `END_NS` includes `frames`; `_cleanup_one` first checks persisted request termination, tags and deletes the whole request namespace, and keeps the obligation through the late-writer lease (`pipeline.py:304-340`). There is no per-attempt frames deletion. S3 listing/tagging uses `frames/<rid>/` and the actual returned object names (`aws.py:224-231,267-284`). Repeated puts of identical bytes can replace the object and remove old tags, but active requests have no cleanup-due tags; after termination the retained cleanup obligation repeats tagging/deletion for late writes. This behavior does not need an attempt prefix.
37: - **Infrastructure:** the relevant grants use `frames/*`; the result lifecycle uses the cleanup-due tag, not an attempt filename (`service/issuer/infra/main.tf:96-129,316-319`; `service/signer-kms/infra/main.tf:111-115`). GCP has no `infra/` directory; its AWS access comes through the issuer role and `deploy.sh`, detailed below. No inspected rule requires the dropped prefix.
38: 
39: ## B. Boundary inventory
40: 
41: Coverage notation: **K-full** = KMS full pipeline tests at `service/signer-kms/tests/test_roundtrip.py:73-93`; **K-slot** = its `:48-70` round trip; **G-slot** = GCP `tests/test_issuer_protocol.py:12-93`. These execute real issuer/signing code with fake infrastructure. A successful representative round trip does not mean every malformed value, limit endpoint or failure interleaving is jointly tested. **Scratch-both** is the additional full pipeline probe from this review; it is not a repository regression test.
42: 
43: ### Requests, frame bytes and storage
44: 
45: | Boundary | Producer and consumers; agreement | Joint coverage |
46: |---|---|---|
47: | JSON envelope and fields | `SlotSigner.send`, `service/issuer/tessera_issue/signers.py:59-71`, emits exactly `{request_id, frame_b64, sign_by}` or `{request_id, frame_ref, frame_sha256, sign_by}`. KMS `signer.py:44-45,128-155` and GCP `policy.py:51-92` accept these exact member sets. JSON member order is immaterial. **Agree for pipeline output.** | K-full, K-slot, G-slot; malformed-shape cases are mainly signer-only. |
48: | Optional `sign_by` at the library API | `SlotSigner.send` allows omission, but pipeline `_send` always supplies `window.sign_until` (`pipeline.py:596`). Both production consumers require it. **Library domains differ; no pipeline mismatch.** | G-slot explicitly tests missing deadline refused (`:66-73`); K-full exercises the supplied value. |
49: | `request_id` | `signers.py:31-34` produces `req-` plus 40 lowercase hex; `pipeline.py:661-665` includes attempt in the scope. KMS `signer.py:40,225-228` and GCP `policy.py:28,66-70` accept 1–128 ASCII letters/digits/`._:-`. **Producer is a strict subset.** The S3 rid is a different identifier. | K-full/K-slot/G-slot; attempt derivation/late routing covered with stand-ins by issuer `tests/test_lifecycle.py:155-198`, not both production consumers. |
50: | `sign_by` representation | Issuer `util.py:69-82`: whole-second `YYYY-MM-DDTHH:MM:SSZ`; KMS `signer.py:77-88,144-146`; GCP `policy.py:79-82` uses verifier `utc`. **Agree for valid emitted dates.** Acceptance of malformed dates need not be identical. | K-full/K-slot/G-slot representative valid values; exact time/stop endpoints mainly signer-only. |
51: | Deadline semantics | Pipeline sends window signing stop, not the removed acceptance+24h deadline (`pipeline.py:594-596`). KMS `signer.py:187-192,231-243`; GCP `policy.py:132-137`, `signer.py:165-180`: refuse strictly **past** either request deadline or configured stop; equality permitted. Post-call check withholds late results. **Agree**, assuming correctly configured stop and clocks. | Successful joint paths; stop/refusal tests in each signer suite, not a joint pipeline endpoint matrix. |
52: | `frame_b64` | Canonical standard padded base64 from issuer `util.py:32-40`; KMS `signer.py:66-74,147-151`; GCP `policy.py:95-103` uses verifier canonical decoder. **Agree.** | K-full/K-slot/G-slot. |
53: | Inline request size | `INLINE_MAX=262144` measures entire UTF-8 JSON body, including ID/deadline/base64; only `>` switches to a reference (`signers.py:27,64-70`). Both signer body caps are 1048576 (`signer-kms/signer.py:35,128-130`; `signer-gcp/policy.py:25,55-56`). The issuer's inline output fits both, including equality. No separate smaller signer inline cap. **Agree.** | Joint small/large paths, not an exact 262144-byte boundary sweep. In-memory issuer queue enforces its size cap (`queues.py:17,40-42`). |
54: | Frame length | Issuer encoder caps payload at `2^24` plus framing (`encode.py:15,29-32`); API content is bounded to 1 MiB. KMS reference cap `2^25` (`signer.py:36,162-165`); GCP cap `2^24+262` (`policy.py:26`, `signer.py:138-146`). Both cover every issuer frame; the shared decoder still enforces schema/payload caps. **Agree; raw cap constants differ harmlessly.** | K-full includes 1 MiB input; Scratch-both does too. G-slot reference is smaller. Maximum codec payload and over-cap rejection not jointly exercised. |
55: | `frame_ref` path and rid | Issuer `_send` and `ResultStore.ref` emit `frames/<64 lowerhex rid>/<64 lowerhex digest>`; rid derives from `api.record_id` (`api.py:41-42`). KMS `RE_REF` (`signer.py:42`) accepts precisely that form. GCP `RE_REF` (`policy.py:29`) also accepts other 1–128-character safe rid components. **Agree on actual output; validators are not identical.** | K-full exercises actual `_send`; G-slot substitutes `rid-7`; new issuer test checks the actual produced path against a copied regex. Scratch-both exercises actual path with GCP. |
56: | `frame_sha256` request | Issuer `signers.py:69` emits SHA-256 of raw frame, 64 lowercase hex. KMS requires filename equals digest and fetched bytes match (`signer.py:152-165`). GCP validates digest shape and bytes (`policy.py:87-92`; `signer.py:147-148`), but does **not** require filename equals supplied digest. **Actual output satisfies both.** GCP's broader acceptance is not an issuer incompatibility. | K-full/K-slot/G-slot; G-slot replaced-object refusal at `:55-63`; KMS digest tampering also signer-only. |
57: | Bucket selection | Bucket is configuration, never request JSON. Issuer S3 store writes to result bucket (`aws.py:221-231`); KMS uses `FRAMES_BUCKET` (`lambda_app.py:33-43,68-69`); GCP uses `FRAME_BUCKET` (`main.py:73-75`; `signer.py:133`). Deployment passes issuer result-bucket output (`service/issuer/infra/outputs.tf:5-7`; signer KMS `infra/variables.tf:19`; GCP `deploy.sh:136-142`). **Agree if wired as documented.** | Fake stores/buckets in joint tests. No joint deployed bucket/IAM test; no live configuration checked. |
58: | Frame tags, encoding and payload fields | Issuer `encode.py:29-32,47-62` emits version-1 framed canonical JSON, `tessera-v1/attest` or `tessera-v1/manifest`. Attest has `common.{alg,binding_forms,content,declared_issue_time,issuer,manifest_sha256,preamble_sha256,profile,spec.{id,sha256},vectors_sha256}` and `signer.key_fp`; manifest has `{alg,issuer,key_fp,sset,ver}`. Both consumers run the service verifier's `read_frame` and require the hybrid alg (KMS `signer.py:168-185`; GCP `policy.py:106-129`). **Agree on producer output.** Signers do not independently establish every receipt-level relationship; `_seal` and pre-ship supply further checks. | K-full uses actual encoder frames; K-slot/G-slot use fixtures. Scratch-both confirms actual GCP attest and manifest policy compatibility. |
59: | Key fingerprints and slot meaning | Issuer `encode.py:35-40`: `spki-sha256:<64 lowerhex>` over SPKI for kms, `gpg-sha256:<64 lowerhex>` over v4 public-key body for gpg. KMS startup pins the former (`signer.py:95-96,109-124`); GCP reconstructs body with configured creation time and pins the latter (`signer.py:66-87`; `main.py:25,64-75`). KMS checks attest signer or manifest `key_fp`; GCP checks attest signer or manifest `sset[0]`. **Agree.** | K-full/K-slot/G-slot fingerprint/signature checks; GCP actual-window key checked by Scratch-both. Wrong startup key/time primarily signer-only. |
60: | Declared time / epsilon | Actual attests carry allocation time (`pipeline.py:653-656`). Both production signers refuse iff absolute clock difference exceeds 86400 seconds (`signer-kms/signer.py:180-184`; `signer-gcp/policy.py:123-128`). Manifest has no declared time and skips epsilon. **Agree.** The issuer stand-in applies epsilon only to gpg (`signers.py:136`), so its policy is weaker than production KMS, but the production KMS tests execute the real check. | K-full successful actual times; G-slot future-time refusal reaches `receive` (`:87-93`), not `drain`. Signer-only tests cover endpoints. |
61: 
62: ### Responses and queue metadata
63: 
64: | Boundary | Producer and issuer consumer; agreement | Joint coverage |
65: |---|---|---|
66: | Response JSON and `request_id` echo | KMS `signer.py:258-269`; GCP `signer.py:154-164,186-198` emit object with echoed ID; invalid requests can have null ID. `SlotSigner.receive` parses objects and substitutes a diagnostic object for malformed bodies (`signers.py:77-89`). `_take` validates `req-<40hex>` and resolves its own index (`pipeline.py:460-483`). **Agree for issuer-created requests.** | K-full/K-slot/G-slot. |
67: | `status` | Both emit exactly `SIGNED` or `REFUSED`. Issuer recognizes these; other values become `OTHER` (`pipeline.py:464`). Unknown responses do not advance jobs. **Agree.** | Both statuses in G-slot, SIGNED through K-full. REFUSED-to-end-and-allocate uses issuer stand-in tests; no retained full GCP refusal lifecycle test. |
68: | `sig_b64` and signature format | Both encode canonical standard base64. KMS returns raw ML-DSA-65 rule-R signature, verifies it locally (`signer.py:195-210,236-243,268`); GCP assembles one OpenPGP v4 P-256 rule-O packet and verifies it (`signer.py:90-108,186-187`). Issuer decodes then verifies exact job frame under pinned slot key (`pipeline.py:467-475,516-521`; `signers.py:37-45`). **Agree.** | K-full/K-slot/G-slot plus Scratch-both. |
69: | `reason` and lifecycle consequences | Issuer accepts bounded `[A-Z][A-Z0-9_]{0,63}`; missing reason becomes `NO_REASON` in the end record, malformed/oversized becomes `UNRECOGNIZED_REASON` with diagnostic reference (`pipeline.py:128,438-453,465,496-500`). It does **not** branch on particular signer reason strings: any matching current unsigned job's REFUSED discards the attempt. KMS reasons include `BAD_REQUEST`, `FRAME_UNAVAILABLE`, `FRAME_TOO_LARGE`, `FRAME_DIGEST_MISMATCH`, `ALG_NOT_ALLOWED`, `KEY_FP_MISMATCH`, `DECLARED_TIME_OUTSIDE_EPSILON`, `SIGNING_STOPPED`, `SIGNING_ERROR`, `INTERNAL_ERROR` and decoder codes; GCP uses corresponding policy/codec reasons, `SIGNER_ERROR`, `INTERNAL`, and `FRAME_UNAVAILABLE` for over-size/final fetch failure. **Names differ but all interoperate with the generic refusal path.** | G-slot reads two concrete refusal reasons and missing-deadline BAD_REQUEST. Signer-only tests cover the wider set; issuer tests independently cover bounded reason handling and discard. No complete real-producer-to-`_take` reason matrix. |
70: | `detail` | Both return optional text; issuer `_take` ignores it. Oversized/malformed **reason**, rather than `detail`, is what `_keep_diagnostic` preserves. **No required dependency or mismatch.** | Present in real responses in round trips; retention of detail is not asserted or implemented. |
71: | `frame_sha256` echo | Both include it on SIGNED and where available on refusals (`signer-kms/signer.py:261-269`; `signer-gcp/signer.py:164`). Issuer ignores this echo and logs the indexed expected digest (`pipeline.py:472-475`), then verifies the signature on stored bytes. **Compatible, but no echo-equality gate.** Do not describe the echo as independently checked. | Emitted in joint tests; no negative echo-consistency test through pipeline. Wrong echo alone does not invalidate a valid signature. |
72: | `signer.slot`, `signer.clock`, `key_fp`, `epsilon_s`, `sign_until` | KMS `_signer_info` (`signer.py:213-215`) and GCP `_signer_info` (`signer.py:111-115`) emit these. Clocks are UTC whole-second strings; GCP captures response metadata at handling start, KMS uses its latest assigned clock. Issuer does not authenticate, compare or use these fields for lifecycle/signature acceptance: slot comes from queue, key from configuration, time from its own clock (`pipeline.py:460-500`). **Compatible diagnostic fields, not independent time evidence.** | Responses transported in joint tests; no pipeline metadata validation because none is specified by its consumer. |
73: | GCP additional fields | `v=1`, `sqs_message_id`, optional `kind`, `sig_sha256`, plus signer `code_sha256`, `image`, `key_version`, `alg` (`signer.py:111-115,154-156,186-187`). Issuer tolerates/ignores all of these; signature hash is recomputed from decoded bytes. KMS need not emit them. **Agree on the required subset.** | G-slot transports them; K-full confirms KMS needs no GCP-only fields. |
74: | SQS body and attributes | Both directions send only `MessageBody`, with no custom `MessageAttributes` required (`queues.py:79-85`; KMS `lambda_app.py:50-51,73-90`; GCP `signer.py:192-193,208-211`). Request redelivery count is system `ApproximateReceiveCount`: KMS Lambda event lower-case `attributes`, GCP polling response `Attributes`; both retry transient provider errors below 3 receives, then respond REFUSED. **Agree; envelope casing follows separate adapters.** | K-slot invokes real Lambda handler with fake mapping; G-slot invokes real GCP run loop with fake SQS. Actual SQS/Lambda envelopes not exercised live. |
75: | Issuer response age/order/count | Issuer `SqsQueue.receive` requests `SentTimestamp` and `ApproximateReceiveCount`; converts milliseconds to seconds; sets seq=0 for SQS; absent timestamp becomes None and unknown count conservatively 2 (`queues.py:82-93`). `SlotSigner.receive` returns `(handle,body,(sent-or-inf,seq,receives))`; drain orders by sent time and batch/slot tie-break, uses receives for resumable handling (`pipeline.py:415-425,491-524`). Signers do not supply these attributes in response JSON; SQS supplies them. **Agree.** | K-full uses actual issuer Message/InMemoryQueue; G-slot's corrected QueueView supplies count but None/0 for sent/seq. Oldest-first and ILC-I9 progress have issuer tests (`test_lifecycle_round3.py:331,483`), not joint cloud-adapter coverage. |
76: | Acknowledgement and retry | KMS mapping deletes successful handled messages and reports partial failures (`lambda_app.py:73-90`; `infra/main.tf:151-155`). GCP sends answer before request deletion (`signer.py:192-193`); failed send/delete permits redelivery. Issuer acknowledges only after `_take` finishes (`pipeline.py:424-432`). **Agree with at-least-once delivery**, not exactly-once signing. | K-slot/K-full mapping fake; G-slot fake SQS; GCP signer-only failed-delete and retry tests. |
77: 
78: ### Infrastructure permissions and configuration
79: 
80: The poller writes frame objects, sends each slot's requests, and receives/deletes responses (`service/issuer/infra/main.tf:237-262`). The API does not need signer-queue or signing grants. Result-bucket encryption is AES256 (`aws.py:231`), so the reference-read design does not require a separate SSE-KMS decrypt grant.
81: 
82: KMS Lambda role: `service/signer-kms/infra/main.tf:100-115` grants request Receive/Delete/GetQueueAttributes, response Send, and GetObject on `${frames_bucket}/frames/*`. `FRAMES_BUCKET` is supplied in `:16-22`, consumed by `lambda_app.py:68-69`. Its event source reads the issuer's kms request queue (`:151-155`). It does not need the issuer's remote signer-role assumption; the KMS README explicitly excludes `kms` from `signer_principals` (`:53-54`).
83: 
84: GCP: there is no `service/signer-gcp/infra/`. `deploy.sh:108-131` constructs the Google web-identity federated role and its permission to assume the issuer's gpg signer role; `:139-142` configures both roles, queues and FRAME_BUCKET. The issuer's `signer_principals` trust and policy (`service/issuer/infra/main.tf:289-319`) supply per-slot request/response access and GetObject on `${results_bucket}/frames/*`. Runtime assumes the configured roles before use (`service/signer-gcp/tessera_signer/main.py:87-95`). GCP's HSM IAM is separate from AWS frame access.
85: 
86: **Repository grants agree with the read paths.** None grants signers object writes or depends on an attempt-prefixed name. They are source inspections backed by static infra/adapter tests, not an applied-plan or live-principal proof. Bucket, role, queue, pinned key/creation time and SIGN_UNTIL still have to be wired consistently at deployment; no test establishes that those deployed values match the issuer window.
87: 
88: ## C. Harness changes
89: 
90: The unpacking edits discard only the new age key; they retain status, signature verification, duplicate-signature identity and queue-empty assertions (`service/signer-kms/tests/test_roundtrip.py:64-70`; `service/signer-gcp/tests/test_issuer_protocol.py:26-27,76-84`). They do not change signer response handling or signer retry thresholds.
91: 
92: GCP `QueueView.receive` now requests the real count from FakeSqs and places it in the issuer's Message (`tests/fakes.py:93-99`). FakeSqs increments and returns the count only when requested (`:50-62`). This strengthens fidelity; it does not hard-code every delivery as first. The scratch check deliberately omitted acknowledgement and advanced past visibility: receives changed **1 → 2**. None of the old receive-count cases was removed. Remaining limitation: sent=None and seq=0 mean this test wrapper cannot test cross-slot oldest-first order; that was not previously covered by these tests either.
93: 
94: ## Appended owner prechecks
95: 
96: | Check | Result | Evidence and consequence |
97: |---|---|---|
98: | 1. Capture row | **PASS** for the reviewed interface claims and this report. | `docs/V1-CONTRACT.md:34-37,50-53,72-74` governs the boundary: fresh attacker-key receipts can pass after DNS+git capture; no capture detection/public visibility is promised. Pinning each configured signer's key and checking its frame does not add a service-key listing or prevent attacker-controlled alternate authority/key material from verifying. |
99: | 2. Trigger clause | **PASS** for the fix's operative conclusions. | Cleanup requires request termination (`pipeline.py:317-329`), not an ended attempt. Refusal-to-discard requires indexed current waiting job (`:479-500`); signing closure is evaluated after recovery (`:681-687`). N-exhaustion is tested only after ending N (`:296-301`). No sampled-unavailability trigger is inferred from age, failure count or the frame rename. Amendment 11 remains explicitly unsigned (`:3-10`); its proposed consequences are not invoked as adopted authority here. |
100: | 3. Requester | **PASS**, bounded to source configuration. | The issuer can cause both signatures by writing policy-conforming requests (`issuer/infra/main.tf:254-257`; `pipeline.py:596`). Anybody else with queue-send or direct invocation/role/code/key-management capabilities may also cause work or change policy. The KMS policy restricts what passes, not whose content it is (`signer-kms/README.md:61-65`). Deployment requester enumeration is still required (`issuer/DEPLOY.md:66-71`), not established by key non-exportability or these tests. Issuing-account compromise remains unprotected (`V1-CONTRACT.md:73`). |
101: | 4. Binding text | **FAIL — pre-existing, not caused by FIX.diff.** | ISI-02: dedicated signer-role placement differs from registered `HYBRID-SUPPLEMENT.md:173-174`; unsigned A11 `:240-250` cannot amend it yet. Gated indefinite-open behavior (`pipeline.py:46-49`; lifecycle decision `:189-196`) does not discharge A2.3 `:288-289`. The frame-reference format and INLINE_MAX are engineering contracts being compared for interoperability, not promoted into registered security requirements. No schedule ruling-budget or 24-hour FAILED rule is used as authority. |
102: 
103: ## Validation and conclusion
104: 
105: Executed `.venv/bin/python -m pytest -q` separately in all four package directories. Results: issuer **235 passed** (133.25 s); signer-kms **48 passed** (14.96 s); signer-gcp **118 passed** (0.47 s); verifier **135 passed, 77 subtests passed** (47.39 s). No suite failures or skips were reported. The scratch probe uses both production signer classes with the real issuer local pipeline and its TEST window keys, while replacing provider clients and queues. Both sizes reached COMPLETE through actual pre-ship checking, and both GCP attestation and manifest were signed. This is local execution evidence; it does not establish deployed code identity, live IAM, model refinement, general liveness, or registration adoption.
106: 
107: The fix is appropriate to keep. No regression was found in attempt isolation, frame binding, cleanup, signature storage, or harness receive counts. Retain the GCP pipeline integration coverage to prevent the same defect class from recurring, and keep the existing registration decisions separate from this functional confirmation.

=== FILE (new): docs/reviews/issuer-signer-interface/DISPOSITION.md
1: # Disposition: issuer <-> signer interface review (owner, 2026-10-30)
2: 
3: Codex report: `CODEX-REVIEW.md`. Brief: `BRIEF.md`. The fix as reviewed: `FIX.diff`.
4: 
5: | Finding | Disposition |
6: |---|---|
7: | Fix (frame name = `sha256(frame)`) | **Confirmed** by Codex: no loss of attempt isolation, cleanup, sealing, retry or IAM behaviour. Kept. |
8: | Interface sweep (B) | No other issuer/signer mismatch found across request, response, queue-metadata and grant boundaries. |
9: | ISI-01 (Low): GCP coverage substituted the frame producer | **Fixed.** `service/signer-gcp/tests/test_pipeline_roundtrip.py` runs both production signer classes behind the issuer's real pipeline, inline and 1 MiB, to COMPLETE and VALID_STRICT, plus the redelivery-count check. Control: with only the issuer fix reverted, the 1 MiB case ends `REFUSED ATTEMPTS_EXHAUSTED`. |
10: | ISI-02 part 1: K-R enforcement "in unsigned Amendment 11" | **Reviewer error, caused by our record.** A11 was signed at `f01e086`; the signing commit is its signing act (A11 preamble), and §A11.5 item 5 amends the K-R enforcement to the signer role. The file's header still says "DRAFT … Not signed" because signed text is not edited. The README status row now says so, so the next reader is not misled. |
11: | ISI-02 part 2: indefinitely open attempts vs A2.3 | **Known and open**: the author's termination decision (handoff 2026-10-30). Owner proposal: a fixed wall-clock bound ending in an explicit refusal, in one V1 implementation amendment. |
12: | Precheck 4 FAIL | Same two items as ISI-02; the first is resolved as above, the second is the open decision. |
13: 
14: Suites after disposition: issuer 235, signer-kms 48, signer-gcp 121, verifier 135 (77 subtests), all passing.

=== FILE (new): docs/reviews/issuer-signer-interface/codex-last.md
1: Wrote [CODEX-REVIEW.md](docs/reviews/issuer-signer-interface/CODEX-REVIEW.md).
2: 
3: Confirmed the fix; no new functional mismatch found. All four suites passed. Report includes the contract inventory, GCP integration coverage gap, and prechecks: three PASS, binding text FAIL for existing registration conflicts.
4: 

=== FILE (new): docs/reviews/signers/REQUESTERS.md
1: # Who can cause a signature (DEPLOY.md step 8, SG-04) — owner, 2026-11-02
2: 
3: Enumerated against the live accounts after steps 5–7. Method: the live KMS key policy, the IAM inline and attached
4: policies of every role in account 477139661040 (there are no IAM users), queue listing, the GCP key and project
5: IAM. `iam simulate-principal-policy` is **unusable** here: the account is an Organizations member and the simulator
6: returns `explicitDeny` with `AllowedByOrganizations: false` for every request, including ones the role plainly allows.
7: So this is a policy reading, not a simulation, and should be confirmed by a reviewer.
8: 
9: ## The account's place in AWS Organizations
10: 
11: - 477139661040 (Tessera) is a **member account** of organization `o-iljslwvgd9`. The management account is
12:   **871341458535**, email `aws-tessera@wamason.com`, the author's login. SCPs are enabled.
13: - The author's session is `AccountFullAccessRole` (AdministratorAccess), assumed via `account-access.amazonaws.com`.
14: - The management account can also assume `AWSManagedAccountManagementAccessRole` (via
15:   `aws-role-management.amazonaws.com`), whose policy can create roles, attach policies and update trust policies: a
16:   full privilege path. And `AWSManagedAdvancedFeaturesActivationRole` (via `account.amazonaws.com`).
17: - **So the author's administrator identity is the management account 871341458535 and whoever holds its
18:   credentials.** Everything below that says "admin" means that.
19: 
20: ## kms slot (AWS KMS key `2c9ba2cf-…`, ML-DSA-65)
21: 
22: | Capability | Who | Basis |
23: |---|---|---|
24: | `kms:Sign` | `tessera-v1-signer-kms-role` only | Live key policy: SignerRoleOnly + DenySignToEveryoneElse. Negative test: the admin session was refused with an explicit deny (DEPLOY-RUN 2026-11-02). |
25: | Send work to the signer (`sqs:SendMessage` on `tessera-v1-issuer-kms-requests`) | `tessera-v1-issuer-poller` (by design); admin | Poller inline policy; AdministratorAccess. |
26: | Change the signer (`lambda:UpdateFunctionCode`, `iam:PassRole` on the signer role, change the role) | admin | AdministratorAccess; management roles. |
27: | `kms:PutKeyPolicy` | the account root principal, i.e. any account administrator | Key policy KeyAdministrationWithoutSign. A management event, recorded by the Object-Locked trail. |
28: 
29: ## gpg slot (GCP KMS `slot2-v1`, HSM P-256)
30: 
31: | Capability | Who | Basis |
32: |---|---|---|
33: | `cloudkms.cryptoKeyVersions.useToSign` on `slot2-v1` | `tessera-signer-gpg@tessera-slot2` only (key IAM) | `gcloud kms keys get-iam-policy slot2-v1`: signer + publicKeyViewer, that SA only. |
34: | Send work (`sqs:SendMessage` on `tessera-v1-issuer-gpg-requests`) | `tessera-v1-issuer-poller`; admin | As above. The signer's AWS path is federated: Google ID token → `tessera-v1-signer-gpg-federated` → `tessera-v1-issuer-signer-gpg` (receive requests, send responses, read `frames/*` only). |
35: | Run, update or override the job; act as or mint tokens for the runtime SA; change key IAM | GCP project owner `wamason@gmail.com` (the only human principal) | Project IAM: `roles/owner` is that user alone; the rest are Google service agents and `slot2-builder` (log writer only). |
36: 
37: ## Outside the V1 path, still present
38: 
39: - `tessera-slot2-signer-sqs` (AWS role, 2026-10-14 prototype): assumable only by the disabled prototype SA
40:   (uniqueId 100451337620005518976); reaches only `tessera-slot2-requests/-responses`, which feed nothing. Cannot
41:   cause a V1 signature. Delete with the prototype queues and the spike keys (HYBRID-SUPPLEMENT §11 item 6).
42: - Spike keys `alias/tessera-pq-spike` and `slot2-spike`: retire-instrument removed the prototype's signing access to
43:   `slot2-spike`; deletion follows the supplement's conditions.
44: 
45: ## Result against the gate
46: 
47: Beyond the issuer (poller), the two signers and the author's administrator identity, **no principal can cause a
48: signature**. The gate passes, with two notes that belong in the V1 contract's limits, not in a fix:
49: 1. The administrator identity is two credentials in two clouds: the AWS management account (871341458535) and the
50:    GCP owner `wamason@gmail.com`. Capturing either one gives control of that one slot's signer. Capturing both gives
51:    control of both. This is C3, already disclosed.
52: 2. AWS Organizations adds the management account's role-management path, which is not visible from the member
53:    account's own IAM. The CloudTrail trail records its effects in this account.

=== FILE (modified; diff hunks, + lines are new): formal/PROPERTIES.md
diff --git a/formal/PROPERTIES.md b/formal/PROPERTIES.md
index cfe79f6..8664eb2 100644
--- a/formal/PROPERTIES.md
+++ b/formal/PROPERTIES.md
@@ -167,4 +167,7 @@ Cross-cutting obligations (A1.4, A1.7):
 - [ ] Parameter ratification at Band 0 exit: δ = 72h, ε = 24h, k = 6,
       and (A2.3) the issuance attempt bound N (working default 3).
+      *(2026-10-29, Amendment 11 c093: S = 24 h belongs in this list. For `tessera-v1-strict`, all five
+      parameters, δ = 72 h, ε = 24 h, k = 6, N = 3 and S = 24 h, were ratified by the author's signature on A9
+      (A9:223-225). The Band 0 exit item stays open outside V1 (A11 §A11.3 row 4).)*
 - [x] **P5 issuance corollary** (anchor confirmed at depth k within δ;
       re-issue on late/reorged anchors) — modeled as a real state machine


=== FILE (new): formal/tla/issuer-lifecycle/RESULTS.md
1: # Issuer lifecycle model: results (2026-10-29)
2: 
3: This is the formal side of the issuer change in `docs/decisions/2026-10-29-issuance-lifecycle.md` (design step 10). It
4: models **revision 4**: steps 1, 2 and 7 to 9 of revision 3, plus steps 3 to 6 and 10 of revision 4, after
5: `docs/reviews/issuance-lifecycle/CODEX-CONFIRM-2.md`. The work started against revision 3. The revision-4 brief arrived
6: before any revision-3 model was finished, so no separate revision-3 module exists. What the revision-3 analysis found
7: is recorded under F8. The AI collaborator entered this model. It is PROPOSED, not adopted.
8: 
9: Files (all in `formal/tla/issuer-lifecycle/`):
10: 
11: | File | Role |
12: |---|---|
13: | `IssuerLifecycle.tla` | The module. One spec; `Variant` selects the correct design or a broken companion. |
14: | `IssuerLifecycle.cfg` / `.out` | Correct model, safety (P1–P3). |
15: | `IssuerLifecycle_B1.cfg` / `.out` | B1′: expiry or discard on incomplete evidence. |
16: | `IssuerLifecycle_B2.cfg` / `.out` | B2: a second concurrent writer. |
17: | `IssuerLifecycle_B3.cfg` / `.out` | B3: expiry on a failed or partial fetch. |
18: | `IssuerLifecycle_Live.cfg` / `.out` | P4 termination. |
19: | `IssuerLifecycle_LiveNoStep5.cfg` / `.out` | P4 control: step 5 disabled. Must be red. |
20: | `IssuerLifecycle_Sanity.cfg` / `.out` | Vacuity witnesses. |
21: | `IssuerLifecycle_Residual.cfg` / `.out` | Residual witnesses. Not checked properties; reachability reports. |
22: | `run-witnesses.sh` | Runs each witness of a witness cfg as its own TLC run, stopping at the first violation. |
23: 
24: TLC: `java -XX:+UseParallelGC -cp ~/.local/lib/tla2tools.jar tlc2.TLC -workers auto -deadlock -noGenerateSpecTE
25: -metadir $(mktemp -d) -config <cfg> IssuerLifecycle.tla`. Witness cfgs use `./run-witnesses.sh <cfg>`. `-deadlock`
26: is needed because terminal states (shipped, refused, MaxTime) are artifacts of the bounds. TLC 2026.07.31, 12 cores.
27: 
28: ## 1. What is modelled, and how
29: 
30: **Timeliness is the registered fact, not the issuer's write.** `bur[i]` is attempt i's `burialAtWall`. `pass[i]` is
31: the chain verdict of the three-conjunct predicate on its lowest qualifying presentation. The attempt is
32: *timely-eligible* when `bur[i] # NoTime /\ bur[i] <= decl[i] + Delta + Slack /\ pass[i]`. That is the expression in
33: `P5cP5P6_BridgeSlack_Latch.tla:49`, inclusive. No fetch, observation or durable write appears in it (ILC2-01).
34: 
35: **Environment, per attempt:**
36: 
37: - **Burial.** Happens at any wall time: before B, after B, or never. `pass` is chosen at burial.
38: - **Two attestations.**
39:   - `a1` sits at the lower height and carries `pass`.
40:   - `a2` sits at a higher height and always fails a conjunct. It is the ILC2-03 decoy.
41:   - Each one's evidence moves through 0 (calendar pending), 1 (attested, but the pinned `h..h+5` segment cannot yet be
42:     obtained) and 2 (segment obtainable). It only goes up, and a segment becomes obtainable only after burial.
43:   - Partial header recovery is modelled as `e2 = 2` while `e1 = 1`, followed later by `e1 -> 2`.
44: - **Fetches.** Each fetch returns, per attestation, any value in `0..e_j` or `Err`. A fetch can therefore be stale,
45:   partial or failed at any time. This is more adversarial than "monotone except a bounded outage". A fetch never shows
46:   more than exists.
47: 
48: **Issuer:**
49: 
50: - **Invocations.** Each invocation runs Start (read state and attempt id), then Fetch, then Send (wall reading,
51:   decision, one guarded write), then Await. Time may pass between any two steps, which models the observation-to-send
52:   delay. An invocation lives at most `Timeout` ticks.
53: - **Concurrency.** With reserved concurrency 1 there is one poller instance at a time.
54: - **Kill.** An invocation can be killed at any step, which covers a crash before persistence. Its sent writes stay
55:   pending and may commit up to `Lease` after the send, so a commit can come after the send. A new invocation may start
56:   while they are pending.
57: - **Resend and Drop.** Resend sends the same transition again (a duplicate transition retry). Drop means the store
58:   rejects the write.
59: - **Fault budget.** Kill, Resend and Drop share `MaxFaults`.
60: - **Guards.** Every write is guarded on (state, attempt id), evaluated atomically at commit.
61: - **Ending an attempt.** It allocates the next attempt in the same write, or records REFUSED at N.
62: 
63: **Decisions, for an open attempt:**
64: 
65: - **Eligible snapshot.** If the snapshot shows eligibility, the poller latches, at any time.
66: - **Complete negative snapshot.** If both segments are in hand and the lowest presentation fails, the attempt ends
67:   DISCARDED (now ≤ B) or EXPIRED (now > B).
68: - **Anything else.** No write, unless now > B + OpPeriod. Then the attempt ends EVIDENCE_UNAVAILABLE.
69: 
70: For a latched attempt the decision is to ship.
71: 
72: **Constants (main cfg):**
73: 
74: - `N = 2`.
75: - `Delta + Slack = 1`, so B = declared + 1. Only the sum enters the model.
76: - `Lease = 1`, `Timeout = 1`, `OpPeriod = 1`.
77: - `MaxTime = 7`, `MaxFaults = 2`.
78: 
79: `TrackGhosts = FALSE` freezes the witness-only ghosts at Init. Issuer actions never read a ghost.
80: 
81: **What is not modelled:**
82: 
83: - More than one request, and more than two attestations.
84: - Reorganisations. k-deep burial is assumed permanent (A1.6).
85: - Evidence authentication.
86: - `SIGNING_CLOSED` and all signing and stamping work.
87: - Step 7's post-latch incurable discard.
88: - Clock error between invocations. There is one wall clock.
89: - Store durability.
90: - The declared time of attempt i+1, which is taken as its allocation instant.
91: - The environment's later evidence for attempts that have already ended. It is irrelevant: a negative end needs
92:   complete evidence, so burial has already happened.
93: - Assembly after the latch, which is reduced to one ship write.
94: - `obsKilled` and `obsAt` are per-attempt approximations. "A timely eligible fetch existed" and "some invocation was
95:   killed holding an eligible snapshot" are recorded separately.
96: 
97: ## 2. Properties and results
98: 
99: | Run | Result | Distinct states | Generated | Depth | Time |
100: |---|---|---|---|---|---|
101: | Correct, P1–P3 (`IssuerLifecycle.cfg`) | **GREEN**: 12 invariants, 4 action properties | 20,932,180 | 82,762,154 | 38 | 3 min 15 s |
102: | P4 termination (`_Live`, MaxTime 11, MaxFaults 1) | **GREEN** | 6,988,497 | 21,986,330 | 55 | 4 min 58 s |
103: | P4 control, step 5 off (`_LiveNoStep5`) | **RED**, Termination (lasso back to state 50) | 1,409,692 | 5,048,583 | 68 | 37 s |
104: | B1′ incomplete-evidence expiry (`_B1`) | **RED**, NoTimelyExpiry, 9-state trace | 17,193 (stopped) | 46,189 | 14 | <1 s |
105: | B2 second concurrent writer (`_B2`, MaxFaults 0) | **GREEN** on the full safety set (see F4) | 29,649,190 | 140,070,613 | 33 | 5 min 04 s |
106: | B3 unavailable-as-false expiry (`_B3`) | **RED**, NoTimelyExpiry, 8-state trace | 4,983 (stopped) | 13,009 | 12 | <1 s |
107: | Sanity, 13 witnesses (`_Sanity`) | **all 13 reachable** (healthy) | n/a | n/a | 11–21 | n/a |
108: | Residual, 3 witnesses (`_Residual`) | **all 3 reachable** | n/a | n/a | 12–19 | n/a |
109: 
110: **P1. NoTimelyExpiry: GREEN.**
111: 
112: - **Claim.** A timely-eligible attempt (registered definition) is never ended EXPIRED or DISCARDED.
113: - **Stronger forms, also green.** `NegativeEndsAreTrue`: every negative end has a failing chain verdict.
114:   `LatchIsTrue`: every latch has a passing one. `ExpiryAfterB`: an EXPIRED decision is taken strictly after B, and a
115:   DISCARDED one at or before B.
116: - **What it assumes about outages: nothing.** Fetches may fail, go stale or be partial forever. P1 also assumes nothing
117:   about the lease, kills, delays or the number of writers.
118: - **What it does assume:**
119:   1. No fetch shows more evidence than exists (evidence soundness).
120:   2. Complete evidence (every calendar attested, every segment obtained) fixes the lowest presentation, so its verdict
121:      is the chain verdict.
122: - **Not claimed.** P1 does not say a timely-eligible attempt is never ended EVIDENCE_UNAVAILABLE. It can be (F1, F2).
123: 
124: **P2. Mutual exclusion and bounds: GREEN.**
125: 
126: - `TypeOK`: one state per attempt.
127: - `OneLive`, `AllocatedPrefix`, `PastAttemptsEnded`: at most N attempts, allocated in order, only the current one live.
128: - `CompleteIffShipped`: at most one shipped.
129: - Action properties:
130:   - `LatchProtects`: latched or shipped never becomes ended.
131:   - `ShipFromLatch`: ship only from latched.
132:   - `EndedFrozen`: no write to an ended attempt takes effect, including orphaned and duplicate writes.
133: 
134: **P3. Refusal is atomic with the final end: GREEN.**
135: 
136: - `NoSilentEnd`: all attempts ended implies REFUSED.
137: - `NeverBetweenAttempts`: an active request always has an open or latched current attempt.
138: - `RefusedOnlyWhenExhausted`.
139: - `TerminalLatched` (action property).
140: 
141: **P4. Termination: GREEN** (`<>(req # "active")`). It rests on these assumptions:
142: 
143: - weak fairness of the poller's Start, Fetch and Send, and of write commit;
144: - strong fairness of Tick, which is disabled while an invocation or a write must resolve first;
145: - the schedule assumption `PollEachTick`: at least one poller start per time unit (the EventBridge rate);
146: - MaxFaults = 1.
147: 
148: There is **no fairness on evidence**: burial may never happen and every fetch may fail forever. Termination comes from
149: step 5. The control proves this: with `OpPeriod > MaxTime` it goes red, with a lasso in which the poller defers
150: forever on evidence that never completes. In a bounded model that lasso sits at MaxTime. The underlying cause, no
151: evidence fairness, does not depend on the bound.
152: 
153: **Sanity witnesses (all reachable):**
154: 
155: - ship;
156: - ship on attempt 2;
157: - refusal;
158: - EXPIRED, DISCARDED and EVIDENCE_UNAVAILABLE ends;
159: - a latch whose burial was after B;
160: - a latch on a timely burial first observed after B;
161: - a latch after a fetch saw the partial-header state (the lower attestation qualifying later);
162: - an orphaned in-flight write;
163: - a send later than its fetch;
164: - a commit later than its send;
165: - a resolved duplicate.
166: 
167: ## 3. Broken companions
168: 
169: **B1′. Expiry on incomplete evidence (revision-3 step 6, ILC2-03): RED on NoTimelyExpiry.**
170: 
171: 1. Attempt 1 is buried at 0 with `pass`.
172: 2. Both calendars attest. `a2`'s segment arrives (`e1 = 1, e2 = 2`).
173: 3. The poller fetches the class "every calendar attested, lowest in-hand presentation fails".
174: 4. It sends DISCARDED at now = 0 ≤ B, and the write commits.
175: 
176: A timely-eligible attempt has been discarded while its lower attestation's segment was still missing. With the full
177: invariant set, B1′ also violates `NegativeEndsAreTrue`.
178: 
179: **B3. Expiry on a failed or partial fetch: RED on NoTimelyExpiry.**
180: 
181: 1. Attempt 1 is buried at 1 = B with `pass`.
182: 2. At now = 2 > B the poller's fetch returns `Err`.
183: 3. The fetch is treated as negative, and EXPIRED commits.
184: 
185: With the main cfg's full set, TLC reports `NegativeEndsAreTrue` first: the expiry of a never-buried attempt on a
186: failed fetch is a shorter path. For that reason the B1′ and B3 cfgs check only `NoTimelyExpiry`.
187: 
188: **B2. A second concurrent writer: GREEN; it did not go red.** The prediction, recorded in the cfg before the run, was
189: green. See F4. Constants differ from main in one place, MaxFaults = 0. Two live processes already overlap writes, and
190: MaxFaults = 2 did not finish within minutes (more than 15M distinct states and still growing after 3 minutes).
191: 
192: ## 4. Design findings (revision 4)
193: 
194: **F1. P1 holds, and none of steps 1, 4(b) or the lease is needed for it.** P1 depends only on:
195: 
196: - evidence soundness;
197: - "complete evidence fixes the verdict".
198: 
199: It holds with fetches that fail forever, with kills, delayed commits and duplicates, and with two writers (B2). This
200: is what step 4 claims ("No lease timing is relied on"). **Step 10's text still says "expiry after `B + lease`".** That
201: is stale wording from revision 3 and contradicts step 4. The model does not use a lease in any expiry guard; the lease
202: only bounds how long writes stay pending.
203: 
204: **F2. EVIDENCE_UNAVAILABLE ends timely-eligible attempts by three distinct paths, not one.** Step 5 calls the named
205: residual "the one case where a refused attempt might have been observed eligible by B". The model reaches three paths:
206: 
207: - **(a) `ResidualKilledObserver`: the named residual.**
208:   1. Burial at 1 = B; evidence complete at 1.
209:   2. An invocation fetches eligibility at 1 and is killed at 2 before sending.
210:   3. The next invocation's fetch is stale. At now = 3 > B + OpPeriod it sends EVIDENCE_UNAVAILABLE, which commits.
211: - **(b) `ResidualUnobserved`: ILC2-01's path.**
212:   1. Burial at 1 = B.
213:   2. No invocation polls until 3.
214:   3. That one fetch fails, and EVIDENCE_UNAVAILABLE commits.
215: 
216:   No kill is involved, and no observation was ever made.
217: - **(c) `ResidualLiveObserver`: a path the design does not mention.**
218:   1. At now = 3, invocation 1's fetch is stale, so it sends EVIDENCE_UNAVAILABLE. Then it is killed and the write is
219:      orphaned.
220:   2. Invocation 2, never killed, fetches eligibility and sends the latch.
221:   3. The orphaned write commits first, and the live latch fails its guard.
222: 
223:   Reserved concurrency 1 serialises invocations, not writes (as CODEX-CONFIRM-2 notes). This happens within one tick,
224:   so no lease length prevents it.
225: 
226: In (a) and (c) the service did observe eligibility on time, so the observation lag was not greater than S. **A2.1's
227: permission ("an attempt whose lag exceeds S may be refused"), which step 5 cites, does not cover them.** Path (b) is
228: covered only under the prose reading in which B is the service's observation time (A2:115-124). It is not covered
229: under the model's `burialAtWall` reading. This is the refinement question ILC2-01 raised. The model exposes it; it
230: cannot settle it, and the owner must.
231: 
232: **F3. Step 5's rule is weaker than its stated residual.** The residual says "permanent loss of the evidence for the
233: whole operating period". The rule as written ("after an operating period past B, an unlatched attempt whose evidence
234: is still incomplete may be ended") is evaluated on one poll's fetch. In trace (a) the evidence was fully obtainable at
235: the moment of the decision, and a single stale or failed fetch after B + OpPeriod was enough.
236: 
237: To match the residual, the rule would need a condition over the period itself. Examples:
238: 
239: - no successful fetch of any source during the period;
240: - a bounded number of consecutive failures spread across it;
241: - re-checking a preserved observation record.
242: 
243: Which to use is an owner choice. As written, the residual is understated.
244: 
245: **F4. The single writer is not load-bearing for any checked safety property.** B2 is the same procedure and guards
246: with a concurrent API writer, and it is green on P1 to P3. (B2 runs with MaxFaults = 0, but the correct model's fault
247: paths already produce writer overlap: the orphaned writes in F2(c).)
248: 
249: The brief required B2 to go red. A faithful second writer cannot make it go red against these properties, and the
250: model does not force a red. What step 1 still buys lies outside this model:
251: 
252: - one fewer source of the F2(c) overlap;
253: - idempotent external work (signing and stamping jobs);
254: - removing the API's existing `settle` writer, which is real code (`api.py:194`) and must be removed regardless.
255: 
256: **F5. Step 5 is the only termination mechanism, and the only expiry path for an attempt that never confirms.** Under
257: revision 4, "pending" evidence (no burial, no attestation) is never a conclusive negative. So an attempt whose anchor
258: never confirms is never EXPIRED. It ends only through EVIDENCE_UNAVAILABLE after B + OpPeriod. The `_LiveNoStep5`
259: control shows that termination fails without that path.
260: 
261: As a result, the common lifecycle end that A2.3 calls expiry is implemented by the path that carries the F2 residuals.
262: EXPIRED is reserved for complete negatives after B. The registered refusal reason for exhausting N attempts is then
263: mostly `EVIDENCE_UNAVAILABLE`, not `ATTEMPTS_EXHAUSTED`. CL-03's reason set and the public status text should say so.
264: 
265: **F6. Underspecified: what EVIDENCE_UNAVAILABLE does to attempt i < N.** Step 5 says the attempt is "ended". Step 8
266: lists `EVIDENCE_UNAVAILABLE` as a *request refusal* reason. The model ends the attempt and allocates i+1. At i = N it
267: records REFUSED with reason EVIDENCE_UNAVAILABLE (and ATTEMPTS_EXHAUSTED when the final attempt was a negative end).
268: If the intent is that unavailability refuses the request at once, whatever i is, the design should say so.
269: 
270: **F7. Confirmed, and worth stating in the design.**
271: 
272: - A latch of a timely burial first observed after B is reachable and protected: the permissive "may".
273: - A late burial that passes the chain predicate also latches.
274: - Partial header recovery then latch is reachable, and a lower attestation qualifying later is honoured.
275: - The guards hold under duplicates and orphans (`EndedFrozen`).
276: - The latch evidence was chain-true in every reachable state (`LatchIsTrue`).
277: 
278: **F8. Revision 3 (not built as a module; analysis only).** In revision 3, outages made fetches *fail*; they did not
279: regress silently. Expiry required (a) not latched, (b) now > B + Lease and (c) a fetch that did not show eligibility.
280: With monotone evidence, (c) alone already prevented a timely *observed* attempt from expiring. If an earlier fetch had
281: shown eligibility, every later successful fetch would too.
282: 
283: So a B1 that drops only the lease wait could not go red unless silent regression was modelled. The lease mattered only
284: for silent regression, which revision 3 itself named in its residual (outage-induced regression), and for step 5's
285: unavailability end if OpPeriod < Lease. Revision 4 removes both dependencies.
286: 
287: ---
288: 
289: ## 5. Revision 5 (`IssuerLifecycleR5.tla`)
290: 
291: This section models design revision 5: steps 5, 8 and 10, rewritten after findings 1 to 6 above. The revision-4
292: files are left unchanged at 8793966, and every R5 file is new. The AI collaborator entered this model. It is
293: PROPOSED, not adopted.
294: 
295: ### 5.1 What changed in the model
296: 
297: - **`us[i]` (`unavailable_since`) and `ver[i]` (record version).** Every applied write to attempt i bumps `ver[i]`.
298: - **Setting `us[i]`.** A poll after B whose fetch does not succeed, and which read `us[i] = NoTime`, writes
299:   `us[i] := t`. The write is guarded on state and attempt id. The design gives it no version guard.
300: - **Reset.** A fetch *succeeds* when it is complete or shows the predicate holding. Every successful fetch of an open
301:   attempt already sends a latch or an end write, and that write is the reset. No separate reset write exists. A
302:   success whose write is lost therefore resets nothing (R5-F2).
303: - **EVIDENCE_UNAVAILABLE.** It is decided only by a live invocation that:
304:   - read `us[i] # NoTime` with `now − us[i] ≥ OpPeriod`;
305:   - had its own fetch fail;
306:   - re-fetched in the same step as the write.
307: 
308:   If the re-fetch succeeds, the poller latches or ends on it instead. Otherwise it sends the ending write, guarded on
309:   state, attempt id and the version it read.
310: - **Allocation and refusal.** Ending any attempt i < N allocates i+1. Ending attempt N records REFUSED with
311:   `ATTEMPTS_EXHAUSTED`. The per-attempt reason is the attempt's state.
312: - **`USReading`.** This constant chooses which wall reading `unavailable_since` takes (R5-F1):
313:   - `"fetch"`: the poll's fetch time, and the fetch must be after B;
314:   - `"send"`: the decision time.
315: 
316:   The main cfg uses `"fetch"`.
317: - **P5, checked as `P5_UnavailablePeriod`.** An attempt ended EVIDENCE_UNAVAILABLE had a failed poll after B at or
318:   before (decision − OpPeriod). The decider's own fetch and re-fetch both failed. No successful poll's write took
319:   effect, because such a write latches or ends the attempt.
320: - **P5 literal (reported, not checked).** "No successful fetch at all during the final OpPeriod before the ending."
321:   This counts fetches whose write was lost. The commit is taken as the ending, over the closed window
322:   [commit − OpPeriod, commit].
323: - **B4.** EVIDENCE_UNAVAILABLE after a single failed poll: the revision-4 rule (now > B + OpPeriod), with no
324:   `unavailable_since` and no re-fetch.
325: - **Bounds.** MaxFaults = 1 and MaxTime = 6; revision 4 used 2 and 7. At revision 4's bounds this module passed 190M
326:   distinct states after 35 minutes without finishing. MaxTime = 6 still lets both attempts end EVIDENCE_UNAVAILABLE;
327:   the sanity witness `RefusalAfterUnavailUnreachable` confirms it. Other constants are as in revision 4: B = declared
328:   + 1, Lease = Timeout = OpPeriod = 1.
329: 
330: ### 5.2 Results
331: 
332: | Run | Result | Distinct states | Depth | Time |
333: |---|---|---|---|---|
334: | Correct, P1–P3 + P5 (`IssuerLifecycleR5.cfg`, 13 invariants + 4 action properties) | **GREEN** | 13,453,877 | 42 | 2 min 20 s |
335: | P4 termination (`R5_Live`, MaxTime 10, MaxFaults 1) | **GREEN** | 100,977,268 | 63 | **3 h 01 min** |
336: | B1′ incomplete-evidence expiry (`R5_B1`) | **RED**, NoTimelyExpiry, 9 states | 16,537 | 14 | <1 s |
337: | B3 unavailable-as-false expiry (`R5_B3`) | **RED**, NoTimelyExpiry, 8 states | 4,592 | 11 | <1 s |
338: | B4 single-failed-poll EVIDENCE_UNAVAILABLE (`R5_B4`) | **RED**, P5_UnavailablePeriod, 9 states | 2,069 | 11 | <1 s |
339: | B2 second concurrent writer (`R5_B2`, MaxFaults 0) | **GREEN** on the full set, incl. P5 | 233,267,456 | 48 | **1 h 10 min** |
340: | `unavailable_since` at the decision (`R5_SendReading`) | **RED**, P5_UnavailablePeriod, 13 states | 67,708 | 15 | <1 s |
341: | Sanity, 10 witnesses (`R5_Sanity`) | all reachable (healthy) | n/a | 10–27 | n/a |
342: | Residual, 3 witnesses + P5 literal (`R5_Residual`) | all 4 reachable | n/a | 17–23 | n/a |
343: 
344: **B2 and Live.** Both are green, B2 as finding F4 predicted. At these bounds both are far outside the minutes budget.
345: If they are re-run routinely, their bounds need lowering. A smaller MaxTime for Live has not been checked for
346: vacuity.
347: 
348: **B4 trace.**
349: 
350: 1. The attempt is buried at 3 and fails its predicate. B = 1.
351: 2. The first poll ever is at 3 > B + OpPeriod, and its fetch fails.
352: 3. EVIDENCE_UNAVAILABLE commits at 3. The first failed poll after B is the deciding poll itself.
353: 
354: **Sanity witnesses (all reachable):** `us` set; latch after `us` was set; attempt 1 EVIDENCE_UNAVAILABLE followed by
355: a ship on attempt 2; refusal with both attempts EVIDENCE_UNAVAILABLE; an orphaned in-flight write; EXPIRED;
356: DISCARDED; EVIDENCE_UNAVAILABLE; ship; refusal.
357: 
358: ### 5.3 Residual paths under revision 5 (correct model, shortest traces)
359: 
360: All three are still **reachable**. In each trace the attempt is timely-eligible on the registered definition: buried
361: at 1 = B with the predicate passing.
362: 
363: **(a) Killed-before-write timely observation: REACHABLE** (18 states).
364: 
365: 1. At 1, a poll fetches eligibility, which is timely. It holds the snapshot across the tick and is killed at 2
366:    before sending.
367: 2. The poll at 2 gets a stale fetch. The evidence was obtainable throughout (`e1 = 2`); the source returned stale
368:    data, it was not down. That poll sets `unavailable_since = 2`.
369: 3. The poll at 3 has its fetch and its immediate re-fetch fail. Since 3 − 2 ≥ OpPeriod, it commits
370:    EVIDENCE_UNAVAILABLE.
371: 
372: The trace needs:
373: 
374: - a kill between the timely fetch and its write;
375: - a failed poll after B that starts the period;
376: - the decider's fetch and re-fetch failing at least OpPeriod later;
377: - no poll in between whose success took effect.
378: 
379: It does **not** need the evidence to be down, only that every poll in the period fails to obtain it, and it does not
380: need any polls between the two ends. Under a real 10-minute schedule, "every poll in the period failed" amounts to
381: whole-period loss as the design says. The rule itself does not require intermediate polls to exist.
382: 
383: **(b) Timely burial never observed: REACHABLE** (13 states).
384: 
385: 1. Burial at 1, while the calendars have not returned (`e1 = e2 = 0`).
386: 2. The poll at 2 fails and sets `unavailable_since = 2`. Its fetch was at 2; its send was at 3.
387: 3. The poll at 3 has its fetch and re-fetch fail, and EVIDENCE_UNAVAILABLE commits.
388: 
389: The trace needs the attempt's evidence to be unobtainable to every poll from the first failed poll after B through
390: the decision. Here it was genuinely absent: the calendars were pending. Whether A2.1 covers (b) is the B-meaning
391: question; see F2.
392: 
393: **(c) Leftover ending write beats a live latch: REACHABLE** (20 states).
394: 
395: 1. `unavailable_since = 2`.
396: 2. At 3, invocation 1's fetch and re-fetch fail. It sends EVIDENCE_UNAVAILABLE, guarded on version 1, and is killed.
397:    The write is left over.
398: 3. Invocation 2 starts, reads version 1, fetches eligibility and sends its latch. It is never killed.
399: 4. The leftover write commits first. The version is still 1, so the guard holds. The live latch then fails its
400:    guard.
401: 
402: The trace needs:
403: 
404: - a kill after the ending write is sent;
405: - a successor's eligible fetch and latch inside that write's lease;
406: - the successor having made **no write** before the leftover commits.
407: 
408: The version guard narrows (c) only to that last condition. It does not remove it, because the successor's latch is
409: itself the first write after the read.
410: 
411: **P5 literal: REACHABLE** (19 states). The ending write is decided at 4 on a failed fetch and re-fetch. The deciding
412: invocation is killed, and a successor fetches eligibility at 4. The leftover ending write commits before the
413: successor sends. A successful fetch therefore lies inside [commit − OpPeriod, commit]. The same is reachable with a
414: lost success *before* the decision: a successful poll that is killed before its write resets nothing.
415: 
416: ### 5.4 Design findings (revision 5)
417: 
418: **R5-F1. Which wall reading `unavailable_since` takes is unspecified, and one reading breaks P5.** "Set by the first
419: poll after B whose fetch cannot complete the evidence" does not say whether the poll's time and its "after B" are
420: judged at the fetch or at the decision. With the decision reading (`R5_SendReading`, RED on P5), the trace is:
421: 
422: 1. A poll fetches at 1 = B, not after B.
423: 2. The invocation is delayed across the tick and decides at 2. It records `unavailable_since = 2`.
424: 3. One failed poll at 3 ends the attempt.
425: 
426: Only one failed fetch strictly after B exists, so the one-failed-poll protection is lost. This is the same shape as
427: the observation-to-send gap in ILC2-02. The size of the shortening is bounded by the invocation duration (300 s
428: against an operating period of hours), but it breaks the rule's own guarantee.
429: 
430: The fetch reading (main cfg) is green. The design should say: `unavailable_since` is a wall reading taken *before*
431: the fetch begins, and the fetch must begin after B.
432: 
433: **R5-F2. "Reset by any poll whose fetch succeeds" holds only for successes whose write takes effect. P5 literal is
434: not attainable by any implementation.**
435: 
436: - A successful poll that is killed before its write, or whose write the store rejects, leaves no durable trace, so
437:   nothing can reset on it.
438: - An ending write already sent can commit after a later successful fetch, as in path (c).
439: 
440: P5 as checked here is the attainable form: one failed poll is never enough, and no durable success intervenes. If
441: the author needs the literal form, it would require a durable record written *before* each fetch, for example a
442: per-invocation fence (R5-F3). That has not been modelled.
443: 
444: **R5-F3. The version guard does not close path (c).** The successor's first write is the latch itself, so the
445: version it read is still current when the leftover ending write commits. A candidate repair, **untested**: each
446: invocation durably bumps the attempt's version (a fence) before fetching, and waits for that write to commit. Any
447: write left over from a predecessor then fails its version guard. This is a candidate only. Revision 4's finding
448: still applies to any write path without a version guard.
449: 
450: **R5-F4. The residual statement in step 5 is accurate for (b), and needs one qualifier for (a).** (a) needs only
451: that every poll in the period *failed to obtain* the evidence. That includes stale or partial answers from sources
452: that are up, not only "evidence then stayed unobtainable" in the sense of an outage. (c) remains as stated, with the
453: condition in 5.3.
454: 
455: **R5-F5 (confirmed, no change needed).**
456: 
457: - Revision 5 is green on P1 to P5 under the fetch reading.
458: - B4 shows that the `unavailable_since` period is what P5 depends on.
459: - P1 is unaffected by the revision-5 changes. B1′ and B3 stay red.
460: - Termination: see the table.
461: - `USAfterB` holds: `unavailable_since` is only ever a failed poll's time strictly after B.
462: 
463: Files added (in `formal/tla/issuer-lifecycle/`):
464: 
465: - `IssuerLifecycleR5.tla`
466: - `IssuerLifecycleR5.cfg` / `.out`
467: - `IssuerLifecycleR5_B1`, `_B2`, `_B3`, `_B4`, `_SendReading`, `_Live`, `_Sanity`, `_Residual`, each as `.cfg` /
468:   `.out`
469: - `run-witnesses-r5.sh`
470: 
471: ---
472: 
473: ## 6. Revision 5.1 (`IssuerLifecycleR51.tla`)
474: 
475: This section models design revision 5.1, step 5, which applies R5-F1 to R5-F4. All files are new. Sections 1 to 5
476: and their files are unchanged. The AI collaborator entered this model. It is PROPOSED, not adopted.
477: 
478: ### 6.1 What changed in the model (relative to `IssuerLifecycleR5.tla`)
479: 
480: - **Fence.** After reading the record, an invocation sends a fence write: guarded on (state, attempt id, version
481:   read), bumping the version. It continues only after the fence commits. If the fence fails its guard or is dropped,
482:   the invocation ends. Every later write of the invocation is guarded on its fenced version and bumps it.
483: 
484:   The design names the version guard only for the fence and the ending write. This model applies it to every write;
485:   see R51-F3.
486: - **The fetch's wall reading `fat` is taken as the fetch starts.**
487:   - Only a failed fetch with `fat > B` counts.
488:   - `unavailable_since` is the `fat` of the first counted failure.
489: - **Counting failures.**
490:   - Each counted failed poll sends a `fail` write that sets `unavailable_since` if it is unset and increments
491:     `failed_polls`.
492:   - A committed latch or end clears both. A success that never commits resets nothing.
493: - **When EVIDENCE_UNAVAILABLE is allowed.** It requires, on the values read:
494:   - `now − unavailable_since ≥ OpPeriod`;
495:   - `failed_polls ≥ Expected − Allowance`, where `Expected = OpPeriod ÷ PollInterval`;
496:   - the decider's fetch fails;
497:   - its immediate re-fetch fails.
498: - **Poll rate.** `MaxPollsPerTick` caps poller starts per time unit:
499:   - 1 is the EventBridge schedule taken as a hard rate;
500:   - 2 is a burst (redelivery, an asynchronous retry, a loop).
501: 
502:   The cap must be finite, because every fence bumps the version. With unlimited polls per tick the first run reached
503:   depth 90 and was still climbing.
504: - **P5 (restated).** An EVIDENCE_UNAVAILABLE end had:
505:   - its first committed failed poll after B, at or before (decision − OpPeriod);
506:   - at least `Expected − Allowance` committed failed polls;
507:   - a failed fetch and a failed re-fetch at the decision;
508:   - no committed success in between.
509: - **`P5_Spread` (new).** Those committed failed polls *started* in at least `Expected − Allowance` distinct time
510:   units before the decision. In other words, no scheduled tick was skipped with the count made up elsewhere.
511: - **B5.** Revision 5.1 without the fence: writes are guarded on the version read at Start.
512: - **Bounds.**
513:   - OpPeriod = 2 and PollInterval = 1, so Expected = 2. Allowance = 0.
514:   - B = declared + 1. Lease = Timeout = 1. MaxFaults = 1. One poll per tick, except where stated.
515:   - Main and companions: N = 2, MaxTime = 6.
516:   - Residual and (c) checks: N = 1, MaxTime = 5. B = 1; the failed polls fall at 2 and 3; the end is decided at 4;
517:     a leftover write can still resolve until 5.
518: 
519: ### 6.2 Results
520: 
521: | Run | Result | Distinct states | Depth | Time |
522: |---|---|---|---|---|
523: | **(A)** (c) on the correct model, 2 polls/tick (`R51_C_Correct`: ResidualLiveObserver, LiveLatchLostToEnd) | **NOT violated: (c) UNREACHABLE** (exhaustive) | 6,042,359 | 78 | 50 s |
524: | (A) (c) on the correct model, 1 poll/tick (`R51_Residual`, ResidualLiveObserver) | **NOT violated: UNREACHABLE** (exhaustive) | 1,336,457 | 47 | n/a |
525: | (A) B5, no fence, same bounds (`R51_C_B5`) | **RED**: (c) reachable again | 653,170 | 27 | 6 s |
526: | (B) residual (a), 1 poll/tick (`R51_Residual`) | **REACHABLE** | 804,942 | 32 | n/a |
527: | (B) residual (b), 1 poll/tick | **REACHABLE** | 345,279 | 26 | n/a |
528: | (B) residual (a), 2 polls/tick (`R51_ResidualBurst`) | **REACHABLE** | 1,486,947 | 33 | n/a |
529: | (B) residual (b), 2 polls/tick | **REACHABLE** | 524,835 | 26 | n/a |
530: | (C) Correct: P1–P3, P5, P5_Spread, USAfterB (15 invariants, 4 action properties; `R51.cfg`) | **GREEN** | 55,000,011 | 59 | 8 min 31 s |
531: | (C) Correct with bursts (`R51_Burst`, 2 polls/tick) | P5 green; **P5_Spread RED** (R51-F1) | 1,098,650 (stopped) | 26 | 7 s |
532: | (C) B1′ (`R51_B1`) | **RED**, NoTimelyExpiry (12 states) | 24,373 | 15 | <1 s |
533: | (C) B3 (`R51_B3`) | **RED**, NoTimelyExpiry (10 states) | 10,870 | 13 | <1 s |
534: | (C) B4 (`R51_B4`) | **RED**, P5_UnavailablePeriod (11 states) | 6,309 | 12 | <1 s |
535: | (C) B2 (`R51_B2`, N = 1, MaxTime 5, MaxFaults 0) | **GREEN** on the full set | 3,095,528 | 46 | 38 s |
536: | (D) Termination (`R51_Live`, N = 1, MaxTime 7, 1 poll/tick, PollEachTick) | **GREEN** (see note) | 494,025 | 60 | 22 s |
537: | Sanity, 8 witnesses (`R51_Sanity`, ghosts on) | all reachable (healthy) | n/a | 9–28 | n/a |
538: 
539: **Termination note.** The first `R51_Live` run was red because of a bound artifact:
540: 
541: 1. The attempt latched at MaxTime = 7.
542: 2. The one-start-per-tick cap allowed no further poll in that final tick, so the ship never ran.
543: 
544: The cap is now lifted at `now = MaxTime` when `PollEachTick` is TRUE. That is the liveness configuration only. Every
545: safety cfg sets `PollEachTick = FALSE`, so their behaviour is unchanged by the edit; the safety `.out` files were
546: produced before it. The artifact run's output was not kept in the repository. Termination at N = 2 was not run: the
547: N = 2 safety space is already 55M states, and the liveness graph would not fit in 30 minutes.
548: 
549: **Why the (A) result is not vacuous.** B5 goes red at identical bounds. The correct-model sanity run reaches an
550: orphaned in-flight write and an orphaned fence. So the bounds can express the race, and the fence removes it.
551: 
552: **B4 trace.**
553: 
554: 1. The first poll ever starts at 4 > B + OpPeriod = 3.
555: 2. It fences, and its fetch fails.
556: 3. EVIDENCE_UNAVAILABLE commits at 4, with `failed_polls = 0`.
557: 
558: ### 6.3 Residual reachability under revision 5.1
559: 
560: In each trace the attempt is timely-eligible: buried at 1 = B with the predicate passing.
561: 
562: **(c) Leftover ending write beats a live latch: UNREACHABLE.** This holds at 1 and at 2 polls per tick, with one
563: kill, delayed commits and drops, checked exhaustively at the bounds above. A leftover ending write carries the
564: version its invocation fenced. Any successor must commit its own fence before it fetches, and that commit bumps the
565: version. The leftover write then fails its guard, or it committed earlier, in which case the successor's fence fails
566: on state and the successor never observes anything.
567: 
568: B5 (no fence) restores (c) in 27 steps:
569: 
570: 1. With polls in ticks 2 and 4, two failures are counted.
571: 2. The decider sends EVIDENCE_UNAVAILABLE and is killed.
572: 3. A successor reads the same version, fetches eligibility and sends its latch.
573: 4. The leftover write commits first.
574: 
575: **(a) Killed-before-write timely observation: REACHABLE**, at 1 poll per tick (32 steps).
576: 
577: 1. The tick-1 poll fences, fetches eligibility at B and is killed before writing.
578: 2. The polls started at 2, at 3 and at 4 (the decider) all run their fence, fetch and write, and all their fetches
579:    fail. The evidence was obtainable the whole time (`e1 = 2`); the sources answered stale or with an error.
580: 3. `unavailable_since = 2`. `failed_polls` reaches 2 by tick 4.
581: 4. The decider's fetch and re-fetch fail, and EVIDENCE_UNAVAILABLE commits at 4.
582: 
583: What it needs:
584: 
585: - a kill between the timely fetch and its write;
586: - **every scheduled poll from the first failed poll through the decision runs, and every one fails to obtain the
587:   evidence;**
588: - the decider's re-fetch fails too.
589: 
590: No poll is skipped. The fence wait shifts the tick-3 poll's fetch into tick 4, which is within the invocation
591: timeout.
592: 
593: **(b) Timely burial never observed: REACHABLE**, at 1 poll per tick (26 steps).
594: 
595: 1. Burial happens at 1. The calendars have not returned (`e1 = e2 = 0`) through tick 4.
596: 2. The polls started at 2, at 3 and at 4 (the decider) all fail.
597: 3. EVIDENCE_UNAVAILABLE commits at 4.
598: 
599: What it needs: every scheduled poll in the period runs and fails, with the evidence genuinely not yet available.
600: Whether A2.1 covers (b) is still the B-meaning question (finding F2).
601: 
602: **With bursts (2 polls/tick), polls can be skipped.**
603: 
604: - (a): the shortest trace needs no skip. The killed observer and a second poll both run in tick 1.
605: - (b): the polls start at 2, 4 and 4, so **tick 3 has no poll at all**. Two failures at 2 and 4 make
606:   `failed_polls = 2`, and the attempt ends at 4.
607: 
608: `R51_Burst` shows the same against `P5_Spread`: polls at 3, 5 and 5, tick 4 skipped, EVIDENCE_UNAVAILABLE at 5. The
609: count requirement is met while a scheduled interval had no poll (R51-F1).
610: 
611: ### 6.4 Design findings (revision 5.1)
612: 
613: **R51-F1. `failed_polls ≥ scheduled polls − allowance` counts polls, not intervals, so bursts can fill the gaps.**
614: EventBridge redelivery, Lambda asynchronous retries, or a poller that visits an attempt more than once per run can
615: add failed polls inside one interval. Those extra failures make up for an interval in which no poll ran at all. So
616: "every scheduled poll in the period ran and failed" is not what the counter guarantees. At one poll per interval it
617: is: `R51.cfg` is green on `P5_Spread`.
618: 
619: Candidate repairs, **not modelled**:
620: 
621: - count at most one failed poll per poll interval, for example by keeping the last counted interval and incrementing
622:   only when it changes;
623: - or keep the set or bitmap of failed intervals and require the period's intervals, less the allowance.
624: 
625: **R51-F2. The fence closes (c), as the design claims.** It costs one extra committed write per poll per attempt. It
626: also introduces an orphaned-fence path, which the sanity run reaches. An orphaned fence that commits late only
627: invalidates a live successor's writes. That is safe, but the successor's work is wasted and it must re-poll.
628: 
629: **R51-F3. The version guard on the `failed_polls` increment is load-bearing, and the design does not state it.** The
630: design names the version guard for the fence and the ending write. If the `fail` write were guarded only on (state,
631: attempt id), a duplicate send (an ambiguous response, then a retry) or a leftover increment would count one failed
632: poll twice. That is the same inflation as R51-F1. This model guards every write on the fenced version, so this is not
633: exercised; it is stated for the design and the code.
634: 
635: **R51-F4. (a) and (b) are narrowed as the design states, under one poll per interval.** Both now need every
636: scheduled poll from the first failed poll after B through the decision to run and fail. (a) additionally needs a kill
637: between a timely fetch and its write. A "fail" includes a source that is up but stale. The design's residual
638: statement is accurate at one poll per interval. With bursts it holds only after R51-F1 is repaired.
639: 
640: Files added (in `formal/tla/issuer-lifecycle/`):
641: 
642: - `IssuerLifecycleR51.tla`
643: - `IssuerLifecycleR51.cfg` / `.out`
644: - `IssuerLifecycleR51_{Burst,B1,B2,B3,B4,C_Correct,C_B5,Residual,ResidualBurst,Sanity,Live}.cfg` / `.out`
645: - `run-witnesses-r51.sh`
646: 
647: ---
648: 
649: ## 7. Revision 5.2 (`IssuerLifecycleR52.tla`, minimal variant)
650: 
651: This section models design revision 5.2, step 5. Finding R51-F1 is repaired by a set of failed interval indices, and
652: R51-F3 by stating that every lifecycle write is version-guarded. The module is `IssuerLifecycleR51.tla` with four
653: changes; everything else is as in section 6. The AI collaborator entered this model. It is PROPOSED, not adopted.
654: 
655: ### 7.1 Changes
656: 
657: - **The failed-interval set.**
658:   - The record keeps `fi[i]`, the set of failed interval indices. An index is (fetch start − `unavailable_since`)
659:     ÷ PollInterval.
660:   - A committed `fail` write adds its index. Indices at or beyond `Expected` lie outside the period and are not
661:     recorded.
662:   - Each interval counts once. A committed success clears the set, together with `unavailable_since` and
663:     `failed_polls`.
664: - **The end condition.** EVIDENCE_UNAVAILABLE needs `now − unavailable_since ≥ OpPeriod` and
665:   `|fi ∩ 0..Expected−1| ≥ Expected − Allowance`, plus the failed fetch and failed re-fetch.
666: - **Version guards.** Every write is version-guarded, as it already was in R51 (R51-F3).
667: - **`P5_Spread` is measured on fetch-start ticks.** The design defines the interval by the fetch start, so: the
668:   committed failed polls' fetches fall in at least `Expected − Allowance` distinct ticks in
669:   [`unavailable_since`, decision).
670: - **B6.** Revision 5.2 with the `failed_polls` counter instead of the set, which is the R51 rule.
671: 
672: **Bounds.** N = 1; B = declared + 1; OpPeriod 2 and PollInterval 1, so Expected = 2; Allowance 0; 2 polls per tick;
673: MaxFaults 1. MaxTime is 6 for the Burst, B6 and Sanity runs, and 5 for the residual and (c) runs.
674: 
675: ### 7.2 Results
676: 
677: | # | Run | Result | Distinct states | Depth | Time |
678: |---|---|---|---|---|---|
679: | 1 | 2 polls per tick (`R52_Burst`: P5, P5_Spread, NoTimelyExpiry, USAfterB), exhaustive | **GREEN** | 18,055,522 | 91 | 2 min 31 s |
680: | 1 | Vacuity at the same bounds (`R52_Sanity`) | EVIDENCE_UNAVAILABLE, refusal and ship all **reachable** | n/a | 16–26 | n/a |
681: | 2 | Burst traces (polls at 2,4,4 / 3,5,5) | **No longer end the attempt.** Covered by #1: no reachable EVIDENCE_UNAVAILABLE end leaves an interval of the period without a failed fetch. | | | |
682: | 3 | Residual (a), 2 polls per tick (`R52_ResidualBurst`) | **REACHABLE**, with a failed fetch in every interval | 1,725,115 | 33 | n/a |
683: | 3 | Residual (b), 2 polls per tick | **REACHABLE**, with a failed fetch in every interval | 591,795 | 26 | n/a |
684: | 4 | (c), correct model, 2 polls per tick (`R52_C_Correct`), exhaustive | **NOT violated: UNREACHABLE** | 7,833,548 | 80 | 1 min 06 s |
685: | 5 | B6, counter instead of set (`R52_B6`) | **RED on P5_Spread** | 684,153 | 26 | 4 s |
686: 
687: **B6 trace (#5).**
688: 
689: 1. A poll fetches at 3, fails, and sets `unavailable_since = 3`.
690: 2. The poll started at 4 waits for its fence and fetches at 5. It fails.
691: 3. A second poll fetches at 5 and fails, and with `failed_polls = 2` it ends the attempt.
692: 
693: Fetch ticks {3, 5}: interval 1 (tick 4) had no fetch, and the counter still allowed the end. This is the 3,5,5 shape
694: from section 6, on fetch-start ticks. Under the set rule the same polls give `fi = {0}` (index 2 lies outside the
695: period), so the attempt does not end. That is #1.
696: 
697: **Residual traces (#3).**
698: 
699: - **(a).** The tick-1 poll fetches eligibility at B and is killed. Fetches at 2, 3 and 4 all fail, with the evidence
700:   obtainable throughout. `fi` becomes {0, 1}. The tick-4 decider's fetch and re-fetch fail, and EVIDENCE_UNAVAILABLE
701:   commits.
702: - **(b).** Burial at 1, calendars pending. Fetches at 2 and 3 fail, so `fi = {0, 1}` (two polls ran in tick 3; one
703:   of them fetched in tick 3). The tick-4 decider fails, and EVIDENCE_UNAVAILABLE commits.
704: 
705: Both shortest traces have a failed fetch in **every** interval of the period. #1 shows exhaustively that no reachable
706: EVIDENCE_UNAVAILABLE end lacks one. So, at 2 polls per tick, (a) and (b) are reachable **only** when every interval
707: from `unavailable_since` to the decision contains a failed fetch. (a) also needs a kill between the timely fetch and
708: its write.
709: 
710: ### 7.3 Findings (revision 5.2)
711: 
712: **R52-F1. The repair works.** The set of interval indices restores "every interval of the period had a failed poll"
713: under bursts. B6 shows that the counter alone does not.
714: 
715: **R52-F2. Minor, for the implementation: intervals are keyed by fetch start, not by the schedule tick.** A poll that
716: waits for its fence across an interval boundary fetches in the next interval. Its own scheduled interval can then be
717: left without a failed fetch, and the attempt waits longer. That is safe: it only delays the end. The runbook's
718: operating period should allow for it. Revision 5.2 measures what the design says, so no change is needed.
719: 
720: No other finding. Not re-run for revision 5.2: P1–P3 at N = 2, B1′, B3, B4, B2, termination. The R52 changes touch
721: only the end condition and its bookkeeping. P5 and NoTimelyExpiry were re-checked in #1.
722: 
723: Files added (in `formal/tla/issuer-lifecycle/`):
724: 
725: - `IssuerLifecycleR52.tla`
726: - `IssuerLifecycleR52_{Burst,B6,ResidualBurst,C_Correct,Sanity}.cfg` / `.out`
727: - `run-witnesses-r52.sh`
728: 
729: ---
730: 
731: ## 8. Revision 5.3 (`IssuerLifecycleR53.tla`)
732: 
733: This section models design revision 5.3, step 5, after `docs/reviews/issuance-lifecycle/CODEX-CONFIRM-3.md` (ILC3-01
734: to ILC3-03 and section B). The module is `IssuerLifecycleR52.tla` with the changes below; its header lists them. The
735: AI collaborator entered this model. It is PROPOSED, not adopted.
736: 
737: ### 8.1 Changes
738: 
739: - **Rolling window (ILC3-03).**
740:   - `failed_intervals` holds **absolute** indices, `fetch_start ÷ PollInterval`, of committed failed fetches started
741:     after B. A committed success clears it.
742:   - EVIDENCE_UNAVAILABLE needs `|Win(now) ∩ failed_intervals| ≥ Expected − Allowance`, plus the failed fetch and
743:     failed re-fetch. `unavailable_since` is kept (for `USAfterB`) but no longer gates the end.
744:   - The constant `WindowMode` chooses `Win` (see R53-F1). With c = now ÷ PollInterval:
745:     - `"completed"`: c−Expected..c−1, the Expected most recent completed intervals. This is the main reading.
746:     - `"literal"`: c−Expected+1..c, the window ending *at* the current interval, counting committed failures only.
747: - **P5 restated over interval membership (ILC3-02).** At the ending commit, at least `Expected − Allowance` intervals
748:   of the decision's window each contain a committed failed fetch that **started** in that interval.
749:   `P5_SpreadOld` is the R51/R52 cardinality property (distinct fetch-start times before the decision), kept for B7.
750: - **`AllowKill` (ILC3-01).** FALSE disables `Kill`.
751: - **Companions.**
752:   - B6 and B7: the R51 counter rule.
753:   - B8: the R52 fixed window, with indices relative to `unavailable_since` and only the first Expected counted.
754: - **The liveness relief at MaxTime is capped at one extra start.** The R51 relief allowed unlimited starts at
755:   MaxTime, which makes the state space infinite whenever an attempt never ends, because every fence bumps the
756:   version. The first Live_A0 run reached depth 3,953 and was stopped. Safety cfgs set `PollEachTick = FALSE` and are
757:   unaffected.
758: - **Bounds.** OpPeriod 2, PollInterval 1 (so Expected = 2), B = declared + 1, Lease = Timeout = 1. All cfgs use
759:   PollInterval = 1, which makes B8's relative index equal R52's. The rest are stated per run.
760: 
761: ### 8.2 Results
762: 
763: | Item | Run | Result | Distinct states | Depth | Time |
764: |---|---|---|---|---|---|
765: | (5) | **Correct safety** (`R53.cfg`: P1–P3, USAfterB, P5 membership, 4 action properties; N = 2, MaxTime 6, 1 poll/tick, MaxFaults 1, Allowance 0) | **GREEN** | 41,001,345 | 60 | 6 min 35 s |
766: | (5) | Correct, 2 polls per tick (`R53_Burst`: P5, NoTimelyExpiry, USAfterB; N = 1, MaxTime 6) | **GREEN** | 20,956,376 | 91 | 2 min 41 s |
767: | (5) | (c) on the correct model, 2 polls per tick, exhaustive (`R53_C_Correct`) | **NOT violated: UNREACHABLE** | 8,322,323 | 80 | 1 min 06 s |
768: | (5) | B1′ / B3 | **RED**, NoTimelyExpiry | 20,527 / 10,093 | 15 / 14 | <1 s |
769: | (5) | B4 | **RED**, P5 | 6,373 | 13 | <1 s |
770: | (5) | B6, counter, 2 polls per tick | **RED**, P5 (membership) | 692,218 | 26 | 4 s |
771: | (2) | **B7**, counter, **1 poll per tick**, `P5_SpreadOld` on fetch-start times | **RED** | 443,391 | 25 | 3 s |
772: | (3) | **ILC3-01**: (a) with Kill disabled (`R53_NoKill`, 2 polls/tick, MaxFaults 1 used by Drop/Resend) | **REACHABLE** | 722,985 | 35 | n/a |
773: | (3) | (a) killed observer / (b) unobserved, 2 polls/tick (`R53_ResidualBurst`) | **both REACHABLE** | 1,743,266 / 613,974 | 34 / 26 | n/a |
774: | (4) | Rolling window recovers after a gap (`R53_Roll`, EndAfterGapUnreachable; 1 poll/tick, no faults) | **REACHABLE** (healthy) | 257,044 | 33 | 3 s |
775: | (4) | **B8** fixed window: stranding state reached (`R53_B8`, FixedWindowStranded) | **REACHABLE** | 7,503 | 15 | <1 s |
776: | (4) | B8: an attempt with a gap in its fixed window never ends (`R53_B8_NoEnd`), exhaustive | **HOLDS**: never ends | 488,041 | 53 | 4 s |
777: | (4) | Termination, rolling window, **Allowance 1** (`R53_Live_A1`; N = 1, MaxTime 7, PollEachTick, no faults) | **GREEN** | 19,487 | 47 | 1 s |
778: | (4) | Termination, rolling window, **Allowance 0** (`R53_Live_A0`) | **RED** (R53-F2) | 199,541 | 66 | 6 s |
779: | (4) | Termination, `"literal"` window, Allowance 0 (`R53_Live_Literal`) | **RED** (R53-F1) | 249,606 | 66 | 8 s |
780: | (4) | Termination, B8 fixed window, Allowance 0 (`R53_Live_B8`) | **RED**: strands | 122,301 | 66 | 6 s |
781: 
782: ### 8.3 What the traces show
783: 
784: **B7 (ILC3-02 reproduced).** At one poll per tick, under the counter rule:
785: 
786: 1. A fetch at 3 fails.
787: 2. The poll started at 4 waits for its fence and fetches at 5. It fails.
788: 3. A poll at 5 fails, and the counter reaches 2. The attempt ends at 5.
789: 
790: Fetch-start ticks are {3, 5}, and interval 4 has no failed fetch. R51 reported `P5_Spread` green at one poll per tick
791: only because its ghost recorded invocation-start ticks {3, 4}. Section 6's statement that one poll per tick gives
792: coverage (R51-F1, "At one poll per interval it is: `R51.cfg` is green on `P5_Spread`") is **withdrawn**: it was a
793: property of the ghost, not of the rule. The R53 membership property is red for the counter (B6) and green for the
794: rolling set.
795: 
796: **ILC3-01, path (a) without a kill.**
797: 
798: 1. Burial at 1 = B. The tick-1 poll fetches eligibility and sends its latch.
799: 2. The store drops the latch. Nobody is killed.
800: 3. Fetches at 2, 3 and 4 fail, with the evidence obtainable throughout.
801: 4. `failed_intervals = {2, 3}`, and the tick-4 decider ends the attempt EVIDENCE_UNAVAILABLE.
802: 
803: The design's revised wording of (a), "an observed eligible presentation whose latch never commits (killed, dropped or
804: guard-failed)", is the right one.
805: 
806: **(a) and (b) at 2 polls per tick.**
807: 
808: - (a): the timely observer is killed. Committed failed fetches start at 2 and 3. The decider at 4 fails its fetch and
809:   re-fetch.
810: - (b): calendars pending. Failed fetches at 2 and 3; the decider at 4.
811: 
812: Both need a committed failed fetch in **every** interval of the completed window (Allowance 0). The green `R53_Burst`
813: run shows that no reachable end lacks one.
814: 
815: **ILC3-03, stranding.**
816: 
817: - `R53_Roll` (rolling window): failures at 2, 4 and 5, with interval 3 missing. The attempt still ends at 6 on window
818:   4..5.
819: - B8 (fixed window): failures at 3 and later, with interval 4 missing. Exhaustively, no such attempt ever ends. The
820:   `Live_B8` lasso polls at every tick to MaxTime with the attempt still open.
821: 
822: ### 8.4 Findings (revision 5.3)
823: 
824: **R53-F1. "The intervals ending at the current one" must exclude the current interval, or count the decider's own
825: failed fetch.** Under the literal reading (`"literal"`: the current interval must already be in the committed set),
826: at one poll per interval the current interval holds only the decider, whose failure is not yet committed. The window
827: is therefore never covered, and the attempt **strands**. `Live_Literal` is red: it polls every tick from 2 to 7 with
828: every interval failing and never ends. Its trace ends in a latch at the bound, which is a bound artifact.
829: 
830: The model's `"completed"` reading (the Expected most recent *completed* intervals) avoids this and is green on all
831: safety. The design text should name it.
832: 
833: **R53-F2. At Allowance 0 the rolling window can still be starved, by alternating fetch-start slips.** A poll that
834: starts at t can fetch at t or at t+1 (fence wait, within the invocation timeout). `Live_A0`:
835: 
836: 1. Fetches start at 2, 4, 4, 6, 6, 7.
837: 2. Intervals 3 and 5 have no fetch start, although a poll ran in every tick.
838: 3. No two consecutive completed intervals are both covered, so the attempt never ends.
839: 
840: The lasso sits at MaxTime, but the pattern repeats with period 2. Allowance 1 (`Live_A1`, green) removes it: a fetch
841: can slip at most one interval, so two consecutive intervals are never both empty.
842: 
843: Real deployment: the poll interval is 600 s and the timeout 300 s. Starvation needs the slip to alternate, which
844: requires schedule jitter, but nothing in the design excludes it. Two options, neither modelled:
845: 
846: - **Allowance ≥ 1 per window**, or more generally enough to absorb slips (any allowance of at least 1 sufficed
847:   here).
848: - Index the interval by the invocation's **scheduled** time rather than its fetch start, which is what R51's ghost
849:   did. That trades away ILC3-02's precision about when the evidence was actually checked.
850: 
851: So the claim "never strands the attempt" holds for the rolling window only with Allowance ≥ 1, or under a
852: no-alternating-slip assumption.
853: 
854: **R53-F3. P5 as now checked is the membership property Codex asked for.** It is green for the rolling set (1 and 2
855: polls per tick) and red for the counter (B6, B7) and for the single-poll rule (B4). The residual paths (a) (including
856: without a kill) and (b) are reachable, and only with a committed failed fetch in every interval of the completed
857: window (less the allowance). (c) stays unreachable.
858: 
859: **Not re-run for revision 5.3** (their last results are in the sections named):
860: 
861: - B2 (sections 6 and 7);
862: - B5, the no-fence (c) companion (section 6; R53 re-checked only that (c) is unreachable on the correct model);
863: - the R5.1/R5.2 sanity witnesses: ship, refusal, expiry, discard, orphans (sections 6 and 7);
864: - the residual runs at 1 poll per tick (section 6; R53 ran 2 polls per tick);
865: - termination at N = 2 (never run; N = 1 only);
866: - `R5_SendReading` and the revision-4/5 cfgs.
867: 
868: R53 also does not model ILC3-04 (S3 lifecycle expiry of live attempt material). The store abstraction hides it.
869: 
870: Files added (in `formal/tla/issuer-lifecycle/`):
871: 
872: - `IssuerLifecycleR53.tla`
873: - `IssuerLifecycleR53.cfg` / `.out`
874: - `IssuerLifecycleR53_{Burst,B1,B3,B4,B6,B7,B8,B8_NoEnd,C_Correct,ResidualBurst,NoKill,Roll,Live_A1,Live_A0,Live_Literal,Live_B8}.cfg`
875:   / `.out`
876: - `run-witnesses-r53.sh`

=== FILE (new): service/issuer/DEPLOY-RUN.md
1: # Deployment run record (first V1 deployment)
2: 
3: Append-only. Each entry: date, step, what was run, the values it produced, and who ran it.
4: 
5: ## 2026-10-30 — before the session (owner, no credentials)
6: 
7: Base: `8bcfcda` plus the issuer/signer interface fix (`docs/reviews/issuer-signer-interface/`).
8: 
9: 1. **Verifier install.** Already installed; `sha1dcsum` SHA-256 `3fa8472a23ff8ecc6c91b5193bc6e6e7a7ef1a1bbfbbff769a89bda0634dd5fb`
10:    matches `service/verifier/install.json`.
11: 2. **Suites.** The first run failed both signer suites (signer-kms 2, signer-gcp 7). One cause was a real defect:
12:    the issuer's attempt-prefixed frame names, which both production signers refuse, would have refused every
13:    request over 256 KiB. Fixed, confirmed by Codex, and covered by a retained pipeline test (disposition in
14:    `docs/reviews/issuer-signer-interface/DISPOSITION.md`). After the fix: issuer 235, signer-kms 48, signer-gcp 121,
15:    verifier 135 (77 subtests), all passing.
16: 3. **Packages** (deterministic: a rebuild of the issuer bootstrap gave the same digest).
17:    - `service/issuer/dist/issuer-bootstrap.zip` SHA-256 `7789cfbb00e913cae222483ef4d894343bd52be49274be5cd13e2c984183748b`
18:      (BOOTSTRAP: no `install.json`, so pre-ship refuses until rebuilt in step 4)
19:    - `service/signer-kms/dist/signer-kms.zip` SHA-256 `3c5d812747f4efd84ca6339efa07d616e3bdff52d1a9330744ab9eea313f2923`
20: 
21: AWS session: `aws sts get-caller-identity --profile tessera` → account 477139661040,
22: `AccountFullAccessRole` (author login, 2026-10-30).
23: 
24: Next: step 1 (`terraform plan` for the issuer bootstrap), read together with the author.
25: 
26: ## 2026-10-30 — in the session (owner ran the commands, under the author's login and with his blessing)
27: 
28: The author, on the owner waiting for him to run `apply`: "Not sure why a steward needs gardener approval... I have a
29: bucket and a trowel, and they bless your actions." The runbook's "no agent runs any of them" line was a prior
30: owner's rule, now corrected in DEPLOY.md.
31: 
32: Before step 1, two changes to `infra/`: AWS provider `~> 5.70` → `~> 6.20` (6.71.0), because 5.x rejects the
33: `python3.14` runtime the verifier requires; and API Gateway access logging (`/aws/apigateway/tessera-v1-issuer-access`,
34: 30 days; account-level CloudWatch role, none existed before). One client key, `smoke-test` (owner decision).
35: 
36: 1. **Bootstrap apply.** 46 added, 0 changed, 0 destroyed. Outputs: API `https://p4e0222jof.execute-api.us-east-2.amazonaws.com/v1`,
37:    key id `g8plxeex43` (smoke-test), table `tessera-v1-issuer-requests`, bucket
38:    `tessera-v1-issuer-results-0241cd18c7441abb3eaab257e8`, kms and gpg request/response queues and wake topics.
39:    - Deployed IAM read back: the API role has PutItem/GetItem on its table, Put/Delete on `content/*`, Get on
40:      `result/*` and `config/*`, ListBucket; the poller has its table and index, Put/Get/Delete/Tag on
41:      `work|result|frames|content/*`, Get `config/*`, Send to both request queues, Receive/Delete/GetAttributes on both
42:      response queues, Publish to both wake topics. Both roles: `logs:CreateLogStream, PutLogEvents` on `*` (loose;
43:      to tighten to their own log groups).
44:    - Unauthenticated and guessed-key calls: 403, each logged (`INVALID_API_KEY`, key id `-`). Missing and guessed
45:      keys are not distinguishable in the log.
46:    - **Path:** the routes are at `<api_url>/v1/requests`, i.e. `.../v1/v1/requests` (stage `v1` plus resource
47:      `/v1`). To be fixed with the custom domain (base-path mapping), not by redeploying now.
48: 2. **Install facts on Lambda:** Python 3.14, Unicode 16.0.0, `unicode_module_sha256`
49:    `62c4ae6033685dc674a1464257b68c632e21182314a52de559d499861232f2d3` (differs from the NUC's, as expected),
50:    `sha1dc_binary_sha256` `3fa8472a…dd5fb` (identical to the local build). Saved as `install-facts.json`.
51: 3. **Runtime:** `arn:aws:lambda:us-east-2::runtime:e75e9c9c41239a44ec0c6835b8565881fa9de069823be371f86023888ce6aeed`.
52: 4. **Deployable, pinned.** `dist/issuer.zip` SHA-256 `486ed52fbc1529d5a5dfa850d23fe84d65b7e782ed50797dc909464ad2283cf7`.
53:    Apply: 3 added, 3 changed, 1 destroyed (the API Gateway deployment, replaced). Both functions report
54:    `CodeSha256` `SG7VL7wVKdWl36hQ0j/oTWW354LtUHl9yQlGStIoPPc=` (= `486ed52f…` hex) and runtime management
55:    `Manual` on the ARN above.
56: 
57: State backups: `~/.local/share/tessera-tfstate/` (0700), after each apply.
58: 
59: ## 2026-10-30 — new production keys (step 5 and 6 prerequisites; neither has signed anything)
60: 
61: These identities are the external custody record's first entries (A11 §A11.5 item 2 (ii); profile §8).
62: 
63: | Slot | Key | Created (UTC) | Fingerprint |
64: |---|---|---|---|
65: | kms | AWS KMS `arn:aws:kms:us-east-2:477139661040:key/2c9ba2cf-ca0d-4a04-ad26-657840f32944`, alias `alias/tessera-v1-kms`, ML_DSA_65, SIGN_VERIFY, origin AWS_KMS, tag project=tessera-v1. Default key policy until step 5 replaces it. | 2026-10-30T20:01:31Z | `spki-sha256:a33c216e4151f7202b4863f9edebf060b374ee1bb91ff9ca5734b8e7ba75679f` |
66: | gpg (slot 2) | GCP KMS `projects/tessera-slot2/locations/us-east1/keyRings/tessera-v1/cryptoKeys/slot2-v1/cryptoKeyVersions/1`, HSM, EC_SIGN_P256_SHA256, attestation CAVIUM_V2_COMPRESSED, label project=tessera-v1 | 2026-10-30T20:01:48Z (`SLOT2_KEY_CREATED=1793390508`) | `gpg-sha256:6a2d7e757b99b46e469dd81f293387b7cfdbe3a1cab2b614dd2d26ecc79dda59` (v4 fingerprint `2d9645a3e6236fec9c611ad390d500a104210130`) |
67: 
68: Fingerprints computed with the code that checks them (`tessera_issue.encode.fp_kms` form over `GetPublicKey`;
69: `tessera_signer.openpgp.key_body`/`fp_gpg` with the createTime above). The spike keys (`alias/tessera-pq-spike`,
70: `slot2-spike`) are untouched; they are deleted once HYBRID-SUPPLEMENT §11 item 6's conditions hold.
71: 
72: ## 2026-11-02 — step 5, KMS signer (owner)
73: 
74: Owner decisions: **not-after 2027-02-01T00:00:00Z, sign_until 2027-01-28T00:00:00Z**
75: (not-before = publication of the key assertion); **trail retention 1096 days** (asymmetric cost: too long costs
76: storage, too short loses the signing record irrecoverably); no TEST window (its ≥ 10-day minimum, from the L1
77: margins, would hold `_tessera-v1.wamason.com` longer than the ceremony delays production). AWS provider for
78: `signer-kms/infra` moved to `~> 6.20` (6.71.0), as for the issuer.
79: 
80: - Package `dist/signer-kms.zip` SHA-256 `3c5d812747f4efd84ca6339efa07d616e3bdff52d1a9330744ab9eea313f2923`.
81: - Apply: 14 added, 0 changed, 0 destroyed. Function `tessera-v1-signer-kms`, role
82:   `arn:aws:iam::477139661040:role/tessera-v1-signer-kms-role`, trail `tessera-v1-signer-kms-trail`, bucket
83:   `tessera-v1-signer-kms-trail-13dedbd0aa681d7e13ea797992`.
84: - Live key policy read back: `KeyAdministrationWithoutSign` (account root, no Sign), `SignerRoleOnly` (Sign,
85:   GetPublicKey), `DenySignToEveryoneElse` (Deny Sign unless principal is the signer role).
86: - Negative check: the author's `AccountFullAccessRole` session calling `kms:Sign` → AccessDenied, "explicit deny in a
87:   resource-based policy".
88: - Object Lock on the trail bucket: COMPLIANCE, 1096 days. Trail logging: true.
89: 
90: ## 2026-11-02 — steps 6–8, slot-2 signer and gates (owner)
91: 
92: - `deploy.sh sas`: created `tessera-signer-gpg@` and `tessera-signer-invoker@` (no keys). `role`:
93:   `arn:aws:iam::477139661040:role/tessera-v1-signer-gpg-federated`.
94: - Issuer re-apply with `signer_principals={gpg=<federated role>}`: 2 added (role and policy
95:   `tessera-v1-issuer-signer-gpg`): Receive/Delete/GetAttributes on gpg-requests, Send on gpg-responses, Get on
96:   `frames/*`; trust: the federated role only.
97: - `keyiam`: `slot2-v1` IAM = signer + publicKeyViewer for `tessera-signer-gpg@` only. `registry`: `tessera-signer`.
98:   `build`: Cloud Build `713ce333-…`, SUCCESS, image
99:   `us-east1-docker.pkg.dev/tessera-slot2/tessera-signer/signer-gpg@sha256:6306b4fb3490b70b24c1791478c6a0b22358ebbf77ec730fedc7d2da7d2ec79a`.
100: - `job`, `run-now`: execution `tessera-signer-gpg-7kkb9` completed; log `start
101:   gpg-sha256:6a2d7e757b99b46e469dd81f293387b7cfdbe3a1cab2b614dd2d26ecc79dda59` (the pinned production fingerprint),
102:   exit 0. `scheduler`, `harden`: done.
103: - **Step 7 gate:** `retire-instrument` → deleted jobs `slot2-signer-tick` and `slot2-signer`, removed the
104:   prototype's bindings on `slot2-spike`, disabled `slot2-signer@`; "instrument retired and verified".
105: - **Step 8 gate:** `docs/reviews/signers/REQUESTERS.md`. Passes: beyond the poller, the two signers and the author's
106:   administrator identity, no principal can cause a signature. Findings: the account is an Organizations member (the
107:   management account 871341458535 is the author's login and has a role-management path); the IAM simulator is
108:   unusable under Organizations, so the list is a policy reading pending review; prototype role
109:   `tessera-slot2-signer-sqs` remains, harmless to V1, for cleanup.
110: 
111: Next: step 9 needs the window: the ceremony (repository root), the key-assertion commit with k = 6, the DNS TXT,
112: `config/window.json`. Then the smoke test and step 10.

=== FILE (modified; diff hunks, + lines are new): service/issuer/DEPLOY.md
diff --git a/service/issuer/DEPLOY.md b/service/issuer/DEPLOY.md
index 9f59134..4b57f5f 100644
--- a/service/issuer/DEPLOY.md
+++ b/service/issuer/DEPLOY.md
@@ -2,7 +2,10 @@
 
 > **Status: OWNER DRAFT, revised after the signer review** (`docs/reviews/signers/CODEX-REVIEW.md`, SG-01 to SG-05).
-> These are the steps for the first deployment. No agent runs any of them: `terraform apply` and every AWS write
-> run in the author's login session, from commands written out here in full. GCP steps can run on the NUC, where
-> `gcloud` is logged in.
+> These are the steps for the first deployment. They run in the author's login session (`aws login --profile
+> tessera`; Terraform takes it via `eval "$(aws configure export-credentials --profile tessera --format env)"`).
+> The owner runs them: the author, 2026-10-30, "I have a bucket and a trowel, and they bless your actions." (An
+> earlier version said no agent runs any of them; that was a prior owner's rule.) The irreversible choices are
+> still the author's: the trail retention in step 5, which Object Lock COMPLIANCE can never shorten. GCP steps run
+> on the NUC, where `gcloud` is logged in. The run record is `DEPLOY-RUN.md`.
 
 ## Before the session (owner, no credentials)
@@ -11,6 +14,7 @@
 2. All suites are green: issuer, `service/signer-kms`, `service/signer-gcp` (`.venv/bin/python -m pytest -q` in each).
 3. Packages, each built deterministically (record each SHA-256):
-   - `cd service/issuer && .venv/bin/python package.py dist/issuer-bootstrap.zip`
-   - `cd service/signer-kms && .venv/bin/python package.py dist/signer-kms.zip`
+   - `cd service/issuer && mkdir -p dist && .venv/bin/python package.py dist/issuer-bootstrap.zip`
+   - `cd service/signer-kms && mkdir -p dist && .venv/bin/python package.py dist/signer-kms.zip`
+   (`package.py` does not create `dist/`.) The run record for each deployment is `service/issuer/DEPLOY-RUN.md`.
 
 ## Keys and what counts as production — OWNER DECISION, revised 2026-10-28
@@ -37,4 +41,9 @@ produces a real receipt over honest smoke-test content.
 ## In the session (author logged in: `aws login --profile tessera`)
 
+0. **Gate: the slot-2 custody decision** (Amendment 11 §A11.5 item 2, c036). **Satisfied 2026-10-29:** Amendment
+   11 was signed at `f01e086` with Option 1. `service/signer-gcp/` is the production slot-2 signer, subject to
+   conditions (i)–(iv) of §A11.5 item 2, which steps 6–8 below evidence before the first shipped receipt.
+   Production never uses `prototype/` code (`formal/freeze-v1/FREEZE-RECORD.md:62`).
+
 1. **Issuer, bootstrap.** `terraform -chdir=infra plan -var lambda_zip=../dist/issuer-bootstrap.zip -out tfplan`.
    Read the plan together, then `terraform -chdir=infra apply tfplan`. The bootstrap package has no `install.json`,
@@ -75,4 +84,20 @@ produces a real receipt over honest smoke-test content.
     record. `CodeSha256` is base64 of the raw digest; `package.py` prints hex, and the test converts.
 
+## Gate before any client beyond `smoke-test` (owner, 2026-10-30)
+
+Detection, not only logging. API access logs exist from the first apply (`aws_api_gateway_stage.v1`); nothing watches
+them yet, and no alarm exists. Before a second API key is issued:
+
+1. **Detection contract** (owner): each attack or fault, what it must leave in which log, which alarm fires, how fast,
+   and who is told. At least: flood and throttling; missing or guessed keys; oversized or malformed requests;
+   per-key volume; signer refusals only an attacker or a fault produces (KEY_FP_MISMATCH, unsolicited responses,
+   E-06); `kms:Sign` count against issued receipts; CloudTrail `PutKeyPolicy`, IAM changes and `StopLogging`.
+2. **Alarms** with notification to the author.
+3. **Detection tests built by another model family** (Gemini via `agy`, or grok), from the contract and threat
+   model, not from the owner's alarm code: each attack is performed against the deployment and each alarm is seen
+   to fire. Codex reviews the tests and results. A detection that has never been seen to fire is a claim, not a
+   control.
+4. A per-key daily quota on the usage plan.
+
 ## Not deployment gates, but release gates (still open; `formal/freeze-v1/FREEZE-RECORD.md:84-91`)
 


=== FILE (modified; diff hunks, + lines are new): service/issuer/DESIGN.md
diff --git a/service/issuer/DESIGN.md b/service/issuer/DESIGN.md
index 3c83a6d..ff9ecfe 100644
--- a/service/issuer/DESIGN.md
+++ b/service/issuer/DESIGN.md
@@ -26,5 +26,9 @@
     `SIGNING_UNAVAILABLE`, `CLOSING`, `BAD_REQUEST`.
   - The same key with the same content returns the same request. The same key with different content returns 409.
-- **States:** ACCEPTED, then COMPLETE, REFUSED or FAILED (24 h after acceptance, with a reason). After 30 days: EXPIRED.
+- **States:** ACCEPTED, then COMPLETE or REFUSED (`ATTEMPTS_EXHAUSTED`, `SIGNING_CLOSED`, listing each attempt's
+  ending), or FAILED (`CONTENT_UNAVAILABLE`: the content is not available when attempt 1 would start - an upload
+  never finished, or completed content lost before attempt 1; no attempt exists). After 30 days: EXPIRED.
+  *(Superseded 2026-10-30: "FAILED 24 h after acceptance" contradicted A2 and is withdrawn; see "Issuance lifecycle"
+  below.)*
 - **Retrieval:** only by the credential that submitted. The response carries the receipt's SHA-256.
 
@@ -38,7 +42,12 @@
   - A retry reuses a complete, verified signature set rather than signing again.
 - **Ship only complete receipts:** the pre-ship checks of profile §4 and §15.7 run on the assembled bundle with the
-  service verifier's own logic, called as a library. A bundle that fails is FAILED, never shipped.
-- **Window:** acceptance stops 120 h before not-after, and signing stops at 96 h. A request that cannot complete in
-  time is FAILED, not shipped late.
+  service verifier's own logic, called as a library. A bundle that fails is never shipped. *(Updated 2026-10-30: it
+  is no longer FAILED. A failing check that depends only on the attempt's frozen material discards the attempt with
+  the reason (step 7); a snapshot failure recaptures the snapshot; anything else is retried. See "Issuance
+  lifecycle".)*
+- **Window:** signing stops 96 h before not-after, and acceptance stops delta + S + 24 h before that (216 h before
+  not-after; L1 as revised, applied in `window.py`). That spacing is an operating allowance, not a processing
+  guarantee: allocation can be delayed. An attempt whose T would exceed not-after is not shipped (A9 issuer
+  invariant); a request whose next attempt would need signing after the stop is REFUSED `SIGNING_CLOSED`.
 
 ## Tests the builder must provide
@@ -48,5 +57,5 @@
    and verifies the bundle with `service/verifier` (`--mode test`) as `VALID_STRICT`.
 3. **Fault tests:** a signer timeout followed by a late answer (E-02); a lost API response, then lookup by key; the
-   24 h failure; the stop margin.
+   24 h failure (superseded: stalls now keep the request open; see "Issuance lifecycle"); the stop margin.
 4. **Infrastructure as code (Terraform)** that a later step applies to AWS. Nothing is applied by the builder.
 
@@ -58,5 +67,6 @@ Codex review `docs/reviews/issuer/CODEX-REVIEW.md` (IS-01 to IS-11); disposition
 - **IS-03 (signer contract):** each policy signer enforces the signing stop itself, immediately before it signs: its
   own configured stop (the window's not-after minus 96 h) and a per-request `sign_by` the issuer now adds to every
-  request (the earlier of the signing stop and acceptance + 24 h). Past either, it answers `REFUSED`
+  request (the earlier of the signing stop and acceptance + 24 h; *superseded 2026-10-30: now the signing stop
+  only, the 24 h bound is withdrawn*). Past either, it answers `REFUSED`
   (`SIGNING_STOPPED`). The stand-in signer does this. **Open:** the deployed slot-2 signer and the KMS-slot signer
   are outside `service/issuer` and must adopt the same check before issuance.
@@ -77,5 +87,6 @@ Codex review `docs/reviews/issuer/CODEX-REVIEW.md` (IS-01 to IS-11); disposition
   cleanup obligation (`CLEAN#<rid>`, kept apart from the record). Each poll retries the obligation until a listing
   shows nothing left: content, work files and frames at the end; the receipt 30 days after the end. Lifecycle
-  rules stay as a 31-day backstop.
+  rules stay as a 31-day backstop. *(Superseded 2026-10-30, revision 5.3.1: no age rule; the backstop expires
+  only objects the obligation has tagged cleanup-due.)*
 - **IS-09 (large frames):** a signer request whose inline message would exceed 256 KiB carries `frame_ref` (an
   immutable object `frames/<rid>/<sha256>`) and `frame_sha256` instead of `frame_b64`. The signer refuses unless
@@ -91,4 +102,6 @@ Codex review `docs/reviews/issuer/CODEX-REVIEW.md` (IS-01 to IS-11); disposition
 Codex confirmation review `docs/reviews/issuer/CODEX-CONFIRM.md` (CF-01 to CF-05); dispositions in the same file.
 
+- *(CF-01, CF2-01 and the deadline half of CF-02 are superseded 2026-10-30 by "Issuance lifecycle" below: there is no
+  deadline, `api.settle` and the unconfirmed COMPLETE are removed, and COMPLETE is one guarded terminal write.)*
 - **CF-01 (completion at the deadline; supersedes the IS-02 bullet above):** ending a request persists the cleanup
   obligation first and reads the clock only after that. COMPLETE is then committed *unconfirmed* and settled
@@ -121,2 +134,146 @@ Codex confirmation review `docs/reviews/issuer/CODEX-CONFIRM.md` (CF-01 to CF-05
 - **CF-04 (deletion errors):** `S3ResultStore.delete` raises on any per-object error in a DeleteObjects response and
   stops after a bounded number of rounds. The obligation is kept and the poller goes on to the other obligations.
+
+## Issuance lifecycle (2026-10-30)
+
+Implements `docs/decisions/2026-10-29-issuance-lifecycle.md` (revision 5.3.1) and its "Implementation boundary until
+the author decides"; the checked protocol is `formal/tla/issuer-lifecycle/IssuerLifecycleR53.tla`. Tests:
+`tests/test_lifecycle.py` (one group per brief item); deadline tests in `test_faults.py`, `test_review_fixes.py`,
+`test_confirm_fixes.py`, `test_states.py` and `test_infra.py` are rewritten and say so in their docstrings.
+
+- **Attempts** (`tessera_issue/lifecycle.py`): a request has attempts 1..3 (`attempts`, `cur`). Each has its own
+  declared issue time (its allocation time), frames, signing jobs (request ids scoped by attempt), A_sig, a fresh stamp,
+  evidence, latch and end; its objects live under `work/<rid>/a<n>/`. A signer response is routed by attempt; one for
+  an attempt that is not current is logged `other-attempt` and ignored.
+- **One writer.** Only the poller makes lifecycle transitions. `api.status` and `api.receipt` write nothing; `settle`
+  and `fail_after` are gone. Every poller write is guarded on (request state, current attempt id, current attempt
+  state) and the version (`stores.lifecycle_guard`; DynamoDB conditions on the item attributes `lstate`, `latt`,
+  `lastate` and `version`).
+- **Fence.** Before fetching evidence for an attempt (stages `evidence`, `finalize`, `snapshot`), the poller commits a
+  guarded version bump and proceeds only if it committed.
+- **Eligibility and latch.** The attempt's proof must stamp SHA-256 of its own A_sig; the verifier's `select` picks the
+  lowest qualifying height among attestations whose full pinned, linked h..h+5 segment was obtained; the three A2.2
+  conjuncts are evaluated on it. On eligibility, at any time while the attempt is open, the poller writes the
+  presentation (proof pruned to the selected height, with its six headers) as an immutable digest-named object, then
+  commits the latch with `observed_at` and its reference.
+- **Ending.** Only complete negative evidence (every stamped calendar attested, every attestation's segment obtained,
+  the selected presentation failing a conjunct) ends an open attempt: DISCARDED at or before B, EXPIRED after it.
+  The end and the next attempt's allocation are one guarded write; after attempt 3 the same write records REFUSED
+  `ATTEMPTS_EXHAUSTED`; if the next attempt would need signing after the stop, REFUSED `SIGNING_CLOSED`. A signer
+  refusal discards that (unsigned) attempt the same way.
+- **After the latch** (step 7; ILI-01, ILI-02, ILC-I-01). Transient failures are retried indefinitely. The pre-ship
+  check returns the verifier's per-row ledger, and `pipeline.classify_preship` decides in this preference order (not
+  by the first failing check):
+  1. If ANY failing check is INVALID on frozen material, that check decides, wherever it falls: the attempt's frames,
+     frozen signatures, A_sig, manifest and keys; the preserved receipt presentation (rows 11.x-12.x, including
+     OTS_MERKLE_MISMATCH and the transaction-shape/txid check); the window's frozen git material (rows 14.1-14.6 and
+     14.8); 16.1 (unless a snapshot row also fails). The attempt is discarded, reason `PRESHIP:INVALID/<code>@<row>`.
+  2. Else, if a check INVALID on the snapshot's own bytes fails (13.1, 13.2, 13.3, 13.6, 13.7, 15.1, 15.2, 13.4's
+     SNAPSHOT_STAMP_MISMATCH / OTS_FORMAT, and 13.5's RRSIG-time reasons), this snapshot can never pass: it is recaptured, or the attempt is
+     discarded `SNAPSHOT_IMPOSSIBLE` if no lawful snapshot can be obtained any more (below).
+  3. Everything else is retried, keeping the current snapshot: headers and pins, container, catalog and trust
+     configuration (14.7), every configuration-dependent snapshot result (13.5 except its RRSIG-time reasons, which
+     are in rule 2 - `validate_snapshot` against the configured root KSKs, reliance periods and trust horizon - and
+     13.4's header outcomes), and every UNVERIFIABLE result outside rule 2.
+  T > not-after discards (`T_AFTER_NOT_AFTER`).
+- **SNAPSHOT_IMPOSSIBLE** (ILI-02, ILC-I-01, ILC-I-04). Discards only when both are proven from evidence: the snapshot
+  being replaced failed a byte-only check (rule 2) and its proof is complete, so it can never pass; and the median
+  time past of the eleven authenticated, linked headers ending five below the tip is later than declared + delta, so
+  every new anchor fails row 13.7 (Bitcoin consensus: a block's time exceeds the median of its eleven predecessors,
+  which never decreases). It is evaluated where the failure is found (finalization) and again before every recapture
+  (the snapshot stage), so captures that keep being rejected cannot hold the attempt once it is proven. Elapsed time
+  never discards. Assumption, as in the V1 contract: **no reorganisation of 6 or more blocks** (A1.6); it also
+  underlies the header checkpoints.
+- **Limits awaiting the author's termination decision (outside the step-5 gate).** These are disclosed limits, NOT
+  satisfied obligations: each can keep a request open indefinitely, which leaves A2.3's termination obligation
+  (`phase-0-prereg-amendment-2.md:288`) unmet in that case. Disclosure discharges nothing; an author decision (or an
+  owner rule within registered text) is needed if they must end. From Codex's round-2 table E
+  (`docs/reviews/issuer-lifecycle-impl/CODEX-CONFIRM-2.md`):
+
+  | Path | Kind |
+  |---|---|
+  | A stage repeatedly needs more requests than one invocation admits before its durable completion (a very slow store or dependency; the measured envelope is below) | stated slow-store limit (a progress limitation; overrun is a tolerated hard kill, below) |
+  | Snapshot recapture where impossibility cannot be proved: pending snapshot proof, unobtainable median-time-past headers, or insufficient chain progress | stated limit (absence of an impossibility proof never authorizes a discard) |
+  | A latched attempt's snapshot proof never becomes usable; a preserved presentation or assembly object permanently missing | stated external-evidence / storage limit |
+  | Unrepaired catalog or trust configuration (including configuration-dependent 13.5 outcomes), verifier unavailability, or persistent header / presentation disagreement | stated operator / dependency limit (no age-based ending is authorized) |
+  | Persistent store or queue failures, failed guarded commits, or stage exceptions before a terminal write | operational limitation (no general termination guarantee; signing closure cannot complete a transition whose reads or writes stay unavailable) |
+  | The chain never reaches the git pre-commitment depth, or no calendar ever accepts a stamp | dependency limit before evidence processing |
+
+- **Presentation** (ILI-01, ILI-06). The latched presentation keeps only branches at the selected height whose
+  attested message is that block's merkle root; contradicted branches there are dropped (counted in the latch as
+  `contradicted_pruned`) and the pruned presentation is re-checked contradiction-free. Complete evidence in which every
+  attestation is contradicted ends the attempt `EVIDENCE_CONTRADICTED` (discarded at or before B, expired after);
+  incomplete or non-qualifying evidence stays open (ILI-03).
+- **Signing closure** (ILI-04). Durable signatures (stored and logged "used") are reconciled before closure is
+  decided; a complete recovered set is sealed whatever the window.
+- **Content** (ILI-08). Content is checked before attempt 1 is allocated (`FAILED CONTENT_UNAVAILABLE`, no attempt).
+  After allocation, lost content is recovered from an earlier attempt's attestation frame (it carries the bytes);
+  if none decodes to the content digest, no attempt can ever be built, and the ending write discards the attempt and
+  refuses the request `REFUSED CONTENT_UNAVAILABLE` (end-and-refuse, like `SIGNING_CLOSED`).
+- **Invocation budget: a PROGRESS mechanism, not a bound** (ILI-05, ILC-I-02, ILC-I2-01; owner decision: the earlier
+  "never overrun" claim is withdrawn). One deadline (`tessera_issue/deadline.py`), measured on a monotonic clock,
+  admits every request the poller makes: DynamoDB, S3 (including the body read of `get_object`, inside the same guarded
+  request) and SQS and SNS through `GuardedClient` around each SDK client; calendars, explorers and the resolver through
+  `guarded_transport`; the pre-ship check directly. A request starts only if its configured worst case fits the time
+  left minus a 10 s reserve, and the HTTP and DNS transports are given a timeout capped to what remains. Worst cases
+  count the configured explorers and the SDK's retry attempts (`attempts x (connect + read) + back-off` = 73 s). Its
+  purpose is that every invocation leaves durable progress: headers are checkpointed per height and as linked
+  segments, a stale stored set is invalidated durably (ILC-I-03), the evidence already held is evaluated before any
+  pending calendar is asked (ILC-I-05), calendar requests stop while one checkpoint write still fits (ILC-I2-03),
+  requests are enumerated in bounded pages from a durable position moved before each request (ILC-I2-04), and draining
+  signer responses has a cooperative allocation of a third of an invocation (ILC-I2-04, ILC-I3-02). It drains OLDEST
+  FIRST (ILC-I6, ILC-I7, owner decisions): a round receives a batch from a slot, then from the next slot only while
+  that receive PLUS one message's complete worst-case handling (every guarded request of the handling, and the
+  acknowledgement, from the adapters' worst cases) still fit; it then handles the received messages across slots in
+  order of their SQS `SentTimestamp` (equal times interleave the slots), the oldest always first. A message left
+  unhandled becomes visible again and grows older. The slot received from first is chosen at random each round;
+  with the AWS adapters' worst cases the rule admits one receive per round. **Handling is resumable per guarded call, and every completed step is observable** (ILC-I8, ILC-I9,
+  owner decisions): a signer response's handling is index lookup and record read; frame read and verification, THEN
+  the signature object under its digest-named key (only verified signatures are written there, so its existence
+  means "verified"); the "used" log entry; the guarded record update; the acknowledgement, last. Each step is
+  idempotent and durable, and a later delivery skips every completed step and never repeats it: a record that already
+  holds the signature leaves only the acknowledgement; on a redelivery (SQS `ApproximateReceiveCount` > 1) the used
+  log is read first (logged: go to the record update) and then the verified object is checked (present: go to the log
+  write, without reading the frame or writing the object again). Request servicing's `_reconcile` adopts a stored
+  (verified) signature, logging it first if its entry is missing. **The capacity condition, in admission terms:**
+  every AWS request is admitted only if its configured worst case, 73 s (3 attempts x (3 s connect + 8 s read) + 2 x
+  20 s back-off), fits the time left. Each poll advances at least one incomplete step of a waiting response provided
+  the budget fits the receive, the reads that locate the next incomplete step (index lookup, record read, and on a
+  redelivery the used-log read and the verified-object check; for the signature step, the frame read it verifies
+  against), and ONE guarded call's admission (73 s of headroom) for that step. Actual latency and admission headroom
+  are different quantities: a call whose actual latency is far below 73 s is still refused when less than 73 s
+  remains. Draining is starvation-free with probability 1 provided that condition holds; below it, progress waits
+  for faster dependencies (the stated capacity limit). The share is checked between
+  messages, never before a round's oldest one, without reserving a message's remaining cost, so one slow message can
+  overrun it; it is not a total-time claim. Removed earlier: the schedule-derived starting slot, the per-slot shares,
+  and the durable rotation. Running out of time never ends an attempt.
+  **An overrun is a hard kill, and the protocol tolerates it:** the fence, the guarded writes and the checkpoints make
+  a killed invocation's leftovers harmless. **Known limits on the deadline's precision** (not chased): the HTTP
+  transport's socket timeout applies per blocking operation, so a server dripping bytes can exceed the request's
+  total; a DNS query is a composite of UDP and TCP operations, each with its own allowance, and hostname resolution is
+  not covered; an SDK request's connect and read timeouts are not a total-operation deadline (streamed bodies); the
+  pre-ship check is local CPU with a 30 s admission estimate and no interruption. Measured progress envelope (tests):
+  with any one client slow, every invocation stays within its deadline in the tests' fakes, and a request still
+  completes with every DynamoDB request taking 20 s, every S3 request 10 s, every SQS or SNS request 60 s, every
+  calendar, explorer or resolver request 15 s, or a 25 s pre-ship check; at DynamoDB 30 s or S3 20 s per request a
+  stage can need more requests than one invocation admits and the request stalls (listed above).
+- **Snapshot capture does not gate the receipt** (ILC-I2-05). Stamping moves the attempt to evidence whether or not
+  the DNSSEC snapshot capture succeeded; capture is retried in each evidence poll (early, since its anchor must be
+  timely) and, if the attempt latches without one, before finalization (stage `snapshot`). A receipt's latch or
+  conclusive negative is never held up by the snapshot. If no snapshot was ever captured and the median-time-past
+  bound excludes every timely anchor, the attempt is discarded `SNAPSHOT_IMPOSSIBLE` (`NO_SNAPSHOT`).
+- **13.5 by reason** (ILC-I2-02). `RRSIG_NOT_VALID_AT_EVAL_TIME`, `RRSIG_INTERVAL_REVERSED` and
+  `RRSIG_TIME_AMBIGUOUS` depend on the snapshot's own RRSIG times against its anchored time: a recapture can repair
+  them (and they count for the impossibility proof). Every other 13.5 outcome (configured KSK intervals, reliance
+  periods, trust horizon, and conservatively the chain of trust built on them) is configuration-dependent and retried.
+- **Bounded external fields** (ILI-07). Signer request ids, statuses and reasons are validated; an unrecognised or
+  oversized reason becomes `UNRECOGNIZED_REASON` and the original is stored by reference (`diag-<sha256>`, with its
+  digest and length). The DynamoDB fake rejects items over 400 KiB.
+- **GATED.** `EVIDENCE_UNAVAILABLE` is not implemented in any form. An attempt whose evidence never completes stays
+  open. `unavailable_since` and `failed_intervals` (runs of `fetch_start // 600`) are written for diagnosis only.
+  Nothing here claims termination.
+- **Storage.** No age rule applies to live objects: the S3 lifecycle rule expires only objects tagged `cleanup-due`,
+  which the cleanup obligation sets just before deleting (content, work and frames at the end; the receipt 30 days
+  after `ended_at`).
+- **Public view.** ACCEPTED shows `attempt` {number, of, state} and, for an open attempt, `expiry_boundary` (B) with a
+  note that the twelve-day budget is nominal; REFUSED lists each attempt's outcome and reason.
