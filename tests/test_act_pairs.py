"""Act-section citations paired with a U.S.C. citation (the parity lens, banking v1)."""

from levadura_salvaje.act_pairs import consensus, pairs


def short(text):
    return [(p["act"], p["act_section"], p["act_desig"], p["title"], p["usc_section"], p["usc_path"])
            for p in pairs(text)]


def test_parenthesized_pair():
    assert short("under section 8(b) of the Federal Deposit Insurance Act (12 U.S.C. 1818(b)), the") == [
        ("Federal Deposit Insurance Act", "8", ["b"], "12", "1818", "1818/b")]


def test_comma_pair_and_year():
    assert short("section 3 of the Bank Holding Company Act of 1956, 12 U.S.C. 1842, as") == [
        ("Bank Holding Company Act of 1956", "3", [], "12", "1842", "1842")]


def test_misaddressed_pair_is_still_a_pair():
    assert short("section 509 of the Gramm-Leach-Bliley Act (12 U.S.C. 6809), may") == [
        ("Gramm-Leach-Bliley Act", "509", [], "12", "6809", "6809")]


def test_unpaired_and_far_citations_are_not_pairs():
    assert short("section 8 of the Federal Deposit Insurance Act applies") == []
    assert short("section 8 of the FDI Act and other law, see 12 U.S.C. 1818") == []
    assert short("section 1.56-1 of the regulations (12 U.S.C. 1818)") == []


def test_short_names_and_letters():
    assert short("section 4(c)(8) of the BHC Act (12 U.S.C. 1843(c)(8))") == [
        ("BHC Act", "4", ["c", "8"], "12", "1843", "1843/c/8")]
    assert short("section 15G of that Act; section 15G of the Exchange Act (15 U.S.C. 78o-11)") == [
        ("Exchange Act", "15G", [], "15", "78o-11", "78o-11")]


def test_consensus_flags_the_odd_one_out():
    ps = [{"act": "GLB Act", "act_section": "509", "title": "15", "usc_section": "6809"}] * 4 + [
        {"act": "GLB Act", "act_section": "509", "title": "12", "usc_section": "6809"}]
    m = consensus(ps, min_n=3, min_share=0.75)
    assert m[("GLB Act", "509")] == {"target": ("15", "6809"), "n": 5, "share": 0.8}
    m = consensus(ps[:3] + ps[4:] * 2, min_n=3, min_share=0.75)
    assert ("GLB Act", "509") not in m  # 3 of 5 is not a consensus


def test_v2_whole_act_citations_do_not_pair():
    assert short("section 10 of the Home Owners' Loan Act (12 U.S.C. 1461 et seq.), a") == []
    assert short("section 203 of the IEEPA Act (50 U.S.C. 1701 note), a") == []


def test_v2_lists_do_not_pair():
    assert short("section 4(c)(13) of the BHC Act (12 U.S.C. 615, 1843(c)(13)), the") == []
    assert short("section 7 of the International Banking Act of 1978 (12 U.S.C. 347d and 3105), a") == []


def test_v2_the_act():
    assert short("section 4(k) of the Act (12 U.S.C. 1843(k)), a") == [
        ("Act", "4", ["k"], "12", "1843", "1843/k")]


def test_v2_commas_in_long_names():
    assert short("section 1101 of the Financial Institutions Reform, Recovery, and Enforcement Act of 1989 "
                 "(12 U.S.C. 3331), a") == [("Financial Institutions Reform, Recovery, and Enforcement Act of 1989",
                                            "1101", [], "12", "3331", "3331")]
