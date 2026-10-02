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
    assert not surface.window(t, 0, 99)["truncated"]


def _walk(t, length, from_end):
    out, off = [], 0
    while off is not None:
        w = surface.window(t, off, length, from_end)
        out.append(w["text"])
        off = w["next_offset"]
    return out


@pytest.mark.parametrize("length", [1, 3, 4, 10, 11])
def test_continuations_cover_the_text_exactly_once(length):
    """Review 2 #4: reverse pages overlapped at the start and continued with forward coordinates."""
    t = "abcdefghij"
    assert "".join(_walk(t, length, False)) == t
    assert "".join(reversed(_walk(t, length, True))) == t


def test_window_edges():
    t = "abcdefghij"
    assert surface.window(t, 8, 4, from_end=True)["text"] == "ab"          # review 2 #4
    assert surface.window(t, 10, 4, from_end=True)["text"] == ""
    past = surface.window(t, 12, 3)                                         # review 2 #5
    assert past["text"] == "" and past["returned"] == 0


def test_anchors_match_at_window_edges():
    import re
    import instrument
    t = "zzzz section 902 qqqq"
    m, at = instrument._first(re.compile(r"^section"), t, [(5, 16)])
    assert m and t[at + m.start():at + m.end()] == "section"
    assert instrument._first(re.compile(r"^qqqq"), t, [(5, 16)]) == (None, 0)



# --- measure, through its own code, with a fake surface ------------------------------

class _FakeSurface:
    m = "M"

    def __init__(self, locators):
        self.locators, self.logged = locators, []

    def _q(self, aql, **bind):
        return [[u, self.locators.get(u)] for u in bind["us"] if u in self.locators]

    def _log(self, tool, args, result):
        self.logged.append((tool, args))
        return result


def _corpus(monkeypatch, texts):
    """texts: unit -> (flat text, citations). The sidecar row's hash is the text's hash."""
    import hashlib
    import instrument
    rows, flat = {}, {}
    for i, (u, (t, cits)) in enumerate(texts.items()):
        rows[u] = {"volume_file": "v", "ordinal": i, "sha256": hashlib.sha256(t.encode()).hexdigest(),
                   "citations": cits}
        flat[("v", i)] = t
    monkeypatch.setattr(instrument.sf, "_rows", lambda: rows)
    monkeypatch.setattr(instrument.sf, "_describe", lambda u: {"unit": u})
    monkeypatch.setattr(instrument.cx, "_hold", lambda p: "sha")
    monkeypatch.setattr(instrument.cx, "_cfr_texts", lambda sha: flat)
    monkeypatch.setattr(instrument, "_population", lambda s, pop: list(texts))
    return {u: r["sha256"] for u, r in rows.items()}


def test_measure_counts_both_sides_anchors_and_stale(monkeypatch):
    import instrument
    texts = {
        "a": ("section 902 was repealed in 2017.", [{"path": "902", "span": [8, 11]}]),
        "b": ("section 902 applies.", [{"path": "902", "span": [8, 11]}]),
        "c": ("nothing cited here, repealed.", []),
        "d": ("section 902 repealed, but this text changed.", [{"path": "902", "span": [8, 11]}]),
    }
    locs = _corpus(monkeypatch, texts)
    locs["d"] = "0" * 64                     # the manifest's locator disagrees: stale, not counted
    s = _FakeSurface(locs)
    out = instrument.measure(s, {"cited_by": "902"}, "repeal", near="902", window=30)
    assert (out["matched"], out["not_matched"], out["no_anchor"], out["stale"]) == (1, 1, 1, 1)
    assert out["matched_units"] == ["a"] and out["not_matched_units"] == ["b"]
    assert out["no_anchor_units"] == ["c"] and out["stale_units"] == ["d"]
    tool, args = s.logged[-1]
    assert tool == "measure" and args["sampled"]["matched"] == ["a"] and args["seed"] == 0


def test_measure_snippets_are_bounded(monkeypatch):
    """Review 2 #6: '.*' returned a whole regulation per sample."""
    import instrument
    long = "x" * 30000
    s = _FakeSurface(_corpus(monkeypatch, {"a": (long, [])}))
    out = instrument.measure(s, {"cited_by": "902"}, ".*")
    assert len(out["matched_sample"][0]["words"]) <= 240 + 2 * instrument.SNIPPET


def test_measure_lists_page_and_returned_counts_what_is_shown(monkeypatch):
    """Review 2 #7: returned undercounted units shown only in samples; lists stopped at 200."""
    import instrument
    texts = {f"u{i:03d}": ("hit", []) for i in range(250)}
    s = _FakeSurface(_corpus(monkeypatch, texts))
    first = instrument.measure(s, {"cited_by": "902"}, "hit", sample=5)
    assert len(first["matched_units"]) == 200 and first["list_next"] == 200 and first["truncated"]
    shown = set(first["matched_units"]) | {x["unit"] for x in first["matched_sample"]}
    assert first["returned"] == len(shown)
    rest = instrument.measure(s, {"cited_by": "902"}, "hit", sample=0, list_cursor=200)
    assert len(rest["matched_units"]) == 50 and rest["list_next"] is None
    assert set(first["matched_units"]) | set(rest["matched_units"]) == set(texts)


@pytest.mark.parametrize("args", [("902", "1", False), (None, None, False), ("", None, False), ("902", None, True)])
def test_population_selector_refuses_ambiguity(args):
    import instrument
    with pytest.raises(ValueError):
        instrument.population_arg(*args)


def test_measure_refuses_a_sidecar_row_from_another_text(monkeypatch):
    """The text matches the locator but the sidecar row (spans) was made from other text."""
    import instrument
    locs = _corpus(monkeypatch, {"a": ("section 902 repealed", [{"path": "902", "span": [8, 11]}])})
    instrument.sf._rows()["a"]["sha256"] = "f" * 64
    out = instrument.measure(_FakeSurface(locs), {"cited_by": "902"}, "repeal")
    assert out["stale_units"] == ["a"] and out["matched"] == 0


# --- lens: stored readings as predicates -------------------------------------------------

def _lens_reads(monkeypatch, judges):
    import instrument
    monkeypatch.setitem(instrument._READINGS, "currency",
                        {"judges": judges, "files": {j: (f"{j}.jsonl", "h") for j in judges}})
    monkeypatch.setattr(instrument.sf, "_describe", lambda u: {"unit": u})


def test_lens_counts_agreement_not_read_stale_and_partial(monkeypatch):
    import instrument
    _lens_reads(monkeypatch, {
        "jev": {"a": {"label": "current", "sha256": "A"}, "b": {"label": "historical", "sha256": "B"},
                "d": {"label": "current", "sha256": "OLD"}, "e": {"label": "current", "sha256": "E"}},
        "qwen": {"a": {"label": "current", "sha256": "A"}, "b": {"label": "current", "sha256": "B"},
                 "d": {"label": "current", "sha256": "OLD"}}})
    monkeypatch.setattr(instrument, "_population", lambda s, pop: ["a", "b", "c", "d", "e"])
    s = _FakeSurface({"a": "A", "b": "B", "c": "C", "d": "D", "e": "E"})
    out = instrument.lens(s, {"cited_by": "902"})
    assert (out["read"], out["not_read"], out["stale"], out["partial"]) == (2, 1, 1, 1)
    assert out["counts"] == {"jev": {"current": 1, "historical": 1}, "qwen": {"current": 2}}
    assert out["judges_agree"] == 1
    assert out["not_read_units"] == ["c"] and out["stale_units"] == ["d"] and out["partial_units"] == ["e"]
    assert out["returned"] == 5                     # review 3 #4: every id shown counts
    tool, args = s.logged[-1]
    assert tool == "lens" and args["combinations"] == out["combinations"] and "files" in args


def test_lens_unit_missing_from_the_manifest_is_stale(monkeypatch):
    import instrument
    _lens_reads(monkeypatch, {"jev": {"a": {"label": "current", "sha256": "A"}}})
    monkeypatch.setattr(instrument, "_population", lambda s, pop: ["a"])
    out = instrument.lens(_FakeSurface({}), {"cited_by": "902"})
    assert out["stale_units"] == ["a"] and out["read"] == 0


def test_lens_pages_every_list_including_stale(monkeypatch):
    """Review 3 #3: stale ids were always the first 200 and never reported truncated."""
    import instrument
    us = [f"u{i:03d}" for i in range(250)]
    _lens_reads(monkeypatch, {"jev": {u: {"label": "current", "sha256": "OLD"} for u in us}})
    monkeypatch.setattr(instrument, "_population", lambda s, pop: us)
    s = _FakeSurface({u: "NEW" for u in us})
    first = instrument.lens(s, {"cited_by": "902"})
    assert len(first["stale_units"]) == 200 and first["truncated"] and first["list_next"] == 200
    rest = instrument.lens(s, {"cited_by": "902"}, list_cursor=200)
    assert rest["stale_units"] == us[200:] and rest["list_next"] is None


def test_lens_label_filter_keeps_counts_and_samples(monkeypatch):
    """Several units per combination and a sample smaller than each, so a shared generator would
    give the kept combination a different sample once the others are filtered out."""
    import instrument
    cur = {f"c{i}": {"label": "current", "sha256": f"c{i}"} for i in range(30)}
    hist_j = {f"h{i}": {"label": "historical", "sha256": f"h{i}"} for i in range(30)}
    hist_q = {f"h{i}": {"label": "current", "sha256": f"h{i}"} for i in range(30)}
    _lens_reads(monkeypatch, {"jev": cur | hist_j, "qwen": cur | hist_q})
    units = sorted(cur) + sorted(hist_j)
    monkeypatch.setattr(instrument, "_population", lambda s, pop: units)
    s = _FakeSurface({u: u for u in units})
    whole = instrument.lens(s, {"cited_by": "902"}, sample=3)
    hist = instrument.lens(s, {"cited_by": "902"}, label="historical", sample=3)
    k = "jev=historical,qwen=current"
    assert list(hist["combinations"]) == [k]
    assert hist["counts"] == whole["counts"] and hist["judges_agree"] == whole["judges_agree"]
    assert hist["samples"][k] == whole["samples"][k]


def test_readings_refuse_a_file_the_ledger_did_not_record(monkeypatch, tmp_path):
    """Review 3 #1: a label changed while the text hash stayed was silently accepted."""
    import json
    import instrument
    f = tmp_path / "jev.jsonl"
    row = {"volume_file": "v", "ordinal": 1, "label": "current", "sha256": "A"}
    f.write_text(json.dumps(row) + "\n")
    import hashlib
    good = hashlib.sha256(f.read_bytes()).hexdigest()
    monkeypatch.setattr(instrument.cx, "ROOT", tmp_path)
    monkeypatch.setattr(instrument, "_ledger_entry",
                        lambda obs: {"population": {"results_file": "jev.jsonl", "results_sha256": good}})
    monkeypatch.setitem(instrument.LENSES, "t", {**instrument.LENSES["currency"], "judges": {"jev": "obs-x"}})
    assert instrument._readings("t")["judges"]["jev"]["cfr26-2025:v:1"]["label"] == "current"
    instrument._READINGS.pop("t")
    f.write_text(json.dumps(row | {"label": "historical"}) + "\n")
    with pytest.raises(LookupError, match="not the file"):
        instrument._readings("t")
    for bad in ([row, row], [row | {"label": "live"}], [row | {"sha256": None}]):
        f.write_text("".join(json.dumps(r) + "\n" for r in bad))
        monkeypatch.setattr(instrument, "_ledger_entry", lambda obs, h=hashlib.sha256(f.read_bytes()).hexdigest():
                            {"population": {"results_file": "jev.jsonl", "results_sha256": h}})
        instrument._READINGS.pop("t", None)
        with pytest.raises(LookupError):
            instrument._readings("t")
    instrument._READINGS.pop("t", None)


def test_lens_refuses_unknown_names_and_labels():
    import instrument
    with pytest.raises(ValueError):
        instrument.lens(_FakeSurface({}), {"cited_by": "902"}, name="nope")
    with pytest.raises(ValueError):
        instrument.lens(_FakeSurface({}), {"cited_by": "902"}, label="live")
