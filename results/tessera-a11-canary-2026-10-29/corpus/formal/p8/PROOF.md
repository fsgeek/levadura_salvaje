# P8 for `tessera-v1-strict`: injectivity, boundary-unambiguity, type separation

> **STATUS: DRAFT, 2026-10-09; revised 2026-10-12 and 2026-10-19 (see CHANGELOG).** Owner instance (Claude Opus 5.5). This is a
> rigorous prose proof, the A1 §A1.4 option "rigorous prose proof plus the golden-vector and rejection suites". It
> covers the encoding in `ENCODING-V1.md` (cited as **E§n**) and V1 only. It is not machine-checked. The evidence
> that goes with it is in `vectors/` (§5). Its time-boxed falsification pass (V1-DERIVATION §5, step 2) ran
> 2026-10-19 (`docs/reviews/p8-falsification/`, `prototype/p8-falsify/REPORT.md`): **SURVIVED WITH GAPS**. No
> encoding collision or accepted-decode disagreement was found. The gaps were P8F-01 (Lemma 9 overclaimed), P8F-02
> to P8F-04 (implementation B outside the stated domain and codes) and the text defects P8F-05 to P8F-07; all are
> now repaired (`docs/reviews/p8-falsification/DISPOSITION.md`). This records no author acceptance.

**CHANGELOG**

- **2026-10-19 (profile review, `docs/reviews/profile-2026-10-19/`).** Tagged `[OWNER 2026-10-19, PR-nn]` in
  place. No lemma, theorem part (a)–(c), vector or code changes.
  - **NARROW-CLAIM (PR-01).** Theorem (iv)(d)'s time relations are to mining of the selected inclusion block, not to
    T: T is that block's header time, not a UTC upper bound (A10.1; A10 rows 5–9). A UTC statement is separate and
    conditional on A-UTC (A10.1.1). The old "after T" sentence was false in UTC for a backward-skewed header.
  - CORRECT (PR-13): the exponent-repair justification's connective ("finite or nonzero" → "finite, nonzero").
- **2026-10-19 (P8 falsification repairs).** Source: `prototype/p8-falsify/REPORT.md`; disposition
  `docs/reviews/p8-falsification/DISPOSITION.md`. Tagged `[OWNER 2026-10-19, P8F-nn]` in place.
  - **NARROW-CLAIM (P8F-01).** Lemma 9 no longer infers `F' = F` from one signature packet verifying over both. The
    review built two distinct accepted frames, with distinct SHA-256 digests, over which one rule-O packet verifies
    under one chosen P-256 key; collision resistance does not exclude this. Lemma 9 now states only the valid
    byte-split: `F ‖ T` determines `F` and `T`. It no longer uses (H), so §2's (H) bullet drops it. Remark 10 keeps
    its byte disjointness and no longer concludes that a reused key's signature cannot be read over a foreign
    document; that is a signature-scheme property, not P8's (§4 "What is not claimed"). No theorem part changes:
    (ii) used only the byte split, and (iv) never used Lemma 9.
  - CORRECT (P8F-05): Lemma 9's trailer is `12 + h` bytes and its final u32 is `6 + h`.
  - CORRECT (P8F-06): Lemma 4's final coverage clause is replaced by the common-extent statement.
  - Implementations B and A repaired (P8F-02 oversized exponents, P8F-03 first-failing-category order, P8F-04
    standalone payload cap); regression tests in `vectors/test_check.py` and `prototype/indep-verifier/tests/test_parsers.py`.
    No vector, reason code or count changes. §5 records the reruns.
- **2026-10-19 (owner wording edits; no lemma changes).** Source: V1-PROFILE §14.2 item 9 (G38) and
  `docs/reviews/levadura-contradictions/DISPOSITION.md`. §6's "Number rule D-1 is not registered yet" bullet is
  replaced: A9.8 registers it. §6's rule-R bullet is annotated as superseded for the hybrid branch by
  HYBRID-SUPPLEMENT §8 and kept as baseline text, as the supplement directs. ENCODING-V1's 2026-10-19 edits are
  wording only and change no set in §1, so no lemma, theorem part or vector count changes. Tagged
  `[OWNER 2026-10-19]` in place.
- **2026-10-12: signature-inclusive receipt anchor.** Source: `docs/reviews/anchor-signatures/CODEX-REVIEW.md`
  findings 4, 5, 6, 9 and 10 (`DISPOSITION.md`). The domain is extended to exact signatures (§1: `Sig`, `Anc`,
  accepted receipts).
  - New Lemma 7a (signature slots).
  - Lemma 7 now recovers ordered (frame, signature) tuples.
  - Theorem (i), (iii) and (iv) are revised. (iv) keeps codec injectivity, digest binding, unforgeability and
    temporal composition as four separate statements (finding 10).
  - Remark 10's byte range is updated.
  - §5's evidence, counts and results are rerun.
- **2026-10-12 (follow-up): issuance window in the key-publication record.**
  - Lemma 11's summary now covers the two RFC 3339 UTC window fields and `DNS_WINDOW`. The grammar is still a
    fixed-order regular language, so the argument is unchanged.
  - The C4 window rule (`ISSUANCE_WINDOW`, E§7.1) is a verifier comparison, not an encoding property. It is
    vector-tested, not proved here.
  - §5's counts are rerun.
- **2026-10-12 (Amendment 9 review disposition): single window of at most 90 days.** E§7 makes
  `issuance-not-before` mandatory and adds `DNS_WINDOW_LENGTH` (not-after − not-before > 90 days). The record is
  still a fixed-order regular language (now with one field order and one length, 255 bytes), so Lemma 11's
  argument is unchanged; its summary and §5's table and counts are updated. No other lemma is affected: the window
  is outside the frame domain.
- 2026-10-09: first draft.

**What P8 says** (A1 §A1.2): `canonical()` is injective on its accepted payload domain; the encoding is
boundary-unambiguous; anything outside the domain is rejected, never normalized. A7 §A7.9 adds: the two
signer-specific frames bind common attested content, and an encoding map places every binding in bytes (E§0). P7
adds: no object of one type is accepted as another.

---

## 1. The accepted domain, exactly

Let **V** be the set of JSON values in E§1.1:
- `null`, `true` and `false`;
- finite binary64 numbers other than −0;
- strings of Unicode scalar values that contain no noncharacter, no code point unassigned in Unicode 16.0.0, and are
  in NFC;
- arrays;
- objects with pairwise distinct names.

Two values are **equal** when they are equal as mathematical structures:
- numbers are equal as doubles;
- strings are equal as scalar sequences;
- arrays are equal as sequences;
- objects are equal as finite maps from names to values. Member order is not part of an object.

That is the sense in which injectivity is claimed. Two JSON *texts* that differ only in spelling denote one value,
and E§1.2 says why that is intended.

The accepted sets are:

- **Payloads.** For a tag `t`, `Pay(t) = { JCS(v) : v ∈ V, Schema_t(v), depth(v) ≤ 64, |JCS(v)| ≤ 2^24 }`. Here
  `Schema_attest` is E§3.2 together with E§3.3, and `Schema_manifest` is E§4.
- **Frames.** `Frm(t) = { frame(t, p) : p ∈ Pay(t) }` for `t ∈ {attest, manifest}`, where
  `frame(t, p) = [|t|] ‖ t ‖ 00 01 ‖ u32(|p|) ‖ p`.
- **Signature slots.** For an algorithm id `a` and a slot `i ∈ {0 (kms), 1 (gpg)}`, `Sig(a, i)` is the set of
  byte strings accepted by the E§5.2 rule for `(a, i)`. It is always a set of **nonempty** strings of length at
  most `cap(a, i)`.
  - Rule O: exactly one legacy-header v4 signature packet, with every inner length consumed exactly.
  - Rule R: the strings of the parameter set's exact signature length.
  - Opaque: every string of 1 to 65536 bytes.
- **Anchor preimages.** `Anc = { A(F0, S0, F1, S1) : F_i ∈ Frm(attest), S_i ∈ Sig(alg(F_i), i) }`, where `alg(F)`
  is the `common.alg` of `F`'s payload and
  `A(F0, S0, F1, S1) = [29] ‖ "tessera-v1/receipt-anchor-sig" ‖ 02 ‖ u32|F0| ‖ F0 ‖ u32|S0| ‖ S0 ‖ u32|F1| ‖ F1 ‖ u32|S1| ‖ S1`.
  The withdrawn frame-only construction (tag `tessera-v1/receipt-anchor`) is not in the domain. Its tag is not in
  T.
- **Snapshot preimages.** `Snp = { S(s) : 1 ≤ |s| ≤ 2^24 }`, where `S(s) = [26] ‖ "tessera-v1/dnssec-snapshot" ‖ u32|s| ‖ s`.
- **Receipts.** A tuple `(F_M, F_0, S_0, F_1, S_1, A)` is an *accepted receipt* (codec level) when all of the
  following hold:
  - `F_M ∈ Frm(manifest)` decodes to a manifest `M`;
  - `F_0` and `F_1` are in `Frm(attest)` and decode to `(C_0, fp_0)` and `(C_1, fp_1)`;
  - `fp_0 = M.key_fp` and `fp_1 = M.sset[0]`;
  - `JCS(C_0) = JCS(C_1)`;
  - `C_0.manifest_sha256 = hex(SHA256(F_M))`, and `C_0.issuer` and `C_0.alg` equal those of `M`;
  - `S_i ∈ Sig(C_0.alg, i)` and `A = A(F_0, S_0, F_1, S_1)`.

  The receipt's structure is `(M, C, S_kms, S_gpg)`. It is **not** a function of `(M, C)` alone. The signer's
  choices are inside `S`: the nonce, the creation time and the unhashed area. So one `(M, C)` has many accepted
  receipts, and P8 claims nothing about which one an issuer produces.

The decoders in E§1.4, E§3.1, E§4, E§5 and E§6 accept exactly these sets and reject everything else with the
stated codes. Lemma 3 shows this for payloads, and Lemmas 5–8 (with 7a) for the rest.

## 2. Assumptions

- **(N) Number formatting.** For every finite double `d`, `ES(d)` (ECMA-262 Number::toString, used by RFC 8785
  §3.2.2.3) is a decimal literal whose round-half-even nearest double is `d`. Decimal-to-double conversion is
  correctly rounded (IEEE 754). The ECMAScript specification requires both. The implementations rely on them
  through `rfc8785` (A) and through `repr` and `float` (B).
- **(H) SHA-256 collision resistance.** This is used **only** in Theorem part (iv), for the
  hash-carried bindings and the anchor digest, which since 2026-10-12 also carries the exact signatures. Parts
  (i)–(iii) are unconditional.
  - **SHA-256 is the only hash function V1's encoding relies on.** Both fingerprint slots are SHA-256: of the SPKI
    for kms, and of the OpenPGP v4 key-packet body for gpg.
  - The git channel's object linkage is SHA-1, but that belongs to C4's dependency manifest, not P8 (E§7.2).
  - An OpenPGP signature as GnuPG emits it carries OpenPGP's own SHA-1 issuer fingerprint in a subpacket. Those
    bytes are committed in `A_sig` like the rest, but no V1 check reads them.
- **(U) Unicode 16.0.0 tables.** These define V's string conditions. They bear on what is accepted, never on
  injectivity.
- **(K) Key use.** Each V1 slot key signs only V1 tagged strings, as OpenPGP type-0x00 documents. The repository
  key and the DNSSEC keys are other keys. This is used only in Remark 10.

P8 assumes nothing about whether signatures can be forged. That is P1 and P3. Nor does P8 assume anything about
time: what an OTS proof establishes about when `SHA256(A_sig)` existed belongs to C5 and its chain-time
residuals. Theorem (iv) states how the three compose, and keeps them apart.

---

## 3. Lemmas

**Lemma 1 (strings).** Let `E(s)` be RFC 8785's escaping of a string `s` of scalar values (E§1.3), and let `Dec`
be RFC 8259 string decoding, which pairs surrogate escapes. Then for every string `s` in V, decoding
`"` E(s) `"` returns exactly `s`, consumes exactly those bytes, and stops at the closing quote.

*Proof.* `E` maps each scalar `c` on its own:
- `"` becomes `\"`;
- `\` becomes `\\`;
- a control character `c < 0x20` becomes its two-character escape where RFC 8785 defines one, and `\u00xx`
  otherwise;
- every other `c` becomes its UTF-8 encoding, which is defined because `s` contains no surrogates.

None of the outputs contains an unescaped `"`. Every output that starts with `\` is a complete escape that `Dec`
maps back to `c`. Every other output is a raw scalar `≥ 0x20`, other than `"` and `\`, which `Dec` copies.

UTF-8 is prefix-free, so the concatenation splits uniquely into these units. The first unescaped `"` is therefore
the closing quote. ∎

**Lemma 2 (numbers).** Let `d` be a finite double other than −0. Then:
- (a) `ES(d)` matches the RFC 8259 number grammar;
- (b) parsing `ES(d)` gives `d`;
- (c) `ES(d)` passes the value-preserving rule E§1.2;
- (d) in `JCS(v)`, `ES(d)` is followed by `,`, `]`, `}` or the end of input.

*Proof.*
- (a) `ES` produces only the forms `digits`, `digits.digits`, `0.0…digits` and `d[.ddd]e±n`, with an optional
  leading `-`. Integer parts have no leading zero, except the single `0` of `0.`. All of these are grammatical.
- (b) This is (N).
- (c) Rule 1: `ES(d)` is never a negative zero, because `d ≠ −0` and `ES(+0) = "0"`. Rule 2: the nearest double
  to `ES(d)` is `d` by (b), which is finite. Rule 3: `ES(d)` is the literal being tested, so its value equals the
  value of `ES` of its nearest double, which is `ES(d)` again.
- (d) JCS puts a number only before a separator or a closing bracket, or at the end of the text. None of those can
  extend a number token, so a maximal-munch number scan over `JCS(v)` stops exactly at the end of `ES(d)`. ∎

**Lemma 3 (canonical payload; P8's injectivity of `canonical()`).** For every `v ∈ V`, the strict parser applied
to `JCS(v)` consumes exactly `JCS(v)` and returns `v`. Hence:
- (a) `JCS` is injective on V;
- (b) a byte string `b` passes `payload()` (E§1.4) if and only if `b = JCS(v)` for some `v ∈ V` within the limits,
  and then `payload(b) = v`.

*Proof.* By induction on `v`.
- Literals are immediate.
- Numbers follow from Lemma 2(b) and (d).
- Strings follow from Lemma 1.
- **Arrays.** `JCS([v1…vn]) = "[" JCS(v1) "," … "," JCS(vn) "]"`. By the induction hypothesis, each `JCS(vi)` is
  parsed to `vi` and consumed exactly. The next byte is then `,` or `]`, and the RFC 8259 grammar is LL(1) on
  that byte, so the element boundaries are forced.
- **Objects.** The same argument applies to `"{" JCS(k1) ":" JCS(u1) "," … "}"`. The parser returns the member
  list `[(k1,u1)…]`. Its names are distinct because `v` is an object in V, so it denotes the map `v`.

For (a): if `JCS(v) = JCS(w)`, then `v = parse(JCS(v)) = parse(JCS(w)) = w`.

For (b), the "if" direction. Parsing `JCS(v)` succeeds by the argument above. Its UTF-8 is valid by Lemma 1.
Every check in E§1.4 passes:
- depth: the parse is `v`, and `v` is within the limits;
- names: `v`'s names are distinct;
- strings: `v`'s strings are in V;
- numbers: every literal in `JCS(v)` is some `ES(d)`, which passes by Lemma 2(c);
- canonical: `JCS(parse(b)) = JCS(v) = b`.

For (b), the "only if" direction. If `payload(b)` succeeds with value `v`, then the checks put `v` in V within the
limits, and the final check gives `b = JCS(v)`. ∎

*Remark (no normalization at the verifier).* By Lemma 3(b), the verifier's accepted payload set is exactly the
image `JCS(V)`. A byte string that is not canonical, such as `9.80`, `1E2`, `A`, extra whitespace or
reordered members, is rejected (XF-23 to XF-30). It is not repaired. Normalization happens only at the issuer's
`ingest`, and there by Lemma 2 and E§1.2 it changes spellings and never values.

**Lemma 4 (headers are prefix-free; tag separation).** Let `T` be the four tags of E§2, and
`header(t) = [|t|] ‖ t`. For distinct `t, t' ∈ T`, no byte string begins with both `header(t)` and `header(t')`.

*Proof.* If `|t| ≠ |t'|`, the two headers differ in byte 0. If `|t| = |t'|`, then `t ≠ t'` differ at some
position `j < |t|`, so the headers differ in byte `1 + j`. Either way the difference falls at a position both
headers cover (byte 0, or byte `1 + j < 1 + |t| = 1 + |t'|`). ∎ [OWNER 2026-10-19, P8F-06] *(Was: "within the
first `1 + max(|t|, |t'|)` bytes, which both headers cover"; headers of unequal length do not both cover that.)*

So the tag is read first (a length byte, then that many bytes), before any other field is interpreted. The decoder
compares it with the expected construction and rejects a mismatch (`TAG_MISMATCH`) or a tag outside T
(`TAG_UNKNOWN`).

**Lemma 5 (frame codec; boundary-unambiguity).**
- For `t ∈ {attest, manifest}` and `p ∈ Pay(t)`: `decode_frame(frame(t, p), t) = parse(p)`.
- For every `b` that `decode_frame(·, t)` accepts: `b = frame(t, JCS(decode_frame(b, t)))`.

So `frame(t, ·)` is a bijection from `Pay(t)`, and through Lemma 3 from the schema-valid part of V, onto `Frm(t)`.

*Proof (boundary-unambiguity).* Every field's start and end are fixed by the bytes before it:

| Field | Bytes | Fixed by |
|---|---|---|
| tag length | [0, 1) | position |
| tag | [1, 1+n) | byte 0 |
| canonicalization version | [1+n, 3+n) | n |
| length L | [3+n, 7+n) | n |
| payload | [7+n, 7+n+L) | n and L |
| end of input | at exactly 7+n+L | n and L; otherwise `TRUNCATED` or `TRAILING` |

No boundary depends on the contents of a later field. In particular, the payload's own JSON structure never
decides where the frame ends; the length does, which is A1 P8's "a parser cannot disagree about where the payload
ends". The fields are then checked in order: tag in T and equal to `t` (Lemma 4); version equal to `0x0001`;
`L ≤ 2^24`; payload in `Pay(t)` (Lemma 3(b) plus the schema).

For the first identity: given `frame(t, p)`, the decoder reads `n = |t|`, the tag `t`, `0x0001` and `L = |p|`. It
finds exactly `L` bytes left, and those bytes are `p`. Then Lemma 3(b) applies.

For the second identity: if `b` is accepted, every field equals the corresponding field of
`frame(t, JCS(parse(payload)))`: the tag was checked to be `t`, the version is `0x0001`, `L` is the actual
remainder, and Lemma 3(b) gives `payload = JCS(parse(payload))`. ∎

**Lemma 6 (the two signer frames).** Let `(F_M, F_0, S_0, F_1, S_1, A)` be an accepted receipt with common value `C`. Then:
- (a) **Common content is byte-identical.** `JCS(C)` occupies bytes `[34, 34 + |JCS(C)|)` of both `F_0` and `F_1`.
  This is A5 §A5.4 / R-3.12's "payload equal across signer slots", as a statement about bytes.
- (b) **The frames are distinct.** `F_0 ≠ F_1`.
- (c) **Each frame's slot is a function of its bytes, and the slots are disjoint.** Under E§3.3, the attestation
  frames whose `key_fp` starts `spki-sha256:` and those whose `key_fp` starts `gpg-sha256:` are disjoint sets. A
  frame accepted in slot `kms` is never accepted in slot `gpg`, and the reverse.

*Proof.*
- (a) `Schema_attest` fixes the payload's names to `common` and `signer`, and `"common" < "signer"` in UTF-16 order.
  So JCS writes `{"common":` (10 bytes) at payload offset 0, followed by `JCS(C)`. The payload starts at frame
  offset 24 (1 + 17 + 2 + 4). Both frames carry the same `C`, because the receipt condition is
  `JCS(C_0) = JCS(C_1)`, which by Lemma 3(a) is the same as `C_0 = C_1`.
- (b) The manifest schema forces `fp_0` to have the prefix `spki-sha256:` and `fp_1` the prefix `gpg-sha256:`.
  These differ in their first character, so the two payload values differ, so the payloads differ by Lemma 3(a),
  so the frames differ by Lemma 5.
- (c) The prefix is part of the frame's bytes, and the receipt condition ties slot `kms` to `M.key_fp` and slot
  `gpg` to `M.sset[0]`, which have different prefixes.

A swapped presentation fails `RECEIPT_SLOT`. So does the same frame presented twice (XR-01, XR-02). A splice that
changes `C` in one slot fails `RECEIPT_COMMON_MISMATCH` (XR-03). ∎

*Why the two frames share one tag.* A5 §A5.4 registers that object type is one of the six fields that are equal
across slots. So separation between the two signers' frames is done by the fingerprint slot and the manifest's
slot order, not by the tag. Lemma 6(c) is that separation.

**Lemma 7a (signature slots).** For every `(a, i)`, the slot decoder accepts a byte string `s` of declared slot
length `n` if and only if `s ∈ Sig(a, i)` and `|s| = n`. When it accepts, it returns `s` itself. The signature's
end is fixed twice, and the two must agree:
- by the slot's `u32` length;
- by the signature's own extent: rule O's packet header, rule R's fixed length, or, for opaque, the slot length.

*Proof.*
- The slot length `n` is read first.
  - `n = 0` gives `SIG_EMPTY`.
  - `n > cap(a, i)` gives `LENGTH_CAP`.
  - Otherwise exactly `n` bytes are taken.
- **Rule O.** Byte 0 must be `0x88` or `0x89`. It fixes the width of the length field (1 or 2 bytes), and the
  shortest-form condition makes that width a function of the body length `m`. So the header is
  `h ∈ {2, 3}` bytes, and the packet ends at `h + m`.
  - `h + m < n` gives `TRAILING`. This includes a second packet.
  - `h + m > n` gives `TRUNCATED`.
  - Inside the body, every field's extent is fixed by bytes before it: four fixed bytes; `u16` and the hashed
    area; `u16` and the unhashed area; two bytes; and then each MPI's `u16` bit count with ⌈bits/8⌉ bytes.
  - Each subpacket area must be consumed exactly by subpackets whose lengths are in shortest form. The body must
    end exactly after the second MPI.
  - Anything else gives `SIG_FORMAT`.
  - So the accepted set is exactly rule O's, and no accepted string has a proper prefix or extension that is also
    accepted at the same slot length.
- **Rule R.** The accepted strings are those of the exact parameter-set length.
- **Opaque.** The accepted strings are those of the slot length.

In every case the decoder returns the bytes it took, unchanged. It normalizes nothing: no re-framing, no low-s,
no subpacket edits. ∎

*Remark.* The decoder returns `s` unchanged, so the codec is injective on signatures trivially. What Lemma 7a
adds is that a signature's boundaries are unambiguous, and that the accepted set is pinned. That second fact keeps
an encoder from choosing among serializations, and it makes two verifiers agree on rejection.

**Lemma 7 (anchor preimage; revised 2026-10-12).** `A(·,·,·,·)` is injective on ordered tuples
`(F0, S0, F1, S1)` with `F_i ∈ Frm(attest)` and `S_i ∈ Sig(alg(F_i), i)`, and
`decode_anchor(A(F0, S0, F1, S1)) = ((F0, S0), (F1, S1))`. Every byte string that `decode_anchor` accepts equals
`A` of its decoded tuple. In particular, `A` of a tuple differs from `A` of any other tuple. That covers each of
these changes:
- the slots swapped;
- the signatures swapped between slots;
- any signature byte replaced;
- one valid signature over a frame replaced by another valid signature over the same frame.

*Proof.* The header comes first (Lemma 4). Then come the fixed count byte `02`, and for each slot `i` in order:
1. the length `u32 L_i`, then exactly `L_i` bytes, decoded as a whole frame (Lemma 5). That decode determines
   `alg(F_i)`;
2. the length `u32 M_i`, then exactly `M_i` bytes, decoded by the rule for `(alg(F_i), i)` (Lemma 7a).

Then the end of input. Each boundary is fixed by bytes already read. The choice of signature rule depends only on
the frame just decoded and the slot position, both already read. No later byte influences an earlier boundary or
rule. So the decoder is a left inverse of `A` on the domain, and `A` is injective. Conversely, an accepted string
is rebuilt exactly by `A` from its decoded tuple, since each field is copied verbatim and each length prefix is
the length of the field after it. ∎

*Corollary (no fallback).* The withdrawn frame-only preimage begins with `header("tessera-v1/receipt-anchor")`.
That tag is not in T, so the decoder rejects it at its header (Lemma 4, `TAG_UNKNOWN`), before any length is read
(XA-09, XR-09).

**Lemma 8 (snapshot preimage).** `S(·)` is a bijection from snapshot bodies of 1 to 2^24 bytes onto `Snp`. The
proof is Lemma 5's with an opaque body.

**Lemma 9 (the OpenPGP hash input splits uniquely; narrowed 2026-10-19, P8F-01).** For a v4 OpenPGP signature of
type 0x00 over document `F`, the hashed input is `F ‖ T`, where `T = 04 00 pa ha ‖ u16 h ‖ sub ‖ 04 FF ‖ u32(6 + h)`
(E§3.5) and `|sub| = h`. The map `(F, T) ↦ F ‖ T` is injective over valid trailers: if `F ‖ T = F' ‖ T'` for valid
trailers `T` and `T'`, then `F = F'` and `T = T'`. In particular, for the trailer `T` that a signature packet fixes,
`F ‖ T = F' ‖ T` implies `F = F'`.

*Proof.* A valid trailer ends with `u32(6 + h)`, where `6 + h` is the length of its hashed header `04 00 pa ha ‖ u16
h ‖ sub`. The whole trailer is that header, the two bytes `04 FF` and the four length bytes, so `|T| = 12 + h`:
the final u32 plus six. Two decompositions `F ‖ T = F' ‖ T'` share their last four bytes, so `6 + h = 6 + h'` and
`|T| = |T'|`. Both trailers are then the same-length suffix of one string, so `T = T'` and `F = F'`. (Corrected
2026-10-19, P8F-05: the final u32 is the hashed-header length, not the trailer's own length; the split is the
final u32 plus six.)

Type 0x01 is excluded because text mode rewrites line-ending bytes, and those bytes occur in frame headers and
lengths. ∎

*What Lemma 9 does not say (NARROW-CLAIM, P8F-01).* Until 2026-10-19 this lemma also claimed that if one signature
packet verifies for `F` and for `F'`, then under (H) `F' = F`. That does not follow: verification does not
establish that the two hashes are equal. The falsification review built two distinct accepted attestation frames
whose SHA-256 digests of `F ‖ T` differ (agreeing only in OpenPGP's left 16 bits) and one rule-O packet that
verifies over both under one chosen P-256 key (`prototype/p8-falsify/lemma9-witness.json`). Whether one signature
can verify over two different documents is a property of the signature scheme and of how the key was generated
(P1, P3), not of the encoding. P8 does not claim it. Theorem (ii) uses only the split above; Theorem (iv) never
used Lemma 9, and (iv)(c) already leaves verification to P1 and P3.

**Remark 10 (no confusion with foreign formats).** Every V1 tagged string begins with a byte in 0x11–0x1d, which
is below 0x20. Each of the following begins with a printable byte:
- a git commit object (`tree …`, 0x74);
- a TXT value of E§7 (`v=`, 0x76);
- RFC 8785 text (`{`, `[`, `"`, a digit, `-`, `t`, `f` or `n`).

So no V1 tagged string is byte-equal to any of them: a V1 signed document is never also a commit, a DNS value or
RFC 8785 text. (K) keeps the slot keys off those formats. [OWNER 2026-10-19, P8F-01, NARROW-CLAIM] *(Was: "With (K)
this is not needed, but it means that a key reused by mistake still could not have one of its V1 signatures read as
a signature over a commit or a DNS value, or the reverse." Different documents do not by themselves prevent one
signature from verifying over both; that is a signature-scheme property (Lemma 9's note), not P8's.)*

**Lemma 11 (DNS record).** The unambiguity of the E§7 record is argued in E§7 itself, because it lies outside the
frame domain. In summary:
- the accepted values form a fixed-order regular language over alphabets that exclude the separators, so parsing
  inverts encoding;
  - this includes, since 2026-10-12, the mandatory `issuance-not-before` and `issuance-not-after` (the first was
    optional until the Amendment 9 disposition), whose values are `YYYY-MM-DDThh:mm:ssZ`, one spelling per instant;
  - `DNS_WINDOW` (not-after ≤ not-before) and `DNS_WINDOW_LENGTH` (not-after − not-before > 90 days) are checks on
    parsed values and play no part in the split;
- one RR with one character-string removes concatenation choices;
- the owner name is compared as a sequence of labels, without regard to ASCII case.

---

## 4. Theorem (P8 for `tessera-v1-strict`)

Let the accepted sets be as in §1.

- **(i) Injectivity.** These maps are injective:
  - `canonical = JCS` on V;
  - `frame(t, ·)` on `Pay(t)`, and so `v ↦ frame(t, JCS(v))` on the schema-valid values;
  - `A` on ordered (frame, signature) tuples `(F_kms, S_kms, F_gpg, S_gpg)` (Lemmas 7, 7a);
  - `S` on snapshot bodies.

  Each decoder is the exact inverse of its encoder on the accepted set: `Dec ∘ Enc = id` on accepted structures,
  and `Enc ∘ Dec = id` on accepted bytes. *(Lemmas 3, 5, 7, 7a, 8.)*

  So the map from an accepted receipt's structure `(M, C, S_kms, S_gpg)` to `(F_M, F_kms, F_gpg, A_sig)` is
  injective outright:
  - `F_M` determines `M`;
  - `F_kms` determines `C`;
  - `A_sig` determines `S_kms` and `S_gpg`, byte for byte.

  The receipt is not determined by `(M, C)` alone (§1).

- **(ii) Boundary-unambiguity.** In every accepted byte string, each field's extent is a function of the bytes
  before it. The end of input is required to fall exactly where the last length prefix says. The JSON payload is
  delimited by the frame's length, never by its own syntax. A signature's extent is fixed by its slot length, and
  it must agree with the signature's own extent. *(Lemmas 5, 7, 7a, 8; Lemma 9 for the split of the OpenPGP hash
  input into frame and trailer.)*

- **(iii) Type and domain separation.** The accepted sets `Frm(attest)`, `Frm(manifest)`, `Anc` and `Snp` are
  pairwise disjoint (Lemma 4). A decoder for one construction rejects every member of the others (`TAG_MISMATCH`).
  The withdrawn frame-only anchor layout is rejected by every decoder (`TAG_UNKNOWN`; Lemma 7's corollary).

  Inside `Frm(attest)`, the `kms` and `gpg` slot frames are disjoint, each frame's slot is fixed by its own bytes,
  and an accepted receipt's two frames are distinct and byte-identical on `JCS(C)` (Lemma 6).

  The DNS value and foreign formats are disjoint from all of these (Remark 10).

- **(iv) Computational binding, under (H)** *(revised 2026-10-12)*. Each of the following binds only under SHA-256
  collision resistance.
  - A frame's signed bytes determine the manifest frame, the specification, the conformance vectors and the
    preamble, through their SHA-256 values.
  - The OTS-stamped digest `SHA256(A_sig)` determines the ordered tuple `((F_kms, S_kms), (F_gpg, S_gpg))`,
    through Lemma 7: the frames **and the exact signature bytes**, in slot order.

  So two different such objects bound by one accepted frame or anchor digest yield a SHA-256 collision. This is
  the only place P8 for V1 rests on a cryptographic assumption.

  **Four statements, kept apart** (finding 10). P8 proves (a) and (b). (c) and (d) are not P8's, and P8 does not
  claim them.
  - **(a) Codec injectivity** (unconditional). `A_sig` decodes to exactly one tuple and is re-encoded from it
    (Lemma 7). A different signature byte string, even a valid one over the same frame, gives a different
    preimage.
  - **(b) Digest binding** (under (H)). A digest determines that tuple. A second tuple with the same digest is a
    SHA-256 collision.
  - **(c) Unforgeability** (P1 and P3, not P8). Whether `S` verifies over `F` under the slot key is a separate
    check. It is made on the committed bytes (E§5.3). Whether a verifying `S` was produced by the key holder
    rests on the signature scheme's security and on key custody.
  - **(d) Temporal composition** (C5, not P8). Suppose valid OTS and Bitcoin evidence shows that
    `SHA256(A_sig)` existed before the selected Bitcoin inclusion block was mined. Then by (b), the exact bytes
    `S_kms` and `S_gpg` existed before that block was mined, under that evidence's own chain-order residuals. Its
    header time T is not a UTC upper bound (A10.1); any UTC statement is separate and conditional on A-UTC
    (A10.1.1), and P8 makes none. [OWNER 2026-10-19, PR-01, NARROW-CLAIM]
    - Hence a signature first produced after that block was mined, for example once a key is stolen or the
      algorithm broken, cannot be substituted into this receipt while (H) and the temporal evidence hold.
    - It does **not** follow that the signatures were produced honestly before that block was mined. That needs
      the historical signing, custody and authority assumptions of CODEX-REVIEW findings 7 and 8, which V1 reports
      as not evaluated.
    - *(Was: "existed by time T", "existed by T", "first produced after T", "produced honestly before T"; a
      signature made after a backward-skewed header's nominal UTC time, but before mining, can fit the anchor,
      A10:248-249.)*

∎ (from the lemmas)

**What is not claimed.** P8 does not claim any of the following:
- that signatures are unforgeable, or that keys are bound to identities (P1, P3);
- that a signature verifying over one document cannot also verify over another (Lemma 9's note; P1, P3)
  [OWNER 2026-10-19, P8F-01];
- that a stamp's time bound makes signing honest (iv)(d);
- that the values have any meaning (A3 §A3.1);
- that any value outside V is accepted. It is rejected with the code its first failing check names.

---

## 5. Evidence: the vectors, and the two-implementation check

`vectors/gen.py` is implementation A: standard library plus `rfc8785` 0.1.4 for serialization. `vectors/check.py`
is implementation B: standard library only, with its own UTF-8 decoder, JSON parser, ECMAScript number formatter,
JCS serializer and every decoder. Since 2026-10-12, B also has its own OpenPGP signature-packet parser and its
own ECDSA P-256 verifier. The two share no code. They share only Python's Unicode 16.0.0 tables, `float`/`repr`
and `hashlib`'s SHA-256.
- A also uses `hmac` (RFC 6979 nonces, pinned by RFC 6979 A.2.5) and SHA-1, both only to *make* the vector
  signatures.
- SHA-1 fills OpenPGP's issuer-fingerprint subpacket. No check reads it, and B never computes it.

| Lemma | Golden vectors | Rejection vectors |
|---|---|---|
| 1 (strings) | C-04, C-05, C-06 | XC-13 to XC-22, XC-28, XC-29 |
| 2 (numbers) | N-01 to N-22 (RFC 8785 Appendix B), C-03, C-10, C-N01 to C-N22 | XC-03 to XC-12, XC-31 to XC-33, XF-27 |
| 3 (canonical payload) | C-01 to C-09 | XC-01, XC-02, XC-23 to XC-27, XC-30, XF-23 to XF-30, XF-48 |
| 4, 5 (tags, frames) | F-01 to F-03, M-01 | XF-01 to XF-22, XF-31 to XF-47, XF-49 to XF-51 |
| 6 (signer frames) | F-01/F-02, R-01 | XR-01 to XR-05 |
| 7 (anchor) | A-01, A-02, R-01 | XA-01 to XA-10, XA-30, XR-06 to XR-09, XR-15 |
| 7a (signature slots) | SIG-01, SIG-02, A-01, A-02 | XA-11 to XA-29, XA-31, XA-32 |
| (iv)(a) negative controls | R-01 | XR-10 to XR-14: a valid signature that is not the committed one fails the anchor check |
| E§5.3 verification stage (P3, not P8) | R-01 | XR-16 (`SIG_INVALID`), XR-17 (`KEY_MISMATCH`) |
| 8 (snapshot) | S-01 | XS-01 to XS-04 |
| 11 (DNS) | DNS-01 to DNS-03; K-01, K-02 (fingerprints) | XD-01 to XD-33 |
| E§7.1 issuance window (C4 rule, not P8) | W-01 (T = not-after), W-02 (declared = not-before); DNS-02 (window exactly 90 days) | XW-01 (T = not-after + 1 s), XW-02, XW-03; XD-23, XD-24 (`DNS_WINDOW`), XD-25, XD-26 (not-after missing), XD-31 (not-before missing), XD-32 (90 days + 1 s), XD-33 (one year) (`DNS_WINDOW_LENGTH`) |

**Counts:** 71 golden vectors and 173 rejection vectors. On 2026-10-09 they were 66 and 126. The changes:
- golden: SIG-01, SIG-02 and A-02 are added, and so are W-01 and W-02 (the window follow-up);
- rejection: XA-09 to XA-32 and XR-09 to XR-17 are added, and so are XD-23 to XD-30 and XW-01 to XW-03 (the
  window follow-up);
- DNS-01 to DNS-03, XD-03, XD-05, XD-16 and XD-22 are regenerated for the window grammar;
- for the 90-day single window (Amendment 9 disposition): XD-31 to XD-33 are added; DNS-01 to DNS-03, W-01, W-02,
  XW-01 to XW-03 and the XD vectors built on the canonical value are regenerated; XD-30 (fractional seconds) no
  longer fits one character-string and is now `DNS_STRINGS`;
- A-01, R-01 and every vector built from the anchor are regenerated for `A_sig`.

**Golden anchor digests.**
- A-01 = R-01's anchor = `06caaf1a462b150f7f5b4a02691da1216259a5a080ad77dcfe1ffefd16ec64e4`. A-01 is 1932 bytes
  and holds two 119-byte signatures. The frame-only A-01 of 2026-10-09 was `2d1e760f…4771427`.
- A-02 (canary) = `1d9f006cfca4e80eb87bd88eb20944b8dba2e5256ffe996f38f9ab27cfd91583`.

The output is deterministic: RFC 6979 nonces, and regeneration reproduces both files byte for byte.

**Signatures.** The signatures are real ECDSA P-256 signatures in OpenPGP v4 packets.
- The keys are public test keys: d = 1 (G, slot kms) and d = 2 (2G, slot gpg), as in K-01 and K-02.
- The packet layout is the one GnuPG 2.4.4 emits.
- A signs. A and B each verify with their own ECDSA code: A uses affine coordinates and B Jacobian, and each
  builds its own OpenPGP hash input.
- **External cross-check** (2026-10-12, by hand in a scratch GnuPG home, not part of the scripts). GnuPG 2.4.4
  reported "Good signature" for SIG-01, SIG-02 and all five negative-control signatures: XR-10 (a second
  nonce), XR-11 and XR-14 (`(r, n − s)`), XR-12 (an edited unhashed area) and XR-13 (signed five years later).
  It reported "BAD signature" for a gpg-slot signature checked over the kms frame. A signature that GnuPG made
  with its own fresh key also passes rule O.

**Result** (2026-10-12; rerun after the 90-day window change, same day).
- A self-checks every vector. Each negative control is asserted at generation: the presented signature verifies,
  and its anchor digest differs from the stamped one.
- B round-trips all **71/71** golden vectors. That includes re-parsing and re-verifying SIG-01 and SIG-02, and
  verifying both committed signatures of R-01.
- B rejects all **173/173** rejection vectors **with the same reason code as A**.
  - B's window check uses its own days-from-civil arithmetic, not `datetime`.
  - It matched `datetime` on 20,000 random instants (a manual check).
- B independently confirms the **5/5** negative controls: the signature verifies, and the anchor check fails.
- `vectors/fuzz.py` runs 60,000 seeded differential cases, and **there were 0 disagreements** in verdict, reason
  code, canonical bytes or decoded anchor tuples.
  - Stages 1 and 2 (40,000 cases: JSON and frames) are unchanged from 2026-10-09. Their verdict histogram
    reproduces that run exactly.
  - Stage 3 adds 20,000 composite-anchor cases: byte edits biased to the signature slots and length prefixes,
    and structural substitutions, duplications, truncations, re-framings and swaps. Its verdicts: 3858 accepted;
    the rest rejected across 13 reason codes, including `SIG_EMPTY`, `SIG_PACKET`, `SIG_FORMAT`, `LENGTH_CAP`,
    `TRUNCATED` and `TRAILING`.
- *Sensitivity check* (by hand, on scratch copies). Two planted defects in B were each caught by the agreement
  run: accepting a non-minimal `0x89` header (XA-20), and skipping signature verification (XR-16).

**Falsification pass repairs** (2026-10-19, P8F-02 to P8F-04). The review found three places where B did not match
E§1: an uncaught `ValueError` on accepted literals whose exponent exceeds Python's integer digit limit (`0e` and 4301
nines); `JSON_SYNTAX` for a BOM followed by invalid UTF-8, where E§1.4 requires `JSON_ENCODING`; and no size cap in
the standalone `payload_value`. B now clamps exponents of more than 18 significant digits (within the payload-size bound, no
nonzero literal with such an exponent rounds to a finite, nonzero binary64 value; zero-valued literals are handled
separately) [OWNER 2026-10-19, PR-13] *(was: "no nonzero such literal is finite or nonzero as a double, and zero is
decided first")*, decodes UTF-8 before the BOM check, and rejects a
standalone payload above 2^24 bytes with `LENGTH_CAP`. The owner found the same three defects in A and repaired
them the same way; A's old direct-decision bound (|exponent| > 100000) also wrongly rejected value-preserving
literals such as `1` + 200000 zeros + `e-200000`, and now applies only above 18 exponent digits.
`vectors/test_check.py` pins each reproduction for A and B. The rerun after the repair: B 71/71, 173/173 and 5/5
baseline, 35/35, 63/63, 1/1 and 6/6 hybrid; A regenerates all four vector files byte for byte (checked in a
scratch copy); `fuzz.py` 60,000 + 90,400 cases, 0 disagreements. No vector changed.

The fuzz found one real defect in A before the 2026-10-09 vectors were frozen. A raised an uncaught `decimal`
error on literals with exponents beyond about 10^18. A now decides those directly, and XC-31, XC-32 and C-10 pin
the case.

**Reproduce:**

```
uv run --no-project --with rfc8785==0.1.4 python formal/p8/vectors/gen.py
python3 formal/p8/vectors/check.py
uv run --no-project --with rfc8785==0.1.4 python formal/p8/vectors/fuzz.py
```

Python 3.14 is needed, for its Unicode 16.0.0 tables.

## 6. Limits of this evidence

- The proof is prose. A reader checks it lemma by lemma, and nothing has machine-checked it. Lean was judged
  unnecessary: every lemma is a decoder-inverts-encoder argument over a fixed grammar.
- "Two implementations agree" is weaker than independence. Both come from one author instance on one runtime, and
  they share the Unicode tables and float conversion. The V1 build is the registered second encoder (V1-DERIVATION
  §5), and it must reproduce these bytes.
- (N) is assumed, not tested exhaustively. N-01 to N-22 check it against RFC 8785's own Appendix B values.
- The golden fingerprints (K-01 `spki-sha256`, K-02 `gpg-sha256`) use the P-256 points G and 2G, and the spec,
  vector, preamble and snapshot bytes are marked ILLUSTRATIVE. The real values come from the real keys and
  documents at the freeze. The layouts do not change.
- The vector signatures are mathematically real, but their private keys are 1 and 2, so anyone can forge them.
  They show encoding, binding and the negative control. They say nothing about unforgeability, which is (iv)(c)
  and not P8 in any case.
- Rule R (raw FIPS 204/205) has no vectors and is not implemented in either codec, because no PQ id is
  registered. It must get golden and rejection vectors, and an agreement run, when one is. *[OWNER 2026-10-19
  annotation: superseded for the hybrid branch by HYBRID-SUPPLEMENT §8 (registered 2026-10-16): the pair id is
  registered, both codecs implement rule R, and `vectors/hybrid-golden.json` (35) and `vectors/hybrid-reject.json`
  (63) pass the agreement run. The bullet is kept as baseline text, as the supplement directs.]*
- The GnuPG cross-check is a manual record, not a scripted step.
- Number rule D-1 is registered by A9.8 for `tessera-v1-strict` (ENCODING-V1 §9), so Lemma 2(c) is stated against
  the registered rule. [OWNER 2026-10-19, G38] *(Was: "Number rule D-1 is not registered yet … If the author keeps
  the literal rule instead, Lemma 2(c) fails as stated …"; the contingency no longer arises.)*
