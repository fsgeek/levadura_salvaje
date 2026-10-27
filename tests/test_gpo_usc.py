

def test_other_titles_are_read_not_silently_skipped(tmp_path):
    # 2026-10-27: DOC matched only "documentid:26_", so a title-35 package gave 0 provisions, silently.
    from levadura_salvaje.gpo_usc import provisions
    doc = ('<!-- documentid:35_-ptII-ch10-sec102 currentthrough:20110107 documentPDFPage:5 -->'
           '<h3 class="section-head">&sect;102. Conditions for patentability; novelty</h3>'
           '<!-- field-start:statute --><p class="statutory-body">(g) text</p><!-- field-end:statute -->')
    p = tmp_path / "USCODE-2010-title35.htm"
    p.write_text(doc)
    secs = [x for x in provisions(p) if x["level"] == "section"]
    assert [x["path"] for x in secs] == ["s102"]
    assert secs[0]["identifier"] == "/us/usc/t35/s102"
