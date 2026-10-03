"""Blind audit of the rule-currency lens (predictions R8, R9).

    uv run python scripts/audit_rule_currency.py sample     # writes the readers' packet (no labels)
    uv run python scripts/audit_rule_currency.py score      # after both readers have answered
    uv run python scripts/audit_rule_currency.py adjust     # population shares under each disagreement rule

`sample` draws up to 15 citations per Qwen label (seed = lens version - 1), shuffles them, and writes
results/rule-currency-audit-v<N>-902-packet.jsonl: item id and excerpt only. The key that
maps items to Qwen labels goes to a separate file, which the readers are never shown.
Each reader writes results/rule-currency-audit-v<N>-902-<reader>.jsonl with
{"item", "label", "decisive_text"}. `score` reports reader-reader agreement, the
consensus (items where both readers agree), and consensus-Qwen agreement, with a confusion
table.
"""

import hashlib
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
# Fixed probes added to a version's sample (keys from measure_rule_currency_qwen.items()); marked in the key
# file, not in the packet. v3: the 1.902-3 ownership exception both v2 readers mislabelled (v2 item 21).
PROBES = {"3": ["CFR-2025-title26-vol11.xml#211#aaf2466f59ad66b3e0b1ed73563d27458a2c0b795761d9896754bdafecb8f0b2#49"]}


def sample() -> None:
    labels = {(r["volume_file"], r["ordinal"], r["index"]): r["label"]
              for r in map(json.loads, m.FINAL.read_text().splitlines())}
    items = m.items()
    rng = random.Random(SEED)
    chosen = []
    for lab in rc.LABELS:
        pool = [it for it in items if labels[(it["volume_file"], it["ordinal"], it["index"])] == lab]
        chosen += rng.sample(pool, min(PER_LABEL, len(pool)))
    probes = set(PROBES.get(V, []))
    chosen += [it for it in items if it["key"] in probes and it["key"] not in {c["key"] for c in chosen}]
    rng.shuffle(chosen)
    packet, key = [], []
    for n, it in enumerate(chosen, 1):
        item = f"item-{n:02d}"
        packet.append({"item": item, "excerpt": it["excerpt"]})
        key.append({"item": item, "key": it["key"], "sectno": it["sectno"], "index": it["index"],
                    "qwen": labels[(it["volume_file"], it["ordinal"], it["index"])],
                    "probe": it["key"] in probes})
    PACKET.write_text("".join(json.dumps(p, ensure_ascii=False) + "\n" for p in packet))
    KEY.write_text("".join(json.dumps(k) + "\n" for k in key))
    print(f"{len(packet)} items -> {PACKET}; key -> {KEY}; per label: {Counter(k['qwen'] for k in key)}")


def _answers(reader: str, items: set[str]) -> dict[str, str]:
    """A reader's answers, refused unless they cover exactly the packet's items, once each, with valid
    labels (review 1, #8)."""
    rows = [json.loads(l) for l in Path(f"results/rule-currency-audit-v{V}-902-{reader}.jsonl").read_text().splitlines()]
    ids = [r["item"] for r in rows]
    if len(ids) != len(set(ids)):
        sys.exit(f"{reader}: duplicate items")
    if set(ids) != items:
        sys.exit(f"{reader}: answers do not match the packet ({len(items - set(ids))} missing, "
                 f"{len(set(ids) - items)} extra)")
    bad = [r["item"] for r in rows if r["label"] not in rc.LABELS]
    if bad:
        sys.exit(f"{reader}: invalid labels on {bad}")
    return {r["item"]: r["label"] for r in rows}


def _load():
    packet = [json.loads(l) for l in PACKET.read_text().splitlines()]
    key = {k["item"]: k for k in map(json.loads, KEY.read_text().splitlines())}
    if {p["item"] for p in packet} != set(key):
        sys.exit("packet and key disagree")
    a, b = (_answers(r, set(key)) for r in READERS)
    probes = {i: k for i, k in key.items() if k.get("probe")}
    sampled = {i: k for i, k in key.items() if not k.get("probe")}   # probes aren't a random draw
    return sampled, a, b, probes


def score() -> None:
    key, a, b, probes = _load()
    items = sorted(key)
    rr = sum(a[i] == b[i] for i in items)
    consensus = [i for i in items if a[i] == b[i]]
    cq = sum(a[i] == key[i]["qwen"] for i in consensus)
    print(json.dumps({
        "packet_sha256": hashlib.sha256(PACKET.read_bytes()).hexdigest(),
        "items": len(items), "reader_agreement": [rr, len(items)],
        "consensus_items": len(consensus), "consensus_agrees_with_qwen": [cq, len(consensus)],
        "confusion_consensus_vs_qwen": dict(Counter(f"{a[i]}|{key[i]['qwen']}" for i in consensus)),
        "disagreements": [{"item": i, "sectno": key[i]["sectno"], "index": key[i]["index"], "a": a[i],
                           "b": b[i], "qwen": key[i]["qwen"]} for i in items if a[i] != b[i]],
        "probes": [{"item": i, "sectno": k["sectno"], "index": k["index"], "a": a[i], "b": b[i],
                    "qwen": k["qwen"]} for i, k in sorted(probes.items())],
    }, indent=1))


def adjust() -> None:
    """Population shares re-estimated from the audit (review 1, #1, #2). Each Qwen stratum's population
    count is reallocated by the audit labels in that stratum, under several rules for the readers'
    disagreements:
    - consensus: agreed items only (assumes disagreements look like agreements: unsupported);
    - reader-a, reader-b: each reader's labels alone, all items;
    - range for label L: every disputed item counted as not-L, then as L (when either reader said L).
    The bootstrap resamples within strata, conditional on the consensus items: it reflects sampling of
    those items only, not the disagreements, shared reader errors or what the excerpt didn't show."""
    key, a, b, _ = _load()
    pop = Counter(r["label"] for r in map(json.loads, m.FINAL.read_text().splitlines()))
    n = sum(pop.values())

    def shares(label_of):
        out = Counter()
        for q in rc.LABELS:
            items = [i for i in key if key[i]["qwen"] == q and label_of(i) is not None]
            for t in rc.LABELS:
                out[t] += pop[q] * sum(label_of(i) == t for i in items) / len(items)
        return {t: round(100 * out[t] / n, 1) for t in rc.LABELS}

    res = {"consensus": shares(lambda i: a[i] if a[i] == b[i] else None),
           "reader-a": shares(lambda i: a[i]), "reader-b": shares(lambda i: b[i])}
    res["range"] = {}
    for t in rc.LABELS:
        lo = shares(lambda i: a[i] if a[i] == b[i] else "_other")[t]
        hi = shares(lambda i: a[i] if a[i] == b[i] else (t if t in (a[i], b[i]) else "_other"))[t]
        res["range"][t] = [lo, hi]
    rng = random.Random(0)
    strata = {q: [a[i] for i in key if key[i]["qwen"] == q and a[i] == b[i]] for q in rc.LABELS}
    boots = {t: [] for t in rc.LABELS}
    for _ in range(10000):
        st = {q: [rng.choice(v) for v in [strata[q]] for _ in v] for q in rc.LABELS}
        for t in rc.LABELS:
            boots[t].append(100 * sum(pop[q] * st[q].count(t) / len(st[q]) for q in rc.LABELS) / n)
    res["consensus_bootstrap_conditional_2.5_97.5"] = {
        t: [round(sorted(v)[250], 1), round(sorted(v)[9750], 1)] for t, v in boots.items()}
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    {"sample": sample, "score": score, "adjust": adjust}[sys.argv[1]]()
