# caller-sonnet-1 (Sonnet 5.5), verbatim final message

**1. Answer**

**Where it concentrates.** Overview shows part 1 has the most broken citations in absolute terms: 8,634 of 103,326 occurrences, in 1,243 of 3,765 sections (33%). Part 48 has the highest broken-citation share among the big parts: 248 of 1,405 occurrences (17.7%), in 66 of 176 sections (37.5%). For comparison, part 301 has 501 broken citations in 144 of 627 sections (23%). The largest single target in part 1 is §902 (repealed), with 548 citations in 73 sections (`cell 1`).

Part 48's concentration is much tighter. In `cell 48`, the single repealed Code section §4061 accounts for 99 broken citations in 30 sections. The next largest are §6416 (18, absent-subdivision), §4063 (15, repealed) and §4073 (14, absent-subdivision). Across the whole corpus, `cited-by 4061` gives 107 citations: 99 in part 48, 7 in part 145, 1 in part 301.

I picked part 48, §4061, because it is the cleanest concentration. The citing sections are the §48.4061(a)-1 through (b)-3 family and 48.4061-1.

**What a reader is misled about.** Take §48.4061(a)-1. `unit` reports 47 citations in the section: 34 repealed, 10 resolves, 1 absent-section, 2 absent-subdivision. The text says: "Section 4061(a)(1) imposes a tax on the sale by the manufacturer, producer, or importer of ... Automobile truck and bus chassis and bodies". `cite` on index 0 resolves "4061(a)(1)" to the Code's section range, whose text is: "[§§ 4061 to 4063. Repealed. Pub. L. 98–369, div. A, title VII, § 735(a)(1), July 18, 1984, 98 Stat. 980]".

A reader would therefore be misled about the status of the whole regulation. It presents itself as current rules for a live tax. It states rates of "10" for sales from Jan 1, 1959 to Sept 30, 1979 and "5" for sales on or after Oct 1, 1979. It also refers to "sales made after December 10, 1971". Those dates show it is written against the pre-1984 statute. As printed, it does not say that the statutory authority it applies has been repealed. It never tells the reader to look at the Code's successor provisions.

I would not overstate this. The Code text I could read says only "repealed 1984". I could not confirm what, if anything, replaced the tax, or whether the regulation still has operative force for old periods. Such periods are plausible, because the tax was imposed on sales. So the likely misleading effect is that a reader treats the regulation as the current rule. I did not establish that.

**Limits of what the index can establish.**
- "Broken" is a mechanical address check. The tool's own caution says it is a lead, not a conclusion.
- The §4061 resolution points at a repeal range, "§§4061 to 4063". The index cannot tell me whether a different §4061 existed later.
- Only 2025 is loaded, so I cannot say when the regulation went stale.
- `resolves` can hide section-number reuse. For example, 10 of the 47 citations in §48.4061(a)-1 "resolve", including §4221 and §4216, and I did not check whether they still mean what the regulation assumes.
- One citation (index 16, "4016(a)", absent-section) looks like a typo for 4061(a) in the text: "the tax imposed by section 4016(a) is computed...". That is a regulation defect, not a repeal.

**2. What I needed that the tool didn't give me**
- A way to read the Code provision text by cited section. `follow provision` accepts only a provision UUID, not "4061" or "4061/a". The only route was `cite`, then reading the `resolves_to` UUID.
- A successor or replacement pointer for repealed sections, for example "see §4051". Without it I could not say what a reader should consult instead.
- Any history, such as the date each regulation was last amended. That is what separates "stale but dormant" from "stale and live".
- Severity, meaning whether a broken citation is the operative authority or a passing cross-reference. All 47 citations in a section are listed with equal weight.
- Section-level aggregation in `drill`. It lists sections but not how many broken citations each has, so I had to open sections one by one.
- A grouped, non-paginated view of a section's citations by target. I had to page through them by hand.
- An error that doesn't crash. `follow provision 4061/a` produced a raw stack trace.

**3. What I did**
- `overview`, which gave the per-part counts.
- `--help` on every tool.
- `cell 48`, then `cell 1`, to compare the targets. I chose part 48 because §4061 is the single most concentrated repealed target there.
- `cited-by 4061`, which gave the 107 citations and the split by part.
- `drill 48`, which listed the sections.
- `unit` on §48.4061(a)-1, which gave the 47 citations, then `follow unit` to read its text.
- `cite` on indexes 0 and 16, which gave the resolution and the quoted passages, then `follow provision` on the resolved UUID, which gave the repeal note.
- A failed `follow provision 4061` and `follow provision 4061/a`, which showed the tool does not accept those handles.
- `unit --only-broken --cursor 20` to see the remaining broken citations.
