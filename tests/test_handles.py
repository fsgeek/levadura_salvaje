import pytest

from levadura_salvaje.ecfr import announced, text, twin
from levadura_salvaje.handles import Store

FIELDS = dict(source_locator="https://www.ecfr.gov/x", issuer="CFPB",
              publication_date="2026-03-02", edition_date="2026-03-02")


def test_the_same_bytes_and_fields_give_the_same_handle(tmp_path):
    s = Store(tmp_path)
    a = s.register(b"<SECTION>one</SECTION>", **FIELDS)
    assert s.register(b"<SECTION>one</SECTION>", **FIELDS) == a
    assert len((tmp_path / "handles.jsonl").read_text().splitlines()) == 1


def test_identity_changes_with_the_bytes_or_the_issuer(tmp_path):
    s = Store(tmp_path)
    a = s.register(b"one", **FIELDS)
    assert s.register(b"two", **FIELDS) != a
    assert s.register(b"one", **(FIELDS | {"issuer": "FRB"})) != a


def test_a_digest_that_contradicts_the_bytes_is_refused(tmp_path):
    with pytest.raises(ValueError):
        Store(tmp_path).register(b"one", artifact_digest="0" * 64, **FIELDS)


def test_every_open_is_logged_even_a_refused_one(tmp_path):
    s = Store(tmp_path)
    h = s.register(b"one", **FIELDS)
    assert s.open(h, by="inv-1", why="check", step=3) == b"one"
    with pytest.raises(KeyError):
        s.open("h-missing", by="inv-1", why="guess")
    reads = s.reads()
    assert [(r["handle"], r["found"], r["step"]) for r in reads] == [(h, True, 3), ("h-missing", False, None)]


def test_a_tampered_blob_is_refused(tmp_path):
    s = Store(tmp_path)
    h = s.register(b"one", **FIELDS)
    (tmp_path / "blobs" / s.describe(h)["artifact_digest"]).write_bytes(b"other")
    with pytest.raises(ValueError):
        s.open(h, by="inv-1", why="check")


def test_applicability_is_appended_beside_the_handle_never_inside_it(tmp_path):
    s = Store(tmp_path)
    h = s.register(b"one", **FIELDS)
    before = (tmp_path / "handles.jsonl").read_text()
    s.assert_applicability(h, asserted_by="gold", basis="FR 2026-0123",
                           affected_entities="non-Board-supervised creditors")
    s.assert_applicability(h, asserted_by="inv-1", basis="read", interpretation_status="superseded")
    assert (tmp_path / "handles.jsonl").read_text() == before
    assert [r["asserted_by"] for r in s.applicability(h)] == ["gold", "inv-1"]
    with pytest.raises(ValueError):
        s.assert_applicability(h, asserted_by="x", basis="y", artifact_digest="0")


def test_twins_pair_both_ways_and_only_where_a_twin_exists():
    assert twin("1026.35") == "226.35"
    assert twin("202.6") == "1002.6"
    assert twin("1013.4") is None
    assert twin("1026") is None


def test_text_strips_tags_and_collapses_space():
    assert text(b"<SECTION><HEAD>\xc2\xa7 1026.20</HEAD>\n <P>(a) Refinancings.</P></SECTION>") == \
        "§ 1026.20 (a) Refinancings."


def test_an_amendment_announcement_is_editorial_not_a_change():
    before = b"<SECTION><P>(a) Rule.</P></SECTION>"
    after = (b"<SECTION><P>Link to an amendment published at 91 FR 21668, Apr. 22, 2026.</P>"
             b"<P>(a) Rule.</P></SECTION>")
    assert text(after, editorial=False) == text(before, editorial=False) == "(a) Rule."
    assert text(after) != text(before)
    assert announced(after) == ["91 FR 21668"] and announced(before) == []
