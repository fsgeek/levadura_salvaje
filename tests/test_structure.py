"""Paragraph structure of a CFR section, in citation-span coordinates (structure.py)."""

import xml.etree.ElementTree as ET

from levadura_salvaje import structure as st
from levadura_salvaje.citations import normalize
from levadura_salvaje.sections import _flat

SECTION = """<SECTION><SECTNO>§ 1.902-9</SECTNO><SUBJECT>Test section.</SUBJECT>
<P>(a) <E T="03">Definitions</E>. For purposes of section 902:</P>
<P>(1) <E T="03">Shareholder</E>. A domestic corporation.</P>
<P>(2) <E T="03">Taxes</E> —(i) <E T="03">In general</E>. Taxes deemed paid under section 902(a).</P>
<P>(ii) <E T="03">Pre-1987</E>. Taxes of years before 1987.</P>
<P>(A) A partnership ( PRS ) item.</P>
<P>(<E T="03">1</E>) An italic first level, under (A).</P>
<FP>A flush paragraph continuing (A)(1).</FP>
<P>(b) <E T="03">Facts</E>. (1) Corporation M is a shareholder.</P>
<EXAMPLE><HD>Example 1.</HD>
<P>(i) In 1992, M computes taxes deemed paid under section 902.</P>
<GPOTABLE><ROW><ENT>Deemed paid under section 902(a)</ENT><ENT>$10</ENT></ROW></GPOTABLE>
<P>(ii) The result follows.</P></EXAMPLE>
<P>(c) <E T="03">Effective/applicability date</E>. This section applies to distributions after 1986.</P>
</SECTION>"""


def _build():
    el = ET.fromstring(SECTION)
    norm, paras = st.paragraphs(el)
    return el, norm, paras


def _para(paras, start):
    return next(p for p in paras if p.text.startswith(start))


def test_text_is_exactly_the_span_coordinate_text():
    el, norm, _ = _build()
    assert norm == normalize(_flat(el))


def test_paragraph_ranges_slice_their_own_text():
    _, norm, paras = _build()
    for p in paras:
        assert norm[p.start:p.end].strip() == p.text


def test_inline_dash_designator_and_ancestry():
    _, _, paras = _build()
    a, two, ii = _para(paras, "(a)"), _para(paras, "(2) Taxes"), _para(paras, "(ii) Pre-1987")
    assert two.designators == ["2", "i"] and two.ancestry == [a.index]
    assert ii.level == 2 and ii.ancestry == [a.index, two.index]


def test_italic_level_under_capital_and_flush_continuation():
    _, _, paras = _build()
    cap, ital, flush = _para(paras, "(A)"), _para(paras, "(1) An italic"), _para(paras, "A flush")
    assert cap.level == 3 and ital.level == 4 and ital.parent == cap.index
    assert flush.designators == [] and flush.parent == ital.index


def test_heading_sentence_opens_a_level():
    _, _, paras = _build()
    b = _para(paras, "(b) Facts")
    assert b.designators == ["b", "1"] and b.level == 1 and b.ancestry == []


def test_example_has_its_own_scope_and_a_table_attaches_to_its_paragraph():
    _, norm, paras = _build()
    first = _para(paras, "(i) In 1992")
    assert first.scope != "main" and first.example_heading == "Example 1." and first.ancestry == []
    at = norm.index("Deemed paid under section 902(a)") + len("Deemed paid under ")
    p, exact = st.enclosing(paras, at)
    assert p.index == first.index and exact is False


def test_applicability_paragraph():
    _, _, paras = _build()
    assert st.applicability(paras).text.startswith("(c) Effective/applicability date")


def test_a_failed_designator_does_not_break_later_chains():
    el = ET.fromstring("<SECTION><P>(a) One.</P><P>(q) Out of order.</P><P>(b) Two.</P>"
                       "<P>(1) Under b.</P></SECTION>")
    _, paras = st.paragraphs(el)
    q, b, one = paras[1], paras[2], paras[3]
    assert q.failed and q.ancestry is None
    assert not b.failed and b.level == 0 and one.ancestry == [b.index]


def test_a_paragraph_failing_on_its_second_designator_leaves_no_partial_chain():
    """'(b)(q)' applies (b) and then fails on (q): the stack must revert, or (1) would hang under a (b)
    that no paragraph owns."""
    el = ET.fromstring("<SECTION><P>(a) One.</P><P>(b)(q) Bad.</P><P>(1) Under a.</P></SECTION>")
    _, paras = st.paragraphs(el)
    a, bad, one = paras
    assert bad.failed and bad.ancestry is None
    assert one.ancestry == [a.index] and None not in one.ancestry
