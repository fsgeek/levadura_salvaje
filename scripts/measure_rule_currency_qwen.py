"""The rule-currency lens (lenses/rule_currency.py) over every citation of one Code section, by Qwen.

Predictions: predictions/2026-10-02-rule-currency-claude.md (written before any call).
Population: every citation of section TARGET in results/cfr-usc-citations-v2-2025.jsonl,
whose spans index citations.normalize(section text); each section's text must hash to the
row's sha256 or the run stops. One question per citation, about the rule that citation sits
in. Qwen3.8-27B (Q4_K_M) on our own llama-server under an ayllu-gpu lease; temperature 0,
JSON-schema-constrained label, thinking off.

Calls are appended to a partial file as they complete; rerun to resume. The ledger entry
is written only when every citation is answered, by `record`, outside the lease.

    scripts/qwen_under_lease.sh 1h "rule-currency lens: 548 citations of section 902" \\
        uv run python scripts/measure_rule_currency_qwen.py http://127.0.0.1:8091
    uv run python scripts/measure_rule_currency_qwen.py record
"""

import hashlib
import json
import sys
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from levadura_salvaje.citations import normalize
from levadura_salvaje.ledger import append, verify
from levadura_salvaje.lenses import rule_currency as rc
from levadura_salvaje.sections import sections

TARGET = "902"
MODEL = "qwen3.8-27b-q4km"
GGUF = "/home/tony/models/Qwen3.8-27B-GGUF/Qwen3.8-27B-Q4_K_M.gguf"
CIT = Path("results/cfr-usc-citations-v2-2025.jsonl")
CIT_SHA256 = "8c8d2c257f79c26355e651d899c4a932bb0927646ef99f4ca68d1742a39308c9"
ZIP = Path("data/cfr/CFR-2025-title-26.zip")
PARTIAL = Path(f"results/rule-currency-qwen-v{rc.LENS_VERSION}-{TARGET}-2025.partial.jsonl")
FINAL = Path(f"results/rule-currency-qwen-v{rc.LENS_VERSION}-{TARGET}-2025.jsonl")
WORKERS = 2


def items() -> list[dict]:
    """One item per citation of TARGET, with its excerpt. Refuses a sidecar or text that has moved."""
    data = CIT.read_bytes()
    if hashlib.sha256(data).hexdigest() != CIT_SHA256:
        sys.exit(f"{CIT} is not the pinned citations file")
    rows = {(r["volume_file"], r["ordinal"]): r for r in map(json.loads, data.decode().splitlines())}
    out = []
    for s in sections(ZIP):
        r = rows.get((s["volume_file"], s["ordinal"]))
        if r is None:
            continue
        cits = [(i, c) for i, c in enumerate(r["citations"])
                if c.get("path") and c["path"].split("/")[0] == TARGET and c.get("span")]
        if not cits:
            continue
        if s["sha256"] != r["sha256"]:
            sys.exit(f"{s['sectno']}: text does not hash to the citations row")
        norm = normalize(s["text"])
        for i, c in cits:
            a, b = c["span"]
            if c["head"] == "section" and TARGET not in norm[a:b]:
                sys.exit(f"{s['sectno']}#{i}: span does not cover the citation")
            text = rc.excerpt(norm, (a, b), s["sectno"], s["subject"])
            out.append({"key": f"{s['volume_file']}#{s['ordinal']}#{s['sha256']}#{i}",
                        "volume_file": s["volume_file"], "ordinal": s["ordinal"], "sectno": s["sectno"],
                        "sha256": s["sha256"], "index": i, "path": c["path"], "head": c["head"],
                        "span": [a, b], "excerpt": text})
    return out


def ask(base: str, text: str) -> dict:
    body = {
        "model": MODEL, "temperature": 0, "max_tokens": 20,
        "messages": [{"role": "system", "content": rc.PROMPT}, {"role": "user", "content": text}],
        "response_format": {"type": "json_schema", "json_schema": {"name": "label", "schema": {
            "type": "object", "properties": {"label": {"type": "string", "enum": list(rc.LABELS)}},
            "required": ["label"]}}},
        "chat_template_kwargs": {"enable_thinking": False},
    }
    req = urllib.request.Request(f"{base}/chat/completions", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        out = json.load(r)
    content = out["choices"][0]["message"]["content"]
    return {"label": json.loads(content)["label"], "raw": content,
            "input_tokens": out.get("usage", {}).get("prompt_tokens"), "model_reported": out.get("model")}


def main() -> None:
    base = sys.argv[1].rstrip("/") + "/v1"
    todo_all = items()
    done = {}
    if PARTIAL.exists():
        for line in PARTIAL.read_text().splitlines():
            row = json.loads(line)
            done[row["key"]] = row
    todo = [it for it in todo_all if it["key"] not in done]
    print(f"{len(todo_all)} citations, {len(todo)} to ask ({len(done)} answered)", flush=True)
    failed = 0
    with PARTIAL.open("a") as out, ThreadPoolExecutor(WORKERS) as pool:
        futures = {pool.submit(ask, base, it["excerpt"]): it for it in todo}
        for n, fut in enumerate(as_completed(futures), 1):
            it = futures[fut]
            try:
                row = {"key": it["key"], "excerpt_sha256": hashlib.sha256(it["excerpt"].encode()).hexdigest(),
                       **fut.result()}
            except Exception as e:  # retried on the next run
                failed += 1
                print(f"FAILED {it['key']}: {type(e).__name__}: {e}", flush=True)
                continue
            done[it["key"]] = row
            out.write(json.dumps(row, sort_keys=True) + "\n")
            out.flush()
            if n % 50 == 0:
                print(f"  {n}/{len(todo)}", flush=True)
    if failed:
        sys.exit(f"{failed} citations failed; rerun to resume. Nothing written.")
    rows = []
    for it in todo_all:
        d = done[it["key"]]
        if d["excerpt_sha256"] != hashlib.sha256(it["excerpt"].encode()).hexdigest():
            sys.exit(f"{it['key']}: the partial answer was for a different excerpt")
        rows.append({k: it[k] for k in ("volume_file", "ordinal", "sectno", "sha256", "index", "path", "head", "span")}
                    | {"label": d["label"], "excerpt_sha256": d["excerpt_sha256"]})
    FINAL.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in rows))
    print(f"wrote {FINAL} ({len(rows)} rows); record it with: uv run python {sys.argv[0]} record")


def record() -> None:
    rows = [json.loads(l) for l in FINAL.read_text().splitlines()]
    by_sec: dict[str, Counter] = {}
    for r in rows:
        by_sec.setdefault(r["sectno"], Counter())[r["label"]] += 1
    rec = append({
        "observed_at": "2025-04-01",
        "observed_at_note": "2025 CFR edition; citations of section 902, all repealed at 119-4",
        "instrument": {
            "name": "scripts/measure_rule_currency_qwen.py", "version": "1", "model": MODEL, "gguf": GGUF,
            "server": "llama.cpp llama-server, own instance under an ayllu-gpu lease (holder levadura-salvaje)",
            "lens": f"levadura_salvaje.lenses.rule_currency v{rc.LENS_VERSION}",
            "prompt_sha256": hashlib.sha256(rc.PROMPT.encode()).hexdigest(),
            "method": f"one question per citation of section {TARGET}, excerpt of the normalized text "
                      f"({rc.BEFORE} before, {rc.AFTER} after, citation marked); JSON-schema label; temperature 0; "
                      "thinking off",
            "known_limits": "excerpt may cut off a limit stated elsewhere in the section; one judge; text, not law",
            "predictions": "predictions/2026-10-02-rule-currency-claude.md",
        },
        "population": {"edition": "2025", "target": TARGET, "citations_file": str(CIT),
                       "citations_sha256": CIT_SHA256, "results_file": str(FINAL),
                       "results_sha256": hashlib.sha256(FINAL.read_bytes()).hexdigest(),
                       "partial_sha256": hashlib.sha256(PARTIAL.read_bytes()).hexdigest()},
        "quantity": "rule_currency_citation_labels_qwen",
        "value": {"citations": len(rows), "sections": len(by_sec),
                  "labels": dict(Counter(r["label"] for r in rows)),
                  "sections_with_no_untimed_citation": sum(1 for c in by_sec.values() if not c["untimed"])},
        "derived_from": ["obs-0132", "obs-0146"],
    })
    print(rec["id"], json.dumps(rec["value"], indent=1))
    print("ledger verified:", verify())


if __name__ == "__main__":
    record() if sys.argv[1:] == ["record"] else main()
