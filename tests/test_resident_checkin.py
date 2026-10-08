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
