# eCFR recheck of 48 findings (2025 CFR edition)

eCFR date used: **2026-10-22** (titles 12 and 31 "up_to_date_as_of"; latest issue dates 2026-10-05 and 2026-10-15). The full-text endpoint needs `Accept-Encoding: gzip`.

## Wrong addresses (24)
- still_wrong: 23
- section_gone: 1
- fixed: 0
- unclear: 0

## Stale twins (24)
- still_diverged: 24 (current ratios within 0.01 of the 2025 ratios; the highest is 226.13 at 0.934)
- converged: 0
- section_gone: 0

## Items that are NOT still_wrong / still_diverged
- **12 CFR 810.6** (section 3(a)(12) of the Securities Exchange Act, cited as 15 U.S.C. 78(a)(12)): section_gone. It returns 404, and the versioner history shows all of part 810 (Federal Financing Bank bills) removed effective 2025-06-16.

## Notes
- The two 12 CFR 48.2 rows and the two 12 CFR 328.107 rows are separate occurrences in the same section. Both occurrences are still present.
- In 45.2, 47.2, 237.2, 349.2, 624.2 and 1221.2, the first section 202(a) citation is correct (80b-2(a)). The second one, under "private fund", still reads "80-b-2(a)".
- 208.77 has one correct citation (12 U.S.C. 1820(d)) and one still-wrong citation (18 U.S.C. 1820(d)).
- 208.31 currently reads "78q-l" (letter l, not 1).
- For every twin, a quick keyword check agrees with the reader note's direction: the 1026/1005/1002 copy has the later amendments. Some notes swap the A and B labels relative to old and new.

Per-item details: recheck.jsonl. Scripts: fetch.py, analyze.py, evidence.py, assemble.py. Cache: cache/.
