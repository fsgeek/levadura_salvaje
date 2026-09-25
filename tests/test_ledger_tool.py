import json
from pathlib import Path

import pytest

from levadura_salvaje.currency_key import answer, score
from levadura_salvaje.ledger_tool import LedgerTool, deterministic_client, render
from levadura_salvaje.worlds import SCHEMA, generate, ledger_epochs, plant

REAL = [json.loads(line) for line in Path("ledger/observations.jsonl").read_text().splitlines()]


@pytest.fixture(params=[0, 57])
def planted(request):
    return plant(generate(REAL, ledger_epochs(REAL), request.param), request.param)


def test_render_shows_only_the_subject_schema(planted):
    world, _ = planted
    for r in world:
        assert set(render(r)) == set(SCHEMA)       # no "event" label, nothing extra
    assert "replace" not in json.dumps([render(r) for r in world])


def test_tool_reveals_only_entries_up_to_the_epoch(planted):
    world, _ = planted
    tool = LedgerTool(world, epoch=3)
    got = tool.query(limit=40)
    assert all(r["epoch"] <= 3 for r in got["records"])
    assert got["total"] == sum(r["epoch"] <= 3 for r in world)


def test_tool_caps_pages_and_filters(planted):
    world, _ = planted
    tool = LedgerTool(world, epoch=22)
    page = tool.query(limit=500)
    assert len(page["records"]) == 40 and page["next_offset"] == 40
    q = world[0]["quantity"]
    assert all(r["quantity"] == q for r in tool.query(quantity=q)["records"])
    assert tool.query(id=world[0]["id"])["records"] == [render(world[0])]
    assert tool.calls == 3


def test_deterministic_client_through_the_tool_scores_current_on_every_probe(planted):
    world, probes = planted
    for p in probes:
        tool = LedgerTool(world, epoch=p["epoch"])
        given = deterministic_client(tool, p)
        assert given == answer(world, p["epoch"], p["quantity"], p["population"],
                               p["observed_at"], p["field"])
        assert score(world, p["epoch"], p["quantity"], p["population"], p["observed_at"], given,
                     p["field"])["value"] == "current"
        assert tool.calls <= 12
