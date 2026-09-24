"""The test snippets of docs/citation-extractor-spec.md §5, verbatim."""

import pytest

from levadura_salvaje.citations import extract

R = lambda a, b: [f"{a}/{i}" for i in range(1, b + 1)]  # noqa: E731

CASES = [
    ("see section 263A and the regulations thereunder", ["263A"]),
    ("(4) Section 37(e)(9)(A) (relating to certain public retirement systems)", ["37/e/9/A"]),
    ("section 103(l)(1)(A) (relating to scholarship bonds)", ["103/l/1/A"]),
    ("as defined in section 7701 (a)(40) and the regulations thereunder", ["7701/a/40"]),
    ("a distribution from a section 4947(a) (2) trust", ["4947/a/2"]),
    ("by reason of section 1402(b)(1) (G) and (H)", ["1402/b/1/G", "1402/b/1/H"]),
    ("the taxes imposed by section 4261(a) and (b) are treated as", ["4261/a", "4261/b"]),
    ("tax-free distribution under section 1081(c) (1) or (2)", ["1081/c/1", "1081/c/2"]),
    ("sections 2055 and 2106(a)(2) (relating to estate tax deductions", ["2055", "2106/a/2"]),
    ("section 2041(b)(2) or 2514(e) of the Code does not apply", ["2041/b/2", "2514/e"]),
    ("see sections 861 through 864, Internal Revenue Code of 1954, and the regulations thereunder", ["861", "864"]),
    ("described in section 71(a) of prior law the same as divorce or separation instruments described "
     "in section 71, as amended by the Tax Reform Act of 1984?", ["71/a", "71"]),
    ("For the purpose of section 511 of the Act and the regulations in this part", []),
    ("under subsection (b) of section 553 of title 5 of the United States Code", []),
    ("under 25 U.S.C. 450 (f), (g), and (h)", []),
    ("the average benefits safe harbor of § 414(r)-5(f) for a testing year (see § 414(r)-5(f)(4)", []),
    ("Section § 414(r)-8 may require", []),
    ("subject to withholding under § 31.3402(g)-1(a)(2)", []),
    ("under §§ 1.267A-1 through 1.267A-3 and 1.267A-5", []),
    ("Section 1.822-3 is applicable only to taxable years beginning after December 31, 1953", []),
    ("as amended by section 8 of the Revenue Act of 1962 (76 Stat. 989)", []),
    ("see section 7815(d)(14) of Public Law 101-239.", []),
    ("Section 607(g) of the Act and this section provide rules", []),
    ("described in section 30D(e)(1)(A) of the Internal Revenue Code (Code)", ["30D/e/1/A"]),
    ("an exemption application for a section 501(c)(9), 501(c)(17), or 501(c)(20) organization under "
     "section 505", ["501/c/9", "501/c/17", "501/c/20", "505"]),
    ("adjustments under section 1016(a) (2) and (3) of the Code for depreciation", ["1016/a/2", "1016/a/3"]),
    ("ownership of stock provided by section 958 (a) and (b), and the principles", ["958/a", "958/b"]),
    ("an exchange described in section 332, 351, 354, 355, 356, or 361.",
     ["332", "351", "354", "355", "356", "361"]),
    ("the three elections listed in section 46(f) (1), (2), and (3), see 26 CFR 12.3",
     ["46/f/1", "46/f/2", "46/f/3"]),
    ("(i) Section 1.475(b)-1(b)(1)(i) (concerning equity interests", []),
    ("withheld as tax under section 3402 of this section", ["3402"]),
    ("a foreign subsidiary (as defined in section 3121(1)(8) and the regulations thereunder)", ["3121/1/8"]),
    ("registered under section 6 of the Securities Exchange Act of 1934 (15 U.S.C. 78f)", []),
    ("meets the requirements of subsection (b) of section 346 falls within", ["346/b"]),
    ("the elections described in section 2632(b)(3) and (c)(5) of the Code", ["2632/b/3", "2632/c/5"]),
    ("subject to the taxes imposed by section 1, 2, 3, or 11 upon any portion", ["1", "2", "3", "11"]),
    ("Sections 75(l), 77(e), 199, 337(2), 455, and 659(6) of the Bankruptcy Act (11 U.S.C. 203(l), "
     "205(e), 599, 737(2), 855, and 1059(6))", []),
    ("(Sec. 613, 46 Stat. 756, as amended, sec. 618, 46 Stat. 757, as amended, sec. 7327, 68A Stat. 871; "
     "(19 U.S.C. 1613, 1618, 26 U.S.C. 7327))", ["7327"]),
    ("a deduction under section 1382 (b)(2) or (c)(2)(B)", ["1382/b/2", "1382/c/2/B"]),
    ("Sections 4911(f) (1) through (3) contain a limited anti-abuse rule", ["4911/f/1", "4911/f/2", "4911/f/3"]),
    ("after application of the exclusions under section 1402(a)(1)-(17)", R("1402/a", 17)),
    ("Section 56.4911-8 provides rules concerning", []),
    ("Outline of regulation provision for section 7701(b)-1 through (b)-9.", []),
    ("the principles of sections 861-863 and the regulations thereunder", ["861", "863"]),
    ("(For provisions relating to the treatment of tips as wages, see 3121(a)(12) and 3121(q).)", []),
    ("the sum of the rates of tax under subsections (a) and (b) of section 3101", ["3101/a", "3101/b"]),
    ("determined in accordance with subparagraph (B) of such section", [None]),
    ("(or by reason of section 24(b) of the Internal Revenue Code of 1939)", []),
    ("pursuant to section 1034(a), or section 112(n) of the Internal Revenue Code of 1939", ["1034/a"]),
    ("any individual described in paragraphs (1) through (10) of section 152(a)", R("152/a", 10)),
    ("paragraphs (4), (6) and (8) of section 6334(a) (relating to property exempt from levy)",
     ["6334/a/4", "6334/a/6", "6334/a/8"]),
    ("(Sec. 7805 of the Internal Revenue Code of 1954, 68A Stat. 917; 26 U.S.C. 7805)", ["7805"]),
    ("the total to be distributed on February 1, 2005, pursuant to § 408(d)(4) is $475.", ["408/d/4"]),
    ("(computed with the application of sections 857(d) and § 1.857-7)", ["857/d"]),
    ("sections 551-558 (relating to foreign personal holding companies), sections 951-964 (relating to "
     "controlled foreign corporations), and section 904 (relating to the limitation on the foreign tax "
     "credit) of the Code", ["551", "558", "951", "964", "904"]),
    ("transaction described in section 368 (a) or 355, with respect to which", ["368/a", "355"]),
    ('established under section 6621 (b) § 301.6621-1 ("adjusted rate")', ["6621/b"]),
    ("The higher penalty under the flush language of section 6707(b)(2) will not apply", ["6707/b/2"]),
    ("Classification of earnings and profits for purposes of section 959 (c)(1) (c)(2) (c)(3) 1963 $100",
     ["959/c/1"]),
    ("see section 6012(b)(3) and 28 U.S.C. 960", ["6012/b/3"]),
    ("to which Congress extends relief under section 302 of the Katrina Emergency Tax Relief Act of 2005.", []),
    ("except in the case of a proceeding under section 77 or chapter X of the Bankruptcy Act", []),
    ("under section 452(b) of title IV of the Social Security Act as amended", []),
    ("as defined in section 3231(e)(1) (for purposes of applying sections 3201(b) and 3221(b) (and so much "
     "of section 3211(a) as relates to the rates of the taxes imposed by sections 3101 and 3111))",
     ["3231/e/1", "3201/b", "3221/b", "3211/a", "3101", "3111"]),
    ("without regard to section 152(b)(1), (b)(2), and (d)(1)(B)", ["152/b/1", "152/b/2", "152/d/1/B"]),
    ("by a trustee of property included in the gross estate under section 2035 through 2038, or section 2041",
     ["2035", "2038", "2041"]),
    ("treated as a single taxpayer under old section 163(j)(6)(C)", ["163/j/6/C"]),
    ("see paragraph (c) (5) of § 53.4947-1", []),
    ("a depository account as defined in § 1.1471- 5(b)(3)(i)", []),
    ("under section 6104(a)(1) (C) or (D)", ["6104/a/1/C", "6104/a/1/D"]),
    ("the deductions provided in part VIII (section 241 and following), subchapter B, chapter 1 of the Code",
     ["241"]),
    ("Under Article VI (2) of the convention … on Form 1120-F", []),
]


@pytest.mark.parametrize("text,expected", CASES)
def test_spec_snippets(text, expected):
    assert [r["path"] for r in extract(text)] == expected


def by_path(text, **kw):
    return {r["path"]: r for r in extract(text, **kw)}


def test_part_57_section_9010_is_the_aca_fee():
    assert extract("Pursuant to section 9010(g)(4), the information reported", part="57") == []
    assert [r["path"] for r in extract("Pursuant to section 9010(g)(4), the information")] == ["9010/g/4"]


def test_truncated_tail_is_dropped():
    assert extract("… for such taxable year for purposes of section 8", truncated=True) == []


def test_flags():
    assert "code_1954" in by_path("see sections 861 through 864, Internal Revenue Code of 1954, and")["864"]["flags"]
    assert by_path("see sections 861 through 864, Internal Revenue Code of 1954, and")["864"]["range"] == \
        {"from": "861", "to": "864", "level": "section"}
    assert "historical" in by_path("described in section 71(a) of prior law the same")["71/a"]["flags"]
    assert "historical" in by_path("treated as a single taxpayer under old section 163(j)(6)(C)")["163/j/6/C"]["flags"]
    assert "attributive" in by_path("a distribution from a section 4947(a) (2) trust")["4947/a/2"]["flags"]
    assert "attributive" not in by_path("under section 505 of")["505"]["flags"]
    assert "self_ref_qualifier" in by_path("withheld as tax under section 3402 of this section")["3402"]["flags"]
    assert "irregular_chain" in by_path("as defined in section 3121(1)(8) and")["3121/1/8"]["flags"]
    assert "range_expanded" in by_path("Sections 4911(f) (1) through (3) contain")["4911/f/2"]["flags"]
    assert "flush" in by_path("under the flush language of section 6707(b)(2) will")["6707/b/2"]["flags"]
    assert "open_range" in by_path("part VIII (section 241 and following), subchapter B")["241"]["flags"]
    assert "code_1954" in by_path("(Sec. 7805 of the Internal Revenue Code of 1954, 68A Stat. 917; "
                                  "26 U.S.C. 7805)")["7805"]["flags"]
    assert extract("subparagraph (B) of such section")[0]["kind"] == "anaphor"
    assert "toc" in extract("section 56(a) adjustments", reg_id="1.56-0")[0]["flags"]
