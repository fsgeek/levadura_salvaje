from levadura_salvaje.baseline import match


def test_phrase_is_case_insensitive():
    assert match("The Alternative Minimum Tax applies.")["phrases"] == ["alternative minimum tax"]


def test_cites_subsections():
    assert match("as defined in section 56(g)(4)(C)")["cites"] == ["56"]


def test_59a_is_not_amt():
    assert match("the tax imposed by section 59A")["positive"] is False


def test_56a_is_amt():
    assert match("adjusted financial statement income under section 56A(c)")["cites"] == ["56A"]


def test_lists_are_read_past_the_first_number():
    assert match("sections 1, 55 and 56 apply")["cites"] == ["55", "56"]
    assert match("sections 53 through 59")["cites"] == ["53", "59"]


def test_longer_numbers_do_not_match_their_prefix():
    assert match("section 5501 and section 553")["positive"] is False


def test_regulation_citations_are_not_code_citations():
    assert match("see § 1.56-1")["positive"] is False
