"""Spike 2 acceptance (spikes/SPIKE2-BRIEF.md, items 1-3). Runs against the tenant's
`levadura_test` database, which it truncates. Skipped when the tenant isn't set up.

    uv run pytest spikes/plumbing2 -v
"""

import json
import math
import random

import pytest

from levadura_salvaje.tenant import CONFIG

pytestmark = pytest.mark.skipif(not CONFIG.exists(), reason="tenant not set up (scripts/tenant_setup.py)")

import fixture as fx  # noqa: E402
import index as ix  # noqa: E402

PINNED = json.loads(fx.EXPECTED.read_text())
ME = "levadura-owner-2026-09-29"


@pytest.fixture(scope="module")
def db():
    from levadura_salvaje.tenant import connect
    d = connect("test")
    ix.ensure(d)
    ix.truncate(d)
    return d


@pytest.fixture(scope="module")
def m1(db):
    return ix.publish(db, fx.STREAM, fx.SNAPSHOT, fx.generation(1), ME)


def as_map(cited_pairs):
    return {t: o for t, o in cited_pairs}


def check_cell(db, m, cell, exp, limit=ix.PAGE) -> list[str]:
    """Rollup, unpaged query and concatenated pages, each compared to the pinned ids."""
    bad = []
    st = ix.rollup(db, m, cell)
    for k in ("units", "occurrences", "broken", "members"):
        if st[k] != exp[k]:
            bad.append(f"{cell} rollup {k}")
    if as_map(st["cited"]) != exp["cited"]:
        bad.append(f"{cell} rollup cited")
    if ix.unpaged(db, m, cell) != exp["members"]:
        bad.append(f"{cell} unpaged")
    pages = ix.drill_all(db, m, cell, limit=limit)
    if [u for p in pages for u in p["page"]] != exp["members"]:
        bad.append(f"{cell} pages")
    n = len(exp["members"])
    if len(pages) != max(1, math.ceil(n / limit)):
        bad.append(f"{cell} page count {len(pages)}")
    seen = 0
    for i, p in enumerate(pages):
        seen += p["returned"]
        if p["population_total"] != n or p["denominator"] != exp["units"]:
            bad.append(f"{cell} page {i} totals")
        if p["returned"] != len(p["page"]) or p["truncated"] != (seen < n):
            bad.append(f"{cell} page {i} truncated={p['truncated']} with {n - seen} left")
    return bad


# --- 1. the fixture is what it claims -------------------------------------------

def test_fixture_is_pinned():
    for g in (1, 2):
        assert fx.expected(fx.generation(g)) == PINNED[str(g)]
    sizes = {c: len(v["members"]) for c, v in PINNED["1"]["cells"].items()}
    assert sizes == {"c00": 0, "c39": 39, "c40": 40, "c41": 41, "c80": 80, "swapA": 3, "swapB": 3}
    assert PINNED["1"]["top"]["conflicts"] == ["T-conf-in", "T-conf-x"]
    assert PINNED["2"]["top"]["conflicts"] == ["T-conf-x"]


# --- per cell, three ways, at every page boundary ---------------------------------

@pytest.mark.parametrize("cell", sorted(PINNED["1"]["cells"]))
def test_cell_three_ways(db, m1, cell):
    assert check_cell(db, m1, cell, PINNED["1"]["cells"][cell]) == []


@pytest.mark.parametrize("limit", [1, 3, 39, 40, 41, 80, 81])
def test_other_page_sizes(db, m1, limit):
    for cell in ("c40", "c41", "c80"):
        assert check_cell(db, m1, cell, PINNED["1"]["cells"][cell], limit=limit) == []


def test_every_page_is_a_query_event(db, m1):
    before = db.collection("queries").count()
    pages = ix.drill_all(db, m1, "c80", limit=40)
    events = list(db.aql.execute("FOR q IN queries SORT q.at DESC LIMIT @n RETURN q", bind_vars={"n": len(pages)}))
    assert db.collection("queries").count() == before + len(pages) == before + 2
    assert sorted(u for e in events for u in e["returned"]) == PINNED["1"]["cells"]["c80"]["members"]
    assert {(e["spec"], e["manifest"], e["cell"]) for e in events} == {(ix.SPEC, m1, "c80")}


# --- merges ---------------------------------------------------------------------

def test_merge_is_order_independent_and_reports_conflicts(db, m1):
    states = list(ix.cell_states(db, m1).values())
    top = PINNED["1"]["top"]
    rng = random.Random(0)
    results = []
    for _ in range(50):
        rng.shuffle(states)
        results.append(ix.merge(states))
    assert all(r == results[0] for r in results)
    r = results[0]
    assert r["members"] == top["members"]
    assert r["conflicts"] == top["conflicts"] == ["T-conf-in", "T-conf-x"]
    assert len(r["cited"]) == top["cited_distinct"] == 128
    assert sum(len(s["cited"]) for s in states) == top["naive_sum_of_cell_distinct"] == 141
    assert r["cited"]["T-conf-x"] == ["absent-section", "in-force"]


def test_merge_refuses_a_unit_in_two_cells(db, m1):
    s = ix.cell_states(db, m1)
    forged = dict(s["swapB"], members=s["swapB"]["members"] + ["s-01"])
    with pytest.raises(ix.MergeConflict):
        ix.merge([s["swapA"], forged])


# --- 2. honest paging: cursors ----------------------------------------------------

def test_cursors_are_bound_and_signed(db, m1):
    p = ix.drill(db, m1, "c80")
    assert p["truncated"] and p["cursor"]
    with pytest.raises(ix.CursorRejected):
        ix.drill(db, m1, "c41", cursor=p["cursor"])  # wrong cell
    body, sig = p["cursor"].rsplit(".", 1)
    forged = json.loads(ix.base64.urlsafe_b64decode(body)) | {"cell": "c41"}
    forged_body = ix.base64.urlsafe_b64encode(json.dumps(forged, sort_keys=True).encode()).decode()
    with pytest.raises(ix.CursorRejected):
        ix.drill(db, m1, "c41", cursor=forged_body + "." + sig)  # rebound without the key
    for junk in ("", "x", "x.y", p["cursor"] + "0"):
        with pytest.raises(ix.CursorRejected):
            ix.drill(db, m1, "c80", cursor=junk)
    with pytest.raises(ix.Unpublished):
        ix.drill(db, "no-such-manifest", "c80")


# --- 3. manifests really pinned -----------------------------------------------------

def test_correction_published_while_paging(db, m1):
    first = ix.drill(db, m1, "c80")
    m2 = ix.publish(db, fx.STREAM, fx.SNAPSHOT, fx.generation(2), ME)
    assert m2 != m1
    cur = ix.current(db, fx.STREAM)
    assert cur["_key"] == m2 and cur["supersedes"] == m1 and cur["seq"] == 2
    # the old cursor finishes the old answer, with the old denominators
    rest = ix.drill(db, m1, "c80", cursor=first["cursor"])
    assert first["page"] + rest["page"] == PINNED["1"]["cells"]["c80"]["members"]
    assert (rest["population_total"], rest["denominator"], rest["truncated"]) == (80, 82, False)
    with pytest.raises(ix.CursorRejected):
        ix.drill(db, m2, "c80", cursor=first["cursor"])  # an m1 cursor can't page m2
    for g, m in (("1", m1), ("2", m2)):
        for cell, exp in PINNED[g]["cells"].items():
            assert check_cell(db, m, cell, exp) == [], (g, cell)
        assert ix.merge(list(ix.cell_states(db, m).values()))["conflicts"] == PINNED[g]["top"]["conflicts"]


def test_publication_is_atomic_and_retryable(db, m1):
    rows = fx.generation(2)
    rows[0]["occurrences"].append(fx.occ("T-late", "repealed", "repealed"))  # c00 gains its first member
    before = ix.current(db, fx.STREAM)
    with pytest.raises(SystemExit):
        ix.publish(db, fx.STREAM, fx.SNAPSHOT, rows, ME, fail_before_manifest=True)
    m3 = ix.manifest_id(fx.STREAM, fx.SNAPSHOT, rows)
    assert ix.current(db, fx.STREAM)["_key"] == before["_key"]
    assert db.collection("units").find({"manifest": m3}).count() > 0  # data landed ...
    with pytest.raises(ix.Unpublished):
        ix.drill(db, m3, "c00")  # ... and nothing answers for it
    with pytest.raises(ix.Unpublished):
        ix.rollup(db, m3, "c00")
    assert ix.publish(db, fx.STREAM, fx.SNAPSHOT, rows, ME) == m3
    assert ix.current(db, fx.STREAM)["seq"] == before["seq"] + 1
    assert ix.drill(db, m3, "c00")["page"] == ["c00-000"]
    assert check_cell(db, m1, "c00", PINNED["1"]["cells"]["c00"]) == []


def test_republish_is_a_no_op(db, m1):
    counts = {c: db.collection(c).count() for c in ("manifests", "units", "occurrences", "assertions", "rollups")}
    assert ix.publish(db, fx.STREAM, fx.SNAPSHOT, fx.generation(1), ME) == m1
    assert {c: db.collection(c).count() for c in counts} == counts


def test_manifest_carries_tiksi_provenance(db, m1):
    p = db.collection("manifests").get(m1)["provenance"]
    assert p["author_instance_id"] == ME and p["authorship_verified"] is False
    assert p["interface_version"] == "levadura.plumbing2.v1"


# --- the checks are not vacuous: each catches the fault it names --------------------

def test_swapped_membership_is_caught_per_cell_not_globally(db, m1):
    m = ix.publish(db, "fixture-mutant", fx.SNAPSHOT, fx.generation(1), ME)
    db.aql.execute("""FOR x IN assertions FILTER x.manifest == @m AND x.unit IN ["s-01", "s-02"]
                      UPDATE x WITH {cell: x.unit == "s-01" ? "swapB" : "swapA"} IN assertions""",
                   bind_vars={"m": m})
    db.aql.execute("FOR r IN rollups FILTER r.manifest == @m REMOVE r IN rollups", bind_vars={"m": m})
    for cell, st in ix.cell_states(db, m).items():
        db.collection("rollups").insert({"_key": ix.key("rollup", ix.SPEC, m, cell), "manifest": m,
                                         "spec": ix.SPEC, "cell": cell, "state": st})
    exp = PINNED["1"]
    # a global oracle passes: same member set, same member count per cell
    assert ix.merge(list(ix.cell_states(db, m).values()))["members"] == exp["top"]["members"]
    assert [len(ix.unpaged(db, m, c)) for c in ("swapA", "swapB")] == [3, 3]
    # the per-cell check does not
    for cell in ("swapA", "swapB"):
        bad = check_cell(db, m, cell, exp["cells"][cell])
        assert {f"{cell} rollup members", f"{cell} unpaged", f"{cell} pages"} <= set(bad)


def test_spike1_truncation_rule_is_caught(db, m1, monkeypatch):
    """Spike 1 set truncated = (returned == limit). Injected into drill, check_cell must fail
    exactly where a cell ends on a page boundary (c40, c80), and nowhere else."""
    real = ix.drill

    def spike1_drill(d, m, cell, cursor=None, limit=ix.PAGE, instance="anonymous"):
        p = real(d, m, cell, cursor=cursor, limit=limit, instance=instance)
        if p["returned"] == limit and not p["truncated"]:
            binding = {"spec": ix.SPEC, "manifest": m, "cell": cell, "order": ix.ORDER}
            p = p | {"truncated": True, "cursor": ix.encode_cursor(binding | {"after": p["page"][-1]})}
        return p

    monkeypatch.setattr(ix, "drill", spike1_drill)
    caught = {c for c, exp in PINNED["1"]["cells"].items() if check_cell(db, m1, c, exp)}
    assert caught == {"c40", "c80"}
    assert "c40 page count 2" in check_cell(db, m1, "c40", PINNED["1"]["cells"]["c40"])


def test_spike1_last_wins_merge_is_caught(db, m1):
    """Spike 1 merged {target: outcome} with MERGE/update: the distinct count survives, but the
    surviving outcome of a conflicted target depends on merge order, and no conflict is reported."""
    states = list(ix.cell_states(db, m1).values())
    rng, survivors = random.Random(1), set()
    for _ in range(50):
        rng.shuffle(states)
        last_wins = {}
        for st in states:
            for t, outcomes in st["cited"]:
                last_wins[t] = outcomes[-1]
        assert len(last_wins) == PINNED["1"]["top"]["cited_distinct"]  # the count still matches
        survivors.add(last_wins["T-conf-x"])
    assert survivors == {"absent-section", "in-force"}  # the answer depends on order


# --- the resolver rule the real corpus never exercises ----------------------------------

def test_any_in_force_version_keeps_an_address_in_force():
    """At 119-4 no cited address has versions that disagree on status, so real-data agreement
    with resolve.py can't vouch for this rule (run_real.py: first-version-wins changes 0 outcomes)."""
    import corpus as cx
    r = cx.IndexResolver.__new__(cx.IndexResolver)
    r.ranges = []
    r.rows = {"9": [{"key": "p0", "status": None, "position": 0}],
              "9/a": [{"key": "p1", "status": "repealed", "position": 1},
                      {"key": "p2", "status": None, "position": 2}],
              "9/b": [{"key": "p3", "status": "repealed", "position": 3},
                      {"key": "p4", "status": "repealed", "position": 4}]}
    assert r.resolve("9/a") == {"outcome": "resolves", "targets": ["p1", "p2"]}
    assert r.resolve("9/b") == {"outcome": "repealed", "targets": ["p3", "p4"]}
    assert r.resolve("9/c")["outcome"] == "absent-subdivision"
    assert r.resolve("10")["outcome"] == "absent-section"
