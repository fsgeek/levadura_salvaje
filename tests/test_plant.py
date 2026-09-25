import json
from pathlib import Path

import pytest

from levadura_salvaje.currency_key import answer, pick, score
from levadura_salvaje.worlds import generate, ledger_epochs, plant

REAL = [json.loads(line) for line in Path("ledger/observations.jsonl").read_text().splitlines()]


# 57, 91 and 96 plant a repeat on an identity with several observations
@pytest.fixture(params=[0, 1, 2, 57, 91, 96])
def planted(request):
    base = generate(REAL, ledger_epochs(REAL), seed=request.param)
    return plant(base, seed=request.param)


def test_six_events_of_the_declared_kinds_at_distinct_post_inventory_epochs(planted):
    world, probes = planted
    events = [r for r in world if r.get("event")]
    assert sorted(r["event"] for r in events) == sorted(
        ["replace", "replace", "replace", "replace_equal", "withdraw", "repeat"])
    epochs = [r["epoch"] for r in events]
    assert len(set(epochs)) == 6 and min(epochs) >= 6


def test_every_probe_is_answerable_and_d_scores_correct(planted):
    world, probes = planted
    for p in probes:
        key = answer(world, p["epoch"], p["quantity"], p["population"], p["observed_at"], p["field"])
        assert key is not None
        assert score(world, p["epoch"], p["quantity"], p["population"], p["observed_at"], key,
                     p["field"]) == {"status": "answered", "value": "current", "source": "current"}


def test_changed_replacements_change_the_probed_field_and_equal_ones_do_not(planted):
    world, probes = planted
    by_id = {r["id"]: r for r in world}
    for r in world:
        if r.get("event") in ("replace", "replace_equal"):
            p = next(p for p in probes if p["event_id"] == r["id"])
            old, new = pick(by_id[r["supersedes"]]["value"], p["field"]), pick(r["value"], p["field"])
            assert (old == new) == (r["event"] == "replace_equal")


def test_before_the_event_the_old_answer_is_correct_after_it_is_stale(planted):
    world, probes = planted
    by_id = {r["id"]: r for r in world}
    for p in probes:
        ev = by_id[p["event_id"]]
        if ev["event"] != "replace" or p["control"]:
            continue
        old = {"value": pick(by_id[ev["supersedes"]]["value"], p["field"]), "source_id": ev["supersedes"]}
        assert score(world, p["epoch"], p["quantity"], p["population"], p["observed_at"], old,
                     p["field"]) == {"status": "answered", "value": "obsolete", "source": "replaced"}


def test_probes_come_at_fixed_lags_with_matched_controls(planted):
    world, probes = planted
    for ev in (r for r in world if r.get("event")):
        mine = [p for p in probes if p["event_id"] == ev["id"]]
        lags = sorted(p["epoch"] - ev["epoch"] for p in mine if not p["control"])
        assert lags == [0, 1, 3]
        assert sorted(p["epoch"] for p in mine if p["control"]) == sorted(
            p["epoch"] for p in mine if not p["control"])
        for p in mine:
            if p["control"]:
                assert not any(r.get("supersedes") == p["target_id"] or r.get("withdraws") == p["target_id"]
                               for r in world)


def test_planting_is_deterministic():
    base = generate(REAL, ledger_epochs(REAL), seed=1)
    assert plant(base, seed=1) == plant(base, seed=1)


def test_a_repeat_becomes_the_latest_observation(planted):
    world, probes = planted
    rep = next(r for r in world if r.get("event") == "repeat")
    same = [r for r in world if (r["quantity"], r["population"]) == (rep["quantity"], rep["population"])]
    assert max(r["observed_at"] for r in same) == rep["observed_at"]
    p = next(p for p in probes if p["event_id"] == rep["id"] and not p["control"])
    assert answer(world, p["epoch"], p["quantity"], p["population"], None, p["field"])["source_id"] == rep["id"]
