import zipfile
from levadura_salvaje.sections import distinct_sections, sections


def _zip(tmp_path, volumes):
    p = tmp_path / "cfr.zip"
    with zipfile.ZipFile(p, "w") as z:
        for name, body in volumes.items():
            z.writestr(name, f"<CFRDOC>{body}</CFRDOC>")
    return p


def test_exact_repeats_are_dropped_but_same_number_with_different_text_is_kept(tmp_path):
    a = "<SECTION><SECTNO>§ 301.1</SECTNO><SUBJECT>A</SUBJECT><P>Same text.</P></SECTION>"
    old = "<SECTION><SECTNO>§ 1.141-1</SECTNO><SUBJECT>Standard deduction.</SUBJECT><P>Old.</P></SECTION>"
    new = "<SECTION><SECTNO>§ 1.141-1</SECTNO><SUBJECT>Definitions.</SUBJECT><P>New.</P></SECTION>"
    p = _zip(tmp_path, {"CFR-1997-title26-vol15.xml": a + a + old + new})
    assert len(list(sections(p))) == 4
    kept = [(s["sectno"], s["subject"]) for s in distinct_sections(p)]
    assert kept == [("301.1", "A"), ("1.141-1", "Standard deduction."), ("1.141-1", "Definitions.")]
