"""Run the dated-period lens (Jev) over the 2025 fossil-candidate sections.

Predictions D1-D5: predictions/2026-09-24-dated-lens-claude.md. The lens
(lenses/dated.py) was written by a separate instance from the intent
section alone. Population: every 2025 section with at least one Code
citation broken at 119-4 (extractor v2, resolver v2).

Chunking, resumption and refusal handling are the AMT runner's
(scripts/measure_amt_lens.py): chunks of at most CHUNK_CHARS, halved per
section on max_tokens_exceeded, and every call is written to a partial file
as it completes. Section label = strongest chunk label, names_ended_period >
silent > no_rules.

Usage: uv run python scripts/measure_dated_lens.py [--pilot N]
"""

import hashlib
import json
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from typesafe_sdk import TypeSafeClient

from levadura_salvaje.chunks import header, split
from levadura_salvaje.ledger import LEDGER, append, verify
from levadura_salvaje.lenses import dated
from levadura_salvaje.sections import sections

EDITION = "2025"
CITATIONS = Path("results/cfr-usc-citations-v2-2025.jsonl")
CHUNK_CHARS = 40_000
MIN_CHUNK_CHARS = 2_500
WORKERS = 8
STRENGTH = {"no_rules": 0, "silent": 1, "names_ended_period": 2}
BROKEN = {"repealed", "absent-section", "absent-subdivision"}
INSTRUMENT = {
    "name": "levadura_salvaje.lenses.dated",
    "version": dated.LENS_VERSION,
    "model": dated.MODEL,
    "lens_sha256": hashlib.sha256(dated.LENS_TEXT.encode()).hexdigest(),
    "method": (
        f"one Jev Choice call per chunk of at most {CHUNK_CHARS} characters (halved per "
        "section on max_tokens_exceeded, down to MIN_CHUNK_CHARS), cut at sentence ends, "
        "each prefixed with a header naming the section and part; section label = "
        "strongest chunk label (names_ended_period > silent > no_rules)"
    ),
    "lens_written_by": "a separate instance, from the intent section of the predictions only",
    "predictions": "predictions/2026-09-24-dated-lens-claude.md",
}


def citation_rows() -> dict:
    return {(r["volume_file"], r["ordinal"]): r
            for r in map(json.loads, CITATIONS.read_text().splitlines())}


def candidates() -> list[dict]:
    cit = citation_rows()
    return [s for s in sections(Path(f"data/cfr/CFR-{EDITION}-title-26.zip"))
            if cit[(s["volume_file"], s["ordinal"])]["broken"]["119-4"] > 0]


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
    r = dated.classify(state, client)
    del r["lens_text"]  # recorded once, by hash, in the instrument
    return {"key": chunk_key(s, b, k), "chunk": k, "chunks": n, "chars": len(state), "budget": b,
            "state_sha256": hashlib.sha256(state.encode()).hexdigest(), **r}


def run(pilot: int | None = None) -> None:
    edition = EDITION
    partial = Path(f"results/dated-jev-v{dated.LENS_VERSION}-{edition}.partial.jsonl")
    done, too_long = load(partial)
    secs = candidates()
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
        sys.exit("incomplete; rerun to resume. Nothing written to the ledger.")

    cit = citation_rows()
    final = Path(f"results/dated-jev-v{dated.LENS_VERSION}-{edition}.jsonl")
    rows = []
    with final.open("w") as f:
        for s in secs:
            b = budgets[id(s)]
            n = len(split(s["text"], b))
            parts = [done[chunk_key(s, b, k)] for k in range(1, n + 1)]
            top = max(parts, key=lambda p: (STRENGTH[p["label"]], p["confidence"] or 0))
            c = cit[(s["volume_file"], s["ordinal"])]
            outs = [x["outcome"]["119-4"]["outcome"] for x in c["citations"] if "outcome" in x]
            row = {
                "volume_file": s["volume_file"], "ordinal": s["ordinal"], "sectno": s["sectno"],
                "sha256": s["sha256"], "label": top["label"], "chunks": n, "chunk_chars": b,
                "decided_by_chunk": top["chunk"],
                "probabilities": top["probabilities"], "confidence": top["confidence"],
                "chunk_labels": [p["label"] for p in parts],
                "request_ids": [p["request_id"] for p in parts],
                "model": top["model"],
                "citations": len(outs), "broken": sum(o in BROKEN for o in outs),
                "broken_kinds": dict(Counter(o for o in outs if o in BROKEN)),
                "amt_fossil": c["amt_fossil"], "in_1997": c["in_1997"],
            }
            f.write(json.dumps(row, sort_keys=True) + "\n")
            rows.append(row)
    results_sha = hashlib.sha256(final.read_bytes()).hexdigest()

    labels = Counter(r["label"] for r in rows)
    cur = {(r["volume_file"], r["ordinal"]): r["label"]
           for r in map(json.loads, Path("results/currency-jev-v1-2025.jsonl").read_text().splitlines())}
    share = lambda rs, lab: [sum(r["label"] == lab for r in rs), len(rs)]
    current = [r for r in rows if cur.get((r["volume_file"], r["ordinal"])) == "current"]
    ident = [r for r in rows if r["in_1997"]]
    other = [r for r in rows if not r["in_1997"]]
    src = [rec for rec in map(json.loads, LEDGER.read_text().splitlines())
           if (rec["quantity"] == "cfr_usc_citation_resolution" and rec["instrument"]["version"] == "2"
               and rec["population"]["release_point"] == "119-4")
           or rec["quantity"] == "currency_lens_section_labels"]
    rec = append({
        "observed_at": "2025-04-01",
        "observed_at_note": "the 2025 CFR's dominant volume date; candidates carry their own volume dates",
        "instrument": INSTRUMENT | {"models_reported": sorted({r["model"] for r in rows})},
        "population": {"edition": edition, "selection": "fossil candidates, v2 at 119-4",
                       "results_file": str(final), "results_sha256": results_sha},
        "quantity": "dated_lens_section_labels",
        "value": {
            "sections": len(rows),
            "labels": {k: labels.get(k, 0) for k in STRENGTH},
            "D3_named_among_currency_current": share(current, "names_ended_period"),
            "D4_named_identical_to_1997": share(ident, "names_ended_period"),
            "D4_named_other": share(other, "names_ended_period"),
            "chunked_sections": sum(r["chunks"] > 1 for r in rows),
            "resplit_sections": [[r["ordinal"], r["sectno"], r["chunk_chars"]]
                                 for r in rows if r["chunk_chars"] < CHUNK_CHARS],
        },
        "derived_from": [x["id"] for x in src],
    })
    print(rec["id"], json.dumps(rec["value"], indent=1)[:2000])


def main() -> None:
    args = sys.argv[1:]
    pilot = int(args[1]) if args[:1] == ["--pilot"] else None
    run(pilot)
    print("ledger verified:", verify(), "entries")


if __name__ == "__main__":
    main()
