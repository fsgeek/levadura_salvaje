"""The capped ledger tool every arm of the pilot uses, and arm D's client.

Subjects see records only through ``render``, which keeps exactly the
subject-facing schema: the generator's internal ``event`` label (which
names a replacement or withdrawal as such) never leaves this module.
"""

from collections.abc import Sequence

from levadura_salvaje.currency_key import answer
from levadura_salvaje.worlds import SCHEMA

MAX_RECORDS = 40


def render(record: dict) -> dict:
    return {k: record.get(k) for k in SCHEMA}


class LedgerTool:
    """Exact-match queries over the records revealed by ``epoch``."""

    def __init__(self, world: Sequence[dict], epoch: int):
        self._revealed = [r for r in world if r["epoch"] <= epoch]
        self.calls = 0

    def query(self, id: str | None = None, quantity: str | None = None,
              population: str | None = None, limit: int = MAX_RECORDS, offset: int = 0) -> dict:
        self.calls += 1
        hits = [r for r in self._revealed
                if (id is None or r["id"] == id)
                and (quantity is None or r["quantity"] == quantity)
                and (population is None or r["population"] == population)]
        limit = max(1, min(limit, MAX_RECORDS))
        page = hits[offset:offset + limit]
        nxt = offset + limit if offset + limit < len(hits) else None
        return {"records": [render(r) for r in page], "total": len(hits), "next_offset": nxt}


def deterministic_client(tool: LedgerTool, probe: dict) -> dict:
    """Arm D: page through the tool for the probe's identity, then resolve it.

    Uses only what the tool returns, so it faces the same caps as a subject.
    """
    records, offset = [], 0
    while offset is not None:
        page = tool.query(quantity=probe["quantity"], population=probe["population"], offset=offset)
        records += page["records"]
        offset = page["next_offset"]
    # withdrawals carry their target's identity, so they are in this set too;
    # the answer key needs an epoch, and everything the tool returned is revealed
    visible = [{**r, "epoch": 0} for r in records]
    got = answer(visible, 0, probe["quantity"], probe["population"], probe["observed_at"], probe["field"])
    return got if got is not None else {"abstain": True}
