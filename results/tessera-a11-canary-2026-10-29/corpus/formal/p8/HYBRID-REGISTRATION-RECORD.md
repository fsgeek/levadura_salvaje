# Branch-registration record (A9.6): REGISTERED 2026-10-16

**Status: REGISTERED 2026-10-16 by the owner instance. A9 was signed by the author at `2ad3489` (2026-10-16 20:44Z).**

- **Branch taken:** HYBRID. Pair id `KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA256`; pure ML-DSA-65, empty context.
- **Supplement:** `formal/p8/HYBRID-SUPPLEMENT-DRAFT.md`, renamed `HYBRID-SUPPLEMENT.md` at registration, SHA-256 6e7e02ffdafe2cbf7182d70adb2abb93cdbecaa7df683d24db50f9549f24ce9c.

- **Baseline:** ENCODING-V1 at A9 signing commit `2ad3489`, SHA-256 d9ea82eb3e893fef865f124a612ecb6784932ea131559d792be8f01e597eb5ec. After the E§5.2 edit (supplement §7, applied 2026-10-16): SHA-256 fe537b1fd68efa51d0a9e6cf29cb8572a9d8ef7906e6a9cf05de035dc446efd0.
- **Specification:** the frozen V1 verification-spec object, hash entered at the 30 Oct freeze (the supplement's §9).
- **Pass-condition evidence (A9.6), all by 2026-10-14, ahead of 21 Oct:**
  1. Pair id with mode and context: supplement §1–2.
  2. Mixed pairing through R-3.12 and P3: supplement §5; `formal/suite/s-p3/proverif/hybrid/` (H1 holds; H2–H4
     red as predicted).
  3. Real KMS ML-DSA-65 over a genuine V1 frame, external μ above 4 KB, verifying offline in two implementations:
     `formal/p8/evidence/v1-hybrid-2026-10-14/` (A/B 27/27; cryptography plus dilithium-py).
  4. Real P-256 from the gpg slot as deployed: `prototype/policy-signer/EVIDENCE.md` (Cloud Run job through the
     queue; refusals for ε, tag and key_fp; access boundary).
  5. Full selected byte profile specified and tested: hybrid vectors 35 golden / 63 reject, codec agreement, fuzz
     90,400 cases with 0 disagreements; profile-conformance cases (a)–(e) plus hybrid positive and negative cases;
     independent verifier and conformance suite 342/342 (`prototype/differential/results-run5.json`).
- **Reviews:** `docs/reviews/hybrid-supplement/` (CODEX-REVIEW HS-01…06, applied; DECISIONS).
