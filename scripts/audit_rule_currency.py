"""Blind audit of the rule-currency lens (predictions R8, R9).

    uv run python scripts/audit_rule_currency.py sample     # writes the readers' packet (no labels)
    uv run python scripts/audit_rule_currency.py score      # after both readers have answered

`sample` draws up to 15 citations per Qwen label (seed = lens version - 1), shuffles them, and writes
results/rule-currency-audit-v<N>-902-packet.jsonl: item id and excerpt only. The key that
maps items to Qwen labels goes to a separate file, which the readers are never shown.
Each reader writes results/rule-currency-audit-v1-902-<reader>.jsonl with
{"item", "label", "decisive_text"}. `score` reports reader-reader agreement, the
consensus (items where both readers agree), and consensus-Qwen agreement, with a confusion
table.
"""

import json
import random
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import measure_rule_currency_qwen as m  # noqa: E402

from levadura_salvaje.lenses import rule_currency as rc  # noqa: E402

PER_LABEL = 15
V = rc.LENS_VERSION
SEED = int(V) - 1   # v1: seed 0; v2: seed 1, a fresh sample
PACKET = Path(f"results/rule-currency-audit-v{V}-902-packet.jsonl")
KEY = Path(f"results/rule-currency-audit-v{V}-902-key.jsonl")
READERS = ("reader-a", "reader-b")


def sample() -> None:
    labels = {(r["volume_file"], r["ordinal"], r["index"]): r["label"]
              for r in map(json.loads, m.FINAL.read_text().splitlines())}
    items = m.items()
    rng = random.Random(SEED)
    chosen = []
    for lab in rc.LABELS:
        pool = [it for it in items if labels[(it["volume_file"], it["ordinal"], it["index"])] == lab]
        chosen += rng.sample(pool, min(PER_LABEL, len(pool)))
    rng.shuffle(chosen)
    packet, key = [], []
    for n, it in enumerate(chosen, 1):
        item = f"item-{n:02d}"
        packet.append({"item": item, "excerpt": it["excerpt"]})
        key.append({"item": item, "key": it["key"], "sectno": it["sectno"], "index": it["index"],
                    "qwen": labels[(it["volume_file"], it["ordinal"], it["index"])]})
    PACKET.write_text("".join(json.dumps(p, ensure_ascii=False) + "\n" for p in packet))
    KEY.write_text("".join(json.dumps(k) + "\n" for k in key))
    print(f"{len(packet)} items -> {PACKET}; key -> {KEY}; per label: {Counter(k['qwen'] for k in key)}")


def score() -> None:
    key = {k["item"]: k for k in map(json.loads, KEY.read_text().splitlines())}
    reads = {r: {x["item"]: x["label"] for x in map(json.loads, Path(
        f"results/rule-currency-audit-v{V}-902-{r}.jsonl").read_text().splitlines())} for r in READERS}
    a, b = (reads[r] for r in READERS)
    items = sorted(key)
    missing = [i for i in items if i not in a or i not in b]
    if missing:
        sys.exit(f"missing answers: {missing}")
    rr = sum(a[i] == b[i] for i in items)
    consensus = [i for i in items if a[i] == b[i]]
    cq = sum(a[i] == key[i]["qwen"] for i in consensus)
    print(json.dumps({
        "items": len(items), "reader_agreement": [rr, len(items)],
        "consensus_items": len(consensus), "consensus_agrees_with_qwen": [cq, len(consensus)],
        "confusion_consensus_vs_qwen": dict(Counter(f"{a[i]}|{key[i]['qwen']}" for i in consensus)),
        "disagreements": [{"item": i, "sectno": key[i]["sectno"], "index": key[i]["index"], "a": a[i],
                           "b": b[i], "qwen": key[i]["qwen"]} for i in items if a[i] != b[i]],
    }, indent=1))


if __name__ == "__main__":
    {"sample": sample, "score": score}[sys.argv[1]]()
