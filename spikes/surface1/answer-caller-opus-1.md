# caller-opus-1 (Opus 5.5), verbatim final message

## 1. Answer

**Where it concentrates.** The tool counts 10,300 citations in the 2025 regulations whose Code address is broken ("broken" means repealed, absent-section or absent-subdivision; tool number). Part 1 holds 8,634 of them, in 1,243 sections (tool number). The largest single target in Part 1 is **§ 902** (the deemed-paid foreign tax credit). It has 548 citations across 73 sections, all marked repealed, and all of them in Part 1 (tool numbers). The Code text the tool returns is: "[§ 902. Repealed. Pub. L. 115–97, title I, § 14301(a), Dec. 22, 2017…]" (quoted). The next largest are § 46 (343 citations, absent-subdivision), § 167 (284) and § 103 (266) (tool numbers).

Not every concentration is real. Part 54 shows 182 absent-section citations to "section 204" in a single section, 54.4980F-1 (tool number). The text reads "section 204(h) of ERISA" (quoted), so that is an ERISA section, not a Code section, and the resolver got it wrong.

**The § 902 cluster: who could be misled.** Many of the 73 sections cite § 902 on purpose, for history, and say so. § 1.367(b)-7 has 21 repealed citations (tool number), but its paragraph (g) says: "As a result of the repeal of section 902 effective for taxable years of foreign corporations beginning on or after January 1, 2018, all … corporations … are treated as nonpooling corporations in post-2017 taxable years" (quoted). That reader is not misled. One gap remains: paragraph (g) "applies to taxable years of foreign corporations ending on or after November 2, 2020" (quoted), so the text alone doesn't say how post-2017 years ending before that date are handled.

**§ 1.6038-2 (Form 5471) is the clearer case.** It has 14 repealed citations to § 902 (tool number). Its own applicability rule makes all of them refer to a section that no longer exists: "This section applies to taxable years of foreign corporations beginning on or after October 3, 2018" (quoted). That is after the repeal took effect. The penalty paragraph (k)(2)(iii) still reads: "In the application of sections 902 and 960 … the amount of taxes paid or deemed paid by each foreign corporation … may be reduced by 10 percent" and "In applying subsections (a) and (b) of section 902, and in applying subsection (a) of section 960, the reduction … shall not apply for purposes of determining the amount of accumulated profits in excess of … taxes" (quoted).

The current statute, IRC § 6038(c)(1)(B), says only "in applying section 960 … the amount of taxes paid or deemed paid … shall be reduced by 10 percent" (quoted). Current § 960(a) deems taxes paid "as are properly attributable to such item of income" (quoted). It no longer mentions accumulated profits.

A reader of § 1.6038-2 could be misled in two ways:
- They would think the 10% penalty for not filing Form 5471 still reaches § 902 deemed-paid credits. The statute now runs that branch only through § 960.
- They would think the penalty has an "accumulated profits" carve-out to apply. That calculation has no current-law counterpart, so the sentence does nothing.

The rule itself is still in force through § 960 and § 901, so the practical risk is wasted or confused work, not a wrong penalty amount. That last point is my legal judgment, not something the index establishes.

**Limits of the index.** "Repealed" is only a statement about the address. The index can't tell a deliberate historical or transition citation (as in § 1.367(b)-7) from a stale one (as in § 1.6038-2). I found that difference only by reading the text. It also produces false positives when another statute is cited (ERISA § 204). Only the 2025 edition is loaded, so I couldn't check whether § 1.6038-2(k) was ever revised after 2017, or confirm when § 6038(c) dropped "902".

## 2. What you needed that the tool didn't give you

- A per-section citation count in `cited-by`. I had to call `unit` on each section to rank them.
- A search inside a section's text. `follow` returns at most 20,000 characters per call, so I paged through and filtered the output myself.
- A flag for whether a section mentions the repeal or limits itself to earlier years. That is the key difference, and the index doesn't record it.
- A link from each citation to the paragraph it sits in, and to that paragraph's applicability date.
- Recognition of other statutes, so that "section 204(h) of ERISA" isn't scored as a Code citation.
- Amendment history for the Code (when § 6038(c) dropped § 902) and earlier CFR editions.
- **Highlight bug:** `cite` on § 1.6038-2, citation 37 (and also 39, 44, 46, 48, 49), returns `"cited": "s 9"` instead of "902" while still reporting `status: ok`. The highlighted span is off by two characters and the hash check didn't catch it.

## 3. What I did

- Ran `overview`. Part 1 dominates in volume, and Part 54 looked dense (197 broken citations, 7 sections).
- Ran `cell 1` and `cell 54`. § 902 is the top broken target in Part 1. In Part 54, § 204 has 182 citations in a single section.
- Ran `cited-by 902` to get the 73 sections, all in Part 1.
- Ran `unit` on § 1.367(b)-7, then `cite` on two citations, then `follow` on § 902's provision to read the repeal note. Paged through § 1.367(b)-7 with `follow`/`--offset` and found paragraphs (g) and (h), which handle the repeal.
- Ran `unit` on five more sections (1.6038-2, 1.1248-1, 1.535-2, 1.704-1, 1.902-1), searching their text for "repeal" or "2018". None of them mentioned it.
- Ran `cite` on § 1.6038-2's eight § 902 citations, then `follow` on § 1.6038-2(k) and its applicability paragraph, then `follow` on IRC § 6038(c) and § 960(a) through resolved citations, to compare the regulation with the current statute.
- Ran `cited-by 204` and `cite` on § 54.4980F-1, which confirmed the ERISA false positive.
