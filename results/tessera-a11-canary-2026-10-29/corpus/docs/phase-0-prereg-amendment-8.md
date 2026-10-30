# Tessera — Phase 0 Pre-Registration, Amendment 8 — the capstone's companion allowance, four registration corrections, the degraded companions' evidence, and the standing key (2026-10-07, extended 2026-10-09)

> **Status: PROPOSED — the rulings below were made by the author on 2026-10-07 in session; this document is
> the instrument and is not yet signed. The author's first commit containing this file is its signing act**
> (the house form since Amendment 5). Drafted the same day by the AI collaborator (Claude, Opus 5.5, owner
> instance) from the author's message answering the routed items of `formal/suite/capstone/RESULTS.md`.
> Layered on the original and Amendments 1–7, and on the frozen capstone registration
> (`formal/suite/capstone/PREDICTIONS.md`, frozen at `3568905`). Per amend-don't-rewrite, none of them is
> edited; the sentences this amendment supersedes are named and left standing in their files.

Labels are the `formal/spike/first-link/DECISION.md` ones. The author's words are in italics inside quotation
marks; everything else is the collaborator's instrumentation of them. On 2026-10-07 the author deferred two further items (*"I think ruling on this at this time is premature"*) and
ruled them on 2026-10-09 (A8.3, A8.4), after the throwaway prototype and the restriction analysis.

---

## A8.1 A companion runs under its case's per-case sum, not the box of the query it is predicted to red — ADOPTED (author)

*"I have no objection to accepting your recommendation for (2)."*

**Superseded sentence.** `PREDICTIONS.md:1868-1869`: *"a companion runs inside the box of the query it is
predicted to red"*, and the per-companion box sentences that follow it (C-C9, C-C16, C-C17, C-C18).

**Replacement.** A companion runs under its case's per-case sum, as the correct-form run does, and adds no
entry to the ceiling.

**This is an exception entered after the freeze, not a reading of the frozen text.** Every capstone run in
ladders 1–3 already ran under the per-case sum, and per-query time was never logged. The registered claim this
gives up is that each companion's severing shows within its 30–60-minute query box. No run measured that, so
nothing observed is lost. **For the method:** a future registration states the run limit it means, and logs
per-query time if it claims per-query boxes.

## A8.2 Four corrections to the capstone's registered red sets — ADOPTED (author)

*"the clerical issues and their proposed resolution seem reasonable to me."*

Each is a red the runs show, by construction of the mutation, that the registration failed to list. Sources:
`RESULTS.md`, "Amendment-shaped items", and `proverif/dev/divergences/DIAGNOSIS.md`.

1. **G1.** The authorship correspondences (`Accept ⟹ IssuerSigned`, honest-key authorship) join C-C5's set
   (1), and the unrestricted form joins C-C17's set (1), in the strict cases. C-C5's own cell describes the
   attack (`PREDICTIONS.md:1774`). This carries over to C-C5 and C-C17 the correction the 2026-09-17 skeptic
   repair S-4 made for C-C7.
2. **G4.** C-Q2 joins C-C15(i)'s set (1) in cases (a) and (b), as the registration's own sentence implies
   (`:2503`).
3. **Conjunct 3 under C-C15(i).** Set (1)'s conjunct-3 membership is assigned to case (d) only, which agrees
   with C-C15(i)'s strict Cases cell (green in strict, red in (d)) and with the runs.
4. **C-Q6 conjunct 1, unrestricted form.** It moves from C-C10's set (2) to its set (1) in (a) and (b), and
   joins C-C14's set (1) in (a) and (b). The dependence is the one `:1018` already encodes: the standing
   path's check 1 pins `t`, and C-C10 removes it while C-C14 subverts it. The honest-key forms stay in both
   companions' green lists. D12's severing (C-C11) is unaffected.

**Not an amendment:** G2 stands as a finding of the composition. The unrestricted standing verdict depends on
authority evidence exactly as `Accept ⟹ IssuerSigned` does.

## A8.3 The eleven degraded companions: slice reds, pre-registered before running — ADOPTED (author)

*"That's what we should do. We've analyzed this, we think we understand the limitations, and I've not seen
anything else that moves this project forward."* (2026-10-09, answering the owner's drafted rulings for
Decisions 1 and 3)

**Ruling.** A case-(d) set-(1) red of C-C2, C-C3, C-C4, C-C5, C-C6, C-C7(i), C-C7(ii), C-C8, C-C8-ii or
C-C17 may be descended from a **slice** of that companion's own registered file. A slice deletes whole
top-level parallel components and all but one query, and changes nothing else. The red counts only when
ProVerif reports `is false` with a reconstructed trace. A slice result **never** descends a green, a witness
requirement or a set (2). Slices, slicing rule and predicted reds are registered in
`formal/suite/capstone/SLICE-PREREG-2026-10-09.md` **before** any counted run. The exploratory runs of
2026-10-04/05 (`proverif/dev/slice_probe/`) are pilot data and are not counted. C-C8-i and C-C8-ii, whose
registered outcomes include greens, are carried on family evidence and labelled *not run under this blob*. No
row's severing rests on them.

**Why.** These companions are the evidence for a bounded **after-capture guarantee**. Here *capture* means only
this: authority-channel credentials are disclosed **while honest signing keys stay secret**. It does not cover
every institutional takeover, nor any signing-key compromise. Under that capture, the companions test that a
captor cannot reattribute honest frames, alter honest signer sets, or carry honest signatures onto other bytes
or keys. **They do not test temporal soundness.** Protection against backdating belongs to the temporal-anchor
models (P5/P6, TLA+) and their assumptions, which these runs do not exercise. The
composed runs cannot finish (ladder 2; `abl_d`). Slicing is sound for reds by trace inclusion
(`proverif/dev/slice_probe/REPORT.md` §2), and a cross-family review found it *sound with conditions*
(`…/codex/REVIEW.md`, `…/codex2/REVIEW.md`). The method and the choice of runs were informed by
the known failures and by successful pilot attacks, and that history is disclosed here and in the
pre-registration. Pre-registering fixes how the subsequent runs will be conducted and counted. **It does not
erase the retrospective origin of the method.** The rejected alternatives are family evidence only (it narrows
§A3.3), and restricting degraded verification to L0 (`proverif/dev/restriction/REPORT.md`: it makes D2 and
D5 unseverable and kills four witnesses).

**Condition.** `slice.py` is validated per source format. Any change to a source's format needs a fresh
structural audit before its slices count.

## A8.4 Standing certifies the key the innermost acceptance actually verified under — ADOPTED (author), reading C

(Same message as A8.3.)

**Ruling.** C-Q6's `kX` is the key under which the **innermost** acceptance actually verified the signature.
The agreement between the standing key and that key is a **property to be checked**: a new query, predicted red
under C-C15(i), registered in the same pre-registration and run with A8.3's batch. This resolves the conflict
between `PREDICTIONS.md:786-791` and C-C15(i)'s cell (`:2503`) in favour of the verified key. Reading A
(the presented key, as a definition) and reading B (C-Q6 not asserted of C-C15(i)) are not adopted.

**The same ruling governs two specification items.** The spec and the prototype are to be changed to follow
it. Until they are, the spec still carries the presented-key wording and O-74 stays open, and the prototype
still makes its outermost-layer choice:
- **O-74 (R-6.24 step 6):** standing compares the terminal lineage record's key against the key the innermost
  acceptance verified under.
- **R-6.44:** standing binds to the innermost layer, as BF-5 already models. The prototype's outermost-layer
  choice (`prototype/GUESSES.md` G-44) is superseded.

**Why.** "True by construction" was where the model and reality parted in the prototype's one false-assumption
finding (signature malleability). A relying party relies on the key that actually verified, not on the key
the bundle names.

## A8.5 What changed, and what did not

- **No property is weakened** (A1 §A1.1). No correct-form verdict depends on A8.1 or A8.2; all 173 are as
  registered.
- **The ten divergent companion configurations** of `RESULTS.md` §2a become *as registered* under A8.2 where
  their divergence is G1, G4, conjunct 3, or C-C10/C-C14's C-Q6. Any that remain divergent are listed when the
  results are re-read under this amendment.
- **Pending runs (A8.3, A8.4):** the eleven's (d) cells and C-C15(i)'s C-Q6 results stay as they are (not run
  under this blob; withheld from discharge) until the pre-registered runs are frozen, run and read. A8.4's query
  runs on the correct form and the three C-C15 configurations, in files derived for that purpose. Ladder 3's
  blob and its other files are untouched.
- **Out of scope, recorded for the relying-party story:** preventing a captured or merged authority from
  issuing new attestations (`docs/guarantee-tiers-DRAFT.md`, "Authority capture").
- **Unchanged:** the ceiling and its exceedance (6.46× over three ladders), and every box in §3's query
  table.
