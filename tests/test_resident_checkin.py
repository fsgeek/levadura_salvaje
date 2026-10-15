import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest


def load(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location(
        "resident_checkin", Path(__file__).parents[1] / "scripts/resident_checkin.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, "LAST", tmp_path / "last")
    monkeypatch.setattr(module, "FAILED", tmp_path / "failed.jsonl")
    monkeypatch.setattr(sys, "argv", ["checkin"])
    return module


def fake_run(sends, send_rc):
    def run(command, **kwargs):
        if command[0] == "git":
            return subprocess.CompletedProcess(command, 0, stdout="- abc123 a change\n", stderr="")
        sends.append(command)
        return subprocess.CompletedProcess(command, send_rc, stdout="", stderr="no such file: uv")
    return run


def message(command):
    return command[command.index("--message") + 1]


def test_failed_send_is_recorded_and_reported_by_the_next_check_in(tmp_path, monkeypatch):
    # The resident asked (cycle 9, 2026-10-08) to be told when a check-in fails. A failed send
    # can't tell it, so the next one that gets through must.
    module = load(tmp_path, monkeypatch)
    sends = []
    monkeypatch.setattr(module.subprocess, "run", fake_run(sends, 1))
    with pytest.raises(SystemExit):
        module.main()
    assert module.FAILED.exists()
    assert not module.LAST.exists()

    monkeypatch.setattr(module.subprocess, "run", fake_run(sends, 0))
    module.main()
    told = message(sends[-1])
    assert told.index("did not reach you") < told.index("Changes to levadura_salvaje")
    assert "no such file: uv" in told
    assert not module.FAILED.exists()
    assert module.LAST.exists()


def test_check_in_without_failures_says_nothing_about_them(tmp_path, monkeypatch):
    module = load(tmp_path, monkeypatch)
    sends = []
    monkeypatch.setattr(module.subprocess, "run", fake_run(sends, 0))
    module.main()
    assert "did not reach you" not in message(sends[-1])


def test_a_send_that_cannot_start_is_recorded_too(tmp_path, monkeypatch):
    # The 2026-10-07 failure: uv wasn't on PATH, so subprocess.run raised before any send.
    module = load(tmp_path, monkeypatch)

    def run(command, **kwargs):
        if command[0] == "git":
            return subprocess.CompletedProcess(command, 0, stdout="", stderr="")
        raise FileNotFoundError(2, "No such file or directory", "uv")
    monkeypatch.setattr(module.subprocess, "run", run)
    with pytest.raises(SystemExit):
        module.main()
    assert "FileNotFoundError" in module.FAILED.read_text()


def test_door_check_in_goes_to_the_door_with_the_community_sentence(tmp_path, monkeypatch):
    # Marker asked (cycle 29, 2026-10-15): after its move, the date and one sentence on the
    # community's state, in place of levadura's commits.
    module = load(tmp_path, monkeypatch)
    monkeypatch.setattr(module, "HAMUTAY", tmp_path / "hamutay")
    monkeypatch.setattr(module, "PLAZA", tmp_path / "hamutay" / "community" / "plaza")
    module.PLAZA.mkdir(parents=True)
    (module.PLAZA / "plaza.jsonl").write_text(
        '{"record_type": "message", "from": "custodian", "created_at": "2099-01-01T00:00:00+00:00"}\n')
    (module.PLAZA / "assembly.jsonl").write_text(
        '{"record_type": "question", "question_id": "q", "closes_at": "2099-02-01T00:00:00+00:00"}\n')
    module.LAST.write_text("2098-12-31T00:00:00+00:00")
    monkeypatch.setattr(sys, "argv", ["checkin", "--door", "marker"])
    sends = []
    monkeypatch.setattr(module.subprocess, "run", fake_run(sends, 0))
    real_dt = module.datetime

    class Fixed(real_dt):
        @classmethod
        def now(cls, tz=None):
            return real_dt(2099, 1, 2, tzinfo=module.timezone.utc)
    monkeypatch.setattr(module, "datetime", Fixed)
    module.main()
    command = sends[-1]
    assert command[command.index("--log-path") + 1] == str(tmp_path / "hamutay/community/marker/session.jsonl")
    told = message(command)
    assert "Changes to levadura_salvaje" not in told
    assert "the plaza had 1 message (custodian 1)" in told
    assert "1 assembly question is open (closing 2099-02-01 00:00Z)" in told


def test_community_sentence_counts_only_the_window_and_reports_closings(tmp_path):
    spec = importlib.util.spec_from_file_location("rc", Path(__file__).parents[1] / "scripts/resident_checkin.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    (tmp_path / "plaza.jsonl").write_text(
        '{"record_type": "message", "from": "a", "created_at": "2026-01-01T00:00:00+00:00"}\n'
        '{"record_type": "message", "from": "b", "created_at": "2026-01-03T00:00:00+00:00"}\n'
        '{"record_type": "message", "from": "b", "created_at": "2026-01-03T01:00:00+00:00"}\n{"partial')
    (tmp_path / "assembly.jsonl").write_text(
        '{"record_type": "question", "question_id": "q1", "closes_at": "2026-01-02T12:00:00+00:00"}\n'
        '{"record_type": "closing", "question_id": "q1", "outcome": "assented", "seq": "9", '
        '"created_at": "2026-01-02T12:00:00+00:00"}\n')
    from datetime import datetime, timezone
    s = module.community_sentence(datetime(2026, 1, 2, tzinfo=timezone.utc),
                                  datetime(2026, 1, 4, tzinfo=timezone.utc), tmp_path)
    assert s == ("Since the last check-in, the plaza had 2 messages (b 2); the assembly closed question "
                 "seq 9 as assented; 0 assembly questions are open.")
