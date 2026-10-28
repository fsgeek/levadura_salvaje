"""Build the two arms of the PTAB context test (predictions/2026-10-28-ptab-context-claude.md, stamped at 6cdbf74).

C0 (context-free): passages only. C1 (context-aware): the same passages plus the patent's grant date and the
pre-AIA rule. 73 bare decisions on pre-AIA patents plus 10 marked controls; order shuffled per arm; three
batches per arm. Keys are kept apart from packets.

Usage: uv run python scripts/build_ptab_context.py
"""

import json
import random
import re
from pathlib import Path

DIR = Path("data/ptab")
OUT = Path("results/ptab-audit-context")
CITE = re.compile(r"35\s+U\.\s?S\.\s?C\.")
RULE = ("This patent was granted before March 16, 2013, so it was examined under the pre-AIA versions of 35 U.S.C. "
        "102 and 103, and those versions govern its patentability.")


def passages(doc):
    t = re.sub(r"\s+", " ", (DIR / "txt" / f"{doc}.txt").read_text())
    return [t[max(0, a - 400):a + 400] for a in [m.start() for m in CITE.finditer(t)][:8]]


rows = [json.loads(x) for x in open("results/ptab-applicability.jsonl")]
pre = [r for r in rows if r["band"] == "pre" and not r["no_text"]]
bare = [r for r in pre if not r["marked"] and not r["old_subdivision"]]
ctrl = random.Random(20261028).sample([r for r in pre if r["marked"]], 10)
OUT.mkdir(exist_ok=True)
for arm, seed in (("c0", 1), ("c1", 2)):
    items = [(r, "bare") for r in bare] + [(r, "control") for r in ctrl]
    random.Random(20261028 + seed).shuffle(items)
    packet, key = [], []
    for i, (r, kind) in enumerate(items, 1):
        item = {"item": f"{arm}-{i:02d}", "passages": passages(r["doc"])}
        if arm == "c1":
            item = {"item": item["item"], "patent_granted": r["grant"], "rule": RULE, "passages": item["passages"]}
        packet.append(item)
        key.append({"item": f"{arm}-{i:02d}", "kind": kind, "doc": r["doc"], "grant": r["grant"]})
    for b in range(3):
        chunk = packet[b::3]
        (OUT / f"{arm}-batch-{b}.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in chunk))
    (OUT / f"{arm}-key.jsonl").write_text("".join(json.dumps(x) + "\n" for x in key))
print(len(bare), "bare,", len(ctrl), "controls")
