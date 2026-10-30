# P3 verification profile: the [assumption] half (H1a evidence)

**Status:** evidence drafted 2026-10-27 for the 20 Nov obligation, revised the same day for Codex review P3R-01..06
(`docs/reviews/p3-profile/CODEX-REVIEW.md`). It is not a tracker move. `formal/PROPERTIES.md` row P3 stays `checked`
until the owner assesses this evidence and the author rules on the translation (§4). The review verdict was
"retain P3 as checked".

**Registered obligation.** `docs/phase-0-prereg-amendment-1.md:144-148` (P3): the implementation's verification
profile is **[assumption]**, "named in Layer 2 and discharged as H1a evidence: exact library and version, accepted
signature encodings, public-key validation behavior, low-order-point handling, cofactor equation variant, and
negative test vectors for each, all recorded in the repository." The [model] half is `formal/suite/s-p3/`.

**Run it** (from `service/verifier`):

```
.venv/bin/python -m pytest -q ../../formal/p3-verification-profile/test_p3_profile.py
```

| File | Contents |
|---|---|
| `vectors/F1-library.json` | library, version, OpenSSL build, wheel tag and binding digest, the four exact calls |
| `vectors/F2-signature-encodings.json` | 65 signature vectors: rule-O encodings (O-01..O-25), rule-O policy (P-01..P-06, P-10..P-25), rule R (R-01..R-18) |
| `vectors/F3-public-key-validation.json` | 37 key vectors (K-01..K-37) |
| `vectors/F4-low-order-points.json` | 8 key vectors (L-01..L-08) |
| `vectors/F5-equation-variant.json` | 11 equation/message-representative vectors (E-01..E-11) and the key-substitution pair (D-01, D-02) |
| `test_p3_profile.py` | vector harness, permissive-backend tests, library characterization, bundle tests, wheel identity |
| `gen_vectors.py`, `p256.py` | provenance of the vector files. `p256.py` is pure-Python point arithmetic used only to build inputs |

Every vector names its expected outcome: `ACCEPT` or the exact code. **The vector harness is function-level.**
`run_sig` calls `parse_signature`, then `sig_policy`, then `signature_verifies` against one known-good key, and
`run_key` calls `public_key`. These are the functions behind bundle rows 3.1/9.3, 9.1/9.4, 9.2/9.5 and 5.1, but the
harness does not reproduce the bundle's order: a bundle evaluates keys (5.1) before signature policy (9.1) and
reports by row precedence. **Precedence is claimed only from the bundle tests** (B01..B08; B08 is a combined key and
policy failure, which reports `KEY_FORMAT`). `SIG_INVALID` in a vector reads as `POSSESSION_INVALID` for a possession
proof, because the same function serves both rows (`verify.py:216`, `verify.py:226`). There are 22 positive controls
across the three slot rules. `TestControls` fails if a file has no `ACCEPT` or only one outcome.

## 0. Scope

P3 concerns the issuer's signatures: the two receipt slots and the two possession proofs. V1's issuer signature
algorithms (V1-PROFILE §8; ENC §5.2) are:

- **slot `kms`, hybrid pair id** `KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA256`: ML-DSA-65 (FIPS 204), pure mode,
  empty context, raw 3309-byte signature (rule R). The key is the exact 1974-byte RFC 9881 SPKI.
- **slot `gpg`** (both ids), and **slot `kms` under the classical fallback id** `OPENPGP4-ECDSA-P256-SHA256`: ECDSA
  P-256 / SHA-256 inside an OpenPGP v4 signature packet (rule O). The `gpg` key is the bare v4 public-key packet
  body; the fallback `kms` key is a 91-byte P-256 SPKI.

The V1 installation's catalog alg is the hybrid id. The fallback is covered because it is codec-known.

The same rule-O functions also verify the git commit signature against the trust configuration's repository key
(`policy.py:57`, `verify.py:278`), so F2/F3 apply to that key too (bundle test B07).

**Outside P3; listed, not profiled:**

| Verifier path | Algorithm | Call |
|---|---|---|
| DNSSEC RRSIG (`dnssec.py:187-200`) | RSASSA-PKCS1-v1_5/SHA-256 (alg 8), ECDSA P-256/SHA-256 (alg 13; key via the same `codec.point`) | `pub.verify(sig, data, padding.PKCS1v15(), hashes.SHA256())`; `pub.verify(encode_dss_signature(r, s), data, ec.ECDSA(hashes.SHA256()))` |
| TEST release stand-in (`release_auth.py:51-75`) | ECDSA over SHA-256 of the JCS body | `serialization.load_der_public_key(spki)` then `pub.verify(der, body, ec.ECDSA(hashes.SHA256()))`. See DIVERGENCES.md D1 |

## 1. F1: exact library and version, and the exact calls

| Item | Value | Backed by |
|---|---|---|
| Library | `cryptography` **50.0.2**, pinned in `service/verifier/requirements.txt` and `pyproject.toml` | `TestF1Library::test_installed_library_is_the_recorded_one`, `test_requirements_pin` |
| Wheel | tag `cp311-abi3-manylinux_2_34_x86_64`; `cryptography/hazmat/bindings/_rust.abi3.so` SHA-256 `1e5d23fa66915204b9b67202a46993844d81cda56f6ad52cead2def37617ee29` | `test_installed_wheel_identity` (verifier venv) |
| Backend | `OpenSSL 4.0.3 29 Sep 2026`, statically linked into that binding (cryptography's wheels bundle OpenSSL), as `backend.openssl_version_text()` reports | `test_installed_library_is_the_recorded_one` |
| Interpreter | CPython 3.14 (3.14.6 at generation) | same test |
| ML-DSA-65 key | `mldsa.MLDSA65PublicKey.from_public_bytes(raw[22:])`, after the verifier checks `len(raw)==1974 and raw[:22]==MLDSA65_SPKI` (`codec.py:257-263`) | `test_recorded_call_is_the_verifiers_call[mldsa65_key]` |
| ML-DSA-65 verify | `key.verify(sig, document, context=b'')`, after the verifier's own `mldsa65_encoding_valid(sig)` gate (`codec.py:288-294`) | `[mldsa65_verify]` |
| P-256 key | `ec.EllipticCurvePublicNumbers(x, y, ec.SECP256R1()).public_key()`, after the verifier's own range and on-curve checks (`codec.py:250-255`) | `[p256_key]` |
| P-256 verify | `key.verify(utils.encode_dss_signature(sig.r, sig.s), digest, ec.ECDSA(utils.Prehashed(hashes.SHA256())))`, digest = SHA256(F ‖ v4 trailer), after the hash-prefix comparison (`codec.py:295-298`) | `[p256_verify]` |

The call tests require each call string to occur exactly once in `codec.py`. F1's "negative vector" is a tripwire:
a different library version, wheel binding, OpenSSL build, interpreter or call fails `TestF1Library`, and this
profile must then be re-recorded. A genuinely different supported build needs its own record.

**Deployment tie.** The issuer Lambda runs the verifier from the zip that `service/issuer/package.py` builds. That
script resolves `cryptography==50.0.2` for `x86_64-manylinux_2_34` and prints the zip's SHA-256, and that zip is what
infra deploys as `lambda_zip`. The deployed verifier's library identity is tied to this record through the package
digest:

- `test_lambda_package_wheel_identity` runs `package.build()` into a fresh temporary directory and checks that the
  zip's `_rust.abi3.so` digest and wheel tag equal F1. It passed in this run, using uv's cache or the network; it
  skips with a stated reason if uv or the build is unavailable.
- `test_deployed_zip_identity` checks a specific zip when `TESSERA_LAMBDA_ZIP` names it. It is skipped unless set.
  Run it on the deployed artifact, whose digest matches the deployed `lambda_zip`.

This is not a Lambda invocation. The record says which bytes are deployed, not that they were exercised on Lambda.

`package.py` does not itself expose the cryptography binding digest; it was not edited. Suggested change, for the
issuer owner: have `build()` return or print the `_rust.abi3.so` SHA-256 and the dist-info `WHEEL` tag beside the
zip digest, and fail if they differ from `formal/p3-verification-profile/vectors/F1-library.json`. A package with a
different backend could then not be built silently.

## 2. F2: accepted signature encodings and rule-O policy

**Rule O encoding (gpg slot; fallback kms slot).** Accepted: exactly one legacy-format signature packet, `0x88 u8`
(body ≤ 255) or `0x89 u16` (256..1021), with a v4 body of type 0x00, algorithm 19, hash 8, shortest-form subpackets,
two prefix octets, then MPIs r and s of 1..256 bits each with exact bit counts; r, s ∈ [1, n−1].

- **Both low-S and high-S are accepted.** O-01 is low-S (s ≤ n/2). O-02 is its high-S twin (r, n−s). A test asserts
  which is which (`test_O01_is_low_s_and_O02_is_its_high_s_twin`).
- **DER is never an accepted input form.** The verifier builds the DER itself from the parsed MPIs. The analogue of
  non-canonical DER, a non-minimal MPI, is `SIG_FORMAT` (O-15).

| Rejected | Code | Vectors |
|---|---|---|
| OpenPGP-format header, non-shortest header, bare DER, raw r‖s, armor | `SIG_PACKET` | O-04..O-08 |
| trailing / truncated | `TRAILING` / `TRUNCATED` | O-09, O-10 |
| v5, type 0x01, algorithm 22, hash 10, MPI with leading zero, 257-bit MPI, r = 0 | `SIG_FORMAT` | O-11..O-17 |
| r = n, s = n, r = 2²⁵⁶−1 | `SIG_POLICY` | O-18..O-20 |
| prefix octets wrong, other document, other key | `SIG_INVALID` | O-21..O-23 |
| rule-O packet in the hybrid kms slot | `SIG_FORMAT` | O-25 |

**Rule-O signature policy** (V1-PROFILE §8, "Rule-O signature policy" and "Advisory metadata, structural
validation"; `codec.sig_policy`). Every P vector is a correctly signed packet over its own hashed area.
`TestRuleOPolicy::test_policy_vector_is_correctly_signed` checks that each one verifies when `sig_policy` is
skipped, so each `SIG_POLICY` outcome is the policy's doing.

- **Hashed area:**
  - exactly one creation-time subpacket (type 2) with exactly 4 data octets, critical or not;
  - no signature-expiration subpacket (type 3), critical or not;
  - types 16 and 33 accepted, critical or not, with exact structure: at most one 16, of 8 octets; at most one 33, of
    21 octets with first octet 04; if both are present, 16 equals the last 8 octets of 33;
  - any other type is ignored if noncritical and a failure if critical.
- **Unhashed area:** ignored entirely, critical bits included, after ENC's subpacket framing.

| Case | Outcome | Vectors |
|---|---|---|
| creation time critical; GnuPG shape (hashed 2 + 33, unhashed 16); hashed 16 + 33 consistent; 16 + 33 both critical; unknown noncritical hashed type | `ACCEPT` | P-01..P-05 |
| unhashed area holding a critical unknown, a critical expiration, malformed and inconsistent 16/33, and duplicate creation times | `ACCEPT` (ignored) | P-06 |
| creation time missing, duplicated, 3, 5 or 0 data octets | `SIG_POLICY` | P-10..P-14 |
| expiration, noncritical or critical | `SIG_POLICY` | P-15, P-16 |
| unknown critical type; RFC-known type 4 marked critical | `SIG_POLICY` | P-17, P-18 |
| type 16 of 7 octets; two type 16; type 33 of 20 octets; type 33 version 05; two type 33; 16/33 inconsistent; zero-data critical 33 | `SIG_POLICY` | P-19..P-25 |

**Rule R (hybrid kms slot).** Accepted: exactly 3309 bytes that pass the FIPS 204 HintBitUnpack and z-bound
conditions and verify under pure ML-DSA-65 with the empty context. Positive controls: a library `sign(F, context=b'')`
signature (R-01) and an `EXTERNAL_MU`-style `sign_mu` signature (R-02, the issuer's path).

| Rejected | Code | Vectors |
|---|---|---|
| length 0 | `SIG_EMPTY` | R-03 |
| length 3308, ML-DSA-44 (2420) | `SIG_FORMAT` | R-04, R-06 |
| length 3310, ML-DSA-87 (4627) | `LENGTH_CAP` | R-05, R-07 |
| hint: nonzero padding, duplicate index, swapped indices (each decodes to the **same** h under a lax decoder), count ω+1, decreasing counts | `SIG_INVALID` | R-08..R-12 |
| z coefficient = ±(γ1−β) | `SIG_INVALID` | R-13, R-14 |
| z in range but wrong, c̃ flipped, other document, other key | `SIG_INVALID` | R-15..R-18 |

R-08..R-14 are rejected by the verifier's own gate before the library is called. `TestMLDSAGate` proves this with a
permissive mock backend, so rejection does not depend on library strictness. The library also rejects them without
the gate (LIB07), so with this build the gate is defence in depth.

## 3. F3: public-key validation behaviour

**P-256 (gpg packet; fallback kms SPKI; repository key).** The verifier requires:

- the exact encoding: the 82-byte v4 packet body with prefix `13 08 2a8648ce3d030107 0203`, or the 26-byte SPKI prefix
  plus 65 bytes;
- an **uncompressed** point `04‖X‖Y`.

It then checks **X < p, Y < p and the curve equation itself, before the EC constructor is called**. All of the
following are `KEY_FORMAT`:

| Case | Vectors |
|---|---|
| compressed point | K-05, K-17 |
| hybrid 06/07 encoding | K-06 |
| off-curve point | K-03, K-15 |
| non-canonical X = x+p | K-04, K-16 |
| non-canonical Y = y+p | K-36, K-37 |
| other curves | K-09, K-18, K-19 |
| wrong version, algorithm, MPI count or length | K-07, K-08, K-10..K-12 |
| cross-slot encodings | K-13, K-20, K-21 |

A bad repository key refuses the trust configuration (`TRUST_CONFIG_UNAUTHENTICATED`, B07).

**Ordering, tested (P3R-02).** `TestPointBeforeConstructor` replaces `codec.ec`, for the codec module only, with a
permissive stand-in whose constructor accepts anything:

- **Rejected without the constructor ever being called:** X ≥ p (K-04, K-16), Y ≥ p (K-36, K-37), curve membership
  (K-03, K-15, L-03, L-01), and representation (compressed, hybrid, leading 00 or 05).
- **Positive controls reach the constructor with the exact (x, y):** K-01, K-02, K-35, K-14.

So the verifier's own checks decide these cases, not the library's defaults. This matters because the library alone
**accepts X ≥ p and Y ≥ p and reduces them** (LIB02, LIB09). Its DER loader also **accepts compressed-point SPKIs and
other curves** (LIB03). The library does reject off-curve points by itself (LIB01), so for curve membership the
verifier's check is shown, by the mock, to come first, but is redundant with this build.

**ML-DSA-65 (hybrid kms).** The only check is the exact 1974-byte SPKI: OID 2.16.840.1.101.3.4.3.18, parameters
absent, zero unused bits, minimal DER (K-22 accepted; K-24..K-34 `KEY_FORMAT`). There is no further public-key
validation. Every 1952-byte string is a well-formed FIPS 204 key: the all-zero key is accepted (K-23), and the
library accepts it too (LIB06). That is decoding behaviour, not a security claim about such a key. The library's
generic DER loader would accept ML-DSA-44/-87 SPKIs as keys of their own parameter sets (LIB04); the verifier's
exact-prefix rule rejects them (K-28, K-29).

## 4. Translation of A1's Ed25519 fields — OWNER READING, contestable

**Not decided here: the algorithm policy.** V1 *requires* both algorithms. The frozen catalog names only the hybrid
`KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA256` (registered 2026-10-16). Any other algorithm is `ALG_UNKNOWN`
(`verify.py:180`), and a receipt missing either signature fails (G3). This section decides only whether checking each
of the two algorithms against its own analogue of A1's Ed25519 checklist meets P3's registered words. Because both
signatures are required, a forgery must break both. A weakness noted below for one algorithm matters only if the
other algorithm also fails.

The registered text names Ed25519 concepts. V1 does not verify Ed25519. The mapping below is the owner's reading and
is open to challenge: whether these analogues discharge the registered words is for the author to rule. (Codex
review: "a reasonable, explicitly contestable owner reading, not a concealed amendment"; its sufficiency still
needs the author's ruling.)

| A1 field (Ed25519 sense) | V1 analogue: ECDSA P-256 (rule O) | V1 analogue: ML-DSA-65 (rule R) |
|---|---|---|
| Exact library and version | §1 | §1 |
| Accepted signature encodings (canonical S < L, canonical R) | §2: OpenPGP v4 packet, exact-bit-count MPIs, r, s ∈ [1, n−1], rule-O policy. **High-S accepted**: ECDSA's (r, s)/(r, n−s) malleability is not removed, and the profile relies on the anchor's exact-copy commitment (ENC §3.5) | §2: exact 3309 bytes; strict HintBitUnpack and z bound, so one (c̃, z, h) has one encoding (R-08..R-10) |
| Public-key validation (canonical A encoding, small-order A) | §3: exact uncompressed encoding, coordinates < p, on-curve, all before the constructor | §3: exact SPKI only. **No algebraic validation exists**, so this is "not applicable beyond encoding" |
| Low-order-point handling (the 8-torsion of Curve25519) | P-256 has **cofactor h = 1**: every finite on-curve point has prime order n, and the only low-order element is the point at infinity. As a **public key** it cannot be received (L-01, L-02, L-06, L-08 `KEY_FORMAT`); as the **result of the verification equation** it is rejected (E-11). The live residue of the concern is **invalid-curve points**, including small-order points on other curves with the same a; the verifier's on-curve check rejects them before the constructor (L-03, an order-2 point of y² = x³ − 3x + 2; L-04, L-07). h = 1 is a property of the curve (SP 800-186), not something a test here derives | **Not applicable**: ML-DSA is lattice-based, with no group, cofactor or torsion. Degenerate keys (e.g. all-zero t1) are accepted (K-23); whether they weaken anything is not tested here |
| Cofactor equation variant (cofactored [8]SB = [8]R + [8]kA vs cofactorless) | With h = 1 the cofactored/cofactorless distinction does not exist. The equation choices that remain, all tested: the message representative is SHA256(F ‖ v4 trailer), passed `Prehashed`, with no second hash and no plain SHA256(F) (E-01..E-03); the hash prefix is checked; **x(R) is reduced mod n before comparison with r**: E-10 is a constructed key with x(R) = n + 3, r = 3, s = 1, accepted, where an unreduced comparison would reject (`TestEquationConstruction` confirms x(R) ≥ n; LIB10 shows the library does the reduction); a verification result of infinity is rejected (E-11) | The variant question becomes **which FIPS 204 interface**. The verifier uses pure ML-DSA, empty context: M′ = 00 ‖ 00 ‖ F. A non-empty context (E-04, E-09), HashML-DSA (E-05, E-06), the internal interface with no domain prefix (E-07) and μ passed as the message (E-08) are all `SIG_INVALID` |
| (P3's premise) the verification equation is not issuer binding | **Demonstrated**: from (F, S) alone, `p256.dsks_keys` computes a different valid P-256 key under which the honest signature verifies (D-02 `ACCEPT` at the function level). In a bundle that key is rejected by the signed fingerprint binding: `KEY_MISMATCH` (B02). Rewriting the manifest to match gives `RECEIPT_MANIFEST_MISMATCH` (B03). This concerns substitution into existing honest signed material, not receipts minted by an attacker who holds both channels | Not demonstrated either way. ML-DSA hashes tr = H(pk) into μ, which is the usual argument for its exclusive-ownership properties; no test here exercises it |

E-10 and E-11 follow Codex's construction (review scratch `probe.py`): choose an on-curve R with x(R) = n + r, then
Q = r⁻¹(R − eG) with s = 1. For E-11, Q = (−e/r)G, so eG + rQ = O.

## 5. Library behaviour claims and the test behind each

| Claim (the F1 wheel, without the verifier's checks) | Test |
|---|---|
| `EllipticCurvePublicNumbers(...).public_key()` rejects an off-curve point | `TestLibraryBehaviour::test_LIB01_numbers_rejects_off_curve` |
| It **accepts** X = x + p and reduces it to x | `test_LIB02_numbers_accepts_and_reduces_x_ge_p` |
| It **accepts** Y = y + p and reduces it to y | `test_LIB09_numbers_accepts_and_reduces_y_ge_p` |
| `load_der_public_key` accepts a compressed-point P-256 SPKI and a secp256k1 SPKI | `test_LIB03_...` |
| `load_der_public_key` accepts ML-DSA-44 and ML-DSA-87 SPKIs | `test_LIB04_...` |
| ECDSA verify accepts high-S; rejects r or s = 0, = n, and r + n, s + n | `test_LIB05_ecdsa_verify_high_s_and_range` |
| ECDSA verify reduces x(R) mod n (E-10 accepted by a direct call) | `test_LIB10_ecdsa_x_of_R_reduced_mod_n` |
| `MLDSA65PublicKey.from_public_bytes` accepts all-zero 1952 bytes and rejects 1951/1953 | `test_LIB06_mldsa_key_loader` |
| ML-DSA verify rejects R-08..R-14, R-04, R-05 **without** the verifier's gate | `test_LIB07_...` (9 cases) |
| ML-DSA verify with `context=None` equals `context=b''`; a 256-byte context raises `ValueError` | `test_LIB08_...` |

## 6. Mutation sensitivity (2026-10-27)

Each verifier check below was removed in a scratch copy of `tessera_verify`, and the module was run against that copy
(`-k "not lambda_package"`, because the copy has no issuer tree). The unmutated copy: 222 passed, 1 skipped.

| Removed from `codec.py` | Result | Failing tests |
|---|---|---|
| (a) creation-time policy | 5 failed | P-10..P-14 |
| (b) type-16/33 structural policy | 7 failed | P-19..P-25 |
| (c) expiration / unknown-critical policy | 4 failed | P-15..P-18 |
| (d) Y < p | 4 failed | K-36, K-37 (vector and before-constructor) |
| (e) curve equation | 4 failed | before-constructor K-03, K-15, L-03, L-01 |
| X < p | 4 failed | K-04, K-16 (vector and before-constructor) |
| all of `sig_policy` | 20 failed | O-18..O-20, P-10..P-25, B05 |
| r, s range only | 4 failed | O-18..O-20, B05 |
| ML-DSA encoding gate | 7 failed | `TestMLDSAGate` permissive-backend R-08..R-14 |

The mutation script is not kept in the repository. Codex's earlier run, which found (a)–(e) surviving, is in the
review.

## 7. What this evidence does not show

- **ML-DSA exclusive ownership / key substitution.** Not tested (§4).
- **Library hint strictness** is shown only for the three lax-equivalent rewrites plus the count and z cases (LIB07).
  The verifier does not rely on it (`TestMLDSAGate`).
- **Rule-R signatures are hedged.** Rerunning `gen_vectors.py` changes the rule-R bytes, but no expected outcome.
  Rule-O vectors use RFC 6979 deterministic signing (normalized to low-S) and fixed keys.
- **Deployed Lambda.** It is tied by package digest only (§1). No Lambda invocation was run.
- **Precedence.** Bundle precedence is covered only by B01..B08 over the shared `tests/fixtures.py` builder.
  Everything else is function-level. The DNSSEC and release paths are inventoried (§0), not profiled.

## 8. Run record (2026-10-27, verifier venv)

```
$ .venv/bin/python -m pytest -q -rs ../../formal/p3-verification-profile/test_p3_profile.py
SKIPPED [1] ... TESSERA_LAMBDA_ZIP not set: no deployed package supplied to tie to this record
223 passed, 1 skipped
$ .venv/bin/python -m pytest -q          # verifier suite, unchanged
135 passed, 77 subtests passed
```
