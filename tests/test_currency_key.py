"""The answer key for the record-currency pilot (docs/investigator-design.md).

A hand-worked world covering every case in the design's Semantics section:
repeated measurement, replacement (and chains), equal-value replacement,
withdrawal, and derived entries left untouched by changes to their inputs.
"""

import pytest

from levadura_salvaje.currency_key import answer, score


def e(id, epoch, q, p, t, value=None, supersedes=None, withdraws=None, derived_from=()):
    return {"id": id, "epoch": epoch, "quantity": q, "population": p, "observed_at": t,
            "value": value, "supersedes": supersedes, "withdraws": withdraws,
            "derived_from": list(derived_from)}


WORLD = [
    e("w-01", 1, "Q1", "P1", "t1", 10),
    e("w-02", 1, "Q1", "P1", "t2", 12),                       # repeated: a later fact, not a replacement
    e("w-03", 1, "Q2", "P1", "t1", 0.25),
    e("w-04", 2, "Q3", "P2", "t1", [3, 9], derived_from=["w-03"]),
    e("w-05", 3, "Q2", "P1", "t1", 0.30, supersedes="w-03"),   # replacement, changed value
    e("w-06", 4, "Q2", "P1", "t1", 0.30, supersedes="w-05"),   # chain, equal value
    e("w-07", 5, "Q1", "P1", "t2", withdraws="w-02"),          # withdrawal, no replacement
]


@pytest.mark.parametrize("epoch, q, p, t, expected", [
    (1, "Q1", "P1", "t1", {"value": 10, "source_id": "w-01"}),
    (1, "Q1", "P1", "t2", {"value": 12, "source_id": "w-02"}),
    (1, "Q1", "P1", None, {"value": 12, "source_id": "w-02"}),     # latest observed
    (2, "Q2", "P1", "t1", {"value": 0.25, "source_id": "w-03"}),   # replacement not yet revealed
    (3, "Q2", "P1", "t1", {"value": 0.30, "source_id": "w-05"}),
    (4, "Q2", "P1", "t1", {"value": 0.30, "source_id": "w-06"}),   # equal value, new source
    (5, "Q1", "P1", "t2", {"withdrawn": True, "source_id": "w-07"}),
    (5, "Q1", "P1", None, {"withdrawn": True, "source_id": "w-07"}),  # latest observed is withdrawn
    (5, "Q1", "P1", "t1", {"value": 10, "source_id": "w-01"}),     # the earlier fact still stands
    (5, "Q3", "P2", "t1", {"value": [3, 9], "source_id": "w-04"}), # derived entry untouched
])
def test_answer_key(epoch, q, p, t, expected):
    assert answer(WORLD, epoch, q, p, t) == expected


def test_unrevealed_identity_has_no_answer():
    assert answer(WORLD, 1, "Q3", "P2", "t1") is None


@pytest.mark.parametrize("given, expected", [
    ({"value": 0.30, "source_id": "w-06"}, "correct"),
    ({"value": 0.30, "source_id": "w-05"}, "stale"),      # right number, replaced source
    ({"value": 0.25, "source_id": "w-03"}, "stale"),
    ({"value": 0.25, "source_id": "w-06"}, "stale"),      # replaced value under a current id
    ({"value": 0.99, "source_id": "w-06"}, "wrong"),
    ({"abstain": True}, "abstain"),
])
def test_score_at_epoch_4(given, expected):
    assert score(WORLD, 4, "Q2", "P1", "t1", given) == expected


def test_withdrawal_scoring():
    assert score(WORLD, 5, "Q1", "P1", "t2", {"withdrawn": True, "source_id": "w-07"}) == "correct"
    assert score(WORLD, 5, "Q1", "P1", "t2", {"value": 12, "source_id": "w-02"}) == "stale"
    assert score(WORLD, 5, "Q1", "P1", "t2", {"abstain": True}) == "abstain"


def test_earlier_valid_observation_is_wrong_not_stale_for_latest():
    # latest Q1/P1 is t2, withdrawn at epoch 5; t1's value was never replaced
    assert score(WORLD, 5, "Q1", "P1", None, {"value": 10, "source_id": "w-01"}) == "wrong"
    assert score(WORLD, 5, "Q1", "P1", None, {"value": 12, "source_id": "w-02"}) == "stale"
