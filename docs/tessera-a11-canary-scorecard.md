# Scorecard: is Tessera's Amendment 11 the last repair, or the canary? (obs-0185)

*2026-10-29. Predictions: `predictions/2026-10-29-tessera-a11-canary-tony-and-claude.md`, stamped at `be17c05`
before any reader ran. Records: `results/tessera-a11-canary-2026-10-29/`. A service to Tony, A11's signer.*

## The answer

**A11 is not the final repair.**
- A11 names a defect class: a registered decision changes what an earlier sentence refers to, and nobody re-reads
  that sentence. **A11's own K-R change commits that defect three times.**
  - The frozen ENCODING-V1 §5.2 still has the issuer obtain `S_kms` from KMS.
  - The hybrid supplement's §1 still calls the issuer's μ computation "the issuer's only path".
  - The supplement's §11 item 6 still has the issuer calling KMS, and A11.5 item 3 calls those lines "unchanged".
- 13 or 14 of the 20 readers found this, in both arms and both reading modes, and both verifiers confirmed it.
- Of the 24 broad-arm findings, 13 would need an amendment beyond A11, in signed or frozen text. The owner's sweep
  never read most of that text: it skipped the frozen specification and, by its own account, the hybrid supplement.

Most findings are wording: wrong locators, stale restatements and unlisted rows. The substantive ones cluster on
the two decisions A11 asks Tony to make.

## Counts

151 candidates from 20 readers. The verifiers agreed on 127 and split on whether 22 were real. agy broke those
ties: 4 real, 18 not real. **28 findings** after deduplication. A finding is counted for each arm whose reader
proposed it.

| | Findings | Touch A11 | Substantive | Repair: A11 draft / new amendment / editable only |
|---|---|---|---|---|
| Narrow arm | 12 | 12 | 6 | 11 / 0 / 1 |
| Broad arm | 24 | 8 | 9 | 7 / 13 / 4 |

Proposed by both reading modes: 8 of 28. Agentic readers only: 14. Whole-packet readers only: 6.

Model spend was $8.89 on OpenRouter. About $2.40 of that went on five runs truncated at a 32k cap, which returned
no answer and were re-run at 120k. The CLIs (Codex, agy, grok) and the Claude subagents used subscriptions.

## Predictions

| | Prediction | Result | |
|---|---|---|---|
| T1 (Tony) | narrow arm 2–3 | 12 (6 substantive) | miss |
| T2 (Tony) | broad arm ≥ 6 | 24 | **hit** |
| T3 (Tony) | broad, touching A11: 1–2 | 8 | miss |
| T4 (Tony) | narrow > broad on A11-touching findings (dilution) | 12 > 8 | **hit** |
| C1 | narrow arm: point 3, range 1–6 | 12 | miss |
| C2 | broad arm: point 9, range 4–18 | 24 | miss |
| C3 | broad, touching A11: point 2, range 0–4 | 8 | miss |
| C4 | narrow > broad on A11-touching findings | 12 > 8 | **hit** |
| C5 | ≥ 1 finding outside the sweep needs a registered text changed | yes (K-R cluster, and 13 needing a new amendment) | **hit** |
| C6 | ≤ 40% of broad findings already in the sweep | 5 of 24 (21%), and the sweep dismissed all 5 | **hit** |
| C7 | fewer than half proposed by both reading modes | 8 of 28 (29%) | **hit** |

Tony's mechanism (T4) held: the narrow arm found half as many A11-touching findings again as the broad arm. Both of us
underestimated the size: the narrow count by 4 to 6 times, the broad count by about 2.7 times.

## Against the owner's sweep (`SWEEP-2026-10-28.md`)

Five broad findings are ones the sweep looked at and dismissed. The verifiers judged all five real:
- **A2:300**: the anchor. The sweep said "A9.5 withdraws the frame-only layout", but A9.7 doesn't list the line.
- **PROPERTIES:167**: the sweep said "the amendment wins". This one is editable only.
- **prereg:401**: the sweep called the TTL lines "vacuous". The key-compromise mitigation still rests on them.
- **A10.4.1, two findings**: the sweep said "cut by name (profile §5)", but no amendment's change table lists the cut.

The other 19 were never seen by the sweep. The sweep ran before A11 took on the K-R change. So no sweep, the one
A11.4 requires included, ever ran against A11's own changes.

## Findings for the three decisions (live A11 re-checked: all still present)

Locations are in the readers' copy of A11 (155 lines). The live file (162 lines) has the same text, 7 lines later
from §A11.2 3(c) onward.

**Decision 2, K-R: accept the substance, but not this wording.**
- ENCODING-V1.md:557: "The issuer obtains `S_kms` … from KMS with `MessageType EXTERNAL_MU` only, sending μ".
  A11.3 doesn't list it. *Substantive.*
- HYBRID-SUPPLEMENT.md:61-65: "External μ … is the issuer's only path"; "the issuer always computes μ". Not
  listed. *Substantive.*
- HYBRID-SUPPLEMENT.md:524: "the issuer always uses EXTERNAL_MU for the kms slot". A11.5 item 3 calls 524-526
  "unchanged". *Substantive.*
- A11.5 item 5 says the signer validates "ε" with no qualification. HYBRID-SUPPLEMENT.md:495 says manifests carry no
  declared time, so the ε check doesn't apply to possession signing.
- Locators: "computed by the issuer" is on :153, not :151-152. Item 5 cites :148-172, which leaves out :173-174.

**Decision 1, the slot-2 signer: neither branch is clean as written.**
- **Yes branch:** condition (i) requires preserving "every property in the frozen record". That record says
  production "retain[s] the selected, deadline-qualified custody implementation" (V1-PROFILE.md:1025), which is
  exactly what the ruling relaxes. As drafted, the condition can't be met.
- **No branch:** "production uses the deadline-qualified prototype signer" conflicts with the freeze record:
  "Instrument code under `prototype/` stays instrument code" and may reach service only by porting with its own
  evidence (FREEZE-RECORD.md:62; A9:198-199). *Substantive.*
- `service/issuer/DEPLOY.md` steps 6–7 deploy `signer-gcp` and retire the prototype unconditionally. The
  deployment plan assumes Yes before the ruling. *Substantive, editable.*
- V1-PROFILE.md:1429-1435 (§14.2 item 5) restates the 21 Oct deadline-qualification rule. A11.3 row 3 doesn't list
  it.

**Decision 3, the amendment as a whole.**
- A10.4.1, rows 25–33. Signed A10 pre-authorized a cut only "for schedule reasons" (A10:455-456). The E9 ruling cut it
  as "an author scope decision, not an invocation of the schedule-slip cut order" (AUTHOR-RULINGS.md:9). No change
  table lists the cut. A11 repairs one symptom of it (A10:675, "row 25"), so A11 is the natural place to register the
  cut itself. The profile also cuts rows 25–32 but still cites row 33 (V1-PROFILE.md:621-622, :1258-1259).
  *Substantive.*
- A11:59: "223 tests, mutation-sensitive (PROFILE.md §6)". §6 mutates nine checks (222 passed, 1 skipped), and the
  owner vector files hold 123 vectors.

**Before any of the three: the bytes.** The P3 floor, `service/signer-gcp/` and `service/signer-kms/` were untracked
in git when the corpus was copied. A11 registers the floor by a manifest hash. That hash changed from `a69204e9…` to
`844cb7ff…` 30 seconds after the copy. Signing A11 alone doesn't fix those bytes in git.

## Broad findings outside A11 (for a later amendment; Tessera's call)

- **Substantive:**
  - A2:260-262 and V1-SERVICE-RESOLUTIONS.md:23. A2 requires waiting through declared + δ + S (96 h). The resolution
    fails any request still incomplete 24 h after acceptance, so a timely-eligible attempt can be failed.
  - A1:444 and A9:143. A1 has authority asserted "at issue time". A9 C4 says DNSSEC "establishes no publication
    before issue". A9.7 doesn't list A1:444.
  - A1:182 and A9:223. A1 has the parameters ratified at Band 0 exit. A9.2 ratifies them by its own signature.
  - V1-PROFILE.md:1395 and :1421/:1437. "YubiKey 2" appears both in the release-key independence item and as the
    repository root, and the release key must be unusable by the repository key. **Tony, 2026-10-29:** "I have four
    unused YubiKeys sitting on the desk in front of me. We had not established how they would be used or
    distributed." So the texts name a device assignment that was never made, and "YubiKey 2 is not in hand" is stale.
    The assignment is an author decision, and it must satisfy the independence requirement (release key separate
    from the repository key).
- **Wording:** ENCODING-V1:334 (the scheme row), ENCODING-V1:538 ("what the gpg signer emits"), V1-PROFILE:386 ("both
  OpenPGP adapters"), V1-PROFILE:850 vs :1182 (whether the anchor digest is an identifier), V1-PROFILE:1244 (the d3
  reason code under hybrid), PROOF:134 (the fingerprint "no V1 check reads"), HYBRID-SUPPLEMENT:154 vs :342 (the RAW
  capture's tag), prereg:640 (dual-signing restated), PROPERTIES:167 (S omitted), V1-SERVICE-RESOLUTIONS:26 (H3 has no
  per-receipt cost).

## Limits

- These are textual findings. Nothing was executed.
- "Touches A11", "repair" and "severity" are verifier labels.
- The Claude reader, the Claude verifier and A11's author are one model family. Codex and agy are the counterweight.
- Codex verified quickly and leniently: 91 real, against Claude's 81.
- Deduplication unions both verifiers' `same_as` links, which can merge too much. The 28 is a floor on distinct
  findings, not a ceiling.
