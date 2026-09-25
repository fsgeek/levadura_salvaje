import json
from pathlib import Path

from levadura_salvaje.worlds import SCHEMA, generate, ledger_epochs, skeleton

REAL = [
    {"id": "obs-0001", "quantity": "elder_state_size", "population": {"source": "elder.jsonl"},
     "observed_at": "2026-03-31", "value": {"cycle": 1, "state_bytes": 12}, "instrument": {"name": "x"}},
    {"id": "obs-0002", "quantity": "elder_state_size", "population": {"source": "elder.jsonl"},
     "observed_at": "2026-04-02", "value": {"cycle": 2, "state_bytes": 900}, "instrument": {"name": "x"}},
    {"id": "obs-0003", "quantity": "fossil_rate", "population": {"edition": "2025"},
     "observed_at": "2025-04-01", "value": {"share": 0.272, "P3": [1675, 6158], "tag": "resolves"},
     "instrument": {"name": "scripts/measure_fossils.py"}, "derived_from": ["obs-0001"]},
]
EPOCHS = {"obs-0001": 1, "obs-0002": 1, "obs-0003": 2}


def test_skeleton_keeps_structure_not_names():
    sk = skeleton(REAL, EPOCHS)
    assert [s["epoch"] for s in sk] == [1, 1, 2]
    assert sk[0]["identity"][:2] == sk[1]["identity"][:2]          # same quantity+population
    assert sk[0]["identity"][2] < sk[1]["identity"][2]             # observation order kept
    assert sk[2]["derived_from"] == [0]


def test_generated_world_leaks_no_real_string():
    world = generate(REAL, EPOCHS, seed=7)
    rendered = json.dumps(world)
    for s in ["elder", "fossil", "measure_fossils", "resolves", "share", "state_bytes",
              "2025", "2026", "edition", "obs-000"]:
        assert s not in rendered, s


def test_values_keep_shape_and_constraints():
    world = generate(REAL, EPOCHS, seed=7)
    v = world[2]["value"]
    assert len(v) == 3
    frac = [x for x in v.values() if isinstance(x, float)][0]
    pair = [x for x in v.values() if isinstance(x, list)][0]
    assert 0 <= frac <= 1 and len(str(frac).split(".")[1]) <= 3
    assert pair[0] <= pair[1] and 1000 <= pair[1] < 10000
    assert [x for x in v.values() if isinstance(x, str)][0] != "resolves"


def test_same_seed_same_world_and_different_seeds_differ():
    assert generate(REAL, EPOCHS, seed=7) == generate(REAL, EPOCHS, seed=7)
    assert generate(REAL, EPOCHS, seed=7) != generate(REAL, EPOCHS, seed=8)


def test_repeated_quantity_keeps_one_token_within_a_world():
    world = generate(REAL, EPOCHS, seed=3)
    assert world[0]["quantity"] == world[1]["quantity"] != world[2]["quantity"]
    assert world[0]["observed_at"] < world[1]["observed_at"]


def _strings(x, out):
    if isinstance(x, str):
        out.add(x)
    elif isinstance(x, dict):
        for k, v in x.items():
            out.add(k)
            _strings(v, out)
    elif isinstance(x, list):
        for v in x:
            _strings(v, out)
    return out


def test_no_real_ledger_string_survives_generation():
    real = [json.loads(line) for line in Path("ledger/observations.jsonl").read_text().splitlines()]
    epochs = ledger_epochs(real)
    assert max(epochs.values()) == 22
    found = set()
    for r in real:
        _strings({k: r[k] for k in ("quantity", "population", "observed_at", "value", "instrument")}, found)
    # schema names are shared by design; digit strings (section numbers) can recur by chance
    real_strings = [x for x in found if len(x) >= 4 and x not in SCHEMA
                    and not x.replace(".", "").isdigit()]
    for seed in range(5):
        rendered = json.dumps(generate(real, epochs, seed))
        assert [x for x in real_strings if x in rendered] == []
