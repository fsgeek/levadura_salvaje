"""PTAB v1: how final written decisions (2021-2026) mark the patent law they apply.

Deterministic; predictions in predictions/2026-10-27-ptab-applicability-claude.md (stamped at f810f93 after the
metadata was fetched and before any decision text was read). Text comes from each decision's PDF via pdftotext
(cached in data/ptab/txt). Bands come from the patent's grant date. Builds audit packet P1 (pre-band unmarked
decisions plus marked controls). One ledger entry, none with --dry-run.

Usage: uv run python scripts/measure_ptab_applicability.py [--dry-run]
"""

import hashlib
import json
import random
import re
import subprocess
import sys
from pathlib import Path

from levadura_salvaje import ptab_marks
from levadura_salvaje.ledger import append, verify

SEED = 20261027
DIR = Path("data/ptab")
OUT = Path("results/ptab-applicability.jsonl")
AUDIT = Path("results/ptab-audit-p1")
PREDICTIONS = "predictions/2026-10-27-ptab-applicability-claude.md"
CITE = re.compile(r"35\s+U\.\s?S\.\s?C\.")


def text_of(doc_id: str) -> str:
    cache = DIR / "txt" / f"{doc_id}.txt"
    if not cache.exists():
        cache.parent.mkdir(exist_ok=True)
        r = subprocess.run(["pdftotext", "-q", str(DIR / "pdf" / f"{doc_id}.pdf"), "-"], capture_output=True, text=True)
        cache.write_text(r.stdout)
    return re.sub(r"\s+", " ", cache.read_text())


def band(grant: str | None) -> str:
    if not grant:
        return "unknown"
    return "pre" if grant < "2013-03-16" else "mid" if grant < "2017" else "late"


def share(rows, key):
    return round(sum(r[key] for r in rows) / len(rows), 4) if rows else None


def main():
    dry = "--dry-run" in sys.argv
    meta = [json.loads(x) for x in (DIR / "meta.jsonl").open()]
    fw = [r for r in meta if (r["documentData"].get("documentTypeDescriptionText") or "").startswith("Final Written Decision")]
    rows, texts = [], {}
    for r in fw:
        did = r["documentData"]["documentIdentifier"]
        if not (DIR / "pdf" / f"{did}.pdf").exists():
            continue
        t = text_of(did)
        texts[did] = t
        rows.append({"doc": did, "trial": r["trialNumber"], "issued": r["decisionData"].get("decisionIssueDate"),
                     "grant": r["patentOwnerData"].get("grantDate"), "band": band(r["patentOwnerData"].get("grantDate")),
                     "chars": len(t), "no_text": len(t.strip()) < 2000, **ptab_marks.marks(t)})
    OUT.write_text("".join(json.dumps(x, sort_keys=True) + "\n" for x in rows))
    ok = [r for r in rows if not r["no_text"]]
    by = {b: [r for r in ok if r["band"] == b] for b in ("pre", "mid", "late")}
    pre_un = [r for r in by["pre"] if not r["marked"]]
    early = [r for r in by["pre"] if (r["issued"] or "")[:4] in ("2021", "2022")]
    late_yrs = [r for r in by["pre"] if (r["issued"] or "")[:4] in ("2025", "2026")]
    m = {"decisions": len(rows), "with_text": len(ok), "expected": len(fw),
         "band_sizes": {b: len(v) for b, v in by.items()},
         "Q1_pre_marked": share(by["pre"], "marked"), "Q2_mid_marked": share(by["mid"], "marked"),
         "Q3_late_marked": share(by["late"], "marked"), "Q4_pre_basis": share(by["pre"], "basis"),
         "Q5_pre_unmarked_old_subdivision": share(pre_un, "old_subdivision"), "pre_unmarked": len(pre_un),
         "Q6_pre_marked_2021_22": share(early, "marked"), "Q6_pre_marked_2025_26": share(late_yrs, "marked"),
         "Q7_no_text_share": round(sum(r["no_text"] for r in rows) / len(rows), 4) if rows else None}
    print(json.dumps(m))
    if dry:
        return

    rng = random.Random(SEED)
    meta_by = {r["documentData"]["documentIdentifier"]: r for r in fw}

    def passages(t):
        spans = [x.start() for x in CITE.finditer(t)][:8]
        return [t[max(0, a - 400):a + 400] for a in spans]

    items = [(r, False) for r in rng.sample(pre_un, min(30, len(pre_un)))] + \
            [(r, True) for r in rng.sample([r for r in by["pre"] if r["marked"]], 10)]
    rng.shuffle(items)
    AUDIT.mkdir(exist_ok=True)
    packet = [{"item": f"p-{i:02d}", "trial": r["trial"], "decision_issued": r["issued"], "patent_granted": r["grant"],
               "patent": meta_by[r["doc"]]["patentOwnerData"].get("patentNumber"), "passages": passages(texts[r["doc"]])}
              for i, (r, _) in enumerate(items, 1)]
    key = [{"item": f"p-{i:02d}", "marked": mk, "doc": r["doc"]} for i, (r, mk) in enumerate(items, 1)]
    (AUDIT / "packet.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in packet))
    (AUDIT / "key.jsonl").write_text("".join(json.dumps(x) + "\n" for x in key))

    entry = append({
        "observed_at": "2026-10-27",
        "observed_at_note": "PTAB final written decisions issued 2021-2026, as held by the USPTO Open Data Portal on 2026-10-27",
        "instrument": {
            "name": "scripts/measure_ptab_applicability.py",
            "method": f"pdftotext of each decision PDF; ptab_marks v{ptab_marks.VERSION} (pre-AIA marker, stated basis, "
                      "pre-AIA-only subdivisions 103(a)/102(e)(f)(g)); bands by the patent's grant date",
            "known_limits": "lexical; grant date stands in for effective filing date (mid and late bands mix regimes); "
                            "the portal holds 2021-2026 decisions only; quoted old law counts as a mark",
            "predictions": PREDICTIONS,
        },
        "population": {"source": "api.uspto.gov/api/v1/patent/trials/decisions/search",
                       "query": 'trialMetaData.trialStatusCategory:"Final Written Decision"',
                       "meta_sha256": hashlib.sha256((DIR / "meta.jsonl").read_bytes()).hexdigest()},
        "quantity": "ptab_applicability_marks_v1",
        "value": {**m, "output": str(OUT), "output_sha256": hashlib.sha256(OUT.read_bytes()).hexdigest(),
                  "audit_packet_sha256": hashlib.sha256((AUDIT / "packet.jsonl").read_bytes()).hexdigest()},
    })
    print(entry["id"])
    print("ledger:", verify())


if __name__ == "__main__":
    main()
