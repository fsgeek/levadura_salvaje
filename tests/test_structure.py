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
    """'(b)(q)' applies (b) and then fails on (q). (1) must not hang under a (b) that no paragraph owns,
    nor under (a): its chain passes through the failure, so it is unknown (Codex review 2, P1 #4)."""
    el = ET.fromstring("<SECTION><P>(a) One.</P><P>(b)(q) Bad.</P><P>(1) Under a.</P></SECTION>")
    _, paras = st.paragraphs(el)
    _a, bad, one = paras
    assert bad.failed and bad.ancestry is None
    assert one.failed and one.ancestry is None      # under the unknown chain, not silently under (a)


def test_applicability_is_the_last_top_level_date_paragraph():
    el = ET.fromstring("<SECTION><P>(a) Definitions and special effective date. Terms.</P><P>(1) One.</P>"
                       "<P>(b) Rules. Text.</P><P>(c) Effective/applicability dates. Applies after 1986.</P>"
                       "</SECTION>")
    _, paras = st.paragraphs(el)
    assert st.applicability(paras).text.startswith("(c) Effective/applicability dates")


def test_a_chain_through_a_failure_is_unknown_until_a_known_sibling():
    """Codex review 2, P1 #4: '(a) Live' -> '(q) Before 1987' -> '(1) ...' gave (1) the ancestor (a),
    losing the possible governing limit in (q)."""
    el = ET.fromstring("<SECTION><P>(a) Live rule.</P><P>(q) Before 1987.</P><P>(1) Section 902 applies.</P>"
                       "<FP>A continuation.</FP><P>(2) More.</P><P>(b) Known again.</P><P>(1) Under b.</P>"
                       "</SECTION>")
    _, paras = st.paragraphs(el)
    _a, q, one, cont, two, b, b1 = paras
    assert q.failed and q.ancestry is None
    for p in (one, cont, two):
        assert p.failed and p.ancestry is None
    assert not b.failed and b.level == 0 and b.ancestry == []
    assert not b1.failed and b1.ancestry == [b.index]


def test_an_inline_roman_opens_a_child_before_continuing_a_letter():
    """Codex review 2, P1 #3 (1.367(b)-4(h)(7)): in '(2) Triangular —(i) Definition', (i) is (2)'s child,
    not a sibling of (h)."""
    lead = "".join(f"<P>({c}) {c.upper()}.</P>" for c in "abcdefg")
    el = ET.fromstring(f"<SECTION>{lead}<P>(h) Rules.</P><P>(1) One.</P>"
                       "<P>(2) <E T=\"03\">Triangular</E> —(i) <E T=\"03\">Definition</E>. Text.</P>"
                       "<P>(ii) Second.</P><P>(i) Applicability date. After 2020.</P></SECTION>")
    _, paras = st.paragraphs(el)
    h, _one, two, ii, i_top = paras[7:]
    assert two.designators == ["2", "i"] and two.level == 2 and two.ancestry == [h.index]
    assert ii.level == 2 and ii.ancestry == [h.index, two.index]
    assert i_top.level == 0 and i_top.ancestry == []


def test_placed_paragraphs_carry_their_path():
    _, _, paras = _build()
    assert _para(paras, "(ii) Pre-1987").path == ("a", "2", "ii")
    assert _para(paras, "(b) Facts").path == ("b", "1")
    assert _para(paras, "A flush").path is None          # a continuation isn't addressable


def test_section_references_are_parsed_only_when_they_say_of_this_section():
    t = ("M is deemed under paragraphs (a) and (b) of this section to have paid $63, and see paragraph "
         "(c)(2)(ii) of this section; but paragraph (d) of § 1.902-1 and paragraph (e) of this example don't count.")
    assert st.section_refs(t) == [("a",), ("b",), ("c", "2", "ii")]


def test_addressed_finds_a_main_scope_paragraph_by_path():
    _, _, paras = _build()
    assert st.addressed(paras, ("a", "2", "ii")).text.startswith("(ii) Pre-1987")
    assert st.addressed(paras, ("a", "2")).text.startswith("(2) Taxes")
    assert st.addressed(paras, ("z",)) is None


def _sec(body):
    return st.paragraphs(ET.fromstring(f"<SECTION>{body}</SECTION>"))[1]


def test_governing_date_is_scoped_to_what_it_says_it_governs():
    """Codex review 2, P1 #5 (1.904-7, 1.338-9): a date paragraph governs the paragraph it names,
    not the whole section; a special-topic date heading is not the section's date."""
    P = _sec("<P>(a) Rule. Text.</P>"
             "<P>(b) Special effective date for high withholding tax interest. For purposes of (a), text.</P>"
             "<P>(c) Other rule. Text.</P><P>(d) D.</P><P>(e) E.</P>"
             "<P>(f) Dividends. Text.</P><P>(1) A rule.</P>"
             "<P>(2) Effective/applicability date. This paragraph (f) shall apply to dividends after 2020.</P>")
    a, f1 = P[0], P[6]
    d = st.governing_date(P, f1)
    assert d is not None and d[0].text.startswith("(2) Effective/applicability date") and d[1] == ("f",)
    assert st.governing_date(P, a) is None          # nothing governs (a): not (b)'s special date, not (f)(2)


def test_governing_date_prefers_the_most_specific_scope():
    """1.985-1: a section-wide date in (a)(2) and a date for (b)(2)(ii) only."""
    P = _sec("<P>(a) Applicability and effective date —(1) Purpose and scope. These regulations provide guidance.</P>"
             "<P>(2) Effective date. These regulations apply to taxable years beginning after December 31, 1986.</P>"
             "<P>(b) Rules —(1) General. Text.</P><P>(2) Special —(i) One. Text.</P><P>(ii) Two. Text.</P>"
             "<P>(A) Effective date. This paragraph (b)(2)(ii) applies to taxable years beginning after April 6, 1998.</P>")
    b1, b2i, ii_eff = P[2], P[3], P[5]
    assert st.governing_date(P, b1)[1] == ()                          # section-wide (a)(2)
    assert st.governing_date(P, b2i)[1] == ()
    assert st.governing_date(P, P[4])[1] == ("b", "2", "ii")          # (b)(2)(ii) is under its own date
    assert st.governing_date(P, P[0]) is not None and st.governing_date(P, P[0])[0].index == 1


def test_a_rate_is_not_a_date():
    """1.963-2: 'effective foreign tax rate' is not an applicability provision."""
    P = _sec("<P>(c) Effective foreign tax rate —(1) Single corporation. The term means the rate.</P>"
             "<P>(e) Foreign income taxes used in determining effective foreign tax rate. Text.</P>")
    assert st.governing_date(P, P[0]) is None


def test_date_scope_follows_the_subject_of_applies():
    """1.367(b)-7: 'Except as otherwise provided in this paragraph (h), this section applies' is
    section-wide."""
    P = _sec("<P>(a) A.</P><P>(b) Applicability dates. Except as otherwise provided in this paragraph (b), "
             "this section applies to transactions after 2010.</P>")
    assert st.date_scope(P, P[1]) == ()


def test_a_date_heading_on_an_outer_designator_counts_when_the_paragraph_applies_something():
    """1.6038-2: '(m) Effective/applicability dates —(1) In general. This section applies ...'"""
    P = _sec("<P>(a) Applicability and effective date —(1) Purpose and scope. These regulations provide guidance.</P>"
             "<P>(b) Effective/applicability dates —(1) In general. This section applies to years after 2020.</P>")
    assert st.date_scope(P, P[0]) is None        # a purpose paragraph under a date heading applies nothing
    assert st.date_scope(P, P[1]) == ()
