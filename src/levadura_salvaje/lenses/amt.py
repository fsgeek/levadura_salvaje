"""AMT lens: does a 26 CFR section state minimum-tax rules, merely mention
the minimum tax, or neither?

One Jev Choice question per section. The question (instructions plus
criteria) is the lens; any edit to its wording is a new lens and must bump
LENS_VERSION, because Jev's probabilities are only comparable across calls
that asked the same question of the same model version.

The model is pinned to a versioned ID rather than the ``jev-latest`` alias:
an alias moves when TypeSafe ships, silently changing the instrument.
"""

import json

from typesafe_sdk import Choice, TypeSafeClient

LENS_VERSION = "1"
MODEL = "jev-1.13.0"
QUESTION_NAME = "amt"
STATE_FIELD = "cfr_section"

INSTRUCTIONS = (
    "How does this section of the Treasury income tax regulations (26 CFR) "
    "relate to the federal minimum tax? Answer operative if the section itself "
    "states minimum tax rules, incidental if it is about something else and "
    "only mentions the minimum tax, and none if it does not concern the "
    "minimum tax. The base erosion and anti-abuse tax (section 59A, BEAT) is "
    "not the minimum tax for this question."
)

CRITERIA = {
    "operative": {
        "what": (
            "The section states rules that determine alternative minimum "
            "taxable income, the tentative minimum tax, AMT adjustments or tax "
            "preference items, the AMT exemption amount, the minimum tax "
            "credit, or the alternative minimum tax foreign tax credit."
        ),
        "regimes": (
            "Any regime of the minimum tax counts: the 1969 add-on minimum tax "
            "on tax preferences, the individual alternative minimum tax, the "
            "corporate alternative minimum tax of 1987 through 2017, or the "
            "2022 corporate alternative minimum tax on adjusted financial "
            "statement income."
        ),
        "not_for": (
            "A section about some other subject that refers to the minimum "
            "tax only in passing."
        ),
    },
    "incidental": {
        "what": (
            "The section is about some other subject but mentions the minimum "
            "tax, for example by saying that a deduction, credit, or item is "
            "also allowed, or is treated differently, for alternative minimum "
            "tax purposes."
        ),
        "not_for": (
            "A section whose own rules determine minimum tax amounts; a "
            "section that never mentions the minimum tax."
        ),
    },
    "none": {
        "what": "The section does not mention the minimum tax.",
        "not_for": (
            "Any section that mentions the alternative minimum tax or the "
            "minimum tax on tax preferences."
        ),
        "note": (
            "A section about the base erosion and anti-abuse tax (BEAT, "
            "section 59A, including its base erosion minimum tax amount) and "
            "nothing else belongs here."
        ),
    },
}

QUESTION = Choice(instructions=INSTRUCTIONS, criteria=CRITERIA)

# The exact question as sent on the wire, recorded with every result.
LENS_TEXT = json.dumps(QUESTION.model_dump(mode="json"))


def classify(text: str, client: TypeSafeClient | None = None) -> dict:
    """Classify one section's text. Pass a client to reuse its connection."""
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
