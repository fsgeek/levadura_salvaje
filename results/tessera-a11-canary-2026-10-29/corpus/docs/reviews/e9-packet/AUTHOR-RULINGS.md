# E9 author rulings

## 2026-10-23 — Row 2: CUT

**AUTHOR RULING (Tony).** In the review conversation, the author stated:

> With that said, I think the decision for Row 2 is Cut, with the explanation that you recommended.

The author chooses to cut the service-key listing (A10.4.1) from V1.
This narrows the option (e) adopted on 2026-10-18; it is an author scope
decision, not an invocation of the schedule-slip cut order. It does not
retroactively authorize the owner's 2026-10-19 cut.

**Rationale (conversation summary).** Keep V1's complexity manageable;
accept the stated dual-authority-capture risk for early receipts; preserve
the option to protect future issuance. The author expects low initial use
and judges the risk from the system's existing complexity to be high.
This decision stands independently of the exit deadline.

**Accepted limitation.** An attacker controlling both DNS and git authority
channels can issue passing receipts under its own keys, even while the
original service keys remain uncompromised. Protection of honest signed
material remains subject to its registered assumptions. Release-key custody
(A10.4.2) remains required.

**Upgrade boundary.** A later version may add the listing for future
issuance. A listing created afterward cannot establish the required
pre-receipt commitment for earlier receipts. This is a known V1 limitation;
adding the mechanism later is an option, not an obligation.

This entry records Row 2 only. It neither accepts other E9 rows nor asserts
that dependent documents and freeze artifacts have been reconciled.

## 2026-10-23 — Consolidated E9 decisions

**AUTHOR CONFIRMATION (Tony).** After discussion of the packet and the
reviewer's clarifications, the author stated:

> Good, then I think we have decisions on all but Row 22, with requested clarifications for Row 22 and comments on Rows 6, 10, 13, 18, 21, and 23.

The following records the decisions reached in that conversation. ACCEPT
applies to each row's bounded statement in `docs/E9-READ-PACKET.md`, with
the comments below. Owner decisions retain their provenance. Acceptance
does not waive prerequisites, close deferred questions, establish production
conformance, or itself open the code gate or finalize the freeze.

| Row | Decision |
|---|---|
| R1 | ACCEPT |
| R2 | CUT (rationale above) |
| R3 | ACCEPT |
| R4 | ACCEPT |
| R5a | ACCEPT |
| R5b | ACCEPT |
| R6 | ACCEPT, with comment below |
| R7 | ACCEPT |
| R8 | ACCEPT |
| R9 | ACCEPT |
| R10 | ACCEPT, with comment below |
| R11 | ACCEPT |
| R12 | ACCEPT |
| R13 | ACCEPT, with comment below |
| R14 | ACCEPT |
| R15 | ACCEPT |
| R16 | ACCEPT |
| R17 | ACCEPT |
| R18 | ACCEPT, with comment below |
| R19 | ACCEPT |
| R20 | ACCEPT |
| R21 | ACCEPT, with comment below |
| R22 | PENDING — wording repairs requested; return for author review |
| R23 | ACCEPT, on corrected understanding below |
| R24 | ACCEPT |
| R25 | ACCEPT |
| R26 | ACCEPT |

### Comments and clarified scope

These are summaries of the author's comments and the clarifications discussed
with the reviewer, not verbatim author quotations or additional model results.

- **R6 — operational boundary.** The named operational environments are
  illustrative, not exhaustive. GCP already participates in signing; another
  provider's name does not establish independence. The requirement is
  independence from the operational environment, assessed by actual roles,
  credentials and release authorization. The author's concerns about trusting
  third-party security services remain relevant. Tupay's developing key
  mechanism is not a current Tessera requirement or dependency.
- **R10 — prose linkage.** Acceptance is of P4's bounded classification result.
  The prose correspondence to ProVerif acceptance is not a machine-checked
  composition. Separate passing models can disagree about required checks,
  their inputs or their outcomes; this is an assurance gap, not a demonstrated
  exploit or evidence of end-to-end correctness. The author raised concern
  about this boundary; acceptance does not close it.
- **R13 — two abstract channels.** The author asked whether the list was
  definitive. The clarified scope is exactly two modelled authority channels,
  corresponding to DNS and the repository, under the stated compromise cases.
  Concrete DNSSEC/git verification is outside the model. This is not a
  general result for arbitrary channels or providers; signing infrastructure
  and authority channels have distinct roles.
- **R18 — deferred questions.** Acceptance acknowledges the reported strict
  results without resolving the eleven unfinished degraded companion runs or
  the disputed key interpretation in the mutated standing check. Those
  deferred questions remain outside V1's strict, no-standing scope; the full
  capstone remains open.
- **R21 — missing statements.** Missing links hinder inspection of existing
  evidence; missing statements leave portions of the explanatory argument
  unavailable for inspection. Neither establishes an implementation exploit
  by itself, but both reduce assurance and can conceal coverage or assumption
  mismatches. Acceptance acknowledges the incomplete sheet and its limits;
  it does not supply missing statements or waive a registered prerequisite.
- **R23 — corrected interpretation.** This is not an any-one-of-multiple-GPG-
  signers rule, and it says nothing about simultaneous versus nested signing.
  A replacement signature can verify cryptographically while differing from
  the exact signature bytes committed in `A_sig`; the anchor check rejects
  it. The control supports binding the temporal evidence to those particular
  signatures.

Additional discussion preserved for context: R3's "fails" means no
`VALID_STRICT`, not necessarily INVALID; a valid replacement possession
signature over the same manifest is permitted. R5b allows source porting
after the opening, with production evidence earned on the resulting code.
R16 accepts the contract inspection, with execution evidence still due.
An adjudicator-facing contract and failure model, possibly analyzed with
Tupay, were discussed as subsequent work, not added exit prerequisites.

### Explicit reviewer reservations — 2026-10-23

**Reviewer: Codex.** The reviewer supports the rulings at their stated scope,
with the following reservations about their subsequent use. The author
described these reservations as reasonable and requested that they be noted.
They preserve limitations already discussed; they do not reverse the ACCEPT
decisions or create additional exit prerequisites.

- **R10 and R21:** accepting the classifier result and incomplete
  correspondence sheet must not be represented as establishing correct
  composition of the models or preservation of their guarantees by the
  implementation. The assurance gap remains real.
- **R18:** accepting the completed strict results must not close the capstone
  or silently resolve its deferred questions.
- **R6:** the operational boundary must follow actual dependencies and
  credentials, including GCP's role. Use of another provider does not by
  itself establish independence.

### R22 — requested repairs before reconsideration

The author agreed with the reviewer's recommendation to return the reliance
guide for bounded wording repairs. No ACCEPT or REJECT is recorded yet.
The requested corrections concern `docs/V1-RELYING-PARTY.md`:

1. Qualify "a missing or changed signature makes the check fail": distinguish
   the receipt signatures committed in `A_sig` from a possession signature
   that may be replaced with another conforming valid signature over the same
   manifest.
2. State that service keys sign frames binding the content, rather than
   suggesting that they sign the raw content directly.
3. Replace the absolute one-bit/hash-change explanation with wording subject
   to the registered cryptographic assumptions.
4. Clarify that CANNOT VERIFY prevents reliance as a verified V1 receipt but
   does not establish fraud or content falsity.

The production-key acquisition instructions still depend on the outstanding
bootstrap work; page acceptance must not imply that procedure is already
usable. These repairs do not require a new contract, Tupay analysis or an
expanded security project. Return the revised Row 22 material to the author.

### Review evidence and remaining mechanics

The reviewer reran `prototype/.venv/bin/python -B formal/p8/vectors/check.py`
in this review: baseline 71/71 golden, 173/173 rejection, 5/5 anchor negative
controls; hybrid 35/35 golden, 63/63 rejection, 1/1 anchor negative control,
6/6 gate demonstrations. R25's archived differential result for L-60 was
inspected, not regenerated. The registration and draft freeze hash entry
supporting R26 were inspected. The formal models were not all rerun.

This record does not assert reconciliation of the packet, its PDF, dependent
documents or freeze artifacts. Those mechanics and the signed opening remain
separate from these author decisions.

## 2026-10-23 — Row 22: ACCEPT

**AUTHOR RULING (Tony).** After the row 22 repairs (`docs/reviews/r22/`: repairs 1–4 and the bootstrap caveat,
checked by Codex, refinements R22-01 to R22-03 applied), the author stated:

> Two issues: (1) the packet's required reading range should now be lines 26–142, rather than 26–133, to include the complete verdict guidance. (2) nevermind, I figured it out on my own. With that I am ready to change Row 22 to Accept.

| Row | Decision |
|---|---|
| R22 | ACCEPT |

The packet's required range for row 22 is corrected to `V1-RELYING-PARTY.md` lines 26–142 (owner, same day). With
this entry every E9 row has a decision. This record does not itself finalize the freeze or open the code gate:
the freeze is reassembled from the commit carrying these rulings, then the signed opening commit follows.
