"""Second judge for the currency lens: local Qwen, same question, same chunks (C7).

Asks Qwen3.8-27B (Q4_K_M, llama.cpp llama-server, our own instance under an
ayllu-gpu lease; never the resident's server on 8081) the frozen currency
lens question (lenses/currency.py, instructions and criteria rendered as a
prompt) about exactly the chunks Jev saw: each section is split at the
budget recorded in results/currency-jev-v1-2025.jsonl. The output is
constrained by JSON schema to one of the three labels. Thinking is off and
temperature is 0. Section label = strongest chunk label, as for Jev.

Calls are appended to a partial file as they complete, so a lease that ends
mid-run loses nothing; rerun to resume. The ledger entry is written only
when every chunk is answered.

Usage (inside the lease, with the server up):
  uv run python scripts/measure_currency_qwen.py http://127.0.0.1:8091
then, outside the lease, on the branch that should carry the entry:
  uv run python scripts/measure_currency_qwen.py record
"""

import hashlib
import json
import sys
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from levadura_salvaje.chunks import header, split
from levadura_salvaje.ledger import LEDGER, append, verify
from levadura_salvaje.lenses import currency
from levadura_salvaje.sections import sections

MODEL = "qwen3.8-27b-q4km"
GGUF = "/home/tony/models/Qwen3.8-27B-GGUF/Qwen3.8-27B-Q4_K_M.gguf"
LABELS = ("current", "historical", "no_rules")
STRENGTH = {"no_rules": 0, "historical": 1, "current": 2}
PARTIAL = Path("results/currency-qwen-v1-2025.partial.jsonl")
FINAL = Path("results/currency-qwen-v1-2025.jsonl")
JEV = Path("results/currency-jev-v1-2025.jsonl")
WORKERS = 2


def prompt() -> str:
    lines = [currency.INSTRUCTIONS, "", "The labels:"]
    for label, crit in currency.CRITERIA.items():
        lines.append(f"\n{label}:")
        lines += [f"  {k}: {v}" for k, v in crit.items()]
    lines.append('\nReply with JSON only: {"label": "<current|historical|no_rules>"}')
    return "\n".join(lines)


PROMPT = prompt()


def ask(base: str, text: str) -> dict:
    body = {
        "model": MODEL, "temperature": 0, "max_tokens": 20,
        "messages": [{"role": "system", "content": PROMPT}, {"role": "user", "content": text}],
        "response_format": {"type": "json_schema", "json_schema": {"name": "label", "schema": {
            "type": "object", "properties": {"label": {"type": "string", "enum": list(LABELS)}},
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
    jev = {(r["volume_file"], r["ordinal"]): r for r in map(json.loads, JEV.read_text().splitlines())}
    secs = [s for s in sections(Path("data/cfr/CFR-2025-title-26.zip")) if (s["volume_file"], s["ordinal"]) in jev]
    done = {}
    if PARTIAL.exists():
        for line in PARTIAL.read_text().splitlines():
            row = json.loads(line)
            done[row["key"]] = row
    todo = []
    for s in secs:
        b = jev[(s["volume_file"], s["ordinal"])]["chunk_chars"]
        pieces = split(s["text"], b)
        for k, piece in enumerate(pieces, 1):
            key = f"{s['volume_file']}#{s['ordinal']}#{s['sha256']}#{b}#{k}"
            if key not in done:
                todo.append((key, header(s["sectno"], s["subject"], k, len(pieces)) + piece))
    print(f"{len(secs)} sections, {len(todo)} chunks to ask ({len(done)} answered)", flush=True)
    failed = 0
    with PARTIAL.open("a") as out, ThreadPoolExecutor(WORKERS) as pool:
        futures = {pool.submit(ask, base, text): (key, text) for key, text in todo}
        for i, fut in enumerate(as_completed(futures), 1):
            key, text = futures[fut]
            try:
                row = {"key": key, "state_sha256": hashlib.sha256(text.encode()).hexdigest(), **fut.result()}
            except Exception as e:  # recorded in the log, retried on the next run
                failed += 1
                print(f"FAILED {key}: {type(e).__name__}: {e}", flush=True)
                continue
            done[key] = row
            out.write(json.dumps(row, sort_keys=True) + "\n")
            out.flush()
            if i % 100 == 0:
                print(f"  {i}/{len(todo)}", flush=True)
    if failed:
        sys.exit(f"{failed} chunks failed; rerun to resume. Nothing written to the ledger.")

    rows = []
    for s in secs:
        j = jev[(s["volume_file"], s["ordinal"])]
        b, n = j["chunk_chars"], j["chunks"]
        parts = [done[f"{s['volume_file']}#{s['ordinal']}#{s['sha256']}#{b}#{k}"] for k in range(1, n + 1)]
        label = max((p["label"] for p in parts), key=STRENGTH.get)
        rows.append({"volume_file": s["volume_file"], "ordinal": s["ordinal"], "sectno": s["sectno"],
                     "sha256": s["sha256"], "label": label, "chunk_labels": [p["label"] for p in parts],
                     "jev_label": j["label"]})
    FINAL.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in rows))
    print(f"wrote {FINAL}; record it with: uv run python scripts/measure_currency_qwen.py record")


def record() -> None:
    rows = [json.loads(l) for l in FINAL.read_text().splitlines()]
    agree = sum(r["label"] == r["jev_label"] for r in rows)
    jev_entry = [rec["id"] for rec in map(json.loads, LEDGER.read_text().splitlines())
                 if rec["quantity"] == "currency_lens_section_labels"]
    rec = append({
        "observed_at": "2025-04-01",
        "observed_at_note": "same population and chunks as obs-0132",
        "instrument": {
            "name": "scripts/measure_currency_qwen.py", "version": "1",
            "model": MODEL, "gguf": GGUF,
            "server": "llama.cpp llama-server, own instance under an ayllu-gpu lease (holder levadura-salvaje)",
            "prompt_sha256": hashlib.sha256(PROMPT.encode()).hexdigest(),
            "lens": f"levadura_salvaje.lenses.currency v{currency.LENS_VERSION} (question rendered as a prompt)",
            "method": "same chunks as the Jev run; JSON-schema-constrained label; temperature 0; thinking off; "
                      "section label = strongest chunk label",
            "predictions": "predictions/2026-09-24-currency-lens-claude.md (C7)",
        },
        "population": {"edition": "2025", "selection": "fossil candidates, v2 at 119-4",
                       "results_file": str(FINAL), "results_sha256": hashlib.sha256(FINAL.read_bytes()).hexdigest(),
                       "partial_sha256": hashlib.sha256(PARTIAL.read_bytes()).hexdigest()},
        "quantity": "currency_lens_section_labels_qwen",
        "value": {
            "sections": len(rows),
            "labels": dict(Counter(r["label"] for r in rows)),
            "C7_agreement_with_jev": [agree, len(rows)],
            "confusion_jev_vs_qwen": dict(Counter(f"{r['jev_label']}|{r['label']}" for r in rows)),
        },
        "derived_from": jev_entry,
    })
    print(rec["id"], json.dumps(rec["value"], indent=1))
    print("ledger verified:", verify())


if __name__ == "__main__":
    record() if sys.argv[1:] == ["record"] else main()
