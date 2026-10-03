# The request for Codex review 2 (rule-currency v3)

Launched 2026-10-03 from the repo root, in the background, with stdin closed. Its output goes to
`docs/rule-currency-review-2.md`. If that file is missing (the run was still going at handoff,
or a restart killed it), rerun:

```
codex exec -s read-only --skip-git-repo-check -o docs/rule-currency-review-2.md "Adversarially review rule-currency lens v3 in this repository (branch lens/rule-currency-v3): src/levadura_salvaje/structure.py (CFR paragraph ancestry in citation-span coordinates) and its tests tests/test_structure.py; rule_currency.excerpt_v3 in src/levadura_salvaje/lenses/rule_currency.py; scripts/measure_rule_currency_qwen.py (items() now parses XML); scripts/audit_rule_currency.py (probes); scripts/probe_rule_ancestry.py; scripts/verify_pins.py; docs/rule-currency-v3-design.md; predictions/2026-10-03-rule-currency-v3-claude.md (check via git log that it precedes the v3 results); results/rule-currency-qwen-v3-902-2025.jsonl and results/rule-currency-audit-v3-902-*; ledger entries obs-0162 to obs-0164; and the 'v3' section of docs/rule-currency-scorecard.md. Find: (1) correctness bugs in structure.py (offset mapping raw->flat->normalized, paragraph ranges, level assignment, ancestry, enclosing/attachment, applicability selection), in excerpt_v3 (wrong parts, wrong paragraph, truncation, the window fallback), and in the audit probe handling; (2) whether W1-W7 verdicts follow from the files or overclaim, especially the 'structure cuts both ways' and 'one ambiguity' readings; (3) whether the claim that reader A follows the lens's carryover criterion is right by the criterion's text; (4) whether verify_pins checks what it claims; (5) what the tests don't check. Rank by severity with file:line. Do not modify files." < /dev/null > /tmp/codex-review-2.log 2>&1 &
```

Note: since the request was written, v4's lens wording (rule_currency.py, LENS_VERSION 4) and
predictions were committed on the same branch. The review targets v3. Read it against the
commit before v4's (`git log --oneline` — "rule-currency v4: closed_inputs label ...").
