"""Run the AMT lens (Jev) over every section of 26 CFR editions.

Each section is split into chunks of at most CHUNK_CHARS characters (see
chunks.py); every chunk is one Jev call, sent with a header naming the
section and its part. The section's label is the strongest chunk label,
operative > incidental > none, as registered in the predictions. If Jev
refuses a chunk as too long (max_tokens_exceeded; dense tables run far below
the usual ~3 characters per token), the whole section is re-split at half the
budget, so its chunks always partition it at one budget, recorded per section.

Calls are written as they complete to results/amt-jev-v<lens>-<edition>.partial.jsonl,
so an interrupted run resumes where it stopped: a chunk already answered for
the same section text (sha256) is not asked again. When every section of an
edition is answered, the per-section file is written and the ledger gets one
entry per volume, like the baseline. If any call still fails, the run stops
before the ledger: an entry is written only for a fully answered edition.

Usage: uv run python scripts/measure_amt_lens.py 1997 2025
       uv run python scripts/measure_amt_lens.py --pilot 40 2025   (asks only the
       first 40 outstanding chunks; answers are kept for the full run)
"""

import hashlib
import json
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from typesafe_sdk import TypeSafeClient

from levadura_salvaje.chunks import header, split
from levadura_salvaje.ledger import LEDGER, append, verify
from levadura_salvaje.lenses import amt
from levadura_salvaje.sections import sections

CHUNK_CHARS = 40_000
MIN_CHUNK_CHARS = 2_500
WORKERS = 8
STRENGTH = {"none": 0, "incidental": 1, "operative": 2}
INSTRUMENT = {
    "name": "levadura_salvaje.lenses.amt",
    "version": amt.LENS_VERSION,
    "model": amt.MODEL,
    "lens_sha256": hashlib.sha256(amt.LENS_TEXT.encode()).hexdigest(),
    "method": (
        f"one Jev Choice call per chunk of at most {CHUNK_CHARS} characters (halved per "
        "section on max_tokens_exceeded, down to MIN_CHUNK_CHARS), cut at "
        "sentence ends, each prefixed with a header naming the section and part; "
        "section label = strongest chunk label (operative > incidental > none)"
    ),
    "lens_written_by": "a separate instance, from the intent section of the predictions only",
}


def chunk_key(s: dict, budget: int, k: int) -> str:
    return f"{s['volume_file']}#{s['ordinal']}#{s['sha256']}#{budget}#{k}"


def load(partial: Path) -> tuple[dict, set]:
    """Answered chunks by key, and (section, budget) pairs Jev refused as too long."""
    done, too_long = {}, set()
    if partial.exists():
        for line in partial.read_text().splitlines():
            row = json.loads(line)
            if row["key"].count("#") == 3:  # written before budgets were in the key
                v, o, h, k = row["key"].split("#")
                row["key"] = f"{v}#{o}#{h}#{CHUNK_CHARS}#{k}"
            if "label" in row:
                done[row["key"]] = row
            elif row.get("error") == "max_tokens_exceeded":
                too_long.add(row["key"].rsplit("#", 1)[0])
    return done, too_long


def budget_for(s: dict, too_long: set) -> int:
    b = CHUNK_CHARS
    while f"{s['volume_file']}#{s['ordinal']}#{s['sha256']}#{b}" in too_long and b > MIN_CHUNK_CHARS:
        b //= 2
    return b


def ask(client, s, b, k, n, piece):
    state = header(s["sectno"], s["subject"], k, n) + piece
    r = amt.classify(state, client)
    del r["lens_text"]  # recorded once, by hash, in the instrument
    return {"key": chunk_key(s, b, k), "chunk": k, "chunks": n, "chars": len(state), "budget": b,
            "state_sha256": hashlib.sha256(state.encode()).hexdigest(), **r}


def run(edition: str, pilot: int | None = None) -> None:
    zip_path = Path(f"data/cfr/CFR-{edition}-title-26.zip")
    partial = Path(f"results/amt-jev-v{amt.LENS_VERSION}-{edition}.partial.jsonl")
    done, too_long = load(partial)
    secs = list(sections(zip_path))
    with TypeSafeClient(timeout=60) as client, partial.open("a") as out:
        while True:
            todo = []
            for s in secs:
                b = budget_for(s, too_long)
                pieces = split(s["text"], b)
                for k, piece in enumerate(pieces, 1):
                    if chunk_key(s, b, k) not in done:
                        todo.append((s, b, k, len(pieces), piece))
            print(f"{edition}: {len(secs)} sections, {len(todo)} chunks to ask ({len(done)} answered so far)")
            if pilot is not None:
                todo = todo[:pilot]
            failed, refused = [], 0
            with ThreadPoolExecutor(WORKERS) as pool:
                futures = {pool.submit(ask, client, *t): t for t in todo}
                for i, fut in enumerate(as_completed(futures), 1):
                    s, b, k, n, _ = futures[fut]
                    try:
                        row = fut.result()
                    except Exception as e:  # recorded, never dropped
                        if "max_tokens_exceeded" in str(e) and b > MIN_CHUNK_CHARS:
                            row = {"key": chunk_key(s, b, k), "error": "max_tokens_exceeded"}
                            too_long.add(row["key"].rsplit("#", 1)[0])
                            refused += 1
                        else:
                            failed.append(f"{s['volume_file']}#{s['ordinal']} {s['sectno']} part {k}: "
                                          f"{type(e).__name__}: {e}")
                            continue
                    else:
                        done[row["key"]] = row
                    out.write(json.dumps(row, sort_keys=True) + "\n")
                    out.flush()
                    if i % 500 == 0:
                        print(f"  {i}/{len(todo)}")
            if failed:
                print(f"FAILED {len(failed)} chunk calls, e.g. {failed[0]}")
            if refused:
                print(f"  {refused} chunks too long for Jev; re-splitting those sections at half budget")
            if not refused or pilot is not None:
                break

    if pilot is not None:
        rows = [done[chunk_key(s, b, k)] for s, b, k, _, _ in todo if chunk_key(s, b, k) in done]
        tok = sum(r["input_tokens"] for r in rows)
        chars = sum(r["chars"] for r in rows)
        print(f"  pilot: {len(rows)} answered, {chars / max(tok, 1):.2f} chars/input token "
              f"(question overhead included), labels {dict(Counter(r['label'] for r in rows))}")
        return
    budgets = {id(s): budget_for(s, too_long) for s in secs}
    if any(chunk_key(s, budgets[id(s)], k) not in done
           for s in secs for k in range(1, len(split(s["text"], budgets[id(s)])) + 1)):
        sys.exit(f"{edition}: incomplete; rerun to resume. Nothing written to the ledger.")

    final = Path(f"results/amt-jev-v{amt.LENS_VERSION}-{edition}.jsonl")
    per_volume = defaultdict(list)
    with final.open("w") as f:
        for s in secs:
            b = budgets[id(s)]
            n = len(split(s["text"], b))
            parts = [done[chunk_key(s, b, k)] for k in range(1, n + 1)]
            top = max(parts, key=lambda p: (STRENGTH[p["label"]], p["confidence"] or 0))
            row = {
                "volume_file": s["volume_file"], "ordinal": s["ordinal"], "sectno": s["sectno"],
                "sha256": s["sha256"], "label": top["label"], "chunks": n, "chunk_chars": b,
                "decided_by_chunk": top["chunk"],
                "probabilities": top["probabilities"], "confidence": top["confidence"],
                "chunk_labels": [p["label"] for p in parts],
                "request_ids": [p["request_id"] for p in parts],
                "model": top["model"],
            }
            f.write(json.dumps(row, sort_keys=True) + "\n")
            per_volume[s["volume_file"]].append(row)
    results_sha = hashlib.sha256(final.read_bytes()).hexdigest()

    structure = {}
    for line in LEDGER.read_text().splitlines():
        rec = json.loads(line)
        if rec["quantity"] == "cfr26_volume_structure" and rec["population"]["edition"] == edition:
            structure[rec["population"]["volume_file"]] = rec
    models = {r["model"] for rows in per_volume.values() for r in rows}
    for volume_file in sorted(structure, key=lambda v: int(v.split("vol")[1].split(".")[0])):
        rows, src = per_volume.get(volume_file, []), structure[volume_file]
        labels = Counter(r["label"] for r in rows)
        rec = append({
            "observed_at": src["observed_at"],
            "derived_from": src["id"],
            "instrument": INSTRUMENT | {"models_reported": sorted(models)},
            "population": {
                "edition": edition, "volume_file": volume_file, "sha256": src["population"]["sha256"],
                "results_file": str(final), "results_sha256": results_sha,
            },
            "quantity": "amt_lens_section_labels",
            "value": {
                "sections": len(rows),
                "labels": {k: labels.get(k, 0) for k in STRENGTH},
                "chunked_sections": sum(r["chunks"] > 1 for r in rows),
                "resplit_sections": [[r["ordinal"], r["sectno"], r["chunk_chars"]]
                                     for r in rows if r["chunk_chars"] < CHUNK_CHARS],
                "operative_sections": [[r["ordinal"], r["sectno"]] for r in rows if r["label"] == "operative"],
                "incidental_sections": [[r["ordinal"], r["sectno"]] for r in rows if r["label"] == "incidental"],
            },
        })
        print(rec["id"], edition, volume_file.split("-")[-1], dict(labels))


def main() -> None:
    args = sys.argv[1:]
    pilot = None
    if args[:1] == ["--pilot"]:
        pilot, args = int(args[1]), args[2:]
    for edition in args:
        run(edition, pilot)
    print("ledger verified:", verify(), "entries")


if __name__ == "__main__":
    main()
