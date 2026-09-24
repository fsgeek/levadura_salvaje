"""Dated-period lens: does an excerpt of a 26 CFR section limit any of its
rules to a period, date range or class of events that ended before 2025?

One Jev Choice question per chunk. Each call sees one excerpt of a section,
preceded by a header naming the section and the part; the question is judged
from that excerpt alone. A section's label is the strongest of its chunks'
labels: names_ended_period > silent > no_rules. That roll-up happens outside
this module.

The question (instructions plus criteria) is the lens; any edit to its
wording is a new lens and must bump LENS_VERSION, because Jev's
probabilities are only comparable across calls that asked the same question
of the same model version.

The model is pinned to a versioned ID rather than the ``jev-latest`` alias:
an alias moves when TypeSafe ships, silently changing the instrument.
"""

import json

from typesafe_sdk import Choice, TypeSafeClient

LENS_VERSION = "1"
MODEL = "jev-1.13.0"
QUESTION_NAME = "dated"
STATE_FIELD = "cfr_excerpt"

# Strongest first: a section takes the strongest label any of its chunks got.
LABEL_ORDER = ("names_ended_period", "silent", "no_rules")

INSTRUCTIONS = (
    "The text is one excerpt of a section of the Treasury income tax "
    "regulations (26 CFR). A header line names the section and says which "
    "part of the section the excerpt is; judge only the excerpt shown, and "
    "do not guess what the rest of the section says. Does the excerpt limit "
    "any of its rules to a period, date range or class of events that ended "
    "before January 1, 2025? Answer names_ended_period if at least one rule "
    "is so limited, silent if the excerpt states rules but limits none of "
    "them to an ended period, and no_rules if the excerpt states no rules at "
    "all. A period has ended before 2025 only if its last day is on or "
    "before December 31, 2024: a period that includes any part of 2025 or "
    "later has not ended, and a start date alone never makes an ended "
    "period. Dates that only say when a regulation, Treasury decision, "
    "notice or statute was published, issued or amended do not limit a rule."
)

CRITERIA = {
    "names_ended_period": {
        "what": (
            "At least one rule in the excerpt applies only to a period, date "
            "range or class of events whose end came before 2025. Examples: "
            "'taxable years beginning before January 1, 1987'; 'property "
            "placed in service before 1981'; 'for 1975 and 1976'; 'amounts "
            "paid before the enactment of the Tax Reform Act of 1986'; "
            "'taxable years beginning after December 31, 1986, and before "
            "January 1, 1989'; 'for taxable years beginning in 1988, the "
            "amount is $40,000'; 'does not apply to taxable years beginning "
            "after December 31, 2012'; 'contracts entered into on or before "
            "March 1, 1986'; 'an election must be filed by March 15, 1988'."
        ),
        "also_counts": (
            "A rule tied to a period before the enactment or effective date "
            "of a named Act enacted before 2025 (every Act these regulations "
            "name, such as the Tax Reform Act of 1986 or the Tax Cuts and "
            "Jobs Act, qualifies). A rule that applies to items, years or "
            "property governed by a Code section or regulation 'as in effect "
            "before' a date before 2025, or by 'prior law' that the excerpt "
            "identifies as superseded before 2025. A rule for 'earlier' or "
            "'prior' years set against a start date before 2025 (for example "
            "'15 percent for taxable years beginning before 1987'). A "
            "sentence directing the reader to other rules for an ended "
            "period, such as 'for taxable years beginning before January 1, "
            "1990, see section 1.57-1 as contained in 26 CFR part 1 revised "
            "April 1, 1989'. A section heading in the header line that "
            "limits the section to an ended period, if the excerpt states "
            "rules."
        ),
        "not_for": (
            "A start date alone, such as 'taxable years beginning after "
            "December 31, 1986' or 'applies to transfers on or after June "
            "1, 1990'. A range that runs into or past 2025, such as "
            "'taxable years beginning after December 31, 2017, and before "
            "January 1, 2026' or 'taxable years beginning before January 1, "
            "2026'. Publication, issuance or amendment dates, such as source "
            "notes ('T.D. 8123, 52 FR 1234, Jan. 1, 1987, as amended by "
            "...'), Federal Register citations, revenue procedure or ruling "
            "citations, and the 'revised as of' date of a CFR edition. Years "
            "that appear only as facts in an example, when no rule is "
            "limited to them."
        ),
    },
    "silent": {
        "what": (
            "The excerpt states rules (definitions, requirements, "
            "computations, elections, effective-date provisions, or "
            "examples applying them) but none of them is limited to a "
            "period, date range or class of events that ended before 2025. "
            "It may give start dates only, ranges that include 2025 or "
            "later, dates of publication or amendment, or no dates at all."
        ),
        "not_for": (
            "An excerpt in which any rule is limited to a period that ended "
            "before 2025; an excerpt that states no rules."
        ),
    },
    "no_rules": {
        "what": (
            "The excerpt states no rules: a table of contents or list of "
            "headings, a section marked [Reserved], a bare source or "
            "authority note, or text that only points to other provisions "
            "(for example 'For rules relating to X, see section 1.y') "
            "without stating any rule itself."
        ),
        "not_for": (
            "An excerpt that states any rule, including a definition or an "
            "effective-date provision; a cross-reference limited to a period "
            "that ended before 2025 belongs under names_ended_period."
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
