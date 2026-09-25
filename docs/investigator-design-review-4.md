# Adversarial review 4 of the investigator design

*2026-09-25. Codex (GPT family, codex-cli 0.155.0, read-only sandbox), on draft 4 and
the code at commit 61657cd (the ledger tool was uncommitted work in the tree it read).
Kept verbatim; line references are to that state.*

**Verdict: not quite as written.** Draft 4 supports the narrow feasibility objective, but reproducible control contamination and malformed-answer crashes need fixing before the smoke test. These are small remaining changes, not a reason to redesign the pilot.

**Validation:** all **73 requested tests passed**, plus **8 ledger-tool tests**. I also exercised planting and probe resolution across seeds 0–399. Tests ran without file capture or cache writes in the read-only sandbox.

References: D = [design](/home/tony/projects/levadura_salvaje/docs/investigator-design.md), K = [scorer](/home/tony/projects/levadura_salvaje/src/levadura_salvaje/currency_key.py), W = [worlds](/home/tony/projects/levadura_salvaje/src/levadura_salvaje/worlds.py).

Review-3 minimum-change dispositions:

| Minimum change | Status | Assessment |
|---|---|---|
| Repair snapshot isolation | **Partially done** | D:113–123 correctly specifies `c + 1`, subprocess probes and live reseeding. Verification remains prospective and omits the requested snapshot-versus-live rendered-input/history comparison. |
| Repair typed scoring | **Partially done** | K:88–139 separates value/provenance and rejects booleans as numbers. Non-object answers still crash; current-field validation remains absent. |
| Replace memory claim with observable call metric | **Done** | D:125–132 explicitly withdraws “from memory” and defines the observable metric for every arm. The new endorsement metric has a separate flaw below. |
| Freeze event/probe/wake rules | **Partially done** | Sampling, lags and wake prompt are concrete (W:175–234; D:100–104), but controls violate the declared matching/untouched conditions. Prior evidence exposure is not recorded by this specification. |
| Validate D through tool interface | **Done for this bounded pilot** | [ledger_tool.py:40](/home/tony/projects/levadura_salvaje/src/levadura_salvaje/ledger_tool.py:40) implements paginated D; tests check answers and ≤12 calls. D shares the oracle’s resolver, so agreement is not independent semantic validation; hand-worked scorer tests provide that check. |

**CRITICAL — None found within the stated narrow claims.**

**HIGH — “Untouched” controls can receive the experimental update.**  
[W:223–234](/home/tony/projects/levadura_salvaje/src/levadura_salvaje/worlds.py:223) excludes used record IDs, not the quantity/population selected by latest-observation queries. It also sets `observed_at=None` for repeat controls. With generation and planting seed **8**, event `w-0149` and its control both query Q12/P111’s latest observation; the control’s correct source changes from `w-0007` to the planted `w-0149`. The “control” is treated.

Separately, seed **3** matches an epoch-7 target with an epoch-3 control because line 223 silently falls back to any eligible epoch, contradicting D:55–57. [test_plant.py:59](/home/tony/projects/levadura_salvaje/tests/test_plant.py:59) checks direct replacement links, not these failures.

**Minimum:** select only targets with eligible matched controls; exclude overlapping queried identities and assert control answers remain unchanged throughout all probe lags.

**HIGH — Malformed model output can abort scoring instead of counting as invalid.**  
[K:88–96](/home/tony/projects/levadura_salvaje/src/levadura_salvaje/currency_key.py:88): reproduced `None` and `12` raising `TypeError`, and `[]` raising `AttributeError`. These are valid JSON values, although invalid answer variants. D:69–77 promises invalid answers remain in the denominator.

**Minimum:** check object type before inspecting keys; normalize parse failures and malformed variants to `invalid`. Add these regression cases.

**HIGH — Numeric occurrence is not documented endorsement.**  
[D:133–137](/home/tony/projects/levadura_salvaje/docs/investigator-design.md:133) counts an obsolete number appearing anywhere in prior state as “endorsed-then-obsolete.” A cycle counter, unrelated measurement, quotation or explicitly rejected value can satisfy that rule, especially for small integers.

**Minimum:** require an affirmative assertion linked to the same identity and field, plus documented exposure; otherwise rename this to “prior numeric occurrence” and remove “held”/“endorsed” interpretations.

**MEDIUM — Validation gaps remain.**

- [K:57](/home/tony/projects/levadura_salvaje/src/levadura_salvaje/currency_key.py:57) still raises `KeyError` when a replacement drops the requested field; validate probe paths across chains before running.
- D:120–123 checks continuing-run noninterference, not snapshot fidelity. Add the review-3 comparison of rendered inputs/history under forced identical memory. Freeze probe RNG seeds too.

**Proceed after those corrections:** build the harness with snapshot fidelity and isolation checks as smoke-test gates. The narrowed descriptive claims are otherwise acceptable.