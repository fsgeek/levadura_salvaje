# Tessera — Phase 0 Pre-Registration, Amendment 2 — ADOPTED

> **Status: ADOPTED.** Signed and in force. Per Amendment 1 precedent,
> this document went through falsification-style non-author review (the A1.7
> discipline, applied to the amendment itself) before the author signed and
> committed it, OpenTimestamps-stamped for subsequent Bitcoin anchoring.
> Review artifacts and dispositions land in `docs/reviews/`.
>
> **What this document is.** The second amendment to the Phase 0
> pre-registration (`phase-0-prereg.md`, commit `75207ba`), layered on
> Amendment 1 (`phase-0-prereg-amendment-1.md`, commit `03cd3db`). The
> original and prior amendments are never edited; this document states what
> changes, and why, on the record.
>
> **Provenance.** Building the P5c issuance-protocol state machine
> (`formal/tla/P5c_IssuanceProtocol.tla`) forced a precision the registered
> prose did not have: "confirmed … within δ" admits a strict reading (depth
> k *reached* by `declared_issue_time + δ` — ratified below in its
> chain-time form: the designated k-th-confirmation block carries an
> in-window timestamp, the chosen proxy, not a wall-clock measurement of
> when burial occurred) and a permissive one (block
> time in-window, depth reached whenever). The fork was flagged in the
> module header per the recorded-decision rule, and resolved by the author
> on 2026-07-07 after an adversarial ratification dialogue with the AI
> collaborator (Claude, per §0/§6 division of labor). All decisions herein
> are the author's (Tony Mason).

---

## A2.0 What the model surfaced, and a correction registered with it

The state machine did what pre-registering models is for: it made a prose
ambiguity mechanically undeniable. The author ratifies the **strict**
reading — restated below on a chain-visible observable so that the issuer
and the verifier check the *same temporal conjuncts* (under the issuance
policy's tolerances; A2.1).

One correction from the ratification dialogue is registered alongside,
because leaving it implicit would invite a misreading of what the strict
rule protects. Consider the **abandoned-anchor artifact**: an issuance
attempt whose anchor lands in an in-window block but buries slowly; the
strict issuer discards and re-issues, yet the discarded transaction
persists and typically confirms later, so a complete, chain-verifiable
(receipt, anchor) pair exists that was never shipped. Checked against the
registered properties: this artifact violates **none of them** — none of
the **pre-Amendment-2 registered set**; A2.2 below changes exactly that
for the **chain-late subclass** (`confirmed_at > declared + δ`), which
it rejects. An operationally abandoned but **chain-valid** artifact
(predicate holds; no timely eligibility latch, so the attempt was
refused — possible under the A2.1 clock roles) is *not* rejected by
A2.2; it is governed by the A2.1/A2.4 standing rules: cryptographically
valid, evidentially admissible, no protocol standing. The
anchor's security content is the block time alone — backdating is bounded
because no forger can place bytes in a past block (P5), and P6's
uncertainty window is bounded by `anchor_time` because signing precedes
block inclusion. *When* depth k was reached enters neither argument. What
the depth-k-within-δ rule actually protects is different: no shipped
receipt can be orphaned by a tolerated reorganization (the P5c
`NoShippedOrphan` invariant), and the issuer's evidence trail stays free
of receipts whose completion needs explaining. The residue the artifact
does create — two verifiable receipts for the same content with different
declared times — is **not closed by this amendment** (correction,
2026-07-21: an earlier draft claimed closure via A2.2 and A2.4; that
argument silently assumed the fused clock, under which every discarded
attempt is chain-late. Under the ruled clock roles of A2.1 a discarded
attempt can be chain-valid, A2.2 rejects only late-burial artifacts, and
A2.4 confines standing without deduplicating content). Closure — a
lineage/equivocation-evidence mechanism or an explicit dedup rule — is
registered as an Amendment 3 obligation.

The ratified form strengthens P5 with a new verifier-side conjunct and
adds obligations; under A1.2's change discipline that requires this
amendment. No A1.2 property is weakened; the A1.1 falsifier is not
triggered (stated precisely in A2.6).

---

## A2.1 "Confirmed within δ": one predicate, both sides

**Vocabulary.** The anchor transaction is included in the block at height
`h`. Confirmation count follows the Bitcoin convention: the including
block is the first confirmation, so `c = tip_height − h + 1`, and the
block that grants the k-th confirmation has height `h + k − 1`. Define

    confirmed_at  :=  timestamp(block at height h + k − 1)

**The rule.** Issuance is complete only if

    confirmed_at  ≤  declared_issue_time + δ

The issuer evaluates this conjunct **as part of the full three-conjunct
temporal predicate** (the P5 temporal test inside `VALID_STRICT`; all
three A2.2 conjuncts — not the whole verdict, which contains more than
the temporal test) before shipping: under
skewed, non-monotonic block timestamps the confirmation conjunct does
not imply the anchor-time conjunct, so shipping on this conjunct alone
could ship a receipt the verifier rejects (surfaced by the bridge model,
`formal/tla/P5cP5P6_Bridge.tla`, 2026-07-21). The verifier evaluates the
same conjuncts on the same chain observables at verification (A2.2),
**under the issuance policy's tolerances**: the verifier-owns-tolerances
discipline permits stricter verifier values of either tolerance (a
stricter δ′ < δ, or a stricter ε′ on the anchor-time lower bound), and
such a verifier may reject honestly-shipped receipts — the
no-disagreement guarantee below is scoped to verification under the
issuance policy's δ and ε.
**Clock roles (ruling, 2026-07-21).** Chain time and wall time hold
separate, explicitly-ranked roles. **Chain time governs evidence:** the
three-conjunct predicate above, evaluated identically by issuer and
verifier on the designated blocks' timestamps. **Wall time governs the
attempt lifecycle:** the service waits through `declared + δ + S` before
treating an attempt as expired, where S ≥ 0 is an **operational slack
constant** joining δ, ε, k, N for ratification at Band 0 exit (working
default S = 24 h, sized to the observation path — outages and polling,
not timestamp skew alone). **No global bound on the backward observation
lag is assumed.** Writing C = `confirmed_at` and B = the service's
wall-clock observation of the designated block: Bitcoin consensus
provides no finite bound on B − C (median-time-past and the two-hour
future rule bound the forward direction only), and B additionally
absorbs the entire observation path — network and header-store delay,
polling, outage and recovery, wall-clock error. Registering a hard
bound would assert, at Phase 0, a property of an operational stack that
does not yet exist. Instead the guarantee is registered **conditionally
on the observable antecedent**: *if B − C ≤ S for an attempt whose
predicate holds, that attempt has a live shipping opportunity at
eligibility* (slack-parameter analysis,
`formal/tla/P5cP5P6_BridgeSlack.tla` and its `_Latch` variant;
predictions-first record in
`docs/reviews/2026-07-21-claude-predictions-slack-bench.md`). Since B
and C are both observable, a violated antecedent is a detectable
operating-envelope event, not a silently failed assumption. Timeliness
is **latched at eligibility**: an attempt eligible within the envelope
cannot be expired by later packaging or scheduling delay —
eligible/finalizing, shipped, and expired/refused are mutually
exclusive states (a construction obligation on the implementation,
registered with the ruling). An attempt whose lag exceeds S may be
refused; a chain-valid artifact of such an attempt remains
cryptographically valid and evidentially admissible but carries **no
protocol standing** (A2.4; enforcing that distinction against later
publication is Amendment 3's lineage/standing obligation). If
operational evidence later supports an SLA-style hard bound, it may
enter a **deployment profile** with monitoring and an explicit
violation outcome — never this pre-registration's assumption set. What
the opportunity guarantee buys is opportunity, not outcome: "every
timely-eligible attempt ships" is a contract obligation on the
implementation, the same proof-versus-contract split as A2.3's refusal.

**Boundary ties, registered per clock.** The chain-side predicate is
stateless: at exactly `confirmed_at = declared + δ` it holds, and holds
identically whenever evaluated — there is no chain-side race. The
wall-side boundary is **resolved by the latch, not raced** (round-3
repair, 2026-07-21: an earlier draft of this paragraph carried the
fused-clock race forward; under latched eligibility there is none).
Eligibility observed at exactly `B = declared + δ + S` is timely — the
boundary is **inclusive and latch-winning**, matching the mechanized
form (`burialAtWall <= declared + Delta + Slack` in the `_Latch`
companion) — so such an attempt latches eligible/finalizing and cannot
expire. Expiry (on the final attempt, refusal) applies only **strictly
after** the boundary, and only to attempts with no timely-latched
eligibility. Atomicity of the latch against the expiry transition is
part of the mutual-exclusion construction obligation (A2.3). If the
predicate fails at issuance time, the attempt is discarded and
re-issued per the P5 corollary, subject to the attempt bound of A2.3.

**Why chain time on both sides.** A wall-clock ship rule ("ship if depth k
by `now ≤ declared + δ`") and a block-timestamp verifier check can
disagree at the δ boundary by the consensus-bounded skew (block timestamps
may run up to about two hours ahead of network-adjusted time). Defining
the rule once, on the chain-visible quantity, removes the divergence: **no
honestly-shipped receipt can fail the verifier's confirmation conjunct
under the issuance policy's δ**, and the issuer's ship rule and the
verifier predicate become the same intended statement about the same
observable under the declared abstractions — the correspondence A1.4
demands, asserted here and checked mechanically by the bridge model
(`formal/tla/P5cP5P6_Bridge.tla`; its own non-author review pending).
P5c's fused-clock guard (`now ≤ declared + δ` at depth k) is a locally
*stronger* condition that implies the chain predicate under that
module's single-clock abstraction; with the clocks decoupled, the
bridge's `Ship` evaluates the chain quantities directly.

**Named residuals.**

- *Adversarial timestamping.* A miner can set `timestamp(h + k − 1)`
  forward within the consensus bound, pushing an honest issuance into the
  tail case. This is a griefing surface bounded to hours against δ = 72
  hours; it can force a re-issue, never a false verdict.
- *Non-monotonic timestamps.* Block timestamps are not monotonic;
  `confirmed_at` may even precede `anchor_time`. The predicate is a single
  comparison on one designated block and is well-defined regardless; no
  monotonicity is assumed.
- *`confirmed_at` is a proxy, including backward skew.* The observable is
  the designated block's header timestamp — the chosen chain-time proxy
  for burial, not a measurement of when depth k was reached in wall-clock
  time. Median-time-past rules allow a block mined after a real-time
  deadline to carry an in-window timestamp (the mirror of the
  forward-skew griefing above). The predicate is well-defined on the
  proxy; wall-clock burial lateness is not what it measures.
- *Header provenance.* The conjunct's verdict is only as trustworthy as
  the headers it is evaluated over. Bundled headers form a candidate
  chain segment, not proof of canonicity: a privately-mined in-window
  fork presented in a bundle, or a lying header store, yields false
  acceptance under naive stateless evaluation. Header authentication
  against the canonical chain — proof-of-work validity, cumulative-work
  or checkpoint anchoring, store identity pinned in declared verifier
  policy, bundle/store conflict rules — is part of the A2.2 evidence
  obligation; its full specification is deferred to that obligation's
  discharge, not silently assumed here.

**Model-convention pin (off-by-one, fixed here so it cannot drift).**
P5c's `depth` variable counts blocks mined *after* inclusion (`depth = 0`
at inclusion), so `depth ≥ DepthK` corresponds to `c ≥ DepthK + 1`. The
correspondence mapping instantiates **`DepthK = k − 1`** (for the strict
default k = 6: `DepthK = 5`). δ, ε, k remain ratified (or revised, on the
record) at Band 0 exit, as registered; δ's 72-hour sizing already included
aggregation-to-confirmation lag, so this amendment does not move it.

---

## A2.2 P5, amended: the strict temporal check gains a third conjunct

`VALID_STRICT` now requires all of:

    declared_issue_time − ε  ≤  anchor_time                       (unchanged)
    anchor_time              ≤  declared_issue_time + δ           (unchanged)
    confirmed_at             ≤  declared_issue_time + δ           (new)

Consequences, stated explicitly:

- The **chain-late subclass** of the A2.0 abandoned-anchor artifact
  (`confirmed_at > declared + δ`) is **rejected outright** — its
  `confirmed_at` exceeds its own window. Within this system the conjunct
  rejects *only* such artifacts: strict issuance ships nothing that fails
  it (A2.1). An operationally abandoned but chain-valid artifact passes
  this conjunct and is governed instead by the A2.1/A2.4 standing rules
  (no protocol standing; closure of the two-receipts residue is
  Amendment 3's obligation, per A2.0).
- **Evidence obligation.** The verifier must evaluate `confirmed_at`
  statelessly (P9): block headers `h … h + k − 1` are available either
  archived in the bundle or from the verifier-distributed header store the
  anchor check already requires — the same trust-configuration pattern as
  A1.5's historical trust-anchor store. Header *authentication* rules
  (canonicity, work validation, store identity in declared policy,
  bundle/store conflict resolution — the header-provenance residual of
  A2.1) are part of this obligation. This joins the H1a evidence
  obligations.
- **Waiver status.** Temporal-anchor consistency is already non-waivable
  (A1.2.1); the new conjunct is part of it. The P4 partition applies
  inside it: performed-and-failed → `INVALID`; unperformable (headers
  unavailable) → `UNVERIFIABLE`; neither is promotable.

---

## A2.3 The re-issue loop terminates: bounded attempts, fail-closed refusal

As registered, the P5 corollary's re-issue rule was an unbounded loop, and
its dominant triggers — fee spikes, congestion, calendar outage — are
*correlated across attempts*: retrying under the same conditions is not a
fresh draw, so "re-issue until it works" can livelock. Fail-closed means
issuance must be able to end in refusal, not only in success.

Amended: issuance makes at most **N attempts**. The expiry clock is the
**wall clock** (A2.1 clock roles): an attempt expires when wall time
passes `declared + δ + S`, except that timely-latched eligibility
excludes expiry — eligible/finalizing, shipped, and expired/refused are
mutually exclusive states (construction obligation, registered with the
ruling). Exhausting them obligates
the implementation to terminate issuance in an **explicit refusal, durably
recorded; reporting is a delivery obligation to be registered in
Amendment 3** — a first-class protocol outcome, not an error path. N is a
protocol constant ratified at Band 0 exit alongside δ, ε, k, and S
(working default **N = 3**; per the A2.1 clock-roles ruling each
attempt's lifecycle is wall-governed through δ + S, so N attempts give
a **nominal lifecycle budget** of N × (δ + S) — twelve days at the
working defaults δ = 72 h, S = 24 h — a nominal budget, not a proven
wall-clock bound on the process; see the model note).
[**Note:** refusal as a separate delivery obligation added 2026/07/21 per
review process/response.]

Model note: P5c's `MaxAttempts` is hereby promoted from a state-space
bound to protocol semantics. The refusal state is modeled by **atomic
entry** (the transition expiring the final attempt's window records the
refusal in the same step; checked, with a broken companion red on
exactly the silent-deadlock invariant among the checked set — review
archived in
`docs/reviews/2026-07-20-codex-p5c-refusal-review.md`). Scope of proof
versus contract, per that review: the model proves the *conditional
safety half* — the refusal state is entered atomically and latches; it
does not prove the crossing occurs (no fairness is assumed), so
**termination is a contract obligation on the implementation, not a
proven liveness property**. The unbounded "eventually ships" claim
likewise remains explicitly unproven. Storage durability, retrievability,
and reporting of the refusal record are implementation/handoff
obligations to be registered in Amendment 3 (planned, not yet in force).
[**Note:** model-note scope split added 2026/07/21, same review cycle.]

---

## A2.4 Anchor identity and declared-time confinement

- **A receipt's anchor is the proof it ships with.** A shipped receipt
  contains exactly one anchor proof (the OTS proof over its canonical
  bytes) together with the anchor transaction's id, which serves as the
  **identity handle** binding the receipt to its chain transaction. (An
  identity/coherence handle, not by itself a retrieval mechanism:
  txid → transaction *availability* requires chain access — a node,
  index, or archive — which is an implementation obligation under the
  evidence discipline, joining A2.2's; the hash argument below covers
  identity, not availability.) Verification evaluates the
  shipped proof and no other; an anchor not shipped inside a receipt
  confers **no validity, no priority, and no claimed anchor identity**
  in verification or dispute — in particular, a discarded attempt's
  transaction confirming later confers nothing toward any of the three.
  (This confines *protocol standing*; it does not render such artifacts
  inadmissible as *evidence* — e.g., of issuer conduct — in dispute
  processes. The stand-alone anchor-standing property is Amendment 3's
  to register; this clause is written to underdetermine it, not
  pre-empt it.) The handle
  requires no new assumption: a txid is the double-SHA-256 of the
  transaction, so txid → transaction → committed bytes rests on the
  SHA-256 resistance already cited in Layer 2, and the OTS proof's merkle
  path binds the anchored bytes to the block independently of the handle.
  (The txid necessarily lives in the bundle outside the signed bytes — the
  anchor is computed over those bytes, so the txid exists only after them;
  the wrapper discipline of P7 makes the containment tamper-evident.)
- **Declared times are existed-by claims, and only that.**
  `declared_issue_time` asserts the artifact existed by that time;
  re-declaration on re-issue moves it forward, which weakens and never
  falsifies. **No verifier policy, and no downstream marketplace rule, may
  order competing receipts by declared time** (first-to-file semantics):
  the re-issue mechanism necessarily gives the issuer discretion over
  declared times within the retry schedule, and priority ordering would
  convert that discretion into a manipulation surface. This confinement is
  a design commitment in the P6 monotonicity style — assumed by the model,
  enforced by policy, deliberately not filed under Layer 2.

---

## A2.5 New model obligations

- **Verifier-side family (P5/P6):** add the `confirmed_at` observable and
  the A2.2 conjunct under the existing verifier-owns-tolerances
  discipline; a broken companion omitting the conjunct must accept the
  the chain-late subclass — witnessing exactly the gap A2.0 records.
  Standing working rules apply (broken companions, `_Sanity` vacuity
  witnesses for every defined-predicate antecedent).
- **P5c:** the header's semantic-fork paragraph resolves to
  ratified-strict in the A2.1 chain-time form; `MaxAttempts` semantics
  per A2.3; `DepthK = k − 1` convention per A2.1.
- **Conformance vectors (A1.7):** extracted traces must include the new
  conjunct's reject case (late-burial artifact → `INVALID`) and its
  unperformable case (missing headers → `UNVERIFIABLE`).
- **Clock-roles analysis (discharged with the ruling, 2026-07-21):** the
  slack companions `P5cP5P6_BridgeSlack.tla` / `_Latch.tla` check the
  conditional opportunity guarantee (B − C ≤ S ⇒ timely opportunity at
  eligibility; residue witnessed non-empty below the bound; cutoff
  exercised; iff status = argument plus bounded check). The committed
  bridge **registers the absence** of a lifecycle guard in its `Ship` —
  it checks the chain-evidence seam only. Predictions-first record and
  outcomes: `docs/reviews/2026-07-21-claude-predictions-slack-bench.md`;
  ruling archive: `docs/reviews/2026-07-21-clock-precedence-ruling.md`.

---

## A2.6 What changed, and what did not

This amendment **strengthens** P5 (a third strict conjunct), **adds**
obligations (header evidence and authentication for stateless
confirmation checking, the attempt bound with recorded refusal —
reporting to be registered in Amendment 3, per A2.3 — the
anchor-identity rule, the declared-time confinement commitment, new
conformance-vector cases), **registers** a correction that narrows
what the strict rule may be claimed to protect, **rules** the
clock-roles question (chain time governs evidence, wall time governs
the attempt lifecycle with operational slack S — a new constant
joining δ, ε, k, N at Band 0 exit; the opportunity guarantee is
conditional on the observable lag, and no hard backward-lag assumption
is registered), and **withdraws** the two-receipts closure claim,
re-registering it as an Amendment 3 obligation.

Stated in A1.1's terms, exactly: no A1.2 property is weakened; no proof
is demoted to an assumption; no declared A1.3 adversary capability is
excluded; the construction remains dual-signature plus temporal anchor.
The A1.1 falsifier is not triggered. In ordinary language, behavior
does change, and this amendment does not pretend otherwise: the
permissive reading's acceptances are excluded by ratifying strict, a
refusal outcome and attempt bound now exist, exactly one shipped anchor
carries protocol standing, and declared-time priority policies are
prohibited — all registered strengthenings or confinements. One
acknowledged cost: the new evidence obligation adds an `UNVERIFIABLE`
path (headers unavailable) where pre-A2 verification could return a
verdict — an availability cost of the strengthened check, carried by
the P4 partition, not a weakening of any registered property. The
bands, hypotheses, hard invariants, and division of labor are
unchanged.
