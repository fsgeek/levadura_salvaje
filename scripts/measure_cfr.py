"""Measure the structure of 26 CFR editions into the ledger, one entry per volume.

Deterministic counts only -- no model judges anything here. Each edition is
the GovInfo bulk-data zip for one year, identified by URL and sha256 so
anyone can fetch the same bytes and check the numbers.

Why per volume: an "edition" is not one moment. Volumes without amendments
are not revised, so the 2025 edition holds volumes dated 2025, 2024 and 2020.
observed_at is each volume's own title-page date (CFRDOC/FMTR/TITLEPG/DATE,
or CFRDOC/DATE in older markup). A "Revised as of" phrase in the body text is
a citation of an earlier edition, not this volume's date, and is ignored.
A volume with no front-matter date is refused.

Usage: uv run python scripts/measure_cfr.py 1997 2025
       (expects data/cfr/CFR-<year>-title-26.zip; see URL below)
"""

import hashlib
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter
from datetime import datetime
from pathlib import Path

from levadura_salvaje.ledger import append, verify

URL = "https://www.govinfo.gov/bulkdata/CFR/{y}/title-26/CFR-{y}-title-26.zip"
DATE_PATHS = ("CFRDOC/FMTR/TITLEPG/DATE", "CFRDOC/DATE")
AS_OF = re.compile(r"as of ([a-z]+ \d{1,2}, \d{4})", re.I)
INSTRUMENT = {
    "name": "scripts/measure_cfr.py",
    "version": "3",
    "method": (
        "xml.etree iterparse per volume; observed_at = front-matter DATE at "
        f"{' or '.join(DATE_PATHS)}; sections = SECTION elements; section numbers = "
        "SECTNO text with leading section signs and whitespace normalized; "
        "paragraphs = P elements inside SECTION; xml_bytes = uncompressed volume"
    ),
}


def measure_volume(data: bytes, handle) -> dict:
    path, date = [], None
    sections, paragraphs = 0, 0
    numbers: Counter = Counter()
    for event, el in ET.iterparse(handle, events=("start", "end")):
        if event == "start":
            path.append(el.tag)
            continue
        where = "/".join(path)
        path.pop()
        if date is None and where in DATE_PATHS:
            m = AS_OF.search(" ".join("".join(el.itertext()).split()))
            if m:
                date = datetime.strptime(m.group(1).title(), "%B %d, %Y").date().isoformat()
        if el.tag == "SECTION":
            sections += 1
            paragraphs += sum(1 for _ in el.iter("P"))
            no = el.find("SECTNO")
            text = "".join(no.itertext()) if no is not None else ""
            numbers[re.sub(r"\s+", " ", text.lstrip("§ ").strip())] += 1
            el.clear()
    repeated = {k: v for k, v in numbers.items() if v > 1}
    return date, {
        "xml_bytes": len(data),
        "sections": sections,
        "distinct_section_numbers": len(numbers),
        "repeated_within_volume": sorted(repeated.items(), key=lambda kv: -kv[1])[:3],
        "paragraphs_in_sections": paragraphs,
        "section_numbers_lexical_min": min(numbers, default=None),
        "section_numbers_lexical_max": max(numbers, default=None),
    }


def main() -> None:
    for year in sys.argv[1:]:
        path = Path(f"data/cfr/CFR-{year}-title-26.zip")
        zip_sha = hashlib.sha256(path.read_bytes()).hexdigest()
        with zipfile.ZipFile(path) as z:
            names = sorted((n for n in z.namelist() if n.endswith(".xml")),
                           key=lambda n: int(re.search(r"vol(\d+)", n).group(1)))
            vols = [int(re.search(r"vol(\d+)", n).group(1)) for n in names]
            absent = sorted(set(range(1, max(vols) + 1)) - set(vols))
            pending = []
            for name in names:
                data = z.read(name)
                with z.open(name) as f:
                    date, value = measure_volume(data, f)
                if date is None:
                    sys.exit(f"REFUSED: {year} {name} has no front-matter date; nothing recorded")
                pending.append((name, date, data, value))
        for name, date, data, value in pending:
            rec = append({
                "observed_at": date,
                "instrument": INSTRUMENT,
                "population": {
                    "source": URL.format(y=year), "zip_sha256": zip_sha, "edition": year,
                    "volume_file": name, "sha256": hashlib.sha256(data).hexdigest(),
                },
                "quantity": "cfr26_volume_structure",
                "value": value,
                **({"coverage_gap": f"volume numbers absent from this zip: {absent}; not examined"}
                   if absent else {}),
            })
            print(rec["id"], year, name.split("-")[-1], date,
                  f"sections={value['sections']:,}")
    print("ledger verified:", verify(), "entries")


if __name__ == "__main__":
    main()
