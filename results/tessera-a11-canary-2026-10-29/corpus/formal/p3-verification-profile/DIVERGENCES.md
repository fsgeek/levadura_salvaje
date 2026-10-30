# Verifier behaviour against V1-PROFILE: divergences found (2026-10-27)

Reported, not fixed. `service/verifier/tessera_verify` was not edited.

## In P3 scope (issuer receipt and possession signatures, transported and repository keys)

**None found.** Every outcome the vectors exercise matches V1-PROFILE §8, ENC §5.2 and HYBRID-SUPPLEMENT §2–§3:

- codes and their order (codec, then `SIG_POLICY`, then `SIG_INVALID`);
- r = 0 → `SIG_FORMAT` against r ≥ n → `SIG_POLICY`; high-S accepted;
- the rule-O signature policy: creation time, expiration, critical subpackets, type-16/33 structure, unhashed area
  ignored;
- the rule-R lengths, and hint and z malformation → `SIG_INVALID`;
- X and Y range, the curve equation and the representation, all checked by the verifier before the EC constructor
  (shown with a permissive stand-in, PROFILE.md §3);
- x(R) reduced mod n, and a verification-equation result of infinity rejected;
- the exact ML-DSA-65 SPKI;
- a bad repository key → `TRUST_CONFIG_UNAUTHENTICATED`.

"None found" covers only what the vectors in this directory test (PROFILE.md §7 lists what they do not).

## Outside P3 (observed while inventorying; for the owner)

**D1. The TEST release stand-in does not restrict the release key to P-256.** `release_auth.authenticate_test_release`
(`release_auth.py:61-69`) requires `alg == 'ECDSA-P256-SHA256'` but checks the loaded key only with
`isinstance(pub, ec.EllipticCurvePublicKey)`. A release signed by a secp256k1 key, with a matching key file, is
accepted (`test_p3_profile.py::test_OBS_test_release_auth_accepts_non_p256_curve`, passing, i.e. the behaviour is
observed). The library's DER loader accepts any named curve, compressed points included (LIB03). Impact is bounded:

- the path is the `tessera-v1-test-release/1` instrument interface, which V1-PROFILE §15.9 R3 withdraws as a release
  format ("survives only as the section 3.5 instrument interface … which an installed verifier refuses (R4)");
- the signer is identified by the SPKI hash the operator supplies.

It is still a mismatch between the declared alg and the accepted keys. If the interface stays, a curve check (or the
verifier's own `codec.point` on an exact SPKI prefix) would close it.
