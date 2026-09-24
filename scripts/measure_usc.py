"""Measure the structure of 26 USC release points into the ledger.

Deterministic counts only -- no model judges anything here. Each release
point is the unmodified OLRC USLM zip archived on the signed tag
corpus/usc26-119-4-119-110, identified by URL and sha256.

One entry per release point (provision counts by level and status), plus one
entry comparing the two (provisions added, removed, and changed in text).
Per-provision detail goes to results/usc26-provisions-<release point>.jsonl.

observed_at is the release point's law date: the title as amended through
that public law. The XML's own dcterms:created can be earlier -- a title that
no law touched is carried forward unchanged -- so it is recorded separately
and not used as the moment.

Usage: uv run python scripts/measure_usc.py
       (expects data/usc/xml_usc26@<rp>.zip)
"""

import hashlib
import json
import re
import zipfile
from collections import Counter
from pathlib import Path

from levadura_salvaje.ledger import append, verify
from levadura_salvaje.usc import LEVELS, provisions, release_point

URL = "https://uscode.house.gov/download/releasepoints/us/pl/119/{law}/xml_usc26@119-{law}.zip"
TAG = "corpus/usc26-119-4-119-110"
# Release point law dates, from the OLRC release point listing (see the tag's release notes).
LAW_DATES = {"119-4": "2025-03-15", "119-110": "2026-09-16"}
INSTRUMENT = {
    "name": "scripts/measure_usc.py",
    "version": "1",
    "method": (
        "xml.etree iterparse of usc26.xml; provisions = section..subitem elements whose USLM "
        "identifier starts /us/usc/t26/; status = the element's status attribute; text = "
        "flattened element text without notes or source credits; text_sha256 over that text"
    ),
}


def created(zip_path: Path) -> str | None:
    with zipfile.ZipFile(zip_path) as z, z.open("usc26.xml") as f:
        m = re.search(rb"<dcterms:created>([^<]+)<", f.read(4096))
    return m.group(1).decode() if m else None


def measure(zip_path: Path) -> tuple[dict, dict]:
    rp = release_point(zip_path)
    out = Path(f"results/usc26-provisions-{rp}.jsonl")
    rows = list(provisions(zip_path))
    out.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in rows))
    ids = Counter(r["identifier"] for r in rows)
    law = rp.split("-")[1]
    rec = append({
        "observed_at": LAW_DATES[rp],
        "observed_at_note": f"law date of release point {rp}; the file's dcterms:created is "
                            f"{created(zip_path)}",
        "instrument": INSTRUMENT,
        "population": {
            "title": "26 USC", "release_point": rp,
            "source": URL.format(law=law), "archived_on_tag": TAG,
            "zip_sha256": hashlib.sha256(zip_path.read_bytes()).hexdigest(),
            "results_file": str(out),
            "results_sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
        },
        "quantity": "usc26_structure",
        "value": {
            "provisions": len(rows),
            "by_level": {lv: sum(r["level"] == lv for r in rows) for lv in LEVELS},
            "by_status": dict(Counter(f"{r['level']}:{r['status']}" for r in rows if r["status"])),
            "sections_in_force": sum(r["level"] == "section" and not r["status"] for r in rows),
            "distinct_identifiers": len(ids),
            "identifiers_with_multiple_versions": sorted(k for k, v in ids.items() if v > 1),
            "chars_in_sections": sum(r["chars"] for r in rows if r["level"] == "section"),
        },
    })
    return rec, {r["identifier"]: r for r in rows}


def compare(old: tuple[dict, dict], new: tuple[dict, dict]) -> dict:
    (orec, o), (nrec, n) = old, new
    added = sorted(set(n) - set(o))
    removed = sorted(set(o) - set(n))
    both = set(o) & set(n)
    changed = [i for i in both if o[i]["text_sha256"] != n[i]["text_sha256"]]
    status = sorted(i for i in both if o[i]["status"] != n[i]["status"])
    sections = lambda ids: sorted({i.split("/")[4] for i in ids})  # /us/usc/t26/<sNNN>/...
    return append({
        "observed_at": nrec["observed_at"],
        "observed_at_note": f"change between {orec['observed_at']} and {nrec['observed_at']}",
        "instrument": INSTRUMENT | {"method": INSTRUMENT["method"] + "; compared by identifier "
                                    "(where one identifier has several versions, the last in "
                                    "document order stands for it)"},
        "population": {"title": "26 USC",
                       "release_points": [orec["population"]["release_point"],
                                          nrec["population"]["release_point"]]},
        "quantity": "usc26_release_diff",
        "value": {
            "added": len(added), "removed": len(removed),
            "text_changed": len(changed), "status_changed": status,
            "added_by_level": dict(Counter(n[i]["level"] for i in added)),
            "removed_by_level": dict(Counter(o[i]["level"] for i in removed)),
            "sections_touched": sections(added + removed + changed),
            "sections_removed": [i for i in removed if o[i]["level"] == "section"],
            "sections_added": [i for i in added if n[i]["level"] == "section"],
        },
        "derived_from": [orec["id"], nrec["id"]],
    })


def main() -> None:
    measured = [measure(Path(f"data/usc/xml_usc26@{rp}.zip")) for rp in LAW_DATES]
    for rec, _ in measured:
        print(rec["id"], rec["population"]["release_point"], rec["value"]["provisions"])
    diff = compare(*measured)
    v = diff["value"]
    print(diff["id"], {k: v[k] for k in ("added", "removed", "text_changed")},
          len(v["sections_touched"]), "sections touched")
    print("ledger verified:", verify())


if __name__ == "__main__":
    main()
