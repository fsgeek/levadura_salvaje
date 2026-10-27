"""How a PTAB decision marks the patent law it applies (ptab v1)."""

from levadura_salvaje.ptab_marks import marks


def test_marked_and_basis():
    t = ("Because the '516 patent has an effective filing date before March 16, 2013, the effective date of "
         "the applicable AIA amendments, we refer to the pre-AIA version of 35 U.S.C. § 103.")
    assert marks(t) == {"marked": True, "basis": True, "old_subdivision": False}


def test_dash_variants_and_old_subdivisions():
    assert marks("under pre–AIA 35 U.S.C. § 102(e)")["marked"] is True
    assert marks("unpatentable under 35 U.S.C. § 103(a) over Smith")["old_subdivision"] is True
    assert marks("anticipated under 35 U.S.C. §§ 102(e) and 103")["old_subdivision"] is True


def test_plain_aia_citation_marks_nothing():
    assert marks("unpatentable under 35 U.S.C. § 103 over Smith and Jones") == {
        "marked": False, "basis": False, "old_subdivision": False}
    assert marks("35 U.S.C. § 102(a)(1) prior art")["old_subdivision"] is False
