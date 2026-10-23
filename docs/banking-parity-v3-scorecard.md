# Scorecard: the parity lens, v3

*Scores predictions/2026-10-23-banking-parity-v3-claude.md (stamped at 05e89b5 before v3 ran)
against obs-0177 and audit A4 (`results/banking-parity-audit-a4/`, 20 fresh controls read blind
by Opus (A) and Sonnet (B)). Written 2026-10-23.*

| # | Predicted | Measured | |
|---|---|---|---|
| W1 pairs | 2,575 (2,540–2,600) | 2,580 | hit |
| W2 flags | 24 (22–27) | 24 | hit |
| W3 A3-real flags still flagged | 24 of 24 (≥ 23) | 24 of 24 | hit |
| W4 A3-false flags still flagged | 0 (≤ 1) | 0 | hit |
| W5 new flags | 0 (≤ 2) | 0 | hit |
| A4 controls misaddressed | ≤ 10% | 0% (A) / 0% (B) | hit |
| v3 flags misaddressed (A3 labels carried) | ≥ 90% each | 100% (A, 24/24) / 95.8% (B, 23/24) | hit |

**What v3 is.** There are now 24 flags, and the readers judged every one of them (A) or all but
one (B) a real wrong address. The flags include the FDI Act § 10 cited in title 18, the Exchange
Act in title 17, the BHC Act § 4 cited at § 1842, the FHLB Act § 21B at 1421b, the Investment
Company Act § 3 at 80a-5, and the "80-b-2(a)" typo for 80b-2. Across A3 and A4, 40 blind controls
have been read twice with no misaddress.

**One change after the stamp, before any ledger entry.** In the dry run, `rekey_letters` as
pre-registered re-read 20 pairs. Two kinds were right: the one "section 4(s)" of the CEA, and
three CEA "1(a)" read as § 1a. Sixteen were wrong: "section 10(a)" of the Home Owners' Loan Act
at 12 U.S.C. 1467a(a) is subsection (a) of § 10, not a § 10a. None of these moved a flag, because
both keys map to 1467a, but the rule was too broad. It now re-reads a lettered designation only
when that removes a disagreement with the (act, N) consensus. One pair is re-keyed (the 4(s)).
The flag results are the same under both versions of the rule.

**What the prediction didn't cover.** Holding titles 7 and 50 changes the in-force figures, so P3
(50% of 22 rated flags cite a section in force) and P4 (99.3% of 139 rated targets in force) are
reported unscored.

**The shape of it.** The consensus map is a set of equivalence classes. Each class gathers the
ways the corpus writes one act section (long name, short name, "the Act" resolved per part) and
maps them to one U.S.C. address. The corpus builds the classes from its own citations, and a flag
is a citation that claims a class it doesn't belong to (Tony, 2026-10-23). Built for 1997, 2010
and 2025 and compared, the classes become the crosswalk the definitions diff needs.

**Cost.** Mechanical, about 100 s per run, mostly `Brillig.galumph`. The readers are Claude
subagents at no OpenRouter cost.
