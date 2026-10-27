"""Citations marked as old law, and transition-date mentions (patents v2)."""

from levadura_salvaje.dated_cites import marker, transition_mentions


def m(text):
    i = text.index("35 U.S.C.")
    j = text.index(" ", text.index("U.S.C.") + 7)
    return marker(text, (i, j))


def test_stated_date_after_citation():
    assert m("under 35 U.S.C. 102(g) as in effect on March 15, 2013, the") == {"marker": "date", "date": "2013-03-15"}
    assert m("35 U.S.C. 103(c) in effect prior to March 16, 2013 applies") == {"marker": "date", "date": "2013-03-16"}


def test_pre_aia_before_citation():
    assert m("under pre-AIA 35 U.S.C. 102(e) the") == {"marker": "pre-AIA", "date": None}


def test_later_or_absent_date_is_not_old_law():
    assert m("35 U.S.C. 102 as in effect on March 16, 2013 or later") == {"marker": None, "date": None}
    assert m("an application under 35 U.S.C. 111(a) filed") == {"marker": None, "date": None}


def test_transition_mentions_are_classed():
    t = ("If a nonprovisional application filed on or after March 16, 2013, contains or contained at any time "
         "a claim to a claimed invention that has an effective filing date before March 16, 2013, the applicant "
         "must so state. Section 1.131 as in effect on March 15, 2013 applies.")
    assert [x["class"] for x in transition_mentions(t)] == ["conditioned", "conditioned", "date-only"]


def test_date_after_a_list_of_subsections():
    # 37 CFR 1.104 (2025), found in v2's dry run.
    assert m("under 35 U.S.C. 102(e), (f), or (g) in effect prior to March 16, 2013, and") == {
        "marker": "date", "date": "2013-03-16"}


def test_hybrid_rule_with_comma_is_conditioned():
    # 37 CFR 1.55 and 1.78 (2025): "contains, or contained at any time", found in v2's dry run.
    t = "filed prior to March 16, 2013, and also contains, or contained at any time, a claim to"
    assert [x["class"] for x in transition_mentions(t)] == ["conditioned"]
