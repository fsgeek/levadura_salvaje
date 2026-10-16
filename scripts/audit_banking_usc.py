"""Build the blind packet for audit A1 (predictions/2026-10-16-banking-usc-claude.md).

40 broken 2025 citations (12 and 31 CFR), sampled with seed 20261016. Each item gives the citing
text and the statute's own record for the cited path at 119-120. It carries no outcome label:
the reader sees what the statute holds, not what the resolver concluded.

Usage: uv run python scripts/audit_banking_usc.py
"""

import json
import random
from pathlib import Path

from levadura_salvaje import usc_cites
from levadura_salvaje.sections import distinct_sections

RP, SEED, N = "119-120", 20261016, 40
OUT = Path("results/banking-usc-audit-a1")


def record(title: str, path: str, prov: dict) -> str:
    sec, *subs = path.split("/")
    if "-" in sec and f"s{sec}" not in prov:
        lo, hi = sec.split("-", 1)
        return "This token may be one section or a range. " + " | ".join(
            record(title, x, prov) for x in (lo, hi))
    s = prov.get(f"s{sec}")
    if s is None:
        near = sorted(k[1:] for k in prov if k.startswith(f"s{sec[:-1] or sec}") and "/" not in k)[:8]
        return (f"Title {title} at release point {RP} has no section element numbered {sec}. "
                f"Section numbers that begin the same way: {', '.join(near) or 'none'}.")
    out = [f"Title {title} § {sec}: heading \"{s['heading']}\"; status: {s['status'] or 'in force'}."]
    for d in range(1, len(subs) + 1):
        key = "s" + "/".join([sec, *subs[:d]])
        parent = "s" + "/".join([sec, *subs[:d - 1]])
        if key not in prov:
            kids = sorted(k[len(parent) + 1:] for k in prov if k.startswith(parent + "/") and k.count("/") == parent.count("/") + 1)
            out.append(f"It has no provision {'/'.join(subs[:d])}. Provisions at that level: {', '.join(kids[:30]) or 'none'}.")
            break
        out.append(f"Provision {'/'.join(subs[:d])}: status {prov[key]['status'] or 'in force'}.")
    return " ".join(out)


def main():
    prov = {t: {} for t in ("12", "15", "31")}
    for t in prov:
        for line in open(f"results/usc{t}-provisions-{RP}.jsonl"):
            p = json.loads(line)
            prov[t].setdefault(p["path"], p)
    broken = []
    for t in ("12", "31"):
        for line in open(f"results/banking-usc-2025-title-{t}.jsonl"):
            r = json.loads(line)
            if r["outcome"] not in ("resolves", "title-not-held", "appendix"):
                broken.append({**r, "cfr_title": t})
    sample = random.Random(SEED).sample(broken, N)
    texts = {}
    for t in ("12", "31"):
        for s in distinct_sections(Path(f"data/banking/CFR-2025-title-{t}.zip")):
            texts[(t, s["volume_file"], s["ordinal"])] = usc_cites.normalize(s["text"])
    OUT.mkdir(exist_ok=True)
    packet, key = [], []
    for i, r in enumerate(sample, 1):
        text = texts[(r["cfr_title"], r["volume_file"], r["ordinal"])]
        a, b = r["span"]
        item = f"item-{i:02d}"
        packet.append({"item": item, "cfr": f"{r['cfr_title']} CFR {r['sectno']} (2025)",
                       "excerpt": text[max(0, a - 300):b + 200], "citation_as_read": text[a:b],
                       "cited": f"{r['title']} U.S.C. {r['path']}",
                       "statute_record": record(r["title"], r["path"], prov[r["title"]])})
        key.append({"item": item, "outcome": r["outcome"], **{k: r[k] for k in ("sectno", "title", "path", "span")}})
    (OUT / "packet.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in packet))
    (OUT / "key.jsonl").write_text("".join(json.dumps(x) + "\n" for x in key))
    print(len(broken), "broken; packet", len(packet))


if __name__ == "__main__":
    main()
