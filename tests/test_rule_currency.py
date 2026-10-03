"""The rule-currency lens's excerpts, and the invariants its measurement and audit scripts enforce
(docs/rule-currency-review-1.md, #4 and #8)."""

import hashlib
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import audit_rule_currency as audit  # noqa: E402
import measure_rule_currency_qwen as m  # noqa: E402

from levadura_salvaje.lenses import rule_currency as rc  # noqa: E402


def test_excerpt_marks_exactly_the_span():
    text = "a" * 2000 + "section 902" + "b" * 1000
    x = rc.excerpt(text, (2008, 2011), "1.1-1", "Subject.")
    assert x.startswith("§ 1.1-1 Subject. [excerpt; the section continues before and after]")
    assert x.count(rc.OPEN) == 1 and x.count(rc.CLOSE) == 1
    assert x[x.index(rc.OPEN) + 1:x.index(rc.CLOSE)] == "902"
    assert "section " + rc.OPEN in x


def test_excerpt_at_the_edges_says_where_it_was_cut():
    x = rc.excerpt("section 902 applies.", (8, 11), "1.1-1", "S.")
    assert "[excerpt" not in x and x.endswith(rc.OPEN + "902" + rc.CLOSE + " applies.")


def _item(i, excerpt="e"):
    return {"key": f"k{i}", "volume_file": "v", "ordinal": 1, "index": i, "excerpt": excerpt}


def _row(i, label="untimed", excerpt="e"):
    return {"volume_file": "v", "ordinal": 1, "index": i, "label": label,
            "excerpt_sha256": hashlib.sha256(excerpt.encode()).hexdigest()}


def test_check_final_accepts_the_exact_population():
    m.check_final([_row(0), _row(1)], [_item(0), _item(1)])


@pytest.mark.parametrize("rows", [
    [_row(0)],                                  # missing
    [_row(0), _row(1), _row(2)],                # unexpected
    [_row(0), _row(0), _row(1)],                # duplicate
    [_row(0), _row(1, label="live")],           # invalid label
    [_row(0), _row(1, excerpt="other")],        # excerpt from another lens version
])
def test_check_final_refuses(rows):
    with pytest.raises(SystemExit):
        m.check_final(rows, [_item(0), _item(1)])


@pytest.mark.parametrize("line", [
    "{not json",
    json.dumps({"key": "k", "label": "live"}),
    json.dumps({"key": "k", "label": "untimed", "model_reported": "another-model"}),
])
def test_resume_distrusts_bad_cached_rows(line):
    assert m._cached(line) is None


def test_resume_keeps_good_cached_rows():
    assert m._cached(json.dumps({"key": "k", "label": "untimed", "model_reported": m.MODEL}))["key"] == "k"


@pytest.fixture
def reader_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "results").mkdir()

    def write(rows):
        Path(f"results/rule-currency-audit-v{audit.V}-902-reader-a.jsonl").write_text(
            "".join(json.dumps(r) + "\n" for r in rows))
    return write


def test_answers_accept_a_complete_valid_set(reader_file):
    reader_file([{"item": "item-01", "label": "untimed"}, {"item": "item-02", "label": "not_a_rule"}])
    assert audit._answers("reader-a", {"item-01", "item-02"}) == {"item-01": "untimed", "item-02": "not_a_rule"}


@pytest.mark.parametrize("rows", [
    [{"item": "item-01", "label": "untimed"}],                                              # missing
    [{"item": "item-01", "label": "untimed"}, {"item": "item-01", "label": "untimed"},
     {"item": "item-02", "label": "untimed"}],                                              # duplicate
    [{"item": "item-01", "label": "live"}, {"item": "item-02", "label": "untimed"}],        # invalid label
    [{"item": "item-01", "label": "untimed"}, {"item": "item-02", "label": "untimed"},
     {"item": "item-03", "label": "untimed"}],                                              # extra
])
def test_answers_refuse(reader_file, rows):
    reader_file(rows)
    with pytest.raises(SystemExit):
        audit._answers("reader-a", {"item-01", "item-02"})
