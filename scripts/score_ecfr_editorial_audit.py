"""Score the blind audit of the eCFR editorial study (E5, E6, J4, J5).

As stamped (predictions/2026-11-03-ecfr-editorial-claude.md and amendment 1):
- E5: among `text_changed` versions Haiku calls `editorial`, the share where *both* readers say
  `editorial` (pass at 50% or more);
- J4: the same for Jev;
- J5: Jev's share is at least Haiku's;
- E6: among the 20 agreement controls, both readers say `substantive` on at least 17.
Readers' `unclear` counts as not siding with the classifier.

Usage: uv run python scripts/score_ecfr_editorial_audit.py
"""

import json
from pathlib import Path

D = Path("results/ecfr-editorial")


def load(p: Path) -> dict:
    return {r["item"]: r for r in map(json.loads, p.read_text().splitlines())}


def verbatim(reader: dict, packet: dict) -> tuple[int, int]:
    """How many of a reader's decisive_text quotes occur in that item's own diff (whitespace-normalized).
    The first reader B labelled from a list with an `editorial` default and quoted stock text; this
    is the check that catches it (audit-instructions-v2-addendum.md)."""
    norm = lambda t: " ".join(str(t).split())  # noqa: E731
    ok = sum(1 for i, r in reader.items() if i in packet and norm(r.get("decisive_text", ""))
             and norm(r["decisive_text"]) in norm(packet[i]["diff"]))
    return ok, len(reader)


def load_parts(prefix: str) -> dict:
    out = {}
    for p in sorted((D / "audit").glob(f"{prefix}*.jsonl")):
        out |= load(p)
    return out


def main() -> None:
    key = load(D / "audit-key.jsonl")
    packet = load(D / "audit-packet.jsonl")
    a, b = load_parts("reader-a"), load_parts("reader-b2")
    for name, r in (("A", a), ("B", b)):
        ok, n = verbatim(r, packet)
        print(f"reader {name}: {n} labels, decisive_text verbatim in its item's diff: {ok}/{n}")
    missing = [i for i in key if i not in a or i not in b]
    both = lambda i, lab: a[i]["label"] == lab and b[i]["label"] == lab  # noqa: E731
    agree = sum(1 for i in key if i in a and i in b and a[i]["label"] == b[i]["label"])
    print(f"{len(key)} items; missing from a reader: {len(missing)}; readers agree on {agree}")

    def precision(classifier: str) -> tuple[int, int]:
        items = [i for i, k in key.items() if k["kind"] == "disagreement" and k[classifier] == "editorial"
                 and i in a and i in b]
        return sum(both(i, "editorial") for i in items), len(items)

    h, hn = precision("classifier")
    j, jn = precision("jev")
    ctrl = [i for i, k in key.items() if k["kind"] == "control" and i in a and i in b]
    c = sum(both(i, "substantive") for i in ctrl)
    print(f"E5 Haiku editorial calls, both readers editorial: {h}/{hn} = {h / hn:.1%} -> "
          f"{'pass' if h / hn >= 0.5 else 'fail'}")
    print(f"J4 Jev editorial calls, both readers editorial:   {j}/{jn} = {j / jn:.1%} -> "
          f"{'pass' if j / jn >= 0.5 else 'fail'}")
    print(f"J5 Jev precision >= Haiku's: {j / jn:.1%} vs {h / hn:.1%} -> {'pass' if j / jn >= h / hn else 'fail'}")
    print(f"E6 controls, both readers substantive: {c}/{len(ctrl)} -> {'pass' if c >= 17 else 'fail'}")
    # Descriptive only, not stamped: each classifier's editorial calls by what the readers said.
    for name in ("classifier", "jev"):
        items = [i for i, k in key.items() if k["kind"] == "disagreement" and k[name] == "editorial"
                 and i in a and i in b]
        split = {}
        for i in items:
            pair = "/".join(sorted((a[i]["label"], b[i]["label"])))
            split[pair] = split.get(pair, 0) + 1
        print(f"  {name} editorial calls by reader labels: {dict(sorted(split.items()))}")


if __name__ == "__main__":
    main()
