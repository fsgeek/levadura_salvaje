# Tessera — Phase 0 Pre-Registration, Amendment 3 — ADOPTED (2026-08-08)

> **Status: DRAFT — not signed, not in force.** This draft was prepared
> 2026-08-07 by the AI collaborator (Claude, Fable 5) from the adopted
> session records and revised 2026-08-08 by Codex through author
> dialogue; §A3.7.2's refusal decomposition and the §A3.4
> survivability floor were further revised 2026-08-08 in three-way
> dialogue (author, Claude, Codex), applied by Claude pending Codex
> review; per the credibility line, every decision below is
> either (a) already the author's, adopted on the record and cited to
> its source, or (b) direction given by the author during drafting and
> recorded here pending cold read. Mechanisms remain deliberately open
> wherever the registered invariant and its observable failure condition
> do not require one exact construction. Nothing here is load-bearing
> until the author has cold-read the resulting text, the amendment has
> passed falsification-style non-author
> review (the A1.7 discipline, applied to the amendment itself, by a
> panel cold to the 2026-08-07 and 2026-08-08 sessions), and the
> author has signed,
> committed, and OpenTimestamps-stamped it.
>
> **What this document is.** The third amendment to the Phase 0
> pre-registration (`phase-0-prereg.md`, commit `75207ba`), layered on
> Amendment 1 (commit `03cd3db`) and Amendment 2 (ADOPTED 2026-07-21,
> commit `62f0c5f`). The original and prior amendments are never
> edited; this document states what changes, and why, on the record.
>
> **Provenance.** Four streams converge here, all adopted or confirmed
> before drafting began: (1) the P1 rulings of 2026-07-28 — the
> identity boundary and the linked evidence floors — recorded in
> `docs/reviews/2026-07-28-identity-boundary-evidence-floors-ruling.md`;
> (2) the survivability-mechanisms rulings of 2026-08-07, recorded in
> `docs/reviews/2026-08-07-survivability-mechanisms-ruling.md` (both
> adopted at commit `68b581c` after two non-author review rounds);
> (3) the Amendment 2 residues that A2.0 and the property tracker
> explicitly registered as Amendment 3 obligations; (4) two confirmed
> findings from a read-only external trace (ChatGPT "Sol", 2026-07-28,
> verified against registered text before acceptance). All ratified
> decisions are the author's (Tony Mason).

---

## A3.0 What forced this amendment

Amendment 2 closed the clock question and left named residues.
Governance review then surfaced that "attestation survives Tessera's
termination" was a stated goal with no registered mechanism, and the
P1 modeling kickoff forced two questions any symbolic statement of
integrity depends on: what exactly Tessera attests, and what minimum
evidence a valid verdict may rest on. Those questions were ruled on
2026-07-28 and 2026-08-07; this amendment registers the rulings,
closes or disposes the A2 residues, and adds the survivability
obligations. Under A1.2's change discipline, tightenings and additions
require amendment; §A3.10 states what changed, what did not, and why
the A1.1 falsifier is not triggered.

---

## A3.1 What Tessera attests: the identity boundary

**Registered (author-ruled 2026-07-28, adopted 68b581c):** Tessera
attests the **identity of the framed bytes presented at an issuance
event** — computational identity under the declared construction and
assumptions — and nothing more. Outside the attestation: meaning,
truth, intended use, future interpretation, and the metaphysical
identity of the payload's referent.

1. **Replay.** Re-presenting a genuinely issued package preserves
   identity; P1 permits it. Whether a replay is appropriate in a
   transaction is policy belonging to a context that must supply
   transaction identity, nonce, audience, or purpose. Tessera does not
   invent that context. P1's symbolic statement is accordingly
   **existential issuance-event authenticity** (a non-injective
   correspondence), with replay and context scoped to caller policy.
2. **The headline precision repair (Sol finding 1).** The H0 headline
   "altering any part requires solving a computationally hard problem"
   is corrected to its operative form, which already coexists in the
   pre-registration (§2, Layer 1): alteration is trivial; **surviving
   verification over altered bytes is what is hard** — no transition
   leads to an accepted receipt over altered bytes. This is a
   claim-correspondence repair, not a construction change or weakening
   under A1.1: the operative form is the checkable claim the models
   already use.
3. **Coverage map obligation.** The repository shall carry a coverage
   map from package component to defending property — bytes → P1,
   signature set → P2, type/wrapper → P7, manifest authority → P10,
   anchor identity → A2.4, framing → P8 — **with open cells visible**.
   An honest map with gaps beats an implied completeness.
4. **The relying-party story is a required artifact.** One page: a
   person holds a receipt and a verdict; these are the decisions they
   may and may not make on it. It opens with the can/does-not-establish
   list recorded verbatim in the 2026-07-28 ruling doc ("Tessera can
   establish: this valid package reconstructs the same framed bytes
   recorded at issuance. Tessera does not establish: the payload is
   true; the issuer understood it; …"). Registered as a Band 0 exit
   artifact.

---

## A3.2 Evidence floors: the A1.2.1 tightening

**Adopted core (2026-08-07, commit 68b581c — adoption route (b): the
minimal requirement adopted, its normative security boundary supplied
here while the realizing mechanism remains open):**

> Every valid verdict requires at least one continuous accepted
> evidentiary chain per independently evaluated attestation layer;
> redundant paths may be waived, but the final complete chain may not
> be.

**Normative expansion (the mapping clause).** "Continuous accepted
evidentiary chain" means **exactly** the following witness chain, and
nothing weaker:

> accepted external authority evidence
> → the exact authority statement consumed from the manifest
> → issuer identity and signing key
> → proof of possession **by that same key**
> → accepted signature verifying under that key
> → the exact framed bytes

Both forms are registered — the sentence is the property statement the
relying-party story and the written proof carry; the chain is the
proof obligation the capstone (§A3.3) discharges. The mapping clause
binds them: neither may drift from the other. (Author ruling
2026-08-07: the two formulations are complementary altitudes, not
rivals; the rationale — report what was done, defer interpretation to
future verifiers and their risk tolerance — is on the record in the
2026-07-28 ruling doc.)

**Why linked, not counted (registered rationale).** Counted floors
("≥1 accepted signature AND ≥1 accepted external evidence") admit the
two-worlds attack: evidence supports manifest M′ while the accepted
signature claims authority from M; both counters pass with the chain
broken — the aTLS genus. And without any floor, the model's
IssuanceEvent correspondence becomes privileged historical knowledge
unavailable to a real verifier: the proof would be of the wrong model.

**Interaction with the A1.2.1 waiver lattice (tightening, stated
exactly):**

1. A1.2.1's waivable item "accepting fewer than all external
   manifest-authority evidences (P10)" is tightened to: **fewer, but
   never zero** — redundant members of the A1.5 evidence set may be
   waived; the final complete chain may not be broken or eliminated.
2. **Unavailability is not waiver.** If every external authority
   evidence for a layer is unavailable, unsupported, or otherwise
   unperformable, the layer's verdict is `UNVERIFIABLE` — never
   `VALID_DEGRADED`. Evidence that is present and whose validation is
   performed but fails yields `INVALID`. The P4 partition applies
   inside the floor exactly as A1.2.1 already requires of
   non-waivable checks.
3. **Proof of possession is chain-internal:** the possession proof
   must be by the same key whose signature is accepted (consistent
   with A1.5's rule that the self-signature is never an authority
   channel). An existential self-signature by another key in a
   multi-key manifest does not close the chain.
4. **Per-layer quantification.** A wrapped package's inner and outer
   attestations are separately typed signed objects (P7); each layer
   contributing to a returned valid verdict carries its own complete
   chain, evaluated independently. The base assessment reports each
   layer's result without replacement by an aggregate judgment; a
   higher-level relying-party policy may consume those results. The
   proof obligation quantifies over every contributing layer.
5. **No change to P4's partition.** The floors bound entry into the
   two VALID states; they add no states and alter no verdict
   semantics. P4 remains correct but incomplete by abstraction.

### A3.2.1 The chain's first-link invariant

A1 §A1.5's two external authority evidences (the DNSSEC chain snapshot
and the anchored repository publication, both archived in the bundle)
publish **issuer-key fingerprints**, not manifest digests. Registering
an exact-manifest-digest mechanism here would both narrow the design
space prematurely and risk a self-reference if the hashed manifest
itself carries the archived evidence.

The requirement is therefore stated at the security boundary:

> External authority evidence must unambiguously bind the exact
> authority statement the verifier consumes. Two manifests that differ
> in any authority-relevant fact must not be supportable by the same
> evidence; differences explicitly declared non-authoritative may remain
> outside that binding.

The mechanism spike may realize this with a separately hashed manifest
core, an exact authorized tuple, or another construction. It must name
which manifest facts are authority-relevant and carry a broken companion
in which two authority-distinct manifests share evidence; the consuming
linkage query must fail. The mechanism is not registered until the spike
has supplied that evidence.

`[AUTHOR DECISION — ratified - 2026-08-08]` **Override of adopted text,
named.** The adopted record (the 07-28 ruling, Ruling 2 item 5)
docketed exactly two options — digest publication or authorized
tuple — required A3 to choose between them, and stated that the exact
links are resolved in A3 before the spike. This section declines both
options in favor of the boundary invariant above and moves mechanism
selection after the spike. Rationale: each docketed option is a
premature narrowing, and the digest option additionally risks
self-reference (verified against A1 §A1.5: the manifest carries the
archived authority evidences). The invariant with its two-worlds
broken companion preserves the falsifiable content the docketed fork
existed to protect. The same ruling covers the chain's second link:
this amendment's "exact authority statement consumed from the
manifest" supersedes the ruling doc's "exact manifest" link, and the
spike targets the chain as registered here.

---

## A3.3 The symbolic suite and the capstone gate

**Registered obligation (requirement level; ruled in dialogue
2026-07-28, restated and adopted 2026-08-07, commit 68b581c):**
per-property ProVerif models over a shared theory library; every model
carries an explicit assumes-from-elsewhere ledger holding **two entry
kinds** — dischargeable cross-model obligations, and exposed Layer 2
assumptions.

> Band 0 exit is gated on a capstone composition context in which
> every ledgered **cross-model** assumption — a fact one symbolic
> model assumes and another must establish — is discharged by a
> machine-checked producer query and carries a broken companion that
> **fails the query consuming the severed link**. Layer 2 assumptions
> (cryptographic primitive security, historical trust-anchor
> correctness, chain availability, implementation fidelity,
> operational independence of authority channels) are explicitly
> exposed and unclaimed in the ledger — never discharged, never
> silently absorbed. Any termination-forced scoping is named in-module
> and disposed by amendment discipline, never silently.

**Ledger conservation rule** (each entry records at least): consumer
property/query; assumed fact; producer module and event/query (or
"Layer 2 — unclaimed"); the shared term establishing correspondence;
adversary capabilities at the join; and any residual Layer 2
assumption. A cross-model entry additionally records the broken
mutation and expected failing query; those fields do not pretend to
discharge a Layer 2 entry.

**The mechanism spike precedes the suite scaffold** (design adopted
2026-08-07): representative complexity first — the §A3.2 witness
chain, the structural worst case — ablating toward the break point on
failure; the drafted ledger interface is the spike's scaffolding (one
artifact); per-query timebox declared before running with three named
outcomes (query violation = counterexample; timeout = mechanism
failure, not property evidence; termination = evidence for the checked
abstraction only); predictions registered before running. The
transcription-pattern capstone is a non-binding implementation
candidate, subject to the spike.

**Additional model obligations from this amendment:** the capstone's
linkage query proves the §A3.2 chain (the links, not just
cardinalities, per-layer); the P4 model's unknown-algorithm transition
(§A3.6) carries its own companion; every symbolic lemma carries a
prose mapping to its registered property (standing rule, reaffirmed).

---

## A3.4 Survivability: three claims, a Designated Community, and the bundle

**The claim "attestation survives Tessera's termination" is split into
three registered claims with different truth conditions (adopted
2026-08-07):**

1. **Portability / self-containment:** a possessed bundle can be
   verified without Tessera. Fully a Band 0/H1a obligation: the bundle
   carries data (P7/P9/P10, A1.5, A2.2), an unambiguous identifier and
   hash for the governing verification specification, and — added by
   this amendment — the Tessera-specific procedure itself.
2. **Availability:** a copy remains obtainable only through retention
   and custody. Custody is necessary **immediately**, not merely past
   the first algorithm death.
3. **Long-horizon evidentiary continuity:** validation across
   cryptographic decay requires renewal by custodians **before** the
   old mechanism becomes unreliable — RFC 4998 (ERS) renewal, under an
   RFC 4810-style cryptographic-maintenance policy; renewal wraps, it
   never replaces (consistent with the wrap-don't-replace re-anchoring
   already registered in the original §4).

**The survivability floor (general, every artifact class).** For every
artifact class Tessera produces, its survivability guarantees are
limited to: creation and the protocol obligations it can observe;
verifiable handoff when acknowledgment occurs; portable identity; and
visible failure while an observer possessing the relevant state
survives. Continued availability after handoff is conditional on
custody. No construction can guarantee recovery after every holder of
the complete artifact loses it. (The three claims above are this
floor applied to receipts; §A3.7.2 applies it to refusal records.)

**Bundle additions registered for claim 1** (from the 2026-07-27
gap analysis and the 2026-08-08 author dialogue):

- An unambiguous verification-spec identifier **and its hash bound into
  the signed bytes** — a verifier can prove which procedure governs.
- **The Tessera verification specification and its conformance vectors
  embedded in each individual receipt bundle as typed, content-addressed
  objects** (P7's enumerated type set gains the specification member;
  the set already includes conformance vectors). A later aggregate
  preservation package may deduplicate those immutable objects without
  changing their identity or semantics.
- **A plain-language purpose preamble** (WIPP-marker style):
  typed and bound Representation Information for *intent*, so a future
  reader knows what this object is for before knowing how to check it.

**The Designated Community declaration:**

> A member of the Designated Community — human, machine, or
> collaboration — can reconstruct Tessera verification and interpret
> its bounded result using only the preserved receipt bundle and the
> exact external standards dependencies declared by that bundle,
> without Tessera-specific institutional knowledge. This
> reconstructability claim is scoped to survivability claim 1 alone;
> it promises nothing about availability or evidentiary continuity.
> For horizons
> requiring claims 2 and 3, the Designated Community is not only the
> bundle's *audience* but its *custodian*: availability and evidentiary
> continuity are declared custodial dependencies, named here rather
> than inherited silently from the ERS citation. Future decision makers
> may amend the custodial practice as they learn; the dependency itself
> is permanent and honest.

**The century horizon is aspirational, not a guarantee or membership
criterion.** Tessera is designed to preserve reconstructability across
successive technology changes for as long as custodians continue the
declared work. It makes no prediction that today's bundle, standards,
algorithms, or competence declaration will suffice one century hence.

`[AUTHOR DECISION — revised - 2026-08-08]` **Competence profile (the
rotation baseline).** A Designated Community member can, using
ordinary documented computing tools: interpret the bundle's declared
public-standard dependencies; implement or execute the deterministic
Tessera verification procedure; run and interpret its positive,
negative, and broken conformance cases; and distinguish each
structured assessment dimension from payload meaning. No
Tessera-specific institutional knowledge is assumed. Every custodial
challenge declares any prerequisite beyond this baseline; failure on
a challenge exceeding it does not by itself establish a bundle
defect. This is the baseline §A3.5's challenge-rotation reading (b)
measures against — and what an amendment revises when that reading
is ruled.

**Dependency closure is layered:**

1. **Tessera verification dependencies** — framing,
   canonicalization, signatures, hashes, temporal proofs, and evidence
   formats needed to verify Tessera's own claim. Tessera owns this
   closure. The bundle identifies each exact external standard edition,
   the normative sections used, known-errata disposition, stable digest
   where canonical bytes exist, retrieval identifier, redistribution
   status, and failure consequence. Tessera-authored procedure and
   conformance artifacts are embedded; external standards are embedded
   opportunistically when lawful, otherwise precisely referenced.
2. **Issuance-profile dependencies** — additional mechanisms chosen by
   an issuer or deployment profile. The profile author declares them;
   Tessera requires an unambiguous cryptographic binding and exposes
   unavailable interpretation as `UNVERIFIABLE` for the affected check.
3. **Payload-interpretation dependencies** — schemas, vocabularies,
   software, ontologies, codecs, or contextual material supplied by the
   submitter as an optional typed Representation Information companion.
   The receipt commits to the companion's exact bytes. Tessera preserves
   its identity but does not assert its correctness, sufficiency,
   legality, availability, or the payload meaning it proposes. Absence
   or uninterpretability affects payload interpretability, never the P4
   envelope verdict.

Continued availability and correct interpretation of precisely
referenced but unembedded standards are exposed Designated Community
assumptions. An unavailable normative dependency is a visible
preservation failure. Our goal is to always disclose such dependencies.

**Demonstrations registered:** the dead-service test (P9: verify with
Tessera unreachable) and the dead-project test (clean-room: a verifier
with no project-specific context receives bundle plus broken
companions only, must reconstruct the procedure and reach correct
verdicts including the INVALID/UNVERIFIABLE traps). Each dead-project
run records its **evaluation conditions** — verifier provenance,
challenge creation time, disclosure state, candidate access — because
recency reduces prior-exposure risk but proves nothing (§A3.5).

---

## A3.5 Tending: custodial attestations and challenge rotation

**The tending obligation.** Tending records custodial assessment, not
an assumption that every assessment produces a renewal artifact. The
record has one of four outcomes:

1. `NO_ACTION_REQUIRED` — the custodian evaluated the declared
   triggers and recorded that none had fired;
2. `RENEWED` — a trigger fired, or discretionary renewal occurred; the
   record references the resulting renewal artifact and its predecessor
   linkage is mechanically checked;
3. `ACTION_DUE` — renewal is required but has not yet completed; or
4. `FAILED` — an attempted required renewal did not complete.

The last two outcomes make the gap visible rather than issuing a
reassuring heartbeat.

Every outcome exposes the policy and version applied; observations and
their provenance; mechanically evaluated trigger results;
judgment-based conclusions; unavailable observations; and, when
applicable, the renewal-artifact reference and predecessor-link result.
The record proves only that a named custodian made the recorded
assessment. Mechanical checks prove only their bounded results; they do
not make a judgment-based `NO_ACTION_REQUIRED` conclusion true.

**Conditional visibility, not predicted safety.** Custodial policy
declares renewal triggers and intended safety margins. Given an
available monitoring clock and custodial record, crossing a trigger
without the required tending record produces a visible stale condition.
The claim that a chosen trigger precedes an unforeseen failure of the
protected mechanism is an exposed operational assumption, periodically
reassessed — never a Tessera guarantee.

Custodial-health monitoring and any relying party holding a current
custodial record may observe the condition. The stateless verifier of an
old bundle cannot: silence is not contained in the bundle. Tending
health therefore never changes a receipt's P4 verdict or protocol
standing. Exact trigger expressions, cadence, clock, monitoring surface,
and succession mechanism remain design obligations. They receive their
own trust assumptions and do not reuse δ, ε, or k merely because the
temporal modeling pattern is familiar.

`[AUTHOR DECISION — ratified -- 2026-08-08]` **Status against the adopted
four questions.** The adopted ruling (§4 of the 2026-08-07 record)
made answering four questions the registrability condition for this
obligation. As registered here: who observes — the custodial monitor
and any holder of a current custodial record (above); what staleness
affects — custodial-health reporting only, never a receipt verdict
(above); where the cadence is declared — in the custodial policy.
The clock question is answered as **clock roles, not one clock**,
consistent with A2.1's discipline (an earlier recommendation of raw
chain time repeated the fused-clock error and was withdrawn in
review: block timestamps are non-monotonic, chain time is existed-by
evidence rather than elapsed time, and A2 assigns operational
lifecycle decisions to the wall clock):

> The custodial policy declares its trigger classes, observation
> sources, uncertainty treatment, and any maximum assessment
> interval. Operational observation time governs when an assessment
> becomes due; external chain time supplies existed-by evidence for
> tending and renewal artifacts. Staleness is evaluated relative to
> the policy's declared operational clock and trust assumptions,
> never inferred from raw block timestamps alone. No claim is made
> that a chosen interval precedes unforeseen mechanism failure.

The cadence parameter lives in each custodial policy or profile, not
as one universal constant; what Band 0 ratifies is the required
parameter schema and the clock-role invariants above. This satisfies
the adopted condition — all four questions answered — while freezing
no global duration before custodial practice exists.

**Challenge rotation (adopted, 2026-08-07).** Conformance vectors are
two layers with different survival properties: a **fixed floor** in
the bundle (memorizable, and acceptably so — a floor need only catch
a naive fail-open verifier), and **novelty minted outside the bundle
as custodial practice**. A bundled generator cannot by itself
guarantee non-exposure or replace custodial rotation; a generator
with a large case space or undisclosed seed may remain useful as a
testing mechanism. Custodial minting reduces prior-exposure and
rote-memorization risk and records its evaluation conditions. When
an existing verifier fails a new challenge, the failure is a
**measurement with three readings**, disposed under amendment
discipline: contamination exposed (the test working); the challenge
exceeds the Designated Community's declared competence (discard it,
or amend the declaration); the bundle genuinely lacks what the
challenge needs (a real gap — fix the bundle).

---

## A3.6 Algorithm agility and the post-quantum path

**The deferral ruled safe, and what makes it safe.** The PQ signature
implementation is deferred from the proof of concept and **gates the
production version** — the demonstrated capacity to add an algorithm
is the registered "future resistant" claim, not a bet on which
algorithm survives. (The cloud leg's path is integration, not
construction: KMS ML-DSA support is already recorded in the original
§3.1. The portable GPG leg is the real gap; OTS is the independent
temporal anchor and does not fill a signing gap.) Hybrid classical+PQ
dual signing is explicitly deferred to a deployment profile or later
amendment — with a clear conscience, recorded here.

**What Band 0 carries now:**

1. **Identifier-binding invariant.** The algorithm identifier and all
   parameters that affect interpretation are unambiguously parsed and
   cryptographically bound to the exact signed object. No substitution
   or alternative interpretation may preserve verification. P3 already
   requires the identifier inside the signed bytes; P8's framing proof
   and golden-vector design must identify its exact encoding. A
   mandatory canonical-payload field is the current implementation
   candidate because it preserves P8's four-field frame, but the
   amendment does not freeze that tactic before the proof and vectors.
   `[AUTHOR DECISION — revised -- 2026-08-08]` The adopted ruling required
   A3 to pin the identifier's location (frame field vs payload field)
   rather than leave it split across two property statements. As
   proposed here, this section pins the **location** — inside the
   canonical payload under P3's obligations; P8's four-field frame
   layout is unchanged — and leaves open only the exact **encoding**,
   which P8's framing proof and golden vectors must fix before Band 0
   exit.
2. **The verdict boundary (adopted, exact):** `UNVERIFIABLE` for
   exactly one case — a well-formed, correctly bound, but unsupported
   algorithm identifier. `INVALID` for: missing identifier;
   identifier/signature encoding mismatch; malformed parameters; an
   identifier prohibited by applicable policy; substitution of the
   signed identifier; a known algorithm whose signature fails.
3. **Landed twice:** a software red-bar suite verifying the
   signing-provider interface with the PQ implementation stubbed; and
   the formal model's P4-partition transition with a broken companion
   — a verifier that fail-opens past an unknown algorithm must go red.
4. **The canary never graduates:** one permanently reserved
   unrecognized algorithm identifier remains in the test suite after a
   real PQ provider lands, so the `UNVERIFIABLE` path is exercised
   forever. A conformance vector ships in the bundle's fixed floor:
   "a signature in an algorithm you do not know; the correct verdict
   is `UNVERIFIABLE`."

---

## A3.7 Amendment 2 residues, closed or disposed

1. **Standing/equivocation (the A2.0 residue).** The abandoned-anchor
   artifact can leave two cryptographically valid issuance artifacts for
   the same content with different declared times; A2.2 and A2.4 confine
   standing without deduplicating content. Comparative visibility is
   insufficient: a presenter of the abandoned artifact could omit a
   later lineage record. The registered invariant is therefore:

   > Cryptographic validity alone confers no protocol standing. Any
   > artifact claiming standing must present verifiable standing
   > evidence binding its issuance identity, attempt lineage, and
   > terminal disposition. Missing standing evidence leaves the artifact
   > evidentially admissible but without protocol standing.

   A terminal lineage record, capability, transparency witness, or
   another construction may discharge the invariant. The chosen
   mechanism must be testable on an abandoned artifact presented alone,
   not only when competing artifacts happen to meet.

   Standing is an **orthogonal assessment dimension**, not a fifth P4
   state. The base result reports at least `ESTABLISHED`, `ABSENT`, or
   `UNVERIFIABLE`, with evidence and reasons, alongside the unchanged P4
   envelope verdict. Thus an artifact may honestly be
   `verification = VALID_STRICT` and `protocol_standing = ABSENT`.
   Relying-party policy decides whether those facts meet its own
   requirements; Tessera does not collapse them into one checkmark.

   `[PANEL-DRIVEN CLARIFICATION — 2026-08-08, from the Kimi cold
   read]` Standing is not a member of the A1.2.1 waiver lattice: it
   is reported, never waived. No verifier policy, strict or degraded,
   rewrites the reported standing value. A relying-party policy may
   accept an artifact whose standing is `ABSENT` or `UNVERIFIABLE`,
   but that acceptance is the policy's own recorded decision outside
   the verdict — the same separation the lattice already enforces
   between waiving a check and erasing its record.
2. **Refusal records (the A2.3 split).** The abstract refusal state
   was discharged atomic-and-latching in Band 0. A2.3 registered
   durability, retrievability, and reporting of the refusal record and
   deliberately deferred their assignment; this amendment assigns
   them. The governing observation (2026-08-08 dialogue): a mortal
   authority cannot guarantee that evidence of its own decision
   becomes externally durable atomically with its local transition —
   local refusal, record delivery, and public publication occur in
   different failure domains, and the honest construction exposes that
   partial order rather than claiming to close it.

   **Refusal state.** `REFUSED` latches atomically when A2.3's
   terminal condition occurs; it is final and independent of all later
   reporting states. Delivery or publication failure cannot reopen
   issuance, consume another attempt, or erase the refusal. The same
   transition creates, as local durable state (creation is neither
   delivery nor publication):

   - the complete portable refusal record — attempt identity,
     disposition, reasons that may be disclosed, and the evidence
     needed to verify it;
   - its non-identifying public commitment value;
   - delivery status `PENDING`; and
   - publication status `PENDING`.

   **Record handoff.** The generating authority retains the complete
   record until the first of: `ACKNOWLEDGED` — a declared custodian
   (the submitter by default) confirms possession of a record that
   verifies against the commitment value; `DELIVERY_FAILED` — a
   non-retryable delivery failure is established; or
   `DELIVERY_EXPIRED` — the declared bounded retention horizon ends
   without acknowledgment. Failure and expiry are visible terminal
   dispositions, never silent deletion; the retained record's
   subsequent disposition follows the declared minimization and
   retention policy, and that disposition is itself recorded. Emission
   with verified handoff is the discharge moment: after
   acknowledgment, continued availability of the complete record is a
   custodial dependency under the §A3.4 survivability floor, not a
   dependency on the generating authority. The handoff mechanism
   remains open.

   **Commitment publication.** Publication is a separate state
   machine: `PENDING`; `PUBLISHED`, only on acknowledgment from the
   declared external channel; `PUBLICATION_FAILED`;
   `PUBLICATION_EXPIRED`. Creating the commitment value is not
   publication, and the handoff acknowledgment does not substitute for
   the channel's — conflating the two acknowledgments would hide
   exactly the crash interval this decomposition exposes. The
   publication channel must declare its survival, availability,
   privacy, and inclusion assumptions, **and** the independence of its
   failure modes from the declared refusal triggers — or the
   correlation: A2.3's dominant triggers (fee spikes, congestion,
   calendar outage) are correlated across attempts, and a channel
   sharing those failure modes is most likely to be unavailable
   exactly when refusals cluster.

   **Observers.** While the authority lives, the submitter and a
   declared operational monitor can observe pending and failed states.
   Observer roles are registered here; the reporting surface is not
   frozen, and refusal reporting is issuance-time operational
   machinery, not §A3.5 tending — the two may share implementation
   later without sharing registration. After `PUBLISHED`, the public
   can observe the external trace under the channel's declared
   assumptions.

   **The irreducible residual, named.** If the authority dies after
   the local refusal transition but before record handoff and before
   publication, no surviving observer holds evidence of the refusal
   disposition — even the failure statuses die with the authority. No
   construction can make an event known only to a destroyed party
   knowable without an independent participant already inside the
   refusal transition. Tessera minimizes the interval, retries while
   alive, refuses to report the reporting workflow as complete, and
   names this residual rather than disguising it as
   `PUBLICATION_FAILED`. Its consequence bound: the submitter may
   retain evidence of its own submission, but Tessera guarantees no
   surviving refusal evidence in this interval; regardless, under
   §A3.7.1 no artifact lacking terminal-disposition evidence can
   claim protocol standing — the interval costs the auditability of
   the refusal, never the integrity of what can be claimed on it.

   **Disclosure architecture (unchanged by this decomposition).** The
   base protocol does not require public disclosure of the complete
   record. A deployment profile may require it for a declared issuance
   class. Tessera does not maintain a foundational auditor-membership
   registry: the submitter may disclose its portable record to an
   auditor, who verifies it against the published commitment.
   Service-side copies and identifying metadata follow the explicit
   minimization and retention policy above. This architecture narrows
   Tessera's possession and disclosure role; the amendment makes no
   legal-process guarantee. The commitment construction must resist
   practical guessing or correlation of identifying fields under its
   declared threat model. It corroborates a disclosed record and does
   not reconstruct a lost one; absent a separately registered
   transparency mechanism, it does not prove that every refusal was
   published.
3. **The bridge finding (tracker; non-author review of the
   disposition performed 2026-08-08 — see
   `docs/reviews/2026-08-08-A3-panel-disposition.md`).**
   A2.1's "The rule" sentence states conjunct 3 only; under decoupled
   clocks conjunct 3 does not imply conjunct 2, so the issuer
   evaluates the **full three-conjunct temporal predicate of A2.2
   (the P5 temporal test inside `VALID_STRICT`)** before shipping —
   as the bridge model's Ship action already does. Evaluation of
   conjunct 3 alone is insufficient and is forbidden. Registered here
   as the authoritative prose repair.

   `[PANEL-DRIVEN REPAIR — 2026-08-08, from the Kimi addendum,
   clerk-verified against the model]` An earlier form of this repair
   said the issuer evaluates "the full `VALID_STRICT` predicate" at
   ship. That overstates the model and the obligation: the bridge
   model's Ship guard is the three-conjunct temporal predicate plus
   the burial-depth requirement (its header registers exactly this),
   and the issuer does not re-run envelope verification (P1–P3) at
   ship. The repair sentence itself is now scoped to match the model
   — the same prose/model discipline this item exists to enforce.

---

## A3.8 The assessment must carry its own boundaries (Sol finding 2)

`VALID_STRICT` attests envelope soundness, never payload truth — and
nothing previously registered prevented a future API or UI from
relaying envelope validity as content validity: the checkmark relay,
the aTLS genus at the semantic layer. Nor may the system collapse
envelope verification, protocol standing, payload interpretability, or
custodial health into one judgment.

**The base assessment is an unsigned, reproducible computation.** It
reports what the verifier can establish at evaluation time and leaves
the relying party to decide whether those facts meet its requirements.
It carries at least:

- identities of the input receipt, bundle members, and evidence actually
  evaluated;
- the P4 envelope-verification result;
- protocol standing (§A3.7.1);
- a machine-readable scope for every claim;
- governing specification, policy, trust configuration, and declared
  evaluation context;
- material reasons, observations, unavailable evidence, and recorded
  waivers; and
- payload Representation Information status when requested.

Custodial health is separately obtainable current information, not an
input to the stateless base receipt verdict. No unqualified aggregate
checkmark is part of the conforming result.

**Rendering red-bar.** Every Tessera-controlled or conforming
third-party surface that renders a result also renders its scope and the
material independent dimensions. A surface showing a checkmark without
those boundaries fails conformance. Tessera does not claim an adversarial
relay cannot discard the result and invent or strip presentation.

**Optional signed verification report.** A party that needs portable
attribution, evaluation-time evidence, or tamper-evident transport may
separately attest the complete base result as a distinct typed wrapper.
Its bounded claim is that an identified evaluator assessed an identified
bundle under an identified environment and obtained the enclosed result.
It neither changes that result nor elevates envelope validity into
payload truth. Signer authority, key lifecycle, and report policy belong
to that separate attestation profile; they are not smuggled into the
base verifier contract.

`[AUTHOR DECISION — ratified -- 2026-08-08]` **Why unsigned, on the
record.** The drafted Sol-finding-2 remedy placed the scope
declaration inside signed verdict bytes. This section replaces it
deliberately: a mandatory signature would introduce a
verifier-signing authority, key lifecycle, and additional trust claim
into the P9 path — and, depending on the selected signer, could also
reintroduce a service dependency — while strengthening nothing about
the reproduced computation itself. The base assessment therefore
remains unsigned. The trade is named: an unsigned result's scope can
be stripped by a non-conforming relay — the rendering red-bar makes
that a conformance failure rather than a cryptographic impossibility,
and parties needing attribution or tamper-evident transport use the
attested report above.

The relying-party story (§A3.1.4) is the human-facing statement of the
same boundaries; the structured fields are their machine-facing twins.

---

## A3.9 New model and artifact obligations (summary)

Tracked in `formal/PROPERTIES.md` upon adoption:

- Capstone mechanism spike (real-first, ledger interface included,
  three-outcome timebox, predictions-first) — precedes suite scaffold.
- Capstone linkage query: the §A3.2 chain, per layer, links not
  cardinalities; the first-link mechanism spike tests the
  authority-statement invariant and its two-worlds companion.
- Unknown-algorithm P4 transition + fail-open broken companion;
  signing-provider red-bar suite with permanent canary.
- Coverage map (component → property, open cells visible).
- Relying-party story page (opens with the can/does-not-establish
  list); assessment scope fields + rendering red-bar vectors.
- Bundle additions: exact verification-spec identity and hash in signed
  bytes; embedded Tessera specification + conformance-vector typed
  objects; layered standards-dependency manifest; optional typed payload
  Representation Information companion; purpose preamble.

`[PANEL-DRIVEN ADDITIONS — 2026-08-08 addendum round]`

- Issuance-path conformance vector for the decoupled-clock divergence
  (Kimi): `anchor_time = declared + δ + 1` (conjunct 2 fails),
  `confirmed_at = declared + δ − 1` (conjunct 3 passes); required
  issuer behavior is refuse-to-ship (discard, count against N).
  Extracted from the bridge model; lands in the H1a red-bar suite as
  a dedicated issuance-path test.
- Bridge broken companion for the exact finding (DeepSeek; clerk
  verified absent from the committed set): a `_BrokenConjunct3Only`
  variant whose Ship guard is burial depth plus conjunct 3 alone,
  expected `HonestShipAccepted` RED. `_BrokenWallClock` exhibits the
  divergence class; this companion exhibits the registered finding
  itself.
- `formal/PROPERTIES.md` carries a pointer at the A2.1 entry (Kimi):
  the frozen "The rule" sentence is superseded by A3.7.3 — issuer
  evaluates the full three-conjunct temporal predicate. Documentation
  hedge only; A2 text is never edited.

`[REGISTERED OBLIGATION — 2026-08-09, Kimi panel finding 2; placement
per the author's tail-search deliberation, recorded in
docs/reviews/2026-08-08-A3-panel-disposition.md]`

**The integrated adversarial lifecycle model.** At least one model in
which the A1.3 adversary drives the full protocol lifecycle —
issuance → wrapping → supersession → refusal → verification → tending
— including a broken companion in which a wrapper transplants
standing evidence from a valid inner artifact onto a forged outer
artifact (expected result: the standing query goes red). Rationale on
record: every composition-class failure this project has actually
observed (the bridge finding, the checkmark relay) arose at a seam
between separately-checked components, and a targeted per-model
companion would assert the cross-model correspondence in prose — the
same relay pattern one layer down. The only non-relayed check of a
cross-model claim is a model containing both sides.

**Trigger and placement — deliberately NOT a Band 0 exit
obligation.** This model consumes the first-link and
standing-mechanism choices, which are outputs of the mechanism spike;
gating Band 0 exit on it would make H0 hostage to decisions its own
process has not yet made. Registered placement: the obligation
triggers on completion of the mechanism spike, and the model must be
green — or its timeout disposed by signed amendment under the
three-outcome discipline — **before the H1a crypto-core freeze**.
Phase 1a opens on unchanged H0 terms. The spike's discipline applies
(per-query timebox, predictions first); reachability and
correspondence queries suffice — equivalence is not required.
- Dead-service and dead-project demonstrations, with recorded
  evaluation conditions.
- Tending-assessment mechanism: exposed policy, observations, judgments,
  unavailable inputs, outcome, and mechanically checked renewal linkage
  when renewal occurs; conditional stale-trigger monitoring with its
  prediction limits explicit.
- Standalone protocol-standing evidence satisfying §A3.7.1, reported
  orthogonally to the P4 verdict and tested on an abandoned artifact
  presented alone.
- Refusal-record decomposition (§A3.7.2): portable record, public
  commitment, and the handoff and publication state machines; bounded
  retention horizon; minimization and retention policy; publication-
  channel assumption declaration including trigger-correlation
  independence. Model obligation: the extended atomic-entry
  invariant — every transition entering `REFUSED` simultaneously
  establishes the complete local refusal record, the commitment
  value, delivery = `PENDING`, and publication = `PENDING` (the
  archived P5c proof covers the latch alone) — with its **primary**
  broken companion latching refusal while postponing or omitting one
  of those creations, and a second companion in which
  `DELIVERY_FAILED` or any reporting state re-enters issuance or
  decrements the attempt bound; both must go red.
- Structured, unsigned base assessment with scope-bearing dimensions,
  rendering red bars, and an optional separately attested verification
  report.
- A2.1 prose repair (issuer ships on full `VALID_STRICT`).

## A3.10 What changed, and what did not

**Tightenings (strengthen, never weaken):** the A1.2.1 waiver lattice
gains the linked floor (§A3.2) — every prior `VALID_DEGRADED` verdict
that satisfied the floors still verifies; verdicts that satisfied
counted-but-unlinked evidence never had a registered guarantee to
lose. The H0 headline is corrected to its operative form (§A3.1.2),
which is the form the models check. The unknown-algorithm verdict
boundary (§A3.6.2) instantiates the existing P4 partition; it adds no
states.

**Additions:** survivability claims and layered bundle contents
(§A3.4), tending and rotation obligations (§A3.5), agility
obligations (§A3.6), residue closures and orthogonal standing
assessment (§A3.7), structured assessment scope and optional report
attestation (§A3.8). Additions impose new obligations on Tessera, none
on prior artifacts.

**The A2.3 completion, named (it changes the obligation's apparent
owner):** A2.3 registered refusal durability, retrievability, and
reporting without assigning their bearer; §A3.7.2 assigns them — to
the generating authority until verified handoff, to the declared
custodian after it, with the published commitment — once externally
acknowledged — becoming the surviving public trace — and names one
honest impossibility (the pre-handoff death interval)
rather than registering a claim no architecture can keep. No A2.3
obligation weakens: refusal remains atomic, latching, and
first-class; what changes is that its evidence now has named
custodians and visible failure states where the registered text had a
passive voice.

**Explicitly not changed:** P4's verdict partition (it becomes one
component of the larger assessment, not the whole result model); P9
statelessness (tending state never enters a bundle verdict); A2.1's
clock roles (tending triggers get their own eventual mechanism and
trust assumptions); the A2.4 standing rules; the misissuance boundary
(A1.3.7).

**The A1.1 falsifier is not triggered:** no property is weakened; no
discharge is abandoned; the scoping honesty of the capstone gate
(cross-model discharged, Layer 2 exposed) narrows a gate ruled in
dialogue to what a symbolic prover can honestly discharge, and was
adopted in that form before this draft existed (commit `68b581c`).

**Mechanisms deliberately left open:** the authority-statement binding
construction (§A3.2.1); capstone transcription tactic (§A3.3);
custodial trigger, clock, monitoring, and succession mechanisms
(§A3.5); exact algorithm-identifier encoding (§A3.6.1); and the
standalone standing-evidence construction (§A3.7.1). Each is governed
by a registered invariant and observable failure condition; the design
space is not narrowed before spike evidence supplies a reason.

**Category (b) register — author directions taken in drafting
dialogue** (compiled by the assistant from the revision record,
2026-08-08; author confirmed completeness at cold read — ratified,
commit `c54d70d`. Status of every item below: **ratified**; the
2026-08-08 four-model panel raised no objection to any register item):

1. §A3.2: per-layer results reported without aggregate replacement
   (resolves the docketed "A3 decides" question).
2. §A3.2.1: boundary invariant replaces the docketed digest/tuple
   fork; mechanism selection moved after the spike (override marked
   in-section).
3. §A3.4: Designated Community declaration recast; century horizon
   made aspirational; layered dependency closure; per-receipt
   embedded specification objects; survivability floor added.
4. §A3.5: four-outcome tending record; conditional visibility;
   trigger/monitoring mechanisms deferred (clock and cadence
   parameter marked in-section).
5. §A3.6.1: identifier-binding invariant; location pin proposal
   marked in-section.
6. §A3.7.1: standing-evidence invariant replaces the docketed
   lineage-vs-dedup fork; standing as an orthogonal assessment
   dimension.
7. §A3.7.2: submitter-held portable record with public commitment;
   revised same day into the three-state-machine decomposition with
   the named residual (three-way dialogue: author, Claude, Codex).
8. §A3.8: unsigned reproducible base assessment with optional
   attested report, replacing the drafted signed-scope remedy
   (rationale marked in-section).

## A3.11 Review plan (predeclared)

Upon author cold read and approval of this draft: falsification-style
non-author review by a panel **cold to the 2026-08-07 and 2026-08-08
sessions** —
the coldness this amendment's source rulings consumed in review is
restored by fresh eyes. Panel scope: the amendment as a whole, plus
the A3.7.3 bridge-finding disposition (its pending non-author
review). Predeclared discipline per the A2 precedent: genuinely new
issues are in scope; re-litigating adopted dispositions is not. After
bounded verification: sign, commit, anchor.

**Author note:** calling it a cold reading after being asked to read
it cold multiple times is an illusion.  I have tried, to the extent
possible, to review an 800+ line document to ensure that it codifies
our decisions.  Each decision point is one where I was present and
participated in the decisions.  I do not attest the decisions are
optimal, only that they are what we agreed was most reasonable.  In
two cases I made small changes to the text in the section being
reviewed.  - TM 2026-08-08
