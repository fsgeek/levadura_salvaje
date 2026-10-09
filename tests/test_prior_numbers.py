import importlib.util
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "prior_numbers", Path(__file__).parents[1] / "scripts/measure_prior_numbers.py")
pn = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pn)

USLM = 'xmlns="http://xml.house.gov/schemas/uslm/1.0"'


def test_number_takes_its_text_when_renumbered_into_it_not_at_first_enactment():
    # §33's text was enacted in 1954 as §32 and renumbered §33 in 1984; the old §33 meant
    # something else until then.
    credit = ("(Aug. 16, 1954, ch. 736, 68A Stat. 13, § 32; Pub. L. 98–369, div. A, title IV, "
              "§ 474(a), July 18, 1984, 98 Stat. 830, renumbered § 33)")
    assert pn.number_acquired("33", credit) == date(1984, 7, 18)
    assert pn.number_acquired("34", "(Pub. L. 97–424, title V, Jan. 6, 1983, 96 Stat. 2097)") == date(1983, 1, 6)


def test_only_a_prior_note_about_the_same_number_counts():
    root = ET.fromstring(f"""<uscDoc {USLM}><main>
      <section identifier="/us/usc/t26/s34"><sourceCredit>(Pub. L. 97–424, Jan. 6, 1983)</sourceCredit>
        <notes><note topic="priorProvisions"><p>A prior section 34, acts Aug. 16, 1954, related to
        dividends received by individuals.</p></note></notes></section>
      <section identifier="/us/usc/t26/s35"><sourceCredit>(Pub. L. 97–424, Jan. 6, 1983)</sourceCredit>
        <notes><note topic="priorProvisions"><p>A prior section 34 was renumbered section 35.</p>
        </note></notes></section>
    </main></uscDoc>""")
    found = pn.prior_numbers(root)
    assert set(found) == {"34"}
    assert found["34"]["acquired"] == date(1983, 1, 6)


def test_regulation_dates_come_from_every_fr_cite_and_lsa_is_flagged():
    sec = ET.fromstring("""<SECTION><SECTNO>§ 1.1-1</SECTNO><P>(z) Added text. [T.D. 9000, 67 FR 100,
      Jan. 2, 2002]</P><CITA>[T.D. 6500, 25 FR 11402, Nov. 26, 1960]</CITA>
      <EDNOTE>For Federal Register citations affecting § 1.1-1, see the List of CFR Sections Affected</EDNOTE>
      </SECTION>""")
    found, lsa = pn.regulation_dates(sec)
    assert sorted(found) == [date(1960, 11, 26), date(2002, 1, 2)]
    assert lsa


def test_classify_against_the_numbers_date():
    reused = date(1983, 1, 6)
    assert pn.classify([date(1960, 11, 26), date(1971, 5, 25)], reused) == "older_than_number"
    assert pn.classify([date(1960, 11, 26), date(1990, 1, 1)], reused) == "amended_across"
    assert pn.classify([date(1990, 1, 1)], reused) == "newer_than_number"
    assert pn.classify([], reused) == "undated"
