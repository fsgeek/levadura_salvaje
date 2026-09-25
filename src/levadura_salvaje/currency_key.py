"""Answer key for the record-currency pilot, and the deterministic arm D.

Semantics are those of docs/investigator-design.md: a measurement identity
is (quantity, population, observed_at). A later observed_at is a new fact,
not a replacement. ``supersedes`` replaces an entry (chains are followed);
``withdraws`` withdraws one with no replacement. Derived entries are reports
of what was computed and are untouched when their inputs change.

``observed_at=None`` asks for the latest observed identity. Observation
times are compared as strings, so worlds must use sortable ones.

``field`` names one scalar inside a nested value, as a tuple of keys and
list indices; ledger values are objects, and a probe asks about one number.
"""

from collections.abc import Sequence


def _revealed(world: Sequence[dict], epoch: int) -> list[dict]:
    return [r for r in world if r["epoch"] <= epoch]


def _identity(r: dict, by_id: dict) -> tuple:
    # a withdrawal carries no identity of its own; it acts on its target's
    if r.get("withdraws"):
        r = by_id[r["withdraws"]]
    return (r["quantity"], r["population"], r["observed_at"])


def pick(value, field: tuple = ()):
    for step in field:
        value = value[step]
    return value


def answer(world: Sequence[dict], epoch: int, quantity: str, population: str,
           observed_at: str | None = None, field: tuple = ()) -> dict | None:
    """The correct typed answer at ``epoch``, or None if nothing is revealed."""
    revealed = _revealed(world, epoch)
    by_id = {r["id"]: r for r in revealed}
    matching = [r for r in revealed if _identity(r, by_id)[:2] == (quantity, population)]
    if not matching:
        return None
    if observed_at is None:
        observed_at = max(_identity(r, by_id)[2] for r in matching)
    chain = [r for r in matching if _identity(r, by_id)[2] == observed_at]
    if not chain:
        return None
    replaced = {r["supersedes"] for r in chain if r.get("supersedes")}
    replaced |= {r["withdraws"] for r in chain if r.get("withdraws")}
    heads = [r for r in chain if r["id"] not in replaced]
    if len(heads) != 1:
        raise ValueError(f"identity {(quantity, population, observed_at)} has {len(heads)} current entries")
    head = heads[0]
    if head.get("withdraws"):
        return {"withdrawn": True, "source_id": head["id"]}
    return {"value": pick(head["value"], field), "source_id": head["id"]}


def _replaced_entries(world: Sequence[dict], epoch: int, quantity: str, population: str,
                      observed_at: str | None, current_id: str) -> list[dict]:
    revealed = _revealed(world, epoch)
    by_id = {r["id"]: r for r in revealed}
    matching = [r for r in revealed if not r.get("withdraws")
                and _identity(r, by_id)[:2] == (quantity, population) and r["id"] != current_id]
    if observed_at is not None:
        matching = [r for r in matching if r["observed_at"] == observed_at]
    return matching


def _same(a, b) -> bool:
    """Typed equality: a boolean is never a number, though Python says True == 1."""
    if isinstance(a, bool) or isinstance(b, bool):
        return type(a) is type(b) and a == b
    return a == b


_MISSING = object()


def _field(value, field: tuple):
    try:
        return pick(value, field)
    except (KeyError, IndexError, TypeError):
        return _MISSING


def _valid(given) -> bool:
    if not isinstance(given, dict):
        return False
    if set(given) == {"abstain"}:
        return given["abstain"] is True
    if not isinstance(given.get("source_id"), str):
        return False
    if set(given) == {"withdrawn", "source_id"}:
        return given["withdrawn"] is True
    return (set(given) == {"value", "source_id"}
            and isinstance(given["value"], (int, float)) and not isinstance(given["value"], bool))


def score(world: Sequence[dict], epoch: int, quantity: str, population: str,
          observed_at: str | None, given, field: tuple = ()) -> dict:
    """Score a typed answer on separate dimensions.

    status: abstain, invalid (wrong shape or type) or answered.
    value:  current (matches the key, or correctly says withdrawn), obsolete
            (matches only a replaced entry's field) or other.
    source: current, replaced (names a replaced entry of this identity) or other.

    An equal-value replacement answered with the old source is therefore a
    provenance error (value current, source replaced), not a factual one.
    """
    if not _valid(given):
        return {"status": "invalid", "value": None, "source": None}
    if given.get("abstain"):
        return {"status": "abstain", "value": None, "source": None}
    key = answer(world, epoch, quantity, population, observed_at, field)
    if key is None:
        raise ValueError("probe asks about an identity not yet revealed")
    # only entries of the identity the key answered for count as replaced, so
    # naming an earlier, still-valid observation is "other", not "replaced"
    by_id = {r["id"]: r for r in _revealed(world, epoch)}
    observed_at = _identity(by_id[key["source_id"]], by_id)[2]
    old = _replaced_entries(world, epoch, quantity, population, observed_at, key["source_id"])
    old_values = [v for v in (_field(r["value"], field) for r in old) if v is not _MISSING]

    if "withdrawn" in given:
        value = "current" if key.get("withdrawn") else "other"
    elif "value" in key and _same(given["value"], key["value"]):
        value = "current"
    elif any(_same(given["value"], v) for v in old_values):
        value = "obsolete"
    else:
        value = "other"
    if given["source_id"] == key["source_id"]:
        source = "current"
    elif given["source_id"] in {r["id"] for r in old}:
        source = "replaced"
    else:
        source = "other"
    return {"status": "answered", "value": value, "source": source}
