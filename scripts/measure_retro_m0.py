"""Retrospective forecast, Stage 1, arm M0 (docs/retrospective-design.md, draft 3;
predictions/2026-09-28-retrospective-claude.md R6-R8).

Each cohort section's score is its per-byte surprise under the two mini-AGI
readers of the fold that held it out (scripts/retro_m0.sh), averaged over the
seeds. No fitted mapping; directions fixed in the design: higher surprise ->
absent, and among present sections lower surprise -> broken. Reports AUCs per
1997 stratum with section and cluster bootstraps, AUC within length
quintiles, and per fold x seed AUCs for training variation.

Usage: uv run --group retro python scripts/measure_retro_m0.py [--record]
"""

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from sklearn.metrics import roc_auc_score

from levadura_salvaje.ledger import append

sys.path.insert(0, str(Path(__file__).parent))
from measure_retro_b1 import CIT_1997, FEATURES, LABELS, auc_ci  # noqa: E402

RUNS = Path("data/retro/runs")
FOLDS, SEEDS = 5, 2


def main() -> None:
    feats = {(r["volume_file"], r["ordinal"]): r
             for r in map(json.loads, FEATURES.read_text().splitlines())}
    labels = {r["sectno"]: r["status_2025"] for r in map(json.loads, LABELS.read_text().splitlines())}
    cited = {}
    for r in map(json.loads, CIT_1997.read_text().splitlines()):
        heads = Counter(c["path"].split("/")[0] for c in r["citations"] if c.get("path"))
        cited[r["sectno"]] = heads.most_common(1)[0][0] if heads else "none"
    scores, reads, files = {}, {}, {}
    for k in range(FOLDS):
        for s in range(SEEDS):
            f = RUNS / f"fold{k}-seed{s}.scores.jsonl"
            files[str(f)] = hashlib.sha256(f.read_bytes()).hexdigest()
            for r in map(json.loads, f.read_text().splitlines()):
                scores.setdefault((r["volume_file"], r["ordinal"]), {})[(k, s)] = r["nats_per_byte"]
                reads[(k, s)] = r["weights_read_chars"]
    assert len(scores) == len(feats) and all(len(v) == SEEDS for v in scores.values())

    value = {"reader_chars": {f"fold{k}-seed{s}": c for (k, s), c in sorted(reads.items())}}
    for stratum, is_fossil in (("fossil", True), ("non_fossil", False)):
        keys = [key for key, f in feats.items() if f["fossil_1997"] is is_fossil]
        y = np.array([labels[feats[key]["sectno"]] for key in keys])
        m = np.array([np.mean(list(scores[key].values())) for key in keys])
        clusters = np.array([cited.get(feats[key]["sectno"], "none") for key in keys])
        length = np.array([feats[key]["log_chars"] for key in keys])
        absent = (y == "absent").astype(int)
        present = y != "absent"
        broken = (y[present] == "present-broken").astype(int)
        quint = np.digitize(length, np.quantile(length, [0.2, 0.4, 0.6, 0.8]))
        within = {}
        for q in range(5):
            i = quint == q
            if len(set(absent[i])) == 2:
                within[str(q)] = round(float(roc_auc_score(absent[i], m[i])), 4)
        per_run = []
        for k in range(FOLDS):
            for s in range(SEEDS):
                i = [j for j, key in enumerate(keys) if (k, s) in scores[key]]
                run = np.array([scores[keys[j]][(k, s)] for j in i])
                if len(set(absent[i])) == 2:
                    per_run.append(round(float(roc_auc_score(absent[i], run)), 4))
        value[stratum] = {
            "n": len(y),
            "R6_auc_absent_higher_surprise": auc_ci(absent, m, clusters),
            "R7_auc_broken_lower_surprise": auc_ci(broken, -m[present], clusters[present]),
            "auc_absent_within_length_quintiles": within,
            "auc_absent_per_fold_seed": per_run,
            "median_surprise": {c: round(float(np.median(m[y == c])), 4) for c in sorted(set(y))},
        }
    print(json.dumps(value, indent=1))
    if "--record" not in sys.argv:
        return
    rec = append({
        "observed_at": "2025-04-01",
        "observed_at_note": "2025 status of 1997 sections, forecast from 1997 text by readers of 1997 only",
        "instrument": {
            "name": "retrospective forecast M0 (mini-AGI surprise, trained on 1997 only)", "version": "1",
            "method": "mini-AGI (volotat/mini-AGI efd4a16) trained from scratch per fold on the 1997 CFR "
                      "minus the fold's cohort sections, 31 minutes on an RTX 4090, resident 16, context "
                      "2048, seeds 0-1; held-out sections scored with fresh context, no learning; "
                      "surprise averaged over seeds; fixed directions, no fitted mapping",
            "known_limits": "time budget, so readers differ in characters read (see reader_chars); "
                            "labels are extractor statuses; exploratory",
            "predictions": "predictions/2026-09-28-retrospective-claude.md",
            "scripts": ["scripts/retro_m0_folds.py", "scripts/retro_m0.sh", "scripts/minagi_score.py",
                        "scripts/measure_retro_m0.py"],
        },
        "population": {"score_files": files,
                       "folds": "results/retro-m0-folds-v1.json",
                       "labels_sha256": hashlib.sha256(LABELS.read_bytes()).hexdigest()},
        "quantity": "retrospective_forecast_m0",
        "value": value,
        "derived_from": ["obs-0139", "obs-0129", "obs-0141", "obs-0150"],
    })
    print(rec["id"])


if __name__ == "__main__":
    main()
