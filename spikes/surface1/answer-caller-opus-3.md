# caller-opus-3 (Opus 5.5), verbatim final message

The broken citations concentrate in part 1. Within part 1, §902 is the largest single cluster, and §1.902-1 itself is where a reader would be misled: its own text never says the statute it implements was repealed.

**1. Answer**

*Where it concentrates (index numbers).* Part 1 holds 8,634 of the 10,300 broken occurrences and 1,243 of the 1,675 member sections. Within part 1, the target with the most citations is §902, outcome "repealed": 548 citations spread over 73 sections. The next largest are §46 (343 citations, absent-subdivision, 30 sections) and §1201 (262, repealed, 63 sections). The old life-insurance sections form a second family: §§802, 804, 809, 810, 815, 821, 822 and 826 add up to about 900 citations. All 548 §902 citations fall in part 1 (cited-by 902).

*Is the citation really dead? (tool text).* Following the provision gives `[§ 902. Repealed. Pub. L. 115–97, title I, § 14301(a), Dec. 22, 2017, 131 Stat. 2221]`.

*Do the regulations know this? (index numbers).* Only 15 of the 73 citing sections contain "before/prior to January 1, 2018" or "as in effect before/on". Only 21 mention 2017, 2018, "Tax Cuts", 115-97 or "repeal" anywhere. The currency lens, which uses two model judges, calls 59 of the 73 sections current by both judges and only 7 historical by both.

*The one to look at: §1.902-1 (tool text).* It has 54 citations to §902, the second most of any section after §1.904-7's 96, and both judges call it current. My search of its full 75,290 characters found none of the 2017/2018/repeal terms above. Its operative rule is written in the present tense: "If a foreign corporation pays a dividend in any taxable year out of post-1986 undistributed earnings to a shareholder that is a domestic shareholder … the recipient shall be deemed to have paid the same proportion of any post-1986 foreign income taxes…" Its applicability paragraph has no end date: "(g) Effective/applicability dates. This section applies to any distribution made in and after a foreign corporation's first taxable year beginning on or after January 1, 1987…" The amendment history in the text runs to "T.D. 9954, 86 FR 52614, Sept. 22, 2021". So Treasury amended the section after the repeal and still left no sunset in the text.

*What a reader would be misled about.* Read alone, §1.902-1 tells a domestic corporation that owns 10% of a foreign corporation that a dividend received in 2025 brings a deemed-paid foreign tax credit, computed from post-1986 pools. The statute behind that credit no longer exists. The regulation's own words don't reveal that; only the Code note does. The same thing shows up in passing elsewhere. §1.6038-3 still reduces "the amount of taxes paid (and deemed paid under sections 902 and 960)" as a penalty, which today only has teeth through §960. §1.1503(d)-7 gives a worked example that "computes foreign taxes deemed paid on the dividend under section 902". Overall, 31 of the 73 sections use "deemed paid" within 150 characters of a §902 citation.

*The limits.* That the reader is misled is my reading of the text. The tool only shows that the citation's address is repealed and that the section's text has no end date. Other parts of the 2025 CFR do handle the change. §1.904-7, §1.904(f)-12 and §1.905-5 scope themselves to years before 2018, and §1.905-5's heading says so. A practitioner reading across sections might therefore get it right. I can't tell from the index whether the 2017 repeal applies by tax year in a way that leaves §1.902-1 legitimately alive for earlier years still open. That is likely, and if so the regulation is unlabeled rather than wrong. The lens is a model judgment, with 96.6% agreement between the two judges. Only 2025 is loaded, so I can't see whether the text was ever revised.

**2. What I needed that the tool didn't give me**
- The Code's effective-date and transition provisions for the repealing act (Pub. L. 115-97 §14301). The tool shows only "Repealed", not when or for which years.
- Any full-text search within one section. I had to page through `follow` in 20,000-character pieces (the most it returns per call) and search the pieces myself. `measure` returns only one sampled snippet per section.
- A way to tell whether a "current" lens judgment rests on the cited dead provision or on some other rule in the same section.
- Earlier CFR years, to see whether §1.902-1 was ever given a sunset.
- More than one lens: only `currency` exists.

**3. What I did**
- `overview`, which showed part 1 dominates.
- `cell 1 --top 30`, which showed §902 as the top broken target.
- `cited-by 902` to list the 73 citing sections.
- `lens --cited-by 902` to see current vs. historical, which pointed me to §1.902-1 judged current.
- `unit` and `cite` on §1.902-1 to confirm the §902 citations.
- `follow provision` to read the Code's repeal note.
- `measure` for pre-2018 language and for 2017/2018/repeal mentions; §1.902-1 matched neither.
- `follow unit` on §1.902-1 page by page to read paragraphs (b) and (g) and the amendment history.
- `measure "deemed paid" --near 902` to see how widely the old credit language persists.
