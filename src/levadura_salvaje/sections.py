"""Iterate the sections of a 26 CFR edition zip, as plain text.

A section is identified by (volume_file, ordinal) -- its position among the
SECTION elements of its volume -- and not by its number alone: the 1997
edition repeats 601 section numbers. ``sectno`` is the normalized number,
used to pair sections across editions; ``sha256`` is over ``text``, so any
later reading of the same section can prove it saw the same words.
"""

import hashlib
import re
import xml.etree.ElementTree as ET
import zipfile
from collections.abc import Iterator
from pathlib import Path


def _flat(el) -> str:
    return " ".join("".join(el.itertext()).split())


def _volume_number(name: str) -> int:
    return int(re.search(r"vol(\d+)", name).group(1))


def sections(zip_path: Path) -> Iterator[dict]:
    with zipfile.ZipFile(zip_path) as z:
        names = sorted((n for n in z.namelist() if n.endswith(".xml")), key=_volume_number)
        for name in names:
            ordinal = 0
            with z.open(name) as f:
                for _, el in ET.iterparse(f, events=("end",)):
                    if el.tag != "SECTION":
                        continue
                    ordinal += 1
                    no = el.find("SECTNO")
                    subject = el.find("SUBJECT")
                    text = _flat(el)
                    yield {
                        "volume_file": name,
                        "ordinal": ordinal,
                        "sectno": re.sub(r"\s+", " ", (_flat(no) if no is not None else "").lstrip("§ ").strip()),
                        "subject": _flat(subject) if subject is not None else "",
                        "text": text,
                        "sha256": hashlib.sha256(text.encode()).hexdigest(),
                    }
                    el.clear()
