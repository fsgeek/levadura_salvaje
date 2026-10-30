> **REGISTERED 2026-10-16 by the owner instance under A9.6** (A9 signed by the author at `2ad3489`). This is the
> dated branch-registration supplement; it is byte-identical in body to `HYBRID-SUPPLEMENT-DRAFT.md` as committed in
> `2ad3489` (SHA-256 4e8e6753…8549f), with this header added. Items labelled OWNER-PROPOSED below are registered
> owner decisions from this date. Record: `HYBRID-REGISTRATION-RECORD.md`.

# Hybrid-branch registration supplement for `tessera-v1-strict` (DRAFT)

> **STATUS: DRAFT, 2026-10-14. Owner instance (Claude Opus 5.5). Not registered.** This is the branch-registration
> supplement that Amendment 9 §A9.6 ("Branch registration") authorizes. It takes effect only if the hybrid pass
> condition is met by 21 Oct, and only once the owner dates it and names the exact ENCODING-V1 and specification
> hashes at the signing commit (§9). Until then the pair id below is **absent from the codec registry**
> (V1-PROFILE §1, "Branch-not-taken id before registration"). **Every choice in this file is OWNER-PROPOSED.** None
> is an author decision, and nothing here changes a registered sentence. Owner decisions of 2026-10-14
> (`docs/reviews/hybrid-supplement/DECISIONS.md`) are recorded where they settle a proposal.
>
> **Revised 2026-10-14** after the Codex non-author review (`docs/reviews/hybrid-supplement/CODEX-REVIEW.md`):
> - HS-01: the genuine V1-frame capture (owner run of `spike_v1_hybrid.py`) is archived and vectored (§8, §10.3);
> - HS-02: §10.4 is narrowed: the deployed-slot path is not yet evidenced;
> - HS-03: mode, context, μ-domain and hint-decoding vectors are added, with gate-disabled demonstrations;
> - HS-04: the A/B results are labelled candidate-codec evidence; the routing cases go to
>   `HYBRID-CONFORMANCE-CASES.md`;
> - HS-05: registration edits only E§5.2; the issuer always uses EXTERNAL_MU;
> - HS-06: RFC 9881 is cited, and §9's specification hashes are distinguished.

**What A9.6 bounds this supplement to, and how this file maps onto it.**

| A9.6 item | Here |
|---|---|
| the pair identifier with its mode and context | §1 |
| the ENCODING-V1 §5.2 edit for rule R | §2 (rule R), §7 (exact edit text) |
| the completed pass-condition evidence | §3 (kms key encoding and fingerprint), §4 (key-use assumptions), §5 (R-3.12), §6 (P3's model), §8 (vectors, agreement run, real signatures), §10 (status per pass-condition bullet) |

**Registration edits ENCODING-V1 §5.2 and nothing else in the baseline** (owner decision 5; HS-05). The
branch-specific kms key definition (§3) and the key-use assumption (K-R) (§4) are carried by this supplement. A9.6's
pass condition requires them to be specified ("slot key and fingerprint encodings, key-use assumptions appropriate
to each slot"), and A9.6 says the signing-commit baseline plus this supplement governs the hybrid branch. E§3.3,
PROOF (K) and every other baseline file are not edited under this authorization.
- Baseline statements that rule R has no id, no vectors, or no implementation (E§5.2's old bullets, E§8 "Out of P8's
  scope", PROOF §6) are **superseded for the hybrid branch** by this supplement and its evidence.
- They remain the baseline's text, unedited.

---

## 1. The pair algorithm identifier, its mode and its context — OWNER-PROPOSED

```
KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA256
```

- **Grammar.** It matches E§3.2's `^[A-Z0-9][A-Z0-9-]{0,63}$`: 47 characters, ASCII capitals, digits and `-`.
- **Reading, in slot order.** Slot `kms`: ML-DSA-65, pure. Slot `gpg`: the classical id's scheme, spelled exactly as
  the classical id (`OPENPGP4-ECDSA-P256-SHA256`), so rule O keeps one name in both branches. *Reason:* `common.alg`
  is one value shared by both frames (R-3.12, §5). It must therefore name the **pair**, in manifest slot order. A
  reader with no V1 software can read both schemes off a hex dump (C6).
- **Mode: pure ML-DSA.** FIPS 204 ML-DSA.Sign / ML-DSA.Verify (Algorithms 2 and 3), not HashML-DSA. Parameter set
  ML-DSA-65.
- **Context: the empty octet string.** So the FIPS 204 message representative is
  `M' = 0x00 ‖ 0x00 ‖ F` (domain byte 0 for pure mode, context length 0, no context bytes). `F` is the frame (§2).
  `PURE` in the id names the mode. The empty context is fixed by this registration, not spelled in the id; a
  non-empty context is a different scheme and needs a different id.
- **External μ is a signer-side computation only, and it is the issuer's only path** (owner decision 6). AWS KMS refuses
  `MessageType RAW` over 4096 bytes (observed 2026-10-13: "Member must have length less than or equal to 4096").
  For one code path whatever the size, the issuer always computes
  `μ = SHAKE256(SHAKE256(pk, 64) ‖ 0x00 ‖ 0x00 ‖ F, 64)` from the slot's own public key and the frame, and sends `μ`
  with `MessageType EXTERNAL_MU`, signing algorithm `ML_DSA_SHAKE_256`, for **attestations and possession proofs
  alike**. `pk` here is the raw 1952-byte key, not the SPKI. The output is an ordinary pure ML-DSA-65 signature over
  `F` (FIPS 204 Algorithms 2, 3, 7, 8; RFC 9881 Appendix D on external μ).
  - The verifier never sees `μ`, never receives a `MessageType`, and verifies over `F`. A signature checked over `μ`
    as if `μ` were the message fails (XM-05).
  - Evidence for the selected path:
    - SIG-G3 / R-G2 is the real KMS EXTERNAL_MU signature over a **genuine** 6753-byte V1 attest frame;
    - SIG-H3 is made from `μ` by implementation A and is byte-identical to A's deterministic signature over the
      frame itself;
    - B recomputes `μ` for both.
  - **RAW captures are comparative only:** SIG-G1 / R-G1 and P-G1 (genuine frames) and SIG-H5 (spike frame). They
    show that a verifier cannot tell the two KMS message types apart. They do not test the selected issuer path.
- **Signing randomness.** Hedged and deterministic FIPS 204 signing both give valid signatures. Nothing in V1
  depends on which KMS uses: the anchor commits the exact bytes (E§5.3), and a second valid signature over the
  same frame fails the anchor (negative control XHR-01).
- **Catalog.** Under the hybrid branch the V1 catalog's single `alg` is this id (V1-PROFILE §1). The classical id
  stays codec-known (rule O for both slots) and becomes policy-unsupported: `UNVERIFIABLE / ALG_UNKNOWN`.

## 2. Rule R for the pair: raw ML-DSA-65 signature bytes — OWNER-PROPOSED

- `S_kms` is the FIPS 204 `sigEncode` output and nothing else: no header, length prefix, wrapper, DER, armor or
  base64.
- **Length: exactly 3309 bytes.** That is `c̃` (λ/4 = 48 bytes) ‖ `z` (5 polynomials × 256 coefficients × 20 bits =
  3200 bytes) ‖ `h` (ω + k = 55 + 6 = 61 bytes). The cap for `(pair id, kms)` is also 3309.
- **Codes, in E§5's order:** length 0 → `SIG_EMPTY`; length above 3309 → `LENGTH_CAP`; any other length below 3309 →
  `SIG_FORMAT`. Rule R reads no byte of `S`, so within an anchor the slot's `u32` length is the signature's only
  boundary: a trailing byte (3310) is `LENGTH_CAP` and a truncation (3308) is `SIG_FORMAT`, never `TRAILING` or
  `TRUNCATED` (XH-01 to XH-04).
- **Internal malformation is a verification failure, not a codec failure (OWNER-PROPOSED).** Out-of-order or
  over-full hint indices, nonzero hint padding, and a `z` coefficient beyond the bound all make FIPS 204
  verification return false: `SIG_INVALID` for a receipt slot, `POSSESSION_INVALID` for a possession proof
  (XHR-04, XHR-05, XHR-12, XHR-16 to XHR-19; gate-off demonstrations in §8). *Reason:* this keeps PROOF Lemma 7a's accepted set for rule R exactly "the strings of
  the exact length", as the baseline proof already states it. Both codecs stay byte-blind for rule R, and the
  boundary argument needs no FIPS 204 parser.
- **The signed message is the frame `F` itself**, for the attestation slot, and `F_manifest` for the kms possession
  proof (R-3.38; V1-PROFILE §8: "Possession proofs use the same per-slot rule over `F_manifest` (rule R for kms
  under the hybrid)"). There is no trailer, so PROOF Lemma 9 has no rule-R counterpart to prove: the message *is*
  `F`.
- **Rule O in the `gpg` slot is unchanged** (E§5.2, cap 1024, V1-PROFILE §8's rule-O signature policy).
- **Malleability (E§3.5).** Under hedged signing one frame has many valid ML-DSA signatures. Exact-copy integrity is
  what the anchor gives, as for rule O; V1 normalizes nothing.

## 3. Slot `kms` key encoding and fingerprint under the pair id — OWNER-PROPOSED

**Key encoding: the exact DER SubjectPublicKeyInfo**, as AWS KMS `GetPublicKey` returns it, with the
AlgorithmIdentifier `id-ml-dsa-65` (OID **2.16.840.1.101.3.4.3.18**, NIST CSOR) and **parameters absent**. Source:
**RFC 9881 §2** (the OID, parameters absent) and **§4** (the SubjectPublicKeyInfo and its public-key encoding).
1974 bytes: 22 fixed bytes, then the 1952-byte FIPS 204
public key `ρ (32) ‖ t1 (6 × 320)`:

```
30 82 07 b2                          SEQUENCE, length 1970
   30 0b                             SEQUENCE (AlgorithmIdentifier), length 11
      06 09 60 86 48 01 65 03 04 03 12   OID 2.16.840.1.101.3.4.3.18 (id-ml-dsa-65); no parameters
   03 82 07 a1                       BIT STRING, length 1953
      00                             zero unused bits
      <1952 bytes>                   FIPS 204 pkEncode(ρ, t1)
prefix (hex): 308207b2300b0609608648016503040312038207a100
```

- Checked against the real key: the KMS spike key's `GetPublicKey` bytes have exactly this prefix and length, and
  `cryptography` 50.0.2 re-exports the parsed key to the same 1974 bytes (K-H2).
- **Fingerprint: unchanged scheme.** `key_fp = "spki-sha256:" + hex(SHA256(SPKI DER))`, as E§3.3 already defines for
  the kms slot. The manifest schema, the frame schema and the DNS record (`kms=<hex>`) are unchanged. The OID sits
  inside the hashed bytes, so a P-256 and an ML-DSA-65 key cannot share a fingerprint under (H).
  - Real spike key: `spki-sha256:d1b35a0e5273912ee85c7f88ee97929cef311e7854ad30c58faa3e0250c4a7a4` (K-H2).
  - Illustrative test key (public seed): `spki-sha256:576e49c28c431d6cf6679ff5a04a0a023ca7dd8d0da2a75881ff0b3dee6c5cb4`
    (K-H1).
- **`KEY_FORMAT`.** Under the pair id, `keys.kms` that is not exactly this encoding is `INVALID / KEY_FORMAT`, before
  `KEY_MISMATCH` (V1-PROFILE §8, row 5.1 then 5.2). The rule is selected by the installed spec and the slot, never by
  the key bytes. That includes a P-256 SPKI, ML-DSA-44 or ML-DSA-87 SPKIs, the right OID with the wrong length,
  NULL parameters, a nonzero unused-bits octet, non-minimal or indefinite DER lengths, a truncation, a trailing byte,
  the bare 1952-byte key and PEM text (XK-01 to XK-12).
  - A generic key loader is not a substitute: `cryptography` accepts the P-256, ML-DSA-44 and ML-DSA-87 SPKIs of
    XK-01 to XK-03 as valid keys of their own algorithms.
- **No further public-key validation exists for ML-DSA.** Every 1952-byte string is a well-formed FIPS 204 public key:
  ρ is arbitrary, and every 10-bit `t1` field is in range. So, unlike P-256's on-curve check, `KEY_FORMAT` for this
  slot is purely the encoding check.
- **Under the fallback** nothing changes: an ML-DSA-65 SPKI in `keys.kms` is `KEY_FORMAT` (V1-PROFILE §8, EA-24).

## 4. Key-use assumptions for the raw slot (what replaces PROOF (K) for `kms`) — OWNER-PROPOSED

PROOF (K) reads: *"Each V1 slot key signs only V1 tagged strings, as OpenPGP type-0x00 documents."* Under the hybrid
that sentence still describes the `gpg` slot and does not describe the `kms` slot. Under the pair id, (K) is
replaced by two assumptions:

- **(K-R), slot `kms`.** The ML-DSA-65 key signs only messages `F ∈ Frm(attest) ∪ Frm(manifest)` (V1 tagged strings),
  in pure mode with the empty context. Every issuer KMS `Sign` call on the key is `MessageType EXTERNAL_MU`, with
  `μ` computed by the issuer from such an `F` and this key's raw public key (§1; owner decision 6).
  - The spike's `MessageType RAW` calls (message exactly `F`) are comparative captures, not the issuer path.
  - They satisfy the same assumption, because the message is a V1 tagged string.

  The key is used with no other context, never in HashML-DSA mode, and by no other protocol or service.
- **(K-O), slot `gpg`.** Unchanged: V1 tagged strings, as OpenPGP type-0x00 documents, through the policy signer
  (A9.6, slot-2 custody).

*Why the type-0x00 clause has no rule-R counterpart.* In rule O the signed hash input is `F ‖ trailer`, and type 0x00
is what excludes text mode's line-ending rewrite (E§3.5). Rule R signs `F` itself, with no transformation, so there
is nothing to exclude. Domain separation comes from the bytes:
- every V1 tagged string begins with a tag-length byte in 0x11–0x1d (Lemma 4, Remark 10);
- pure mode's `M'` begins `0x00`, where HashML-DSA's begins `0x01` (FIPS 204's own separation, should the key ever
  be misused in that mode).

PROOF uses (K) only in Remark 10, and Remark 10's argument holds unchanged with message = `F`.

*What enforces (K-R), stated so it is not overread.*
- The HSM cannot check that a message is a V1 frame. Under EXTERNAL_MU it does not even see the message: whoever
  may call `kms:Sign` on the key can sign any message by computing `μ`.
- So (K-R) is an issuer-code and IAM assumption: the key policy grants `kms:Sign` only to the issuer role, and the
  issuer code builds only V1 frames. It is not an HSM property. The operations runbook carries the key policy.
- This is the same single-controller position C3 already states. Capture of the issuing account confers signing
  capability for both slots.

## 5. R-3.12 for the mixed pair

R-3.12: *"the six non-fingerprint fields of every required signer's frame — object type, algorithm, identity,
manifest hash, canonicalization version, payload — are equal across signer slots; only the key-fingerprint field
differs."* What it requires of the mixed pair, and why it holds:

1. **One algorithm value in both frames.** `common.alg` is the pair id in both frames, and the manifest's `alg` is the
   same id (E§4; `RECEIPT_MANIFEST_MISMATCH` otherwise). The slots' *schemes* differ, but the *field* is equal: the
   verifier takes each slot's scheme from `(common.alg, slot)` (E§5.2), never from the frame, the key or the
   signature bytes.
2. **Byte equality of `common` is unaffected.** PROOF Lemma 6(a) is unchanged: `JCS(C)` occupies bytes
   `[34, 34 + |JCS(C)|)` of both frames (F-H1/F-H2, F-H3/F-H4). Lemma 6(b) and (c) are unchanged too: the
   fingerprint prefixes `spki-sha256:` and `gpg-sha256:` still differ in their first byte.
3. **Rule choice stays left-to-right.** Lemma 7 chooses each slot's rule from that slot's own frame and position,
   both already read. Lemma 7a already covers rule R ("the strings of the parameter set's exact length"); this
   supplement fixes that length at 3309.
4. **The failing shape is rejected.** M9 is the shape where each slot carries its own scheme's id (V1-DERIVATION:
   "KMS ECDSA + gpg OpenPGP is `INVALID` under R-3.12"). Here the kms frame carries the pair id and the gpg frame the
   classical id. That is `RECEIPT_COMMON_MISMATCH` (XHR-08), and it is why A9.6 requires one pair id.

**Status: holds, by construction and by vector.** No model run is needed for R-3.12 itself. It is a byte condition
that the receipt check enforces, and both codecs agree on it.

## 6. P3's model: what "passes P3's model" requires, and the run

**What P3 is.** Key binding (anti-DSKS), `formal/PROPERTIES.md` row P3: `[model]+[assum]`, tool ProVerif, status
`checked`, artifact `formal/suite/s-p3/`. Its two-signer model is S-P3.Q5 (`sp3_q5_multikey_correct.pv`). Its
adversary holds the registered DSKS capability (theory library D-4). The case is degraded mode with the sole
authority channel compromised: the P3 hard case.

**Why the existing models do not cover the pair.** Every S-P3 model signs every slot with the library's single
family `sign/checksign`, which carries one DSKS capability. The mixed pair has two schemes, chosen per slot by one
id. That is a different signature algebra, so "passes P3's model" needs a model run. Reading the old green results
across would not do.

**The model change** (`formal/suite/s-p3/proverif/hybrid/`, derived from Q5 recut 3 and nothing else changed):
- slot A (= kms) signs possession and attestation with a second, model-local family `signR/checksignR`;
- that family has **its own DSKS capability** `dsksR`, of the library's shape. This is conservative: ML-DSA is not
  assumed to resist key substitution;
- slot B (= gpg) keeps the library family;
- both frames and the tuple carry one value `algPair`;
- the verifier accepts only `algPair`, and checks slot A with `checksignR` and slot B with `checksign`, for both the
  possession proof and the attestation.

Predictions were written into each model header before the first run of any of them.

| Model | Prediction (pre-run) | Observed | Outcome |
|---|---|---|---|
| H1 correct (`sp3_h1_hybrid_correct.pv`) | ReattributedA, ReattributedB, PossessionTransplanted unreachable; N1 reachable (p~0.85) | all three **unreachable**; HonestAccepted and Accept2 **reachable** | **as predicted** |
| H2 broken: slot A possession unnamed (`sp3_h2_companion_possession_unnamed_R.pv`) | PossessionTransplanted reachable through `dsksR` (p~0.75) | PossessionTransplanted **reachable**; the derivation applies `dsksR` to the honest rule-R possession signature of `skA2`; Reattributed A/B unreachable | **red as predicted**: the rule-R family's DSKS capability is live in H1 |
| H3 broken: slot A frame unbound (`sp3_h3_companion_unboundA_R.pv`) | ReattributedA reachable only (p~0.75) | ReattributedA **reachable**; ReattributedB and PossessionTransplanted unreachable | **red on exactly slot A** |
| H4 rule O applied to both slots (`sp3_h4_companion_single_rule.pv`) | HonestAccepted unreachable; Accept2 reachable (p~0.8) | HonestAccepted **unreachable**; Accept2 reachable; no violation reachable | **as predicted**: wrong rule selection fails closed (liveness), not open |

Run (ProVerif 2.05, about one second per model, against boxes of 15–30 minutes):

```
formal/suite/s-p3/proverif/hybrid/run_hybrid.sh
# = for each model: proverif -lib ../../../lib/tessera_theory.pvl <model>.pv > <model>.out   (ladder.log records rc and seconds)
```

**Status: H1 passes, and its companions go red exactly where registered.** The mixed pairing passes P3's [model]
half under DSKS on both schemes.
- *Not shown.* The [assumption] half (verification profile, H1a), which stays open as it is for P-256.
- *Not shown.* Anything about the schemes' real security or malleability (the model's signatures are deterministic;
  W1).
- *Not re-run.* S-P2's Q6 (common content). R-3.12 is enforced as a byte rule (§5), not by a new model.
- *Reviewed.* Codex (non-author, 2026-10-14) reran all four models: every query polarity matched, and the trace
  readings above held. Its observations:
  - H3's red is impersonation colliding with honest bytes, not DSKS;
  - H4's "fails closed" covers the honest hybrid flow and the safety queries only;
  - H1's saved HonestAccepted witness is slot B. A scratch query emitted only by JudgeA was also reachable, with the
    safety queries still unreachable. That is review evidence, not registered evidence.
- *Open improvement (not required by A9.6).* Distinct slot-A and slot-B honest witnesses in future model headers.
- PROPERTIES.md is not changed by this supplement.

## 7. The exact ENCODING-V1 §5.2 edit — OWNER-PROPOSED

Applied at registration, with the date filled in. The text below replaces the second row of the §5.2 table, and the
rule R block from "The signed message is the frame itself." through "They are added when an id is registered."

**Table row (replaces the "a hybrid pair id, registered only if the 21 Oct spike passes (not assigned here)" row):**

```
| `KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA256` (hybrid pair id; registered by the branch-registration supplement of <DATE>, A9.6) | rule R: ML-DSA-65 (FIPS 204), pure, empty context | rule O (OpenPGP P-256; slot-2 custody per A9.6) | `kms`: exactly 3309; `gpg`: 1024 |
```

**Rule R block (replaces the five bullets from "The signed message is the frame itself." to "They are added when an
id is registered."):**

```
- The signed message is the frame itself (`F_manifest` for a possession proof). No trailer, no transformation.
- **Registered pair (branch-registration supplement of <DATE>, A9.6).** `KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA256`:
  slot `kms` is ML-DSA-65 (FIPS 204) in pure mode with the empty context, so the FIPS 204 message representative is
  `0x00 ‖ 0x00 ‖ F`; slot `gpg` is rule O. `S_kms` is exactly 3309 bytes. Length 0 gives `SIG_EMPTY`, above 3309
  `LENGTH_CAP`, any other length `SIG_FORMAT`. The codec reads no byte of `S_kms`: a malformed hint encoding or an
  out-of-range `z` is a verification failure (`SIG_INVALID`; `POSSESSION_INVALID` for possession), not a codec code.
- The issuer obtains `S_kms` (attestation and possession) from KMS with `MessageType EXTERNAL_MU` only, sending
  μ = SHAKE256(SHAKE256(pk, 64) ‖ 0x00 ‖ 0x00 ‖ F, 64), pk the raw 1952-byte key (RFC 9881 Appendix D). The result is
  an ordinary pure signature over `F`. The verifier never sees μ and verifies over `F`.
- The kms key under this id is the exact DER SubjectPublicKeyInfo with OID 2.16.840.1.101.3.4.3.18 and no parameters
  (22-byte prefix `308207b2300b0609608648016503040312038207a100`, then the 1952-byte key); anything else is
  `KEY_FORMAT` (RFC 9881 §§2, 4). Its fingerprint is §3.3's `spki-sha256`, unchanged. Key-use assumption (K-R) of
  the supplement replaces PROOF (K) for this slot; the supplement carries both definitions.
- *Consequence to record:* `common.alg` is one value, equal across slots (§0), naming the pair in slot order.
- Vectors: `vectors/hybrid-golden.json` and `vectors/hybrid-reject.json`; agreement run and differential fuzz as in
  PROOF §5 (supplement §8).
- **Branch recorded:** <hybrid | fallback>, <DATE> (A9.6).
```

**This is the only baseline edit registration makes** (HS-05; owner decision 5).
- No other ENCODING-V1 section and no PROOF text is edited.
- Baseline sentences saying rule R has no id, no vectors or no implementation (E§8, PROOF §6) are superseded for the
  hybrid branch by this supplement, and stay unedited.

## 8. Evidence: vectors, agreement run, fuzz, real signatures

**What kind of evidence this is (HS-04).** Implementations A (`gen.py`) and B (`check.py`) are **candidate-codec and
cryptographic-profile evidence**.
- Both hard-code the classical id and the pair id in one codec registry.
- Both treat registry membership as the condition for verifying signatures.
- Neither has an input for the selected catalog id or for registration state.

So they establish:
- the rule R and rule O codecs;
- the ML-DSA-65 and P-256 verification;
- the key encodings;
- R-3.12's byte checks.

They do **not** establish the catalog and registration routing (V1-PROFILE §1 r2-F01, EA-09; §6.4 M5). Those claims
rest on the five profile-conformance cases (a)–(e) in `formal/p8/HYBRID-CONFORMANCE-CASES.md`, which are for
`prototype/conformance` and have not been run.

**Files** (`formal/p8/vectors/`).
- `gen.py` writes the hybrid vectors to `hybrid-golden.json` and `hybrid-reject.json`.
- `golden.json` and `reject.json` regenerate **byte-identical** to the 2026-10-12 baseline (checked with `cmp`
  against copies taken before any edit).
- `check.py` reports the two sets on separate lines.

**Two ML-DSA-65 implementations, no shared local code.**
- **A** (in `gen.py`): KeyGen; Sign from the message or from μ; Verify from the message or from μ. It uses the
  butterfly NTT and big-integer bit packing. Checked by hand against dilithium-py 1.4.0 and cryptography 50.0.2:
  from one seed, the identical public key and the identical deterministic signature.
- **B** (in `check.py`): Verify only. It evaluates and interpolates at the roots ζ^(2·brv8(i)+1) directly, with no
  butterfly and no zeta table, and reads bit fields with a cursor. It parses the SPKI DER field by field, where A
  compares a prefix.
- What they share: hashlib's SHA-256, SHAKE-128 and SHAKE-256 (plus the baseline's Unicode tables and float), and one
  author instance. "No shared code" means no shared local implementation, not independent authors or independent
  cryptographic backends (PROOF §6's limit).
- **Demonstration switches (vectors only).** Both verifiers can switch off exactly one decoding gate at a time:
  `norm`, `order` or `padding`. This lets a vector show that it fails on that gate alone. The cumulative-count gates
  cannot be switched off, because without them the hint field is undecodable.

**Golden vectors (35).**

*Illustrative test key (public seed):*
- fingerprint K-H1;
- manifest M-H1;
- frames F-H1 to F-H4 (F-H3/F-H4 are 5246 bytes);
- SIG-H1 (pure, deterministic) and SIG-H3 (made from external μ);
- rule O under the pair id: SIG-H2, SIG-H4;
- anchors A-H1, A-H2;
- receipts R-H1, R-H2;
- possession P-H1 (kms, rule R over `F_manifest`) and P-H2 (gpg, rule O).

*Real keys, earlier spike captures:*
- K-H2: the real KMS key's fingerprint;
- SIG-H5 (KMS RAW, comparative) and SIG-H6 (KMS EXTERNAL_MU). These are over the spike's V1-**shaped** frames, with
  tag `tessera-v1/receipt`, which is not in T. They are verified over the exact bytes KMS signed and are **not
  re-framed**;
- SIG-H7: GCP HSM rule O over a real V1 attest frame that carries the classical id.

*Genuine capture (HS-01): both real keys over genuine V1 hybrid frames.* The owner ran `spike_v1_hybrid.py` at about
03:23Z on 2026-10-14. These vectors are the archived bytes, unaltered:
- manifest M-G1;
- frames F-G1 to F-G4 (758 / 757 and 6753 / 6752 bytes; both decoders accept all four as `attest`);
- **SIG-G3**: KMS EXTERNAL_MU over the 6753-byte F-G3, the selected issuer path, with μ recorded and recomputed by B;
- SIG-G1: KMS RAW over F-G1, **comparative**;
- SIG-G2, SIG-G4: GCP HSM rule O, instrument-direct;
- anchors A-G1 (`89dac77b…02c2e37`) and A-G2 (`a4c24658…f28013d`);
- receipts R-G1 and R-G2: both real committed signatures verify under the real slot keys, in A and in B;
- possession P-G1 (kms; KMS RAW, comparative) and P-G2 (gpg).

**Rejection vectors (63).**

| Group | Vectors | Codes |
|---|---|---|
| Anchor codec (14) | XH-01 to XH-14: truncated (3308), trailing (3310), slot length ±1, empty, two signatures, ML-DSA-44 and ML-DSA-87 sizes, wrong-slot rules both ways, slots swapped, ML-DSA under the classical id, base64 text, unknown id above the opaque cap | `SIG_FORMAT`, `LENGTH_CAP`, `SIG_EMPTY` |
| Receipt (19) | XHR-01 (negative control: a second valid hedged signature); XHR-02, XHR-03, XHR-11 (signature over another frame, a c̃ bit flipped); XHR-05; XHR-06 / XHR-07 (P-256 SPKI / another ML-DSA key); XHR-08 (M9 shape); XHR-09 (unknown id); XHR-10. **HS-03 mode and context:** XHR-13 (valid signature with nonempty context `tessera-v1`), XHR-14 (valid HashML-DSA / SHA-256), XHR-15 (valid signature over μ computed without `00 00`). Each has its anchor rebuilt, so the failure is verification. **HS-03 hint decoding**, all 3309 bytes and codec-valid: XHR-04 (indices out of order) and XHR-16 (a duplicate index), each **accepted with only the `order` gate off**; XHR-17 (nonzero padding), **accepted with only the `padding` gate off**; XHR-12 (z norm), **accepted with only the `norm` gate off**; XHR-18 (cumulative count 56 > ω) and XHR-19 (decreasing counts), explicit decoder failures, rejected even with every switchable gate off | `RECEIPT_ANCHOR_MISMATCH`, `SIG_INVALID`, `KEY_FORMAT`, `KEY_MISMATCH`, `RECEIPT_COMMON_MISMATCH`, `UNVERIFIABLE` |
| Key encoding (13) | XK-01 to XK-13 (§3) | `KEY_FORMAT`, `KEY_MISMATCH` |
| Possession (11) | XP-01 to XP-08 (wrong frame or manifest, truncated, wrong-slot rules, wrong key, P-256 SPKI); **HS-03:** XP-09 to XP-11, the nonempty-context, HashML-DSA and no-prefix-μ signatures over `F_manifest` | `POSSESSION_INVALID`, `SIG_FORMAT`, `LENGTH_CAP`, `KEY_MISMATCH`, `KEY_FORMAT` |
| Real KMS signatures (6) | XM-01 to XM-06 | `SIG_INVALID`, `SIG_FORMAT`, `LENGTH_CAP`, `KEY_FORMAT` |

The codec stays byte-blind for rule R; there is no `sigDecode` gate in either codec (owner decision 3).

**Results** (2026-10-14, after the HS revisions; Python 3.14.6):
- **A** self-checks every vector, its expected code, and each demonstration: the gate-off acceptance, and the
  decoder failure even with every gate off.
- **B, baseline:** 71/71 golden, 173/173 rejections with A's code, 5/5 negative controls (unchanged).
- **B, hybrid:** 35/35 golden round-trip and verify; 63/63 rejections with A's code; 1/1 negative control; and
  **6/6 gate demonstrations**, checked with B's own verifier.
- **Differential fuzz** (`fuzz.py`):
  - stages 1–3 reproduce the baseline histograms exactly (60,000 cases);
  - stages 4–6 add 30,400 hybrid cases, now drawing on the genuine anchors and signatures as well;
  - **0 disagreements** in 90,400 cases;
  - stage 4: 20,000 anchor mutations, 2481 accepted, the rest across 13 reason codes;
  - stage 5: 10,000 SPKI mutations (`KEY_FORMAT` 9400, `KEY_MISMATCH` 596, OK 4);
  - stage 6: 400 verify pairs (347 false, 53 true).
- **Sensitivity** (each defect planted in a scratch copy of B). Caught:
  - rule R accepting short lengths;
  - skipped verification;
  - NULL parameters accepted;
  - a trailing SPKI byte accepted;
  - hint order unchecked (XHR-04/16 demonstrations);
  - padding unchecked (XHR-17);
  - z bound loosened (XHR-12);
  - μ computed without `00 00` (19 failures).

  Not catchable: removing the "count ≤ ω" bound. A count above 55 cannot form a consistent signature, so XHR-18 is
  a decoder-failure check, as HS-03 asks, not an acceptance demonstration.
- **External cross-check** (by hand). cryptography/OpenSSL and dilithium-py agree with A and B on:
  - every genuine signature (SIG-G1, SIG-G3, R-G1, R-G2, P-G1: verify);
  - every HS-03 mode, context and hint vector, **except one third-party finding:** dilithium-py 1.4.0 *accepts*
    XHR-16 (duplicate hint index), which cryptography, A and B reject. dilithium-py's hint decoding is not strict
    about duplicates, so it is not a sufficient reference for FIPS 204's strong-unforgeability encoding checks;
  - XHR-13 itself verifies in dilithium-py under its own context `tessera-v1`, which confirms it is a valid signature
    in the wrong mode.

**The genuine-capture archive (HS-01)** is in `formal/p8/evidence/v1-hybrid-2026-10-14/`:
- `capture.json`: a byte-exact copy of `prototype/spike-pq/out-v1-hybrid/capture.json`;
- `evidence.json`, which records:
  - the manifest;
  - both attestation pairs, with exact frames, signatures, lengths and frame hashes;
  - both possession proofs;
  - the kms SPKI and its fingerprint, the gpg point, creation time and fingerprint;
  - for each pair, the KMS mode at capture and the issuer-computed μ: for the large frame (6753 bytes), μ =
    `d7d8feea7605f0cb253a12625f0acb354d0d57fba209fa402da06673e5c03e48c071cc61476b8940192a0ac45df9cfd235d2333179eaee647f10d48753611872`;
  - the capture hash and tool versions (Python 3.14.6, cryptography 50.0.2, dilithium-py 1.4.0, rfc8785 0.1.4,
    and the gen.py, check.py and instrument hashes; the instrument hash `c06cae46…26c6da` is the script as run, before a later comment-only edit);
- `verify-ab.log`: 27 offline checks, all PASS. A and B, each on its own:
  - both frames of each pair decode as `attest`, including the large one;
  - each exact KMS signature verifies over its exact frame;
  - both receipts and both possession proofs pass;
  - cryptography and dilithium-py verify every kms signature;
- `derive.py`: regenerates the other two files offline from `capture.json`.

**Reproduce** (offline):

```
uv run --no-project --with rfc8785==0.1.4 python formal/p8/vectors/gen.py
python3 formal/p8/vectors/check.py
uv run --no-project --with rfc8785==0.1.4 python formal/p8/vectors/fuzz.py      # about 4 minutes
prototype/.venv/bin/python formal/p8/evidence/v1-hybrid-2026-10-14/derive.py
formal/suite/s-p3/proverif/hybrid/run_hybrid.sh
```

## 9. Objects and hashes named by this supplement (HS-06)

**What A9.6's "exact ENCODING-V1 and specification hashes" name.**
- **ENCODING-V1 baseline.** `formal/p8/ENCODING-V1.md` at A9's signing commit, the object A9 incorporates
  (V1-PROFILE §1, "Encoding"; "Baseline", G37). Its hash at drafting is below.
- **The specification.** The **frozen V1 verification-spec object**: the multipart object whose hash is the
  catalog's spec hash and every frame's `common.spec.sha256` (`tessera-v1-strict/verification-spec/1`; V1-PROFILE §1
  "Baseline", §15.8). It exists only at the 30 Oct freeze, so its hash is entered then. It is not substituted by any
  file below.
- **`docs/implementation-spec.md` is a design reference only.** Its hash is recorded so the reading can be traced.
  It is not the specification object A9.6 names.
- **The registration record** must also name the final hash of this supplement and of the edited E§5.2 artifact
  (ENCODING-V1 after §7's edit).

At drafting (2026-10-14, after the HS revisions):

| Object | Role | SHA-256 |
|---|---|---|
| `formal/p8/ENCODING-V1.md` (unedited) | ENCODING-V1 baseline (replace with the signing-commit value) | `d9ea82eb3e893fef865f124a612ecb6784932ea131559d792be8f01e597eb5ec` |
| frozen V1 verification-spec object | the A9.6 specification hash | *entered at the 30 Oct freeze* |
| `docs/implementation-spec.md` | design reference only | `75b3e7cc3348293703c6119cb7608245b3bfc532e34539566d1fc133406f07e7` |
| `formal/p8/PROOF.md` (unedited) | baseline proof | `06910a5f81128e05694e4ee8c3034e8149fbac04b330dcb2a1ed9386fd21ff30` |
| `vectors/golden.json`, `vectors/reject.json` | baseline vectors, unchanged | `27feee26…aab880bdf`, `0891f76c…eadef59f5f` |
| `vectors/hybrid-golden.json` | hybrid golden (35) | `cb568c29ce79a9d2d8b1fc417576d4b1c4534fdde3a2f05ded87f095310c12ec` |
| `vectors/hybrid-reject.json` | hybrid rejection (63) | `13b176190c49870d5ad96cf4a3c272f819b3f02acdda83d11f5eea185507e16d` |
| `vectors/gen.py` / `vectors/check.py` | implementations A / B | `d9257fe28626d3bb838f5b3b011f5e96951f7993319bd8cafb3de904d4d2bac3` / `51546d40a7cdc8af3090878e60a4e9cd0102d7e4a2a499a5dd275ad19ed955ae` |
| `evidence/v1-hybrid-2026-10-14/capture.json` | genuine capture (= `prototype/spike-pq/out-v1-hybrid/capture.json`) | `5895f79438f82cb95b15ef1fe57ff4726970bc2635f25dd05d84ec1d50648e92` |
| `evidence/v1-hybrid-2026-10-14/evidence.json` | archive record | `233d995265b750acb86d25041c6486cec97ffd1925c809b401cdd709a00165ed` |
| `evidence/v1-hybrid-2026-10-14/verify-ab.log` | offline A/B output | `3bacc119fad460a193f9a14b4df575db7b35dba5c1502ecff65199c64c8b227e` |
| `prototype/spike-pq/out-kms/capture.json`, `out-gcp/capture.json` | earlier spike captures | `ff1b2c96…1d87c3ed`, `cb46cd80…48b40bf3` |

Under the hybrid, the frozen conformance-vector object (`vectors_sha256`) includes the two hybrid vector files and the
genuine-capture vectors in them (owner decision 6; V1-PROFILE §15.8).

## 10. Pass condition, bullet by bullet (A9.6), as of 2026-10-14 (after the HS revisions)

1. **The pair identifier is registered with its mode and context.** Drafted (§1). The id is the owner's choice
   (decision 4). Registration is the owner's dated act.
2. **The mixed-format pairing passes R-3.12 and P3's model.** R-3.12 holds (§5, XHR-08). P3's model: H1 holds, and
   the companions are red exactly as predicted (§6). Codex reran all four models and found every polarity unchanged.
3. **A real KMS ML-DSA-65 signature over a V1 frame (external μ above 4 KB) verifies offline in two
   implementations.** **Met** (HS-01).
   - SIG-G3 / R-G2 is the real KMS EXTERNAL_MU signature over the genuine 6753-byte V1 attest frame F-G3.
   - Both frame decoders accept F-G3 as `attest`. Both verifiers, A and B, verify the exact signature over the exact
     frame, and so do cryptography and dilithium-py.
   - The issuer-computed μ is archived.
   - Evidence: §8 and `formal/p8/evidence/v1-hybrid-2026-10-14/`, capture SHA-256 `5895f794…50648e92`.
   - The RAW items (R-G1, P-G1) are comparative.
4. **A real P-256 signature from the `gpg` slot as deployed verifies offline.** **HSM custody and offline rule-O
   compatibility met (HS-02); deployed-slot path **Met 2026-10-14**: see
   `prototype/policy-signer/EVIDENCE.md`.
   - Through the deployed queue path, with no direct key call: a genuine V1 hybrid attest frame (declared time = now)
     was signed by Cloud Run job `slot2-signer` (image `sha256:80342551…adb5`) using `slot2-spike/cryptoKeyVersions/1`
     (HSM, P-256). The 119-byte rule-O packet verifies in A and B; the full receipt is accepted by both codecs; the
     manifest possession signature verifies (`prototype/policy-signer/out/evidence-a.json`). Owner re-check
     2026-10-14: gen.py verifies, the frame's key_fp equals fp_gpg of the key, and tamper is rejected.
   - Refusals: declared time 25 h past gives `DECLARED_TIME_OUTSIDE_EPSILON` (ε = 86,400 s); wrong tag gives
     `TAG_UNKNOWN`/`TAG_MISMATCH`; the kms key_fp in a gpg frame gives `KEY_FP_MISMATCH`.
   - Access boundary: the key's IAM policy grants signer/publicKeyViewer only to `slot2-signer@`; the AWS side holds
     no GCP credential; the signer reaches SQS by Google-OIDC web identity federation to role
     `tessera-slot2-signer-sqs` (no static keys). Default compute Editor and legacy Cloud Build grants were removed
     (`prototype/policy-signer/RESOURCES.md`).
   - Stated limit: manifests carry no declared time, so the ε check does not apply to possession signing; C3 holds.
   - The bullets below record the earlier state.
   - SIG-H7, SIG-G2, SIG-G4 and P-G2 are genuine GCP HSM rule-O signatures, made by direct instrument calls
     (`gcloud kms asymmetric-sign`).
   - None exercises A9.6's queue-pulling policy signer: its complete-frame validation, its own-clock declared-time
     refusal, or the boundary that keeps the issuing AWS account from invoking the GCP key.
   - *To complete by 21 Oct:*
     - the dated deployment and access-policy record;
     - a signature captured through the selected policy signer over an accepted valid frame;
     - a refusal for a declared time outside ε;
     - an evidence record naming the signer version, clock policy, queue path, key version and access boundary.
   - The owner is building the policy signer separately; this supplement does not.
5. **The full selected byte profile is specified and tested.** Met at the candidate-codec level:
   - attestation and possession for both slots, genuine and illustrative (R-G*, P-G*, R-H*, P-H*, XHR-*, XP-*);
   - slot key and fingerprint encodings (§3, K-H*, XK-*);
   - key-use assumptions (§4);
   - golden and rejection vectors with an agreement run for rule R (§8).

   The routing claims additionally need the profile-conformance cases (a)–(e) (HS-04), which are not yet run.

## 11. Decisions: resolved and open

**Resolved by the owner, 2026-10-14** (`docs/reviews/hybrid-supplement/DECISIONS.md`):
1. Re-capture genuine V1 hybrid frames: **done** (HS-01, §10.3).
2. The gpg-slot custody is the GCP Cloud KMS HSM, with no token capture. The deployed policy-signer path is still
   owed (§10.4).
3. Malformed ML-DSA internals are `SIG_INVALID`. The codec stays length-only, and PROOF Lemma 7a is unchanged.
4. The identifier, as proposed.
5. **Resolved:** the key encoding and K-R stay in this supplement. Registration edits only E§5.2 (§7).
6. **Resolved:** the issuer always uses EXTERNAL_MU for the kms slot, attestations and possession alike. RAW
   captures are comparative. `vectors_sha256` covers the hybrid files at the freeze. Both spike keys are deleted
   after the re-capture verifies, once the review clears (REPORT.md).

**Still open:**
- HS-02 deployed-slot evidence through the policy signer, by 21 Oct (§10.4).
- HS-04 profile-conformance cases (a)–(e), run in `prototype/conformance`.
- The frozen verification-spec hash and the final supplement and E§5.2 hashes, entered in the registration record
  (§9).
- KMS key policy for (K-R) (runbook): `kms:Sign` only for the issuer role. Restricting `kms:MessageType` to
  EXTERNAL_MU now matches the selected path, but it cannot bind what a μ hashes.
- Optional: distinct slot-A and slot-B honest witnesses in the P3 hybrid models (§6).
