"""Twin regulations in 2025 12 CFR, v1: each Dodd-Frank-transferred regulation's old copy against
the CFPB's, section by section.

Deterministic; predictions in predictions/2026-10-25-banking-twins-claude.md (stamped before this
ran). Sections pair by the number after the part (202.14 with 1002.14). Similarity is difflib's
ratio over words, after masking part numbers and agency names; a pair below 0.95 is diverged.
Builds the W1 audit packet (diverged pairs plus blind controls, shown as unattributed A and B).
One ledger entry, none with --dry-run.

Usage: uv run python scripts/measure_banking_twins.py [--dry-run]
"""

import difflib
import hashlib
import json
import random
import re
import sys
from pathlib import Path

from levadura_salvaje.ledger import append, verify
from levadura_salvaje.sections import distinct_sections

SEED = 20261025
TWINS = {"B": ("202", "1002"), "E": ("205", "1005"), "M": ("213", "1013"), "V": ("222", "1022"),
         "Z": ("226", "1026"), "P": ("332", "1016")}
DIVERGED = 0.95
ZIP = Path("data/banking/CFR-2025-title-12.zip")
OUT = Path("results/banking-twins-2025.jsonl")
AUDIT = Path("results/banking-twins-audit-w1")
PREDICTIONS = "predictions/2026-10-25-banking-twins-claude.md"
AGENCY = re.compile(r"\b(?:Board of Governors of the Federal Reserve System|Federal Reserve System|Board|Bureau|"
                    r"Bureau of Consumer Financial Protection|Consumer Financial Protection Bureau|CFPB|"
                    r"Federal Deposit Insurance Corporation|FDIC|Corporation)\b")


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def words(text: str, parts: tuple[str, str]) -> list[str]:
    t = re.sub(rf"\b(?:{parts[0]}|{parts[1]})(?=\.\d)", "N", text)
    t = re.sub(rf"\bpart (?:{parts[0]}|{parts[1]})\b", "part N", t)
    return AGENCY.sub("AGENCY", t).split()


def line_diff(a: list[str], b: list[str], limit: int = 40) -> list[str]:
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op != "equal":
            out.append(f"{op}: A[{' '.join(a[i1:i2])[:300]}] B[{' '.join(b[j1:j2])[:300]}]")
            if len(out) == limit:
                out.append("(more changes not shown)")
                break
    return out


def main():
    dry = "--dry-run" in sys.argv
    wanted = {p for pair in TWINS.values() for p in pair}
    secs = {s["sectno"]: re.sub(r"\s+", " ", s["text"]).strip() for s in distinct_sections(ZIP)
            if s["sectno"].split(".")[0] in wanted}
    rows = []
    for reg, (old, new) in TWINS.items():
        tails = {k.split(".", 1)[1] for k in secs if k.split(".")[0] in (old, new)}
        for tail in sorted(tails, key=lambda t: [int(x) if x.isdigit() else x for x in re.split(r"(\d+)", t)]):
            a, b = secs.get(f"{old}.{tail}"), secs.get(f"{new}.{tail}")
            row: dict = {"regulation": reg, "old": f"{old}.{tail}", "new": f"{new}.{tail}",
                   "kind": "pair" if a and b else "only-old" if a else "only-new"}
            if a and b:
                wa, wb = words(a, (old, new)), words(b, (old, new))
                row.update(ratio=round(difflib.SequenceMatcher(None, wa, wb, autojunk=False).ratio(), 4),
                           old_words=len(wa), new_words=len(wb))
                row["diverged"] = row["ratio"] < DIVERGED
            rows.append(row)
    OUT.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in rows))

    pairs = [r for r in rows if r["kind"] == "pair"]
    by = {reg: [r for r in pairs if r["regulation"] == reg] for reg in TWINS}
    share = {reg: round(sum(r["diverged"] for r in v) / len(v), 4) if v else None for reg, v in by.items()}
    nob = [r for r in pairs if r["regulation"] != "B"]
    m = {
        "T1_pairs": len(pairs),
        "T2_diverged_share_excl_B": round(sum(r["diverged"] for r in nob) / len(nob), 4),
        "diverged_share_by_regulation": share,
        "T3_highest": max((s, reg) for reg, s in share.items() if s is not None)[1],
        "T4_lowest": min((s, reg) for reg, s in share.items() if s is not None)[1],
        "T5_only_new_excl_B": sum(r["kind"] == "only-new" and r["regulation"] != "B" for r in rows),
        "only_old": sum(r["kind"] == "only-old" for r in rows),
        "diverged": sum(r["diverged"] for r in pairs),
    }
    print(json.dumps(m))
    if dry:
        for r in pairs:
            if r["diverged"]:
                print(r["old"], r["new"], r["ratio"], r["old_words"], r["new_words"])
        return

    rng = random.Random(SEED)
    div = [r for r in pairs if r["diverged"]]
    picks = rng.sample(div, min(40, len(div)))
    controls = rng.sample([r for r in pairs if not r["diverged"]], 10)
    items = [(r, True) for r in picks] + [(r, False) for r in controls]
    rng.shuffle(items)
    AUDIT.mkdir(exist_ok=True)
    packet, key = [], []
    for i, (r, is_div) in enumerate(items, 1):
        old, new = TWINS[r["regulation"]]
        a, b = secs[r["old"]], secs[r["new"]]
        flip = rng.random() < 0.5  # which copy is shown as A is random, so position says nothing
        ta, tb = (b, a) if flip else (a, b)
        wa, wb = words(ta, (old, new)), words(tb, (old, new))
        item = f"item-{i:02d}"
        packet.append({"item": item, "regulation": f"Regulation {r['regulation']}",
                       "section": f"§ N.{r['old'].split('.', 1)[1]}",
                       "text_A": " ".join(wa)[:9000], "text_B": " ".join(wb)[:9000],
                       "truncated": max(len(wa), len(wb)) > 1400, "diff": line_diff(wa, wb)})
        key.append({"item": item, "diverged": is_div, "old": r["old"], "new": r["new"],
                    "A_is": "new" if flip else "old", "ratio": r["ratio"]})
    (AUDIT / "packet.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in packet))
    (AUDIT / "key.jsonl").write_text("".join(json.dumps(x) + "\n" for x in key))

    entry = append({
        "observed_at": "2025-01-01",
        "observed_at_note": "12 CFR as of Jan 1, 2025",
        "instrument": {
            "name": "scripts/measure_banking_twins.py",
            "method": "sections of each old/CFPB twin part paired by number after the part; difflib ratio over "
                      "words with part numbers and agency names masked; diverged below 0.95",
            "known_limits": "pairing by section number only (a renumbered section reads as only-old plus "
                            "only-new); appendices and supplements not read; similarity is not meaning: a "
                            "diverged pair is a candidate until audited (W1)",
            "predictions": PREDICTIONS,
        },
        "population": {"edition": "2025", "title": "12", "twins": {k: list(v) for k, v in TWINS.items()},
                       "source_sha256": sha(ZIP)},
        "quantity": "banking_twin_divergence",
        "value": {**m, "output": str(OUT), "output_sha256": sha(OUT),
                  "audit_packet_sha256": sha(AUDIT / "packet.jsonl")},
    })
    print(entry["id"])
    print("ledger:", verify())


if __name__ == "__main__":
    main()
