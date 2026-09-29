"""Retrospective forecast, Stage 1, arm B1 (docs/retrospective-design.md, draft 3;
predictions/2026-09-28-retrospective-claude.md R1-R5).

Multinomial logistic regression on allowlisted 1997 features, one model per
1997 stratum, 5-fold cross-validated (stratified by 2025 status, seed 0).
B0 is each training fold's class prevalence. Reports AUCs with a section
bootstrap and a cluster bootstrap (cluster = the section's most-cited Code
section in 1997), log loss against B0, the no-part ablation and onset.

Usage: uv run --group retro python scripts/measure_retro_b1.py [--record]
"""

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss, roc_auc_score
from sklearn.model_selection import StratifiedKFold

from levadura_salvaje.ledger import append

FEATURES = Path("results/retro-features-v1-1997.jsonl")
LABELS = Path("results/retro-labels-v1.jsonl")
CIT_1997 = Path("results/cfr-usc-citations-v2-1997.jsonl")
CLASSES = ["absent", "present-broken", "present-clean"]
BOOT = 1000


def design(rows: list[dict], parts: list[str], use_part: bool, fill: float) -> np.ndarray:
    cols = []
    for r in rows:
        year = r["last_fr_year"]
        x = [r["broken"], r["broken_share"], r["citations"], r["log_chars"],
             (year if year is not None else fill), float(year is None)]
        if use_part:
            x += [float(r["part"] == p) for p in parts]
        cols.append(x)
    return np.array(cols, dtype=float)


def oof(rows: list[dict], y: np.ndarray, use_part: bool) -> tuple[np.ndarray, np.ndarray]:
    """Out-of-fold class probabilities for B1 and B0, columns in CLASSES order."""
    p1, p0 = np.zeros((len(y), 3)), np.zeros((len(y), 3))
    for tr, te in StratifiedKFold(5, shuffle=True, random_state=0).split(np.zeros(len(y)), y):
        train = [rows[i] for i in tr]
        parts = sorted({r["part"] for r in train})
        years = [r["last_fr_year"] for r in train if r["last_fr_year"] is not None]
        fill = float(np.median(years))
        xtr = design(train, parts, use_part, fill)
        xte = design([rows[i] for i in te], parts, use_part, fill)
        mu, sd = xtr.mean(0), xtr.std(0) + 1e-9
        m = LogisticRegression(max_iter=5000).fit((xtr - mu) / sd, y[tr])
        probs = m.predict_proba((xte - mu) / sd)
        for k, c in enumerate(m.classes_):
            p1[te, CLASSES.index(c)] = probs[:, k]
        prev = Counter(y[tr])
        p0[te] = [(prev[c] + 0.5) / (len(tr) + 1.5) for c in CLASSES]
    return p1, p0


def auc_ci(y01: np.ndarray, score: np.ndarray, clusters: np.ndarray) -> dict:
    rng = np.random.default_rng(0)
    point = roc_auc_score(y01, score)
    sect, clus = [], []
    ids = np.unique(clusters)
    members = {c: np.where(clusters == c)[0] for c in ids}
    for _ in range(BOOT):
        i = rng.integers(0, len(y01), len(y01))
        if len(set(y01[i])) == 2:
            sect.append(roc_auc_score(y01[i], score[i]))
        j = np.concatenate([members[c] for c in rng.choice(ids, len(ids))])
        if len(set(y01[j])) == 2:
            clus.append(roc_auc_score(y01[j], score[j]))
    q = lambda v: [round(float(np.percentile(v, 2.5)), 4), round(float(np.percentile(v, 97.5)), 4)]
    return {"auc": round(float(point), 4), "ci_sections": q(sect), "ci_clusters": q(clus)}


def main() -> None:
    feats = [json.loads(line) for line in FEATURES.read_text().splitlines()]
    labels = {r["sectno"]: r["status_2025"]
              for r in map(json.loads, LABELS.read_text().splitlines())}
    cited = {}
    for r in map(json.loads, CIT_1997.read_text().splitlines()):
        heads = Counter(c["path"].split("/")[0] for c in r["citations"] if c.get("path"))
        cited[r["sectno"]] = heads.most_common(1)[0][0] if heads else "none"
    value = {}
    for stratum, is_fossil in (("fossil", True), ("non_fossil", False)):
        rows = [r for r in feats if r["fossil_1997"] is is_fossil]
        y = np.array([labels[r["sectno"]] for r in rows])
        clusters = np.array([cited.get(r["sectno"], "none") for r in rows])
        absent = (y == "absent").astype(int)
        p1, p0 = oof(rows, y, use_part=True)
        p1_np, _ = oof(rows, y, use_part=False)
        present = y != "absent"
        broken = (y[present] == "present-broken").astype(int)
        onset_score = p1[present, 1] / (p1[present, 1] + p1[present, 2])
        value[stratum] = {
            "n": len(y), "status": dict(Counter(y)),
            "clusters": int(len(np.unique(clusters))),
            "R1_R2_auc_absent": auc_ci(absent, p1[:, 0], clusters),
            "R3_log_loss": {"B1": round(log_loss(y, p1, labels=CLASSES), 4),
                            "B0": round(log_loss(y, p0, labels=CLASSES), 4)},
            "R4_auc_absent_no_part": auc_ci(absent, p1_np[:, 0], clusters),
            "R5_auc_broken_vs_clean_present": auc_ci(broken, onset_score, clusters[present]),
        }
    print(json.dumps(value, indent=1))
    if "--record" not in sys.argv:
        return
    rec = append({
        "observed_at": "2025-04-01",
        "observed_at_note": "2025 status of 1997 sections, forecast from 1997 inputs",
        "instrument": {
            "name": "retrospective forecast B1 (logistic regression on 1997 features)", "version": "1",
            "method": "per-stratum multinomial logistic regression (sklearn defaults, standardized), "
                      "5-fold stratified CV seed 0; features broken, broken_share, citations, log_chars, "
                      "last_fr_year (+missing indicator), part one-hot; bootstrap 1000 over sections "
                      "and over most-cited-Code-section clusters",
            "known_limits": "retrospective supervised prediction: the model learns other 1997 sections' "
                            "2025 outcomes; statuses are extractor outcomes, not adjudicated decay; "
                            "exploratory (designer had seen turnover counts)",
            "predictions": "predictions/2026-09-28-retrospective-claude.md",
            "scripts": ["scripts/retro_build.py", "scripts/measure_retro_b1.py"],
        },
        "population": {"features": str(FEATURES),
                       "features_sha256": hashlib.sha256(FEATURES.read_bytes()).hexdigest(),
                       "labels": str(LABELS),
                       "labels_sha256": hashlib.sha256(LABELS.read_bytes()).hexdigest()},
        "quantity": "retrospective_forecast_b1",
        "value": value,
        "derived_from": ["obs-0139", "obs-0129", "obs-0141"],
    })
    print(rec["id"])


if __name__ == "__main__":
    main()
