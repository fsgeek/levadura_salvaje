# caller-sonnet-2 (Sonnet 5.5), verbatim final message

**1. Answer**

**Where it concentrates.** The overview gives 10,300 broken citations in 124,993 occurrences. Of those, 8,634 are in part 1 (1,243 of its 3,765 sections have at least one broken citation).

Cell 1's top broken targets are:
- 902, repealed: 548 citations in 73 sections
- 46, absent-subdivision: 343 citations in 30 sections
- 167, absent-subdivision: 284 citations in 28 sections
- 103, absent-subdivision: 266 citations in 17 sections
- 1201, repealed: 262 citations in 63 sections

Part 54 looks dense, with 197 broken citations in 7 sections. That count is an artifact. 182 of those citations are to "204", and all sit in one section, 54.4980F-1. The quoted passage (via `cite`) reads "section 204(h) of ERISA". That is ERISA §204(h), 29 U.S.C. 1054(h), not Code §204. The resolver treats it as a Code section that doesn't exist. Cell 54's 197 broken citations are therefore mostly not a Code-reliance problem. The tool counts only the citing text and cannot tell which statute a citation points to.

**The concentration I chose: §902, the deemed-paid foreign tax credit.**
- `cited-by 902` shows all 548 citations are "repealed", in 73 sections, all in part 1. Many of those sections (as the sample listing shows) sit in the foreign tax credit, subpart F and §367 areas (1.901-3, 1.902-1, 1.965-x, 1.367(b)-x).
- 1.902-1 has 59 repealed citations of its own (`unit`). 1.902-2 has 18 and 1.901-3 has 13 (`cited-by` listing).

**What a reader would be misled about.**
- 1.902-1 opens: "(a) Definitions and special effective date. For purposes of section 902, this section, and § 1.902-2…" and gives definitions such as "(1) Domestic shareholder… after December 31, 1986…". Quoted text via `follow`, first 1,500 of 75,290 characters.
- A reader of those first 1,500 characters would see a live credit, with no notice that §902 is gone for the years the text addresses. The statute was repealed for foreign corporations' tax years beginning on or after 1 January 2018.
- The repeal is acknowledged in some sections. 1.367(b)-7(g) says: "As a result of the repeal of section 902 effective for taxable years of foreign corporations beginning on or after January 1, 2018…". 1.901(m)-1 splits its definition at 1 January 2018.
- `measure --cited-by 902 --pattern 'repeal|2018|2017'` matched 21 of 73 sections. 52 had none of those strings, including 1.902-0, 1.901-3 and 1.901-2A.
- So I can say that in many of the 73 sections the text gives no repeal signal near the §902 citation. I cannot say the others mislead. A section may state the effective date in different words, and I read only one section's opening.

The practical misleading is of two kinds:
1. A reader may think a §902 credit is available for post-2017 years.
2. Sections that pair §902 with live provisions (such as the §960 deemed-paid credit) can read as if the two work together today.

**What the index can't establish.** It cannot say whether a given passage is read against the right year. A "repealed" outcome is only a lead (the overview's caution). Only 2025 is loaded, so I can't compare against an earlier edition. The regex counts are mechanical and keyword-based.

**2. What I needed that the tool didn't give me**
- A flag separating Code citations from ERISA, PHSA and other statutes. This is a false-positive class, and it inflated cell 54.
- The Code release date a "repealed" outcome applies from, and the repealing statute (e.g. Pub. L. 115-97). I had to rely on outside knowledge.
- Whether the section itself states a sunset or effective-date note. `measure` only gives a keyword match, and its sample showed 20 sections at a time.
- A way to list every section the regex did not match. The samples were capped, so I couldn't confirm whether 1.902-1 was in either list.
- A per-section view of "repealed citations with a repeal acknowledgment nearby". I built a rough one by hand.
- Paging through a long section. I could only read one 1,500-character slice of 1.902-1's 75,290 characters.

**3. What I did**
- `overview`, then the cell list, then `cell 54` (high density, only 7 sections).
- `drill 54`, `cited-by 204`, and `unit` / `cite` on 54.4980F-1, which showed the ERISA §204(h) false positive. `measure --cell 54 --near 204` confirmed the "of ERISA" phrasing.
- `cell 1`, `cell 9` and `cell 12` to see the broken targets in the larger and denser cells. I picked §902 in cell 1 as the real concentration.
- `cited-by 902` for the 73 sections, then `unit 1.902-1` and `follow unit` to read the opening text.
- `measure --cited-by 902` with several patterns (repeal, 2017, 2018, effective) to estimate how many sections acknowledge the repeal.
