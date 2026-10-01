"""Tests for the surface's pure parts: the fixes callers' reports led to."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import surface  # noqa: E402

# A flat text with the spacing the CFR's italic markup leaves: normalize closes "( PRS )".
FLAT = "A partnership ( PRS ) holds assets. None of the property is section 751 property."


def _citation():
    # Pinned, not computed with the code under test: "751" is at 66 in the normalized text
    # ("( PRS )" -> "(PRS)" removes two characters) and at 68 in the flat text.
    return {"path": "751", "head": "section", "span": [66, 69]}


def test_span_indexes_normalized_text():
    out = surface.context(FLAT, _citation())
    assert out["cited"] == "751" and out["span_check"] == "ok"


def test_flat_text_slice_would_drift():
    """The bug caller-opus-1 found: slicing the flat text with the span misses the number."""
    a, b = _citation()["span"]
    assert FLAT[a:b] != "751"


def test_a_wrong_span_is_reported_not_passed():
    c = _citation() | {"span": [0, 3]}
    assert surface.context(FLAT, c)["span_check"] == "mismatch"


@pytest.mark.parametrize("bad", ["4061/a", "4061", "../x", ""])
def test_provision_ids_are_validated_before_the_database(bad):
    assert not surface.UUID.fullmatch(bad)
