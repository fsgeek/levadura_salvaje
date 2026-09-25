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


def S(status, value=None, source=None):
    return {"status": status, "value": value, "source": source}


@pytest.mark.parametrize("given, expected", [
    ({"value": 0.30, "source_id": "w-06"}, S("answered", "current", "current")),
    ({"value": 0.30, "source_id": "w-05"}, S("answered", "current", "replaced")),  # provenance only
    ({"value": 0.25, "source_id": "w-03"}, S("answered", "obsolete", "replaced")),
    ({"value": 0.25, "source_id": "w-06"}, S("answered", "obsolete", "current")),
    ({"value": 0.99, "source_id": "w-06"}, S("answered", "other", "current")),
    ({"value": 0.99, "source_id": "w-03"}, S("answered", "other", "replaced")),    # invented, not recalled
    ({"abstain": True}, S("abstain")),
])
def test_score_at_epoch_4(given, expected):
    assert score(WORLD, 4, "Q2", "P1", "t1", given) == expected


def test_withdrawal_scoring():
    assert score(WORLD, 5, "Q1", "P1", "t2", {"withdrawn": True, "source_id": "w-07"}) == \
        S("answered", "current", "current")
    assert score(WORLD, 5, "Q1", "P1", "t2", {"value": 12, "source_id": "w-02"}) == \
        S("answered", "obsolete", "replaced")
    assert score(WORLD, 5, "Q1", "P1", "t2", {"abstain": True}) == S("abstain")


@pytest.mark.parametrize("given", [
    {"value": True, "source_id": "w-01"},          # True == 1 in Python; not here (review 3)
    {"value": None, "source_id": "w-07"},          # a null value is not a withdrawal (review 3)
    {"value": "10", "source_id": "w-01"},
    {"withdrawn": False, "source_id": "w-07"},
    {"value": 10},
    {"abstain": False},
    {"value": 10, "source_id": "w-01", "extra": 1},
    None, 12, [], "10",                             # valid JSON, not answers (review 4)
])
def test_malformed_answers_are_invalid_not_scored(given):
    assert score(WORLD, 5, "Q1", "P1", "t1", given) == S("invalid")


def test_bool_never_matches_a_numeric_key():
    world = [e("b-1", 1, "Q", "P", "t", 1)]
    assert score(world, 1, "Q", "P", "t", {"value": True, "source_id": "b-1"}) == S("invalid")
    assert score(world, 1, "Q", "P", "t", {"value": 1.0, "source_id": "b-1"}) == \
        S("answered", "current", "current")


def test_earlier_valid_observation_is_other_not_obsolete_for_latest():
    # latest Q1/P1 is t2, withdrawn at epoch 5; t1's value was never replaced
    assert score(WORLD, 5, "Q1", "P1", None, {"value": 10, "source_id": "w-01"}) == \
        S("answered", "other", "other")
    assert score(WORLD, 5, "Q1", "P1", None, {"value": 12, "source_id": "w-02"}) == \
        S("answered", "obsolete", "replaced")


def test_probe_names_one_field_inside_a_nested_value():
    world = [e("n-1", 1, "Q9", "P9", "t1", {"K1": [4, 10], "K2": 0.5}),
             e("n-2", 2, "Q9", "P9", "t1", {"K1": [5, 10], "K2": 0.5}, supersedes="n-1")]
    assert answer(world, 1, "Q9", "P9", "t1", ("K1", 0)) == {"value": 4, "source_id": "n-1"}
    assert answer(world, 2, "Q9", "P9", "t1", ("K1", 0)) == {"value": 5, "source_id": "n-2"}
    assert score(world, 2, "Q9", "P9", "t1", {"value": 4, "source_id": "n-2"}, ("K1", 0)) == \
        S("answered", "obsolete", "current")
    # K2 did not change: the old source is a provenance error only
    assert score(world, 2, "Q9", "P9", "t1", {"value": 0.5, "source_id": "n-1"}, ("K2",)) == \
        S("answered", "current", "replaced")
