import json

from levadura_salvaje.lenses import dated

LABELS = {"names_ended_period", "silent", "no_rules"}


def test_lens_text_is_json_with_all_labels():
    d = json.loads(dated.LENS_TEXT)
    assert set(d["criteria"]) == LABELS
    assert d["instructions"] == dated.INSTRUCTIONS


def test_label_order_covers_labels_strongest_first():
    assert set(dated.LABEL_ORDER) == LABELS
    assert dated.LABEL_ORDER[0] == "names_ended_period"
    assert dated.LABEL_ORDER[-1] == "no_rules"


def test_model_pinned():
    assert dated.MODEL == "jev-1.13.0"
    assert "latest" not in dated.MODEL
    assert dated.LENS_VERSION == "1"
