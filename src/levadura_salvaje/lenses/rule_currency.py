"""Rule-currency lens: is the rule that one citation sits in limited to the past?

The currency lens (currency.py) asks a section-level question: does the section
state *any* rule with no time limit? Three callers of the tool surface found that
this is not the question a reader has about a repealed citation
(docs/surface1-scorecard.md, round 3). Their question is whether the rule *that
depends on the citation* is presented as live. A section with one untimed
definition and forty citations of a repealed provision, all inside transition
rules, is `current` under the section lens and harmless under this one.

One question per citation occurrence. The model sees the section's number and
heading and an excerpt of the section's normalized text (citations.normalize)
around the citation, which is marked ⟦like this⟧. Labels:

- ``untimed``: the marked citation sits in a rule that, on its own terms, applies to
  periods in 2025 or later, including a rule with no stated time limit or only a
  start date;
- ``time_limited``: the marked citation sits in a rule limited, by its own terms or
  by a limit the excerpt shows covers it, to periods that ended before 2025;
- ``not_a_rule``: the marked citation is not part of a rule: a cross-reference, a
  history note, an amendment or authority citation, or a heading.

Version 2 (2026-10-02) adds rules for three cases v1 left open. The blind audit of v1
(obs-0157) found that 18 of 45 sampled citations sat in worked examples, and that each of
three judges applied its own consistent rule to them: untimed, time_limited, not_a_rule.
v2 decides:
- worked examples take the timing of the rule they illustrate (an example's dated facts
  are hypothetical, not a limit);
- carryover and transition rules that apply past amounts in later periods, with no end
  date, are untimed;
- pointers to rules elsewhere ("see § 1.909-6T for rules applicable to ...") are not_a_rule.

Like the currency lens, it tests the text, not the law: the model must not use
outside knowledge that the cited provision was repealed. Any edit to the wording
is a new lens and must bump LENS_VERSION.
"""

import json

LENS_VERSION = "2"
LABELS = ("untimed", "time_limited", "not_a_rule")
BEFORE, AFTER = 1500, 700   # characters of context either side of the citation
OPEN, CLOSE = "⟦", "⟧"

INSTRUCTIONS = (
    "The text is an excerpt of a section of the Treasury regulations (26 CFR). One "
    "citation in it is marked with " + OPEN + " and " + CLOSE + ". Judge only the rule "
    "that the marked citation is part of, not the rest of the excerpt. Judge from the "
    "text alone: do not use outside knowledge of whether the cited provision was "
    "repealed, amended, or has expired. The question is what the text says about when "
    "the rule containing the marked citation applies. Answer untimed if that rule, on "
    "its own terms, applies to periods in 2025 or later, including a rule that states "
    "no time limit at all or only a starting date. Answer time_limited if that rule is "
    "limited to years, events, or periods that ended before 2025, either in its own "
    "words or by a limit that the excerpt shows covers it (for example a paragraph or "
    "section heading or an applicability sentence). Answer not_a_rule if the marked "
    "citation is not part of a rule: a cross-reference, a history or amendment note, a "
    "statement of authority, or a heading."
)

CRITERIA = {
    "untimed": {
        "what": "The rule containing the marked citation applies, as written, to periods in 2025 or later.",
        "examples": "A citation inside a worked example (\"Example 1. ... In 1992, Corporation M ...\") takes "
                    "the timing of the rule the example illustrates. The dates in an example's facts are "
                    "hypothetical and do not limit the rule. If the excerpt shows that the illustrated rule "
                    "applies only to past periods, the citation is time_limited; otherwise it is untimed.",
        "carryovers": "A rule that carries amounts from a past period (losses, earnings, taxes, pools) into "
                      "later periods with no end date applies today and is untimed, even if it is labelled a "
                      "transition rule.",
        "no_time_limit": "A rule that states no time limit counts as untimed, however old its wording looks.",
        "open_ended_dates": "A rule limited only by a starting date (\"taxable years beginning after December "
                            "31, 1986\") has no end and is untimed.",
        "not_for": "A rule the excerpt shows is limited to periods that ended before 2025; a citation that is "
                   "not part of a rule.",
    },
    "time_limited": {
        "what": "The rule containing the marked citation is limited to periods that ended before 2025, for "
                "example \"taxable years beginning before January 1, 2018\", \"distributions before 1987\", or "
                "a transition rule whose period has run out.",
        "inherited_limits": "A limit stated once for a paragraph or the section (in a heading, or a sentence "
                            "such as \"this paragraph applies only to taxable years beginning before 1987\") "
                            "covers the rules under it, if the excerpt shows that it does.",
        "as_in_effect": "A citation of a provision \"as in effect before\" a date, inside a rule that applies "
                        "only to periods before that date, is time_limited. Inside a rule with no end date, "
                        "the rule is untimed.",
        "not_for": "A rule with no end date or one reaching 2025; a citation that is not part of a rule.",
    },
    "not_a_rule": {
        "what": "The marked citation is not part of a rule: \"see section 902 for rules\", a bracketed "
                "amendment or authority note, a table of contents, or a heading.",
        "pointers": "A sentence that only directs the reader to rules elsewhere (\"see § 1.909-6T for rules "
                    "applicable to ...\", \"for corresponding rules ..., see ...\") is not_a_rule, even if the "
                    "rules it points to are limited to the past.",
        "examples": "A worked example is not not_a_rule: judge it by the rule it illustrates.",
        "not_for": "A sentence that applies, defines, computes, requires, limits or allows something by "
                   "reference to the cited provision. Such a sentence states a rule.",
    },
}


def prompt() -> str:
    lines = [INSTRUCTIONS, "", "The labels:"]
    for label, crit in CRITERIA.items():
        lines.append(f"\n{label}:")
        lines += [f"  {k}: {v}" for k, v in crit.items()]
    lines.append('\nReply with JSON only: {"label": "<untimed|time_limited|not_a_rule>"}')
    return "\n".join(lines)


PROMPT = prompt()


def excerpt(norm_text: str, span: tuple[int, int], sectno: str, subject: str) -> str:
    """The section header and up to BEFORE/AFTER characters around the citation, which is marked.
    `span` indexes `norm_text`, which must be citations.normalize(section text)."""
    a, b = span
    lo, hi = max(0, a - BEFORE), min(len(norm_text), b + AFTER)
    head = f"§ {sectno} {subject}".strip()
    cut = (" [excerpt; the section continues before and after]" if lo > 0 and hi < len(norm_text) else
           " [excerpt; the section continues before]" if lo > 0 else
           " [excerpt; the section continues after]" if hi < len(norm_text) else "")
    return (f"{head}{cut}\n\n" + ("… " if lo > 0 else "") + norm_text[lo:a] + OPEN + norm_text[a:b] + CLOSE
            + norm_text[b:hi] + (" …" if hi < len(norm_text) else ""))


LENS_TEXT = json.dumps({"instructions": INSTRUCTIONS, "criteria": CRITERIA, "version": LENS_VERSION},
                       sort_keys=True)
