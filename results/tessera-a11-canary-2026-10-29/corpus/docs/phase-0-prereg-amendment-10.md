# Tessera — Phase 0 Pre-Registration, Amendment 10 — six wording corrections to Amendment 9; a conditional UTC assessment, protection against key substitution and release-key custody (2026-10-16, revised 2026-10-17 and 2026-10-18)

> **Status: PROPOSED, ready for the author's signing commit. This document is the instrument and is not yet signed.
> The author's first commit containing this file is its signing act** (the house form since Amendment 5). Drafted
> 2026-10-16 by the AI collaborator (Claude, Opus 5.5, owner instance) from
> `docs/reviews/plain-pilot/CODEX-REVIEW.md` ("Findings about A9 itself", A01–A06), A9, A8 §A8.3 and §A8.5, A2
> §A2.1, A1 §A1.6, `docs/V1-PROFILE.md` §7.1–§7.2 and `formal/p8/ENCODING-V1.md` §7. Revised 2026-10-16 after the
> Codex non-author review of this draft (`docs/reviews/amendment-10/CODEX-REVIEW.md`), applying all eight findings
> as disposed in `docs/reviews/amendment-10/DISPOSITION.md`. **Revised 2026-10-17** to add three items from the
> decision memo `docs/decisions/2026-10-17-utc-bound-and-capture-visibility.md` (as revised after its Codex review,
> `docs/reviews/utc-capture-memo/CODEX-REVIEW.md` and `DISPOSITION.md`), with the tolerance evidence in
> `docs/decisions/2026-10-17-a-utc-tolerance-evidence.md`: §A10.1.1 (a conditional UTC assessment), option (e) of
> §A10.4 with §A10.4.1 (protection against key substitution) and §A10.4.2 (release-key custody). Revised again
> 2026-10-17 after the Codex non-author review of that revision (`docs/reviews/amendment-10-r2/CODEX-REVIEW.md`),
> applying all eight findings with Codex's exact text as disposed in `docs/reviews/amendment-10-r2/DISPOSITION.md`.
> Layered on the original and Amendments 1–9. Per amend-don't-rewrite, none of them is edited: every registered
> sentence this amendment changes is listed in §A10.7 with its source line and its replacement, and is left standing
> in its file. A10.4.2's gate timing was revised 2026-10-17 on the owner's proposal after the custody review
> (`docs/reviews/custody/CODEX-REVIEW.md`), and its TEST-key and bootstrap text after
> `docs/reviews/amendment-10-r3/CODEX-REVIEW.md` (R3-02, and the A10 part of R3-03). A10.4.1's listing
> pre-commitment (an owner decision of 2026-10-18) was narrowed after `docs/reviews/amendment-10-r4/CODEX-REVIEW.md`
> (R4-01 to R4-04), disposed in `docs/reviews/amendment-10-r4/DISPOSITION.md`.
>
> **AUTHOR ADOPTED 2026-10-18 (recommended by the owner and Codex): A10.1.1, A10.4 option (e) with A10.4.1, and
> A10.4.2** (`docs/reviews/amendment-10-r4/AUTHOR-RULINGS.md`). The author, 2026-10-18, after his question about how
> a 2106 adjudicator knows the contents of the service-key listing: *"That's it.  The other three items, while
> dense, seem rational are accepted."* Confirming the owner's reading that this adopts A10.1.1, A10.4 option (e)
> with A10.4.1 (including the listing's chain-order pre-commitment) and A10.4.2 (the release-custody gate at the
> first public verifier release), 2026-10-18: *"Yes. That's my understanding.  I focused on reading those sections
> of the document.  A 10.4.2 stood out because you disagreed, but even for those where you were in agreement, I read
> what was proposed and accepted the recommendation as being "rationally based.""* Rows 15–16 and 20–39 of A10.7 are
> *Owner note, 2026-10-18:* "you disagreed" in the author's statement refers to the owner's proposal to move A10.4.2's gate from the 30 Oct freeze to the first public verifier release, departing from the earlier drafted text. This is the owner's reading; the author can correct it before signing.
> AUTHOR ADOPTED. By this ruling the author adopts the A-UTC trust assumption; his signature does not establish that
> miners satisfy it. The narrowing from review r4 was applied after his ruling, and he was told of it before
> signing.

## In plain words

This amendment has two parts.

**Part 1** corrects six wording problems in Amendment 9. The owner decided these corrections. They add no
mechanism. The verifier uses the same checks and gives the same verdicts. A review of the plain version of
Amendment 9 found the six problems.

Bitcoin is a public system that adds blocks to a chain. A block header states a chain time. This value is not a
measurement of real time. The registered number k is six.

- **A01.** Amendment 9 says that the content existed "no later than" T. T is a chain time, not real time. The
  correction says this in the claim and in the other sentences that use T in this way.
- **A02.** Amendment 9 says, in its own words, that the keys "were allowed to issue during a stated window". The
  verifier makes only two comparisons with the window. The correction states only those two comparisons.
- **A03.** Amendment 9 excludes Bitcoin history "deeper than k". The correction defines the depth of a
  reorganization. The exclusion then also includes a reorganization of exactly k blocks. The models already
  exclude that case.
- **A04.** Amendment 9 does not say which receipts V1 protects after an attacker obtains authority-record
  credentials. The author chose option (e) on 18 October 2026. Part 2 describes it.
  - The adopted text protects the frames and signatures that the service keys made honestly. This protection
    applies before and after the attacker obtains the credentials.
  - Without the key list of Part 2, V1 does not prevent new receipts under the attacker's own keys.
  - The service must publish its authority record. A third party can inspect a substituted key if that record is
    public. The verifier does not check publication. V1 does not guarantee that an attacker publishes the record.
- **A05.** Amendment 9 does not give the order of the steps that select a Bitcoin attestation. The correction
  gives the steps that the profile already uses.
- **A06.** DNS (the Domain Name System) holds one authority record. Amendment 9 says "owner name D". The verifier
  must check the DNS owner name `_tessera-v1.wamason.com`. The correction names it.

**Part 2** has three new items. The owner and Codex recommended them. Codex is a second AI system that reviews this
work. The author accepted all three on 18 October 2026. They add new mechanism to V1.

**UTC: what U is.** UTC (Coordinated Universal Time) is the standard measure of real time. Amendment 9 states no
UTC time.

- Under A-UTC, U is a UTC upper bound: the latest chain time of the six confirming blocks, plus two hours.
- The claim is conditional: if A-UTC is true, the content and both signatures existed before U.

**UTC: the assumption A-UTC.** A miner is a party that makes Bitcoin blocks.

- A-UTC says: at least one of those six blocks states a chain time no more than two hours before its real
  production time.
- A-UTC is false only if the miners of all six blocks state chain times more than two hours early.
- Nothing in Bitcoin or in the verifier makes sure that A-UTC is true.
- The author's signature accepts A-UTC as an assumption. The signature does not show that miners make A-UTC true.

**UTC: the evidence.**

- The retained measurements cover 2015 to 2026. In each complete set of six, one recorded arrival was no later
  than chain time plus 1065 seconds.
- The dataset rejects arrival times more than two hours from the chain time. It cannot show failures beyond that
  limit.
- Observer clocks can also be wrong. These measurements do not show that A-UTC was true.

**UTC: the output.**

- The verifier reports U with its assumption identifier, `A-UTC-7200-6`, in `utc_assessment`.
- U, conditional on A-UTC, is outside the six fields that later verifiers must reproduce. U does not change the
  verdict.
- Each statement of U must give the assumption A-UTC next to it.

**UTC: the year 2106.** In 2106 the Bitcoin time field reaches its maximum. The calculation of U, whose UTC claim
depends on A-UTC, stays correct for the saved headers of older blocks. Bitcoin, not V1, must define the times of
blocks after that point.

**Key substitution: the problem.** An attacker with both authority-record credentials can make authority records
that name the attacker's own keys. Without a new mechanism, receipts under those keys can get VALID.

**Key substitution: option (e).**

- Option (e) adds a list of the service keys to the trust file. The release key authenticates the trust file.
- The verifier gives INVALID or CANNOT VERIFY for a receipt whose keys are not on the list.
- The release-key holder must not add keys to the list only because the two authority records name them.
- The author chose option (e). He did not choose option (a), which has no list, or options (b) to (d).

**Key substitution: the limits.**

- The protection applies only to a user whose verifier release is authentic and comes from an honest release-key
  holder.
- It stops those users from accepting such receipts.
- It does not make sure that anybody finds or publishes the attack.
- An attacker who also has the release key can make a release that lists the attacker's keys.

**Key substitution: time.** A release must list the exact keys and window before the receipt's Bitcoin anchor. To
check this after release-key theft, keep the first listing release and its proof, and authenticate the Bitcoin
history for both anchors independently of the stolen key. The release-key fingerprint alone cannot identify a forged
release history. Keep this evidence together with the receipt.

**Release-key custody: the rule.** AWS means Amazon Web Services, the provider of the service's cloud account.
Amendment 9 already requires these access limits:

- The DNS credential and the repository key must not give access to the release key.
- Access to the AWS account must not give access to the release key.
- Hardware or offline software for the release key is acceptable only with a written procedure.

The procedure has these contents:

- The procedure must say who authorizes each release.
- The procedure must say where the signing occurs.
- The procedure must say how backups stay outside the systems that operate the service.
- The procedure must say how a separate system checks each release before the signing.
- The procedure must say how files move into and out of the signing system.

**Release-key custody: when.**

- At the freeze, the rule, the release format and the contents of the procedure must be fixed.
- After the freeze, the owner builds and tests the signing system.
- A reviewer must check the procedure before the first public verifier release.
- The target for that release is before 20 November 2026.

**Release-key custody: test releases.** Each early release uses a separate test release key. Production checks
never accept this key. Users must authenticate the production release key before they rely on a release. The
service must not offer an early release for real use. A test must show that production checks refuse a release
with only a test signature.

**Release-key custody: risks that the owner names.**

- The schedule risk moves later. The owner must start the preparation early.
- The rules do not change after the freeze, because the release format is fixed at the freeze.
- Production checks refuse an early release, because it has only a test signature.
- The author accepts the use of his time in November. He wrote: "(4) is acceptable to me".
- The service does not offer an early release for real use.

**Release-key custody: if independence fails.** The purchase of hardware alone does not make the key independent.
If the owner cannot show independence before the first public verifier release, the author gets a NARROW-MODEL. That
model is a smaller protection against an attacker with authority-record credentials. The removal of the key list
does not repair this.

Two other mechanisms are recorded as candidates only: time-stamp authorities and a witnessed public log. This
amendment does not require anybody to make them.

Each change has a kind:

- CLARIFY: the meaning does not change.
- NARROW-CLAIM: the claim becomes smaller, so that it states only what the checks establish.
- CORRECT: the wording disagreed with a registered rule or model. The correction follows that rule or model
  without reducing the claim.
- BROADEN: the claim becomes larger. It adds a mechanism or a stated assumption.
- GATE: the change adds or changes a prerequisite, a trigger, or a cut order. The row states any scope change that
  follows.

New words in this summary (owner proposals; not yet in the plain-language dictionary):

| Word | Meaning |
|---|---|
| UTC | Coordinated Universal Time, the standard measure of real time. |
| miner | A party that makes Bitcoin blocks. |
| U | Under A-UTC, a UTC upper bound: the latest chain time of the six confirming blocks, plus two hours. |
| A-UTC | The assumption that at least one of those six blocks states a chain time no more than two hours before its real production time. |
| key list | The list of the service keys in the trust file. |
| freeze | The point, by 30 October 2026, after which the V1 rules do not change. |
| first public verifier release | The first verifier release that users get, signed with the real release key. |
| test release key | A separate key that signs each verifier release before the first public verifier release. Production checks never accept it. |
| NARROW-MODEL | A smaller model of the attacker against whom V1 holds. Only the author can accept it. |

---

**Provenance labels** (as in A9). **AUTHOR DECISION**: the author ruled, in his own quoted words, dated. **AUTHOR
ADOPTED**: the author adopted a recommendation in his own quoted words, dated (an AUTHOR DECISION in A9's sense;
equivalent to ADOPTED (author)); the recommendation's provenance stays beside it. **OWNER DECISION**: taken by the
owner instance under the project ownership the author assigned on 2026-10-12; not an author ruling. **RECOMMENDED**:
drafted, not decided by anyone. "Recommended by the owner and Codex" means the owner recommended it and a Codex
review supported it. What the signature means for OWNER items is as in A9: the author has read them and does not
object.

**Weakening (A1 §A1.1).** No A1.2 property, registered check, verdict, reason code, parameter (δ, ε, k, N, S),
vector, encoding, model, or scenario-mapping verdict, fixture or safe-decision category is weakened or withdrawn.
A10.1–A10.4 narrow sentences of A9's prose claim to what A9's own checks, A8.3's runs and the cited models
establish; no evidence is withdrawn. A10.3 removes one boundary case from the claim that the registered assumption
(A1.6) and the model (P5c) never covered. This signed amendment is the record A1 §A1.1 requires for each narrowing.

**Mechanism added by the author-adopted items.** A10.1–A10.6 and A10.4 option (a) add no mechanism. The three
items the author adopted on 2026-10-18 do:
- A10.1.1 adds one reported assessment (`utc_assessment`), one named assumption (A-UTC) and two frozen catalog
  constants (Δ = 7200 s, m = 6). It enters no verdict, no reason code and no stable field.
- A10.4 option (e) adds one trust-file field (`service_keys`), one check, one reason code
  (`SERVICE_KEYS_NOT_LISTED`), the release-authorization closure invariants and one issuer invariant. It
  deliberately makes one new case INVALID or UNVERIFIABLE: a receipt under keys the release does not list. The
  listing's chain-order pre-commitment (OWNER DECISION 2026-10-18, narrowed after review r4) adds release stamping,
  the listing-evidence package as declared inputs, the ordered listing subchecks and three proposed reason codes
  (`LISTING_PROOF_MISSING`, `LISTING_STAMP_MISMATCH`, `LISTING_NOT_PRECOMMITTED`); with
  `SERVICE_KEYS_NOT_LISTED`, A10.4.1 adds four new reason codes.
- A10.4.2 adds a release-key independence gate before the first public verifier release, a release format frozen
  at the freeze, and a TEST release key for every earlier release.

Neither addition weakens a registered claim: the listing only rejects more, and A-UTC supports only the new UTC
assessment, while every chain-order claim stands without it. The scenario mapping's verdicts are unchanged; "no
verdict changes" is withdrawn as a description of option (e). Evidence for option (e) is its construction plus
prospective vectors; A8.3 and A8.5 supply none, and no formal model run supports it.

---

## A10.1 "Existed no later than T" is chain time, not UTC — OWNER DECISION, NARROW-CLAIM (review A01)

A9 says the bytes and signatures "existed no later than a time T fixed by Bitcoin" (A9:36-37; again at :114,
:133 and in C5, :144). A9 also says that header times are chain-time proxies (C5) and that a finite UTC cutoff
"requires an additional, explicit backward-skew assumption that V1 does not establish" (:444-446). The ordinary
reading of "no later than T" is a real-time bound, which A9 does not support.

**Reading adopted.** "No later than T" means chain order: the bytes and exact signatures existed before the
selected Bitcoin block was mined, because that block commits to their SHA-256 hash (under the registered
cryptographic and chain assumptions). T is that block's header time, a chain-time value. It is not an upper bound
in UTC: A2.1 registers no finite bound on B − C, and neither ε nor S is one. A UTC reading needs the additional
backward-skew assumption that V1 does not establish. A10.1.1 recommends one such assumption, for a separate
assessment only; this section does not depend on it.

**Other registered uses of the same bound.** The scenario mapping (:177, :186), the issue order (:294-295) and
guarantee 1 (:433-439) use T as the same clock bound. Each is qualified the same way (rows 5–9 of A10.7). These
qualifications change the explanation of the safe decisions, not their verdicts, fixtures or case membership.
Scenario i's parties' signature-checking duty and guarantee 1's `historical_security: NOT_EVALUATED` stay. The
issue-order case is concrete: a signature made after a backward-skewed header's nominal UTC time, but before the
block is mined, can fit the block's anchor.

**Assembled C5 claim cell** (rows 4 and 17 of A10.7 both point here):

> The frames **and their exact signatures** existed before the selected Bitcoin block was mined. T is that block's
> header time, not a UTC upper bound. The selected block belongs to the qualifying Bitcoin attestation at the lowest
> block height in the presented OTS proof, under A10.5's stages; T and its confirmations come from that same
> attestation. The three-conjunct predicate holds at k = 6. Header times need not be monotone; selection uses chain
> order, not the least header time (OWNER DECISION 2026-10-14, F03).

C5's non-claims stay, with the reorganization residual amended by A10.3 (row 14). Under A10.1.1 (author adopted
2026-10-18), row 21 adds its conditional sentence after this cell; the cell itself does not change.

**A1.6.** A1.6 (:485-505) contains older, compressed clock and depth language. A1 stays standing. This amendment is
a V1 qualification of that inherited clock wording; the unchanged historical prose does not itself establish a UTC
bound. The changed sentences are rows 1–9 of A10.7.

### A10.1.1 A conditional UTC assessment — AUTHOR ADOPTED 2026-10-18 (recommended by the owner and Codex), BROADEN

Source: the decision memo, Part 1 (U1) and Part 3; its Codex review, F03, F04 and "Questions checked" 1; the
tolerance evidence file. A10.1 stays as decided independently of this section.

**Author ruling, 2026-10-18** (`docs/reviews/amendment-10-r4/AUTHOR-RULINGS.md`): *"That's it.  The other three
items, while dense, seem rational are accepted."* And, confirming the owner's reading that this adopts A10.1.1,
A10.4 option (e) with A10.4.1 and A10.4.2: *"Yes. That's my understanding.  I focused on reading those sections of
the document.  A 10.4.2 stood out because you disagreed, but even for those where you were in agreement, I read what
was proposed and accepted the recommendation as being "rationally based.""*

**Notation.** h* is the receipt proof's selected inclusion height (A10.5). A2.1 counts it as confirmation one, so
h*+5 is confirmation six. r(j) is the real (UTC) time at which block j was first produced.

**Assumption A-UTC** (`assumption_id: "A-UTC-7200-6"`). *At least one of the six blocks h* … h*+5 has a header
time no more than 7200 s before it was actually mined*, that is, `nTime(j) ≥ r(j) − 7200 s` for some j in
[h*, h*+5]. A-UTC is an assumption of the UTC assessment only. It is not a Bitcoin consensus rule, the verifier
does not check it, and no bundle carries evidence of it. It is a sufficient one-sided assumption, not a minimal one.
Δ = 7200 s and m = 6 are frozen in the governing specification's catalog, not in the mutable trust file, and are
not shown to be optimal.

**Recommended claim text**, added after the A10.1 claim it qualifies (rows 20–21):

> Under assumption A-UTC (at least one of the blocks h* … h*+5 has a header time no more than 7200 s before it was
> actually mined; an assumption of the UTC assessment, not a consensus rule, and not checked by the verifier), the
> bytes and both signatures existed before U = max nTime(h* … h*+5) + 7200 s, in UTC. V1 reports U only in
> `utc_assessment`, beside its assumption identifier, outside the six stable fields. A2.1's refusal to bound the
> observation lag B − C is unchanged.

**Derivation** (memo, checked by Codex). (1) `A_sig` existed before r(h*), because h*'s merkle root commits to
`SHA256(A_sig)` under the registered commitment and history assumptions. (2) r(h*) ≤ r(j) for every j ≥ h*,
because block j commits to a chain that contains h*. (3) A-UTC supplies j in [h*, h*+5] with r(j) ≤ nTime(j) + 7200.
(4) So r(h*) ≤ r(j) ≤ nTime(j) + 7200 ≤ U. The chain-order claims of A10.1 rest on steps 1–2 only.

**Output contract** (memo, F03). `utc_assessment` contains `assumption_id: "A-UTC-7200-6"` and `utc_upper_bound`
(RFC 3339 string or null). It is computed from the receipt proof's selected h* and its six qualified headers. Its
bound is conditional on A-UTC and the existing commitment/history assumptions. It is null exactly when T is null.
It does not change the six-field V1 stable result (A9:162, A9.4). Reporting a value with INVALID or UNVERIFIABLE
does not establish a valid service receipt or valid service signatures. U is never a stable field, and V1's
documentation and relying-party text never state U without A-UTC beside it.

**Arithmetic and the 2106 boundary** (memo, F04). Verification of a preserved V1 receipt does not consult the
current clock. Each bundled nTime is the profile's unsigned epoch-seconds value, widened before arithmetic:
`U_seconds = 7200 + max(uint64(nTime(h*)), …, uint64(nTime(h*+5)))`, encoded as an RFC 3339 UTC string without
reduction modulo 2^32 (for max nTime = 4294967295, U = `2106-02-07T08:28:15Z`, not a 1970 time). This 64-bit
arithmetic covers preserved headers. Timestamp representation for Bitcoin blocks produced after the 2106 rollover
of the 32-bit field is a Bitcoin protocol matter outside V1; the profile's serial-time unwrapping applies to DNSSEC
RRSIG fields only.

**What the ruling and signature do and do not do.** By his 2026-10-18 ruling and his signature, the author adopts
A-UTC as a trust assumption. It does not establish that miners satisfy it, and nothing in V1 can.

**Justification of the tolerance against the intended adversary**
(`docs/decisions/2026-10-17-a-utc-tolerance-evidence.md`). The intended adversary is A9's backdater (A9:40): bytes
that exist only at real time e, presented with a receipt whose U is earlier than e.
- **Failure condition.** A-UTC fails, and U can be wrong, only if the miners of all six confirming blocks set
  lagging timestamps: every block h* … h*+5 has a header time more than 7200 s before it was mined.
- **A non-mining backdater** can choose only when to stamp and which proof to present. Lowest-height selection fixes
  the result within a presented proof, but does not eliminate choice among available presentations. The UTC
  assessment relies on A-UTC for the selected segment in every case. Over 559,718 retained complete six-block
  windows (heights 369,715–941,944, 2015–2026; Bitcoin Block Arrival Time Dataset, multiple observers, CC0), every
  window contained a block whose recorded arrival lag was at most 1,065 s. The minimum computed U minus the
  inclusion block's recorded first-seen time was 6,135 s (median 9,908 s); U's UTC interpretation remains
  conditional on A-UTC. If the selected observer readings do not understate production time, these observations
  support A-UTC for the sampled windows. Observer clock error is not bounded here. The dataset's ±7200 s quality
  filter and excluded incomplete windows prevent an inference about the frequency of A-UTC failures outside the
  retained sample. The largest single-block lag observed was 3,918 s; the median was 18 s. A mempool.space sample of
  481 blocks (2024) and Bowden et al. (arXiv:1801.07447, 2018) are consistent with this.
- **Consensus.** Consensus requires each timestamp to exceed the median of the preceding eleven header times. The
  evidence reproduces 545 windows in which every recorded first-seen-minus-MTP value exceeds 7200 s. These MTPs use
  the actual predecessor timestamps and the observer-clock qualification. The count does not bound a coalition
  changing the six timestamps, since changes within the window also change later MTPs. A majority coalition can
  sustain lagging timestamps; A-UTC is not consensus protection against that adversary.
- **Limits of the evidence.** The dataset's own quality check rejects any arrival more than 7200 s from its header
  time, so it cannot show a lag above the threshold; its distribution below the threshold has no observation
  between 3,918 s and 7,200 s. Observer clock error is not separated. The data describe ordinary miner behaviour,
  not a deliberate coalition.
- Δ equals Bitcoin's node-local forward tolerance; that match does not validate it. m = 6 reuses the k = 6 headers
  that V1 already requires and pins, so U needs no new input.

**Relation to A2.1 and guarantee 2.** A2.1 refuses to bound B − C, the service's observation lag, and keeps
SLA-style bounds out of the assumption set. A-UTC bounds a different quantity (production time versus header time),
and U never enters a verdict, the shipping predicate or S. Guarantee 2 keeps its chain-time meaning and is not
translated to UTC (row 23).

**Recorded, not obligations.** RFC 3161 tokens over `SHA256(A_sig)` from at least two independently operated
time-stamp authorities (U_TSA = max_i(genTime_i + a_i), memo U2) are a recorded candidate, with no V2 or later
obligation. Unresolved use requirements, also recorded only: whether a court or another examiner will accept A-UTC;
whether a particular use needs qualified timestamps.

The changed sentences are rows 20–24 of A10.7.

## A10.2 The window establishes two comparisons, not issuance "inside" it — OWNER DECISION, NARROW-CLAIM (review A02)

A9's opening says the keys "were allowed to issue during a stated window" (:36), and guarantee 2's heading says
"Signing capability mints only inside the window, in chain time" (:441). The C4 verifier rule (:419-421) checks
only two comparisons, and says "T itself is not compared with not-before".

**Reading adopted.** The verifier establishes exactly two inclusive comparisons, with no margin:
- the declared issue time is not earlier than `issuance-not-before`;
- the verified chain-time T is not later than `issuance-not-after`.

It does not establish that T is not earlier than not-before, that the declared issue time is not later than
not-after, or that any signing act occurred inside the interval. The review's two arithmetic witnesses satisfy the
two window comparisons and all three A2 temporal comparisons. They are not executed receipt vectors or evidence
that an honest issuer ships those values. The checks do not change. The issuer invariant (:422, an attempt whose T
would exceed not-after is not shipped) stays an issuer duty, not a verifier comparison. "Issuance window" stays the
name of the record's two values. The changed sentences are rows 10–12 of A10.7.

## A10.3 Reorganization depth, at k = 6 and `DepthK = k − 1` — OWNER DECISION, NARROW-CLAIM (review A03)

A9 excludes "Bitcoin history deeper than k" (:49-50) and calls "Reorganization deeper than k" a residual (C5,
:144). A9 also imports k = 6 under `DepthK = k − 1` (:105) and A2.1's count, in which the including block is the
first confirmation.

**Definition.** The depth of a reorganization is the number of blocks it removes from the tip of the chain. A
reorganization of depth d removes every block that has d or fewer confirmations when it occurs. At k = 6
confirmations, five blocks follow the anchor block; P5c's `depth` counts those five (`depth = c − 1`, so
`DepthK = 5`).

**Correction.** The registered assumption is that anchors with k or more confirmations are permanent (A1.6:
"anchors at depth ≥ k are treated as permanent"). P5c's `Reorg` action can orphan an anchor only while
`depth < DepthK`, that is, at five or fewer confirmations. So a reorganization of depth exactly k, which removes an
anchor with k confirmations, is outside both. A9's "deeper than k" read literally leaves that case inside the
claim, with no evidence. The excluded residual is therefore **a reorganization of depth k or more**. This narrows
A9's literal prose claim at equality. It changes neither the model nor its permanence assumption, and withdraws no
checked model result. This does not affect C4's chain-order gap (`g + 5 < r`), which the review found correct. The
changed sentences are rows 13–14 of A10.7.

## A10.4 Authority capture: honest signed material protected; publication remains an issuer duty; key substitution — AUTHOR ADOPTED 2026-10-18: option (e) (recommended by the owner; option (e) also by Codex), NARROW-CLAIM and BROADEN (review A04)

A9's adversary sentence includes "anyone who captures authority-channel credentials while signing capability stays
uncompromised (A8.3's sense of capture)" (:41-42). It names no set of receipts and no object for "signing
capability". A8.3 (:72-76) bounds the tested property: under capture, "a captor cannot reattribute honest frames,
alter honest signer sets, or carry honest signatures onto other bytes or keys". That property concerns honest
service material, not only receipts issued before disclosure; the capture fixtures disclose the credentials before
the honest signing processes run. A8.5 (:123-124) puts "preventing a captured or merged authority from issuing new
attestations" out of scope. A captor holding both required channel credentials can sign and anchor a key assertion
that names its own keys, without publishing it; receipts under those keys can then pass V1. Capture of only one
required channel does not generally suffice.

**The author's standard** (2026-10-08, `docs/guarantee-tiers-DRAFT.md`, "Authority capture"): *"perhaps the right
way to attack the problem is distribution and admission that governance changes are out of scope"*, and
*"Authority capture must be visible in such instances. For an adjudicator to be convinced incorrectly requires the
takeover be invisible."* The owner summarizes it as: prevent, no; rewrite the past, no; visible, yes. The summary
is the owner's, not a quotation. These words are the motivation for A10.4. They are not evidence that the visibility
property is established. No option below establishes it: option (e) prevents acceptance by a scoped set of relying
parties; it does not ensure that anyone detects or publicly exposes a capture.

**Recommended text.** Replace the adversary clause with:

> anyone who captures authority-channel credentials (the DNS credential or the repository key, including both
> together) while the original service keys stay secret and their signing capability stays uncompromised (A8.3's
> sense of capture), as to frames honestly signed by those service keys, whether before or after credential
> disclosure: such a captor cannot reattribute those frames to other keys or another service, alter their honest
> signer sets, or carry their signatures onto other bytes or keys (A8.3);

and add to "The boundaries", before its last sentence:

> V1 does not prevent a captor of both required authority-channel credentials from issuing new receipts under a key
> assertion that names the captor's own keys, even while the original service keys remain uncompromised. Public
> publication of the key-assertion repository remains an issuer duty (A9.7, "Changed in effect"). If the
> substituted assertion is publicly published, a third party can inspect the substituted keys. The verifier does
> not check publication; V1 does not guarantee that a captor publishes the assertion, that capture is detected, or
> that new receipts are publicly visible.

Under option (e), row 26 replaces this boundary's first sentence with a scoped one (A10.4.1).

Backdating stays with the temporal checks (C4's chain-order pre-commitment, C5) under their own assumptions; A8.3's
runs do not test it (A8.3). Whole-author-sphere capture stays excluded (R-2.15). Guarantee 2's proviso
"provided the authority channels are not also captured" (:443) is unchanged and consistent with this text.

**Options for the author.** (a) Adopt the bounded honest-material claim above, with the new-receipt limitation and
conditional publication statement. (b) Deliberately restrict even that claim to receipts honestly issued before
capture; this gives up the honest post-capture material covered by A8.3's stated property and must be recorded as
an additional author choice. (c) Extend presentation protection to arbitrary new receipts under captor-selected
keys for every relying party, with issuer detection or public visibility; this needs a mechanism V1 does not have
(for example a witnessed public log), and is not supported by this amendment. (d) Rule other text. **(e) Adopt (a)
and add protection against key substitution: the trust-file service-key listing of A10.4.1**, with its ordered
classifier and authorization closure, scoped to relying parties using an authentic, trustworthy release. This is a
BROADEN; it adds mechanism (rows 25–33, 37–39). Rows 15–16 take effect on (a) or (e); rows 25–33 and 37–39 only on
(e).

**Owner recommendation: (e)**, which the Codex review of the decision memo supports. **Author ruling, 2026-10-18**
(`docs/reviews/amendment-10-r4/AUTHOR-RULINGS.md`): *"That's it.  The other three items, while dense, seem rational
are accepted."* And, confirming the owner's reading that this adopts A10.1.1, A10.4 option (e) with A10.4.1 and
A10.4.2: *"Yes. That's my understanding.  I focused on reading those sections of the document.  A 10.4.2 stood out
because you disagreed, but even for those where you were in agreement, I read what was proposed and accepted the
recommendation as being "rationally based.""* The author therefore adopted option (e), including option (a)'s clause
and boundary (rows 15–16) and A10.4.1. If the listing is later cut for schedule reasons while A9.5's independent
release boundary is established, (a) applies and the absence of new-key protection is stated (row 33). Release-key
custody (A10.4.2) is a separate ruling and applies under every option. *The earlier draft's recommendation, (a) with
option (c)'s mechanism registered as a named V2 obligation, is withdrawn.* Timestamp authorities and a witnessed
append-only log of key assertions are recorded as **candidates only**; neither creates an obligation in V1, V2 or
later.

### A10.4.1 Protection against key substitution (option (e)) — AUTHOR ADOPTED 2026-10-18 (recommended by the owner and Codex), BROADEN

Source: the decision memo, Part 2 and Part 3; its Codex review, F05, F07 and "Questions checked" 2–3. Mechanism
details are the memo's. Adopted by the author with option (e) on 2026-10-18 (A10.4, author ruling).

**Mechanism.** The trust configuration gains `service_keys`, an array of
`{domain, kms_fp, gpg_fp, not_before, not_after, sources}` entries. Endpoints are finite, with
not_before ≤ not_after. Fingerprints are canonical; entries are unique; the array has an explicit sort order.

**Ordered classifier** (one new check; one new reason code, `SERVICE_KEYS_NOT_LISTED`; `TRUST_HORIZON` exists):

> First, an exact match on D, both canonical fingerprints and both inclusive window endpoints passes this check.
> Otherwise, overlap with any listed window **or** not_before ≤ as_of yields INVALID / SERVICE_KEYS_NOT_LISTED.
> Otherwise yield UNVERIFIABLE / TRUST_HORIZON. Overlap includes a shared endpoint. Overall verdict and reason use
> the registered failure precedence, not an early return from this check.

**Authorization closure:**

> The initial release independently authorizes and records the complete service-key schedule through as_of. Later
> releases retain every existing entry unchanged, introduce no overlapping interval, and add an entry only if its
> not_before is strictly greater than the previous as_of. Thus absence through a past horizon is permanently
> closed. Completeness concerns authorized entries, not arbitrary channel assertions. The release authority must
> not authorize a new service-key tuple solely because the two potentially captured channels assert it.

**Issuer invariant.** No receipt ships under keys that are not listed in a published release.

**Chain-order pre-commitment of the listing — OWNER DECISION 2026-10-18, BROADEN; narrowed before signing after
review r4 (NARROW-CLAIM of an owner proposal).** It is part of option (e), which the author adopted on 2026-10-18
(A10.4). The fourth Codex review (`docs/reviews/amendment-10-r4/CODEX-REVIEW.md`, R4-01 to R4-04) found the owner
proposal as first drafted too broad; its text below applies Codex's exact corrections. The narrowing was applied
after the author's ruling, and the author was told of it before signing. *Gap:* the listing is release-signed but
not tied to time. A release key stolen decades later can sign a forked, internally consistent release chain that
lists the thief's keys for a past window; authorization closure protects only along the authentic chain. *Rule,*
mirroring C4's git rule:
- Every verifier release is OpenTimestamps-stamped over the SHA-256 of its trust configuration.
- A receipt's service keys count as listed only if the release that **first** lists their exact entry has a
  qualifying anchor (A10.5) at a lower height than the receipt's selected anchor: `h_release + 5 < h_receipt`, the
  same convention as C4.
- The bundle does not carry the release. The verifier receives the listing evidence with the installed trust file,
  as the listing-evidence package below states.

**Scope of the retrospective protection (R4-01).** The retrospective protection requires a conforming verifier and
independently authenticated Bitcoin history for both selected anchors and their six-header segments. The receipt,
listing, snapshot and git proofs must use the same independently authenticated history. For this theft protection,
a signature under the possibly stolen release key is not sufficient pin authentication. Compare every used pin with
independently validated Bitcoin history, or with a previously retained, independently authenticated genuine release
that covers that height. An earlier release with no pin at the height supplies no witness. A party unable to
establish this history has not established the retrospective protection. Authenticating only the bootstrap
public-key fingerprint does not distinguish a fork signed with the stolen genuine key. An independently retained
genuine release/configuration commitment can distinguish such a fork to the extent of its recorded contents and
ancestry. A9's separate distribution-compromise boundary stays: an attacker-signed executable can simply omit the
rule. The historical check is evaluated by a trusted conforming verifier; it does not authenticate arbitrary newly
acquired code after release-key theft. A later release-key theft can still issue new bad releases.

**Initial-window bootstrap (R4-02).** Initial-window bootstrap: publish the authenticated initial listing release C0
and stamp SHA256(C0). After its selected inclusion block and five successors exist, publish an append-only release
C1 whose configuration pins those six headers and whose installed listing evidence includes C0 and its completed
proof. Before issuing the first receipt, make that usable release/evidence available. The receipt must select a
height strictly greater than h_C0+5. C1 retains the exact entry unchanged; its own later stamp is not the
first-listing witness for that entry. This adds a confirmation wait, at least one pin-extension release for
bootstrap, and custody of the listing evidence. Under this sequence an honest first-window receipt can satisfy the
rule. For later windows, an installed configuration with coverage of the first-listing stamp is required before
issuance; merely submitting or publishing a release stamp does not supply that coverage. The single-window and
separately registered successor boundaries stay.

**Listing-evidence package (R4-03).** An installed, archived listing-evidence package, outside the receipt bundle,
contains:
- The canonical first-listing configuration, its authenticated release/archive binding and signatures, its completed
  OTS proof, and raw headers for its selected six-header segment. A10.5's selection rules apply to this fourth proof
  using a specified installed header pool; the profile states how that pool combines with bundle headers and how
  conflicting duplicates are handled.
- A release-authenticated manifest mapping each exact service-key/window tuple to the first-listing configuration's
  SHA-256. The release checker establishes that reference against the authenticated predecessor chain, verifying
  that the entry is absent before its introducing release and retained unchanged afterward. The intervening
  configurations and authentication/key-transition evidence needed to reproduce that check are preserved; they are
  never fetched implicitly from Tessera during offline verification.
- Independently authenticated history/pin evidence as R4-01 requires, plus the independently retained bootstrap
  record identifying the production key and original genuine baseline. A signature freshly verifiable under the
  stolen key is not historical provenance. The actual verifier/specification/catalog and current configuration used
  for the original verdict are retained, alongside the receipt bundle and its original three proofs/headers. Any
  separate safe-before/theft-cutoff assessment stays outside the stable six, as A9.4 requires.
- *Declared inputs.* The exact listing-evidence manifest, proof/header bytes and independent-history inputs are
  declared verification inputs. Their content hashes are recorded with the existing configuration/spec diagnostics.
  Exact reproduction requires the same bytes and policy; replacing a proof, supplying missing headers or changing
  history witnesses is a declared-input change. No network lookup may silently affect the stable result.

*Holder instruction* (relying-party text): preserve this package with the receipt, including the release that first
lists the exact entry and its proof. Failure to retain evidence is not evidence of fraud. These are required inputs
to the check, not a claim that dead-project reconstruction has been demonstrated.

**Failure cases and reporting (R4-04).** The reporting insertion goes after existing row 15.2 and before 16.1 of the
profile's total check order, preserving all existing rows' relative order: the tuple classifier first, then these
listing subchecks in this order.

| Listing subcheck | Outcome |
|---|---|
| First-listing configuration/reference authentic and internally consistent | Provisioning prerequisite under the existing trust-authentication refusal rule; missing or invalid required configuration/manifest gives `TRUST_CONFIG_UNAUTHENTICATED`, no receipt verdict. This does not include the separately supplied OTS proof, whose absence is handled below. |
| Listing OTS proof present | Absent: `UNVERIFIABLE / LISTING_PROOF_MISSING` |
| OTS grammar/bounds/message sizes | Malformed: `INVALID / OTS_FORMAT` |
| Detached file digest equals SHA256 of the canonical first-listing configuration bytes | Mismatch: `INVALID / LISTING_STAMP_MISMATCH` (additional proposed code) |
| No contradicted branch | `INVALID / OTS_MERKLE_MISMATCH` |
| Qualifying attestation and selected h_release | None: `UNVERIFIABLE / HEADERS_MISSING`, or `ANCHOR_PENDING_ONLY` for pending-only proof |
| Selected-height transaction/path subset | Apply the snapshot/git parts (1), (2), (4), with `INVALID / OTS_TX_SHAPE`; no receipt-txid comparison |
| h_release+5 < h_receipt | False with both heights available: `INVALID / LISTING_NOT_PRECOMMITTED`; otherwise blocked by the earlier unavailable input, with no invented order-failure reason |

Header rows 10.1–10.3 extend to the explicitly defined installed listing-header inputs, with deterministic
source/path ties for duplicate or conflicting evidence. Every new row has its necessary-input dependencies; the
tuple match uses the parsed domain/fingerprints/window, not successful DNSSEC authentication, as a prerequisite. The
classifier's position is registered, so `SERVICE_KEYS_NOT_LISTED` is not unordered. The existing
first-failed/else-first-unperformable aggregation applies, and independent receipt-anchor evaluation continues to
determine T. Agreement cases (prospective conformance obligations): missing listing proof plus an invalid signature;
bad listing order plus `ISSUANCE_WINDOW`; wrong listing digest; missing listing headers; and the first-window C0/C1
sequence. These profile changes are made after this amendment's signing commit.

**Verdict stability.** Passes and both INVALID conclusions of the **tuple classifier** survive every allowed append.
An UNVERIFIABLE result may later pass, as A9.5 permits. This does not extend to the height comparison: pin
extensions can qualify a previously nonqualifying earlier attestation and change the selected height. A9.4's contract
stays identical output for identical complete declared inputs, the configuration and listing evidence included, and
pin extensions can still change selection, T and U across releases. Historical-security assessments stay separate.

**V1's single window.** A9.6 registers one window. V1's configuration lists exactly one entry, authorized at the
freeze. A successor window needs a release that lists it, authorized before it opens, in addition to A9.6's
rotation registration.

**Scope.** The protection covers relying parties who run an authentic verifier release whose trust configuration
lists D's service keys. "Authentic" means authenticated distribution plus trustworthy release-authority behaviour;
uncompromised key storage alone does not validate an authorization decision. Within this scope, a captor of both
channel credentials who lacks release authorization cannot make a receipt under keys other than those listed pass
V1. Such a receipt is INVALID when its window overlaps a listed window or starts at or before the configuration's
`as_of`, and UNVERIFIABLE otherwise.

**Limits.**
- It prevents acceptance by those relying parties. It does not ensure that anyone detects or publicly exposes a
  capture. It provides no issuer detection and no public visibility.
- A horizon result means the keys are not yet covered. It is not proof of a takeover.
- Release-key compromise is distribution compromise, already a stated boundary. A captor with both channels and the
  release key can ship a release that lists its own keys. A release delivered to one party is not detectable by
  others.
- A stale trust file gives an honest new-window receipt `UNVERIFIABLE / TRUST_HORIZON`, a safe false reject until
  the relying party updates. This cannot occur in V1, which has one window.
- A8.3 and A8.5 supply no evidence for this property, and no formal model run supports it. Its evidence is the
  check's construction plus prospective vectors (memo, Part 3, row 5), which are exit evidence once registered.

**Change accounting.** This is a BROADEN, not a wording correction. C4 gains a third authenticated source for the
key set, the release. The adversary text gains a protection, within the scope above. The scenario mapping's
verdicts are unchanged; a fresh captor-key receipt is deliberately a newly rejected case. The signed bytes, the P8
encoding, `A_sig`, the existing two-channel checks and every existing reason code are unchanged. The specification
hash changes. Adding the listing to the cut order is a gate and scope change and is labelled as one (row 33). The
changed sentences are rows 25–33 and 37–39 of A10.7.

### A10.4.2 Release-key custody — AUTHOR ADOPTED 2026-10-18 (recommended by the owner and Codex; gate timing by owner proposal, 2026-10-17), GATE

Source: the decision memo, Part 2 ("Release independence"); its Codex review, F05; `docs/V1-PROFILE.md` §5 and
§14.2 items 1–2; the custody review `docs/reviews/custody/CODEX-REVIEW.md` (C01 and C02, HIGH); the owner's timing
proposal of 2026-10-17, recorded here. This section applies under every option of A10.4.

**Author ruling, 2026-10-18** (`docs/reviews/amendment-10-r4/AUTHOR-RULINGS.md`): *"That's it.  The other three
items, while dense, seem rational are accepted."* And, confirming the owner's reading that this adopts A10.1.1,
A10.4 option (e) with A10.4.1 and A10.4.2: *"Yes. That's my understanding.  I focused on reading those sections of
the document.  A 10.4.2 stood out because you disagreed, but even for those where you were in agreement, I read what
was proposed and accepted the recommendation as being "rationally based.""*

- **Prerequisite.** Independence of the release key from the DNS credential, the repository key and the issuing AWS
  account is an existing prerequisite of A9.5's trust-configuration authority (A9:326-332). It already protects
  V1's KSKs, repository trust and header pins against the channel captor, with or without the listing. It is still
  OPEN (profile §14.2 item 1; YubiKey 2 is not in hand).
- **Custody form.** Hardware or offline-software custody of the release key is acceptable **only** with a written
  custody and release-authorization procedure. The procedure states who authorizes releases, where signing occurs,
  and how backups stay outside the operational environment of the service. After the custody review it must also
  state (C01) the independent review-and-build environment that checks each candidate release against an approved
  baseline kept outside the operational environment and binds approval to the exact archive hash, and (C02) the
  controlled media crossing into and out of the signing session. The dated custody record names the procedure.
- **Hardware is not independence.** Buying hardware alone does not establish independence.
- **When: the first public verifier release, not the freeze.** The custody review found that real independence
  needs an independent review-and-sign environment and a controlled media crossing (C01, C02), which cannot be ready
  by 30 Oct. The *first public verifier release* is the first verifier release signed by the production release key
  and offered to relying parties.
  - **Frozen at the 30 Oct freeze:** this requirement; the release format (the release archive, the release-signature
    format, and how the trust-file hash binds to the release; profile §14.2 item 2), which must be frozen by 30 Oct;
    and the custody procedure's required contents (the bullet above).
  - **After the freeze, before the first public verifier release** (target: before the 20 Nov issuance milestone):
    the environment is built and rehearsed, the written procedure is reviewed, and independence is established.
- **Test releases.** Every verifier release made before that gate is signed with a separate TEST release key. Its
  public key is never published as the release key, never named in the freeze record or relying-party text, and
  never introduced by a production release. A pre-gate TEST signature cannot authenticate a production release.
  Production authentication must use the independently authenticated production release key and must reject TEST
  authority, including TEST provisioning overrides. This does not protect a user who skips authentication or
  acquires a substituted initial key.
  - *Offering restriction.* No pre-gate artifact is offered for production reliance: pre-gate releases are offered
    only as TEST releases, never as releases on which relying parties may rely.
  - *Required rehearsal.* Before the first public verifier release, a rehearsal must show that an otherwise correct
    archive with only a TEST signature is refused by the production acquisition and verification procedure,
    including when the TEST key is supplied through the test interface (profile §3.5's provisioning override).
    Missing or substituted bootstrap authority is not accepted as production merely because a signature verifies.
  - Profile §3.5 binds no production release; it supplies no evidence that the production path excludes TEST
    provisioning. The rehearsal is that evidence.
- **Risks and mitigations** (owner's proposal):
  1. *Schedule.* The schedule risk moves later. Mitigation: start preparing the environment and procedure early.
  2. *Post-freeze specification change.* Avoided: the release format is frozen by 30 Oct.
  3. *Convenience release* (a release signed outside the procedure because the environment is not ready). Closed for
     production authentication by the test-release rule and its rehearsal above.
  4. *The author's time in November.* Accepted by the author, 2026-10-17: *"(4) is acceptable to me"*. This
     accepted that risk only; his ruling on A10.4.2 is the 2026-10-18 ruling above.
  5. *Relying parties.* No pre-gate artifact is offered for production reliance (the offering restriction above),
     and production authentication rejects TEST authority. A user who skips authentication or acquires a substituted
     initial key is not protected; that is the existing distribution boundary (A9.5).
- **Bootstrap record.** Profile §5 and runbook §6 put the release public key's fingerprint in the freeze record.
  Under this timing the production release key need not exist at the freeze. Its fingerprint is therefore recorded
  in a dated first-production-release bootstrap record that identifies the original freeze baseline and the actual
  production key. The original freeze record is preserved; it is not amended to claim that the fingerprint was
  present on 30 Oct. Profile §5, §14.2 items 1–2 and runbook §6 are reconciled with this split between registration
  at the freeze and execution before the first public verifier release, after this amendment's signing commit.
- **Fallback.** If independence cannot be established before the first public verifier release, the author receives
  a NARROW-MODEL of the channel-capture claim (A9:41-42, as amended by rows 15 and 25) before that release. Cutting
  the listing does not cure it. A custody failure is never an automatic, invisible reversion of the threat model.

The changed sentences are rows 34–36 of A10.7.

## A10.5 Attestation selection, in stages — OWNER DECISION, CLARIFY (review A05)

C5 selects "the verified attestation at the lowest block height in the presented OTS proof" (:144). C6 says "A
selected anchor (C5) beyond the newest pin is `UNVERIFIABLE`", "Every supplied header must be pinned" and "An
unselected attestation without its headers supplies no fact and is not a failure" (:145). "Verified" can be read
with or without pin coverage. The profile already fixes one order (`docs/V1-PROFILE.md` §7.1–§7.2, OWNER
2026-10-14, G05, G07, G23; precedence rows 10–11). This amendment states that order as A9's meaning.

These stages explain qualification and selection within the existing verifier. They do not replace other
registered checks, their dependencies, or dispatch and reason-code precedence. A failure of an independently
performable required check takes precedence over an unperformable check under A4.2. The header-pool link checks,
OTS grammar and stamp checks, and selected-height transaction/path checks remain unchanged. A stage's UNVERIFIABLE
entry is an unperformable-check result, not an early return that suppresses other checks.

**Stages**, for each of the receipt, snapshot and git proofs:
1. **Header pool.** Every supplied header, used or not, is checked against the pins. A header at a height with no
   pin gives `UNVERIFIABLE / HEADERS_NOT_COVERED`; a header that differs from its pin gives `INVALID /
   HEADER_CONFLICTS_PIN`.
2. **Qualification ("verified").** A Bitcoin attestation at height h qualifies only if the bundled header at h has
   a merkle root equal to the attestation message, headers h … h+5 are all bundled, each equals its pin, and each
   links to the one before. Pin coverage is part of "verified". A pinned header at h whose merkle root contradicts
   the attestation gives `INVALID / OTS_MERKLE_MISMATCH`.
3. **Selection.** The selected anchor is the qualifying attestation at the lowest height h*. T and the confirmation
   count come from h*. A non-qualifying attestation, including one without headers or one beyond the newest pin,
   is never selected; it supplies no fact and is not a failed check, except as stages 1–2 state. A failed check at
   h* never moves selection to a higher height.
4. **No qualifying attestation.** The check is unperformable (`HEADERS_MISSING`, or `ANCHOR_PENDING_ONLY` if only
   pending attestations; `SNAPSHOT_NOT_ANCHORED` and `GIT_NOT_ANCHORED` for those proofs). The overall verdict is
   `UNVERIFIABLE` unless another independently performable required check fails, in which case it is `INVALID`
   under A4.2.

**Cases**, each subject to A4.2 precedence over any other failed check. A qualifying path at h = 100 and a lower,
headerless attestation at h = 90: h* = 100. A sole attestation beyond the newest pin, without headers: stage 4,
unperformable. The same with its headers supplied: stage 1, `HEADERS_NOT_COVERED`, unperformable. So C6's
"selected anchor beyond the newest pin" cannot arise; an anchor beyond the pins makes a check unperformable through
stage 1 or stage 4. The assembled C5 claim cell is in A10.1. The changed sentences are rows 17–18 of A10.7.

## A10.6 The DNS owner name is `_tessera-v1.<D>` — OWNER DECISION, CORRECT (review A06)

C4 says "DNSSEC (owner name D, …)" (:143). In DNS, the owner name is the complete name that owns the record. The
encoding A9 adopts (:149) requires the owner `_tessera-v1.<D>`, where D is `common.issuer` (ENCODING-V1 §7, :551 at
A9's signing commit `2ad3489`, :562 in the workspace), compared as a label sequence (:623-624 at `2ad3489`, :634-635
in the workspace). A9.6 (:414-415) already rejects a substituted per-key owner. Read
literally, "owner name D" names `wamason.com`, the wrong record. For V1 the owner is `_tessera-v1.wamason.com`. The
changed sentence is row 19 of A10.7.

## A10.7 What changed

**Registered sentences changed.** Paths are `docs/` unless given; "A9" is `phase-0-prereg-amendment-9.md`, at its
signing commit `2ad3489`. Quotation marks mark exact source words. The A9.7 kind column uses A9.7's letters (R
replaced or narrowed; K clarified; G gate or trigger moved) and one letter A9.7 does not have: **B**, broadened.
Every change applies to `tessera-v1-strict` only. A row whose source cell begins "(no sentence" adds text where A9
has none. Rows 15–16 and 20–39 are **AUTHOR ADOPTED 2026-10-18**, each with its recommendation provenance; the
author's words are in the status block.

| # | Registered sentence | file:line | Replacement | Kind | A9.7 kind |
|---|---|---|---|---|---|
| 1 | "and that the bytes *and both signatures* existed no later than a time T fixed by Bitcoin" | A9:36-37 | "and that the bytes *and both signatures* existed before the Bitcoin block that fixes a time T was mined; T is that block's header time, a chain-time value, not a bound in UTC" (A10.1) | NARROW-CLAIM | R |
| 2 | "no later than time T" (success definition 1) | A9:114 | "before the selected Bitcoin block was mined; its header time T is not a UTC upper bound" (A10.1) | NARROW-CLAIM | R |
| 3 | "the signed frames and their exact signatures existed no later than T" | A9:133 | "the signed frames and their exact signatures existed before the selected Bitcoin block was mined, that is, no later than T in chain time" (A10.1) | NARROW-CLAIM | R |
| 4 | "The frames **and their exact signatures** existed no later than T" | A9:144 (C5) | A10.1's assembled C5 claim cell | NARROW-CLAIM | R |
| 5 | "these bytes were presented to Tessera by T" (scenario a, g) | A9:177 | "these bytes were presented to Tessera before the selected Bitcoin block was mined; its header time T is not a UTC upper bound" (A10.1) | NARROW-CLAIM | R |
| 6 | "this signed contract existed by T." (scenario i) | A9:186 | "this signed contract existed before the selected Bitcoin block was mined; its header time T is not a UTC upper bound." The parties' signature-checking duty stays (A10.1) | NARROW-CLAIM | R |
| 7 | "A signature made after T cannot fit the anchor." | A9:294-295 | "A signature made after the selected Bitcoin inclusion block was mined cannot fit that block's anchor under the registered commitment and history assumptions." (A10.1) | NARROW-CLAIM | R |
| 8 | "A receipt whose exact signatures are anchored by T" | A9:433 | "A receipt whose exact signatures are committed by the selected Bitcoin inclusion block" (A10.1) | NARROW-CLAIM | R |
| 9 | each "before T" in guarantee 1 (three uses) | A9:436-439 | "before inclusion in that block"; the remaining conditions and `historical_security: NOT_EVALUATED` stay (A10.1) | NARROW-CLAIM | R |
| 10 | "and were allowed to issue during a stated window" | A9:36 | "and stated an issuance window for them" (A10.2); the sentence after it, which gives the two comparisons, stays | NARROW-CLAIM | R |
| 11 | "**Signing capability mints only inside the window, in chain time.**" | A9:441 | "**Signing capability cannot mint a receipt that passes V1 with verified T after the window's not-after, in chain time.**" The body stays (A10.2) | NARROW-CLAIM | R |
| 12 | "**Issuance window.**" | A9:407 | The name stays; it names the record's two values and asserts no issuance inside the interval; the verifier establishes only C4's two comparisons (A10.2) | CLARIFY | K |
| 13 | "Bitcoin history deeper than k" | A9:49-50 | "Bitcoin history to a reorganization depth of k or more" (A10.3) | NARROW-CLAIM | R |
| 14 | "Reorganization deeper than k is a residual." | A9:144 (C5) | "A reorganization of depth k or more, which can remove a block with k confirmations, is a residual." (A10.3) | NARROW-CLAIM | R |
| 15 | "anyone who captures authority-channel credentials while signing capability stays uncompromised (A8.3's sense of capture);" | A9:41-42 | A10.4's recommended adversary clause (honest signed material, before or after credential disclosure). Takes effect on option (a) or (e). **AUTHOR ADOPTED 2026-10-18** (recommended by the owner and Codex) | NARROW-CLAIM | R |
| 16 | (no sentence; "The boundaries" names no limit on new receipts after capture) | A9:45-52 | A10.4's recommended boundary: no prevention of new receipts under a captor's key assertion; publication remains an issuer duty; V1 does not guarantee that a captor publishes the assertion, that capture is detected, or that new receipts are publicly visible. Takes effect on option (a) or (e); under (e) its first sentence is as row 26 gives it. **AUTHOR ADOPTED 2026-10-18** (recommended by the owner and Codex) | NARROW-CLAIM | R |
| 17 | "the verified attestation at the lowest block height in the presented OTS proof" | A9:144 (C5) | A10.1's assembled C5 claim cell (qualifying attestation, A10.5's stages) | CLARIFY | K |
| 18 | "A selected anchor (C5) beyond the newest pin is `UNVERIFIABLE`." and "An unselected attestation without its headers supplies no fact and is not a failure" | A9:145 (C6) | "An attestation beyond the newest pin never qualifies. If no attestation qualifies, or a supplied header is at a height with no pin, the applicable check is unperformable (A10.5 stages 1, 4); the overall verdict is UNVERIFIABLE unless another independently performable required check fails, in which case it is INVALID under A4.2. Existing reason-code precedence is unchanged." and "A non-qualifying attestation supplies no fact and is not a failure, except as A10.5 stages 1–2 state." | CLARIFY | K |
| 19 | "DNSSEC (owner name D, evaluated at the snapshot's own anchored time)" | A9:143 (C4) | "DNSSEC (for the fixed authority-record owner `_tessera-v1.<D>`, compared as a label sequence (ENCODING-V1 §7); for V1, `_tessera-v1.wamason.com`; evaluated at the snapshot's own anchored time)" (A10.6) | CORRECT | K |
| 20 | (no sentence; the opening claim states no UTC bound) | A9:32-38 | After row 1's replacement: "Under assumption A-UTC, which the verifier does not check and V1 does not establish, the bytes and both signatures also existed before U = max nTime(h* … h*+5) + 7200 s, in UTC; V1 reports U only in `utc_assessment`, beside A-UTC's identifier, never as a stable field." (A10.1.1) **AUTHOR ADOPTED 2026-10-18** (recommended by the owner and Codex) | BROADEN | B |
| 21 | (no sentence; C5 states no UTC bound) | A9:144 (C5) | Claim: A10.1.1's recommended claim text, after A10.1's assembled cell. Non-claim added: "U is conditional on A-UTC, which the verifier does not check; U enters no verdict, reason code or stable field." (A10.1.1) **AUTHOR ADOPTED 2026-10-18** (recommended by the owner and Codex) | BROADEN | B |
| 22 | (no item; the profile list names no output outside the stable field set at :162) | A9:148-165 | Added after "*Stable field set*": "*UTC assessment* (outside the stable field set): `utc_assessment` with `assumption_id: "A-UTC-7200-6"` and `utc_upper_bound`, as A10.1.1's output contract states; Δ = 7200 s and m = 6 frozen in the specification catalog." (A10.1.1) **AUTHOR ADOPTED 2026-10-18** (recommended by the owner and Codex) | BROADEN | B |
| 23 | "Translating this into a finite UTC cutoff requires an additional, explicit backward-skew assumption that V1 does not establish: A2.1 registers no finite bound on B − C, and neither ε nor S is one." | A9:444-446 | The sentence stays. Added: "A-UTC (A10.1.1) is such an assumption, registered only for the UTC assessment of existence (U). V1 still does not establish it, and guarantee 2 keeps its chain-time meaning; it is not translated to UTC." **AUTHOR ADOPTED 2026-10-18** (recommended by the owner and Codex) | CLARIFY | K |
| 24 | (no sentence; "The boundaries" names no UTC assumption or timestamp rollover) | A9:45-52 | Added: "The UTC assessment rests on A-UTC. The signature adopts this trust assumption; it does not establish that miners satisfy it. A-UTC is false exactly when every one of the six confirming blocks has a header time more than 7200 s before its production. In that case the conditional UTC guarantee is unavailable; the computed value need not itself be false. Its 64-bit arithmetic covers preserved headers; timestamp representation for Bitcoin blocks produced after the 2106 rollover is a Bitcoin protocol matter outside V1." (A10.1.1; limit of rows 20–22) **AUTHOR ADOPTED 2026-10-18** (recommended by the owner and Codex) | CLARIFY | K |
| 25 | (no sentence; the adversary clause, as row 15 gives it, names no protection against new receipts under captor keys) | A9:41-43 | Added after row 15's clause: "against a relying party running an authentic verifier release whose trust configuration lists D's service keys, a captor of both channel credentials who lacks release authorization cannot make a receipt under keys other than those listed pass V1. Such a receipt is INVALID when its window overlaps a listed window or starts at or before the configuration's `as_of`, and UNVERIFIABLE otherwise." (A10.4.1) Option (e) only. **AUTHOR ADOPTED 2026-10-18** (recommended by the owner and Codex) | BROADEN | B |
| 26 | Row 16's first sentence ("V1 does not prevent a captor of both required authority-channel credentials from issuing new receipts …") | A9:45-52 (as row 16 adds) | "V1 does not prevent a captor of both required authority-channel credentials from issuing new receipts under a key assertion that names the captor's own keys; such receipts do not pass V1 for a relying party in row 25's scope. Release-key compromise is distribution compromise. A release delivered to one party is not detectable by others. V1 provides no issuer detection, and does not ensure that anyone detects or publicly exposes a capture." The rest of row 16 stays. (A10.4.1) Option (e) only. **AUTHOR ADOPTED 2026-10-18** (recommended by the owner and Codex) | BROADEN | B |
| 27 | "The verifier fixes the required set." (C4, claim cell) | A9:143 (C4) | Added after it: "The release-signed trust configuration lists D's authorized service-key schedule; the receipt's key pair and window pass only by an exact listed match, under A10.4.1's ordered classifier (`SERVICE_KEYS_NOT_LISTED`, `TRUST_HORIZON`)." Non-claim added: "The listing gives non-acceptance within A10.4.1's scope, not issuer detection or public visibility." Option (e) only. **AUTHOR ADOPTED 2026-10-18** (recommended by the owner and Codex) | BROADEN | B |
| 28 | "root KSK-2017 and KSK-2024 with separate publication, signing and reliance periods; the repository key; a signed, versioned set of pinned mainnet header hashes." (trust configuration) | A9:154-155 | Adds: "; the authorized service-key schedule for D (`service_keys`: domain, both canonical fingerprints, inclusive window, sources), as A10.4.1 states" Option (e) only. **AUTHOR ADOPTED 2026-10-18** (recommended by the owner and Codex) | BROADEN | B |
| 29 | "*Issuer invariant:* a receipt ships only when complete; an operator refusal never concerns a shipped receipt." | A9:165 | Adds: "No receipt ships under keys that are not listed in a published release." (A10.4.1) Option (e) only. **AUTHOR ADOPTED 2026-10-18** (recommended by the owner and Codex) | BROADEN | B |
| 30 | "Capture of an authority-channel credential grants no ability to sign a release, authorize a configuration hash, or replace the compiled trust root." | A9:330-331 | Adds: "The release authority must not authorize a new service-key tuple solely because the two potentially captured channels assert it." (A10.4.1) Option (e) only. **AUTHOR ADOPTED 2026-10-18** (recommended by the owner and Codex) | BROADEN | B |
| 31 | "KSKs, header pins and repository keys are never removed, and finalized period endpoints never change." | A9:333-334 | Adds service-key entries to the append-only list, with A10.4.1's authorization closure: the initial release authorizes the complete schedule through `as_of`; later releases retain every entry unchanged, add no overlapping interval, and add an entry only if its not_before is strictly greater than the previous `as_of`. Option (e) only. **AUTHOR ADOPTED 2026-10-18** (recommended by the owner and Codex) | BROADEN | B |
| 32 | "This amendment registers the first issuance window only; it does not yet authorize successor issuance." | A9:410-411 | Adds: "V1's trust configuration lists exactly one service-key entry, authorized at the freeze. A successor window also needs a release listing it, authorized before it opens." (A10.4.1) New timing prerequisites of the listing. The successor requirement remains conditional on a separately registered rotation; it creates no automatic successor project. Option (e) only. **AUTHOR ADOPTED 2026-10-18** (recommended by the owner and Codex) | GATE | G |
| 33 | "and nothing else is on the list" (cut order) | A9:211-213 | "the second item cut is the service-key listing (A10.4.1). If it is cut while A9.5's independent release boundary is established, A10.4 option (a) applies and the absence of new-key protection is stated. Cutting it does not cure a failure of release-key independence (A10.4.2). The rest stays required." A gate and scope change. Option (e) only. **AUTHOR ADOPTED 2026-10-18** (recommended by the owner and Codex) | GATE | G |
| 34 | "Releases are authenticated by a key that neither the DNS credential, the repository key nor the issuing AWS account can use; the dated custody record names that key and its access boundary." | A9:328-330 | Adds: "This independence is a prerequisite. Hardware or offline-software custody is acceptable only with a written custody and release-authorization procedure that states who authorizes releases, where signing occurs, and how backups stay outside the operational environment; the procedure also states the independent review-and-build environment and the controlled media crossing into and out of the signing session, and the custody record names it. Buying hardware alone does not establish independence. The gate is the first public verifier release, not the freeze: the 30 Oct freeze registers this requirement, the release format (release archive, release-signature format, and how the trust-file hash binds) and the procedure's required contents; the environment is built and rehearsed, the procedure reviewed and independence established after the freeze and before the first public verifier release (target: before the 20 Nov issuance milestone). The production key's fingerprint is recorded in a dated first-production-release bootstrap record that identifies the original freeze baseline and the actual production key; the original freeze record is preserved." (A10.4.2) **AUTHOR ADOPTED 2026-10-18** (recommended by the owner and Codex) | GATE | G |
| 35 | (no sentence; A9 states no route if release-key independence cannot be established) | A9:326-332 | "If independence cannot be established before the first public verifier release, the author receives a NARROW-MODEL of the channel-capture claim before that release. Cutting the service-key listing does not cure it." (A10.4.2) **AUTHOR ADOPTED 2026-10-18** (recommended by the owner and Codex) | GATE | G |
| 36 | (no sentence; A9 states no rule for verifier releases made before release-key independence is established) | A9:326-332 | "Every verifier release made before the first public verifier release is signed with a separate TEST release key; its public key is never published as the release key, never named in the freeze record or relying-party text, and never introduced by a production release. A pre-gate TEST signature cannot authenticate a production release. Production authentication must use the independently authenticated production release key and must reject TEST authority, including TEST provisioning overrides. This does not protect a user who skips authentication or acquires a substituted initial key. No pre-gate artifact is offered for production reliance. Before the first public verifier release, a rehearsal must show that an otherwise correct archive with only a TEST signature is refused by the production acquisition and verification procedure, including when the TEST key is supplied through the test interface." (A10.4.2) **AUTHOR ADOPTED 2026-10-18** (recommended by the owner and Codex) | GATE | G |
| 37 | "**Chain-order pre-commitment** (…): the git assertion's selected anchor height plus 5 is lower than the receipt's selected anchor height" (C4, claim cell) | A9:143 (C4) | Added after it: "The release that first lists the receipt's service-key entry is OpenTimestamps-stamped over its trust-configuration SHA-256, and its selected anchor height plus 5 is lower than the receipt's selected anchor height; otherwise the listing subchecks of A10.4.1 apply (`LISTING_PROOF_MISSING`, `OTS_FORMAT`, `LISTING_STAMP_MISMATCH`, `OTS_MERKLE_MISMATCH`, `HEADERS_MISSING` or `ANCHOR_PENDING_ONLY`, `OTS_TX_SHAPE`, `LISTING_NOT_PRECOMMITTED`), in the order registered there." Non-claim added: "The retrospective protection requires a conforming verifier and independently authenticated Bitcoin history for both selected anchors and their six-header segments. The receipt, listing, snapshot and git proofs must use the same independently authenticated history. For this theft protection, a signature under the possibly stolen release key is not sufficient pin authentication. Compare every used pin with independently validated Bitcoin history, or with a previously retained, independently authenticated genuine release that covers that height. An earlier release with no pin at the height supplies no witness. A party unable to establish this history has not established the retrospective protection. Authenticating only the bootstrap public-key fingerprint does not distinguish a fork signed with the stolen genuine key. An independently retained genuine release/configuration commitment can distinguish such a fork to the extent of its recorded contents and ancestry." (A10.4.1, OWNER DECISION 2026-10-18, narrowed after review r4) Option (e) only. **AUTHOR ADOPTED 2026-10-18** (with option (e); owner decision 2026-10-18, narrowed after review r4) | BROADEN | B |
| 38 | "*Trust configuration* (ships with the verifier, never from the bundle)" | A9:154 | Adds to what ships with the verifier, never from the bundle: "an installed, archived listing-evidence package, outside the receipt bundle: for each exact service-key/window tuple, the canonical first-listing configuration, its authenticated release/archive binding and signatures, its completed OTS proof and the raw headers of its selected six-header segment; a release-authenticated manifest mapping each tuple to the first-listing configuration's SHA-256, established by the release checker against the authenticated predecessor chain, with the intervening configurations and authentication/key-transition evidence preserved; and independently authenticated history/pin evidence and the bootstrap record. These are declared verification inputs, hashed in the diagnostics; none is fetched from Tessera during offline verification." (A10.4.1, OWNER DECISION 2026-10-18, narrowed after review r4) Option (e) only. **AUTHOR ADOPTED 2026-10-18** (with option (e); owner decision 2026-10-18, narrowed after review r4) | BROADEN | B |
| 39 | "*Issuer invariant:* a receipt ships only when complete; an operator refusal never concerns a shipped receipt." | A9:165 | Adds, after row 29's sentence: "Every verifier release is OpenTimestamps-stamped. Before issuing any receipt in a window, an installed configuration with coverage of the stamp of the release that first lists the exact entry is available, with its listing evidence; for the initial window this is the C0/C1 bootstrap of A10.4.1, and the receipt selects a height strictly greater than h_C0+5." Relying-party text adds: "Preserve the listing-evidence package with the receipt, including the release that first lists the exact entry and its proof. Failure to retain evidence is not evidence of fraud." (A10.4.1, OWNER DECISION 2026-10-18, narrowed after review r4) Option (e) only. **AUTHOR ADOPTED 2026-10-18** (with option (e); owner decision 2026-10-18, narrowed after review r4) | BROADEN | B |

**Named and not changed:** every existing verifier check, reason code and precedence row; δ, ε, k, N, S; A2.1's
predicate, its refusal to bound B − C, and its `DepthK = k − 1` pin; ENCODING-V1, P8, `A_sig` and the signed frames;
the existing two-channel checks; A9.1's six-field stable set (:162) and A9.4's contract and verdict stability
(:267-283), since `utc_assessment` is outside the stable six; A9's "no lower time bound or priority" (:46-47); A8.3
and A8.5, which supply no evidence for option (e); A9.6's issuer invariant and guarantee 2's body, its chain-time
meaning and its capture proviso; A9's public-publication issuer duty ("Changed in effect", :495-500); the scenario
mapping's verdicts, fixtures and safe-decision categories. `docs/V1-PROFILE.md` is not changed by this amendment:
A10.5 states its existing order, and the profile changes that rows 20–39 would need (memo, Part 3, "Minimal spec and
verifier changes") are made after this amendment's signing commit. A1.6 (:485-505) stays standing: its clock wording is
qualified for V1 by A10.1, and its parenthetical "a reorganization deeper than k is out of model" uses the same
phrase as rows 13–14, while its governing clause ("anchors at depth ≥ k are treated as permanent") already matches
A10.3. A9's header still reads "PROPOSED"; its signing act is commit `2ad3489` under the house form, and this
amendment does not change that.

**In sum:** thirty-nine rows. Rows 1–14 and 17–19 are OWNER DECISIONS and add no mechanism. Rows 15–16 and 20–39 are
AUTHOR ADOPTED (2026-10-18). By kind: fifteen narrow claims (rows 1–11, 13–16), one correction to the registered
encoding (row 19), five clarifications (rows 12, 17, 18, 23, 24), thirteen broadenings (rows 20–22, 25–31, 37–39)
and five gate changes (rows 32–36; row 33 also states its scope change). The broadenings add mechanism: one reported
assessment and one named assumption (A10.1.1); one trust-file field, the tuple classifier and the ordered listing
subchecks, four reason codes, closure invariants, release stamping, the listing-evidence package and one issuer
invariant (A10.4.1). The scenario mapping's verdicts are unchanged; option (e) deliberately rejects new cases:
receipts under unlisted keys, and receipts whose listing was not pre-committed. No existing verdict, parameter or
vector is changed; the existing header checks extend to the installed listing headers (A10.4.1).

---

## Open items, not decided by this amendment

- **Ruled 2026-10-18, no longer open:** A10.1.1, A10.4 (option (e), with A10.4.1) and A10.4.2 (AUTHOR ADOPTED;
  see the status block).
- **Release-key independence** stays OPEN (profile §14.2 item 1) until the environment is built and rehearsed and the
  procedure is reviewed, before the first public verifier release (A10.4.2). The custody procedure itself is outside
  this amendment.
- **Profile, runbook and custody reconciliation** after the signing commit: the listing-evidence package, the
  listing subchecks and their total-order rows, the C0/C1 bootstrap, the bootstrap record, and the profile §5,
  §14.2 items 1–2 and runbook §6 timing.
- **Recorded as candidates, with no obligation:** RFC 3161 time-stamp authorities (memo, U2); a witnessed
  append-only log of key assertions, for the broader visibility objective that no option here meets.
- **Recorded as unresolved use requirements, not V1 obligations:** whether a court or another examiner will accept
  A-UTC; whether a particular use needs qualified timestamps.
