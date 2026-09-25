"""Generated worlds for the record-currency pilot (docs/investigator-design.md).

A world keeps the real ledger's structure (which entries arrive in which
epoch, which share a measurement identity, the shape of each value, the
``derived_from`` edges) and replaces everything else. Every string becomes
an opaque per-world token, and every number is redrawn by shape. Neither
training data nor this project's history can then supply an answer, and no
interpretation in the real ledger reaches the subject.

Planting replacements and withdrawals is a separate step, done over a
generated world.
"""

import json
import random
from collections.abc import Mapping, Sequence


# Ledger length after each merge to main that grew it, PR #2 through #45
# (`git log --first-parent main -- ledger/observations.jsonl`). One epoch each.
LEDGER_EPOCH_ENDS = (7, 8, 45, 82, 119, 121, 122, 125, 130, 131, 133, 134, 136,
                     137, 138, 140, 141, 142, 144, 145, 146, 147)

SCHEMA = ("id", "epoch", "quantity", "population", "observed_at", "instrument", "version",
          "supersedes", "withdraws", "derived_from", "value")


def ledger_epochs(real: Sequence[dict], ends: Sequence[int] = LEDGER_EPOCH_ENDS) -> dict[str, int]:
    """Epoch of each real entry, by the merge that brought it to main."""
    return {r["id"]: next(k for k, end in enumerate(ends, 1) if n <= end)
            for n, r in enumerate(real, 1)}


def _pop_key(population) -> str:
    return json.dumps(population, sort_keys=True)


def skeleton(real: Sequence[dict], epochs: Mapping[str, int]) -> list[dict]:
    """Structure only: epoch, identity (as real keys, for mapping), shape, edges."""
    index = {r["id"]: i for i, r in enumerate(real)}
    return [{
        "epoch": epochs[r["id"]],
        "identity": (r["quantity"], _pop_key(r["population"]), r["observed_at"]),
        "instrument": r["instrument"].get("name", ""),
        "value": r["value"],
        "derived_from": [index[d] for d in r.get("derived_from", []) if d in index],
    } for r in real]


class _Tokens:
    """Stable opaque names per world, numbered in a shuffled order."""

    def __init__(self, prefix: str, rng: random.Random, universe: Sequence[str]):
        order = sorted(set(universe))
        rng.shuffle(order)
        self.map = {k: f"{prefix}{n + 1}" for n, k in enumerate(order)}
        self.prefix = prefix

    def __call__(self, key: str) -> str:
        if key not in self.map:
            self.map[key] = f"{self.prefix}{len(self.map) + 1}"
        return self.map[key]


def _decimals(x: float) -> int:
    text = repr(x)
    return min(len(text.split(".")[1]), 4) if "." in text and "e" not in text else 4


def _redraw(v, rng: random.Random, keys: _Tokens, strings: _Tokens):
    if isinstance(v, bool) or v is None:
        return rng.random() < 0.5 if isinstance(v, bool) else None
    if isinstance(v, int):
        digits = len(str(abs(v)))
        return rng.randrange(0 if digits == 1 else 10 ** (digits - 1), 10 ** digits)
    if isinstance(v, float):
        d = _decimals(v)
        if 0 <= v <= 1:
            return round(rng.random(), d)
        return round(v * rng.uniform(0.5, 2.0), d)
    if isinstance(v, str):
        return strings(v)
    if isinstance(v, list):
        if (len(v) == 2 and all(isinstance(x, int) and not isinstance(x, bool) for x in v)
                and 0 <= v[0] <= v[1]):
            d = _redraw(v[1], rng, keys, strings)
            return [rng.randint(0, d), d]
        return [_redraw(x, rng, keys, strings) for x in v]
    if isinstance(v, dict):
        return {keys(k): _redraw(x, rng, keys, strings) for k, x in v.items()}
    raise TypeError(f"unexpected value type {type(v)}")


def generate(real: Sequence[dict], epochs: Mapping[str, int], seed: int) -> list[dict]:
    """A world in the subject-facing schema, deterministic in ``seed``."""
    rng = random.Random(seed)
    sk = skeleton(real, epochs)
    quantities = _Tokens("Q", rng, [s["identity"][0] for s in sk])
    populations = _Tokens("P", rng, [s["identity"][1] for s in sk])
    instruments = _Tokens("I", rng, [s["instrument"] for s in sk])
    keys = _Tokens("K", rng, [])
    strings = _Tokens("S", rng, [])
    # observation times become order-preserving tokens
    times = {t: f"t{n + 1:04d}" for n, t in enumerate(sorted({s["identity"][2] for s in sk}))}
    world = []
    for i, s in enumerate(sk):
        q, p, t = s["identity"]
        world.append({
            "id": f"w-{i + 1:04d}",
            "epoch": s["epoch"],
            "quantity": quantities(q),
            "population": populations(p),
            "observed_at": times[t],
            "instrument": instruments(s["instrument"]),
            "version": 1,
            "supersedes": None,
            "withdraws": None,
            "derived_from": [f"w-{j + 1:04d}" for j in s["derived_from"]],
            "value": _redraw(s["value"], rng, keys, strings),
        })
    return world
