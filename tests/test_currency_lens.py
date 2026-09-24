"""The currency lens question serializes without calling the API."""

import json

from levadura_salvaje.lenses import currency


def test_lens_text_is_json_with_all_labels():
    q = json.loads(currency.LENS_TEXT)
    assert q["type"] == "choice"
    assert set(q["criteria"]) == {"current", "historical", "no_rules"}
    assert q["instructions"] == currency.INSTRUCTIONS


def test_model_is_pinned():
    assert currency.MODEL == "jev-1.13.0"
    assert currency.MODEL != "jev-latest"
