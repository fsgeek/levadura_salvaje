# caller-opus-2 (Opus 5.5), verbatim final message

1. **Answer**

**Where it concentrates.** The tool labels a citation "broken" when the Code address it points to is repealed, or the section or subsection no longer exists. Part 1 (income tax) holds 8,634 of the 10,300 broken citations in the index, and 1,243 of the 1,675 regulations that contain one (tool numbers). Within part 1, the largest single target is **§902, the indirect ("deemed-paid") foreign tax credit**: 548 citations, all repealed, spread across 73 regulations (tool). Next come §46 (343 citations, subsection missing), §167 (284, subsection missing) and §1201 (262, repealed). The tool's text of §902 reads: "[§ 902. Repealed. Pub. L. 115–97, title I, § 14301(a), Dec. 22, 2017…]" (quoted).

The §902 citations are themselves bunched. Six regulations hold 299 of the 548 (my sum of tool counts): 1.904-7 (96), 1.909-6 (84), 1.902-1 (54), 1.904(f)-12 (23), 1.952-1 (21) and 1.367(b)-7 (21).

**How many flag the repeal.** Measured over the 73 regulations that cite §902 (tool counts; these are regex matches, not readings):
- 7 contain the word "repeal" anywhere. Some of those hits are about other repeals, such as §963 and §904(d)(1)(E).
- 17 mention "2017" or "2018" anywhere. 56 never do.
- 13 have a date or "as in effect" qualifier within 300 characters of a §902 citation.

Some regulations handle it properly. 1.367(b)-7(g) says: "As a result of the repeal of section 902 effective for taxable years of foreign corporations beginning on or after January 1, 2018…" (quoted). 1.904-2 cites "section 902 (as in effect on December 21, 2017)" (quoted).

**What a reader could be misled about.**

(a) *The core regulation, 1.902-1, gives no sign that it has expired.* Its applicability paragraph is open-ended: "This section applies to any distribution made in and after a foreign corporation's first taxable year beginning on or after January 1, 1987…" (quoted, para. (g)). Its amendment history ends at "T.D. 9954, 86 FR 52614, Sept. 22, 2021" (quoted). So Treasury amended it after the repeal and still did not add an end date. The text never mentions 2017 or 2018. A reader who takes 1.902-1 at face value would think a domestic corporation can still claim a deemed-paid credit on a dividend from a 10%-owned foreign corporation. For tax years of foreign corporations beginning in 2018 or later, the statute behind it is gone. 1.902-2 (amended through 2006) and 1.902-3 (amended through 2021) are in the same position.

(b) *Current rules still send the reader into the repealed section.*
- 1.6038-2 says it "applies to taxable years of foreign corporations beginning on or after October 3, 2018" (quoted). Yet it defines its short-period reporting by reference to an accounting period "as described in section 902(c)(5)" (quoted). That definition no longer exists in the current Code, so the reader has to go to a pre-2018 edition to apply a post-2018 rule.
- 1.545-2 (personal holding company adjustments) has no date limit in the passage I read. It still allows a deduction for "the foreign income taxes deemed to be paid for such taxable year under section 902(a) in accordance with §§ 1.902-1 and 1.902-2 or section 960(a)(1)…" (quoted). It does not say that only the §960 half can still apply.

**What a reader would not be misled about.** Much of the concentration is deliberate transition law. 1.909-6 is titled "Pre-2011 foreign tax credit splitting events", 1.905-5 covers years "beginning before January 1, 2018", and 1.904-7 and 1.904(f)-12 are titled "Transition rules" (quoted subjects). A broken citation there is history, not an error.

**What the index cannot establish.** It cannot tell whether practitioners are actually misled; most international practitioners know §902 was repealed. It cannot tell whether a regulation that never mentions the repeal gets its date limit from a cross-reference elsewhere. "Resolves" says nothing about whether a citation's meaning has changed. Only the 2025 edition is loaded, so I cannot show when these citations were written or whether later editions added date limits.

2. **What I needed that the tool didn't give me**
- Matched-sample output capped at 20 even when I asked for more. That kept me from reading every match in context.
- A way to get the end of a regulation, where the applicability paragraph usually sits, without first fetching its length.
- Structural search, such as "the applicability paragraph of each regulation in this population", instead of regexes over the whole text.
- Earlier CFR editions or amendment dates by paragraph, to show whether date limits were ever added.
- Whether other cited sections, such as §960(a)(1), changed meaning even though they still resolve.
- A ranking by citations per regulation, so I didn't have to add up the concentration by hand.

3. **What I did**
- Ran overview, then `cell 1` to rank broken targets; §902 came out on top.
- Ran `cited-by 902` to list the 73 regulations and their citation counts.
- Used `measure` with patterns for "repeal", "2017|2018" and date or "as in effect" qualifiers near 902, to count how many regulations flag the repeal.
- Ran `unit` and `cite` on 1.902-1, then `follow provision` to read the repealed §902 text.
- Read the applicability paragraph and amendment history at the end of 1.902-1, and the endings of 1.902-2 and 1.902-3.
- Ran `cite` on the §902 citations in 1.545-2 and 1.6038-2 to test whether current rules still point into the repealed section.
