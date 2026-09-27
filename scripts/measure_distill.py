"""Distill Jev's section labels into a fastText student (predictions/2026-09-26-jev-distill-claude.md).

For each lens (dated, currency): 5-fold stratified cross-validation of a
fastText classifier trained on Jev's labels, with hyperparameters fixed in the
predictions. Reports agreement, Cohen's kappa, per-class recall, the majority
baseline and the confidence cascade. With ``--record`` it appends one ledger
entry and writes out-of-fold predictions to results/.

Usage: uv run --group distill python scripts/measure_distill.py [--record]
"""

import hashlib
import json
import random
import re
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

import fasttext

from levadura_salvaje.ledger import append
from levadura_salvaje.sections import sections

LENSES = {"dated": ("results/dated-jev-v1-2025.jsonl", "obs-0135"),
          "currency": ("results/currency-jev-v1-2025.jsonl", "obs-0132")}
PARAMS = dict(epoch=25, lr=0.5, wordNgrams=2, dim=50, minCount=1, loss="softmax",
              seed=0, thread=1, verbose=0)
FOLDS = 5
TARGET = 0.95


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def texts() -> dict:
    return {(s["volume_file"], s["ordinal"]): s
            for s in sections(Path("data/cfr/CFR-2025-title-26.zip"))}


def folds(labels: list[str]) -> list[int]:
    """Stratified fold number per item, seed 0."""
    rng = random.Random(0)
    fold = [0] * len(labels)
    by = defaultdict(list)
    for i, y in enumerate(labels):
        by[y].append(i)
    for y in sorted(by):
        idx = by[y]
        rng.shuffle(idx)
        for k, i in enumerate(idx):
            fold[i] = k % FOLDS
    return fold


def train(docs: list[str], labels: list[str]):
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        f.writelines(f"__label__{y} {d}\n" for d, y in zip(docs, labels))
    model = fasttext.train_supervised(f.name, **PARAMS)
    Path(f.name).unlink()
    return model


def predict(model, doc: str) -> tuple[str, float]:
    (lab,), (p,) = model.predict(doc, k=1)
    return lab.removeprefix("__label__"), float(min(p, 1.0))


def kappa(y: list[str], p: list[str]) -> float:
    n = len(y)
    po = sum(a == b for a, b in zip(y, p)) / n
    cy, cp = Counter(y), Counter(p)
    pe = sum(cy[k] * cp[k] for k in cy) / n / n
    return (po - pe) / (1 - pe)


def cascade(y, p, conf) -> dict:
    order = sorted(range(len(y)), key=lambda i: -conf[i])
    best, agree = 0, 0
    curve = {}
    for k, i in enumerate(order, 1):
        agree += y[i] == p[i]
        if agree / k >= TARGET:
            best = k
        for share in (0.25, 0.5, 0.75, 1.0):
            if k == round(share * len(y)):
                curve[str(share)] = round(agree / k, 4)
    return {"keep_share_at_target": round(best / len(y), 4), "kept": best,
            "agreement_by_kept_share": curve}


def run_lens(name: str, path: str, secs: dict) -> tuple[dict, list[dict], list[str], list[str]]:
    rows = [json.loads(line) for line in Path(path).read_text().splitlines()]
    docs = [normalize(secs[(r["volume_file"], r["ordinal"])]["text"]) for r in rows]
    y = [r["label"] for r in rows]
    fold = folds(y)
    p, conf = [None] * len(y), [0.0] * len(y)
    for k in range(FOLDS):
        tr = [i for i in range(len(y)) if fold[i] != k]
        model = train([docs[i] for i in tr], [y[i] for i in tr])
        for i in range(len(y)):
            if fold[i] == k:
                p[i], conf[i] = predict(model, docs[i])
    counts = Counter(y)
    majority = counts.most_common(1)[0]
    result = {
        "n": len(y), "jev_labels": dict(counts),
        "agreement": round(sum(a == b for a, b in zip(y, p)) / len(y), 4),
        "kappa": round(kappa(y, p), 4),
        "majority_baseline": round(majority[1] / len(y), 4),
        "recall_vs_jev": {c: round(sum(a == b == c for a, b in zip(y, p)) / counts[c], 4)
                          for c in sorted(counts)},
        "confusion": {f"{a}->{b}": n for (a, b), n in sorted(Counter(zip(y, p)).items())},
        "cascade": cascade(y, p, conf),
        "duplicate_texts": len(docs) - len(set(docs)),
    }
    oof = [{"volume_file": r["volume_file"], "ordinal": r["ordinal"], "sectno": r["sectno"],
            "jev": a, "student": b, "confidence": round(c, 4), "fold": f}
           for r, a, b, c, f in zip(rows, y, p, conf, fold)]
    return result, oof, docs, y


def main() -> None:
    secs = texts()
    value, outs = {}, {}
    for name, (path, _) in LENSES.items():
        value[name], outs[name], docs, y = run_lens(name, path, secs)
        print(name, json.dumps(value[name], indent=1))
        if "--model" in sys.argv:  # full-data student for the deployment check
            train(docs, y).save_model(f"results/distill-v1-{name}.bin")
    if "--record" not in sys.argv:
        return
    files = {}
    for name, rows in outs.items():
        out = Path(f"results/distill-v1-{name}-2025.jsonl")
        out.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in rows))
        files[str(out)] = hashlib.sha256(out.read_bytes()).hexdigest()
    rec = append({
        "observed_at": "2025-04-01",
        "observed_at_note": "2025 CFR sections, as labeled by Jev on 2026-09-24",
        "instrument": {
            "name": "fastText student of Jev (5-fold cross-validated)", "version": "1",
            "method": "fastText supervised on lowercased, whitespace-collapsed section text; "
                      f"fixed parameters {json.dumps({k: v for k, v in PARAMS.items() if k != 'verbose'})}; "
                      "stratified 5-fold, seed 0; out-of-fold predictions compared with Jev",
            "known_limits": "cascade share is chosen on the same out-of-fold predictions, so "
                            "it is optimistic; one corpus, one edition; the teacher's own noise "
                            "floor (obs-0122) is not subtracted",
            "predictions": "predictions/2026-09-26-jev-distill-claude.md",
            "scripts": ["scripts/measure_distill.py"],
        },
        "population": {"edition": "2025", "sections": value["dated"]["n"],
                       "results_files": files, "fasttext": fasttext.__name__ + "-wheel 0.9.2"},
        "quantity": "jev_distillation_agreement",
        "value": value,
        "derived_from": [ref for _, ref in LENSES.values()],
    })
    print(rec["id"])


if __name__ == "__main__":
    main()
