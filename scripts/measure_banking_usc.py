"""Measure explicit U.S.C. citations in banking regulation against titles 12, 15 and 31 at 119-120.

Deterministic; predictions in predictions/2026-10-16-banking-usc-claude.md (stamped before any
resolution). One ledger entry per text (12 CFR 1997, 2010, 2025; 31 CFR 2025). Per-citation detail
goes to results/banking-usc-<edition>-title-<t>.jsonl.

Usage: uv run python scripts/measure_banking_usc.py
"""

import hashlib
import json
from collections import Counter
from pathlib import Path

from levadura_salvaje import usc_cites
from levadura_salvaje.ledger import append, verify
from levadura_salvaje.resolve import Statute
from levadura_salvaje.sections import distinct_sections

RP = "119-120"
HELD = ("12", "15", "31")
TEXTS = [("1997", "12"), ("2010", "12"), ("2025", "12"), ("2025", "31")]
NOT_RATED = {"title-not-held", "appendix"}
PREDICTIONS = "predictions/2026-10-16-banking-usc-claude.md"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def measure(edition: str, title: str, statutes: dict) -> dict:
    src = Path(f"data/banking/CFR-{edition}-title-{title}.zip")
    out = Path(f"results/banking-usc-{edition}-title-{title}.jsonl")
    rows = []
    for s in distinct_sections(src):
        text = usc_cites.normalize(s["text"])  # spans index this text
        for c in usc_cites.extract(text, normalized=True):
            r = usc_cites.resolve(c, statutes)
            rows.append({"sectno": s["sectno"], "volume_file": s["volume_file"], "ordinal": s["ordinal"],
                         "title": c["title"], "path": c["path"], "span": c["span"], "flags": c["flags"],
                         "et_seq": c["et_seq"], "note": c["note"], "app": c["app"], **r})
    out.write_text("".join(json.dumps(x, sort_keys=True) + "\n" for x in rows))

    rated = [x for x in rows if x["outcome"] not in NOT_RATED]
    broken = [x for x in rated if x["outcome"] != "resolves"]
    secs = {}
    for x in rated:  # section-level outcome for each distinct cited section
        key = (x["title"], x["path"].split("/")[0])
        secs.setdefault(key, x["outcome"] if x["outcome"] != "absent-subdivision" else "resolves")
    citing = {}
    for x in rated:
        k = (x["volume_file"], x["ordinal"])
        citing[k] = citing.get(k, False) or x["outcome"] != "resolves"
    hyphen = [x for x in rated if "hyphen" in x["flags"]]
    m = {
        "citations": len(rows),
        "outcomes": dict(Counter(x["outcome"] for x in rows)),
        "rated_citations": len(rated),
        "broken_citations": len(broken),
        "P1_broken_share": round(len(broken) / len(rated), 4) if rated else None,
        "distinct_cited_sections": len(secs),
        "dead_sections": sum(v != "resolves" for v in secs.values()),
        "P2_dead_section_share": round(sum(v != "resolves" for v in secs.values()) / len(secs), 4) if secs else None,
        "citing_cfr_sections": len(citing),
        "cfr_sections_with_broken": sum(citing.values()),
        "P3_share": round(sum(citing.values()) / len(citing), 4) if citing else None,
        "P4_absent_subdivision_share_of_broken":
            round(sum(x["outcome"] == "absent-subdivision" for x in broken) / len(broken), 4) if broken else None,
        "hyphen_rated": len(hyphen),
        "P6_hyphen_range_share": round(sum(x.get("via") == "range" for x in hyphen) / len(hyphen), 4) if hyphen else None,
    }
    entry = append({
        "observed_at": f"{edition}-01-01",
        "observed_at_note": f"{edition} CFR title {title} edition (annual; title 12 revised as of Jan 1, "
                            f"title 31 as of Jul 1), read against USC release point {RP}",
        "instrument": {
            "name": "scripts/measure_banking_usc.py",
            "method": f"usc_cites v{usc_cites.VERSION}: explicit 'N U.S.C. M' citations in distinct_sections, "
                      f"resolved with resolve.Statute v{__import__('levadura_salvaje.resolve', fromlist=['VERSION']).VERSION} "
                      f"against USLM titles {', '.join(HELD)} at {RP}; hyphen tokens tried as a section, then a range",
            "known_limits": "explicit citations only (no bare 'section N', no named acts); titles other than 12, 15 "
                            "and 31 and the pre-1958 appendices are not rated; editions predate the statute "
                            "(older editions are read anachronistically); a break is a candidate until audited",
            "predictions": PREDICTIONS,
        },
        "population": {"edition": edition, "title": title, "source_sha256": sha(src), "release_point": RP},
        "quantity": "banking_usc_citation_resolution",
        "value": {**m, "output": str(out), "output_sha256": sha(out)},
    })
    print(edition, title, entry["id"], json.dumps(m))
    return m


def main():
    statutes = {t: Statute.load(RP, title=t) for t in HELD}
    for edition, title in TEXTS:
        measure(edition, title, statutes)
    print("ledger:", verify())


if __name__ == "__main__":
    main()
