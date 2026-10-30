# Tessera — Phase 0 Pre-Registration, Amendment 5 — the probe and cross-family findings: precision repairs, one boundary, three verifier obligations (2026-09-12)

> **Signing recorded, 2026-09-13 (AI collaborator, recording the record; the stale status line below is retained per amend-don't-rewrite).** The author's first commit containing this file is `504e662` (2026-09-12, "Completed further revisions, clarifications, and marked decisions."), OTS-stamped at `f0398ea`. By the sentence below ("the author's first commit containing this file is its signing act") this amendment has been in force since that commit. `README.md` and `formal/PROPERTIES.md` already read it so.
>
> **Status: PROPOSED — the rulings below were adopted in session
> 2026-09-12 (author); this document is the instrument and is not yet
> signed. It becomes in force on the author's commit of this file.**
> (Stated in the house form of Amendment 4's status line, and matching
> `ROUTED-2026-09-06.md` "What happens now", which registers this
> amendment as *drafted PROPOSED*. The labels are the
> `formal/spike/first-link/DECISION.md` ones: the per-section
> **ADOPTED (author)** labels are the author's endorsements; the
> document's own status is not.) Every ruling below was made by the
> author on 2026-09-12 in dialogue, answering items C1–C4 and C8–C11 of
> `formal/suite/ROUTED-2026-09-06.md` §C after three Codex pre-read
> passes (`docs/reviews/2026-09-11-codex-pre-read-of-routed-batch-c.md`).
> This text was drafted by the AI collaborator (Claude, Fable 5.1) the
> same day from those answers, quoting the author where he gave
> reasons. **The author's first commit containing this file is its
> signing act**, stated here so that the Amendment 4 status question
> (§A5.0) does not recur. Per amend-don't-rewrite, the original and
> Amendments 1–4 are not edited; this document states what changes
> and why.
>
> **What this document is.** The fifth amendment, layered on
> `phase-0-prereg.md` (`75207ba`), Amendment 1 (`03cd3db`), Amendment 2
> (`62f0c5f`), Amendment 3 (`8ae4720`), and Amendment 4 (`5188e7a`). It
> selects no mechanism and weakens no property. Three sections repair
> registered prose to a precise reading the models already implement
> or the probes exposed (§A5.1–§A5.3); one bounds a principle
> Amendment 4 registered too broadly (§A5.7); three register verifier
> checks the cross-family reviews showed the registered sentences had
> assumed without stating (§A5.4–§A5.6). Each of the three adds a
> post-freeze query and a companion to one suite family; those are
> registered as dated addenda in the family's `PREDICTIONS.md` before
> any model is changed.
>
> **Provenance.** Sources: the P9 and P10 non-discharging TLA+ probes
> commissioned by Amendment 4 §A4.1 (`formal/spike/tla-probes/P9/`,
> `P10/`, their `RESULTS-PROBE.md`); the cross-family falsification
> review of the four suite models
> (`docs/reviews/2026-09-06-codex-suite-falsification-s-p1-s-p2-s-p7-s-standing.md`,
> items 12, 18, 23); the Codex pre-read of the routed batch
> (2026-09-11, three passes); the author's answers of 2026-09-12.

---

## A5.0 Amendment 4's signing commit — CONFIRMED (author)

Amendment 4 was committed with its DRAFT status line unchanged at
`5188e7a` ("Address outstanding issues, clarify unclear text,
commission a (non-blocking) TLA+ probe"), OTS-stamped at `5dfd82b`.
The suite library's D-6 entry, the tracker's P9/P10 rows, and the
seven S-STANDING models read that commit as the signature. The author
confirms it: `5188e7a` is Amendment 4's signing commit and Amendment
4 has been in force since. (ROUTED C1: *"C1-C4 as recommended."*)

## A5.1 P9's conformance vector: what it must carry — ADOPTED (author)

**What Amendment 4 says.** §A4.1(ii): one H1a red-bar vector — the
same bundle and declared policy, verified on two isolated machines
with no network, must yield the same verdict, and a verifier that
consults any optional service must fail the vector.

**What the P9 probe showed** (`formal/spike/tla-probes/P9/RESULTS-PROBE.md`
F2–F4; three stateful verifiers written besides the pure one —
`LIVE_FALLBACK`, `LIVE_FAILCLOSED`, `REPLAY_LATCH`. On the two-machine
VECTOR configuration two of the three are wholly undetected
(`LiveFallback_Vector.out`, `ReplayLatch_Vector.out`: both invariants
green) and the third is caught only by the probe's `Purity`
invariant — the expected-verdict oracle that §A4.1(ii) as worded does
not carry; its agreement clause, which is what the wording says,
passes all three). (a) A verifier that consults an optional service and falls
back to the bundle when the service is unreachable is
indistinguishable from a pure one on two isolated machines. (b) A
fail-closed consulting verifier returns `UNVERIFIABLE` on both
machines: they agree with each other and disagree with what bundle
plus policy determine. (c) Verifier-local history (a replay latch) is
invisible to two fresh machines.

**§A4.1(ii) is hereby written as:** the vector carries the **expected
verdict** determined by bundle and declared policy; each machine's
verdict is compared to *that*, not only to the other machine's; one
case presents the same bundle twice on one machine and requires the
same verdict both times; and the clause "a verifier that consults any
optional service must fail" is discharged by the inspection leg (i)
together with one case in which the optional service is reachable and
contradicts the bundle, not by the two-machine run alone. P9's
discharge label is unchanged: **[inspection + vector]**. This is a
precision repair in the A4.2 style: the obligation is made to catch
what its own probe showed it missed; nothing is weakened.

## A5.2 Waived-but-failing evidence: the registered reading — ADOPTED (author)

**The fork the P10 probe exposed** (`formal/spike/tla-probes/P10/RESULTS-PROBE.md`
R1 and §C3). A `VALID_DEGRADED` verdict can coexist with a waived
channel evidence that is present and fails — invalid signature, late
anchor, or naming a different key. Under P4 as ratified (A4.2; waived
checks do not determine the verdict) the verdict stands and the
observation goes in the record. Under A3 §A3.2 item 2's second
sentence read literally — "Evidence that is present and whose
validation is performed but fails yields `INVALID`" — the verifier
refuses. Both probe modules pass every invariant; they differ on the
classification of that state, and the literal reading turns some
`VALID_DEGRADED` and `UNVERIFIABLE` cases into `INVALID`. Its cost is
an **availability attack**: an adversary who alters only the waived
evidence in a bundle — no authority compromised, bytes it may alter
under A1.3 item 1 — can turn an otherwise `VALID_DEGRADED` package
into `INVALID`.

**Registered reading: P4's.** A3 §A3.2 item 2's second sentence is
hereby written: "**Required** evidence that is present and whose
validation is performed but fails yields `INVALID`." Evidence the
declared policy has waived is evaluated and its condition recorded
(§A5.3) and never determines the verdict. Reasons: A3.2 item 5
already says P4 "remains correct but incomplete by abstraction";
refusing on evidence the policy waived contradicts the waiver's
purpose; and the alternative hands an availability attack to anyone
who can touch the bundle. The P10 probe's `_A32Reading` module is
the recorded rejected alternative. P4's `ExactDegraded` invariant is
unchanged.

**The registered reading's own cost, recorded.** It is not free: a
package may be reported `VALID_DEGRADED` while its bundle carries
waived evidence that is present and demonstrably fails — including one
naming a different key, which is evidence of equivocation and not mere
absence. The registered mitigation is §A5.3 (the observation is
evaluated and recorded) read with §A4.6 as bounded by §A5.7 (the
degraded label excuses nothing the waiver rules did not permit, and
the final evidence chain is not waivable — A3 §A3.2 item 1). That cost
belongs in the relying-party story, stated as the counterpart of the
availability attack the rejected reading carried.

## A5.3 What a degraded verdict records — ADOPTED (author)

**Two different "why"s.** P10 says the degraded verdict names "which
authority evidence was waived and why"; §A1.2.1 says the record holds
"the precise waived check set and the policy that authorized the
waiver". The first is what the verifier *observed* about the waived
evidence; the second is the *policy* that permitted the waiver. No
registered text required the observation to be recorded; under §A4.6
it is the load-bearing half for an adjudicator, who otherwise cannot
distinguish a lapsed registrar from a conflicting publication.

**Registered: both.** The verifier evaluates what it does not
require, and the record holds, for each waived check, the policy that
authorized the waiver **and** the verifier's observation of the
waived evidence — at least the six values the probe needed: absent,
unperformable, invalid, anchor-late, names-other-key, would-pass.
Evaluation is bounded by the bundle and the declared inputs (P9);
inability to evaluate is itself one of the recorded observations and
never a reason to consult anything. The record format is an H1a
obligation, entered on the band-1 docket. (ROUTED C4, with Codex's two
refinements.)

## A5.4 P2: all required signers attest to the same content — ADOPTED (author)

**What the review found** (cross-family review item 12; S-P2
`sp2_q2_degraded_compromised.pv`). Two honest signers under one
manifest can sign *different* payloads and the verifier accepts. P2's
registered text says the signed bytes commit to the required-signer
manifest and never says the signers attest to common content; the
frozen plan assumed it.

**The framing fork** (Codex pre-read, 2026-09-11). Each signer's
frame carries that signer's own key fingerprint inside the signed
bytes (P3's field list), so two signers' frames can never be
byte-equal. Either (a) common attested content in separate,
signer-specific frames, or (b) one shared frame with the key binding
moved into the manifest — which changes P3's field list and P8's
frame layout for multi-signer objects.

**Registered: (a).** The author: *"C8 seems obvious to me - what does
it mean if they signed different bytes?"* **How that is read, stated
so it can be corrected** (the wording is ROUTED's, not a stronger
one): the author's sentence endorses C8's recommendation, which is
(a); he did not name (a) or (b) himself. If he meant (b) — one shared
frame — then P3's field list and P8's frame change and the S-P2
addendum registered below is withdrawn. For a multi-signer
attestation, the six non-fingerprint fields of every required
signer's frame — object type, algorithm, identity, manifest hash,
canonicalization version, payload — are equal across signer slots;
only the key-fingerprint field differs. This is what "the canonical
signed bytes commit to the required-signer manifest" plainly meant.
P3's field list is unchanged. Three of the six equalities are already
carried by the shared manifest tuple (algorithm, identity, manifest
hash); the verifier gains the other three (object type,
canonicalization version, payload), and a payload-splicing companion
must go red. Registered in `formal/suite/s-p2/PREDICTIONS.md` as a
post-freeze addendum before any model is changed.

## A5.5 P7: the wrapper's recorded inner canonicalization version must be true — ADOPTED (author)

P7 says the wrapper "records both inner and outer canonicalization
versions"; the review (item 18) showed a lying record is accepted.
Registered: the verifier checks the wrapper's recorded inner version
against the inner frame's own canonicalization-version field and
rejects on mismatch; a lying-wrapper companion must go red. The
record is a checked claim, not an informational one. Registered in
`formal/suite/s-p7/PREDICTIONS.md` as a post-freeze addendum.

## A5.6 Standing binds to the identity in the core, not only to the key — ADOPTED (author)

The review (item 23) showed a core issued under identity A, with its
honest terminal lineage record, gains standing under a second honest
authority tuple naming the same key as identity B, because the
standing path binds the key to the presented tuple and never the
presented tuple to the core's embedded one. Registered: the standing
path checks that the presented authority tuple equals the tuple
embedded in the core it derives the artifact identity from —
`ENUMERATION.md` note 4 item 2's principle (the standing path relies
on nothing the envelope path established), applied to the tuple as it
is already applied to the key; an alias companion must go red. What
this does **not** decide: whether an issuer holding two identities on
one key keeps one terminal lineage record or two. The check settles
only that a core issued under one identity cannot gain standing when
presented under the other; a single TLR under that key may still name
cores from both. Registered in `formal/suite/s-standing/PREDICTIONS.md` as a
post-freeze addendum.

## A5.7 The boundary of §A4.6 — ADOPTED (author)

Amendment 4 §A4.6 says a correspondence that holds in strict mode and
fails in degraded mode is "never a defect of the construction —
provided the verdict says it is degraded." That is broader than what
the author ruled: read literally it would excuse accepting altered
bytes under an honest key (a P1 violation) or losing the last
complete evidence chain (an A3.2 floor violation) so long as the
verdict said "degraded". The author's reason — Tessera does not
decide for the adjudicator — licenses neither. §A4.6 is hereby
bounded by the following sentence, Codex's wording, adopted verbatim:

> Only losses permitted by the registered waiver rules and the
> declared policy are degradation costs. A degraded label does not
> excuse violating a non-waivable requirement or misreporting a
> required check's outcome.

This keeps the verifier/adjudicator division, bounds what Tessera
claims to have verified, and explicitly prevents a declared policy
from waiving the final evidence chain. The drafting error was the
collaborator's; the record of its detection is the Codex pre-read.

## A5.8 What did not change

No property is weakened; no mechanism is selected or altered; no
tracker row moves on this amendment. P3's field list and P8's frame
are unchanged (§A5.4 chose the reading that leaves them so). P4's
model and companions are unchanged (§A5.2 registered the reading the
model implements). The three verifier obligations of §A5.4–§A5.6
change no registered prediction of their families; each is a new
query with its own registered prediction and companion, recorded as
a post-freeze addendum, and each family's tracker row moves only on
its other recorded prerequisites (ROUTED C5, as corrected
2026-09-11). Band 0's exit list (§8) is unchanged.
