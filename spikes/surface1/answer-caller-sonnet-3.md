# caller-sonnet-3 (Sonnet 5.5), verbatim final message

**1. Answer**

**Where it concentrates.** I read "no longer exist, as written" as broken citations: repealed, absent-section or absent-subdivision.

- Overview totals: 10,300 broken of 124,993 occurrences, in 1,675 of 6,158 units (27.2%).
- Part 1 holds 8,634 of the broken citations (overview).
- Part 48 has the highest share among large cells: 248 broken of 1,405 occurrences in 66 of 176 units.
- Within part 1, the largest single targets from `cell 1` are:

| Code section | Outcome | Citations | Units |
|---|---|---|---|
| 902 | repealed | 548 | 73 |
| 46 | absent-subdivision | 343 | 30 |
| 167 | absent-subdivision | 284 | 28 |
| 103 | absent-subdivision | 266 | 17 |
| 1201 | repealed | 262 | 63 |

**A false concentration.** Part 54 looks dense: 197 broken in 7 members (`cell 54`). But 182 of those are "section 204" in `54.4980F-1`, flagged absent-section.
- The quoted text reads: "section 4980F(e) of the Internal Revenue Code and section 204(h) of ERISA".
- So it is ERISA §204(h), not a Code section, and the resolver mis-addressed it.
- A measure for "ERISA" within 200 characters of "204" matched only this unit, 1 of the 4 units flagged for 204 (the other 3 are unrelated).
- Four more in part 54 are `54.9816-8T` citing "section 10(a) of title 9, United States Code", which is the Federal Arbitration Act.
- At least 186 of part 54's 197 broken citations are therefore not Code gaps. That shows how much a "broken" count can overstate.

**The concentration I picked: section 902 (indirect foreign tax credit).**
- Every one of the 548 citations of §902 is "repealed" (`cited-by 902`), across 73 units, all in part 1.
- The clustering is in the foreign tax credit and international sections. Examples are `1.902-1` (54 citations), `1.902-2` (18) and `1.901-3` (13).

**What a reader would be misled about.**
- `1.902-1` reads as a live operating rule. Its opening: "For purposes of section 902, this section, and § 1.902-2, the definitions... apply."
- It defines domestic shareholder, first-tier and second-tier corporations, and has worked examples on 1992 dividends.
- A targeted measure for "repeal / Tax Cuts / 115-97 / after December 31, 2017" did not match `1.902-1`. I did not read its paragraph (a)(13) special effective date, so I cannot say it is silent on post-2017 years.
- Other regulations do carry the caveat. `1.367(b)-7(g)` says: "As a result of the repeal of section 902 effective for taxable years of foreign corporations beginning on or after January 1, 2018...". `1.901(m)-1` separates taxable years beginning after December 31, 2017.
- So the repeal is acknowledged inconsistently. Of the 73 units, 9 contain repeal or 2017 language that my first pattern caught. A second pattern for post-2018 applicability language matched only 2.
- A reader of `1.902-1` alone would not learn that the deemed-paid credit it computes is unavailable for taxable years of foreign corporations beginning on or after January 1, 2018.
- The "currency" lens read 62 of the 73 units as current (Jev) and 61 (Qwen). It therefore treats most of these as still operative.
- The misleading effect is plausibly real for the 1.902-x family. For most of the other 73 units, §902 is a side reference and the mislead is small.
- The index cannot say how a practitioner would actually read the section.

**What the index cannot establish.**
- It confirms only that the address no longer exists.
- It does not show what the cited provision said when the regulation was written.
- Only 2025 is loaded, so there is no history.
- The regex counts are not readings.

**2. What I needed that the tool didn't give me**
- A way to tell Code citations from ERISA, PHSA, Title 9 or other statutes. `204` and `10` are mislabelled as Code, and they dominated part 54.
- Per-unit text search that returns the matching span for a named unit. `measure` samples are random, and a unit can be checked only by membership in the matched list.
- Navigation to a named paragraph, such as (a)(13) of `1.902-1`. `follow` takes only character offsets, in a 75,290-character section.
- A statutory-history link, such as "§902 repealed by P.L. 115-97 effective 2018". I had to infer it from the text.
- A ranking of broken citations that discounts false positives.

**3. What I did**
- `overview`, then `--help` on every tool.
- `cell 54` and `lens --cell 54`, because its share was the most concentrated.
- `cited-by 204`, `unit` and `cite` on `54.4980F-1` and `54.9816-8T` to see why. This showed the ERISA and Title 9 mis-resolution.
- A `measure` for "ERISA" near 204 to confirm.
- `cell 1` and `cell 48` to find real concentrations.
- `cited-by 902` and `lens --cited-by 902`, and `follow` on `1.902-1` (start and end).
- Three `measure` regexes for repeal or post-2017 language across the §902 population, then the `lens` historical label.
