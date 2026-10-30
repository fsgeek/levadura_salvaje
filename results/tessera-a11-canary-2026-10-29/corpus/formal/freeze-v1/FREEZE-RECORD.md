# V1 freeze record and Phase 1a opening (`tessera-v1-strict`)

> **Status: PROPOSED, ready for the author's signing commit.** A9's signing commit is `2ad3489`; A10's is `9ade764`.
> The A9/A10 locators were refreshed against them before this assembly (FR-01, `docs/reviews/freeze-record/LOCATORS.md`). The author's first commit containing this file is
> the explicit, dated, signed opening commit that A9.2 requires (A9.7 row 2). Prepared 2026-10-24 by the owner
> instance (Claude Opus 5.5). It supersedes `FREEZE-RECORD-DRAFT.md`, which stays as history.

## What is frozen

The objects are assembled from tracked bytes at **one named commit**:
`270ca49bc1384a1ec716b6312f381b2230bb5277` (2026-10-24). It carries the author's E9 rulings (`0a7b336`) and the
locator refresh.

| Object | Bytes | SHA-256 |
|---|---|---|
| `spec.bin` (A9, A10, PROOF, V1-PROFILE, ENCODING-V1, hybrid supplement) | 470034 | `397581f781830b38ce1d07a25867f26d2c025e439cdd2a94e83ee77685d26daf` |
| `vectors.bin` (inventory: `prototype/conformance/VECTORS-OBJECT.md`) | 3123748 | `19ac772a155daf3808727587407a09410572e8291235524b8c36a1ac870bdf3f` |
| `preamble.bin` (`formal/freeze-v1/PREAMBLE.txt`, E9 row 1) | 1205 | `1eebd4a8c2ac405117ba5c4951f053c92459952194a760993dafea1c8959468f` |
| `dependency-manifest.json` | 41181 | `20020475a8ef852fbd3d9331b370a3161e925a44cddf83c8f51d26be2ac9e063` |
| `catalog.json` | 662 | `aaf4306fed070119022c8486219f5160dc869edaa929f323d962fbb679e27fc2` |

Machine-readable form, with every part's blob id: `formal/freeze-v1/freeze-record.json`. Assembler:
`formal/freeze-v1/assemble.py`.

**Hybrid registration completion** (FR-02). For the Specification entry of `formal/p8/HYBRID-REGISTRATION-RECORD.md`,
the frozen spec-object SHA-256 is the one in the table above; it supersedes the draft record's value. The selected
branch stays HYBRID, registered 2026-10-16. The frozen ENCODING-V1 SHA-256 is in `freeze-record.json`; its registered
post-§5.2 baseline is `fe537b1fd68efa51d0a9e6cf29cb8572a9d8ef7906e6a9cf05de035dc446efd0`. ENCODING-V1's 2026-10-19
change accounting and profile §13 note 11 account for the changes in between.

**E18-02** (FR-04). E18's bounded sign-off stands. E18-02 stays open: the archived bridge runner needs a
repository-relative version with a source hash manifest. The E18 review classified it as non-blocking, and the owner
defers it past the opening; the packet's instruction to close it before the opening is superseded by this
record.

**How it was checked (owner, 2026-10-24).**
- Assembled twice from a clean worktree of `270ca49`; the outputs were byte-identical.
- `assemble.py --check`: agreement OK.
- The installed profile matches `270ca49`'s blob.
- Dry run: `prototype/e2e/driver.py` in dry mode with `--freeze-dir formal/freeze-v1`, whose freeze stage recorded
  commit `270ca49` and catalog `aaf4306f…`. The verdict was `VALID_STRICT / OK`, with `utc_assessment`.
- `formal/p8/vectors/check.py`: baseline and hybrid, all counts pass.

The formal models were not all rerun for this record. Their results are those reviewed in E9.

## The author's E9 judgments

Every row has the author's decision (`docs/reviews/e9-packet/AUTHOR-RULINGS.md`, 2026-10-23). There are 27
decisions over rows 1–26, because row 5 has two parts (5a, 5b):
- 26 ACCEPT, at each row's bounded statement in `docs/E9-READ-PACKET.md`. This includes row 22, accepted after the
  requested repairs (`docs/reviews/r22/`).
- Comments and clarified scope on rows 6, 10, 13, 18 and 21. Row 23 is accepted on the corrected understanding that
  the control binds temporal evidence to the exact receipt signatures committed in `A_sig`.
- **Row 2 CUT:** the service-key listing (A10.4.1) is not in V1. This is the author's own narrowing of option (e),
  with his rationale. It is not an invocation of the cut order.

The reviewer's reservations (rows 6, 10, 18, 21) are recorded with the rulings. They stand.

## What the opening permits

Phase 1a opens for **V1-profile code only** (A9.2): the V1 issuer and verifier for `tessera-v1-strict`.
Instrument code under `prototype/` stays instrument code. Service code may port it (owner reading,
`docs/V1-FREEZE-OPEN.md`), but it must earn its own evidence on its own bytes: E10 vectors against AWS, and the P9
code inspection.

## What the opening does not establish

- It discharges nothing in the original H0 or the full capstone gate, and no A9.3 obligation (A9.2). The capstone's
  deferred questions stay open (row 18).
- The models are separate results. Their composition and their preservation by an implementation are not
  established (rows 10 and 21; the E8/E7/E11 sheet's gaps). The contract's guarantee table is a set of mappings,
  not pairs (`docs/V1-CONTRACT.md` §5).
- Instrument outputs, including the two real receipts, are not C-row evidence and discharge no obligation. They may
  inform investigation and select among registered branches, as A9.2 permits.
- **V1's accepted limit:** when both authority channels are captured, receipts under the captor's own keys pass.
- H2 is not adjudicated.

## Still to do (owner, unless marked)

- **By 13 Nov:** E10 extraction.
- **By 20 Nov:** the V1 issuer on AWS behind an API; the service verifier; P3's assumption half; E10 vectors run
  against AWS; the P9 code inspection and its outstanding execution evidence, including the two-machine vector;
  bounded local refusal; A9.4's missing-capture negative control; H3 measured.
- **Before the first public verifier release** (A10.4.2):
  - the custody procedure and its rehearsal;
  - the production release key;
  - the fingerprint channels, named by the author, independent of the operational environment by role and
    credential (row 6);
  - the release-format test vectors;
  - the GCP VPC Service Controls perimeter;
  - a policy for responses the signer was not asked for (E-06).
- **4 Dec:** the relying-party test and the dead-service test. Ship or stop is the author's decision.
