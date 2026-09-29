"""Fold corpora for the retrospective forecast's M0 arm (docs/retrospective-design.md, draft 3).

Cohort sections (retro-labels-v1) are split into 5 folds, stratified by
1997 stratum x 2025 status (seed 0); the cohort has no duplicate texts.
Fold k's reader trains on every 1997 section except fold k's cohort
sections, minus a 2% seeded validation slice; sections outside the cohort
(repeated numbers) are always training text. Writes the corpora to
data/retro/fold{k}/{train,val}/cfr1997/<volume>.txt in the form the obs-0147
corpus used, plus results/retro-m0-folds-v1.json (membership).

Usage: uv run --group retro python scripts/retro_m0_folds.py
"""

import json
import random
from collections import defaultdict
from pathlib import Path

import numpy as np
from sklearn.model_selection import StratifiedKFold

from levadura_salvaje.sections import sections

FOLDS = 5


def main() -> None:
    feats = {r["sectno"]: r for r in map(json.loads, Path("results/retro-features-v1-1997.jsonl").read_text().splitlines())}
    labels = [json.loads(line) for line in Path("results/retro-labels-v1.jsonl").read_text().splitlines()]
    strata = [f"{feats[r['sectno']]['fossil_1997']}|{r['status_2025']}" for r in labels]
    fold_of = {}
    for k, (_, te) in enumerate(StratifiedKFold(FOLDS, shuffle=True, random_state=0)
                                .split(np.zeros(len(labels)), strata)):
        for i in te:
            f = feats[labels[i]["sectno"]]
            fold_of[(f["volume_file"], f["ordinal"])] = k
    secs = list(sections(Path("data/cfr/CFR-1997-title-26.zip")))
    for k in range(FOLDS):
        rng = random.Random(f"retro-m0-fold{k}")
        out = defaultdict(lambda: defaultdict(list))
        for s in secs:
            key = (s["volume_file"], s["ordinal"])
            if fold_of.get(key) == k:
                continue
            split = "val" if rng.random() < 0.02 else "train"
            out[split][s["volume_file"]].append(f"§ {s['sectno']} {s['subject']}\n{s['text']}\n\n")
        for split, vols in out.items():
            d = Path(f"data/retro/fold{k}/{split}/cfr1997")
            d.mkdir(parents=True, exist_ok=True)
            for vol, parts in vols.items():
                (d / vol.replace(".xml", ".txt")).write_text("".join(parts))
        print(k, {split: sum(len(p) for v in vols.values() for p in v) for split, vols in out.items()})
    Path("results/retro-m0-folds-v1.json").write_text(json.dumps(
        [{"volume_file": v, "ordinal": o, "fold": k} for (v, o), k in sorted(fold_of.items())], indent=0))


if __name__ == "__main__":
    main()
