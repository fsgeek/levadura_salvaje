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

Version 3 (2026-10-03) keeps v2's question and labels and changes what the judge sees
(docs/rule-currency-v3-design.md). Codex's review of v2 found that a fixed window can miss
the limit that governs a citation, such as an example heading 4,251 characters back. So v3
builds the excerpt from the section's paragraph structure (structure.py): the opening of
each ancestor paragraph, the example and what introduces it, the citation's own
paragraph, and the applicability paragraph. Where the structure can't be placed, it falls
back to v2's window and says so.

Version 4 (2026-10-03) adds a label. Two blind audits found the readers agreeing on 0 of 10 items
in 1.909-6, against about 90% elsewhere, with the direction flipping between audits
(docs/rule-currency-scorecard.md, v3). Every such item is a rule whose *inputs* are closed (pre-2011
split taxes, pre-2018 years) while its *application* is open-ended. v2's carryover clause called
these `untimed`, and judges split on following it. A second instance's read (relayed by Tony,
2026-10-03): the categories have a hole. Such a rule never expires on paper; it runs out of things
to apply to. v4 names that as `closed_inputs` and drops the carryover clause from `untimed`. If
the disagreement collapses, it was the instructions; if it persists, it is in the text.

Like the currency lens, it tests the text, not the law: the model must not use
outside knowledge that the cited provision was repealed. Any edit to the wording
is a new lens and must bump LENS_VERSION.
"""

import json

LENS_VERSION = "4"
LABELS = ("untimed", "closed_inputs", "time_limited", "not_a_rule")
BEFORE, AFTER = 1500, 700   # characters of context either side of the citation
OPEN, CLOSE = "⟦", "⟧"

INSTRUCTIONS = (
    "The text is an excerpt of a section of the Treasury regulations (26 CFR). One "
    "citation in it is marked with " + OPEN + " and " + CLOSE + ". Judge only the rule "
    "that the marked citation is part of, not the rest of the excerpt. Judge from the "
    "text alone: do not use outside knowledge of whether the cited provision was "
    "repealed, amended, or has expired. The question is what the text says about when "
    "the rule containing the marked citation applies, and to what. Answer untimed if that rule, on "
    "its own terms, applies to periods in 2025 or later, including a rule that states "
    "no time limit at all or only a starting date, and is not confined to things from past periods. "
    "Answer closed_inputs if the rule itself has no end date but applies only to amounts, items, "
    "or events from periods that ended before 2025 (for example taxes paid in pre-2011 years, "
    "pre-1987 accumulated profits, losses from taxable years beginning before 2005): it does not "
    "expire on paper, but it has a closed set of things to apply to. Answer time_limited if that rule is "
    "limited to years, events, or periods that ended before 2025, either in its own "
    "words or by a limit that the excerpt shows covers it (for example a paragraph or "
    "section heading or an applicability sentence). Answer not_a_rule if the marked "
    "citation is not part of a rule: a cross-reference, a history or amendment note, a "
    "statement of authority, or a heading. The excerpt is made of labelled parts: the section heading; "
    "the opening words of each paragraph above the one that contains the marked citation; for a citation "
    "in a worked example, the example's heading and the paragraph that introduces it; the paragraph "
    "that contains the marked citation; and the section's effective-date or applicability paragraph, if "
    "it has one. A limit stated in any of these parts can cover the rule containing the marked citation."
)

CRITERIA = {
    "untimed": {
        "what": "The rule containing the marked citation applies, as written, to periods in 2025 or later.",
        "examples": "A citation inside a worked example (\"Example 1. ... In 1992, Corporation M ...\") takes "
                    "the timing of the rule the example illustrates. The dates in an example's facts are "
                    "hypothetical and do not limit the rule. If the excerpt shows that the illustrated rule "
                    "applies only to past periods, the citation is time_limited; otherwise it is untimed.",
        "open_inputs": "A rule is untimed only if what it applies to is open too: future or ongoing "
                       "amounts, items or events. A rule confined to amounts from past periods is closed_inputs.",
        "no_time_limit": "A rule that states no time limit counts as untimed, however old its wording looks.",
        "open_ended_dates": "A rule limited only by a starting date (\"taxable years beginning after December "
                            "31, 1986\") has no end and is untimed.",
        "not_for": "A rule the excerpt shows is limited to periods that ended before 2025; a citation that is "
                   "not part of a rule.",
    },
    "closed_inputs": {
        "what": "The rule containing the marked citation has no end date of its own, but it applies only to "
                "amounts, items, or events from periods that ended before 2025: \"pre-2011 split taxes\", "
                "\"pre-1987 accumulated profits\", \"losses from taxable years beginning before January 1, "
                "2005\". It still applies in later years, to that closed set.",
        "carryovers": "A carryover, recapture, or transition rule that brings past-period amounts into later "
                      "years with no end date is closed_inputs.",
        "not_for": "A rule whose own application ends before 2025 (time_limited); a rule that applies to "
                   "current or future amounts (untimed).",
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
    lines.append('\nReply with JSON only: {"label": "<' + "|".join(LABELS) + '>"}')
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


# --- v3: excerpts from structure ---------------------------------------------------------------

OPENING = 300        # characters of each ancestor or introducing paragraph
OWN = 2400           # characters of the citation's own paragraph, centred on the citation if longer
APPLIES = 900        # characters of the applicability paragraph
CITED = 600          # v4: characters of each paragraph of the section a worked example cites
CITED_TOTAL = 1800   # v4: at most this much of them in all
BUDGET = 5200


def _mark(norm: str, a: int, b: int, lo: int, hi: int) -> str:
    return norm[lo:a] + OPEN + norm[a:b] + CLOSE + norm[b:hi]


def _opening(p) -> str:
    return p.text if len(p.text) <= OPENING else p.text[:OPENING].rstrip() + " …"


def excerpt_v3(norm: str, paras: list, span: tuple[int, int], sectno: str, subject: str) -> tuple[str, str]:
    """(excerpt, mode). mode: "structure", "structure_attached" (the citation is in a table or extract,
    attached to the paragraph before it), or "window" (v2's window, when the structure can't be placed)."""
    from levadura_salvaje import structure as st
    a, b = span
    head = f"§ {sectno} {subject}".strip()
    p, exact = st.enclosing(paras, a)
    if p is None or p.ancestry is None:
        why = "no paragraph contains it" if p is None else "its paragraph numbering could not be placed"
        return (f"{head}\n\n[The section's structure is unavailable for this citation ({why}); "
                f"a window of text around it follows.]\n\n" + excerpt(norm, span, "", "").split("\n\n", 1)[1],
                "window")
    by = {q.index: q for q in paras}
    parts = [head]
    above = [by[i] for i in p.ancestry]
    if p.scope != "main":
        first = min(q.index for q in paras if q.scope == p.scope)
        intro = next((q for q in reversed(paras[:first]) if q.scope == "main"), None)
        if intro is not None and intro.ancestry is not None:
            parts.append("[Paragraphs above the worked example, opening words only:]\n"
                         + "\n".join(_opening(by[i]) for i in intro.ancestry + [intro.index]))
        parts.append(f"[The marked citation is inside a worked example: {p.example_heading or 'Example'}]")
    if above:
        parts.append("[Paragraphs above the one containing the marked citation, opening words only:]\n"
                     + "\n".join(_opening(q) for q in above))
    lo, hi = p.start, p.end
    if not exact:                       # a table or extract after p: show p's opening, then the cited cell
        parts.append("[The paragraph before the table or extract that contains the marked citation:]\n" + _opening(p))
        lo, hi = max(0, a - 600), min(len(norm), b + 300)
        parts.append("[The table or extract text around the marked citation:]\n… "
                     + _mark(norm, a, b, lo, hi) + " …")
    else:
        if hi - lo > OWN:
            lo, hi = max(lo, a - OWN * 2 // 3), min(hi, b + OWN // 3)
        cut_l, cut_r = ("… " if lo > p.start else ""), (" …" if hi < p.end else "")
        parts.append("[The paragraph containing the marked citation:]\n" + cut_l + _mark(norm, a, b, lo, hi) + cut_r)
    if p.scope != "main" and int(LENS_VERSION) >= 4:
        # what the example illustrates: the paragraphs of this section it cites by number (review 2, P1 #1).
        # After the citation's own paragraph, so a truncated excerpt loses these before the citation.
        shown = set(p.ancestry) | {p.index}
        if intro is not None and intro.ancestry is not None:
            shown |= set(intro.ancestry) | {intro.index}
        cited, lost, room = [], [], CITED_TOTAL
        for path in st.section_refs(" ".join(q.text for q in paras if q.scope == p.scope)):
            q = st.addressed(paras, path)
            if q is None:
                lost.append("paragraph " + "".join(f"({t})" for t in path))
            if q is None or q.index in shown or room <= 0:
                continue
            t = q.text if len(q.text) <= min(CITED, room) else q.text[:min(CITED, room)].rstrip() + " …"
            cited.append(t); shown.add(q.index); room -= len(t)
        if cited:
            parts.append("[Paragraphs of this section that the worked example cites, opening words:]\n"
                         + "\n".join(cited))
        if lost:
            parts.append(f"[The worked example also cites {', '.join(lost)} of this section, which could "
                         f"not be located in the section's structure; it is not shown.]")
    if int(LENS_VERSION) >= 4:
        # the date provision that covers this citation, labelled with what it governs (review 2, P1 #5)
        got = st.governing_date(paras, p)
        ap, sc = got if got is not None else (None, None)
        label = ("[The section's effective-date or applicability paragraph:]" if sc == () else
                 "[The effective-date paragraph governing paragraph "
                 + "".join(f"({t})" for t in (sc or ())) + " of this section:]")
    else:
        ap, label = st.applicability(paras), "[The section's effective-date or applicability paragraph:]"
    if ap is not None and ap.index != p.index and ap.index not in p.ancestry:
        t = ap.text if len(ap.text) <= APPLIES else ap.text[:APPLIES].rstrip() + " …"
        parts.append(label + "\n" + t)
    out = "\n\n".join(parts)
    if len(out) > BUDGET:               # drop the outermost ancestors first, and say so
        out = out[:BUDGET].rstrip() + " … [excerpt truncated]"
    return out, ("structure" if exact else "structure_attached")

