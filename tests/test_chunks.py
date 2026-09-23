from levadura_salvaje.chunks import header, split


def test_short_text_is_one_chunk():
    assert split("A short section.", 100) == ["A short section."]


def test_chunks_cover_the_text_exactly_and_fit():
    text = " ".join(f"Sentence number {i} says something." for i in range(500))
    pieces = split(text, 300)
    assert "".join(pieces) == text
    assert all(len(p) <= 300 for p in pieces)
    assert all(p.endswith(". ") for p in pieces[:-1])


def test_falls_back_to_spaces_then_hard_cuts():
    assert "".join(split("word " * 100, 23)) == "word " * 100
    assert split("x" * 10, 4) == ["xxxx", "xxxx", "xx"]


def test_header_marks_fragments():
    assert "part 2 of 3" in header("1.56(g)-1", "Adjusted current earnings.", 2, 3)
    assert "part" not in header("1.55-1", "AMTI.", 1, 1)
