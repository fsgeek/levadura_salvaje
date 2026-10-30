# Band 0 — property obligations tracker

Working tracker for discharging the pre-registered properties of
Amendment 1 §A1.2 (commit `03cd3db`, anchored), as amended by
Amendment 2 (`docs/phase-0-prereg-amendment-2.md`, ADOPTED 2026-07-21
after three non-author review rounds and the clock-precedence ruling;
its model obligations are tracked here). The *authoritative*
statements live in the amendments; this file only tracks discharge status
and artifact locations. If this table and the amendment ever disagree, the
amendment wins — and the disagreement is a bug in this file.

Status values: `open` → `modeling` → `checked` (tool passes) →
`discharged` (tool passes + agreement-gate falsification review passed).
Per A1.1, any weakening of a property is *not* recorded here — it
requires a signed amendment.

**Amendment 4 (signed 2026-09-06, `5188e7a`)** moved P10 to `checked`
([model] half; tool assignment corrected to ProVerif), changed P9's
discharge label, ratified P4's fail-vs-unperformable precedence,
qualified P4's and P5/P6's registered sentences to what the models
implement, registered the general degraded-mode principle (§A4.6), and
commissioned non-discharging TLA+ probes of P9 and P10 whose green
results are never cited here.

**Amendment 5 (adopted 2026-09-12; in force on the author's commit of
`docs/phase-0-prereg-amendment-5.md`)** moves no row. It registers
P4's reading of waived-but-failing evidence (§A5.2), the
degraded-verdict record content (§A5.3), the P9 vector's required
cases (§A5.1), three verifier checks for P2, P7 and standing with
post-freeze symbolic queries and companions registered before any run
(§A5.4–§A5.6), and the boundary of A4.6 (§A5.7).

| Prop | Short name                         | Discharge      | Tool (A1.4)        | Status | Artifact |
|------|------------------------------------|----------------|--------------------| -------|----------|
| P1   | Integrity (headline)               | [model]        | TLA+ and ProVerif  | checked | `formal/suite/s-p1/` Q1 both channel variants + Q2 (headline); companions Q3/Q4 red on exactly the headline, N1 reachable in all five; TLA+ half owned by P4's verdict partition across the `Accept` ↔ P4 join (`formal/tla/P4_VerifierStates.tla`; COVERAGE-MAP row 1), never symbolically discharged |
| P2   | Signature-set completeness         | [model]        | TLA+ and ProVerif  | checked | `formal/suite/s-p2/` Q1 both variants + Q2 (the P2 claim); companions Q3/Q4/Q5-C2 red on exactly their named queries, Q5-C1/C3 green as registered, N1 witnesses reachable; §A5.4 common-content query Q6 green, companion Q6-C red on exactly `Spliced` (2026-09-12); TLA+ half: degraded clause joins P4 `DegradedNeedsExplicitWaiver`, non-Accept paths join P4's verdict partition (COVERAGE-MAP row 2 note, 2026-09-12), never symbolically discharged |
| P3   | Key binding (anti-DSKS)            | [model]+[assum]| ProVerif; H1a prof.| checked| `formal/suite/s-p3/` ([model] half; [assum] half open, H1a) |
| P4   | Fail-closed state logic            | [model]        | TLA+               | checked| `formal/tla/P4_VerifierStates.tla` |
| P5   | Temporal soundness (verifier side) | [model]+[assum]| TLA+               | checked| `formal/tla/P5P6_TemporalRevocation.tla` |
| P5c  | Issuance corollary (depth k, reissue)| [model]      | TLA+               | checked| `formal/tla/P5c_IssuanceProtocol.tla` |
| P6   | Revocation over uncertainty window | [model]        | TLA+               | checked| `formal/tla/P5P6_TemporalRevocation.tla` |
| P7   | Wrapper / object-type soundness    | [model]        | ProVerif; H1a vector (A6.1; was TLA+ and ProVerif) | checked| `formal/suite/s-p7/` Q1 both variants + Q2 (C1/C2, InnerSigTransplanted); companions Q3/Q4×2/Q5c/Q6a/Q6b red on exactly their named queries, Q4 opaque control green, Q5 depth-2 green; §A5.5 recorded-version query Q7 green, companion Q7-C red on exactly `VersionLied` (2026-09-12); verdict-independence half: Q4 control + companions and the A6.1 H1a vector (docket) |
| P8   | Canonicalization inj. + framing    | [proof]        | Lean4 or prose+vec | open   | —        |
| P9   | Verification statelessness         | [inspection+vector] (A4.1) | inspection; H1a vector; TLA+ probe non-discharging | open   | inputs enumerated `formal/spike/standing-probe/RESULTS-PROBE.md` Q6; two-machine vector owed (H1a) |
| P10  | Manifest authority                 | [model]        | ProVerif (A4.1; was TLA+); TLA+ probe non-discharging | checked| `formal/spike/first-link/` Q1/Q3 both variants; `formal/suite/s-p3/` Q1 strict; degraded half carried by P4; possession half S-P3 ledger 2 |
| SC   | Standing evidence (A3 §A3.7.1)     | [model]        | ProVerif           | open   | `formal/suite/s-standing/` (seven models + SS.Q6/Q6-C, tool passes; panel criterion 4 condition 2 not claimed satisfied) |
| A3.6.2 | Unknown-algorithm verdict transition (A3 §A3.6.2 item 3) | [model] | TLA+ (P4 module) | checked| `formal/tla/E6a/` (2026-10-19, PROPOSED, AI collaborator): `E6a_AlgVerdict` instantiates P4's `VerdictFor` unchanged; 32 invariants green in the V1 (7,938 states) and general (15,876) instances; 13 witnesses reachable as expected; fail-open companion red on `UnknownAlgNeverValid`, plus six further companions (mixed case, missing signature vs missing evidence, dispatch) red, all 14 per-invariant matrices exactly as predicted; P4 re-run unchanged. `formal/tla/E6a/RESULTS.md`. Codex falsification pass and E9 read owed (registered 2026-08-09; row added 2026-09-13, note below) |
| A3.7.2 | Extended atomic-entry refusal invariant (A3 §A3.9, §A3.7.2 bullet) | [model] | TLA+ (P5c module) | open | — (registered 2026-08-09; row added 2026-09-13, note below) |

Cross-cutting obligations (A1.4, A1.7):

- [x] Tool spike complete; choice committed (`formal/spike/DECISION.md`)
      **before any substantive proof work** (A1.4). **Chosen: ProVerif**
      (2026-07-05; Tamarin rejected on the counterexample-readability
      tie-breaker).
- [ ] Symbolic-suite architecture (ruled in dialogue 2026-07-28;
      requirement-level restatement 2026-08-07, scope narrowed on
      Codex non-author review same day; author accepted as written
      2026-08-07, adoption completes at commit — see
      `docs/reviews/2026-08-07-survivability-mechanisms-ruling.md` §1):
      per-property ProVerif models over a shared theory library; every
      model carries an explicit assumes-from-elsewhere ledger holding
      two entry kinds — dischargeable cross-model obligations and
      exposed Layer 2 assumptions; **Band 0 exit is gated on a
      capstone composition context in which every ledgered cross-model
      assumption is discharged by a machine-checked producer query and
      carries a broken companion that must fail the query consuming
      the severed link; Layer 2 assumptions are explicitly exposed and
      unclaimed, never silently absorbed.** Any termination-forced
      scoping is named in-module and disposed by amendment discipline,
      never silently. Implementation note (non-binding, subject to the
      mechanism spike below): current candidate is a single capstone
      model that transcribes the shared library. Obligation text
      registered at requirement level in Amendment 3 §A3.3 (adopted
      2026-08-09, commit `8ae4720`). The suite itself remains unbuilt;
      this box closes when the per-property models, ledgers, and
      capstone exist and are checked.
- [x] Capstone mechanism spike (2026-08-07 ruling §2; precedes the
      suite scaffold) — **COMPLETE 2026-08-13**: first-link spike run
      per its frozen registration (`formal/spike/first-link/`), all
      queries and negative controls as predicted or with registered
      branches fired and recut on the record; mechanism decision
      entered at `459aff0` (transcription binding; DECISION.md status
      DECIDED, stale-header correction at `33e196e`); form lifecycle
      DEFERRED (band-1 docket item 18). Original obligation text
      retained below. Was: exercise the capstone pattern at representative
      complexity — the linked evidence floor chain (2026-07-28
      Ruling 2) — real-first, ablate on break. The drafted
      assumes-from-elsewhere ledger interface (conservation-rule
      schema in the 2026-08-07 ruling §1) is the spike's scaffolding
      (one artifact, not two; merges the middle step of the A3 →
      ledger interface → scaffold sequence). Per-query timebox
      declared before running, with three named outcomes: query
      violation (counterexample), timeout (mechanism-viability
      failure — ablate or change tactic; not evidence about the
      property), successful termination (evidence for the checked
      abstraction only). Predictions registered before running.
- [ ] Every symbolic lemma carries a prose mapping to its A1.2 property.
- [ ] Cross-model correspondence mapping (TLA+ ↔ symbolic) in the written
      proof.
- [x] Cross-model correspondence (TLA+ ↔ TLA+): P5c (issuance) and P5P6
      (verifier) agree on the A2.1 confirmation predicate in prose but
      model the quantity incompatibly — operational `depth` vs. free
      integer `confirmedAt`; the join was asserted, not checked.
      **Bridge model built and checked 2026-07-21:**
      `formal/tla/P5cP5P6_Bridge.tla` — block timestamps decoupled from
      the tick clock (skewed, non-monotonic), `confirmedAt` DERIVED from
      the chain (never latched — the by-construction vacuity trap
      avoided), issuer and verifier transcribed independently (depth
      convention vs. height-h+k−1 convention), with the `DepthK = k − 1`
      pin as a checked INVARIANT, not an ASSUME. Green (456k states):
      PinAgreement, ShippedDesignatedAgree (the join itself),
      HonestShipAccepted (A2.1's by-construction claim, now checked),
      LateBurialRejected; all six vacuity witnesses fire, including the
      ε side (unrepresentable under P5c's fused clock) and wall-clock/
      chain-time divergence. Companions: `_BrokenAnchorSubst` (the
      obligated one — verifier substitutes `anchorAt`) red on exactly
      the correspondence + late-burial invariants, isolation green
      passes; `_BrokenWallClock` (P5c's fused-clock ship rule
      transplanted) red on HonestShipAccepted — A2.1's "why chain time
      on both sides" exhibited; `_BrokenPin` cfg (DepthK = KConf) red at
      configuration time. Scoped abstractions, named in the module: one
      attempt (no retry/refusal), no reorgs (A1.6 permanence — reorg
      re-verification NOT discharged here), stateless verdicts, no
      UNVERIFIABLE arm. **Design-time finding routed to the A2 review
      rounds:** A2.1's "The rule" sentence states conjunct 3 only; under
      decoupled clocks conjunct 3 does not imply conjunct 2, so the
      issuer must evaluate the full VALID_STRICT at ship (the bridge's
      Ship does; A2.1's prose should say so). Calibration artifact:
      `docs/reviews/2026-07-21-claude-predictions-bridge-bench.md`.
      Surfaced 2026-07-18; "burial delay vanishes" did NOT reproduce
      under Codex non-author check on the fused model, and the bridge
      confirms: the vanishing requires the broken substitution.
      Disposition REGISTERED at Amendment 3 §A3.7.3 (adopted
      2026-08-09, `8ae4720`) and validated in scope by the cold panel's
      addendum round (`docs/reviews/2026-08-08-A3-panel-disposition.md`);
      the bridge broken companion for the exact finding and the
      conjunct-3 red-bar vector land in the H1a suite per A3. See
      `docs/exploration-2026-07-18-causal-dag-commons.md` §0/§8/§8b.
- [ ] Agreement-gate falsification reviews run by non-author models
      — P3 [model] half: run 2026-09-05 (two non-author models, blind,
      `docs/reviews/2026-09-05-blind-falsification-sp3-q2.md`); author
      read of the corrected Q2 header against P3's sentence passed the
      same day ("the narrowed header says what that verifier does, no
      more"). Row moved `open` → `checked`; `discharged` waits on the
      [assumption] half (verification profile, H1a evidence).
      — P4, P5, P5c, P6 (TLA+): cross-family review run 2026-09-06
      (Codex gpt-6-astra, one run per module, jailed by content;
      `docs/reviews/2026-09-06-codex-tla-falsification-p4-p5p6-p5c.md`,
      inputs under `formal/tla/falsification-2026-09-06/`). No
      invariant or status changed; three registered-text precision
      items ROUTED to the author (P4 fail-vs-unperformable precedence
      ratification; "required" qualifier on P4's unperformable
      sentence; qualifier on Amendment 1's revocation-after-anchor
      sentence); header/comment fixes and two mechanical additions
      owed by the collaborator. **Correction to this file's P5c entry
      below:** the `RefusalBuriedAnchorUnreachable` witness fires at
      `MaxTime = 12` (re-run confirmed, 21 violations), so "+DepthK
      headroom = 14 exercises post-refusal burial" is not what that
      witness guards — it does not encode chronology; recut owed.
      Author reads of the plain-language statements: not yet
      possible (reading aids for these modules not yet written).
      Other properties: not yet run;
      artifacts in `docs/reviews/`.
- [ ] Conformance vectors extracted from checked traces (feeds H1a).
- [ ] Informal written proof (defend-it-cold) in repository.
- [ ] Parameter ratification at Band 0 exit: δ = 72h, ε = 24h, k = 6,
      and (A2.3) the issuance attempt bound N (working default 3).
- [x] **P5 issuance corollary** (anchor confirmed at depth k within δ;
      re-issue on late/reorged anchors) — modeled as a real state machine
      in `formal/tla/P5c_IssuanceProtocol.tla` (checked; broken companion
      exhibits ship-shallow-then-reorg, the Gemini-named harm). The
      semantic fork the model surfaced (strict vs. permissive reading)
      was RATIFIED strict on 2026-07-07 in the chain-time form —
      `confirmed_at := timestamp(block h+k−1) ≤ declared + δ`, one
      predicate for issuer and verifier — by Amendment 2 (A2.1), which
      also pins the depth convention `DepthK = k − 1`.
- [x] **A2.2 confirmation-timing conjunct (verifier side)** — added to
      `formal/tla/P5P6_TemporalRevocation.tla` (`confirmedAt`,
      `AbandonedArtifactRejected`; checked, all invariants green, all
      vacuity witnesses fire). New broken companion `_BrokenConf` carries
      the pre-A2 verifier: ForgeryRejected and ReceiptIndependence HOLD,
      AbandonedArtifactRejected VIOLATED with the abandoned-anchor
      artifact as the counterexample — the A2.0 correction made
      mechanical (the artifact is no forgery; only the new conjunct
      rejects it).
- [ ] A2.2 conformance-vector cases: late-burial artifact → `INVALID`;
      headers unavailable → `UNVERIFIABLE` (with the general extraction
      obligation above).
- [x] **A2.3 refusal state** (2026-07-20, round-3 ruling 4 construction,
      AUTHOR-ADOPTED FOR STAGE-ONE DRAFTING; non-author review passed
      same day, `docs/reviews/2026-07-20-codex-p5c-refusal-review.md` —
      "accept the atomic-entry safety construction", three prose
      overclaims folded) — `refused` added to
      `formal/tla/P5c_IssuanceProtocol.tla` by **atomic entry**: the Tick
      expiring the FINAL attempt's window records the refusal in the same
      transition, making it a transition-level safety fact — safety-only,
      no fairness, no liveness claim. Checked (all green, MaxTime raised
      8→14: minimum 12 = MaxAttempts·(Delta+1) for the final window to
      expire at all — below it the refusal invariants are vacuous, the
      `RefusalUnreachable` witness guards; +DepthK headroom = 14
      exercises post-refusal burial, the `RefusalBuriedAnchorUnreachable`
      witness guards): `NoSilentDeadlock` (no reachable state with the
      final window expired and no refusal recorded),
      `RefusedOnlyWhenExhausted` (which contains shipped/refused mutual
      exclusion), and action property `RefusalLatched` (in-model latch).
      New companion `P5c_IssuanceProtocol_BrokenSilent` implements the
      review's warned construction (separately enabled Refuse,
      postponable): red on exactly `NoSilentDeadlock` among the checked
      set; its `_Green` cfg (all other invariants) passes. Ship and the
      refusal trigger deliberately overlap at now = declared+Delta — an
      intentional boundary race, named in the module. Discharged claim
      (narrowed on review; the reviewer withdrew its own round-3
      wording): **the abstract refusal state is entered atomically and
      latches** — storage durability, retrievability, and reporting are
      Amendment 3 disposition items (the refusal tracker line; A2.3's
      draft text was aligned to this split 2026-07-21). Also explicitly unclaimed: that the final
      crossing ever occurs (Tick is postponable; safety-only).
      Calibration artifact:
      `docs/reviews/2026-07-20-claude-predictions-p5c-refusal-bench.md`
      (first run caught a TLA+ precedence bug that silently disabled the
      atomic entry — `NoSilentDeadlock` flagged its own author's error).
      **Note 2026-09-06 (STATUS: PROPOSED — produced by the AI
      collaborator; not adopted; the commit is the author's; appended,
      nothing above altered).** The parenthetical above, "+DepthK
      headroom = 14 exercises post-refusal burial, the
      `RefusalBuriedAnchorUnreachable` witness guards", was not true of
      the witness as it stood: `~(refused /\ depth >= DepthK)` encoded
      no chronology, and an anchor placed before the refusal and buried
      by the final ticks satisfied it at `MaxTime = 12` (cross-family
      review item 15, `docs/reviews/2026-09-06-codex-tla-falsification-
      p4-p5p6-p5c.md`; confirmed by re-run, 21 violations). **Recut
      2026-09-06:** `P5c_IssuanceProtocol.tla` gains one recording
      variable, `refusedAt` (the clock value at which the refusing Tick
      entered the refusal; sentinel before), one guard invariant on it,
      `RefusalTimeConsistent`, and the witness becomes `~(refused /\
      anchorAt >= refusedAt /\ depth >= DepthK)` — the anchor must have
      landed at or after the refusal instant and then reached full
      depth. Re-run 2026-09-06: main cfg green on all six invariants and
      the action property (3606/2190 states, unchanged); `_Sanity` all
      seven witnesses fire at 14; the recut witness does NOT fire at
      `MaxTime = 12` or 13 (`formal/tla/falsification-2026-09-06/P5c/
      recut/`), so the sentence above is true of the recut witness.
      `_Broken` and `_BrokenSilent` carry the variable verbatim (their
      "identical state space" claims stay literal); `_Broken` red on
      `NoShippedOrphan`, `_BrokenSilent` red on `NoSilentDeadlock`,
      `_BrokenSilent_Green` green with `RefusalTimeConsistent` added to
      its set. Every committed `.out` in `formal/tla/` was regenerated
      the same day so trace line numbers match the modules (review item
      19). Log: `formal/tla/falsification-2026-09-06/FIXES-2026-09-06.md`.

**Note 2026-09-12 — P1 → `checked` (STATUS: PROPOSED — produced by the AI collaborator; not adopted; the commit is the author's; appended, nothing above altered).** P1's row is moved `open` → `checked` on the three prerequisites disposition B2 records (`formal/suite/ROUTED-2026-09-06.md` B2; `formal/suite/s-p1/RESULTS.md` "Status toward discharge"): (a) the S-P1 ladder — five models, all three correct runs green on every registered query, Q2(ii) red as registered, both companions red on exactly the headline with N1 reachable; (b) P4 already `checked`; (c) the `Accept` ↔ P4 verdict-partition join written in `formal/COVERAGE-MAP.md` row 1 with P4's four producer invariants named — written, not checked, and per ENUMERATION §4 never dischargeable by a symbolic query. The author's C5 read of the Q2 claim block (`formal/suite/READ-C5-2026-09-12.md`) returned one NO — model line 28's "in degraded-compromised mode it is not" — repaired in place to "it need not be" with a dated CORRECTION marker citing the N1 witness; the model re-ran byte-identical. `discharged` waits on the agreement-gate falsification review being read by the author and on the cross-model correspondence mapping; the 2026-09-06 Codex cross-family review of this family has run but the author has not read it. Committed with this move: the COVERAGE-MAP row 1 amendment note that disposition B3 announced (below, note 3).

**Note 2026-09-12 — P2 → `checked` (STATUS: PROPOSED — same provenance).** P2's row is moved on the prerequisites `formal/suite/s-p2/RESULTS.md` "Status toward discharge" records: tool passes (all correct models green, N1 witnesses reachable, every companion red on exactly its named query, C1 green as registered); the author's C5 read of the Q2 claim block returned YES (2026-09-12); ROUTED C8 ruled (Amendment 5 §A5.4, reading (a)) and its leg run (Q6 green, Q6-C red on exactly `Spliced`); and the `Accept` ↔ P4 join for P2, which S-P2's ledger entry 4 already states, now written into `formal/COVERAGE-MAP.md` row 2 (note 3 below) in the same form as row 1's. `discharged` waits on the author's read of the 2026-09-06 cross-family review and on a cross-family review of the §A5.4 additions (running 2026-09-12, not yet reported).

**Note 2026-09-12 — SC row added `open` (STATUS: PROPOSED — same provenance).** A3 §A3.7.1's standing invariant has had no row in this file since the construction was selected (2026-09-04, `formal/spike/standing-probe/DECISION.md`, whose "Entered" note records "PROPERTIES.md is untouched"); `formal/COVERAGE-MAP.md` row 13 carries it as "no TRK row", which that file's own legend calls an open cell, and its header makes this file the home of record. The row is added `open`, not moved. Its recorded prerequisites, assembled here from three files for the first time: panel criterion 4 (`formal/spike/FIRST-LINK-SPIKE.md` item 4, signed `8ae4720`) — the chosen mechanism modeled in the symbolic suite before Band 0 exit under the A1.3 adversary, RULED stands as signed 2026-08-29; ENUMERATION amendment note 4 items 1–2 — the A3.7.1 invariant as the query, the Kimi-2 transplant as the companion, the SC-3 outcomes as mandatory red vectors, the S4 row with pairwise-distinct reason codes and a collapsing companion, and the entitled-key check inside the standing path. Condition 1 (selection) is satisfied; condition 2 is open by the family's own statement (`formal/suite/s-standing/RESULTS.md`, "What S-STANDING does not discharge"). The author's C5 read of the S-STANDING claim block returned YES on 2026-09-12 and is recorded against this row; the §A5.6 tuple-pin query SS.Q6 and its alias companion are run but not falsification-reviewed. Band 0 exit remains gated on this row. Also not moved today: P7 — the author's C5 NO on model line 55 is repaired only after the running cross-family review finishes reading the file, and no record yet accounts for P7's assigned TLA+ leg (routed to the author separately).

**Note 2026-09-12 — P7 → `checked` on Amendment 6 (STATUS: PROPOSED — produced by the AI collaborator; not adopted; the commit is the author's; appended, nothing above altered).** ROUTED D1 was adopted by the author in session (*"let's go with your recommendation as the project owner"*): P7's tool assignment is amended by `docs/phase-0-prereg-amendment-6.md` §A6.1 to ProVerif plus one H1a conformance vector, the verdict-independence half being discharged by S-P7 Q4's opaque-embedding control and re-serialization companions plus the vector. The row moves on that amendment's signing commit. Its other prerequisites: tool passes (`formal/suite/s-p7/RESULTS.md` "Status toward discharge" and the 2026-09-12 addendum); cross-family reviews run 2026-09-06 and 2026-09-12; the author's C5 read returned one NO (model line 55, the wrapper's authorship misattributed to S-P3 entry 1), repaired in place the same day, re-run byte-identical. `discharged` waits on the author's read of the two reviews.

**Note 2026-09-13 — two registered model obligations given rows `open` (STATUS: PROPOSED — produced by the AI collaborator; not adopted; the commit is the author's; appended, nothing above altered except the two rows added to the table).** Amendment 3 §A3.9 says its obligations are "tracked in `formal/PROPERTIES.md` upon adoption"; the amendment was adopted 2026-08-09 (`8ae4720`) and two of them never received a row. (1) §A3.6.2 item 3: "the formal model's P4-partition transition with a broken companion — a verifier that fail-opens past an unknown algorithm must go red", with the verdict boundary of §A3.6.2 item 2 (`UNVERIFIABLE` for exactly one case — a well-formed, correctly bound, unsupported identifier; `INVALID` for the listed malformations). (2) §A3.9's refusal-record bullet: "the extended atomic-entry invariant — every transition entering `REFUSED` simultaneously establishes the complete local refusal record, the commitment value, delivery = `PENDING`, and publication = `PENDING` (the archived P5c proof covers the latch alone) — with its primary broken companion latching refusal while postponing or omitting one of those creations, and a second companion in which `DELIVERY_FAILED` or any reporting state re-enters issuance or decrements the attempt bound; both must go red." `formal/COVERAGE-MAP.md` rows 4, 6 and 15 recorded both as "no TRK line" on 2026-09-06. The rows are added `open`, not moved; neither is modelled. Both are Band 0 model obligations by their registration and appear as item E6 of `formal/BAND0-EXIT.md`.

**Note 2026-09-13 — reading aids for P4, P5/P6, P5c exist (STATUS: PROPOSED — produced by the AI collaborator; not adopted; the commit is the author's; appended, nothing above altered).** The falsification bullet above says "Author reads of the plain-language statements: not yet possible (reading aids for these modules not yet written)". `formal/tla/READING-AID-P4.md`, `formal/tla/READING-AID-P5P6.md` and `formal/tla/READING-AID-P5c.md` have existed since 2026-09-06; the sentence is superseded and left as written. The author's read of these four rows' review findings is `formal/BAND0-EXIT.md` item E9, one batched sitting.
