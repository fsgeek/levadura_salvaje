# Adversarial review 3 of the investigator design

*2026-09-25. Codex (GPT family, codex-cli 0.155.0, read-only sandbox), on draft 3 and
the code at commit 88f1b6f (before `worlds.plant` existed). Kept verbatim; line
references are to that commit. The first attempt hung waiting on stdin and was
killed; this is the second run.*

**No. Draft 3 is not yet acceptable with its stated claims.** It could become an acceptable feasibility pilot, but its headline measure cannot identify memory use, and its snapshot protocol can manufacture the failure it seeks.

References: **D** = [draft 3](/home/tony/projects/levadura_salvaje/docs/investigator-design.md), **K** = [currency_key.py](/home/tony/projects/levadura_salvaje/src/levadura_salvaje/currency_key.py), **W** = [worlds.py](/home/tony/projects/levadura_salvaje/src/levadura_salvaje/worlds.py). All 26 existing tests pass; they do not cover the principal failures below.

**Review-2 dispositions**

| Finding | Verdict | Reason |
|---|---|---|
| CRITICAL: database access dressed as investigation | **Partially fixed** | Narrowing is real; D exists. But “ceiling” and architectural conclusions still exceed the comparison (D:25–31). |
| HIGH: incomplete currency semantics | **Partially fixed** | Identity, withdrawal and derived-report rules are explicit (D:35–52); scoring still conflates dimensions and lacks type validation. |
| HIGH: probe weighting | **Partially fixed** | Fixed events, lags, controls and denominator help (D:79–101). Target/path sampling and end-of-run handling remain unspecified. |
| HIGH: assessment isolation/resources | **Partially fixed** | Package labeling and numerical budgets help (D:108–140). Snapshot fidelity and random-state isolation are unestablished. |
| HIGH: fragile variance estimates | **Fixed for narrow feasibility claims** | Repeated runs and conservative scenarios are appropriate (D:149–166). Shuffling remains limited structural variation. |
| MEDIUM: full-context success | **Fixed** | Explicitly legitimate, with cost reporting and an equivalence margin (D:143–145). The margin alone cannot establish statistical equivalence. |

For review 2’s inherited review-1 checklist: **1 partial; 2 fixed; 3 partial; 4 fixed for package comparisons; 5 partial; 6 partial; 7 fixed for feasibility; 8 fixed by removal; 9 partial.** Remaining reasons follow.

**CRITICAL — “From memory” measures absence of a new ledger call, not memory or misremembering.** [D:102–106](/home/tony/projects/levadura_salvaje/docs/investigator-design.md:102)

F·L can copy a current answer directly from its prompt without calling anything. P can correctly retain an updated measurement acquired during the preceding wake. P can also use `recall`/`compare` without a ledger call. Conversely, an irrelevant ledger call makes an answer cease to count as “from memory.” These are fundamentally different behaviors collapsed into one metric.

Rename it **“no probe-time ledger call,”** report it for every arm, and separate factual accuracy, source currency and actual evidence exposure. Claims of persistent obsolete belief require prior documented endorsement. Making a nonzero rate a headline failure overcorrects **against P**, punishing successful caching.

**HIGH — The proposed snapshot can omit the update and perturb the continuing experiment.** [D:110–114](/home/tony/projects/levadura_salvaje/docs/investigator-design.md:110)

[`seed_history`](/home/tony/projects/hamutay/src/hamutay/taste_open.py:3252) reconstructs state **before** `up_to_cycle`, excluding that cycle. Passing the “current cycle” after an update drops the freshly updated state: an artificial lag-zero disadvantage for P. Specify post-wake snapshot timing and the required cycle offset.

Moreover, [`_pick_memory`](/home/tony/projects/hamutay/src/hamutay/taste_open.py:3283) uses module-global randomness. In-process probes can advance the live run’s future memory draws while its log hash remains unchanged. The cited ablation explicitly supplies `force_memory`; this design does not. Test identical rendered inputs/state/history under controlled injection, and isolate probe RNGs. Log immutability is insufficient.

**HIGH — The scorer turns provenance errors into apparent memory failures and accepts wrong types.** [K:74–90](/home/tony/projects/levadura_salvaje/src/levadura_salvaje/currency_key.py:74)

I reproduced `{value: true, source_id: current}` scoring **correct** when the numeric key is `1`: Python equality is not typed validation. An invented value `999` with an obsolete source scores **stale**, indistinguishable from accurately recalling an obsolete measurement. Equal-value replacements likewise inflate “staleness” without factual error.

Withdrawal status is a defensible rule, but null-valued withdrawals expose another bug: matching an obsolete null value with the withdrawal’s current ID scores wrong, because missing current `value` also becomes `None`.

Validate answer variants/types and report factual/status accuracy, provenance currency and obsolete-value matches separately. Validate field paths across replacement chains; `pick()` otherwise raises rather than classifying.

**HIGH — The actual experimental distribution remains discretionary.** [D:79–96](/home/tony/projects/levadura_salvaje/docs/investigator-design.md:79)

The generator implements neither event planting nor shuffled epochs ([W:10–11](/home/tony/projects/levadura_salvaje/src/levadura_salvaje/worlds.py:10), 94–121). No frozen rule selects targets, scalar paths, or feasible matched controls. Events near epoch 22 cannot receive +3 probes without an explicit extension or restriction. Wake instructions are also absent: what makes P acquire the eventual target before replacement?

These choices can favor either arm. Freeze them before outcomes; assert complete lag coverage, control eligibility and prior exposure. Stamping an unspecified sampler does not remove selection discretion.

**MEDIUM — D is an oracle, not yet an operational ceiling.** [K:36–57](/home/tony/projects/levadura_salvaje/src/levadura_salvaje/currency_key.py:36)

D directly scans all revealed records; subjects face capped tool responses. Its correctness is tautological because scoring calls the same function. Keep it as an independently checked answer oracle, and implement a deterministic client through the actual ledger interface. Neither universal success nor failure proves where currency “belongs” architecturally (D:28–31).

**MEDIUM — Neutralization removes prose but preserves fingerprints and damages realism.** [W:98–119](/home/tony/projects/levadura_salvaje/src/levadura_salvaje/worlds.py:98)

Keys and categorical tokens are allocated in encounter order from empty universes. Across two seeds, **147/147 value-key/string layouts were identical**. IDs and shapes also persist. This does not demonstrate answer leakage, but contradicts strong per-world neutralization claims. Independent numeric redraws destroy relational cues and can penalize P’s accumulated understanding. Randomize token mappings, audit structural shortcuts, and describe the task as opaque record retrieval.

**Minimum changes:** repair snapshot isolation and typed scoring; replace the memory claim with an observable call metric; freeze event/probe/wake rules; validate D through the tool interface. Then **yes for feasibility**, without causal claims about misremembering or architectural superiority.