"""How a citation to a renumbered statute names its subdivision: ordinal paragraph or letter (patents I5)."""

from levadura_salvaje.para_forms import forms


def f(text):
    return [x["form"] for x in forms(text, title="35", section="112")]


def test_letter_form():
    assert f("means-plus-function under 35 U.S.C. 112(f), the") == ["letter"]


def test_ordinal_after():
    assert f("as required by 35 U.S.C. 112, sixth paragraph, the") == ["ordinal"]
    assert f("35 U.S.C. 112, ¶ 6 applies") == ["ordinal"]
    assert f("under 35 U.S.C. 112, paragraph 2, and") == ["ordinal"]


def test_ordinal_before():
    assert f("the first paragraph of 35 U.S.C. 112 requires") == ["ordinal"]


def test_bare_and_other_sections():
    assert f("an application under 35 U.S.C. 112 and 35 U.S.C. 111(a)") == ["bare"]
    assert f("35 U.S.C. 111, first paragraph") == []


def test_numbered_paragraph_in_parentheses_is_ordinal():
    # 37 CFR 41.110 (2010): "35 U.S.C. 112(6)" means the sixth paragraph, not a subsection.
    assert f("in the form permitted under 35 U.S.C. 112(6), file") == ["ordinal"]
    assert f("under 35 U.S.C. 112(1) of an") == ["ordinal"]
