"""Read the eCFR's point-in-time text of a section, keyed by the bytes that came back.

The eCFR versioner (https://www.ecfr.gov/api/versioner/v1/) serves every section as it stood on a
date, with no key. Each fetch is cached under ``data/ecfr/`` by date and section, and is
identified by the sha256 of its bytes. The eCFR is editorial, not the official CFR (National
Archives), so its dates locate text; they do not settle which text governs (replay design,
Sol's review item 4).

The endpoint refuses uncompressed responses (HTTP 406), so every request asks for gzip.
"""

import gzip
import hashlib
import json
import re
import urllib.request
from pathlib import Path

BASE = "https://www.ecfr.gov/api/versioner/v1"
CACHE = Path("data/ecfr")
# Dodd-Frank moved these regulations to the CFPB; the Board kept its own copies.
TWINS = {"1002": "202", "1005": "205", "1026": "226"}
ISSUER = {"1002": "CFPB", "1005": "CFPB", "1026": "CFPB", "202": "FRB", "205": "FRB", "226": "FRB"}


def _get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"Accept-Encoding": "gzip",
                                               "User-Agent": "levadura-salvaje (research)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        body = r.read()
        return gzip.decompress(body) if r.headers.get("Content-Encoding") == "gzip" else body


def versions(title: int, since: str, cache: Path = CACHE) -> list[dict]:
    """Every content version of a title issued on or after `since`, cached once per call date."""
    path = cache / f"versions-title-{title}-since-{since}.json"
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(_get(f"{BASE}/versions/title-{title}.json?issue_date%5Bgte%5D={since}"))
    return json.loads(path.read_text())["content_versions"]


def section_xml(date: str, section: str, title: int = 12, cache: Path = CACHE) -> tuple[bytes, str, str]:
    """(bytes, sha256, source url) of `section` (e.g. "1026.20") as it stood on `date`."""
    part = section.split(".")[0]
    url = f"{BASE}/full/{date}/title-{title}.xml?part={part}&section={section}"
    path = cache / "full" / date / f"{section}.xml"
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(_get(url))
    data = path.read_bytes()
    return data, hashlib.sha256(data).hexdigest(), url


# The eCFR inserts this when an amendment is *published*, before it takes effect. The versioner
# records the insertion as a substantive version on the publication date. In smoke-1 it was the
# whole of four "changes" on 2026-04-22; the text changed on 2026-07-21 (91 FR 21668).
ANNOUNCED = re.compile(r"Link to an amendment published at (\d+ FR \d+), ([A-Z][a-z]{2}\.? \d{1,2}, \d{4})\.?")


def text(xml: bytes, editorial: bool = True) -> str:
    """The section's words, tags removed and whitespace collapsed. With editorial=False, the
    eCFR's amendment-announcement notices are dropped, so only the regulation's own text is left."""
    t = " ".join(re.sub(r"<[^>]+>", " ", xml.decode("utf-8")).split())
    return t if editorial else " ".join(ANNOUNCED.sub(" ", t).split())


def announced(xml: bytes) -> list[str]:
    """The Federal Register citations of amendments the eCFR says are published but not yet in
    this text."""
    return [m.group(1) for m in ANNOUNCED.finditer(text(xml))]


def twin(section: str) -> str | None:
    """The other agency's copy of a section (1026.20 -> 226.20), or None if the part has no twin."""
    part, _, rest = section.partition(".")
    other = TWINS.get(part) or {v: k for k, v in TWINS.items()}.get(part)
    return f"{other}.{rest}" if other and rest else None
