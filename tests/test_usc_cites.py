"""Explicit "N U.S.C. M" citations (banking port, step 1). Cases are forms seen in the
2026-10-16 survey of 12 CFR (1997, 2010, 2025) and 31 CFR (2025)."""

from levadura_salvaje.usc_cites import extract


def paths(text):
    return [(c["title"], c["path"]) for c in extract(text)]


def test_plain_and_designators():
    assert paths("under 31 U.S.C. 1304.") == [("31", "1304")]
    assert paths("see 5 U.S.C. 504(c)(2).") == [("5", "504/c/2")]
    assert paths("12 U.S.C. 1424(a)(1)(B)) and § 925.6(a)(2)") == [("12", "1424/a/1/B")]


def test_letter_suffixed_sections():
    assert paths("(42 U.S.C. 4012a(b));") == [("42", "4012a/b")]
    assert paths("12 U.S.C. 1467a(a)(1)(F))") == [("12", "1467a/a/1/F")]
    assert paths("15 U.S.C. 78fff-3(c)(1), to the extent") == [("15", "78fff-3/c/1")]


def test_lists_share_the_title():
    assert paths("(20 U.S.C. 1681, 1682, 1683, 1685, 1686, 1687, 1688).") == [
        ("20", n) for n in ("1681", "1682", "1683", "1685", "1686", "1687", "1688")]
    assert paths("7 U.S.C. 1a(22), 1a(23), and 1a(31)); or") == [
        ("7", "1a/22"), ("7", "1a/23"), ("7", "1a/31")]
    assert paths("(5 U.S.C. 552 and 552a), see part 501") == [("5", "552"), ("5", "552a")]


def test_list_stops_at_another_title_or_other_citation():
    assert paths("12 U.S.C. 5385(f) and 15 U.S.C. 78fff-3(c)(1), to") == [
        ("12", "5385/f"), ("15", "78fff-3/c/1")]
    assert paths("5 U.S.C. 5514 and 5 CFR part 550, subpart K") == [("5", "5514")]
    assert paths("50 U.S.C. 1701-1706; E.O. 12170, 44 FR 65729;") == [("50", "1701-1706")]
    assert paths("12 U.S.C. 1818(h) and 12 CFR part 308.") == [("12", "1818/h")]


def test_et_seq_note_and_ranges_are_marked():
    [c] = extract("(15 U.S.C. 78a et seq. ), provided")
    assert c["path"] == "78a" and c["et_seq"]
    [c] = extract("(28 U.S.C. 2461 note). (2) The")
    assert c["path"] == "2461" and c["note"]
    [a, b] = extract("12 U.S.C. 601 et seq., and 611 et seq.). (b)")
    assert (a["path"], a["et_seq"], b["path"], b["et_seq"]) == ("601", True, "611", True)
    [c] = extract("(5 U.S.C. 554-557) governing")
    assert c["path"] == "554-557" and "hyphen" in c["flags"]


def test_spans_cover_the_cited_text():
    text = "under 12 U.S.C. 1818(b)(1) the"
    [c] = extract(text)
    assert text[c["span"][0]:c["span"][1]] == "12 U.S.C. 1818(b)(1)"


def test_not_citations():
    assert paths("26 U.S.C. (I.R.C. 1954) section 501(c)(20))") == []
    assert paths("the U.S.C. generally") == []


def test_section_sign_and_app():
    assert paths("12 U.S.C. § 1818(i)") == [("12", "1818/i")]
    [c] = extract("50 U.S.C. App. 5(b)")
    assert c["path"] == "5/b" and c["app"]


def test_section_word_lowercase_app_and_annotated():
    assert paths("(15 U.S.C. section 77e), in which") == [("15", "77e")]
    assert paths("with 12 U.S.C. section 24 (Seventh) and") == [("12", "24")]
    [c] = extract("once 50 U.S.C. app. 527 or the")
    assert c["path"] == "527" and c["app"]
    assert paths("Bank Act, 12 U.S.C.A. 1430(j) (") == [("12", "1430/j")]


def _statute():
    from levadura_salvaje.resolve import Statute
    st = Statute("test")
    st.status.update({"1818": None, "1818/b": None, "1701": None, "1706": None,
                      "78fff-3": None, "78fff-3/c": None, "78fff-3/c/1": None,
                      "1464": None, "1730": "repealed"})
    return {"12": st, "15": st, "50": st}


def test_resolve_against_titles_held():
    from levadura_salvaje.usc_cites import resolve
    st = _statute()
    out = lambda text: [resolve(c, st)["outcome"] for c in extract(text)]
    assert out("12 U.S.C. 1818(b)") == ["resolves"]
    assert out("12 U.S.C. 1818(z)") == ["absent-subdivision"]
    assert out("12 U.S.C. 1730") == ["repealed"]
    assert out("12 U.S.C. 1999") == ["absent-section"]
    assert out("42 U.S.C. 4012a") == ["title-not-held"]
    assert out("50 U.S.C. App. 5") == ["appendix"]


def test_resolve_hyphen_section_before_range():
    from levadura_salvaje.usc_cites import resolve
    st = _statute()
    [c] = extract("15 U.S.C. 78fff-3(c)(1)")
    assert resolve(c, st) == {"outcome": "resolves"}
    [c] = extract("50 U.S.C. 1701-1706")
    assert resolve(c, st) == {"outcome": "resolves", "via": "range", "ends": ["resolves", "resolves"]}
    [c] = extract("12 U.S.C. 1701-1999")
    assert resolve(c, st)["outcome"] == "absent-section"
