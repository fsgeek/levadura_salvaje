# Instructions for a reader

For each item in results/rule-currency-audit-v3-902-packet.jsonl, read its excerpt and answer the question below about the citation marked with ⟦ ⟧.

The text is an excerpt of a section of the Treasury regulations (26 CFR). One citation in it is marked with ⟦ and ⟧. Judge only the rule that the marked citation is part of, not the rest of the excerpt. Judge from the text alone: do not use outside knowledge of whether the cited provision was repealed, amended, or has expired. The question is what the text says about when the rule containing the marked citation applies. Answer untimed if that rule, on its own terms, applies to periods in 2025 or later, including a rule that states no time limit at all or only a starting date. Answer time_limited if that rule is limited to years, events, or periods that ended before 2025, either in its own words or by a limit that the excerpt shows covers it (for example a paragraph or section heading or an applicability sentence). Answer not_a_rule if the marked citation is not part of a rule: a cross-reference, a history or amendment note, a statement of authority, or a heading. The excerpt is made of labelled parts: the section heading; the opening words of each paragraph above the one that contains the marked citation; for a citation in a worked example, the example's heading and the paragraph that introduces it; the paragraph that contains the marked citation; and the section's effective-date or applicability paragraph, if it has one. A limit stated in any of these parts can cover the rule containing the marked citation.

The labels:

untimed:
  what: The rule containing the marked citation applies, as written, to periods in 2025 or later.
  examples: A citation inside a worked example ("Example 1. ... In 1992, Corporation M ...") takes the timing of the rule the example illustrates. The dates in an example's facts are hypothetical and do not limit the rule. If the excerpt shows that the illustrated rule applies only to past periods, the citation is time_limited; otherwise it is untimed.
  carryovers: A rule that carries amounts from a past period (losses, earnings, taxes, pools) into later periods with no end date applies today and is untimed, even if it is labelled a transition rule.
  no_time_limit: A rule that states no time limit counts as untimed, however old its wording looks.
  open_ended_dates: A rule limited only by a starting date ("taxable years beginning after December 31, 1986") has no end and is untimed.
  not_for: A rule the excerpt shows is limited to periods that ended before 2025; a citation that is not part of a rule.

time_limited:
  what: The rule containing the marked citation is limited to periods that ended before 2025, for example "taxable years beginning before January 1, 2018", "distributions before 1987", or a transition rule whose period has run out.
  inherited_limits: A limit stated once for a paragraph or the section (in a heading, or a sentence such as "this paragraph applies only to taxable years beginning before 1987") covers the rules under it, if the excerpt shows that it does.
  as_in_effect: A citation of a provision "as in effect before" a date, inside a rule that applies only to periods before that date, is time_limited. Inside a rule with no end date, the rule is untimed.
  not_for: A rule with no end date or one reaching 2025; a citation that is not part of a rule.

not_a_rule:
  what: The marked citation is not part of a rule: "see section 902 for rules", a bracketed amendment or authority note, a table of contents, or a heading.
  pointers: A sentence that only directs the reader to rules elsewhere ("see § 1.909-6T for rules applicable to ...", "for corresponding rules ..., see ...") is not_a_rule, even if the rules it points to are limited to the past.
  examples: A worked example is not not_a_rule: judge it by the rule it illustrates.
  not_for: A sentence that applies, defines, computes, requires, limits or allows something by reference to the cited provision. Such a sentence states a rule.



Write one JSON line per item to your output file: {"item": "item-NN", "label": "<untimed|time_limited|not_a_rule>", "decisive_text": "<the few words that decided it>"}
