# P8 encoding for `tessera-v1-strict` (V1 only)

> **STATUS: DRAFT, 2026-10-09; revised 2026-10-12 and 2026-10-19 (see CHANGELOG).** Owner instance (Claude Opus 5.5). This is the O-79 encoding map and the byte
> layout that P8 (A1 §A1.2) requires "before the Band 1 freeze", **for the V1 profile only**. It changes no
> registered sentence. Where it needs a registered sentence to change, §9 says so. The proof is `PROOF.md`. The
> vectors are `vectors/` (implementation A `gen.py`, implementation B `check.py`, differential `fuzz.py`).
> Every choice carries a one-line reason. G-nn refers to `prototype/GUESSES.md` and `prototype/PHASE3-REPORT.md`,
> and each one is resolved here for V1.

**CHANGELOG**

- **2026-10-19 (profile review PR-01 sweep; no codec rule change).** Source:
  `docs/reviews/profile-2026-10-19/CODEX-REVIEW.md` PR-01 and its disposition. Tagged `[OWNER 2026-10-19, PR-01]`
  in place. No rule, field, length, tag, reason code, reason order, golden byte or vector changes.
  - NARROW-CLAIM: §5's re-stamp sentence ("a new, later time bound") and §7.1's rationale ("the anchor prevents
    claiming an earlier T") are restated in chain order. A later block can carry an earlier header time, so
    neither "later" nor "earlier T" follows (A10.1).
- **2026-10-19 (P8 falsification repairs; no codec rule change).** Source:
  `prototype/p8-falsify/REPORT.md` and `docs/reviews/p8-falsification/DISPOSITION.md`. Tagged `[OWNER 2026-10-19,
  P8F-nn]` in place. No rule, field, length, tag, reason code, reason order, golden byte or vector changes.
  - CORRECT (P8F-05): §3.5's trailer sentence. The final u32 is `6 + hlen`, the hashed-header length; the trailer is
    `12 + hlen` bytes, so it splits off as the final u32 plus six. The citation is PROOF Lemma 9, not Lemma 7.
  - CORRECT (P8F-07): §8's canonicalization-version offset is `1 + len(tag)` (18 for attest, 20 for manifest), not
    "18".
  - CLARIFY (P8F-04): §1.4 states that `payload(bytes)` enforces §1.1's 2^24-byte size limit first, with the code
    the frame's `payload_length` check already gives (`LENGTH_CAP`). Through a frame the outcome is unchanged; the
    standalone helpers in implementations A and B now match.
  - P8F-02 and P8F-03 needed no text change: implementations B and A were repaired to match §1.2 and §1.4.
- **2026-10-19 (owner wording edits; change accounting per V1-PROFILE §1 "Baseline", G37).** Sources: V1-PROFILE
  §14.2 item 9 (G01, G02, G18, G28, G38, r2-contra) and the Levadura contradiction search
  (`docs/reviews/levadura-contradictions/DISPOSITION.md`). Each edit is tagged `[OWNER 2026-10-19]` in place.
  - **No codec change.** No rule, field, length, tag, reason code, reason order, golden byte or vector changes.
    Both codecs and every vector stand as they are; PROOF's lemmas are unaffected.
  - CORRECT: §7.1's window-provenance sentence (G02: no "fixed … before any receipt" claim; chain-order
    pre-commitment and A9 C4's DNSSEC non-claim instead); §7.1's selection sentence ("earliest" → lowest block
    height, A9 C5 and A10.5); §7.2's "that commit adds the assertion blob" (the profile does not check it); §5.3's
    "not registered" (→ not the catalog-supported id); §3.2's "V1 issues" comment (the registered hybrid branch).
  - CLARIFY: §2's header sentence (scoped to slot-key signatures and the two tagged OTS preimages; the git stamped
    message and the TXT value are untagged); §8's "single in-profile UNVERIFIABLE" → codec-level (G01); §3.2 and
    §7 field grammars (G18); §5.2 subpacket length forms (G28); §1.2 and D-1's "needs an author sentence" → A9.8
    registered it (G38). §8's PQ scope bullet is annotated, not edited (HYBRID-SUPPLEMENT: baseline text kept).
  - **Governing text is unchanged.** The baseline is ENCODING-V1 at A9's signing commit `2ad3489` plus the
    registered hybrid supplement (whose §5.2 edit gave SHA-256 `fe537b1f…efd0`). This edited text replaces that
    file only through the freeze record, which names both hashes and this list. Where any sentence here differs
    from A9, A10 or the supplement, they govern.
- **2026-10-12 (Amendment 9 review disposition): a single issuance window of at most 90 days.** Source:
  `docs/reviews/amendment-9/DISPOSITION.md`, Skeptic findings 2, 10 and 12, and Codex finding 2.
  - §7: `issuance-not-before` is now **mandatory** (`DNS_FIELD_MISSING` when absent; XD-31). There is one field
    order. Every canonical value is now exactly 255 bytes.
  - §7: new rejection `DNS_WINDOW_LENGTH` (step 15) when `issuance-not-after − issuance-not-before` exceeds 90 days
    (7 776 000 s). Boundary vectors: DNS-02 is exactly 90 days (accepted), XD-32 is 90 days + 1 s, XD-33 is the
    first draft's one-year window.
  - §7.1: the verifier's lower comparison is no longer conditional. The rationale is restated in chain time
    (Codex finding 2): the guarantee is "no receipt passes with verified T after not-after"; a UTC cutoff needs a
    backward-skew bound V1 does not establish. The issuer's stop margin is an operating number and leaves this
    document (`docs/V1-OPERATIONS-RUNBOOK.md`).
  - Vectors: DNS-01 is now a 30-day window, DNS-02/03 and W-01/W-02 use the 90-day window; XD-05 gains the
    not-before field; XD-04, XD-08, XD-09, XD-20, XD-22 and XD-29 are built on a not-before-less value so that their
    earlier code fires within 255 bytes; XD-30 (fractional seconds) is now 257 bytes and is `DNS_STRINGS`, because it
    cannot be one character-string. Counts: 71 golden, 173 rejection.
  - Also updated: D-12, D-13, D-17, the DNS-02 example, `PROOF.md` Lemma 11 and §5.
- **2026-10-12: signature-inclusive receipt anchor.** Source: `docs/reviews/anchor-signatures/CODEX-REVIEW.md`
  findings 4, 5, 6, 9 and 10, as disposed in `DISPOSITION.md` (owner decision of 2026-10-12).
  - §5: the receipt anchor `A_sig` now commits each slot's exact detached signature, not only its frame. It has a
    new tag, `tessera-v1/receipt-anchor-sig`. The frame-only layout is withdrawn and has no fallback.
  - §5.2 adds signature-slot rules keyed by `(common.alg, slot)`; §5.3 adds the committed-bytes verification rule,
    and §5.4 the issue order (finding 6).
  - Revised along with them: §0 (the encoding map), §2 (the tags), §3.5 (W1 and malleability, finding 5), §8 (the
    identifier rule) and §9 (D-8, D-10 and D-13, plus new D-14 to D-16).
  - §7 adds the git channel's anchor target (finding 9).
  - `PROOF.md` Lemma 7 and Theorem (iv) are revised to match, and so are both codecs and the vectors (finding 10).
- **2026-10-12 (follow-up owner decision): pre-committed issuance window.**
  - The key-publication record (§7) gains `issuance-not-before` (optional) and `issuance-not-after` (mandatory),
    in RFC 3339 UTC. They replace the date-only `not-before`.
  - New codes: `DNS_WINDOW` (the record) and `ISSUANCE_WINDOW` (the C4 verifier rule, §7.1).
  - §7.1 records the rationale and the A2.1 chain-time residual. The git blob carries the same value (§7.2).
  - Also updated: the §0 map, D-13, new D-17, both codecs, and the vectors (DNS-01 to DNS-03, W-01, W-02, XD-16,
    XD-22 to XD-30, XW-01 to XW-03).
- 2026-10-09: first draft.

Notation. `||` is concatenation. `u8`, `u16` and `u32` are unsigned big-endian integers of 1, 2 and 4 bytes. `JCS(v)` is
the RFC 8785 serialization of the JSON value `v`. `SHA256(x)` gives 32 bytes, and `hex(x)` is lowercase hex. All
strings in tags and fixed fields are ASCII.

---

## 0. What V1 encodes, and the encoding map (O-79)

V1 signs, hashes or publishes eight byte strings. Nothing else in the bundle is signed or anchored directly, except
the git channel's stamped message (the signed commit's 40-hex id plus LF, A9.5), through which row 8's git copy is
anchored (§7.2). [OWNER 2026-10-19, Levadura C6]

| # | Byte string | Constructed as | Signed / hashed by | Section |
|---|---|---|---|---|
| 1 | Attestation frame, slot `kms` | frame, tag `tessera-v1/attest` | KMS key; committed byte for byte in the anchor preimage | §3 |
| 2 | Attestation frame, slot `gpg` | frame, tag `tessera-v1/attest` | gpg key; committed byte for byte in the anchor preimage | §3 |
| 3 | Detached signature `S_kms` over frame 1 | one signature in the serialization §5.2 pins for `(alg, kms)` | committed byte for byte in the anchor preimage; verified over frame 1 from those committed bytes (§5.3) | §5.2 |
| 4 | Detached signature `S_gpg` over frame 2 | one signature in the serialization §5.2 pins for `(alg, gpg)` | committed byte for byte in the anchor preimage; verified over frame 2 from those committed bytes (§5.3) | §5.2 |
| 5 | Manifest frame (map-v1 tuple) | frame, tag `tessera-v1/manifest` | both keys (possession proofs); its SHA-256 is `manifest_sha256` | §4 |
| 6 | Receipt-anchor preimage `A_sig` | tagged, tag `tessera-v1/receipt-anchor-sig` | SHA-256, stamped by OpenTimestamps | §5 |
| 7 | DNSSEC-snapshot preimage | tagged, tag `tessera-v1/dnssec-snapshot` | SHA-256, stamped by OpenTimestamps (C4 snapshot rule) | §6 |
| 8 | Key-publication value (keys + issuance window) | ASCII record at `_tessera-v1.<D>`; the same value in the git key-assertion blob | the zone's DNSSEC keys; the repository key via the signed, anchored commit | §7, §7.1, §7.2 |

Rows 3 and 4 are new as of 2026-10-12. A signature is the signer's output, not a construction of P8. P8 fixes only
its serialization and its place in `A_sig`.

The spec, conformance-vector and preamble objects are content-addressed: their SHA-256 values sit inside the
signed common bytes (§3.2), and they are never signed or anchored on their own.

**Where each of the seven symbolic bindings lives** (A5 §A5.4; A7 §A7.9; R-3.12a):

| Binding (`framed(...)` argument) | Lives in | Equal across slots? |
|---|---|---|
| object type `objType` | the envelope's `type_tag` = `tessera-v1/attest` | yes (one tag for both slots) |
| canonicalization version `canonVer` | the envelope's `canonicalization_version` = `0x0001` | yes |
| algorithm `alg` | the payload's `common.alg` (A3 §A3.6.1: in the canonical payload) | yes |
| issuer identity `issuerId` | the payload's `common.issuer` = D | yes |
| manifest hash `manifestHash` | the payload's `common.manifest_sha256` = hex(SHA256(manifest frame)) | yes |
| payload | the payload's `common` member: the requester's `content` plus the common metadata | yes, **byte-equal** |
| key fingerprint `kfp` | the payload's `signer.key_fp`, the **only** signer-specific member | no |

**Requester content versus signer metadata.** The requester's content is exactly `common.content`. All other
`common` members are common metadata, written by the issuer and equal for both signers. `signer` holds the only
signer-specific field. That makes A5 §A5.4's "payload equal across signer slots" a statement about bytes (§3.4).

---

## 1. Canonical payload bytes: RFC 8785 over the accepted domain

### 1.1 The accepted value domain V

A JSON value is in V if and only if all of the following hold.
- **Literals.** `null`, `true` and `false`.
- **Numbers.** A finite IEEE 754 binary64 value other than −0. *Reason: this is exactly what RFC 8785 can
  serialize without loss.*
- **Strings, including member names.** A sequence of Unicode scalar values with:
  - no surrogate code point (U+D800 to U+DFFF), and so no lone `\uD8xx` escape;
  - no noncharacter (U+FDD0 to U+FDEF, and U+xFFFE or U+xFFFF in every plane). *Reason: RFC 7493 §2.1 (I-JSON); G-04.*
  - no code point that is unassigned (General_Category `Cn`) in **Unicode 16.0.0**. *Reason: this pins the NFC test
    (next item) to one table. Under Unicode's stability policy, a string built from characters assigned in 16.0.0
    that is NFC under 16.0.0 stays NFC under every later version. An unassigned code point carries no such
    guarantee, so two verifiers on different Unicode versions could disagree about it.*
  - the string already in NFC. It is **rejected, never normalized**. *Reason: R-3.4, "inputs relying on Unicode
    normalization assumptions"; G-05 kept.*
- **Arrays.** Arrays of members of V.
- **Objects.** Objects with pairwise distinct member names, compared after unescaping. *Reason: R-3.4's duplicate
  names; G-04.*
- **Depth.** Nesting depth is at most **64** for a whole payload. Each array or object adds 1. The requester's
  `content` sits at depth 3, so it may nest at most **62** levels. *Reason: this pins a limit that real parsers
  otherwise set differently.*
- **Size.** A payload is at most **2^24 bytes** (16 MiB). *Reason: a fixed cap that both implementations
  enforce. No V1 payload comes near it.*

### 1.2 The number rule: value-preserving (G-03 and G-56 resolved for V1)

A number **literal** `L` (RFC 8259 grammar) in submitted JSON text is accepted if and only if:
1. L is not a negative zero: no `-` with zero value (`-0`, `-0.0`, `-0e5`). *Reason: the R-3.4 list.*
2. `d` = the binary64 nearest to L's exact decimal value, under round-half-even, is finite. Overflow is rejected.
3. **The exact decimal value of `ES(d)` equals the exact decimal value of L.** `ES` is ECMAScript
   Number::toString, the serialization RFC 8785 §3.2.2.3 uses.

Accepted: `9.8`, `9.80`, `1E2`, `1e21`, `5e-324`, `123456789012345680000` and `0e99999999999999999999`. Each keeps its
value, and only the spelling changes.

Rejected, each with its reason:
- `1e400`: overflow.
- `1e-400`: nonzero, and rounds to 0.
- `333333333.33333329` and `9007199254740993`: the value would change.
- `0.1000000000000000055511151231257827021181583404541015625`: this is *exactly* a double, but RFC 8785 prints it as
  `0.1`, which has a different value.
- `4.9e-324`: rounds to the smallest subnormal, which prints as `5e-324`.
- `-0`.
- `NaN` and `Infinity`: not JSON at all.

Subnormals that survive rule 3 are accepted, so G-03b is reversed: RFC 8785 treats them as ordinary.

**Why this rule and not the registered literal rule.** Read literally, "exactly representable as a double" does
not compose with RFC 8785. It *accepts* `0.1000000000000000055511151231257827021181583404541015625`, whose
canonical form `0.1` it then *rejects* when the verifier re-reads the payload. So under that reading,
`canonical()` maps its own domain outside itself. The value-preserving rule is the largest rule under which:
- (a) canonicalization never changes a value; and
- (b) every canonical output is itself accepted.
**This changes A1 P8's rejection item and prereg §4.3's wording. A9.8 registers it for `tessera-v1-strict`,
replacing both (A9.7 rows 22–23).** [OWNER 2026-10-19, G38] *(Was: "… and it needs an author sentence (§9, D-1). The
V1 derivation's profile line, 'registered number rule unchanged', must be reconciled with it either way." A9.8
supplied the sentence, and the derivation's line now states the value-preserving rule.)*

What "never helpfully normalized" means here. The **issuer's ingestion** normalizes *spelling only*:
- insignificant whitespace;
- member order;
- escape choice;
- number spelling.

It never changes a value. The **verifier normalizes nothing**: a payload must already equal `JCS` of its own
parse (§1.4, `JSON_NONCANONICAL`). Injectivity (PROOF.md) is stated over *values*. Two texts that differ only in
spelling are one value by definition, and they get one canonical byte string. That is intended.

### 1.3 Serialization

`canonical(v) = JCS(v)` (RFC 8785):
- UTF-8 output, with no insignificant whitespace;
- object members sorted by the UTF-16 code units of their names;
- numbers printed by `ES`;
- strings escaped only for `"`, `\` and U+0000 to U+001F: `\b \t \n \f \r` where defined, `\u00xx` with
  lowercase hex otherwise. Every other scalar appears literally.

*Reason: R-3.1 binds to RFC 8785. Vectors C-04 and C-05 pin the escape and the UTF-16 ordering traps, for example
U+1F600 sorting before U+E000.*

### 1.4 Decoding, and the order in which rejections are reported

Two entry points.
- `ingest(text)` takes requester JSON: whitespace is allowed, and the depth limit is 62.
- `payload(bytes)` takes in-frame bytes: the depth limit is 64, and the bytes must be canonical. Before the
  checks below it enforces §1.1's size limit: more than 2^24 bytes gives `LENGTH_CAP`, the code a frame's
  `payload_length` check gives for the same bytes (§3.1), so the standalone entry point and the frame agree.
  [OWNER 2026-10-19, P8F-04]

Each runs these checks in this order and reports the **first category that fails**, scanning the whole value for
each category. *Reason: both implementations then agree on the reason code, not only on rejection.*

1. `JSON_ENCODING`: the bytes are not strict UTF-8. Overlongs, encoded surrogates and values above U+10FFFF are
   rejected.
2. `JSON_SYNTAX`:
   - a BOM; not exactly one RFC 8259 JSON text; trailing non-whitespace;
   - a raw control character in a string; bad escapes; leading zeros; `+`; `.5`; `1.`; `NaN`; `Infinity`.
3. `JSON_DEPTH`.
4. `JSON_DUPLICATE_NAME`.
5. `JSON_STRING`: a surrogate, a noncharacter, an unassigned code point, or text that is not NFC.
6. `JSON_NUMBER`: §1.2.
7. *(`payload` only)* `JSON_NONCANONICAL`: the bytes are not equal to `JCS` of the parsed value.

---

## 2. The tagged byte strings: one header, four tags

Every byte string that a V1 slot key signs (attestation and manifest frames), and every receipt-anchor and snapshot
preimage that OTS stamps, begins with the same header. Two V1 byte strings carry no header: the git channel's
stamped message, which is exactly the 40 lowercase hex digits of the signed commit id followed by one LF (A9.5,
§7.2), and the key-publication value (§7), which the repository key and the DNSSEC keys sign through git and DNS.
Neither is a frame (Remark 10 of PROOF.md). [OWNER 2026-10-19, Levadura C6] *(Was: "Every V1 byte string that a V1
key signs or that OTS stamps begins with the same header:", which the git stamped message contradicts.)*

The header:

```
header(t) = u8 len(t) || t                       t ∈ T (ASCII, no NUL)
```

| Tag `t` | len | First bytes (hex) | Construction |
|---|---|---|---|
| `tessera-v1/attest` | 17 | `11 74 65 73 …` | frame, §3 |
| `tessera-v1/manifest` | 19 | `13 74 65 73 …` | frame, §4 |
| `tessera-v1/receipt-anchor-sig` | 29 | `1d 74 65 73 …` | signature-inclusive anchor preimage `A_sig`, §5 |
| `tessera-v1/dnssec-snapshot` | 26 | `1a 74 65 73 …` | snapshot preimage, §6 |

`tessera-v1/receipt-anchor` (25, `19 …`), the frame-only anchor tag of the 2026-10-09 draft, is **withdrawn**. It
is not in T, so it is rejected with `TAG_UNKNOWN` (§5.1).

- One string serves as both the domain-separation tag and the object type. R-3.11 lists the two as separate items,
  but A1 P8's four-field frame has a single slot. The prefix `tessera-v1/` does the domain separation, and the
  suffix names the type (G-07 resolved).
- A tag outside T is rejected with `TAG_UNKNOWN`. That includes P7 types V1 does not use (`tessera-v1/wrapper`)
  and later versions (`tessera-v2/attest`). A tag in T that is not the expected one is rejected with
  `TAG_MISMATCH`. *Reason: these are the registered "type-tag mismatch" rejections, and the tag decides the
  construction before any other byte is read.*
- The length byte makes T prefix-free as headers. The proof's Lemma 4 depends on that.
- *Why ASCII tags:* a reader with no V1 software can see them in a hex dump. That helps C6.

---

## 3. The attestation frame (one per signer)

### 3.1 Layout (the four registered fields, A1 P8 / A7 §A7.1)

```
frame(t, p) = header(t) || u16 canonicalization_version || u32 payload_length || payload
            with canonicalization_version = 0x0001 and payload_length = len(payload) ≤ 2^24
```

| Offset | Width | Field | Value / rule | Reason |
|---|---|---|---|---|
| 0 | 1 | tag length | `0x11` for attest | prefix-free tags |
| 1 | 17 | `type_tag` | `tessera-v1/attest` | §2 |
| 18 | 2 | `canonicalization_version` | `0x0001` means RFC 8785 + §1's domain + §1.2's number rule. Any other value: `CV_UNKNOWN` | fixed width; G-02 resolved (u16, value 1) |
| 20 | 4 | `payload_length` | the exact payload length, ≤ 2^24, else `LENGTH_CAP` | G-01 changed from u64 to u32. Four bytes cover the cap, and a smaller field is one less thing to get wrong |
| 24 | L | `payload` | `JCS(value)`, §3.2 | A7 §A7.1: the canonical payload bytes |

The frame ends **exactly** at offset 24 + L.
- If fewer than L payload bytes remain, the result is `TRUNCATED`. Truncation inside the header also gives
  `TRUNCATED`.
- If more remain, the result is `TRAILING`.

The registered rejections "length-prefix mismatch" and "trailing bytes" are therefore one condition, reported by
its direction. Once the length is the only payload boundary, a short length and a trailing byte are the same
event.

### 3.2 The attestation payload

The payload is exactly this object. **No member may be missing or added** (`SCHEMA`). *Reason: a closed schema
means no unsigned or unknown field can carry meaning, which is R-3.39.*

```
{"common":{
   "alg":                 A,     ^[A-Z0-9][A-Z0-9-]{0,63}$          V1 issues the catalog id (see below)
   "binding_forms":       [F…],  nonempty, strictly ascending, each ^[A-Z][A-Z0-9_]{0,31}$
   "content":             <any value in V>                          the requester's content
   "declared_issue_time": "YYYY-MM-DDThh:mm:ssZ"                    a real UTC date and time, seconds 00–59
   "issuer":              D,     lowercase LDH name, ≥ 2 labels, labels 1–63, total ≤ 241
   "manifest_sha256":     hex64  hex(SHA256(manifest frame)), §4
   "preamble_sha256":     hex64  hex(SHA256(purpose-preamble bytes))
   "profile":             "tessera-v1-strict"                       exact
   "spec":{"id": S,  ^[a-z0-9][a-z0-9._/-]{0,127}$                  V1: "tessera-v1-strict/verification-spec/1"
           "sha256": hex64}      hex(SHA256(specification bytes))
   "vectors_sha256":      hex64  hex(SHA256(conformance-vector bytes))
 },
 "signer":{"key_fp": FP}}        FP ∈ §3.3
```

`hex64` means exactly 64 **lowercase** hex digits. Members appear in JCS order, which is the order shown.

- **The id V1 issues.** Under the registered hybrid branch (A9.6; HYBRID-SUPPLEMENT §1, registered 2026-10-16), V1
  issues the pair id `KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA256` (§5.2). The classical id
  `OPENPGP4-ECDSA-P256-SHA256` stays codec-known (rule O in both slots) and is policy-unsupported in the V1
  installation: `UNVERIFIABLE / ALG_UNKNOWN` (V1-PROFILE §1, §8). [OWNER 2026-10-19, Levadura C2] *(Was: `V1 issues
  "OPENPGP4-ECDSA-P256-SHA256"`, the fallback branch's id; the supplement's superseded-statement list omitted it.)*
- **Field grammars** [OWNER 2026-10-19, G18; codifies what both codecs already do, no vector change].
  `declared_issue_time`: years 0001–9999, proleptic Gregorian, seconds 00–59. `issuer`: labels match
  `[a-z0-9-]{1,63}` with no leading or trailing hyphen; all-numeric labels, the top label included, are allowed; at
  least two labels; at most 241 bytes in total.

| Field | Reason, and the G-id it resolves |
|---|---|
| `alg`: any well-formed id, not only V1's | P8 accepts a well-formed unknown id, and stage (c) returns `UNVERIFIABLE`. The canary (R-3.53) needs this, and G-10b's failure mode is avoided. The id names the scheme: "a v4 OpenPGP binary-document signature whose document is the frame, ECDSA P-256, SHA-256" (G-57 kept). Its location inside the payload is A3 §A3.6.1's. G-11 is resolved for V1. |
| `binding_forms`: a sorted, unique, nonempty array | R-3.37 says P8 "defines the set's canonical encoding, ordering, uniqueness and bounds". It sits in the attestation's signed bytes (G-17 kept). *Which* forms V1 requires is C4 profile work. The vectors use `["STMT_DIRECT"]` for illustration. |
| `declared_issue_time`: second precision, `Z` | One spelling per instant. No leap second, because Unix time and Bitcoin time have none. G-16 kept. |
| `issuer` = D, at most 241 characters | D is bound in the signed bytes for the owner-name check (C4, G-21). 241 keeps `_tessera-v1.<D>` within DNS's 255-octet name limit (§7). |
| `manifest_sha256` over the manifest **frame** | The hash covers a tagged string, so it is domain-separated by construction. G-14 is resolved: the hash covers the frame of the tuple and nothing more. |
| `spec`, `vectors_sha256`, `preamble_sha256` | R-3.50: the spec id and hash are in the signed bytes. The vectors and preamble are bound the same way. Each hash is over the object's raw bytes, so `sha256sum` reproduces it with no Tessera code. G-18 and G-47 are resolved as far as P8 goes: they are bound. Consuming them is verifier work. |
| `profile` inside `common` | The signed bytes name their own profile (C6). Dispatch reads the bundle's unsigned profile label first (§8). |
| `content` is arbitrary V | Any JSON value in V. A bare digest string is accepted (C-06 and F-03). |

### 3.3 Fingerprint slot encodings (G-10 resolved; owner ruling for the DNS record)

| Slot | `key_fp` string | Definition |
|---|---|---|
| `kms` | `spki-sha256:` + 64 hex | hex(SHA256(DER SubjectPublicKeyInfo)). For P-256 the SPKI is the 26-byte prefix `3059301306072a8648ce3d020106082a8648ce3d030107034200` followed by `04‖X‖Y` (91 bytes). This is what KMS `GetPublicKey` returns. |
| `gpg` | `gpg-sha256:` + 64 hex | hex(SHA256(body)), where `body` is the v4 public-key packet body (RFC 9580 §5.5.2): `04` ‖ u32 creation ‖ `13` ‖ `08 2a8648ce3d030107` ‖ u16 `0x0203` ‖ `04‖X‖Y`. These are exactly the bytes that the v4 fingerprint hashes *after* its `0x99` ‖ u16 length prefix. That prefix is **not** included, and SHA-1 is not used. This is **not** the fingerprint gpg prints; a tool computes it from the exported key packet. |

- The scheme prefix makes the two slots' strings differ in their first byte, so they can never be equal. It also
  makes the frame self-describing.
- The DNS record (§7) carries the bare hex under the slot name. The verifier compares `kms=<h>` with
  `spki-sha256:<h>` and `gpg=<h>` with `gpg-sha256:<h>`.
- *Consequences to record:*
  - V1 uses no SHA-1 for key binding. The gpg slot binds the whole key packet body, creation time included, under
    SHA-256.
  - The KMS key's OpenPGP key-packet creation time is **not** covered by its `spki-sha256` fingerprint. This is
    **accepted**: for the KMS slot the verifier binds the SPKI (the key KMS actually holds), not the OpenPGP key
    packet. The OpenPGP wrapper's creation time therefore carries no meaning for that slot.

### 3.4 The two frames, as bytes (A5 §A5.4 and R-3.12 stated over bytes)

For one receipt with common value `C`:

```
F_kms = 11 'tessera-v1/attest' 0001 u32(L_kms) '{"common":' JCS(C) ',"signer":{"key_fp":' JCS(fp_kms) '}}'
F_gpg = 11 'tessera-v1/attest' 0001 u32(L_gpg) '{"common":' JCS(C) ',"signer":{"key_fp":' JCS(fp_gpg) '}}'
```

- `JCS(C)` occupies bytes **[34, 34 + |JCS(C)|)** of both frames and is byte-identical. That covers the requester
  content and every common binding.
- The frames differ only in bytes 20–23 (the length) and in the `signer` member. In F-01/F-02 they first differ
  at offset 23, then from offset 745, and the lengths differ by 1 byte (the prefixes `spki-sha256:` and
  `gpg-sha256:`).
- Payload-byte identity of `common` is therefore **not** frame equality. The two frames are never equal (C1).
- No slot name is written: A5 §A5.4 says only the fingerprint differs. The slot comes from the manifest's order:
  `key_fp` is slot `kms` and `sset[0]` is slot `gpg` (G-09 kept). A frame in the wrong slot gives
  `RECEIPT_SLOT`.

### 3.5 What exactly is signed (OpenPGP trailer, PHASE3 finding 4)

Under `alg = OPENPGP4-ECDSA-P256-SHA256`, each slot's signature is an OpenPGP v4 signature of **type 0x00
(binary document)** whose document is the frame. Its exact byte serialization is fixed by §5.2, rule O. A raw
FIPS 204/205 signer signs the frame itself (§5.2, rule R). For OpenPGP, the signed hash input is
`frame ‖ trailer`, where:

```
trailer = 04 ‖ 00 ‖ pubalg ‖ hashalg ‖ u16 hlen ‖ hashed-subpackets ‖ 04 FF ‖ u32(6 + hlen)
```

- The trailer's last four bytes give `6 + hlen`, the length of its hashed header (`04 ‖ 00 ‖ pubalg ‖ hashalg ‖
  u16 hlen ‖ hashed-subpackets`); the whole trailer is `12 + hlen` bytes, that value plus six. So `frame ‖ trailer`
  splits into frame and trailer reading from the end, and the frame's own `payload_length` then delimits the
  payload. PROOF.md Lemma 9 covers this. [OWNER 2026-10-19, P8F-05] *(Was: "The trailer's last four bytes give its
  own length … PROOF.md Lemma 7 covers this.")*
- **Signature type 0x01 (text) must be rejected:** text mode rewrites line endings, and frame headers and lengths
  can contain the bytes `0x0a` and `0x0d`.
- The unhashed subpacket area carries no meaning. Its exact bytes are nonetheless committed by `A_sig` (§5), as
  are all of the signature's bytes.
- **Identifier rule (W1, revised 2026-10-12, finding 5).** No V1 semantic, standing or attempt identifier is
  derived from signature bytes. The anchor digest `SHA256(A_sig)` does commit to them, by design. It is an
  existence commitment for this receipt's exact bytes, not an identifier of the statement (§8).
- **Malleability now means exact-copy integrity, not forgery.** A signature can be changed and still verify:
  - ECDSA's `(r, n − s)`;
  - an edited unhashed subpacket;
  - another packet serialization;
  - a fresh randomized signature over the same frame.

  Any such change gives bytes that fail the stamped anchor (`RECEIPT_ANCHOR_MISMATCH`, negative controls XR-10
  to XR-14). So none of them lets a new signature inherit an old time bound.
  - What remains is copy integrity. A mirror that alters a signature byte damages its copy, just as altering a
    frame byte would. Preservation must keep the committed bytes exactly.
  - A later re-stamp of an altered copy gets a new anchor in a block mined later. It does not restore the
    original one. Its header time need not be later (A10.1). [OWNER 2026-10-19, PR-01] *(Was: "gets a new, later
    time bound.")*
  - V1 does not require signatures to be unique, and it normalizes no signature (low-s or otherwise). Low-s would
    not cover OpenPGP serialization or unhashed-area changes, and any normalization after stamping would break the
    anchor. Serialization choices are made before stamping (§5.4).

---

## 4. The manifest frame (map-v1 tuple; G-08, G-14, G-22)

```
F_manifest = frame("tessera-v1/manifest", JCS({"alg":A,"issuer":D,"key_fp":fp_kms,"sset":[fp_gpg],"ver":"map-v1"}))
manifest_sha256 = hex(SHA256(F_manifest))
```

- The schema is closed: `key_fp` must be a `spki-sha256:` string, and `sset` must hold exactly one `gpg-sha256:`
  string. `ver` is exactly `map-v1`. Anything else is `SCHEMA`.
- *Reason: this is the map-v1 tuple of R-3.36 in the slot order of the C-C2 trace (G-09). Each key's possession
  proof (R-3.38) is its OpenPGP signature over this same frame. The `tessera-v1/manifest` tag keeps that
  signature apart from the same key's attestation signature (P7).*

## 5. The receipt-anchor preimage `A_sig` (G-19 and G-59 resolved; K-2; revised 2026-10-12)

```
A_sig = header("tessera-v1/receipt-anchor-sig") ‖ u8 0x02
        ‖ u32 len(F_kms) ‖ F_kms ‖ u32 len(S_kms) ‖ S_kms
        ‖ u32 len(F_gpg) ‖ F_gpg ‖ u32 len(S_gpg) ‖ S_gpg
anchor digest = SHA256(A_sig), the value OpenTimestamps stamps
```

- `S_x` is slot x's detached signature over `F_x`, exactly as §5.2 serializes it.
- Slots appear in **manifest slot order**: `kms` is the manifest's `key_fp`, and `gpg` is `sset[0]`.
- The count byte is the number of slots. It must be 2 (`ANCHOR_COUNT`).

**Decoding, slot by slot.** Each step's boundary is fixed by bytes already read.
1. `u32` frame length. Above 2^24 + 64 gives `LENGTH_CAP`. Then exactly that many bytes, decoded as one complete
   attestation frame (§3.1). That decode yields the frame's `common.alg`.
2. `u32` signature length. 0 gives `SIG_EMPTY`. Above the cap of the rule for `(common.alg, slot)` gives
   `LENGTH_CAP`.
3. Exactly that many bytes, decoded by that rule (§5.2).
4. After the second signature, any byte gives `TRAILING`. A slot running past the end of input gives
   `TRUNCATED`.

The rule for a slot is chosen from that slot's own frame and its position, both already read.

*Reason.* One OTS proof must cover a receipt that has two signed frames (R-3.42 with reading (a)). It must commit
to the signatures, not only the frames: a stamp over unsigned frames proves only that the frames existed. It
leaves open signing them later, once signing capability for every required slot has been obtained (CODEX-REVIEW
finding 1; finding 2 for "every slot"). Length prefixes and whole, exactly consumed parts make the preimage
injective without any hash assumption (PROOF Lemma 7). The tag keeps it from being taken for a snapshot's proof.

**Outside the preimage.**
- The outputs of anchoring: the OTS proof, txid, block headers and confirmation evidence. Including them would
  be circular (finding 4).
- Transport decoration: armor, containers and the bundle format.

### 5.1 Why the tag changes (and the count byte does not)

The 2026-10-09 frame-only layout used the tag `tessera-v1/receipt-anchor`. That tag is **withdrawn and removed
from T**. A frame-only preimage is therefore rejected at its header with `TAG_UNKNOWN` (XA-09). A fully signed
receipt presented with a frame-only anchor is rejected the same way (XR-09).

There is **no fallback**. No verifier accepts a frame-only anchor under any profile label.

Reasons:
- **Separation by construction.** With a distinct tag, rejecting the old layout is PROOF Lemma 4: the header
  alone decides it. It does not depend on whether bytes in the old layout happen to fail a signature rule.
  - Under the old tag, that dependence would be real. Under rule R, any byte string of the right length is a
    syntactically valid signature.
  - XA-10 shows the same-tag case: the old layout is rejected today only because the gpg frame's first byte
    fails rule O's packet header.
- **Readable dumps.** A hex dump names which construction it holds (C6).
- **No migration cost.** Nothing was issued under the draft layout, so replacing it costs nothing.

The count byte keeps its meaning (two slots), so it is not the place to carry the version.

### 5.2 Signature-slot rules (by algorithm identifier)

Each slot's `S` is **exactly one detached signature** in the single serialization its rule pins.
- `S` is **nonempty** and **at most the rule's cap**.
- The decoder **consumes `S` exactly**. Bytes beyond the signature's own extent give `TRAILING`, which covers a
  second packet. Fewer bytes give `TRUNCATED`.
- **Never `S`:** ASCII armor, a display string, a keyring, or any container that can hold more than one
  signature.

The rule is chosen by `(common.alg, slot)`:

| `common.alg` | slot `kms` | slot `gpg` | Cap per `S` |
|---|---|---|---|
| `OPENPGP4-ECDSA-P256-SHA256` (the classical V1 signers) | rule O | rule O | 1024 bytes |
| `KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA256` (hybrid pair id; registered by the branch-registration supplement of 2026-10-16, A9.6) | rule R: ML-DSA-65 (FIPS 204), pure, empty context | rule O (OpenPGP P-256; slot-2 custody per A9.6) | `kms`: exactly 3309; `gpg`: 1024 |
| any other well-formed id (§3.2) | opaque | opaque | 1 to 65536 bytes; no inner rule. Stage (c) gives `UNVERIFIABLE` (canary, A-02) |

**Rule O (OpenPGP v4 signature, ECDSA P-256, SHA-256; RFC 9580 §4.2, §5.2.3).**

*The packet header (`SIG_PACKET`).*
- `S` is exactly one Signature packet (tag 2) with a **legacy-format header in its shortest form**:
  - `0x88 ‖ u8 n` when the body has n ≤ 255 bytes;
  - `0x89 ‖ u16 n` when 256 ≤ n ≤ 1021.
- Each of these gives `SIG_PACKET`:
  - any other first byte: an OpenPGP-format `0xC2` header, another packet tag, or ASCII armor's `-`;
  - a longer length form than needed.
- This also excludes partial and indeterminate lengths.

*The packet body (`SIG_FORMAT`).* The body is, in order:
1. version `04`, type `00`, public-key algorithm `13` (19, ECDSA), hash algorithm `08` (SHA-256);
2. `u16` hashed length, then the hashed subpackets;
3. `u16` unhashed length, then the unhashed subpackets;
4. two bytes: the left 16 bits of the digest;
5. MPI r;
6. MPI s.

Each of the following holds, or the result is `SIG_FORMAT`:
- each subpacket area is an exact sequence of subpackets, each at least 1 byte, with shortest-form lengths. The
  length forms are RFC 9580 §5.2.3.7's: first octet < 192, one octet; 192–254, two octets
  `((o1−192)<<8)+o2+192` (192–16319); 255, then a four-octet big-endian value (five octets in all). The length
  counts the type octet and is ≥ 1. A longer form than needed is `SIG_FORMAT`; this is a V1 rule, not an RFC ban.
  [OWNER 2026-10-19, G28];
- each MPI is 1 to 256 bits, with an exact bit count;
- the body ends exactly after s.

Type `0x01` (text) is `SIG_FORMAT` (D-10). The codec does not interpret subpacket contents.

*Reasons.*
- **The legacy header is what the gpg signer emits.** GnuPG 2.4.4 emits exactly this header for a detached
  P-256 signature: `88 75 04 00 13 08 …`, a 119-byte packet, observed 2026-10-12. Its output is therefore `S`
  unchanged.
  - The KMS slot's packet is assembled by Tessera's own code, and it must emit the same form.
  - A tool that emits an OpenPGP-format header must have its output re-framed **before stamping**. The header is
    not covered by the signature hash, so re-framing does not affect validity.
  - A verifier never re-frames.
- **The cap.** 1024 bytes is about 8× a GnuPG signature, and it still bounds the malleable unhashed area.

**Rule R (raw FIPS 204 / FIPS 205 signature).**
- `S` is the raw signature byte string that the standard's signing algorithm outputs (the FIPS 204 `sigEncode`
  output; the FIPS 205 signature). It has no header and no wrapper.
- Its length is **exactly** the parameter set's signature size. Any other nonzero length gives `SIG_FORMAT`.
- The signed message is the frame itself (`F_manifest` for a possession proof). No trailer, no transformation.
- **Registered pair (branch-registration supplement of 2026-10-16, A9.6).** `KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA256`:
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
- **Branch recorded:** hybrid, 2026-10-16 (A9.6).

### 5.3 Verification uses the committed bytes, and only those

The verifier first obtains the ordered tuple `(F_kms, S_kms, F_gpg, S_gpg)`, by either route below. The two are
the same by PROOF Lemma 7.
- decode `A_sig`; or
- encode the presented tuple into `A_sig`.

It checks that `SHA256(A_sig)` is the digest the OTS evidence attests. It then verifies **each committed `S` over
its committed `F` under its slot's key**, using exactly those bytes.

The verifier never does any of these:
- verify a separately selected, re-serialized, normalized or reconstructed signature;
- accept a receipt whose presented frames or signatures differ in any byte from the committed tuple
  (`RECEIPT_ANCHOR_MISMATCH`), even when the presented signature is itself valid (negative controls XR-10 to
  XR-14);
- accept a frame-only anchor.

The vectors exercise the following verification-stage codes. They are reported after every codec code:
- `KEY_MISMATCH`: the presented public key does not hash to its slot's manifest fingerprint;
- `SIG_INVALID`: a committed signature does not verify (XR-16, signatures swapped between slots, anchor rebuilt);
- `UNVERIFIABLE` (`ALG_UNKNOWN`): the algorithm id is well-formed but is not the installation's catalog-supported
  id. Being codec-known (a row of §5.2's table) is not being policy-supported: under the hybrid branch the
  classical id is codec-known and still `UNVERIFIABLE` (V1-PROFILE §1, "Codec-known versus policy-supported").
  [OWNER 2026-10-19, Levadura contested 5] *(Was: "the algorithm id is not registered", which used "registered" in
  two senses.)*

These codes belong to the signature verification profile (P3), not to P8.

### 5.4 Issue order (finding 6)

1. Fix the manifest and the common metadata, including `declared_issue_time`.
2. Build `F_kms` and `F_gpg`.
3. Produce one detached signature per slot over its frame.
4. Verify both signatures over their frames under the slot keys, using the exact bytes to be committed.
5. **Freeze** `S_kms` and `S_gpg`. Any serialization step, such as rule O re-framing, happens before this
   point. Nothing changes a signature byte after it.
6. Build `A_sig` and stamp `SHA256(A_sig)` with OpenTimestamps: **one** stamp per receipt (R-3.42).
7. Obtain and validate the confirmation and time evidence.
8. Ship the complete receipt.

- A signature never includes its own eventual anchor time or proof.
- A retry that changes any frame or signature byte needs a fresh stamp, and it obeys the existing reissue and
  temporal rules.
- There is no per-signer stamp, and no frame-only proof is kept alongside.
- R-3.9 is clarified, not weakened. Signatures commit to frames, and the receipt anchor commits to frames plus
  signatures.

## 6. The DNSSEC-snapshot preimage

```
S = header("tessera-v1/dnssec-snapshot") ‖ u32 len(snapshot) ‖ snapshot        1 ≤ len ≤ 2^24
```

- The snapshot body's internal format belongs to the profile document (Track 3). P8 fixes only its envelope.
- *Reason:* C4's snapshot rule gives the snapshot its own OTS proof. The tag keeps that proof from being
  presented as a receipt anchor, or the reverse.

---

## 7. DNS key-publication record

C4(i) needs a DNSSEC-authenticated record that binds V1's two keys to D. Neither the spec nor wamason.com has one
yet (spike report; R-4.26 says only "DNSSEC records publishing the fingerprints").

**Owner name:** `_tessera-v1.<D>`, where D is `common.issuer`.
- The verifier rebuilds this name from the signed `issuer` and compares it, label by label and ignoring ASCII
  case, with the validated RRset's owner name. Anything else gives `DNS_OWNER`.
- *Reason:* the owner name itself is then the C4 owner-name check (G-21/M2). An underscore label cannot collide
  with a hostname, and the `-v1` suffix lets a later profile publish next to it.

**Type:** TXT. **RRset:** exactly **one** TXT record at the owner name (`DNS_RRSET` if there are zero or more).
**RDATA:** exactly **one** character-string (`DNS_STRINGS` otherwise). If a string's length byte runs past the
RDATA, the result is `DNS_RDATA`.
- *Reason:* one string removes every question about how several strings concatenate. A provider that splits a
  value is non-conforming for V1.
- Every canonical value is **exactly 255 bytes**, the limit for one string (DNS-02): each field has a fixed length
  and, since 2026-10-12, every field is mandatory. That leaves no room for another field. A later field needs a new
  record version.

**Value grammar** (ABNF; the canonical form is the only accepted form):

```
value      = "v=tessera1" ";profile=tessera-v1-strict" ";kms=" 64LHEX ";gpg=" 64LHEX
             ";issuance-not-before=" utc ";issuance-not-after=" utc
LHEX       = %x30-39 / %x61-66                              ; lowercase hex only
utc        = 4DIGIT "-" 2DIGIT "-" 2DIGIT "T" 2DIGIT ":" 2DIGIT ":" 2DIGIT "Z"
             ; RFC 3339 UTC; a real Gregorian date and time, seconds 00-59, no fraction
             ; years 0001-9999, proleptic Gregorian [OWNER 2026-10-19, G18]
```

- `kms` is the hex of §3.3's `spki-sha256`. `gpg` is the hex of §3.3's `gpg-sha256`.
- `issuance-not-before` and `issuance-not-after` are both **mandatory** (since 2026-10-12; `issuance-not-before` was
  optional before). `not-after` must be strictly later than `not-before` (`DNS_WINDOW`), and
  `not-after − not-before` must be at most 90 days, 7 776 000 s (`DNS_WINDOW_LENGTH`; Amendment 9's single V1
  window). §7.1 gives their meaning.
- `utc` is exactly the grammar of `declared_issue_time` (§3.2), so the window and the declared time compare
  without conversion. The record's previous grammar was a date only. A one-second boundary cannot be stated with
  a date, so the window uses the same time grammar as the signed bytes.
- The 2026-10-09 optional `not-before=<date>` is replaced by `issuance-not-before` and is now `DNS_FIELD_UNKNOWN`
  (XD-29).
- The value has no spaces and no trailing `;`. Field order is fixed. Bytes are printable ASCII from 0x21 to 0x7E.

Example (DNS-02):

```
v=tessera1;profile=tessera-v1-strict;kms=5cd252fb…7cd3;gpg=5ecd7121…8fc3;issuance-not-before=2026-10-12T00:00:00Z;issuance-not-after=2027-01-10T00:00:00Z
```

**Rejection order** (the first that applies):
1. `DNS_OWNER`
2. `DNS_RRSET`
3. `DNS_RDATA`
4. `DNS_STRINGS`
5. `DNS_SYNTAX`:
   - a byte outside 0x21–0x7E;
   - a field that is not `key=value`, with key `[a-z][a-z-]*` and a nonempty value containing no `=`;
   - an empty field.
6. `DNS_VERSION`: the first field is not `v=tessera1`, or `v` appears again.
7. `DNS_FIELD_UNKNOWN`: an extra field.
8. `DNS_SLOT_DUPLICATE` (`kms` or `gpg` appears twice) or `DNS_FIELD_DUPLICATE` (another field appears twice).
9. `DNS_SLOT_MISSING`.
10. `DNS_FIELD_MISSING` (`profile`, `issuance-not-before` or `issuance-not-after`).
11. `DNS_ORDER`.
12. `DNS_PROFILE`.
13. `DNS_VALUE`: the hex or a time fails its grammar.
14. `DNS_WINDOW`: `issuance-not-after` ≤ `issuance-not-before`.
15. `DNS_WINDOW_LENGTH`: `issuance-not-after − issuance-not-before` > 90 days (7 776 000 s).

**Why the record is unambiguous** (outside PROOF.md's frame domain):
- The accepted values form a regular language. Every field begins with a fixed literal key, and every value
  comes from an alphabet without `;` or `=`, so splitting on `;` and then on the first `=` recovers the fields
  uniquely.
- The field order is fixed, and every value has exactly one spelling: lowercase hex, and `YYYY-MM-DDThh:mm:ssZ`.
  So the map from (kms, gpg, issuance-not-before, issuance-not-after) to value strings is injective, and its
  inverse is the parse. `:` is outside the separators, and `DNS_WINDOW` and `DNS_WINDOW_LENGTH` are checks on parsed
  values, so none of them affects the split.
- One RR with one character-string removes concatenation ambiguity. The RDATA length byte delimits the string.
- The owner name is compared as a label sequence, so `_tessera-v1.wamason.com` cannot match
  `_tessera-v1.wamason.com.evil.example` or `tessera-v1.wamason.com` (XD-12 to XD-14).
- The value begins `v=` (0x76), while every tagged string in §2 begins with a byte from 0x11 to 0x1d. So a TXT
  value can never be a V1 frame, and a frame can never be a TXT value.

### 7.1 Pre-committed issuance window (owner decision 2026-10-12; single 90-day window per Amendment 9)

The key-publication record carries the issuance window. For V1 there is one window, of at most 90 days
(`DNS_WINDOW_LENGTH`), with no overlapping successor: before it ends, either a rotation mechanism is registered or
issuance stops (Amendment 9, A9.6). It is the same canonical value in both channels: the DNS
TXT record, and the git key-assertion blob (§7.2). The same window value is authenticated by the anchored git
assertion and by DNSSEC at the snapshot's own anchored time. Its pre-commitment is **chain order**: the git
assertion's selected anchor height plus 5 is lower than the receipt's selected anchor height, so the window was
confirmed at k = 6 in the chain before the receipt was anchored (A9 C4; V1-PROFILE §6.3, `GIT_NOT_PRECOMMITTED`).
That is chain order, not UTC (A2.1), and DNSSEC evidence establishes no publication before issue (A9 C4). [OWNER
2026-10-19, G02 CORRECT; Levadura C1] *(Was: "The window is therefore fixed in DNSSEC-authenticated and anchored
authority evidence before any receipt that relies on it", which overstated both channels.)*

**Verifier rule (C4).** A receipt passes C4 only if both of these hold:
- `issuance-not-before` ≤ `declared_issue_time`;
- **T ≤ `issuance-not-after`**, where T is the header time of the qualifying attestation at the **lowest block
  height** in the presented OTS proof (A9 C5; A10.5's stages; V1-PROFILE §7.1). Header times are not monotone, so
  selection is by height, never by least header time. [OWNER 2026-10-19, r2-contra; Levadura contested 1] *(Was:
  "the time of the earliest verified attestation", A9's pre-2026-10-14 wording.)*

Otherwise the verdict is `INVALID`, with reason `ISSUANCE_WINDOW`. Both bounds are inclusive: W-01 is
T = not-after, W-02 is declared time = not-before. XW-01 is T = not-after + 1 s, and XW-02 is a declared time
1 s early.

*Rationale, recorded.*
- **A surviving or stolen key cannot mint a receipt that passes with T after the window.** Keys may outlive the
  service's exit, or be stolen. Even signing capability for every required slot cannot produce a receipt that
  passes with verified T after `issuance-not-after`, under continuing anchor, history and authority assumptions. A fresh mint's `A_sig` (§5) can only
  be stamped at or after the moment it exists, and the anchor prevents claiming an earlier block; a later block's
  header time can still be earlier, which is why the claim is only about verified T [OWNER 2026-10-19, PR-01]
  *(was: "the anchor prevents claiming an earlier T")*. So every receipt
  whose verified T is after the window fails (XW-03). This is a statement in chain time, not in UTC (see the
  residual below).
  - A compromise *before* `not-after` is not covered. Within the window, a thief mints receipts that pass, subject
    to the historical-security caveats of CODEX-REVIEW findings 7 and 8.
- **Key-format expiries are not relied on.**
  - OpenPGP key-expiration subpackets live in a self-signature. Any keyholder, a thief included, can re-issue that
    self-signature to extend them.
  - A raw SPKI key, such as a KMS ML-DSA key, carries no expiry at all.
  - The window is instead fixed in authority evidence that the keyholder alone cannot rewrite after the fact.
    Rewriting it means re-publishing the record, which is a new authority event with its own evidence times.

*Residual: chain time (A2.1).*
- T is the **header-time-derived T as registered**. The verifier compares it with `issuance-not-after` directly,
  with no margin added or subtracted. That keeps one registered meaning of T.
- A Bitcoin header's timestamp is not an exact UTC clock. Consensus constrains it only loosely: it must exceed the
  median of the previous eleven blocks, and nodes accept it up to about two hours ahead of their own clock.
- In the direction that matters here, a stamp actually made **after** `not-after` can carry a header time at or
  before `not-after`. Its receipt passes. A2.1 registers no finite bound on that backward skew, and neither ε nor S
  is one. So what this rule guarantees is "no receipt passes with verified T after `not-after`". Translating that
  into a finite UTC cutoff needs an additional, explicit backward-skew assumption that V1 does not establish
  (Codex review of Amendment 9, finding 2; an earlier draft of this paragraph claimed such a bound).
- The opposite error, an honest stamp made just before `not-after` getting a later header time and failing, is
  the safe direction.
- *Issuer invariant:* an attempt whose T would exceed `not-after` is not shipped. The stop margin that implements
  it is an operating number, not part of this encoding (`docs/V1-OPERATIONS-RUNBOOK.md`). The verdict reports the
  comparison with T as registered.

### 7.2 Git channel: what its OTS stamp must cover (finding 9; added 2026-10-12)

- **The blob's content.** Since the issuance-window decision (§7.1), the git key-assertion blob carries the same
  canonical value as the TXT record, so both channels assert one byte string, window included.
- **What P8 does not fix.** The blob's path, and any byte framing around the value: for example, whether a
  trailing LF is allowed. Those are not P8's.
- **What P8 fixes here.** The blob's anchor target.

- **The stamp targets the signed commit's object id.** That commit's tree contains the assertion blob at the
  profile path (V1-PROFILE §6.3, `tessera-v1/key-assertion`), and it carries a `gpgsig` header that verifies under
  the repository key. Whether this commit introduced the blob is not checked (V1-PROFILE §15.4). [OWNER 2026-10-19,
  r2-contra; Levadura C4] *(Was: "That commit adds the assertion blob".)*
- These stamp targets are **not acceptable**:
  - the tree;
  - the blob;
  - an unsigned commit, including the unsigned payload that the commit signature covers.
- *Why, from git's documented object format:*
  - gitformat-signature(5) (git 2.43.0, "COMMIT SIGNATURES") gives a commit signature's payload as the commit
    object, embedded as the header entry `gpgsig`.
  - gitglossary(7) says an object "is uniquely identified by the SHA-1 of its contents".
  - So a signed commit's id is computed over the object **including** its `gpgsig` header. The signature lies
    inside the anchored bytes.
  - A stamp over the tree or blob covers no signature. A stamp over the unsigned commit is the receipt's own
    pre-stage-then-sign gap again.
- *Checked 2026-10-12* (git 2.43.0, GnuPG 2.4.4, scratch repository):
  - the signed commit's id equals `SHA-1("commit " ‖ decimal size ‖ 0x00 ‖ raw object)`;
  - the raw object contains the `gpgsig` header;
  - `git hash-object -t commit` reproduces the id;
  - the unsigned commit with the same tree had a different id, while its tree id was identical.
- **Matching the repository's convention.** This repository stamps a file `timestamps/<id>` holding the commit's
  lowercase hex id and LF, after the commit exists. For a signed commit, that is this target.
- **What the verifier does.** It:
  1. recomputes the id from the presented raw commit object;
  2. verifies `gpgsig` over the object without that header;
  3. follows the commit to its tree and then to the blob;
  4. checks that the stamped bytes name that id.
- The git signature is ASCII-armored inside the commit header. §5.2's binary rule applies to receipt slots only.
- **Residual, already recorded.** Two parts are SHA-1:
  - the commit id itself;
  - the commit → tree → blob linkage.

  Both are in the dependency manifest (V1-DERIVATION's bundle contents and custody residual) and outside P8's
  SHA-256 scope (PROOF (H)). Anchoring a signed commit puts its signature inside the anchored bytes. It does not
  turn the SHA-1 links into SHA-256 bindings.

---

## 8. Identifiers and versions, collected

| Identifier | Encoding | Where |
|---|---|---|
| Construction / object type | `tessera-v1/{attest,manifest,receipt-anchor-sig,dnssec-snapshot}` | §2 header |
| Canonicalization version | u16 `0x0001` | frame offset `1 + len(tag)`: 18 for attest, 20 for manifest [OWNER 2026-10-19, P8F-07] |
| Profile | `"tessera-v1-strict"` | `common.profile`; DNS `profile=` |
| Verification spec | `common.spec.id` + `common.spec.sha256` | §3.2 |
| Authority statement version | `"map-v1"` | manifest `ver` |
| DNS record version | `v=tessera1` | §7 |
| Algorithm | `common.alg` | §3.2 |
| Signature-slot rule | `(common.alg, slot)` | §5.2 |

**Identifier rule (finding 5).**
- No identifier in this table, and no semantic, standing or attempt identifier anywhere in V1, is derived from
  signature bytes.
- The receipt-anchor digest `SHA256(A_sig)` commits to the signature bytes, by design. It is an existence
  commitment, not an identifier (§3.5).

**Dispatch boundary (O-78, an owner decision):**
- The verifier dispatches on the bundle's **unsigned** profile label. An unrecognized label gives
  `UNVERIFIABLE / OUT_OF_PROFILE`, and nothing in this document is evaluated.
- Once a bundle is dispatched to `tessera-v1-strict`, every rejection here is `INVALID`. That includes a signed
  `profile` other than `tessera-v1-strict`, an unknown tag and an unknown canonicalization version, because the
  bundle claimed V1 and its signed bytes contradict that claim.
- The single **codec-level** in-profile `UNVERIFIABLE` that concerns these bytes is a well-formed unknown `alg`
  (stage (c)), and P8 lets that through. The profile adds further in-profile `UNVERIFIABLE` outcomes on these bytes
  (for example `BINDING_FORM_UNSUPPORTED` and `SPEC_UNKNOWN`; V1-PROFILE §3.1 item 5). [OWNER 2026-10-19, G01;
  Levadura C5] *(Was: "The single in-profile `UNVERIFIABLE` …".)*

## 9. Owner decisions taken here, for the author's record

D-1 **Number rule: value-preserving (§1.2).** This changes A1 P8's item "numbers not exactly representable as
IEEE 754 doubles" and prereg §4.3's "must be exactly representable". **A9.8 registers it** (A9.7 rows 22–23), as
Codex review 14 asked. The registered wording also fails to compose with RFC 8785 (§1.2). [OWNER 2026-10-19, G38]
*(Was: "It needs an A9 sentence. … The derivation's profile line, which says the rule is unchanged, must be revised
to match." Both are done.)*
D-2 Unicode 16.0.0 is pinned. Unassigned code points are rejected, and text that is not NFC is rejected rather than
normalized.
D-3 Limits: a payload of at most 2^24 bytes; depth 64 for the payload and 62 for content.
D-4 Widths: a u8 tag length, a u16 canonicalization version equal to 1, and a u32 length (G-01 changed from u64).
D-5 One tag for both signers' frames (A5 §A5.4). Slots are told apart by the fingerprint and the manifest order,
and no slot name is written.
D-6 Fingerprint strings carry scheme prefixes: `spki-sha256` for kms and `gpg-sha256` for gpg.
**Owner decision (2026-10-09): no SHA-1 in V1.** The gpg key is bound by SHA-256 over its OpenPGP v4 public-key
packet body, not by the v4 SHA-1 fingerprint, and this applies to the frame, the manifest and the DNS record. The
KMS key stays SHA-256 of its SPKI. Its OpenPGP creation time is unbound, and that is accepted because the
verifier binds the SPKI for that slot (§3.3).
D-7 `manifest_sha256` is computed over the manifest frame. Spec, vectors and preamble are bound by SHA-256 of their
raw bytes.
D-8 *(revised 2026-10-12, findings 4 and 10)* The anchor preimage `A_sig` holds each slot's full frame and its
exact detached signature, in manifest slot order, with a count byte, under the new tag
`tessera-v1/receipt-anchor-sig`. The 2026-10-09 frame-only layout and its tag are withdrawn, with no fallback
(§5.1). The DNSSEC snapshot has its own tagged envelope.
D-9 A closed schema. `declared_issue_time` has second precision with no leap second. D is at most 241 characters.
`binding_forms` is a sorted array.
D-10 OpenPGP signature type 0x00 only. Since 2026-10-12, the anchor codec enforces this (§5.2, rule O).
D-11 The dispatch boundary in §8.
D-12 The DNS record: one RR, one string, a fixed order, no spaces, and the owner name compared without regard to
case. Since 2026-10-12 every field is mandatory, so every canonical value is 255 bytes.
D-13 Reason codes, and the order in which they are reported (§1.4, §3.1, §5, §7). "Trailing bytes" and
"length-prefix mismatch" are reported as `TRAILING` or `TRUNCATED`, and this now includes a signature's own
extent against its slot length. New in 2026-10-12:
- `SIG_EMPTY`, `SIG_PACKET` and `SIG_FORMAT` (§5.2);
- `LENGTH_CAP` for a signature above its cap;
- the verification-stage codes of §5.3;
- `DNS_WINDOW` (§7) and the C4 code `ISSUANCE_WINDOW` (§7.1);
- `DNS_WINDOW_LENGTH` (§7; Amendment 9 disposition, 2026-10-12).

D-14 *(2026-10-12)* Signature-slot rules are chosen by `(common.alg, slot)`. Rule O is one legacy-header binary v4
packet of at most 1024 bytes. Rule R is raw FIPS 204/205 bytes of the exact parameter-set length. An unregistered
id gets opaque bytes, 1 to 65536 of them.
D-15 *(2026-10-12, finding 6)* The issue order is: frames, sign, verify, freeze the signature bytes, then stamp
`A_sig` (§5.4).
D-16 *(2026-10-12, finding 9)* The git channel's OTS stamp targets the signed commit's object id, never a tree, a
blob or an unsigned commit (§7.2).
D-17 *(2026-10-12, follow-up owner decision)* The issuance window lives in the key-publication record, in both
channels. A receipt is `INVALID / ISSUANCE_WINDOW` unless not-before ≤ declared time and T ≤ not-after. T is the
registered header-time-derived T, with no margin. Key-format expiries are not relied on (§7.1). *Revised
2026-10-12 (Amendment 9 disposition):* both bounds are mandatory and the window is at most 90 days
(`DNS_WINDOW_LENGTH`).

**Out of P8's scope, and named so that nothing is dropped quietly:**
- the bundle's container format and transport encoding (G-26);
- where the observed anchor delay is recorded (G-40);
- the snapshot body's format;
- the git blob path;
- the signature verification profile (P3 [assumption]). P8 now fixes each signature's *serialization* and its
  place in `A_sig` (§5.2). Whether a signature verifies, and what that proves, remains P3's question.
- the PQ algorithm id(s), the parameter set and the signing mode. They are registered only if the 21 Oct spike
  passes (§5.2, rule R); *[OWNER 2026-10-19 annotation: superseded for the hybrid branch by HYBRID-SUPPLEMENT §1–§2,
  registered 2026-10-16 (pair id, ML-DSA-65, pure, empty context). The bullet is kept as baseline text, as the
  supplement directs.]*
- which binding forms V1 requires.
