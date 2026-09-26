You are an independent, blind scorer for a pre-registered pilot in the repository at the current directory. Another model family designed it; you have no stake in the result.

Read ONLY these:
- predictions/2026-09-25-record-currency-pilot-claude.md (predictions R1-R11, stamped before any model call)
- docs/investigator-design.md (the design, including the "Failed calls" and "Size" sections, which record deviations made before scored data)
- results/pilot-v1/analysis.txt (output of scripts/analyze_pilot.py)
- results/pilot-v1/**/probes.jsonl and wake_failures.jsonl (raw scored probes), scripts/analyze_pilot.py, src/levadura_salvaje/currency_key.py
Do NOT read docs/handoffs.md, any file named *scorecard*, or git log messages; they carry other instances' framing.

Tasks:
1. Independently recompute from the raw probes.jsonl files (write your own short script; do not import analyze_pilot.py): per-arm accuracy, obsolete rate, invalid rate, no-probe-time-ledger-call rate, and the R6/R7/R8/R10 breakdowns. Report any disagreement with analysis.txt, and any bug you find in analyze_pilot.py.
2. Score each of R1-R11 as pass / fail / not scorable, against the stamped wording exactly. For each, quote the wording, give the number(s), and state every judgment call you had to make (e.g. whether C counts as scored under R2 given the design says C probes are failed attempts; how "every model arm" is read; which probes count as "changed-value replacement"). Where a reasonable reader could score it the other way, say so.
3. R11 (cost <= $40): use the per-probe and per-wake costs in the raw logs if present; the design states a total of $38.92 from billing — say whether the raw files can confirm it.
4. List anything in the data that the predictions did not anticipate and that a scorer should report.

Be terse and exact. Output markdown.
