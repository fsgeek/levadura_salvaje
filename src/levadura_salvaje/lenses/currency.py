"""Currency lens: judged from its own text alone, does an excerpt of a 26 CFR
section state rules that apply in 2025 or later, only rules limited to
earlier periods, or no rules at all?

One Jev Choice question per chunk of each fossil-candidate section. Labels:

- ``current``: the excerpt states at least one rule that, on its own terms,
  applies to taxable years, events, returns, or periods in 2025 or later,
  including any rule with no stated time limit;
- ``historical``: every rule the excerpt states is limited, by its own terms,
  to earlier years, events, or periods;
- ``no_rules``: the excerpt states no rules (a table of contents, a reserved
  section, or pure cross-references).

A section's label is the strongest of its chunks' labels
(current > historical > no_rules); that aggregation happens outside this
module. The question tests the text, not the law: a section whose text states
no time limit is ``current`` even if the Code section it implements has been
repealed. Such a section is an unmarked fossil, which is what the lens is
meant to find, so the question tells the model not to bring in outside
knowledge of repeal or expiry.

The question (instructions plus criteria) is the lens; any edit to its
wording is a new lens and must bump LENS_VERSION, because Jev's probabilities
are only comparable across calls that asked the same question of the same
model version.

The model is pinned to a versioned ID rather than the ``jev-latest`` alias:
an alias moves when TypeSafe ships, silently changing the instrument.
"""

import json

from typesafe_sdk import Choice, TypeSafeClient

LENS_VERSION = "1"
MODEL = "jev-1.13.0"
QUESTION_NAME = "currency"
STATE_FIELD = "cfr_excerpt"

INSTRUCTIONS = (
    "The text is one excerpt of a section of the Treasury income tax "
    "regulations (26 CFR). A header line gives the section number and "
    "heading and may say that the excerpt is one part of a longer section. "
    "Judge only the text of this excerpt. Do not guess what the rest of the "
    "section says, and do not use outside knowledge of the law: whether the "
    "underlying statute was repealed, amended, or has expired does not "
    "matter. The question is what the text itself says about when its rules "
    "apply. Answer current if the excerpt states at least one rule that, on "
    "its own terms, applies to taxable years, events, returns, or periods in "
    "2025 or later, and that includes any rule that states no time limit at "
    "all. Answer historical if the excerpt states rules and every one of them "
    "is limited, by its own terms, to years, events, or periods that ended "
    "before 2025. Answer no_rules if the excerpt states no rules at all."
)

CRITERIA = {
    "current": {
        "what": (
            "The excerpt states at least one rule (a requirement, "
            "computation, definition, election, limitation, or treatment) "
            "that, as written, applies to taxable years, events, returns, or "
            "periods in 2025 or later."
        ),
        "no_time_limit": (
            "A rule that states no time limit counts as current, even if its "
            "wording or the statute it cites looks old. Silence about dates "
            "means the rule, on its own terms, still applies."
        ),
        "open_ended_dates": (
            "A rule limited only by a starting date, such as \"taxable years "
            "beginning after December 31, 1986\" or \"property placed in "
            "service after 1980\", has no end date and is current. So is a "
            "rule whose stated period includes 2025, such as \"taxable years "
            "beginning after December 31, 2017, and before January 1, 2026\"."
        ),
        "effective_dates": (
            "An effective-date or applicability paragraph that says when the "
            "section's rules begin to apply, with no end date, does not make "
            "the rules historical. If the excerpt mixes rules with no time "
            "limit and rules limited to past periods, the answer is current."
        ),
        "not_for": (
            "An excerpt in which every rule is expressly limited to periods "
            "that ended before 2025; an excerpt that states no rules."
        ),
    },
    "historical": {
        "what": (
            "The excerpt states rules, and every rule it states is limited by "
            "its own words to taxable years, events, returns, or periods that "
            "ended before 2025, for example \"taxable years beginning before "
            "1987\", \"property placed in service before 1981\", "
            "\"transactions entered into before January 1, 1990\", or a "
            "transition or effective-date rule whose period has run out."
        ),
        "section_wide_limits": (
            "A limit can be stated once for the whole excerpt, for example "
            "\"the rules of this section apply only to taxable years "
            "beginning before January 1, 1984\"; the rules it covers are then "
            "limited even if each one does not repeat the date."
        ),
        "definitions": (
            "A definition takes its time limit from the rules it serves. If "
            "the excerpt shows that a definition is used only by rules that "
            "are limited to past periods, the definition does not make the "
            "excerpt current. If the excerpt does not show such a limit, "
            "treat the definition as a rule with no time limit."
        ),
        "not_for": (
            "An excerpt with any rule that states no time limit, has only a "
            "starting date, or covers any period in 2025 or later; an excerpt "
            "that states no rules."
        ),
    },
    "no_rules": {
        "what": (
            "The excerpt states no rules: it is a table of contents or list "
            "of section headings, a section marked \"[Reserved]\", or only "
            "cross-references that tell the reader where rules can be found "
            "(\"For rules relating to X, see § 1.123-4\")."
        ),
        "not_for": (
            "An excerpt that states any rule, whether current or limited to "
            "past periods. A sentence that makes other rules apply, such as "
            "\"the rules of § 1.123-4 apply for purposes of this section\", "
            "states a rule and is not a pure cross-reference."
        ),
        "note": (
            "A header or section heading by itself is not a rule. Judge the "
            "body of the excerpt."
        ),
    },
}

QUESTION = Choice(instructions=INSTRUCTIONS, criteria=CRITERIA)

# The exact question as sent on the wire, recorded with every result.
LENS_TEXT = json.dumps(QUESTION.model_dump(mode="json"))


def classify(text: str, client: TypeSafeClient | None = None) -> dict:
    """Classify one excerpt's text. Pass a client to reuse its connection."""
    own = client is None
    if own:
        client = TypeSafeClient(timeout=60)
    try:
        r = client.system_one(
            state={STATE_FIELD: text},
            questions={QUESTION_NAME: QUESTION},
            model=MODEL,
        )
    finally:
        if own:
            client.close()
    a = r.choices[QUESTION_NAME]
    return {
        "label": a.choice,
        "probabilities": dict(a.probabilities),
        "confidence": a.confidence,
        "model": r.model,
        "lens_version": LENS_VERSION,
        "lens_text": LENS_TEXT,
        "input_tokens": r.usage.input_tokens,
        "output_tokens": r.usage.output_tokens,
        "request_id": r.request_id,
    }
