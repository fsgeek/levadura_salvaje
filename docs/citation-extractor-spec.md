# Code citation extractor for 26 CFR: specification (v1)

## 0. Scope and output

**Input:** the text of one regulation section. It comes with `part` (for example `1`, `57`, `301`), `reg_id` (for example `1.414(r)-7`), and `truncated` (a boolean; true when the text was cut at the character cap).

**Output:** an ordered list of records. There is one record per Code citation occurrence.

```
{ path: "56/b/1/A" | null,      # section + "/"-joined designators; null = unresolvable
  section: "56", desig: ["b","1","A"],
  span: [start, end],             # offsets in the NORMALIZED text; start = offset of section-number token
  head: "section" | "sec_abbrev" | "sign" | "usc26" | "inverted" | "continuation",
  group: int,                     # records produced from one head share a group id
  range: {from: path, to: path, level: "section"|"desig"} | null,
  flags: [ ... ] }                # see §3; flags never change the path
```

- A path checks against USLM as `/us/usc/t26/s` + `path` (for example `/us/usc/t26/s56/b/1/A`).
- Designator case is kept as written: `A` and `a` are different.
- Section numbers are kept verbatim, including suffixes: `263A`, `45Y`, `1400Z-2`.
- A record with `path: null` means the text refers to the Code but the target can't be determined. It must carry a `kind` field: `anaphor` or `range_open`.
- **Out of scope, never emitted as paths:**
  - Structural units (chapter, subchapter, subtitle, part, subpart).
  - The Code as a whole ("the Code", "Title 26 of the United States Code").
  - The Code section embedded in a regulation number (§ 1.338(h)(10)-1 yields nothing).

**Dedupe rule:** a character offset can be the section-number token of at most one group. When two rules would claim the same token, the inverted form (§1.5) wins, and after that the earlier head wins.

---

## 1. Normalization (applied first, in order)

1. Replace NBSP (U+00A0), thin space and other Unicode spaces with a normal space. Collapse runs of whitespace, newlines included, into one space. All offsets refer to this normalized text.
2. Italic designators: `\(\s+([A-Za-z0-9]{1,6})\s+\)` → `(\1)`. So `( a )` becomes `(a)`, and `( 1 )` becomes `(1)`.
3. Doubled keyword: `\b[Ss]ection\s+§` → `§`. So "Section § 414(r)-8" becomes "§ 414(r)-8".
4. Do **not** change case, and do not touch `l` versus `1`.

---

## 2. Positive forms

### 2.1 Tokens (Python `re` syntax)

```
SECNUM   = (?P<sec>\d{1,4}(?:[A-Z]{1,2}(?:-\d{1,2})?)?)      # 1, 42, 263A, 6038D, 45Y, 1400Z-2
DESIG    = \((?P<d>[a-z]{1,6}|[A-Z]{1,6}|\d{1,3}[A-Z]?)\)     # candidate; level-validated below
REG_BLOCK= (?!\s?\.\d)                                         # SECNUM must NOT be followed by ".digit"
GLOSS    = \s*\((?![a-z]{1,6}\)|[A-Z]{1,6}\)|\d{1,3}[A-Z]?\))[^()]*(?:\([^()]*\)[^()]*)*\)
                                                               # any balanced parenthetical that is not a lone designator
```

A `SECNUM` must end at a word boundary, and it must not be followed by `\.\d` or by `,\d`. If `\.\d` follows, the token is a regulation number ("Section 1.822-3", "section 1.475(c)-1(c)", "Section 57.3(a)(2)(ii)"). Reject the head. The regulation token and every item in its list continuation are consumed as not-code (§3.1).

### 2.2 Designator levels (the chain grammar)

The levels follow the Code's hierarchy:

| level | name | accepted token |
|---|---|---|
| L1 | subsection | `[a-z]` (one letter; includes `l`, `i`, `v`, `x`) |
| L2 | paragraph | `\d{1,3}[A-Z]?` |
| L3 | subparagraph | `[A-Z]` or a doubled letter `([A-Z])\1` |
| L4 | clause | lowercase roman `[ivxl]+`, and it must parse as a valid roman numeral |
| L5 | subclause | uppercase roman `[IVXL]+`, valid roman numeral |
| L6 | item | doubled lowercase `([a-z])\1` (`aa`, `bb`) |

**CHAIN:** the `DESIG` tokens that follow `SECNUM`. Each token is either *adjacent* (no space) or *spaced* (exactly one space before the `(`).

1. The first designator is expected at L1.
   - If it is a digit, accept it and add the flag `irregular_chain`. This covers old `1221(1)` and the OCR form `3121(1)(8)`.
2. Each later designator is expected at the previous level + 1. It is classified by that expected level only: `(i)` at L1 is the letter i, and at L4 it is roman one.
3. **Adjacent** designator that doesn't fit the expected level:
   - If it fits some level, append it and add `irregular_chain`.
   - Otherwise, end the chain.
4. **Spaced** designator: append it only if it fits the expected level exactly. Otherwise, end the chain before it.
   - This accepts `7701 (a)(40)`, `4947(a) (2)`, `1402(b)(1) (G)`, `2039 (e)`, `1382 (b)(2)`.
   - It stops `959 (c)(1) (c)(2) (c)(3)`, a flattened table, after `959(c)(1)`, because `(c)` is L1 where L3 was expected.
5. A parenthetical that is not a lone designator ends the chain. Examples: `(relating to …)`, `(interest)`, `(see …)`, `(and in section …)`, `(Code)`.
6. After the chain:
   - If `\s?-\s?\d` follows, the whole match is a **regulation number with its part prefix missing**. Reject it (§3.1, E2). Examples: `§ 414(r)-5(f)`, `section 7701(b)-1`.
   - If `-\(` follows, it is a designator range (§2.4).

### 2.3 Heads (where a citation can start)

Every head is followed by `\s*` and then `SECNUM`, `REG_BLOCK`, and `CHAIN`.

| id | head regex | notes |
|---|---|---|
| H1 | `\b[Ss]ections?\b` | Case-insensitive on the first letter. Matches "section", "Section" and "sections". "subsection" doesn't match (no `\b`). |
| H2 | `\b[Ss]ec\.` | Accepted only under the authority-note rule in §3.3-A. |
| H3 | `§(?!§)` | A Code cite only if REG_BLOCK and the post-chain `-\d` test both pass, as in "§ 408(d)(4)". Nearly every `§` in 26 CFR is a regulation, and these checks reject them. `§§` is always a regulation list. |
| H4 | `\b26 U\.S\.C\.\s*\(?` | The optional `(` handles `26 U.S.C. (856(f)(2))`. Any other title (`25 U.S.C.`, `11 U.S.C.`) is **not** a head. |
| H5 | the inverted form, §2.5 | |

**Things that are never heads:** a bare number, `Form N`, `Article N`, `T.D.`, `FR`, `CFR`, `Stat.`, `Pub. L.`, `Example (n)`, `Q-n` and `A-n`, and `paragraph (x) of this section`. None of these can produce a citation.

### 2.4 Group continuation (lists, siblings, ranges)

After a head cite, repeatedly try to extend the group.

```
SEP  = (?:GLOSS)?\s*(?:,\s*(?:(?:and|or|and/or)\s+)?|\s+(?:and|or|and/or)\s+)
RSEP = \s+(?:through|to)\s+ | -            # range separators
```

A GLOSS may sit between items and is skipped: "section 162 (relating to …), section 170 (…), or section 217". Its contents are still scanned independently for their own heads.

Each continuation step is one of these:

**(a) Sibling designator.** `SEP` followed by `DESIG(\s?DESIG)*`.
- Find the attach level. It is the **deepest** level ≤ depth(previous item) whose charset admits the sibling's first designator.
- The new path is the previous item's path truncated to (attach level − 1), plus the sibling chain. The rest of the sibling chain is validated as in §2.2, starting from the attach level.
- If no level fits, or the previous item has depth 0, stop.
- Worked examples:
  - `4261(a) and (b)` gives `4261/b`.
  - `50(a)(3) and (6)` gives `50/a/6`.
  - `2632(b)(3) and (c)(5)` gives `2632/c/5`.
  - `152(b)(1), (b)(2), and (d)(1)(B)` gives `152/b/2` and `152/d/1/B`.
  - `6104(a)(1) (C) or (D)` gives `6104/a/1/C` and `6104/a/1/D`.

**(b) Bare section item.** `SEP` followed by `SECNUM CHAIN` with no keyword. This is allowed only when the group head is H1, H2, H3 or H4.
- The item is rejected, and the group ends, if the item is followed by any of these:
  - `\.\d`
  - `\s?-\s?\d` after a chain
  - ` U.S.C.` or ` Stat.` or ` CFR` or ` FR`
  - `,\d`
  - `\s+(?:percent|days|months|years|dollars)\b`
- It is also rejected if it is preceded by `$`.
- Examples: `section 162 or 212`, `section 1, 2, 3, or 11`, `section 301(d), 334(a), or 358(a)(2)`, `a section 501(c)(9), 501(c)(17), or 501(c)(20) organization`.

**(c) Repeated keyword.** `SEP` followed by a new H1/H2/H3/H4 head.
- This **ends** the current group and starts a new one: "section 2011 or section 2014", "sections 551-558 (…), sections 951-964 (…), and section 904".
- It matters because qualifiers (§3.2) bind per group.

**(d) Section range.** `SECNUM` `RSEP` `SECNUM`. This is allowed after H1, whether singular or plural ("section 2035 through 2038").
- Emit both endpoints as records, plus `range: {from, to, level: "section"}` on the second endpoint.
- **Do not enumerate the integers in between.** Section numbering is sparse and has letter suffixes. The checker expands the range against the USLM section list in document order.
- Hyphen ranges (`sections 861-863`, `sections 551-558`) are accepted only when both endpoints are pure digits and to > from. Otherwise, reject the hyphen token.
- `SECNUM` greedily keeps `1400Z-2` whole, because a letter comes before the hyphen.

**(e) Designator range.** `(x)` `RSEP` `(y)`, where `(y)` is a sibling. Examples: "(1) through (3)" and "(a)(1)-(17)".
- If both endpoints fall at the same level with the same charset class, and start < end (numeric, alphabetic or roman order), and the count is ≤ 60:
  - Enumerate every value inclusive.
  - Add the flag `range_expanded` to the interior items.
- If the end designator has a deeper chain than the start ("(a) through (c)(2)"), emit the endpoints only and add `range_unexpanded`.

**(f) Open range.** `SECNUM\s+and following`. Emit the section and add the flag `open_range`.

**Stop conditions.** The group ends at the first token that doesn't fit (a)–(f). In particular, it ends at:
- `§` or `§§`
- `paragraph`, `this section`, or `the regulations`
- `28 U.S.C.` or any `N U.S.C.`
- a sentence end

Examples: "sections 857(d) and § 1.857-7" emits `857/d` only. "section 6621 (b) § 301.6621-1" emits `6621/b` only.

### 2.5 Inverted form (subdivision before section)

```
INV = \b(?:sub)?(?:section|paragraph|subparagraph|clause|subclause)s?\s+
      (?P<list> DESIG(\s?DESIG)* (?: SEP-or-RSEP DESIG(\s?DESIG)* )* )
      \s+of\s+(?:(?P<kw>section)\s+SECNUM CHAIN REG_BLOCK | (?P<ana>such|that|said)\s+section\b)
```

The literal word `section` is required after `of`. `§` doesn't count, and neither does `this section`. So "paragraph (a) of § 1.954-5" and "paragraph (b)(1) of this section" never match.

- Each list item is appended to the section's chain. The first designator must fit level depth(chain)+1; if it doesn't, add `irregular_chain`.
- Ranges are handled as in §2.4(e).
- The span of the `of section …` part is consumed, so no separate bare record is produced for it.
- The trailing qualifier test (§3.2) applies after the SECNUM chain: "subsection (b) of section 553 of title 5 of the United States Code" yields nothing.
- If `ana` matched, emit `path: null` with `kind: "anaphor"`. "subparagraph (B) of such section" is an example. Do not resolve it.

Examples:
- `subsection (b) of section 346` gives `346/b`.
- `subsections (a) and (b) of section 3101` gives `3101/a` and `3101/b`.
- `paragraphs (1) through (10) of section 152(a)` gives `152/a/1` through `152/a/10`.
- `paragraphs (4), (6) and (8) of section 6334(a)` gives `6334/a/4`, `6334/a/6` and `6334/a/8`.

### 2.6 Explicit Code qualifiers

These confirm a Code citation. None of them is required. Most Code cites carry no qualifier, and the default is the Code.

After the group end, skip GLOSS parentheticals, then test:
- `of the Code\b(?! of Federal)`
- `of (?:the )?Internal Revenue Code(?: \(Code\))?(?! of 1939)`
- `of such Code`
- `,\s*(?:the )?Internal Revenue Code of (?:1954|1986)`

A match on the 1954 Code adds the flag `code_1954`. That Code is the current Code (renamed in 1986), so it is **not** an exclusion.

### 2.7 Attributive or term-of-art uses (emit and flag)

"section 338(h)(10) election", "the section 2801 tax", "section 197 intangibles", "section 4947(a)(2) trust", "section 987 QBU".

Add the flag `attributive` when either condition holds:
1. The head is immediately preceded by `\b(?:a|an|the|each|any|no|every|its|their|such)\s+`.
2. The next word after the group is lowercase alphabetic and **not** in this stoplist: `and or of to for in on at is are was were be been applies apply applied provides provide provided does do did shall will may must and as with by under through relating concerning including that which if unless except has have had not requires require described defined thereunder`.

The following noun is never part of the path.

---

## 3. Exclusions (emit nothing)

### 3.1 Regulation numbers

- **E1. Dotted regulation number.** A SECNUM followed by `\.\d` under any head, or anything after `§`/`§§` with the shape
  `\d{1,3}\.\d+[A-Za-z]*(?:\([^()\s]{1,6}\))*\s?-\s?[\dl]+[A-Za-z0-9]*(?:\s?\([^()]{1,6}\))*`.
  Examples: "§ 31.3402(g)-1(a)(2)", "Section 1.822-3", "Sections 48.4041-3 through …", "§ 1.1471- 5(b)(3)(i)", "§ 25.2502-l(c)(1)", "§§ 1.998-1.1000".
  - Its list continuation is consumed as regulation items with the same grammar as §2.4(a)/(b)/(d)/(e), and nothing is emitted. Examples: "§§ 44.4403-1 and 44.6001-1", "§ 1.414(r)-11(b)(6), (7) and (8)".
- **E2. Part prefix missing.** A chain followed by `\s?-\s?\d`. Examples: "§ 414(r)-5(f)", "§ 414(r)-8", "section 7701(b)-1 through (b)-9".
- **E3. The regulation's own number and heading.** `reg_id` is never converted to a Code cite. Text inside a heading line is still scanned normally.

### 3.2 Trailing qualifier naming another statute

Skip GLOSS parentheticals after the group end. Then optionally skip `,?\s*(?:and|or)\s+(?:chapter|subchapter|title|part)\s+[\wIVXLC]+\s+`. Then test the patterns below.

The qualifier binds to the **whole preceding group** (every item since the last head), and only that group. It never binds to an earlier group that had its own head.

| cue (regex, anchored at the test point) | meaning | example |
|---|---|---|
| `of the Internal Revenue Code of 1939` or `,\s*(?:the )?Internal Revenue Code of 1939` | 1939 Code | "section 24(b) of the Internal Revenue Code of 1939" |
| `of (?:title [IVXLC\d]+ of )?(?:the )?(?:[A-Z][\w.'&-]*\s+)(?:(?:[A-Z][\w.'&-]*\|of\|and\|for\|the\|\d{4})\s+)*Act\b` | named act | "of the Revenue Act of 1962", "of the Bankruptcy Act", "of title IV of the Social Security Act" |
| `of the Act\b` | act defined elsewhere (parts 2, 3, 302) | "section 511 of the Act", "section 607(g) of the Act" |
| `of (?:Public Law\|Pub\. ?L\.)` | public law | "section 7815(d)(14) of Public Law 101-239" |
| `of the Revised Statutes` | | "sections 3466 and 3467 of the Revised Statutes" |
| `of title (\d+) of the United States Code` with the title ≠ 26 | other U.S.C. title | "section 553 of title 5 of the United States Code" |
| `of the convention\|of the treaty` | treaty | |

Two exceptions:
- `as amended by the … Act` and `as added by … Act` are **not** exclusions. They qualify a Code section. Add the flag `historical` only if §4 says so.
- A `section N` inside that clause ("as added by section 144 of the Tax Reform Act of 1984") is its own head, and E-act applies to it.

### 3.3 Context rules

- **A. `Sec.`/`sec.` (H2) in authority notes.**
  - The segment runs from the head to the next H2 head or the close of the outermost enclosing parenthetical, whichever comes first.
  - Accept the cite only if the segment contains `68A Stat.`, or `Internal Revenue Code` not followed by ` of 1939`, or `26 U.S.C.` followed by the same SECNUM.
  - Otherwise, emit nothing. This covers the Tariff Act "Sec. 613, 46 Stat. 756" and the 1893 act "Sec. 3." quoted in part 50.
  - When an H2 cite is accepted, drop any H4 (`26 U.S.C.`) record in the same segment with an identical path, so the citation counts once.
- **B. Part 57.** When `part == "57"`, `section 9010` with any chain is the ACA fee provision, not the Code. Emit nothing.
- **C. Truncation.** If `truncated` is true, drop every record whose span end is ≥ `len(text) - 2`. Also drop any record whose chain contains an unclosed `(`. For example, "for purposes of section 8" at the cut yields nothing.
- **D.** An `N U.S.C.` with N ≠ 26, a `CFR` cite, `FR`, `T.D.`, `Stat.`, `Form`, `Article`, `Example`, `Q-n`/`A-n`, and FR image ids are excluded because none of them is a head (§2.3). They also stop a group (§2.4).

---

## 4. Ambiguous forms: rule for each

Use the principle "unresolvable rather than guess". Flags are advisory, and the path is emitted as written unless the rule says `null`.

| form | rule |
|---|---|
| `such section`, `that section`, `said section`, `Such sections`, `those sections`, `that Internal Revenue Code section` | Emit `path:null, kind:"anaphor"` only in the inverted form (§2.5). Otherwise emit nothing. Never resolve. |
| Historical: preceded by `\b(?:former\|old)\s+`; or followed (after the group, inside the qualifier window) by `of prior law`, `as in effect (?:on\|before\|prior)`, `prior to (?:amendment\|repeal)`, `before amendment`, `\(as in effect before the effective date of its repeal\)`; or `had not been repealed` in the same sentence | Emit the path with the flag `historical`. The checker must not score a missing USLM id as an extraction error for these cites. |
| `section N … of this section` (drafting error, e.g. "section 3402 of this section") | Emit it as Code with the flag `self_ref_qualifier`. |
| `l` versus `1` (`3121(1)(8)`, `1221(l)`) | Emit as written. `irregular_chain` fires automatically for a leading digit. The extractor never swaps characters. The checker may try a single `1`↔`l` swap only as a flagged repair (`ocr_repair`). |
| Bare Code number with no keyword ("see 3121(a)(12) and 3121(q)") | Emit nothing. This is an accepted loss of recall. |
| Section ranges | Endpoints plus a `range` record (§2.4d). The checker expands them against USLM. Never expand integers. |
| `and following` | Emit the section with `open_range`. |
| "the flush language of section N(x)" | Emit `N/x` with the flag `flush`. The target text is the flush text after that subdivision. |
| TOC sections (`reg_id` ends in `-0`, or the text contains "lists the captions") | Emit with the flag `toc`, so counts can exclude them. |
| Heading or caption lines | Extract normally; `toc` covers table-of-contents sections. |
| Version-dependent parts (a part-level definition that says "the Code" means the 1954 Code before amendments, e.g. 1.822-4, 20.0-1) | The extractor does nothing. This is resolver policy. |
| Spaced designator glued to a list marker ("section 367(a) (1) The …") | Accepted by §2.2 if it fits the expected level. This is a known residual risk; the checker should flag a path that doesn't resolve. |
| Structural units, "Title 26 of the United States Code", FICA/FUTA/RRTA named as Acts | No path. Optionally emit a separate `kind:"structure"` record. It never counts as a section citation. |

---

## 5. Test snippets (normalized text; expected paths in order)

A ⟨flag⟩ note means that flag must be present on the record.

1. `see section 263A and the regulations thereunder` → `263A`
2. `(4) Section 37(e)(9)(A) (relating to certain public retirement systems)` → `37/e/9/A`
3. `section 103(l)(1)(A) (relating to scholarship bonds)` → `103/l/1/A`
4. `as defined in section 7701 (a)(40) and the regulations thereunder` → `7701/a/40`
5. `a distribution from a section 4947(a) (2) trust` → `4947/a/2` ⟨attributive⟩
6. `by reason of section 1402(b)(1) (G) and (H)` → `1402/b/1/G`, `1402/b/1/H`
7. `the taxes imposed by section 4261(a) and (b) are treated as` → `4261/a`, `4261/b`
8. `tax-free distribution under section 1081(c) (1) or (2)` → `1081/c/1`, `1081/c/2`
9. `sections 2055 and 2106(a)(2) (relating to estate tax deductions` → `2055`, `2106/a/2`
10. `section 2041(b)(2) or 2514(e) of the Code does not apply` → `2041/b/2`, `2514/e`
11. `see sections 861 through 864, Internal Revenue Code of 1954, and the regulations thereunder` → `861`, `864` (range 861→864) ⟨code_1954⟩
12. `described in section 71(a) of prior law the same as divorce or separation instruments described in section 71, as amended by the Tax Reform Act of 1984?` → `71/a` ⟨historical⟩, `71`
13. `For the purpose of section 511 of the Act and the regulations in this part` → none
14. `under subsection (b) of section 553 of title 5 of the United States Code` → none
15. `under 25 U.S.C. 450 (f), (g), and (h)` → none
16. `the average benefits safe harbor of § 414(r)-5(f) for a testing year (see § 414(r)-5(f)(4)` → none
17. `Section § 414(r)-8 may require` → none
18. `subject to withholding under § 31.3402(g)-1(a)(2)` → none
19. `under §§ 1.267A-1 through 1.267A-3 and 1.267A-5` → none
20. `Section 1.822-3 is applicable only to taxable years beginning after December 31, 1953` → none
21. `as amended by section 8 of the Revenue Act of 1962 (76 Stat. 989)` → none
22. `see section 7815(d)(14) of Public Law 101-239.` → none
23. `Section 607(g) of the Act and this section provide rules` → none
24. `described in section 30D(e)(1)(A) of the Internal Revenue Code (Code)` → `30D/e/1/A`
25. `an exemption application for a section 501(c)(9), 501(c)(17), or 501(c)(20) organization under section 505` → `501/c/9`, `501/c/17`, `501/c/20` (all ⟨attributive⟩), `505`
26. `adjustments under section 1016(a) (2) and (3) of the Code for depreciation` → `1016/a/2`, `1016/a/3`
27. `ownership of stock provided by section 958 (a) and (b), and the principles` → `958/a`, `958/b`
28. `an exchange described in section 332, 351, 354, 355, 356, or 361.` → `332`, `351`, `354`, `355`, `356`, `361`
29. `the three elections listed in section 46(f) (1), (2), and (3), see 26 CFR 12.3` → `46/f/1`, `46/f/2`, `46/f/3`
30. `(i) Section 1.475(b)-1(b)(1)(i) (concerning equity interests` → none
31. `withheld as tax under section 3402 of this section` → `3402` ⟨self_ref_qualifier⟩
32. `a foreign subsidiary (as defined in section 3121(1)(8) and the regulations thereunder)` → `3121/1/8` ⟨irregular_chain⟩
33. `registered under section 6 of the Securities Exchange Act of 1934 (15 U.S.C. 78f)` → none
34. `meets the requirements of subsection (b) of section 346 falls within` → `346/b`
35. `the elections described in section 2632(b)(3) and (c)(5) of the Code` → `2632/b/3`, `2632/c/5`
36. `subject to the taxes imposed by section 1, 2, 3, or 11 upon any portion` → `1`, `2`, `3`, `11`
37. `Sections 75(l), 77(e), 199, 337(2), 455, and 659(6) of the Bankruptcy Act (11 U.S.C. 203(l), 205(e), 599, 737(2), 855, and 1059(6))` → none
38. `(Sec. 613, 46 Stat. 756, as amended, sec. 618, 46 Stat. 757, as amended, sec. 7327, 68A Stat. 871; (19 U.S.C. 1613, 1618, 26 U.S.C. 7327))` → `7327` (exactly once)
39. `… for such taxable year for purposes of section 8` (end of text, `truncated=true`) → none
40. `a deduction under section 1382 (b)(2) or (c)(2)(B)` → `1382/b/2`, `1382/c/2/B`
41. `Sections 4911(f) (1) through (3) contain a limited anti-abuse rule` → `4911/f/1`, `4911/f/2` ⟨range_expanded⟩, `4911/f/3`
42. `after application of the exclusions under section 1402(a)(1)-(17)` → `1402/a/1` … `1402/a/17` (17 paths)
43. `Section 56.4911-8 provides rules concerning` → none
44. `Outline of regulation provision for section 7701(b)-1 through (b)-9.` → none
45. `the principles of sections 861-863 and the regulations thereunder` → `861`, `863` (range 861→863)
46. `(For provisions relating to the treatment of tips as wages, see 3121(a)(12) and 3121(q).)` → none
47. `the sum of the rates of tax under subsections (a) and (b) of section 3101` → `3101/a`, `3101/b`
48. `determined in accordance with subparagraph (B) of such section` → `null` (kind anaphor)
49. `(or by reason of section 24(b) of the Internal Revenue Code of 1939)` → none
50. `pursuant to section 1034(a), or section 112(n) of the Internal Revenue Code of 1939` → `1034/a`
51. `any individual described in paragraphs (1) through (10) of section 152(a)` → `152/a/1` … `152/a/10`
52. `paragraphs (4), (6) and (8) of section 6334(a) (relating to property exempt from levy)` → `6334/a/4`, `6334/a/6`, `6334/a/8`
53. `(Sec. 7805 of the Internal Revenue Code of 1954, 68A Stat. 917; 26 U.S.C. 7805)` → `7805` (once) ⟨code_1954⟩
54. `the total to be distributed on February 1, 2005, pursuant to § 408(d)(4) is $475.` → `408/d/4`
55. part 57: `Pursuant to section 9010(g)(4), the information reported` → none
56. `(computed with the application of sections 857(d) and § 1.857-7)` → `857/d`
57. `sections 551-558 (relating to foreign personal holding companies), sections 951-964 (relating to controlled foreign corporations), and section 904 (relating to the limitation on the foreign tax credit) of the Code` → `551`, `558` (range), `951`, `964` (range), `904`
58. `transaction described in section 368 (a) or 355, with respect to which` → `368/a`, `355`
59. `established under section 6621 (b) § 301.6621-1 ("adjusted rate")` → `6621/b`
60. `The higher penalty under the flush language of section 6707(b)(2) will not apply` → `6707/b/2` ⟨flush⟩
61. `Classification of earnings and profits for purposes of section 959 (c)(1) (c)(2) (c)(3) 1963 $100` → `959/c/1`
62. `see section 6012(b)(3) and 28 U.S.C. 960` → `6012/b/3`
63. `to which Congress extends relief under section 302 of the Katrina Emergency Tax Relief Act of 2005.` → none
64. `except in the case of a proceeding under section 77 or chapter X of the Bankruptcy Act` → none
65. `under section 452(b) of title IV of the Social Security Act as amended` → none
66. `as defined in section 3231(e)(1) (for purposes of applying sections 3201(b) and 3221(b) (and so much of section 3211(a) as relates to the rates of the taxes imposed by sections 3101 and 3111))` → `3231/e/1`, `3201/b`, `3221/b`, `3211/a`, `3101`, `3111`
67. `without regard to section 152(b)(1), (b)(2), and (d)(1)(B)` → `152/b/1`, `152/b/2`, `152/d/1/B`
68. `by a trustee of property included in the gross estate under section 2035 through 2038, or section 2041` → `2035`, `2038` (range), `2041`
69. `treated as a single taxpayer under old section 163(j)(6)(C)` → `163/j/6/C` ⟨historical⟩
70. `see paragraph (c) (5) of § 53.4947-1` → none
71. `a depository account as defined in § 1.1471- 5(b)(3)(i)` → none
72. `under section 6104(a)(1) (C) or (D)` → `6104/a/1/C`, `6104/a/1/D`
73. `the deductions provided in part VIII (section 241 and following), subchapter B, chapter 1 of the Code` → `241` ⟨open_range⟩
74. `Under Article VI (2) of the convention … on Form 1120-F` → none