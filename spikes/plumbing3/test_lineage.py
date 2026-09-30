"""Spike 3 acceptance: delta generations answer exactly as full copies would.

The oracle is spikes/plumbing2/fixture.expected(rows), plain Python over the rows each
generation intends to hold. It shares nothing with lineage.py. Runs against the tenant's
`levadura_test` database, which it truncates.

    uv run pytest spikes/plumbing3 -v
"""

import copy
import math
import random
import sys
from pathlib import Path

import pytest

from levadura_salvaje.tenant import CONFIG

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "plumbing2"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fixture as fx  # noqa: E402
import index as ix  # noqa: E402
import lineage as lx  # noqa: E402

ME = "levadura-owner-2026-09-30"


@pytest.fixture(scope="module")
def db():
    if not CONFIG.exists():
        pytest.skip("tenant not set up (scripts/tenant_setup.py)")
    from levadura_salvaje.tenant import connect
    d = connect("test")
    lx.ensure(d)
    lx.truncate(d)
    return d


def check(db, m, rows, limit=ix.PAGE, vanished=()) -> list[str]:
    """Every cell, three ways, plus the merged top, against expected(rows). Cells in
    `vanished` must have no rollup and no state."""
    exp, bad = fx.expected(rows), []
    states = lx.cell_states(db, m)
    if sorted(states) != sorted(exp["cells"]):
        bad.append(f"cells {sorted(set(states) ^ set(exp['cells']))}")
    for cell in vanished:
        if cell in states:
            bad.append(f"{cell} vanished but has state")
        try:
            lx.rollup(db, m, cell)
            bad.append(f"{cell} vanished but has a rollup")
        except KeyError:
            pass
    for cell, e in exp["cells"].items():
        try:
            st = lx.rollup(db, m, cell)
        except KeyError:
            bad.append(f"{cell} no rollup")
            continue
        for k in ("units", "occurrences", "broken", "members"):
            if st[k] != e[k]:
                bad.append(f"{cell} rollup {k}")
        if dict(map(tuple, st["cited"])) != e["cited"]:
            bad.append(f"{cell} rollup cited")
        st2 = states.get(cell, {})
        if [st2.get(k) for k in ("units", "occurrences", "broken", "members")] != \
                [e[k] for k in ("units", "occurrences", "broken", "members")] or \
                dict(map(tuple, st2.get("cited", []))) != e["cited"]:
            bad.append(f"{cell} states")
        if lx.unpaged(db, m, cell) != e["members"]:
            bad.append(f"{cell} unpaged")
        pages = lx.drill_all(db, m, cell, limit=limit)
        if [u for p in pages for u in p["page"]] != e["members"]:
            bad.append(f"{cell} pages")
        n = len(e["members"])
        if len(pages) != max(1, math.ceil(n / limit)):
            bad.append(f"{cell} page count")
        if any(p["population_total"] != n or p["denominator"] != e["units"] for p in pages):
            bad.append(f"{cell} totals")
    top = ix.merge(list(states.values()))
    if (top["conflicts"], top["members"], top["units"], top["broken"], len(top["cited"])) != (
            exp["top"]["conflicts"], exp["top"]["members"], exp["top"]["units"], exp["top"]["broken"],
            exp["top"]["cited_distinct"]):
        bad.append("top")
    return bad


def mutate(rows: list[dict], rng: random.Random, n: int) -> list[dict]:
    """n random corrections: outcome flips, new units, deletions, moves between cells, dropped citations."""
    rows = copy.deepcopy(rows)
    cells = sorted({r["cell"] for r in rows}) + ["c-new"]
    for _ in range(n):
        op = rng.choice(["flip", "flip", "flip", "add", "delete", "move", "drop"])
        r = rng.choice(rows)
        if op == "flip":
            o = rng.choice([o for o in r["occurrences"]] or [None])
            if o and o["path"]:
                o["outcome"] = "in-force" if o["outcome"] in fx.BROKEN else rng.choice(fx.BROKEN)
                o["target_outcome"] = o["outcome"]
        elif op == "add":
            uid = f"n-{rng.randrange(10**6):06d}"
            if uid not in {x["unit"] for x in rows}:
                rows.append(fx.unit(uid, rng.choice(cells), rng.random() < 0.5, rng.randrange(30)))
        elif op == "delete" and len(rows) > 10:
            rows.remove(r)
        elif op == "move":
            r["cell"] = rng.choice(cells)
        elif op == "drop" and r["occurrences"]:
            r["occurrences"].pop()
    return rows


def written(db, m) -> dict:
    return db.collection(lx.C["manifests"]).get(m)["written"]


# --- deltas answer exactly as full copies would -----------------------------------------------

def test_first_generation_and_a_correction(db):
    g1, g2 = fx.generation(1), fx.generation(2)
    m1 = lx.publish(db, "fx", fx.SNAPSHOT, g1, ME)
    m2 = lx.publish(db, "fx", fx.SNAPSHOT, g2, ME)
    assert check(db, m1, g1) == [] and check(db, m2, g2) == []
    w = written(db, m2)
    # the correction touches c80 (5 units), c41 (a new unit) and c39 (one citation), not the corpus
    assert w["units"] == 1 and w["assertions"] <= 12 and w["retractions"] <= 12, w
    assert sorted(db.collection(lx.C["manifests"]).get(m2)["touched"]) == ["c39", "c41", "c80"]
    assert lx.publish(db, "fx", fx.SNAPSHOT, g2, ME) == m2  # no change, no new generation


def test_a_chain_of_random_corrections(db):
    """Twenty generations of random corrections; every generation stays exactly readable."""
    rng = random.Random(7)
    rows = fx.generation(1)
    chain = [(lx.publish(db, "chain", fx.SNAPSHOT, rows, ME), rows)]
    while len(chain) < 21:
        nxt = mutate(rows, rng, rng.choice([1, 3, 10]))
        if nxt == rows:
            assert lx.publish(db, "chain", fx.SNAPSHOT, nxt, ME) == chain[-1][0]  # no change, no generation
            continue
        rows = nxt
        chain.append((lx.publish(db, "chain", fx.SNAPSHOT, rows, ME), rows))
    assert len({m for m, _ in chain}) == len(chain)
    for i, (m, rows) in enumerate(chain):
        assert check(db, m, rows) == [], i
    total = sum(sum(written(db, m).values()) for m, _ in chain[1:])
    full = sum(len(v) for v in lx.slots(chain[0][1], fx.SNAPSHOT).values())
    assert total < full, (total, full)  # twenty corrections cost less than one copy


def test_correction_while_paging(db):
    rows1 = fx.generation(1)
    m1 = lx.publish(db, "paging", fx.SNAPSHOT, rows1, ME)
    first = lx.drill(db, m1, "c80")
    m2 = lx.publish(db, "paging", fx.SNAPSHOT, fx.generation(2), ME)
    rest = lx.drill(db, m1, "c80", cursor=first["cursor"])
    assert first["page"] + rest["page"] == fx.expected(rows1)["cells"]["c80"]["members"]
    assert (rest["population_total"], rest["denominator"]) == (80, 82)
    with pytest.raises(ix.CursorRejected):
        lx.drill(db, m2, "c80", cursor=first["cursor"])


@pytest.mark.parametrize("stage", [s for s in lx.STAGES if s != "commit"])
def test_a_crash_is_invisible_and_retryable(db, stage):
    stream = f"crash-{stage}"
    base = fx.generation(1)
    m1 = lx.publish(db, stream, fx.SNAPSHOT, base, ME)
    rows = mutate(base, random.Random(stage), 5)
    with pytest.raises(SystemExit):
        lx.publish(db, stream, fx.SNAPSHOT, rows, ME, crash_at=stage)
    assert lx.current(db, stream)["_key"] == m1
    assert check(db, m1, base) == []  # orphaned records and retractions don't leak into the parent
    m2 = lx.publish(db, stream, fx.SNAPSHOT, rows, ME)
    assert check(db, m2, rows) == [] and check(db, m1, base) == []


def test_concurrent_corrections_rebase(db):
    """Six corrections race from one parent. All commit, each on whatever was current, and each
    generation still reads exactly as the rows it intended."""
    from concurrent.futures import ThreadPoolExecutor
    from levadura_salvaje.tenant import connect
    stream = "race"
    base = fx.generation(1)
    lx.publish(db, stream, fx.SNAPSHOT, base, ME)
    import threading
    variants = [mutate(base, random.Random(100 + i), 4) for i in range(6)]
    barrier, local = threading.Barrier(6), threading.local()

    def hold_once():  # every publisher computes its delta against the same parent, then all commit at once
        if not getattr(local, "held", False):
            local.held = True
            barrier.wait(timeout=60)

    before = lx.REBASES
    with ThreadPoolExecutor(6) as pool:
        got = list(pool.map(lambda rows: lx.publish(connect("test"), stream, fx.SNAPSHOT, rows, ME,
                                                    before_commit=hold_once), variants))
    assert lx.REBASES - before >= 5  # one wins the first round; every other publisher lost at least once
    chain = list(db.aql.execute(f"FOR x IN {lx.C['manifests']} FILTER x.stream == @s SORT x.seq RETURN x",
                                bind_vars={"s": stream}))
    assert [x["seq"] for x in chain] == list(range(1, 8))
    assert [x["parent"] for x in chain[1:]] == [x["_key"] for x in chain[:-1]]
    assert set(got) == {x["_key"] for x in chain[1:]}
    for m, rows in zip(got, variants):
        assert check(db, m, rows) == []


# --- the oracle is not vacuous ---------------------------------------------------------------

def test_ignoring_retractions_is_caught(db, monkeypatch):
    rows1, rows2 = fx.generation(1), fx.generation(2)
    lx.publish(db, "mut-retract", fx.SNAPSHOT, rows1, ME)
    m2 = lx.publish(db, "mut-retract", fx.SNAPSHOT, rows2, ME)
    real = lx.visible
    monkeypatch.setattr(lx, "visible", lambda kind, filters="": real(kind, filters).replace(
        "AND NOT HAS(goneset, x._key)", ""))
    bad = set(check(db, m2, rows2))
    # the five retracted c80 members come back; c80's persisted rollup, written before the mutant, is still right
    assert {"c80 unpaged", "c80 pages", "c80 states", "c80 totals"} <= bad and "c80 rollup members" not in bad, bad


def test_oldest_rollup_is_caught(db, monkeypatch):
    rows1, rows2 = fx.generation(1), fx.generation(2)
    lx.publish(db, "mut-rollup", fx.SNAPSHOT, rows1, ME)
    m2 = lx.publish(db, "mut-rollup", fx.SNAPSHOT, rows2, ME)
    from arango.aql import AQL
    real_execute = AQL.execute

    def oldest(self, q, *a, **kw):
        return real_execute(self, q.replace("SORT POSITION(@anc, r.born, true) DESC",
                                            "SORT POSITION(@anc, r.born, true) ASC"), *a, **kw)

    monkeypatch.setattr(AQL, "execute", oldest)
    bad = check(db, m2, rows2)
    assert {"c80 rollup members", "c41 rollup units"} <= set(bad), bad


def test_a_large_correction_becomes_a_checkpoint(db):
    """Past CHECKPOINT of the corpus retracted since the last root, a generation is a fresh root:
    no ancestry, every slot rewritten. Older generations still read as before."""
    rng = random.Random(3)
    rows1 = fx.generation(1)
    m1 = lx.publish(db, "ckpt", fx.SNAPSHOT, rows1, ME)
    small = mutate(rows1, rng, 3)
    m2 = lx.publish(db, "ckpt", fx.SNAPSHOT, small, ME)
    big = copy.deepcopy(small)
    for r in big:
        for o in r["occurrences"]:
            if o["path"]:
                o["outcome"] = o["target_outcome"] = "in-force" if o["outcome"] in fx.BROKEN else "repealed"
    m3 = lx.publish(db, "ckpt", fx.SNAPSHOT, big, ME)
    docs = {m: db.collection(lx.C["manifests"]).get(m) for m in (m2, m3)}
    assert docs[m2]["checkpoint"] is False and docs[m3]["checkpoint"] is True
    assert docs[m3]["ancestors"] == [m3] and docs[m3]["parent"] == m2 and docs[m3]["written"]["retractions"] == 0
    for m, rows in ((m1, rows1), (m2, small), (m3, big)):
        assert check(db, m, rows) == [], m
    rows4 = mutate(big, rng, 2)
    assert rows4 != big
    m4 = lx.publish(db, "ckpt", fx.SNAPSHOT, rows4, ME)  # deltas resume on the new root
    assert db.collection(lx.C["manifests"]).get(m4)["ancestors"] == [m3, m4]
    assert check(db, m4, rows4) == []


# --- cases the random chain never reached (REVIEW.md #6) -------------------------------------

def test_cells_vanish_and_return_units_and_citations_come_back(db):
    rows1 = fx.generation(1)
    m1 = lx.publish(db, "vanish", fx.SNAPSHOT, rows1, ME)
    swap_a = [r for r in rows1 if r["cell"] == "swapA"]
    dropped = copy.deepcopy(rows1[0]["occurrences"][-1])
    rows2 = [r for r in copy.deepcopy(rows1) if r["cell"] != "swapA"]  # a whole cell disappears
    rows2[0]["occurrences"].pop()                                       # a citation is dropped
    m2 = lx.publish(db, "vanish", fx.SNAPSHOT, rows2, ME)
    assert check(db, m2, rows2, vanished=["swapA"]) == []
    rows3 = copy.deepcopy(rows2) + copy.deepcopy(swap_a)                 # the cell returns, same units, same content
    rows3[0]["occurrences"].append(dropped)                             # the citation is restored
    m3 = lx.publish(db, "vanish", fx.SNAPSHOT, rows3, ME)
    assert fx.expected(rows3) == fx.expected(rows1)
    assert check(db, m3, rows3) == [] and check(db, m2, rows2, vanished=["swapA"]) == []
    assert check(db, m1, rows1) == []


def test_paging_order_is_one_comparator(db):
    """REVIEW.md #1: sorting and continuation must agree. Ids that server collation and code
    points order differently (case, accents, a decomposed accent) must page without loss."""
    ids = ["a", "\u00e5", "b", "B", "\u00e9", "e\u0301", "z", "Z", "\u00e4", "A", "_", "~", "10", "9"]
    rows = [fx.unit(i, "uni", True, 1) for i in ids]
    m = lx.publish(db, "unicode", fx.SNAPSHOT, rows, ME)
    for limit in (1, 2, 3, 5):
        pages = lx.drill_all(db, m, "uni", limit=limit)
        assert [u for p in pages for u in p["page"]] == sorted(ids), limit  # code-point order, no loss
    assert lx.unpaged(db, m, "uni") == sorted(ids)


def test_same_rows_new_snapshot_is_a_new_generation(db):
    """REVIEW.md #2: identity covers the snapshot, not just the rows."""
    rows = fx.generation(1)
    m1 = lx.publish(db, "snap", "fx-1", rows, ME)
    m2 = lx.publish(db, "snap", "fx-2", rows, ME)
    assert m2 != m1
    got = set(db.aql.execute(f"""FOR x IN {lx.C['assertions']} FILTER x.stream == "snap" AND x.born == @m
                                 RETURN DISTINCT x.snapshot""", bind_vars={"m": m2}))
    assert got == {"fx-2"} and check(db, m2, rows) == []


def test_retry_under_a_changed_plan_is_a_new_generation(db, monkeypatch):
    """REVIEW.md #3: a crash staged under one checkpoint plan must not poison a retry under another."""
    rows1 = fx.generation(1)
    lx.publish(db, "plan", fx.SNAPSHOT, rows1, ME)
    big = copy.deepcopy(rows1)
    for r in big:
        for o in r["occurrences"]:
            if o["path"]:
                o["outcome"] = o["target_outcome"] = "in-force" if o["outcome"] in fx.BROKEN else "repealed"
    monkeypatch.setattr(lx, "CHECKPOINT", float("inf"))
    with pytest.raises(SystemExit):
        lx.publish(db, "plan", fx.SNAPSHOT, big, ME, crash_at="retractions")
    small = mutate(rows1, random.Random(9), 2)  # checkpoints off, committed: the manifest must store
    assert small != rows1                        # the disabled threshold (measure.py's first failure)
    m_off = lx.publish(db, "plan-off", fx.SNAPSHOT, rows1, ME)
    m_off2 = lx.publish(db, "plan-off", fx.SNAPSHOT, small, ME)
    assert db.collection(lx.C["manifests"]).get(m_off2)["checkpoint_threshold"] is None and m_off != m_off2
    monkeypatch.setattr(lx, "CHECKPOINT", 0.25)
    m = lx.publish(db, "plan", fx.SNAPSHOT, big, ME)
    assert db.collection(lx.C["manifests"]).get(m)["checkpoint"] is True
    assert check(db, m, big) == []


def test_duplicate_units_are_refused():
    rows = fx.generation(1)
    with pytest.raises(ValueError):
        lx.slots(rows + [copy.deepcopy(rows[0])], fx.SNAPSHOT)
