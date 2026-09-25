"""Stub-backend gates for the pilot harness (design: 'Gates before any model run').

Needs Hamut'ay: run with ``uv run --with-editable ../hamutay pytest tests/test_investigator.py``.
"""

import hashlib
import json
from pathlib import Path

import pytest

pytest.importorskip("hamutay.taste_open")

from levadura_salvaje import investigator as inv  # noqa: E402
from levadura_salvaje.ledger_tool import LedgerTool  # noqa: E402
from levadura_salvaje.worlds import generate, ledger_epochs, plant  # noqa: E402

REAL = [json.loads(line) for line in Path("ledger/observations.jsonl").read_text().splitlines()]
WORLD, PROBES = plant(generate(REAL, ledger_epochs(REAL), 0), 0)
EPOCHS = 8


def live_run(log: Path, probe_each_epoch: bool) -> list[dict]:
    s = inv.session(inv.StubBackend(), log)
    # make involuntary memory fire often, identically in both runs, so the gate
    # has draws that a leaking probe could disturb
    s._memory_base_prob = 0.5
    for epoch in range(1, EPOCHS + 1):
        inv.reseed(0, "P.Q", epoch)
        with inv.arm_tools(LedgerTool(WORLD, epoch), memory_tools=True):
            s.exchange(inv.wake_message(WORLD, epoch, False))
        if probe_each_epoch:
            before = hashlib.sha256(log.read_bytes()).hexdigest()
            p = next(p for p in PROBES if p["epoch"] >= 6) if epoch >= 6 else None
            probe = p or {"quantity": WORLD[0]["quantity"], "population": WORLD[0]["population"],
                          "observed_at": WORLD[0]["observed_at"], "field": []}
            got = inv.probe_in_subprocess({
                "world": WORLD, "probe": probe, "epoch": epoch, "persistent": True,
                "in_context": False, "live_log": str(log), "after_cycle": s.cycle,
                "probe_log": str(log.with_suffix(f".probe{epoch}.jsonl")),
                "seed_parts": [0, "P.Q", epoch, 0]})
            assert got["answer"] == {"abstain": True}
            assert hashlib.sha256(log.read_bytes()).hexdigest() == before
    return inv.read_log(log)


def test_probing_does_not_perturb_the_live_run(tmp_path):
    plain = live_run(tmp_path / "plain.jsonl", probe_each_epoch=False)
    probed = live_run(tmp_path / "probed.jsonl", probe_each_epoch=True)
    key = lambda recs: [(r["cycle"], json.dumps(r.get("memory_injection"), sort_keys=True),
                         hashlib.sha256(json.dumps(r.get("prior_state"), sort_keys=True).encode()).hexdigest())
                        for r in recs]
    assert key(plain) == key(probed)
    # the gate is only meaningful if involuntary memory actually fired somewhere
    assert any(r.get("memory_injection") for r in plain)


def test_snapshot_renders_what_the_live_session_would(tmp_path):
    log = tmp_path / "live.jsonl"
    live = inv.StubBackend()
    s = inv.session(live, log)
    for epoch in range(1, EPOCHS + 1):
        inv.reseed(0, "P.Q", epoch)
        with inv.arm_tools(LedgerTool(WORLD, epoch), memory_tools=True):
            s.exchange(inv.wake_message(WORLD, epoch, False))
    nxt = inv.wake_message(WORLD, EPOCHS + 1, False)
    forced = None  # hold involuntary memory identical: none in both
    snap_backend = inv.StubBackend()
    snap = inv.snapshot(snap_backend, log, s.cycle, None)
    assert snap.state == s.state
    with inv.arm_tools(LedgerTool(WORLD, EPOCHS + 1), memory_tools=True):
        s.exchange(nxt, force_memory=forced)
        snap.exchange(nxt, force_memory=forced)
    assert snap_backend.seen[-1] == live.seen[-1]


def test_snapshot_after_a_failed_wake_matches_the_live_session(tmp_path):
    log = tmp_path / "live.jsonl"
    live = inv.StubBackend()
    s = inv.session(live, log)
    for epoch in range(1, 6):
        inv.reseed(0, "P.Q", epoch)
        msg = inv.wake_message(WORLD, epoch, False)
        with inv.arm_tools(LedgerTool(WORLD, epoch), memory_tools=True):
            if epoch == 3:
                with pytest.raises(RuntimeError):
                    s.exchange(msg + " FAIL-THIS-WAKE")
            s.exchange(msg)
    assert sum(r.get("status") == "failed" for r in inv.read_log(log)) == 1
    snap_backend = inv.StubBackend()
    snap = inv.snapshot(snap_backend, log, s.cycle, None)
    assert snap.state == s.state
    # the history recall and involuntary memory draw from must match too
    history = lambda sess: [(c, st) for c, _, st, _ in sess._prior_states]
    assert history(snap) == history(s)
    nxt = inv.wake_message(WORLD, 6, False)
    with inv.arm_tools(LedgerTool(WORLD, 6), memory_tools=True):
        s.exchange(nxt, force_memory=None)
        snap.exchange(nxt, force_memory=None)
    assert snap_backend.seen[-1] == live.seen[-1]
