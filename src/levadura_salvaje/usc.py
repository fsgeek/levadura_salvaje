"""Read a 26 USC release point (OLRC USLM XML) as a set of provisions.

Every structural element that carries a USLM ``identifier`` attribute is a
provision: a section (``/us/usc/t26/s56``) or anything below it down to the
subclause (``/us/usc/t26/s56/a/1/A/i``). A provision's ``status`` (repealed,
renumbered, reserved, omitted) is kept, because a repealed section still has
an element -- its number exists, its rules do not.

``text_sha256`` is over the provision's flattened text, notes excluded, so
two release points can be compared provision by provision.
"""

import hashlib
import re
import xml.etree.ElementTree as ET
import zipfile
from collections.abc import Iterator
from pathlib import Path

NS = "{http://xml.house.gov/schemas/uslm/1.0}"
LEVELS = ("section", "subsection", "paragraph", "subparagraph", "clause", "subclause", "item", "subitem")
TAGS = {NS + level: level for level in LEVELS}
PREFIX = "/us/usc/t26/"


def _flat(el) -> str:
    """Element text without its notes (editorial matter, not law)."""
    parts = []

    def walk(e):
        if e.tag in (NS + "notes", NS + "note", NS + "sourceCredit"):
            if e.tail:
                parts.append(e.tail)
            return
        if e.text:
            parts.append(e.text)
        for child in e:
            walk(child)
        if e is not el and e.tail:
            parts.append(e.tail)

    walk(el)
    return " ".join("".join(parts).split())


def release_point(zip_path: Path) -> str:
    return re.search(r"@(\d+-\d+)", zip_path.name).group(1)


def provisions(zip_path: Path) -> Iterator[dict]:
    """Yield every identified provision, innermost first (iterparse end order)."""
    with zipfile.ZipFile(zip_path) as z, z.open("usc26.xml") as f:
        for _, el in ET.iterparse(f, events=("end",)):
            level = TAGS.get(el.tag)
            ident = el.get("identifier", "")
            if level is None or not ident.startswith(PREFIX):
                continue
            num, heading = el.find(NS + "num"), el.find(NS + "heading")
            text = _flat(el)
            yield {
                "identifier": ident,
                "path": ident[len(PREFIX):],
                "level": level,
                "status": el.get("status"),
                "num": num.get("value") if num is not None else None,
                "heading": " ".join("".join(heading.itertext()).split()) if heading is not None else "",
                "chars": len(text),
                "text_sha256": hashlib.sha256(text.encode()).hexdigest(),
            }
            if level == "section":
                el.clear()
