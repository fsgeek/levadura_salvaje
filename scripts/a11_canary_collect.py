"""Collect the A11 canary readers' candidates into one list, and a blind copy for the verifiers.

The blind copy has no reader or arm, and its order is shuffled with a fixed seed, so the verifiers can't tell who
proposed a candidate or under which task. The key (candidates-key.json) maps each id back.

Usage: uv run python scripts/a11_canary_collect.py OUT_DIR
Reads OUT_DIR/{narrow,broad}/*: OpenRouter responses (*.json with "response"), CLI final messages (cli__*.txt) and
agent arrays (agent__*.json). Truncated first runs (*.run1-truncated.json) are skipped; the reruns replace them.
"""

import json
import random
import sys
from pathlib import Path


def array_in(text: str) -> list:
    """The JSON array in a reader's final message, which may be fenced or preceded by narration."""
    end = text.rindex("]") + 1
    for start in (i for i, ch in enumerate(text) if ch == "["):
        try:
            got = json.loads(text[start:end])
        except json.JSONDecodeError:
            continue
        if isinstance(got, list) and all(isinstance(x, dict) for x in got):
            return got
    raise ValueError("no JSON array of objects found")


def read(path: Path) -> list:
    if path.name.startswith("cli__"):
        return array_in(path.read_text())
    data = json.loads(path.read_text())
    if isinstance(data, list):
        return data
    return array_in(data["response"]["choices"][0]["message"]["content"])


def main():
    out = Path(sys.argv[1])
    rows, report = [], []
    for arm in ("narrow", "broad"):
        for path in sorted((out / arm).iterdir()):
            if "truncated" in path.name or path.suffix not in (".json", ".txt"):
                continue
            reader = path.stem.removeprefix("cli__").removeprefix("agent__")
            try:
                found = read(path)
            except Exception as e:  # a reader with no usable answer is reported, not dropped silently
                report.append(f"{arm} {reader}: UNUSABLE ({e})")
                continue
            found = [f for f in found if f.get("loc_a") or f.get("loc_b")]  # drop "could not read" notes
            report.append(f"{arm} {reader}: {len(found)}")
            rows += [{"arm": arm, "reader": reader, **f} for f in found]
    random.Random(20261029).shuffle(rows)
    key, blind = [], []
    for i, r in enumerate(rows):
        cid = f"c{i:03d}"
        key.append({"id": cid, "arm": r["arm"], "reader": r["reader"]})
        blind.append({"id": cid, **{k: r.get(k, "") for k in
                                    ("loc_a", "quote_a", "loc_b", "quote_b", "kind", "explanation")}})
    (out / "candidates-key.json").write_text(json.dumps(key, indent=1))
    (out / "candidates-blind.json").write_text(json.dumps(blind, indent=1, ensure_ascii=False))
    (out / "collect-report.txt").write_text("\n".join(report) + f"\ntotal {len(rows)}\n")
    print("\n".join(report), f"\ntotal {len(rows)}")


if __name__ == "__main__":
    main()
