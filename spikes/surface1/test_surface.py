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


# --- review 1: tests through the methods, with a fake database -------------------------

class _Coll:
    def __init__(self, docs=None, log=None):
        self.docs, self.log = docs or {}, log if log is not None else []

    def get(self, key):
        self.log.append(("get", key))
        return self.docs.get(key)

    def insert(self, doc):
        self.log.append(("insert", doc))


class _DB:
    def __init__(self, colls):
        self.colls = colls

    def collection(self, name):
        return self.colls.setdefault(name, _Coll())


def _surface(colls=None):
    s = object.__new__(surface.Surface)
    s.who, s.m, s.um, s._db = "test", "M", "U", _DB(colls or {})
    return s


@pytest.mark.parametrize("bad", ["4061/a", "4061", "../x", ""])
def test_follow_refuses_malformed_provision_ids_before_the_database(bad):
    provisions = _Coll()
    s = _surface({"provisions": provisions})
    with pytest.raises(KeyError, match="not a provision key"):
        s.follow("provision", bad)
    assert provisions.log == []


def test_follow_refuses_a_provision_of_another_usc_generation():
    key = "8d999877-8d77-52ce-afb8-914f7b9ae2d8"
    s = _surface({"provisions": _Coll({key: {"manifest": "OTHER", "locator": {}}})})
    with pytest.raises(KeyError, match="no provision"):
        s.follow("provision", key)


@pytest.mark.parametrize("call", [
    lambda s: s.follow("unit", "u", offset=-2),
    lambda s: s.unit("u", cursor=-1),
    lambda s: s.cited_by("902", cursor=-1),
    lambda s: s.cell("1", cursor=-1),
])
def test_negative_cursors_and_offsets_are_refused(call):
    with pytest.raises(ValueError, match="non-negative"):
        call(_surface())


def test_cite_refuses_when_the_sidecar_and_the_stored_occurrence_disagree(monkeypatch):
    """Review 1 #1: the sidecar said 960 where the index holds 902, and cite combined them."""
    unit = "cfr26-2025:CFR-2025-title26-vol1.xml:5"
    monkeypatch.setattr(surface, "_rows", lambda: {unit: {"citations": [{"path": "960", "head": "section",
                                                                           "span": [0, 3]}]}})
    occ = _Coll({surface.ix.key("M", unit, 0): {"path": "902"}})
    with pytest.raises(LookupError, match="disagree"):
        _surface({"occurrences": occ}).cite(unit, 0)


def test_the_sidecar_is_pinned(monkeypatch, tmp_path):
    other = tmp_path / "citations.jsonl"
    other.write_text('{"volume_file": "v", "ordinal": 1, "citations": []}\n')
    monkeypatch.setattr(surface.cx, "CIT", other)
    surface._rows.cache_clear()
    try:
        with pytest.raises(LookupError, match="not the file the index was built from"):
            surface._rows()
    finally:
        surface._rows.cache_clear()


def test_failed_calls_are_footprints():
    queries = _Coll()
    _surface({"queries": queries}).failed("follow", {"id": "4061/a"}, "KeyError: x")
    (op, doc), = queries.log
    assert op == "insert" and doc["error"] == "KeyError: x" and doc["who"] == "test"


# --- after round 2 -----------------------------------------------------------------------

def test_window_pages_forward_and_from_the_end():
    t = "abcdefghij"
    first = surface.window(t, 0, 4)
    assert first["text"] == "abcd" and first["next_offset"] == 4 and first["truncated"]
    assert surface.window(t, first["next_offset"], 4)["text"] == "efgh"
    last = surface.window(t, 0, 3, from_end=True)
    assert last["text"] == "hij" and last["next_offset"] is None and last["truncated"]
    assert surface.window(t, 3, 3, from_end=True)["text"] == "efg"
    assert not surface.window(t, 0, 99)["truncated"]


def test_anchors_match_at_window_edges():
    import re
    import instrument
    t = "zzzz section 902 qqqq"
    m, at = instrument._first(re.compile(r"^section"), t, [(5, 16)])
    assert m and t[at + m.start():at + m.end()] == "section"
    assert instrument._first(re.compile(r"^qqqq"), t, [(5, 16)]) == (None, 0)
